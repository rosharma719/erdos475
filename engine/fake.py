"""Deterministic stand-in LLM for --dry-run and tests. Emits the exact formats the orchestrator parses."""
from .claude import LLMResult

class FakeLLM:
    def __init__(self, referee_verdict="GAPS"):
        self.referee_verdict = referee_verdict
        self.calls = []

    def complete(self, *, role, system, task, max_tokens, web_search=False, **kw):
        self.calls.append(role)
        usage = dict(input=1000, output=500, cache_read=0, cache_write=0)
        return LLMResult(getattr(self, role)(task), "end_turn", "fake", usage, 0.01)

    def director(self, task):
        if "REASSESS" in task:
            return "NEXT: continue\nRATIONALE: dry run.\n"
        import re
        cid = re.search(r"AVAILABLE: ([\w\-]+)", task).group(1)
        return f"CONTRACT: {cid}\nPROGRAMME: B\nRATIONALE: dry run picks the first open contract.\n"

    def literature(self, task):
        return "## Findings\n(dry run: no literature consulted)\n"

    def prover(self, task):
        import re
        node = re.search(r"TARGET_NODE: ([\w\-]+)", task).group(1)
        return f"""## THEOREM
For p = 7, every 3-subset C of F_p^* has complement with a valid ordering.
## PROOF
Exhaustive check only (NOT a general proof). We enumerate every 3-subset C of F_7^* and exhibit an explicit ordering of the complement for each. We enumerate every 3-subset C of F_7^* and exhibit an explicit ordering of the complement for each. We enumerate every 3-subset C of F_7^* and exhibit an explicit ordering of the complement for each. We enumerate every 3-subset C of F_7^* and exhibit an explicit ordering of the complement for each. 
## DEPENDENCIES
(none)
## GAPS
G1: the statement for general p is not proved; only p=7 was checked exhaustively.
## NOVELTY
dry run: nothing new.
## OBSTRUCTION_ADDRESSED
none (dry run)
## STATUS_CLAIM
partial
## CHECKS
```check
# supports: {node}
# kind: finite
bad = fixed_complement_check(7, 3)
print("INSTANCES: p=7, |C|=3")
print("RESULT: PASS" if not bad else "RESULT: COUNTEREXAMPLE %s" % bad)
```
## FAILED_ROUTES
Tried small cases first.
"""

    def referee(self, task):
        return (f"## VERDICT: {self.referee_verdict}\n## ISSUES\n1. (repairable) Only finite instances are covered; "
                "no argument for general p.\n## COUNTEREXAMPLE_ATTEMPTS\nnone\n")

    def compare(self, task):
        return '{"relation": "new", "closest": null, "note": "dry run"}'

    def synthesis(self, task):
        return """```json
{"ledger_entry": "Dry run: finite check for p=7 only.",
 "graph_updates": [{"id": "X", "action": "note", "text": "dry-run note"}],
 "failed_attempts": [{"title": "dry-run attempt", "why_failed": "finite only, no general argument"}],
 "new_gaps": []}
```"""
