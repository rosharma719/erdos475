import shutil, yaml, pytest
from pathlib import Path
from engine.proof_graph import ProofGraph, GraphError
from engine.storage import Storage, BudgetExceeded
from engine import verification as V

def g(tmp_path):
    return ProofGraph(tmp_path / "g.yaml")

def test_model_cannot_promote(tmp_path):
    G = g(tmp_path)
    G.add_node("A", "a")
    assert not G.apply_model_status("A", "analytically_verified")
    assert G.nodes["A"]["status"] == "candidate"

def test_promotion_gates(tmp_path):
    G = g(tmp_path)
    G.add_node("D", "dep"); G.add_node("A", "a", depends_on=["D"], major=True)
    G.record_referee("A", "r1", "ACCEPT"); G.record_referee("A", "r2", "ACCEPT")
    ok, why = G.try_promote("A")
    assert not ok and any("dependency D" in w for w in why) and any("human" in w for w in why)
    G.nodes["D"]["status"] = "published"
    assert not G.try_promote("A")[0]            # still needs human
    assert G.human_approve("A")[0]
    assert G.nodes["A"]["status"] == "analytically_verified"

def test_reject_resets_audit(tmp_path):
    G = g(tmp_path); G.add_node("A", "a")
    G.record_referee("A", "r1", "ACCEPT"); G.record_referee("A", "r2", "REJECT")
    assert G.nodes["A"]["audit"]["referee_accepts"] == 0

def test_cycle_rejected(tmp_path):
    G = g(tmp_path); G.add_node("A", "a"); G.add_node("B", "b", depends_on=["A"])
    with pytest.raises(GraphError):
        G.add_dependency("A", "B")

def test_finite_check_never_solid(tmp_path):
    G = g(tmp_path); G.add_node("A", "a")
    nid = G.record_finite_restriction("A", "t", "p<=7")
    assert G.nodes["A"]["status"] == "candidate"            # universal claim unchanged
    assert G.nodes[nid]["status"] == "finite_verified" and G.promotion_blockers(nid)

def test_partial_accept_not_counted(tmp_path):
    G = g(tmp_path); G.add_node("A", "a")
    G.record_referee("A", "r1", "ACCEPT", claim_complete=False)
    assert G.nodes["A"]["audit"]["referee_accepts"] == 0

def test_budget(tmp_path):
    s = Storage(tmp_path / "s.db")
    s.record_call("r", "prover", "m", dict(input=1, output=1), 5.0, "end_turn")
    with pytest.raises(BudgetExceeded):
        s.check_budget("r", 5.0, 100)

def test_check_runner():
    ok = V.run_check('# supports: X\n# kind: finite\nprint("INSTANCES: p=5")\nassert find_ordering([1,2,3,4],5) is not None or True\nprint("RESULT: PASS")')
    assert ok.result == "PASS" and ok.instances == "p=5"
    assert V.run_check("raise SystemExit(3)").result == "ERROR"
    assert V.run_check("while True: pass", timeout=1).result in {"TIMEOUT", "ERROR"}

def test_known_small_orderings():
    out = V.run_check('print("INSTANCES: p=7,|C|=3")\nbad=fixed_complement_check(7,3)\nprint("RESULT: PASS" if not bad else "RESULT: FAIL "+str(bad))')
    assert out.result in {"PASS", "FAIL"}   # exercise the prelude; outcome reported, not assumed

def test_dry_run_round_and_resume(tmp_path, monkeypatch):
    import engine.orchestrator_v2 as O, engine.context as C
    root = tmp_path / "repo"
    shutil.copytree(C.ROOT, root, ignore=shutil.ignore_patterns(".venv", "runs", "state.db", "__pycache__", ".git"))
    (root / "runs").mkdir()
    monkeypatch.setattr(O, "ROOT", root); monkeypatch.setattr(O, "RUNS", root / "runs")
    monkeypatch.setattr(C, "ROOT", root); monkeypatch.setattr(C, "R", root / "research")
    from engine.fake import FakeLLM
    from engine.proof_graph import ProofGraph
    cfg = yaml.safe_load((root / "config.yaml").read_text())
    G = ProofGraph(root / "research" / "proof_graph.yaml"); db = Storage(tmp_path / "s.db")
    llm = FakeLLM()
    d = O.Round(cfg, llm, db, G, run_id="t1").run()
    assert (d / "report.md").exists()
    n = len(llm.calls)
    O.Round(cfg, llm, db, G, run_id="t1").run()       # resume: every step cached
    assert len(llm.calls) == n
    assert any(k.startswith("GAP_") for k in G.nodes)                       # declared gap registered
    assert any("__FIN_" in k for k in G.nodes)                             # finite check -> separate node
    assert G.nodes[[k for k in G.nodes if k.startswith("GAP_")][0]]["status"] == "blocked"
    assert not G.validate()


def test_lint_and_verdict():
    from engine.lint import lint_submission, derive_verdict
    L = lint_submission({"THEOREM": "t", "PROOF": "Clearly this holds. " * 30, "STATUS_CLAIM": "partial", "GAPS": ""})
    assert any("PREMATURE" in f for f in L["flags"]) and L["handwave"]
    assert derive_verdict("## ISSUES\n1. (fatal) step 3 false", "ACCEPT") == "REJECT"
    assert derive_verdict("## ISSUES\n1. (cosmetic) typo", "GAPS") == "GAPS"

def test_gap_dedupe(tmp_path):
    from engine.novelty import jaccard
    G = ProofGraph(tmp_path / "g.yaml"); G.add_node("T", "t")
    a = G.add_gap("T", "prove the avoidance lemma for dense sets mod p", "x1", None, jaccard)
    b = G.add_gap("T", "prove the avoidance lemma for dense sets mod p again", "x2", None, jaccard)
    assert a == b and len([k for k in G.nodes if k.startswith("GAP_")]) == 1


def test_scope_and_mandated_enforcement():
    from engine.lint import effective_claim, mandated_status, parse_scope
    assert effective_claim("partial", "known_regime_only", True) == "failed"
    assert effective_claim("complete", "advances_hard_target", False) == "failed"
    assert effective_claim("partial", "foundational", True) == "partial"
    assert parse_scope("## SCOPE: known_regime_only\n") == "known_regime_only"
    ok, bad = mandated_status("## MANDATED_INSTANCES\nM1: PASS\nM2: FAIL\n", [{"id": "M1"}, {"id": "M2"}])
    assert not ok and bad == ["M2"]
    assert mandated_status("no section", [{"id": "M1"}])[0] is False       # omission fails
    assert mandated_status("x", [])[0] is True
