"""Deterministic submission lint: evaluation done by code, not by an LLM.

Targets the failure modes of LLM mathematics: hand-waved steps outside any declared gap, premature
stopping with no explicit gap, claims of completeness that contradict the declared gaps."""
from __future__ import annotations
import re

HANDWAVE = [r"\bclearly\b", r"\bobviously\b", r"\bsimilarly\b", r"by a similar argument", r"it is easy to (see|check|verify)",
            r"\broutine\b", r"\bwe omit\b", r"\bleft to the reader\b", r"\bwithout loss of generality\b(?! \()",
            r"\bstandard (argument|technique|computation)\b", r"\bone can (show|check|verify)\b", r"\bit follows (easily|readily)\b",
            r"\bas expected\b", r"\bheuristic(ally)?\b"]

def parse_gaps(gap_section: str):
    """Lines like `G1: statement` (continuation lines attach to the previous gap)."""
    gaps, cur = [], None
    for line in gap_section.splitlines():
        m = re.match(r"\s*[-*]?\s*(G\d+)\s*[:.)]\s*(.*)", line)
        if m:
            cur = [m.group(1), m.group(2).strip()]
            gaps.append(cur)
        elif cur and line.strip():
            cur[1] += " " + line.strip()
    return [(g, t) for g, t in gaps if t and t.lower() not in {"none", "(none)"}]

def lint_submission(sec: dict) -> dict:
    proof = sec.get("PROOF", "")
    claim = sec.get("STATUS_CLAIM", "").strip().lower()
    gaps = parse_gaps(sec.get("GAPS", ""))
    flags = []
    hits = sorted({m.group(0).lower() for pat in HANDWAVE for m in re.finditer(pat, proof, re.I)})
    if hits:
        flags.append(f"hand-wave phrases in PROOF outside any declared gap: {hits} — each must be proved or moved into GAPS")
    if claim.startswith("complete") and gaps:
        flags.append("claims `complete` but declares gaps")
    if not claim.startswith("complete") and not gaps:
        flags.append("PREMATURE STOP: claim is not complete but no explicit gap is declared")
    if not sec.get("THEOREM") or not sec.get("PROOF"):
        flags.append("missing THEOREM or PROOF")
    if len(proof) < 400 and claim.startswith("complete"):
        flags.append("suspiciously short proof for a `complete` claim")
    return dict(flags=flags, gaps=gaps, handwave=hits)

SEV = re.compile(r"\b(fatal|repairable|cosmetic)\b", re.I)

def derive_verdict(referee_text: str, stated: str) -> str:
    """Never more lenient than the severities the referee itself assigned."""
    m = re.search(r"##\s*ISSUES(.*?)(?=\n##|\Z)", referee_text, re.S)
    sev = [s.lower() for s in SEV.findall(m.group(1))] if m else []
    # `fatal for the contract, not for the stated theorem` style wording counts as scope, not logic
    derived = "REJECT" if "fatal" in sev else ("GAPS" if "repairable" in sev else "ACCEPT")
    order = {"ACCEPT": 0, "GAPS": 1, "REJECT": 2}
    return stated if order[stated] >= order[derived] else derived

SCOPE_RE = re.compile(r"##\s*SCOPE:?\s*([A-Za-z_]+)")
MAND_RE = re.compile(r"^\s*(M\d+)\s*[:.)]\s*(PASS|FAIL)", re.M)

def parse_scope(referee_text: str) -> str:
    m = SCOPE_RE.search(referee_text)
    s = m.group(1).lower() if m else "unknown"
    return s if s in {"advances_hard_target", "known_regime_only", "foundational"} else "unknown"

def mandated_status(referee_text: str, mandated: list):
    """All contract-mandated instances must be reported PASS by the referee; missing or FAIL => automatic fail."""
    if not mandated:
        return True, []
    got = dict(MAND_RE.findall(referee_text.split("MANDATED_INSTANCES", 1)[-1] if "MANDATED_INSTANCES" in referee_text else ""))
    bad = [m["id"] for m in mandated if got.get(m["id"]) != "PASS"]
    return not bad, bad

def effective_claim(claim: str, scope: str, mandated_ok: bool) -> str:
    """No negative signal for easy wins is the root failure; this supplies it. A proof confined to the known regime,
    or one that fails a mandated hard instance, is `failed` no matter how correct it is."""
    if scope == "known_regime_only" or not mandated_ok:
        return "failed"
    return claim
