"""Builds the smallest relevant context for each role. Referee context deliberately excludes the prover's exploration."""
from __future__ import annotations
import re, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "research"

def read(p, default=""):
    p = Path(p)
    return p.read_text() if p.exists() else default

def load_contracts():
    out = {}
    for f in sorted((R / "contracts").glob("*.yaml")):
        c = yaml.safe_load(f.read_text())
        out[c["id"]] = c
    return out

def agent_prompt(name):
    return read(ROOT / "agents" / f"{name}.md")

def claims_for(contract, graph):
    parts = []
    for k in contract.get("known_inputs", []):
        text = read(R / "claims" / f"{k}.md")
        parts.append(f"### claim file: {k}\n{text.strip() or '(no file)'}")
        if k in graph.nodes:
            parts.append(graph.brief([k]))
    return "\n\n".join(parts)

def relevant_obstructions(contract, limit=6000):
    """All obstruction files whose text mentions the contract id or tags; otherwise the general pitfalls."""
    keys = {contract["id"], *contract.get("tags", [])}
    hits = []
    for f in sorted((R / "obstructions").glob("*.md")):
        t = f.read_text()
        if f.name == "pitfalls.md" or any(k in t for k in keys):
            hits.append(f"### {f.stem}\n{t.strip()}")
    return "\n\n".join(hits)[:limit]

def pitfalls():
    return read(R / "obstructions" / "pitfalls.md")

def ledger_excerpt(contract, limit=40000):
    """Ledger sections (## headings) mentioning the contract's id/tags; falls back to the tail."""
    text = read(R / "ledger.md")
    secs = re.split(r"(?m)^(?=#{2,3} )", text)
    keys = [contract["id"], *contract.get("tags", [])]
    hit = [s for s in secs if any(k.lower() in s.lower() for k in keys)]
    return ("\n".join(hit) if hit else text[-limit:])[:limit]

def problem():
    return read(R / "problem.md")

def frontier():
    return read(R / "frontier.md")
