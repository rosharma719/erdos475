"""Campaign controller: the high-level loop. Runs rounds until the ROOT claim is analytically verified (only the
audit gates can set that), the budget is gone, or the system needs a human. It does not stop because a round
was disappointing: it adapts, within a fixed escalation ladder, and stops only to ask when adaptation is exhausted.

Big model: proving. Small models: direction, comparison, synthesis, bookkeeping, and THIS controller (plain code)."""
from __future__ import annotations
import json, re, yaml
from pathlib import Path
from . import context as C
from .orchestrator_v2 import Round
from .views import write_frontier_view

OVR = C.R / "contract_overrides.yaml"
LOG = C.R / "campaign_log.md"

def _load_ovr():
    return yaml.safe_load(OVR.read_text()) if OVR.exists() else {}

def _save_ovr(d):
    OVR.write_text(yaml.safe_dump(d, sort_keys=False, width=100, allow_unicode=True))

def apply_overrides(contracts):
    for k, o in _load_ovr().items():
        if k in contracts:
            contracts[k].update(o)
    return contracts

def log(msg):
    with open(LOG, "a") as f:
        f.write(msg + "\n")
    print(msg)

def run_campaign(cfg, llm, db, graph, max_rounds=10, start_contract=None, min_round_usd=2.5, stall_limit=3):
    ca = cfg.get("campaign", {})
    streak = {}                 # contract -> consecutive no-progress rounds
    empties = 0                 # consecutive rounds with no usable output at all
    total_np = 0
    contract = start_contract
    for n in range(max_rounds):
        remaining = cfg["budget"]["total_usd"] - db.spent()
        if graph.nodes[graph.root]["status"] == "analytically_verified":
            log("STOP: root verified"); return "solved"
        if remaining < min_round_usd:
            log(f"STOP: budget (${remaining:.2f} left < ${min_round_usd} per-round minimum)"); return "budget"
        pending = [k for k, v in graph.nodes.items() if v["major"] and v["audit"]["referee_accepts"] >= cfg["round"]["referee_passes_for_complete"]
                   and v["audit"]["human"] != "approved" and v["status"] not in {"analytically_verified", "refuted"}]
        if pending:
            log(f"PAUSE for human review of: {pending} (python -m engine human-approve <NODE>)"); return "human"
        o = _load_ovr()
        if o and all(v.get("status") == "cooldown" for v in o.values()) or not any(c.get("status", "open") == "open" for c in C.load_contracts().values() if c["id"] not in o):
            for v in o.values():
                v.pop("status", None) if v.get("status") == "cooldown" else None
            _save_ovr(o)
        rnd = Round(cfg, llm, db, graph, contract_id=contract)
        apply_overrides(rnd.contracts)
        d = rnd.run()
        st = rnd.state
        cid = st.get("contract")
        prog = bool(st.get("progress"))
        nxt = st.get("next", "continue")
        usable = not (d / "report.md").read_text().startswith("All branches were refused")
        streak[cid] = 0 if prog else streak.get(cid, 0) + 1
        total_np = 0 if prog else total_np + 1
        empties = 0 if usable else empties + 1
        log(f"[round {rnd.run_id}] {cid}: progress={prog} usable={usable} next={nxt} spent=${db.spent():.2f}")
        # carry the director's obstruction-breaking idea into the next round of this contract
        txt = (d / "07_reassess.md").read_text() if (d / "07_reassess.md").exists() else ""
        m = re.search(r"OBSTRUCTION_BREAKING:(.*)", txt, re.S)
        if m and cid:
            o = _load_ovr(); o.setdefault(cid, {})["obstruction_breaking"] = m.group(1).strip()[:3500]; _save_ovr(o)
        write_frontier_view(graph, C.R / "views" / "frontier.md")
        # ---- escalation ladder (code, not model whim) ----
        if empties >= 2:
            log("STOP: two rounds in a row produced no usable prover output (starved/refused). Needs a human decision on model/effort/budget."); return "starved"
        if total_np >= stall_limit:
            log(f"STOP: {total_np} consecutive rounds with no hard-target progress. Needs a human: sharper conjecture, data, or different programme."); return "stalled"
        if prog and nxt == "continue":
            contract = cid                       # keep pushing a live line
        else:
            contract = None                      # let the director choose; cool down stuck contracts
            for k, v in streak.items():
                if v >= 2 and k in rnd.contracts:
                    o = _load_ovr(); o.setdefault(k, {})["status"] = "cooldown"; _save_ovr(o)
    log("STOP: round limit"); return "limit"
