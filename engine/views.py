"""Human-readable views of the proof graph (the raw YAML is hard to read)."""
from __future__ import annotations
import re

CLS = {"published": "pub", "analytically_verified": "ver", "finite_verified": "fin", "candidate": "cand", "blocked": "blk", "refuted": "ref"}

def mermaid(graph, max_nodes=45):
    rows = graph.frontier()
    keep = {"ERDOS475"} | {k for _, k, _, _ in rows[:max_nodes]}
    for k, n in graph.nodes.items():
        if n["status"] in {"published", "analytically_verified"} and any(d in keep for d in graph.dependents(k)):
            keep.add(k)
    out = ["```mermaid", "flowchart BT"]
    for k in sorted(keep):
        n = graph.nodes.get(k)
        if not n:
            continue
        label = re.sub(r"[\"\[\]()]", "", " ".join(n["statement"].split())[:48])
        out.append(f'  {k}["{k}<br/>{n["status"]}<br/>{label}"]:::{CLS[n["status"]]}')
    for k in sorted(keep):
        for d in graph.nodes[k]["depends_on"]:
            if d in keep:
                out.append(f"  {d} --> {k}")
    out += ["  classDef pub fill:#cfe8cf", "  classDef ver fill:#9fd89f", "  classDef fin fill:#e8e3b0",
            "  classDef cand fill:#e6e6e6", "  classDef blk fill:#f3c9a8", "  classDef ref fill:#f1a9a9", "```"]
    return "\n".join(out)

def write_frontier_view(graph, path):
    gaps = [(n, k, s, t) for n, k, s, t in graph.frontier()]
    lines = ["# Frontier view (auto-generated; do not edit)", "", graph.coverage_report(), "", "## Open claims ranked by closure impact",
             "| impact | id | status | statement |", "|---|---|---|---|"]
    lines += [f"| {n} | {k} | {s} | {t} |" for n, k, s, t in gaps[:40]]
    refs = [k for k, n in graph.nodes.items() if n["status"] == "refuted"]
    lines += ["", "## Refuted (do not revisit without a new mechanism)", ", ".join(refs) or "(none)", "", "## Graph", mermaid(graph)]
    path.parent.mkdir(exist_ok=True)
    path.write_text("\n".join(lines))
