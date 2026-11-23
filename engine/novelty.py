"""Novelty against persistent state. The model does not remember the frontier; the repository does.
Retrieval is lexical (cheap, deterministic); the LLM only does COMPARISON of a statement against retrieved
candidates (what it is good at), never absolute 'is this good/new' evaluation."""
from __future__ import annotations
import json, re

def toks(s: str) -> set:
    return {w for w in re.findall(r"[a-z0-9_]{3,}", s.lower())}

def jaccard(a: str, b: str) -> float:
    x, y = toks(a), toks(b)
    return len(x & y) / max(1, len(x | y))

def retrieve(graph, text: str, k=6, exclude=()):
    scored = [(jaccard(text, n["statement"]), i) for i, n in graph.nodes.items() if i not in exclude]
    return [(i, s) for s, i in sorted(scored, reverse=True)[:k] if s > 0.05]

def known_boundary(graph, obstruction_titles, limit_chars=9000) -> str:
    lines = []
    for i, n in graph.nodes.items():
        if n.get("source") == "verification engine":
            continue
        lines.append(f"- {i} [{n['status']}]: {' '.join(n['statement'].split())[:170]}")
    out = "\n".join(lines)[:limit_chars]
    return out + "\n\nDocumented obstructions: " + "; ".join(obstruction_titles)[:2500]

def compare_prompt(statement: str, cands) -> str:
    body = "\n".join(f"[{i}] {t}" for i, t in cands)
    return (f"NEW STATEMENT:\n{statement}\n\nKNOWN STATEMENTS:\n{body}\n\n"
            "For the NEW statement, compare it with each KNOWN one. Reply with one JSON object only: "
            '{"relation": "new|restates|weaker_than_known|stronger_than_known|unrelated", "closest": "<id or null>", "note": "<=20 words"}. '
            "`restates` = same content up to notation; `weaker_than_known` = implied by a known statement.")

def parse_relation(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.S)
    try:
        d = json.loads(m.group(0))
        d.setdefault("relation", "unrelated")
        return d
    except Exception:
        return {"relation": "unknown", "closest": None, "note": "unparseable"}
