"""Proof graph: the canonical record of what is proved, what is open, and what the models may NOT change.

Key rule: a model-driven path can never set `analytically_verified`. Promotion requires
(a) >= N independent referee ACCEPTs, (b) every dependency verified/published,
(c) no finite-only evidence standing in for a general claim, and (d) human approval for major results.
"""
from __future__ import annotations
import yaml
from pathlib import Path

STATUSES = ["published", "analytically_verified", "finite_verified", "candidate", "blocked", "refuted"]
SOLID = {"published", "analytically_verified"}
# statuses a model-originated update may assign directly
MODEL_SETTABLE = {"candidate", "blocked"}

class GraphError(ValueError):
    pass

class ProofGraph:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        data = yaml.safe_load(self.path.read_text()) if self.path.exists() else {}
        self.root = data.get("root", "ERDOS475")
        self.nodes: dict = data.get("nodes", {})

    def save(self):
        self.path.write_text(yaml.safe_dump({"root": self.root, "nodes": self.nodes}, sort_keys=False, width=100))

    # ---- construction ----
    def add_node(self, id, statement, status="candidate", depends_on=(), covers=(), major=False,
                 programme=None, source="", notes=""):
        if id in self.nodes:
            raise GraphError(f"node {id} exists")
        if status not in STATUSES:
            raise GraphError(f"bad status {status}")
        self.nodes[id] = dict(statement=statement, status=status, depends_on=list(depends_on),
                              covers=list(covers), major=major, programme=programme, source=source,
                              notes=notes, audit=dict(referee_accepts=0, rounds=[], human="none"),
                              finite_instances="", history=[])
        self._check_acyclic()

    def add_dependency(self, id, dep):
        if dep not in self.nodes or id not in self.nodes:
            raise GraphError("unknown node")
        if dep not in self.nodes[id]["depends_on"]:
            self.nodes[id]["depends_on"].append(dep)
        self._check_acyclic()

    def _check_acyclic(self):
        state = {}
        def visit(n, stack):
            if state.get(n) == 1:
                raise GraphError("dependency cycle: " + " -> ".join(stack + [n]))
            if state.get(n) == 2:
                return
            state[n] = 1
            for d in self.nodes[n]["depends_on"]:
                if d in self.nodes:
                    visit(d, stack + [n])
            state[n] = 2
        for n in self.nodes:
            visit(n, [])

    # ---- status changes ----
    def _log(self, id, msg):
        self.nodes[id]["history"].append(msg)

    def apply_model_status(self, id, status, reason=""):
        """Model-originated status change. Only candidate/blocked are accepted; anything else is
        downgraded to a note. Never demotes a solid node without a deterministic refutation."""
        n = self.nodes[id]
        if status not in MODEL_SETTABLE:
            self._log(id, f"model proposed '{status}' (not applied): {reason}")
            return False
        if n["status"] in SOLID | {"refuted", "finite_verified"}:
            self._log(id, f"model proposed '{status}' over '{n['status']}' (not applied): {reason}")
            return False
        n["status"] = status
        self._log(id, f"-> {status}: {reason}")
        return True

    def add_gap(self, target, text, tag, programme=None, dedupe_fn=None):
        """Register an explicitly declared gap as a blocked node the target depends on (so the target
        cannot be promoted while it stands). Deterministic: not left to an LLM summary."""
        if dedupe_fn:
            for i, n in self.nodes.items():
                if n.get("kind") == "gap" and dedupe_fn(text, n["statement"]) > 0.6:
                    self.add_dependency(target, i)
                    return i
        gid = f"GAP_{target}_{tag}"
        if gid in self.nodes:
            return gid
        self.add_node(gid, text, "blocked", programme=programme, source="declared gap",
                      notes="explicitly declared by a prover/referee; close it or refute it with evidence")
        self.nodes[gid]["kind"] = "gap"
        self.add_dependency(target, gid)
        return gid

    def record_refutation(self, id, evidence: str):
        """Only the deterministic verification engine calls this."""
        self.nodes[id]["status"] = "refuted"
        self.nodes[id]["finite_instances"] = evidence
        self._log(id, f"-> refuted by deterministic check: {evidence[:200]}")

    def record_finite_restriction(self, claim_id, tag, instances: str):
        """A finite check NEVER changes the status of the universal claim. It creates a separate
        finite_verified proposition recording exactly the domain tested."""
        nid = f"{claim_id}__FIN_{tag}"
        if nid in self.nodes:
            return nid
        self.add_node(nid, f"Finite restriction of {claim_id}, exactly the tested domain: {instances}",
                      "finite_verified", source="verification engine",
                      notes="proof_of_universal_claim: false")
        self.nodes[nid]["finite_instances"] = instances
        self.nodes[nid]["restriction_of"] = claim_id
        self._log(claim_id, f"finite restriction recorded as {nid}; status of {claim_id} unchanged")
        return nid

    def record_referee(self, id, round_id, verdict, claim_complete=True):
        """Acceptance of a PARTIAL result is logged but never counts toward promotion."""
        a = self.nodes[id]["audit"]
        if round_id in a["rounds"]:
            return
        a["rounds"].append(round_id)
        if verdict == "ACCEPT" and not claim_complete:
            self._log(id, f"referee ACCEPT of a partial result in {round_id} (not counted toward promotion)")
        elif verdict == "ACCEPT":
            a["referee_accepts"] += 1
        else:
            a["referee_accepts"] = 0   # any rejection resets the audit
        self._log(id, f"referee {verdict} in {round_id}")

    def promotion_blockers(self, id, required_passes=2, human_required=True):
        n, out = self.nodes[id], []
        if n["audit"]["referee_accepts"] < required_passes:
            out.append(f"needs {required_passes} referee accepts (has {n['audit']['referee_accepts']})")
        for d in n["depends_on"]:
            if self.nodes.get(d, {}).get("status") not in SOLID:
                out.append(f"dependency {d} is {self.nodes.get(d, {}).get('status', 'missing')}")
        if n["status"] in {"refuted", "blocked"}:
            out.append(f"status is {n['status']}")
        if n["status"] == "finite_verified":
            out.append("finite evidence only; a finite restriction is not a proof")
        if human_required and n["major"] and n["audit"]["human"] != "approved":
            out.append("major result awaits human review")
        return out

    def try_promote(self, id, required_passes=2, human_required=True):
        blockers = self.promotion_blockers(id, required_passes, human_required)
        if blockers:
            return False, blockers
        self.nodes[id]["status"] = "analytically_verified"
        self._log(id, "-> analytically_verified (audit gates passed)")
        return True, []

    def human_approve(self, id, required_passes=2):
        n = self.nodes[id]
        n["audit"]["human"] = "approved"
        return self.try_promote(id, required_passes, human_required=True)

    # ---- analysis ----
    def dependents(self, id):
        return [k for k, v in self.nodes.items() if id in v["depends_on"]]

    def validate(self):
        errs = []
        for k, n in self.nodes.items():
            if n["status"] == "analytically_verified":
                for d in n["depends_on"]:
                    if self.nodes.get(d, {}).get("status") not in SOLID:
                        errs.append(f"{k} verified but depends on non-solid {d}")
            for d in n["depends_on"]:
                if d not in self.nodes:
                    errs.append(f"{k} depends on unknown {d}")
        return errs

    def frontier(self):
        """Open claims ranked by how much of the graph they unblock (closure, not volume)."""
        def downstream(n, seen):
            for d in self.dependents(n):
                if d not in seen:
                    seen.add(d)
                    downstream(d, seen)
            return seen
        rows = []
        for k, n in self.nodes.items():
            if n["status"] in {"candidate", "blocked", "finite_verified"}:
                rows.append((len(downstream(k, set())), k, n["status"], n["statement"].strip().split("\n")[0][:90]))
        return sorted(rows, reverse=True)

    def coverage_report(self):
        solid, open_, fin = [], [], []
        for k, n in self.nodes.items():
            for c in n["covers"]:
                (solid if n["status"] in SOLID else fin if n["status"] == "finite_verified" else open_).append((c, k, n["status"]))
        lines = [f"Target: {self.root} (all primes p, all A)", "", "PROVED coverage:"]
        lines += [f"  {c}  [{k}: {s}]" for c, k, s in solid] or ["  (none recorded)"]
        lines += ["", "FINITE-ONLY coverage (not a proof of anything beyond the listed instances):"]
        lines += [f"  {c}  [{k}]" for c, k, s in fin] or ["  (none)"]
        lines += ["", "UNPROVED coverage claims:"]
        lines += [f"  {c}  [{k}: {s}]" for c, k, s in open_] or ["  (none)"]
        return "\n".join(lines)

    def brief(self, ids):
        out = []
        for i in ids:
            n = self.nodes.get(i)
            if n:
                out.append(f"- {i} [{n['status']}]: {n['statement'].strip()}")
        return "\n".join(out)
