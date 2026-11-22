"""One resumable research round: direct -> literature -> prove (x approaches) -> referee -> verify -> synthesize -> reassess.

Every step writes its output to runs/<run_id>/<step>.md; re-running with --resume skips finished steps.
"""
from __future__ import annotations
import json, re, time, datetime as dt
from pathlib import Path

import yaml

from . import context as C
from .claude import LLM
from .proof_graph import ProofGraph, SOLID
from .storage import Storage, BudgetExceeded
from . import verification as V

ROOT = C.ROOT
RUNS = ROOT / "runs"


def sections(text: str) -> dict:
    parts = re.split(r"(?m)^## ", "\n" + text)
    out = {}
    for p in parts[1:]:
        head, _, body = p.partition("\n")
        out[head.split(":")[0].strip().upper()] = body.strip()
    return out


def parse_verdict(text: str) -> str:
    m = re.search(r"VERDICT:\s*(ACCEPT|REJECT|GAPS)", text)
    return m.group(1) if m else "GAPS"          # unparseable => not accepted


class Round:
    def __init__(self, cfg, llm: LLM, storage: Storage, graph: ProofGraph,
                 run_id: str | None = None, contract_id: str | None = None):
        self.cfg, self.llm, self.db, self.graph = cfg, llm, storage, graph
        self.run_id = run_id or time.strftime("%Y%m%dT%H%M%S")
        self.dir = RUNS / self.run_id
        self.dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.dir / "state.json"
        self.state = json.loads(self.state_file.read_text()) if self.state_file.exists() else {"contract": contract_id}
        self.contracts = C.load_contracts()

    # ---------- plumbing ----------
    def _save_state(self):
        self.state_file.write_text(json.dumps(self.state, indent=1))

    def call(self, role, system_name, task, web_search=False):
        b = self.cfg["budget"]
        self.db.check_budget(self.run_id, b["per_round_usd"], b["total_usd"])
        r = self.llm.complete(role=role, system=C.agent_prompt(system_name), task=task,
                              max_tokens=self.cfg["max_tokens"].get(role, 32000), web_search=web_search)
        self.db.record_call(self.run_id, role, r.model, r.usage, r.cost_usd, r.stop_reason)
        (self.dir / f"prompt_{role}_{len(list(self.dir.glob('prompt_*')))}.md").write_text(task)
        if r.refused:
            self.refusals = getattr(self, "refusals", []) + [f"{role}: {r.stop_details}"]
            return f"[REFUSED by safety classifier; no usable output from {role}] {r.stop_details}"
        if r.stop_reason == "max_tokens":
            return r.text + "\n\n[TRUNCATED: hit max_tokens — treat any unfinished argument as incomplete]"
        return r.text

    def step(self, name, fn):
        f = self.dir / f"{name}.md"
        if f.exists():
            return f.read_text()
        out = fn()
        f.write_text(out)
        self.state.setdefault("done", []).append(name)
        self._save_state()
        return out

    # ---------- the round ----------
    def run(self):
        contract_id = self.state.get("contract")
        self.db.start_run(self.run_id, contract_id or "?", None)
        try:
            self._run()
            self.db.finish_run(self.run_id, "complete", self.state.get("next", ""))
        except BudgetExceeded as e:
            self.state["paused"] = str(e)
            self._save_state()
            self.db.finish_run(self.run_id, "paused_budget", str(e))
            print(f"[paused] {e}. Resume with: python -m engine run --resume {self.run_id}")
        return self.dir

    def _run(self):
        # 1. choose the gap
        direction = self.step("01_director", self._director)
        cid = self.state.get("contract") or self._parse_contract(direction)
        self.state["contract"] = cid
        self._save_state()
        contract = self.contracts[cid]
        self.db.db.execute("UPDATE runs SET contract=?, programme=? WHERE id=?",
                           (cid, contract.get("programme"), self.run_id))
        self.db.db.commit()
        target = contract.get("target_node", cid)
        if target not in self.graph.nodes:
            self.graph.add_node(target, contract["goal"].strip(), "candidate",
                                depends_on=[k for k in contract.get("known_inputs", []) if k in self.graph.nodes],
                                programme=contract.get("programme"), source="contract")
            self.graph.save()

        # 2. existing knowledge (literature)
        lit = self.step("02_literature", lambda: self._literature(contract))

        # 3-4. prove + challenge, N genuinely different approaches
        results = []
        for i in range(1, self.cfg["round"]["approaches_per_target"] + 1):
            prev = "\n\n".join(f"Approach {r['i']} (verdict {r['verdict']}): {r['theorem'][:600]}\nIssues: {r['issues'][:1200]}"
                               for r in results)
            prover_out = self.step(f"03_prover_{i}", lambda: self._prover(contract, lit, i, prev))
            if prover_out.startswith("[REFUSED"):
                results.append(dict(i=i, theorem="", claim="refused", verdict="REFUSED", issues=prover_out, explor="", ver=""))
                continue
            sec = sections(prover_out)
            verdict, issues = self._referee_pass(contract, i, sec)
            # 5. targeted exact verification (prover's and referee's check blocks)
            ver = self.step(f"05_verification_{i}",
                            lambda: self._verify(prover_out + "\n" + (self.dir / f"04_referee_{i}.md").read_text(), i))
            results.append(dict(i=i, theorem=sec.get("THEOREM", ""), claim=sec.get("STATUS_CLAIM", "").strip().lower(),
                                verdict=verdict, issues=issues, explor=sec.get("FAILED_ROUTES", "")[:1500], ver=ver))
            self._apply_audit(target, i, verdict, results[-1]["claim"])
            if verdict == "ACCEPT" and results[-1]["claim"].startswith("complete"):
                break           # a fully audited proof ends the round early
        self.graph.save()

        if all(r["verdict"] == "REFUSED" for r in results):
            self.state["next"] = "refused"
            self._save_state()
            (self.dir / "report.md").write_text("All prover attempts were refused by the safety classifier; "
                                                "no record updated.\n" + "\n".join(results[-1]["issues"].splitlines()[:3]))
            return
        # 6. durable progress
        syn = self.step("06_synthesis", lambda: self._synthesis(contract, results))
        self._apply_synthesis(contract, syn)
        self.graph.save()

        # 7. reassess
        report = self._report(contract, results)
        (self.dir / "report.md").write_text(report)
        re_out = self.step("07_reassess", lambda: self.call(
            "director", "director", f"REASSESS\n\nContract: {cid}\n\nRound report:\n{report}\n\n"
            f"Graph frontier:\n{self._frontier_text()}\n\nAnswer with `NEXT: continue|broaden|abandon` and `RATIONALE:`."))
        m = re.search(r"NEXT:\s*(continue|broaden|abandon)", re_out)
        self.state["next"] = m.group(1) if m else "continue"
        self._save_state()
        with open(C.R / "frontier.md", "a") as f:
            f.write(f"\n## {dt.date.today()} {cid} ({self.run_id}) -> {self.state['next']}\n{re_out.strip()}\n")

    # ---------- steps ----------
    def _frontier_text(self):
        return "\n".join(f"- impact={n} {k} [{s}] {t}" for n, k, s, t in self.graph.frontier()[:12]) or "(empty)"

    def _director(self):
        if self.state.get("contract"):
            return f"CONTRACT: {self.state['contract']}\n(fixed by caller)\n"
        counts, tgt = self.db.programme_counts(), self.cfg["programmes"]
        rows = "\n".join(f"- {k} [programme {c.get('programme')}, status {c.get('status')}] {c['goal'].strip()[:300]}"
                         for k, c in self.contracts.items() if c.get("status", "open") == "open")
        task = (f"Choose the single most consequential unresolved lemma for this round.\n\n"
                f"AVAILABLE: {','.join(k for k, c in self.contracts.items() if c.get('status','open')=='open')}\n\n"
                f"## Open contracts\n{rows}\n\n## Proof-graph frontier (ranked by downstream closure)\n{self._frontier_text()}\n\n"
                f"## Coverage\n{self.graph.coverage_report()}\n\n"
                f"## Programme effort: target {tgt}, rounds so far {counts}\n\n"
                f"## Recent runs\n{self.db.recent_runs()}\n\n## frontier.md\n{C.frontier()[-4000:]}\n\n"
                "Reply with `CONTRACT: <id>`, `PROGRAMME: <A|B|C>`, `RATIONALE:` (name the mathematical dependency "
                "or obstruction that justifies this choice), and `GLOBAL_LINK:` (how success moves the full conjecture).")
        return self.call("director", "director", task)

    def _parse_contract(self, text):
        m = re.search(r"CONTRACT:\s*([\w\-]+)", text)
        if m and m.group(1) in self.contracts:
            return m.group(1)
        return next(iter(self.contracts))

    def _contract_text(self, c):
        return yaml.safe_dump(c, sort_keys=False, width=100)

    def _literature(self, c):
        task = (f"## Problem\n{C.problem()}\n\n## Contract\n{self._contract_text(c)}\n\n"
                f"## Ledger excerpt\n{C.ledger_excerpt(c)}\n\n## Known obstructions\n{C.relevant_obstructions(c)}\n\n"
                "Find theorems, methods and prior obstructions relevant to the principal gap. For every result "
                "give exact source (authors, title, year, venue/arXiv) and state what it ACTUALLY says; flag anything "
                "you could not locate as UNVERIFIED. Do not invent citations.")
        return self.call("literature", "literature", task, web_search=self.cfg["round"]["literature_web_search"])

    def _prover(self, c, lit, i, prev):
        n = self.cfg["round"]["approaches_per_target"]
        hints = c.get("approaches", [])
        hint = f"Suggested line of attack (you may deviate with justification): {hints[i-1]}\n" if i <= len(hints) else ""
        task = (f"## Problem\n{C.problem()}\n\n## Contract\n{self._contract_text(c)}\n\n"
                f"## Established claims this contract may use\n{C.claims_for(c, self.graph)}\n\n"
                f"## Ledger excerpt\n{C.ledger_excerpt(c)}\n\n## Known obstructions (do not repeat these)\n{C.relevant_obstructions(c)}\n\n"
                f"## Literature notes\n{lit[:12000]}\n\nTARGET_NODE: {c.get('target_node', c['id'])}\n\n"
                f"You are attempting approach {i} of {n}. "
                + ("It must use a genuinely different mechanism from the earlier attempts:\n" + prev + "\n" if prev else "")
                + hint)
        return self.call("prover", "prover", task)

    def _referee_pass(self, c, i, sec):
        passes = (self.cfg["round"]["referee_passes_for_complete"]
                  if sec.get("STATUS_CLAIM", "").strip().lower().startswith("complete") else 1)
        verdicts, outs = [], []
        for k in range(1, passes + 1):
            def go(k=k):
                deps = [d.strip("-* ").split()[0] for d in sec.get("DEPENDENCIES", "").splitlines() if d.strip("-* ")]
                task = (f"## Contract goal\n{c['goal'].strip()}\n\nSTATUS CLAIMED BY AUTHOR: {sec.get('STATUS_CLAIM','?')}\n\n"
                        f"## Theorem\n{sec.get('THEOREM','(missing)')}\n\n## Proof\n{sec.get('PROOF','(missing)')}\n\n"
                        f"## Declared dependencies (statuses from the proof graph)\n"
                        f"{self.graph.brief([d for d in deps if d in self.graph.nodes]) or '(none resolvable)'}\n\n"
                        f"## Known pitfalls and failure patterns\n{C.pitfalls()}\n\n"
                        f"(Independent audit pass {k} of {passes}.)")
                return self.call("referee", "referee", task)
            outs.append(self.step(f"04_referee_{i}" if k == 1 else f"04_referee_{i}_pass{k}", go))
        for o in outs:
            v = parse_verdict(o)
            if v == "ACCEPT" and re.search(r"FINITE_ONLY:\s*yes", o, re.I):
                v = "GAPS"
            verdicts.append(v)
        verdict = "ACCEPT" if all(v == "ACCEPT" for v in verdicts) else ("REJECT" if "REJECT" in verdicts else "GAPS")
        issues = "\n".join(sections(o).get("ISSUES", "") for o in outs)
        return verdict, issues

    def _verify(self, text, i):
        v = self.cfg["verification"]
        res = V.run_all(text, v["timeout_seconds"], v["memory_mb"])
        lines = []
        for k, r in enumerate(res, 1):
            lines.append(f"### check {k}: supports={r.supports or '-'} kind={r.kind} result={r.result}\n"
                         f"instances: {r.instances or '-'}\n```\n{r.stdout.strip()[-1500:]}\n```")
            if r.supports in self.graph.nodes:
                if r.result == "PASS" and r.kind == "finite" and r.instances:
                    self.graph.record_finite_verification(r.supports, r.instances)
                elif r.result == "COUNTEREXAMPLE":
                    self.graph.record_refutation(r.supports, r.stdout.strip()[-300:])
                    p = ROOT / "experiments" / "counterexamples" / f"{self.run_id}_{r.supports}_{k}.py"
                    p.write_text(r.code)       # kept for human audit: model-authored checks can be buggy
        return "\n\n".join(lines) or "(no check blocks)"

    def _apply_audit(self, target, i, verdict, claim):
        if target not in self.graph.nodes:
            return
        self.graph.record_referee(target, f"{self.run_id}:{i}", verdict)
        if verdict == "ACCEPT" and claim.startswith("complete"):
            n = self.cfg["round"]["referee_passes_for_complete"]
            ok, blockers = self.graph.try_promote(target, n, self.cfg["human_review_required_for_major"])
            self.state.setdefault("promotion", {})[target] = "promoted" if ok else blockers
            self._save_state()

    def _synthesis(self, c, results):
        body = "\n\n".join(
            f"### Approach {r['i']}  author claim: {r['claim']}  referee: {r['verdict']}\nTheorem: {r['theorem']}\n"
            f"Referee issues:\n{r['issues']}\nVerification:\n{r['ver']}\nAuthor exploration notes:\n{r['explor']}" for r in results)
        task = (f"## Contract\n{self._contract_text(c)}\n\n## Round results\n{body}\n\n"
                f"## Current graph nodes in scope\n{self.graph.brief(list(self.graph.nodes)[:60])}\n\n"
                f"Promotion outcome: {self.state.get('promotion', 'none')}")
        return self.call("synthesis", "synthesis", task)

    def _apply_synthesis(self, c, text):
        m = re.search(r"```json\n(.*?)```", text, re.S)
        try:
            data = json.loads(m.group(1)) if m else {}
        except json.JSONDecodeError:
            data = {}
            self.state["synthesis_parse_error"] = True
        stamp = f"## {dt.date.today()} {c['id']} — run {self.run_id}\n"
        entry = data.get("ledger_entry") or "(synthesis produced no parseable entry; see run directory)"
        with open(C.R / "ledger.md", "a") as f:
            f.write("\n" + stamp + entry.strip() + "\n")
        for u in data.get("graph_updates", []):
            try:
                a, nid = u.get("action"), u.get("id")
                if a == "add_node" and nid not in self.graph.nodes:
                    self.graph.add_node(nid, u.get("statement", ""), "candidate", u.get("depends_on", []),
                                        u.get("covers", []), programme=c.get("programme"), source=f"run {self.run_id}")
                elif a == "set_status" and nid in self.graph.nodes:
                    self.graph.apply_model_status(nid, u.get("status", ""), u.get("reason", ""))
                elif a == "add_dependency" and nid in self.graph.nodes:
                    self.graph.add_dependency(nid, u["dep"])
                elif a == "note" and nid in self.graph.nodes:
                    self.graph.nodes[nid]["history"].append(f"note ({self.run_id}): {u.get('text','')}")
            except Exception as e:           # a malformed update must not lose the round
                self.state.setdefault("update_errors", []).append(f"{u}: {e}")
        for k, fa in enumerate(data.get("failed_attempts", []), 1):
            (C.R / "obstructions" / f"{self.run_id}_{k}.md").write_text(
                f"# {fa.get('title','failed attempt')}\n\nTags: {c['id']} {' '.join(c.get('tags', []))}\n\n"
                f"{fa.get('why_failed','')}\n\nDo not repeat unless the specific failure is addressed.\n")
        for g in data.get("new_gaps", []):
            if g.get("id") and g["id"] not in self.graph.nodes:
                self.graph.add_node(g["id"], g.get("statement", ""), "blocked", g.get("depends_on", []),
                                    programme=c.get("programme"), source=f"run {self.run_id}")
        self._save_state()

    def _report(self, c, results):
        t = c.get("target_node", c["id"])
        node = self.graph.nodes.get(t, {})
        lines = [f"# Round {self.run_id}: {c['id']}", "", f"Programme: {c.get('programme')}  |  Target node: {t} [{node.get('status')}]",
                 f"Spend: ${self.db.spent(self.run_id):.2f} (total ${self.db.spent():.2f})", ""]
        for r in results:
            lines += [f"## Approach {r['i']}: author claim `{r['claim']}`, referee `{r['verdict']}`", r["theorem"][:800], "",
                      "Referee issues:", r["issues"][:1500] or "(none)", "", "Verification:", r["ver"][:1500], ""]
        lines += ["## Promotion", str(self.state.get("promotion", "none")), "", "## Coverage", self.graph.coverage_report()]
        errs = self.graph.validate()
        if errs:
            lines += ["", "## GRAPH ERRORS", *errs]
        return "\n".join(lines)
