"""Deterministic verification engine: runs model-supplied check scripts in a resource-limited
subprocess. Local-trust sandbox (rlimits + timeout + temp cwd); it does NOT block network access.

Check block format (inside a prover/referee reply):

```check
# supports: NODE_ID
# kind: finite | counterexample | identity
...python... (prelude from experiments/checks/prelude.py is prepended)
print("INSTANCES: p<=31, |C|=3")   # required for finite
print("RESULT: PASS")              # or RESULT: COUNTEREXAMPLE <details> / RESULT: FAIL
```
"""
from __future__ import annotations
import re, subprocess, sys, tempfile, resource
from dataclasses import dataclass
from pathlib import Path

PRELUDE = (Path(__file__).resolve().parent.parent / "experiments" / "checks" / "prelude.py")
BLOCK = re.compile(r"```check\n(.*?)```", re.S)

@dataclass
class CheckResult:
    supports: str
    kind: str
    result: str          # PASS | COUNTEREXAMPLE | FAIL | ERROR | TIMEOUT | NONE
    instances: str
    stdout: str
    code: str

def extract_checks(text: str):
    return [m.strip() for m in BLOCK.findall(text)]

def _hdr(code, key, default=""):
    m = re.search(rf"^#\s*{key}:\s*(.+)$", code, re.M)
    return m.group(1).strip() if m else default

def run_check(code: str, timeout=120, memory_mb=2048) -> CheckResult:
    def limits():
        resource.setrlimit(resource.RLIMIT_CPU, (timeout, timeout))
        if sys.platform != "darwin":   # RLIMIT_AS is unreliable on macOS
            resource.setrlimit(resource.RLIMIT_AS, (memory_mb << 20,) * 2)
    full = PRELUDE.read_text() + "\n\n" + code
    supports, kind = _hdr(code, "supports"), _hdr(code, "kind", "finite")
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "check.py"
        f.write_text(full)
        try:
            p = subprocess.run([sys.executable, "-I", str(f)], cwd=d, capture_output=True, text=True,
                               timeout=timeout, preexec_fn=limits)
        except subprocess.TimeoutExpired:
            return CheckResult(supports, kind, "TIMEOUT", "", "", code)
    out = (p.stdout + ("\n[stderr]\n" + p.stderr[-1500:] if p.returncode else ""))[-6000:]
    if p.returncode:
        return CheckResult(supports, kind, "ERROR", "", out, code)
    m = re.search(r"^RESULT:\s*(PASS|COUNTEREXAMPLE|FAIL)", p.stdout, re.M)
    inst = re.search(r"^INSTANCES:\s*(.+)$", p.stdout, re.M)
    return CheckResult(supports, kind, m.group(1) if m else "NONE", inst.group(1) if inst else "", out, code)

def run_all(text, timeout=120, memory_mb=2048):
    return [run_check(c, timeout, memory_mb) for c in extract_checks(text)]
