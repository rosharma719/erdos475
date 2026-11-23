"""Parallel research round.

director -> literature (cached per contract) -> K parallel prover BRANCHES, each with its own context:
    prover -> deterministic lint -> blind referee (+ derived verdict) -> exact checks -> [repair passes that
    are biased AGAINST stopping: fix the critical-path gap or exhibit an obstruction] -> novelty comparison
-> main thread applies graph updates (single writer) -> synthesis -> reassess -> human-readable views.

Design choices map to known LLM-math failure modes:
- stopping early / false synthesis: lint flags premature stops and hand-waves; repair passes push on the
  critical-path gap; a branch ends only on ACCEPT-complete, a rigorous counterexample, or the pass limit.
- floundering: one critical gap per repair pass; branches are parallel and independent, not interleaved.
- rederiving samples: the prover is given a KNOWN boundary; a cheap comparison step flags restatements.
- gaps explicit: GAPS are parsed deterministically and registered as blocking nodes in the graph.
- evaluation weakness: verdict severity is derived by code; promotion gates are code; models only compare/produce.
"""
from __future__ import annotations
import json, re, threading, time, datetime as dt
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from pathlib import Path
import yaml

from . import context as C
from .claude import LLM
from .lint import lint_submission, derive_verdict, parse_gaps, parse_scope, mandated_status, effective_claim
from .novelty import known_boundary, retrieve, compare_prompt, parse_relation, jaccard
from .orchestrator import sections, parse_verdict            # shared parsers
from .storage import Storage, BudgetExceeded
from . import verification as V
from .views import write_frontier_view

ROOT = C.ROOT
RUNS = ROOT / "runs"

DEFAULT_BRANCHES = [
    "REFUTE-FIRST: before proving anything, spend a third of your effort trying to construct a counterexample or a precise obstruction to the key lemma (use a ```check block), then prove what survives.",
    "REDUCTION: reduce the target to the smallest sharper statement on the critical path and prove it, or isolate exactly why it is out of reach.",
    "STRUCTURE: look for a different framework or invariant in which the documented obstruction does not arise; justify why it escapes.",
]


