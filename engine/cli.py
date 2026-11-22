import argparse, os, sys, yaml
from pathlib import Path
from . import context as C
from .proof_graph import ProofGraph
from .storage import Storage

ROOT = C.ROOT

def load_env():
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                if v.strip():
                    os.environ.setdefault(k.strip(), v.strip())

def main(argv=None):
    ap = argparse.ArgumentParser(prog="engine")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="one research round")
    r.add_argument("--contract"); r.add_argument("--resume"); r.add_argument("--dry-run", action="store_true")
    sub.add_parser("status"); sub.add_parser("coverage"); sub.add_parser("check-graph")
    h = sub.add_parser("human-approve", help="record human review of a major result"); h.add_argument("node")
    sub.add_parser("regress", help="feed known-bad proofs to the referee (costs money)")
    a = ap.parse_args(argv)

    cfg = yaml.safe_load((ROOT / "config.yaml").read_text())
    graph = ProofGraph(ROOT / "research" / "proof_graph.yaml")
    db = Storage(ROOT / "state.db")

    if a.cmd == "status":
        print(f"spent ${db.spent():.2f} of ${cfg['budget']['total_usd']}")
        for row in db.recent_runs(): print(row)
        for n, k, s, t in graph.frontier()[:10]: print(f"  frontier impact={n} {k} [{s}] {t}")
    elif a.cmd == "coverage":
        print(graph.coverage_report())
    elif a.cmd == "check-graph":
        errs = graph.validate(); print("\n".join(errs) or "graph OK"); sys.exit(1 if errs else 0)
    elif a.cmd == "human-approve":
        ok, why = graph.human_approve(a.node, cfg["round"]["referee_passes_for_complete"]); graph.save()
        print("promoted" if ok else f"approval recorded; still blocked: {why}")
    elif a.cmd == "regress":
        load_env()
        from .regression import run_regressions
        from .claude import ClaudeLLM
        sys.exit(run_regressions(ClaudeLLM(cfg), db))
    elif a.cmd == "run":
        from .orchestrator import Round
        if a.dry_run:
            from .fake import FakeLLM
            llm = FakeLLM()
        else:
            load_env()
            if not os.environ.get("ANTHROPIC_API_KEY"):
                sys.exit("ANTHROPIC_API_KEY not set (copy .env.example to .env, or `ant auth login`)")
            from .claude import ClaudeLLM
            llm = ClaudeLLM(cfg)
        d = Round(cfg, llm, db, graph, run_id=a.resume, contract_id=a.contract).run()
        print(f"round written to {d}\nreport: {d / 'report.md'}")
