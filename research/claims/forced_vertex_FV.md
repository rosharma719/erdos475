# Forced vertices and the minimal-counterexample route (FV) (Claude, 2026-11-24)
GPT proposed returning to F_p and studying the vertices forced in every valid cycle that starts with t. Code: `experiments/exploration/forced_vertex/`.

## Relation to existing work
- K(B, z) is the repo's EC/MC object (`cycle_flexibility.md`).
- The reflection K = t − K is the ledger's tail-reversal symmetry V ↔ z − V.
- The single-merge reduction is FP∀ (`dense_avoidance.md`).
- **What is new** is the framing: minimal counterexample plus *all* admissible contractions at once.

## FV (one-point avoidance)
**Statement.** For every zero-sum B ⊆ F_p^×, every t ∈ B and every x ∉ {0, t, t/2}, some valid cycle of B starting with t avoids x. This is MC without the half point; the known MC exception family has x = z/2.

**FV ⇒ Graham.** Take a zero-sum A with an admissible split t = x + y ∉ A ∪ {0} (it exists for 5 ≤ |A| ≤ p − 2 by Dias da Silva–Hamidoune). Apply FV to B = (A ∖ {x, y}) ∪ {t} and expand the t-step.

**Independent exhaustive verification (`fv.c`; all sets of every size, up to dilation):**

| p | tests (B, t, x) | failures | time |
|---|---|---|---|
| 11 | 600 | 0 | |
| 13 | 2,220 | 0 | |
| 17 | 29,232 | 0 | |
| 19 | 115,920 | 0 | |
| 23 | 1,844,700 | 0 | 0.5 s |
| 29 | 120,551,340 | 0 | 35 s |
| 31 | 485,408,700 | 0 | 2.5 min |

This is the cleanest-data statement in the project: no exception list besides x = t/2.

## Two-point avoidance is false, but rare (`fv2.c`)
- p = 11: 313 / 2,100 fail. p = 13: 592 / 9,990 fail, mostly from small sets.
- p = 17, sizes 5–12: **4 / 180,908** fail, all from B = {4, 5, 8, 9, 12, 13}, which is structured.
- **Consequence.** FV does not self-reduce by arbitrary two-point avoidance (an inner contraction needs to avoid x *and* a forced intermediate vertex). An induction must exploit the specific geometry of the second point.

## The minimal-counterexample formulation (the actual target)
If A is a minimum counterexample, then **for every** admissible split (x, y) we have x, y ∈ K(B_xy, x + y). There are at least min(p − n − 1, n − 4) distinct sums, each giving a constraint on a different smaller set. The goal is to show these constraints are incompatible, for example by an exchange lemma relating cycles of B_xy and B_x′y′ for two splits sharing an element or a sum.

## Update (2026-11-24): two-edge exchange refuted (GPT round, audited)
- **Exchange criterion** (a shared-element or shared-sum swap of two labels, keeping both arcs) and the **frozen-cut theorem**: if {ΣU, ΣV} = {−a, −b}, the exchanged cycle (a, U, b, V) collides for *every* internal ordering. **CORRECT.** The cut vertices a + ΣU and a + ΣU + b depend only on the arc sums.
- **Counterexamples at p = 11, A = {1, 2, 3, 4, 5, 8, 10}: VERIFIED** (`exchange_counterexamples.py`).
  1. Split (5, 1), giving B with t = 6: 44 rooted cycles, 6 blocked. **All 6** are frozen-cut for the exchange to (5, 4) → t′ = 9, even though B′ has a good cycle avoiding 5.
  2. The blocked cycle (9, 4, 10, 5, 2, 3) of split (1, 8) has **no** valid outgoing exchange to any of the 3 splits sharing an element or the sum.
- **Scope.**
  - This refutes local two-edge exchange as a universal mechanism.
  - It does **not** test the global statement: in a minimal counterexample *every* cycle of every B_xy is blocked, whereas here only 6/44 are.
  - Refinement (GPT, correct): FV is needed only for x, y ∉ B (x ≠ y, x + y = t). The FP∀ form suffices, not avoidance of labels already in B.