class Round:
    def __init__(self, cfg, llm: LLM, storage: Storage, graph, run_id=None, contract_id=None, branches=None):
        self.cfg, self.llm, self.db, self.graph = cfg, llm, storage, graph
        self.run_id = run_id or time.strftime("%Y%m%dT%H%M%S")
        self.dir = RUNS / self.run_id
        self.dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.dir / "state.json"
        self.state = json.loads(self.state_file.read_text()) if self.state_file.exists() else {"contract": contract_id}
        self.contracts = C.load_contracts()
        from .campaign import apply_overrides
        apply_overrides(self.contracts)
        self.lock = threading.RLock()
        self.n_branches = branches or cfg["parallel"]["branches"]

    # ---------- plumbing ----------
    def _save_state(self):
        with self.lock:
            self.state_file.write_text(json.dumps(self.state, indent=1))

    def _ov(self, role):
        return ((getattr(self, "cur_contract", None) or {}).get("roles") or {}).get(role, {})

    def _est(self, role, system, task, max_tokens):
        model = self._ov(role).get("model") or (self.cfg.get("roles", {}).get(role, {}) or {}).get("model", self.cfg["model"])
        p = (self.cfg.get("pricing") or {}).get(model) or self.cfg["pricing_per_mtok"]
        return ((len(system) + len(task)) / 3.5) * p["input"] / 1e6 + max_tokens * p["output"] / 1e6 * 0.5

    def call(self, role, system_name, task, web_search=False, max_tokens=None):
        b = self.cfg["budget"]
        system = C.agent_prompt(system_name)
        mt = max_tokens or self.cfg["max_tokens"].get(role, 32000)
        est = self._est(role, system, task, mt)
        self.db.reserve(self.run_id, est, b["per_round_usd"], b["total_usd"])
        try:
            ov = self._ov(role)
            r = self.llm.complete(role=role, system=system, task=task, max_tokens=mt, web_search=web_search,
                                  model=ov.get("model"), effort=ov.get("effort"), task_budget=ov.get("task_budget"))
        finally:
            self.db.release(self.run_id, est)
        self.db.record_call(self.run_id, role, r.model, r.usage, r.cost_usd, r.stop_reason)
        with self.lock:
            (self.dir / f"prompt_{role}_{len(list(self.dir.glob('prompt_*')))}.md").write_text(task)
        if r.refused:
            return f"[REFUSED by safety classifier; no usable output from {role}] {getattr(r, 'stop_details', '')[:200]}"
        if r.stop_reason == "max_tokens":
            return r.text + "\n\n[TRUNCATED: hit max_tokens — treat any unfinished argument as incomplete]"
        return r.text

    def step(self, name, fn):
        f = self.dir / f"{name}.md"
        if f.exists():
            return f.read_text()
        out = fn()
        f.write_text(out)
        with self.lock:
            self.state.setdefault("done", []).append(name)
        self._save_state()
        return out

    # ---------- the round ----------
    def run(self):
        self.db.start_run(self.run_id, self.state.get("contract") or "?", None)
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
        direction = self.step("01_director", self._director)
        cid = self.state.get("contract") or self._parse_contract(direction)
        self.state["contract"] = cid
        self._save_state()
        c = self.contracts[cid]
        self.cur_contract = c
        self.db.db.execute("UPDATE runs SET contract=?, programme=? WHERE id=?", (cid, c.get("programme"), self.run_id))
        self.db.db.commit()
        target = c.get("target_node", cid)
        if target not in self.graph.nodes:
            self.graph.add_node(target, c["goal"].strip(), "candidate", programme=c.get("programme"), source="contract")
        lit = self._literature(c)
        known = known_boundary(self.graph, [f.stem for f in (C.R / "obstructions").glob("*.md")])
        specs = self._specs(c)

        with ThreadPoolExecutor(max_workers=self.cfg["parallel"]["max_workers"]) as ex:
            futs = [ex.submit(self._branch_safe, c, lit, known, s, specs) for s in specs]
            results = [f.result() for f in futs]
        if any(r is None for r in results):
            raise BudgetExceeded(self.state.get("paused", "budget reached inside a branch"))

        # ---- single-writer graph updates ----
        for r in results:
            self._apply_branch(c, target, r)
        self.graph.save()
        if all(r["verdict"] in {"REFUSED", "STARVED"} for r in results):
            self.state["next"] = "refused"
            self._save_state()
            (self.dir / "report.md").write_text("All branches were refused or budget-starved (no text produced); record not updated. Raise max_tokens or lower effort.\n")
            return

        self.state["progress"] = any(r["scope"] in {"advances_hard_target", "foundational"} and r["claim"] != "failed"
                                     and r["verdict"] != "REJECT" for r in results)
        if not self.state["progress"]:
            self.state["no_progress_note"] = "NO PROGRESS: no branch advanced the hard target (all known-regime-only, failed mandated instances, rejected, or failed)."
        self._save_state()
        syn = self.step("06_synthesis", lambda: self._synthesis(c, results))
        self._apply_synthesis(c, syn)
        self.graph.save()
        report = self._report(c, results)
        (self.dir / "report.md").write_text(report)
        write_frontier_view(self.graph, C.R / "views" / "frontier.md")
        re_out = self.step("07_reassess", lambda: self.call(
            "director", "director", f"REASSESS\n\nContract: {cid}\n\nRound report:\n{report[:12000]}\n\n"
            f"Graph frontier:\n{self._frontier_text()}\n\nAnswer with `NEXT: continue|broaden|abandon`, `RATIONALE:`, and, if continuing or broadening, "
            f"`OBSTRUCTION_BREAKING:` naming the documented obstruction the next round must overcome and the new idea. "
            f"Reject any next step that meets a documented obstruction without a new mechanism.", max_tokens=3000))
        m = re.search(r"NEXT:\s*(continue|broaden|abandon)", re_out)
        self.state["next"] = m.group(1) if m else "continue"
        if not self.state.get("progress") and self.state["next"] == "continue":
            self.state["next"] = "broaden"          # code-enforced: no progress can never be followed by `continue`
        self._save_state()
        with open(C.R / "frontier.md", "a") as f:
            f.write(f"\n## {dt.date.today()} {cid} ({self.run_id}) -> {self.state['next']}\n{re_out.strip()}\n")

    # ---------- director / literature ----------
    def _frontier_text(self):
        return "\n".join(f"- impact={n} {k} [{s}] {t}" for n, k, s, t in self.graph.frontier()[:12]) or "(empty)"

    def _director(self):
        if self.state.get("contract"):
            return f"CONTRACT: {self.state['contract']}\n(fixed by caller)\n"
        counts, tgt = self.db.programme_counts(), self.cfg["programmes"]
        open_ids = [k for k, c in self.contracts.items() if c.get("status", "open") == "open"]
        rows = "\n".join(f"- {k} [programme {self.contracts[k].get('programme')}] {self.contracts[k]['goal'].strip()[:300]}" for k in open_ids)
        task = (f"Choose the single most consequential unresolved lemma for this round. The candidate set is fixed by the human; "
                f"choose only among AVAILABLE.\n\nAVAILABLE: {','.join(open_ids)}\n\n## Open contracts\n{rows}\n\n"
                f"## Proof-graph frontier (deterministic closure ranking)\n{self._frontier_text()}\n\n## Coverage\n{self.graph.coverage_report()}\n\n"
                f"## Programme effort: target {tgt}, rounds so far {counts}\n\n## Recent runs\n{self.db.recent_runs()}\n\n"
                f"## frontier.md\n{C.frontier()[-4000:]}\n\nReply with `CONTRACT: <id>`, `PROGRAMME:`, `RATIONALE:`, `GLOBAL_LINK:`, `OBSTRUCTION_BREAKING:` "
                "(documented obstruction + the specific new idea; if none, do not propose it).")
        return self.call("director", "director", task, max_tokens=3000)

    def _parse_contract(self, text):
        m = re.search(r"CONTRACT:\s*([\w\-]+)", text)
        return m.group(1) if m and m.group(1) in self.contracts else next(iter(self.contracts))

    def _contract_text(self, c):
        return yaml.safe_dump(c, sort_keys=False, width=100)

    def _scope_block(self, c):
        m = "\n".join(f"  {x['id']}: {x['description']}" for x in c.get("mandated_instances", [])) or "  (none)"
        return (f"HARD TARGET: {c.get('hard_target', '(see goal)')}\nKNOWN REGIME (earns nothing): {c.get('known_regime', [])}\n"
                f"MANDATED INSTANCES (failure = automatic fail):\n{m}")

    def _literature(self, c):
        """Cached per contract: literature changes slowly, so don't pay for it every round."""
        cache = C.R / "literature" / f"{c['id']}.md"
        if cache.exists() and not self.cfg["round"].get("refresh_literature"):
            return cache.read_text()
        out = self.step("02_literature", lambda: self.call(
            "literature", "literature",
            f"## Problem\n{C.problem()}\n\n## Contract\n{self._contract_text(c)}\n\n## Ledger excerpt\n{C.ledger_excerpt(c)}\n\n"
            f"## Known obstructions\n{C.relevant_obstructions(c)}\n\nFind theorems, methods and prior obstructions relevant to the principal gap. "
            "For every result give exact source (authors, title, year, venue/arXiv id), a VERBATIM quoted sentence of what it states, and a confidence tag "
            "CONFIRMED (you saw the abstract/page this session) or UNVERIFIED (from memory). Never invent citations. UNVERIFIED items must not be used as established facts.",
            web_search=self.cfg["round"]["literature_web_search"]))
        if not out.startswith("[REFUSED"):
            cache.write_text(out)
        return out

    # ---------- branches ----------
    def _specs(self, c):
        pool = list(c.get("approaches", [])) + DEFAULT_BRANCHES
        return [dict(i=i + 1, label=pool[i % len(pool)]) for i in range(self.n_branches)]

    def _prover_task(self, c, lit, known, spec, specs):
        others = "\n".join(f"  - branch {s['i']}: {s['label'][:140]}" for s in specs if s["i"] != spec["i"])
        return (f"## Problem\n{C.problem()}\n\n## Contract\n{self._contract_text(c)}\n\n"
                f"## Established claims this contract may use\n{C.claims_for(c, self.graph)}\n\n"
                f"## KNOWN BOUNDARY — do NOT restate or re-derive these; a result inside the already-proved coverage is worthless unless it is on the critical path\n{known}\n\n"
                f"## Coverage so far\n{self.graph.coverage_report()}\n\n"
                f"## Ledger excerpt\n{C.ledger_excerpt(c)}\n\n## Known obstructions (do not repeat these)\n{C.relevant_obstructions(c)}\n\n"
                f"## SCOPE\n{self._scope_block(c)}\n\n## Obstruction-breaking hypothesis\n{c.get('obstruction_breaking', '(none given: state which documented obstruction you target)')}\n\n"
                f"## Local computation data (verified; use it)\n{C.data(c) or '(none)'}\n\n## Director guidance from the last round\n{C.frontier()[-3500:]}\n\n## Literature notes (UNVERIFIED items are leads, not facts)\n{lit[:10000]}\n\nTARGET_NODE: {c.get('target_node', c['id'])}\n\n"
                f"## YOUR BRANCH ({spec['i']} of {len(specs)})\n{spec['label']}\nParallel branches are working on:\n{others}\nStay in your lane; duplication wastes the round.\n\n"
                "Budget discipline: begin writing the structured submission early; reasoning that never reaches the output sections is wasted. Do not stop at the first obstacle. Work the critical-path gap to the end: either close it, or reduce it to a precisely stated sub-gap you can show is necessary, "
                "or exhibit a rigorous counterexample. Every unproved step must appear in GAPS; a hand-wave outside GAPS counts as a defect.")

    def _repair_task(self, c, prev, ref_text, lint, ver, scope="unknown", mand_bad=()):
        return (f"TARGET_NODE: {c.get('target_node', c['id'])}\n\n## Contract\n{self._contract_text(c)}\n\n## Your previous submission\n{prev}\n\n## Referee report\n{ref_text}\n\n"
                f"## Deterministic lint flags\n{json.dumps(lint['flags'], indent=1)}\n\n## Exact-check results\n{ver[:3000]}\n\n"
                + (f"NOTICE: referee SCOPE = {scope}. " + ("Your result is confined to the known regime and earns NOTHING: your next version must attack the hard target or isolate precisely why it resists. " if scope == "known_regime_only" else "") + (f"Mandated instances failed or missing: {list(mand_bad)}. " if mand_bad else "") + "\n\n" + f"## SCOPE\n{self._scope_block(c)}\n\n") + "REPAIR PASS. You may not stop here. Identify the SINGLE gap or fatal issue on the critical path (the one whose closure most reduces what remains) and spend your effort on it. "
                "Fix every referee issue marked fatal/repairable or explain precisely why it is not an error. If the claim cannot be closed, reduce it to a sharper stated sub-gap or give a rigorous counterexample. "
                "Never weaken the theorem silently: a weaker theorem must be stated as a NEW theorem and the original stays in GAPS. Same output format as before.")

    def _branch_safe(self, c, lit, known, spec, specs):
        try:
            return self._branch(c, lit, known, spec, specs)
        except BudgetExceeded as e:
            with self.lock:
                self.state["paused"] = str(e)
            self._save_state()
            return None

    def _referee(self, c, tag, sec, claim, ref_text_hint=""):
        passes = self.cfg["round"]["referee_passes_for_complete"] if claim.startswith("complete") else 1
        verdicts, outs = [], []
        deps = [d.strip("-* ").split()[0] for d in sec.get("DEPENDENCIES", "").splitlines() if d.strip("-* ")]
        for k in range(1, passes + 1):
            task = (f"## Contract goal\n{c['goal'].strip()}\n\n## SCOPE\n{self._scope_block(c)}\n\nSTATUS CLAIMED BY AUTHOR: {sec.get('STATUS_CLAIM', '?')}\n\n"
                    f"## Theorem\n{sec.get('THEOREM', '(missing)')}\n\n## Proof\n{sec.get('PROOF', '(missing)')}\n\n"
                    f"## Gaps declared by the author\n{sec.get('GAPS', '(none)')}\n\n"
                    f"## Declared dependencies (statuses from the proof graph)\n{self.graph.brief([d for d in deps if d in self.graph.nodes]) or '(none resolvable)'}\n\n"
                    f"## Known pitfalls and failure patterns\n{C.pitfalls()}\n\n(Independent audit pass {k} of {passes}.)")
            outs.append(self.step(f"{tag}_referee_{k}", lambda task=task: self.call("referee", "referee", task)))
        for o in outs:
            v = derive_verdict(o, parse_verdict(o))
            if v == "ACCEPT" and re.search(r"FINITE_ONLY:\s*yes", o, re.I):
                v = "GAPS"
            verdicts.append(v)
        verdict = "ACCEPT" if all(v == "ACCEPT" for v in verdicts) else ("REJECT" if "REJECT" in verdicts else "GAPS")
        return verdict, "\n".join(sections(o).get("ISSUES", "") for o in outs), "\n".join(outs)

    def _checks(self, tag, text):
        def go():
            v = self.cfg["verification"]
            return json.dumps([asdict(r) for r in V.run_all(text, v["timeout_seconds"], v["memory_mb"])])
        return [V.CheckResult(**d) for d in json.loads(self.step(f"{tag}_verify", go))]

    def _branch(self, c, lit, known, spec, specs):
        i = spec["i"]
        out = self.step(f"b{i}_prover_0", lambda: self.call("prover", "prover", self._prover_task(c, lit, known, spec, specs)))
        res = dict(i=i, label=spec["label"], rounds=0, checks=[], refused=False, scope="unknown", mand_bad=[], claim_author="")
        for r in range(self.cfg["parallel"]["repair_passes"] + 1):
            if "THEOREM" not in sections(out) and "[TRUNCATED" in out:      # budget-starved: all tokens went to reasoning
                res.update(verdict="STARVED", claim="starved", scope="unknown", theorem="", issues="output budget exhausted before any text was produced", gaps=[], lint=dict(flags=["STARVED"]), final=out)
                return res
            if out.startswith("[REFUSED"):
                res.update(refused=True, verdict="REFUSED", claim="refused", scope="unknown", theorem="", issues=out, gaps=[], lint=dict(flags=[]), final=out)
                return res
            sec = sections(out)
            claim = sec.get("STATUS_CLAIM", "").strip().lower()
            lint = lint_submission(sec)
            if not claim.startswith("complete") and len(sec.get("PROOF", "").strip()) < 300:
                # no mathematical content: do not pay a referee. The attempt's failure record is still kept.
                res.update(verdict="NOPROOF", claim="failed", claim_author=claim, scope="unknown", theorem=sec.get("THEOREM", ""),
                           issues="no proof content; referee skipped", gaps=lint["gaps"], lint=lint, final=out, sec=sec,
                           ver="", failure_record=sec.get("FAILURE_RECORD", ""))
                return res
            verdict, issues, ref_text = self._referee(c, f"b{i}_r{r}", sec, claim)
            scope = parse_scope(ref_text)
            mand_ok, mand_bad = mandated_status(ref_text, c.get("mandated_instances", []))
            eff = effective_claim(claim, scope, mand_ok)
            checks = self._checks(f"b{i}_r{r}", out + "\n" + ref_text)
            ver = "\n".join(f"check supports={k.supports or '-'} kind={k.kind} result={k.result} instances={k.instances or '-'}\n{k.stdout[-800:]}" for k in checks) or "(no checks)"
            res.update(rounds=r + 1, claim=eff, claim_author=claim, scope=scope, mand_bad=mand_bad, verdict=verdict, issues=issues, theorem=sec.get("THEOREM", ""), gaps=lint["gaps"],
                       lint=lint, checks=checks, final=out, sec=sec, ver=ver, ref_text=ref_text)
            refuted = any(k.result == "COUNTEREXAMPLE" and k.kind == "counterexample" for k in checks)
            done = (verdict == "ACCEPT" and eff.startswith("complete")) or refuted
            if done or r == self.cfg["parallel"]["repair_passes"]:
                break
            out = self.step(f"b{i}_prover_{r + 1}", lambda: self.call("prover", "prover", self._repair_task(c, out, ref_text, lint, ver, scope, mand_bad)))
        res["novelty"] = self._novelty(i, res.get("theorem", ""))
        return res

    def _novelty(self, i, theorem):
        if not theorem.strip():
            return dict(relation="unknown")
        cands = retrieve(self.graph, theorem, k=6)
        if not cands:
            return dict(relation="new", closest=None, note="no lexical neighbours")
        txt = self.step(f"b{i}_novelty", lambda: self.call(
            "compare", "referee", compare_prompt(theorem[:2500], [(k, ' '.join(self.graph.nodes[k]['statement'].split())[:500]) for k, _ in cands]), max_tokens=600))
        return parse_relation(txt)

    # ---------- single-writer application ----------
    def _apply_branch(self, c, target, r):
        if r["verdict"] in {"REFUSED", "STARVED", "NOPROOF"}:
            return
        i = r["i"]
        for k, ck in enumerate(r["checks"], 1):
            if ck.supports in self.graph.nodes:
                if ck.result == "PASS" and ck.kind == "finite" and ck.instances:
                    self.graph.record_finite_restriction(ck.supports, f"{self.run_id}_b{i}_{k}", ck.instances)
                elif ck.result == "COUNTEREXAMPLE" and ck.kind == "counterexample":
                    self.graph.record_refutation(ck.supports, ck.stdout.strip()[-300:])
                    (ROOT / "experiments" / "counterexamples" / f"{self.run_id}_b{i}_{ck.supports}_{k}.py").write_text(ck.code)
        if target in self.graph.nodes:
            self.graph.record_referee(target, f"{self.run_id}:b{i}", r["verdict"], claim_complete=r["claim"].startswith("complete"))
            if r["verdict"] == "ACCEPT" and r["claim"].startswith("complete") and not r["gaps"]:
                ok, why = self.graph.try_promote(target, self.cfg["round"]["referee_passes_for_complete"], self.cfg["human_review_required_for_major"])
                self.state.setdefault("promotion", {})[target] = "promoted" if ok else why
            for g, text in ([] if r["scope"] == "known_regime_only" else r["gaps"]):
                self.graph.add_gap(target, text, f"{self.run_id[-6:]}b{i}{g}", c.get("programme"), jaccard)
        rel = r.get("novelty", {}).get("relation")
        if target in self.graph.nodes and rel in {"restates", "weaker_than_known"}:
            self.graph._log(target, f"branch {i} flagged {rel} vs {r['novelty'].get('closest')} (rederivation)")
        self._save_state()

    def _synthesis(self, c, results):
        body = "\n\n".join(
            f"### Branch {r['i']} ({r['label'][:70]}) scope={r['scope']} claim={r['claim']} (author said {r['claim_author']}) mandated_failed={r['mand_bad']} referee={r['verdict']} novelty={r.get('novelty', {})}\n"
            f"Theorem: {r['theorem'][:1500]}\nFailure record: {r.get('failure_record', '')[:1200]}\nDeclared gaps: {r['gaps']}\nLint: {r['lint']['flags']}\nReferee issues:\n{r['issues'][:2500]}\nVerification:\n{r.get('ver', '')[:1500]}"
            for r in results if r["verdict"] not in {"REFUSED", "STARVED"})
        return self.call("synthesis", "synthesis",
                         f"## Contract\n{self._contract_text(c)}\n\n{self.state.get('no_progress_note', 'Round made progress on the hard target.')}\nRecord known_regime_only results as at most ONE note; do not add nodes or gaps for them; they are not progress.\n\n## Round results\n{body}\n\nPromotion outcome: {self.state.get('promotion', 'none')}", max_tokens=6000)

    def _apply_synthesis(self, c, text):
        from .orchestrator import Round as _V1
        _V1._apply_synthesis(self, c, text)

    def _report(self, c, results):
        t = c.get("target_node", c["id"])
        node = self.graph.nodes.get(t, {})
        lines = [f"# Round {self.run_id}: {c['id']} ({len(results)} parallel branches)", "",
                 f"Programme: {c.get('programme')}  |  Target node: {t} [{node.get('status')}]",
                 f"Spend: ${self.db.spent(self.run_id):.2f} (total ${self.db.spent():.2f})", self.state.get("no_progress_note", "PROGRESS: at least one branch advanced the hard target."), ""]
        for r in results:
            lines += [f"## Branch {r['i']}: {r['label'][:90]}", f"scope `{r['scope']}`, claim `{r['claim']}` (author: {r['claim_author']}), mandated failed {r['mand_bad']}, referee `{r['verdict']}`, passes {r['rounds']}, novelty `{r.get('novelty', {}).get('relation')}` ({r.get('novelty', {}).get('closest')})",
                      "", r["theorem"][:900], "", "Declared gaps:", *(f"- {g}: {t_[:300]}" for g, t_ in r["gaps"]), "",
                      "Lint flags:", *(f"- {f}" for f in r["lint"]["flags"]), "", "Referee issues:", r["issues"][:1500] or "(none)", "",
                      "Verification:", r.get("ver", "")[:1200], ""]
        lines += ["## Promotion", str(self.state.get("promotion", "none")), "", "## Coverage", self.graph.coverage_report()]
        errs = self.graph.validate()
        if errs:
            lines += ["", "## GRAPH ERRORS", *errs]
        return "\n".join(lines)
