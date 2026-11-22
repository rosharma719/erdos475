"""Failure-pattern regressions: known-bad proofs the referee must NOT accept. Files: experiments/regression/*.md
with a front line `expect: reject|gaps` followed by the flawed theorem/proof in prover format."""
import re
from . import context as C
from .orchestrator import sections, parse_verdict

def run_regressions(llm, db):
    bad = 0
    for f in sorted((C.ROOT / "experiments" / "regression").glob("*.md")):
        text = f.read_text()
        expect = re.match(r"expect:\s*(\w+)", text).group(1).upper()
        sec = sections(text)
        task = (f"## Theorem\n{sec.get('THEOREM','')}\n\n## Proof\n{sec.get('PROOF','')}\n\n"
                f"## Known pitfalls and failure patterns\n{C.pitfalls()}")
        r = llm.complete(role="referee", system=C.agent_prompt("referee"), task=task, max_tokens=16000)
        db.record_call("regression", "referee", r.model, r.usage, r.cost_usd, r.stop_reason)
        v = parse_verdict(r.text)
        ok = v != "ACCEPT"
        print(f"{'ok  ' if ok else 'FAIL'} {f.name}: referee said {v} (expected not ACCEPT; label {expect})")
        bad += not ok
    return 1 if bad else 0
