# Audit: singular-projection elimination (Claude, 2026-11-24)
The submission was pasted in chat. Scripts: `experiments/audits/singular_projection/` (`sp.py` is the submitted verifier; `dimk.py` is the scope check).

## Accepted (hand-checked)
- **Thm 1 (singular projection eliminates a minimal counterexample): CORRECT.**
  - Setup: x ∈ K = L^⊥, where L is spanned by incidence vectors of *all* actual zero-sum subsets. So an actual zero-sum interval forces a projected zero-sum interval.
  - The Z-labels are inserted as {first element} and {tail} in two gaps. The split matters: a Graham ordering of a non-zero-sum A_Z may revisit 0, but the tail path cannot.
  - Any cyclic interval meets R in a cyclic interval of the projected cycle. If that part is proper, the projected sum is nonzero. If it is empty or all of R, the interval or its complement lies inside one gap's piece, which is internally simple.
- **Thm 2 (single-defect swap repair): ACCEPTED.**
- **Thm 3 (permanent certificate): CORRECT.** Each f_ℓ is linear in ε. The coefficient of ε₁⋯ε_q is per(C)·∏δ_k, and the Combinatorial Nullstellensatz on {0, 1}^q applies.
- **Thm 4 (forced chord relations): CORRECT.**
  - Equalities x_j = x_k are proper subspaces of H_i = ker u_i unless u_j − u_k = λu_i.
  - With ≤ p proper subspaces they cannot cover H_i, and an avoiding vector has distinct nonzero coordinates, so Thm 1 applies.
- **Examples and sampled run reproduced:**
  - the p = 13 single-defect repair (1, 9, 8, 2, 12, 3, 4);
  - the p = 17 multiset projection;
  - the p = 13 rank-one obstruction;
  - 873 rank-two sets, all eliminated (826 simple, 47 single-defect).

## Scope: the method needs dim K ≥ 2, and generic dense sets have dim K = 1
Random zero-sum sets, 40 per cell (`dimk.py`):

| p | n = 6 | n = 8 | n = 10 | n = 12, 14, 16 |
|---|---|---|---|---|
| 23 | dim K ≥ 3 | 1–5, mostly 2–3 | 39/40 have dim K = 1 | **40/40 dim K = 1** |
| 31 | ≥ 3 | 2–5 | 35/40 dim K = 1 | **40/40** |
| 37 | ≥ 3 | 2–6 | 26/40 dim K = 1 | **40/40** |

**Heuristic.** There are about 2ⁿ/p zero-sum subsets. Once 2ⁿ ≫ np they span a^⊥, so dim K ≥ 2 essentially requires n ≲ log₂ p + O(log log p). This is the same logarithmic regime as dissociated repair (`modular_repair_audit.md`).

**Consequence.** The submission's "next high-leverage target", the rank-one case, is **not a residual case**: it is the generic dense case, that is, the whole remaining conjecture. Singular projection is a correct elimination tool for small n. It does not reduce the dense problem.
