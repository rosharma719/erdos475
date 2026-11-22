# erdos-475 — autonomous proof-search system

Goal: a complete, human-readable proof of Erdős #475. Each round must shrink a defined gap, find a new mechanism, or rigorously eliminate an approach.

## Quick start
```bash
python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'
cp .env.example .env              # add ANTHROPIC_API_KEY (git-ignored)
.venv/bin/python -m engine run --dry-run        # plumbing check, no API calls (writes into the repo; use a copy)
.venv/bin/python -m engine run --contract NC3C  # one real round
.venv/bin/python -m engine run --resume <run_id>
.venv/bin/python -m engine status | coverage | check-graph
.venv/bin/python -m engine human-approve <NODE> # required for `major` nodes
.venv/bin/python -m engine regress              # referee must reject known-bad proofs (costs money)
```
**State of the record:** `research/ledger.md` is the Nov 22 ledger (Ledger-3); `proof_graph.yaml`, `claims/`, `contracts/` and `obstructions/` are seeded from it. Results the ledger calls "proved by Claude" are `candidate` here until the referee audits them. Contracts: `LSA1` (FP∀/DFL, programme A), `NC3C` (|A|=p−4, B), `IRC1` (C); `CNALL` is parked. Re-run `ledger.md` → graph sync by hand when the ledger changes; the engine appends new entries but does not re-import.

## Round
director → literature (web search) → prover ×2 genuinely different approaches → blind referee (theorem + proof + deps + pitfalls only; ×2 independent passes if "complete") → exact checks → synthesis → reassess. Each step is saved to `runs/<id>/NN_step.md`; resume skips finished steps. Budgets (`config.yaml`): per-round and total USD, per-call token cap; hitting one pauses the round resumably.

## Integrity rules (enforced in `engine/proof_graph.py`)
- Models can only set `candidate`/`blocked`. `finite_verified`/`refuted` come only from the check runner; `analytically_verified` only via ≥2 referee ACCEPTs, all deps solid, no finite-only evidence, and human approval for `major` nodes. Any REJECT resets the audit.
- Refutations by model-written code are saved to `experiments/counterexamples/` for human audit.
- Check scripts run in a resource-limited subprocess, **not** a network-isolated sandbox.

## Layout
`research/` canonical knowledge (ledger, proof_graph.yaml, claims/, obstructions/, contracts/) · `runs/` raw rounds incl. failures · `agents/` role prompts · `engine/` code · `experiments/` checks, counterexamples, regression · `proof/draft.md` (assembled only once the graph closes).

Lean enters only after the formalization gate: complete dependency graph to published/internal lemmas, explicit hypotheses, independent review finds no gaps.
