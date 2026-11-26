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

## Update 2 (2026-11-24): structured avoidance and global blocking (GPT round, audited)
**Verified** (`sia.py`, `cnt.py`, rerun exactly):
- **Structured inner avoidance (SIA)** never fails: exhaustive p ≤ 17, sampled p = 19 and 23. The strict self-reducing version (s ∉ {x, y}) fails only at |B| ∈ {3, 4}, and only for lack of an admissible pair. Restricted FV for |B| ≤ 4 is proved directly (read).
- **Model obstruction** B = {4, 5, 8, 9, 12, 13} mod 17: K = {0, t}, and the unavoidable pairs are {1, 4}, {9, 13} at t = 5. All 88 structured expansions succeed.
- **Counting identities through p = 13:**
  - (1): 2Σ_e c(B_e) = E_good + N₁ + 2N₂.
  - (4): one-repeat orderings counted by gluing two smaller zero-sum cycles.
  - The bounds c(B_e) ≤ H_e (component) and c(B_e) ≤ J_e (double petal).
  - The combined criterion covers every nonsymmetric set at p ≤ 13; the 6 uncovered sets are symmetric.
- **Not re-run:** the p = 17 dense failure F₁₇^× ∖ {1, 2, 14} (Σ c(B_e) = 5,163,930 < N_one = 17,995,452, and c < min(H, J) for every split).

**Proved (hand-checked).**
- Thm 1/2 (structured criterion and compression form).
- Thm 3 (one-repeat multiplicity ≤ 2).
- **Thm 5 (double petals):** in a minimal counterexample, every admissible split (x, y) has a hub z ∈ {x, y} lying in two zero-sum sets L ∪ {z} and R ∪ {z} that meet only in z. The arcs sum to −y, y − x and −y.
- The double-petal condition is automatic at density > 1/2, so only petal *counts* carry force.

**Assessment (Claude).** The counting bounds are relaxations of identity (1). Making them "compatibility-aware" converges to computing c(B_e) exactly, which is tautological. New force must come from **structure**, not sharper counting: either a proof of SIA, or a structure theorem for minimal counterexamples followed by an explicit treatment of structured sets.

## Update 3 (2026-11-24, Claude): every inner pair works, and the domino hierarchy (DOM)
Code: `mult.c` (per-pair census), `afv2.c` (two pairs), `afvk.c` (k pairs or maximal families). All runs are exhaustive over zero-sum B with |B| ≥ 5, t = 1 after dilation, and every external split x + y = 1 with x, y ∉ B.

| statement | p = 17 | p = 19 |
|---|---|---|
| **AFV**: *each* admissible inner pair (u, v) is adjacent in some x-avoiding t-cycle | 23,602 / 23,602 pairs | 136,907 / 136,907 pairs |
| AFV, 2 disjoint pairs | 35,154 tests, 0 failures | |
| AFV, 3 disjoint pairs | 10,476 tests, 0 failures | |
| AFV, maximal disjoint families | 45,286 tests, 0 failures | running |

Here "admissible" means the pair sums are distinct and outside B ∪ {0, x, y}. The tests were also run at p = 13 with 0 failures.

**DOM (domino conjecture).** For zero-sum B, t ∈ B, and an external split x + y = t, *any* family Π of disjoint admissible pairs in B ∖ {t} (distinct sums, outside B ∪ {0, x, y}) is realised as adjacencies in some valid t-rooted cycle avoiding x. Π = ∅ is restricted FV; |Π| = 1 is AFV, which is far stronger than SIA.

**Induction structure (proved, easy).** Let π = (u, v) ∈ Π and C_π = (B ∖ π) ∪ {s}. Then Π ∖ {π} stays admissible in C_π, and expansion preserves the other adjacencies. So DOM(B, Π) ⟺ [some cycle of C_π realising Π ∖ {π} and avoiding x also has its s-step expandable]. Since expandability is exactly "π adjacent", the naive induction on |Π| is circular. A proof needs a mechanism that *chooses* the C_π-cycle: this is the simultaneous-expansion (pseudoforest) problem of the reverse-rank rounds, now in F_p with no span constraint.

## Update 4 (2026-11-24): DOM, the orientation graph, and switching (GPT round, audited)
- **Cross-check.** GPT's independent SIA census matches mine exactly: 23,602 pairs at p = 17 and 136,907 at p = 19.
- **DOM with maximal families at p = 19: exhaustive, 436,183 tests, 0 failures** (`afvk.c`, Claude).
- **GPT samples:** 500,000 maximal and common-difference-biased matchings at p = 23 and 29, all succeed; one node-capped case was resolved explicitly.
- **Accepted (hand-checked).**
  - The exact polynomial encoding.
  - The **orientation-graph criterion**: for a fixed contracted cycle, simultaneous expansion is possible iff each component is a tree with ≤ 1 forbidden vertex or unicyclic with none. This is the pseudoforest theorem of `simultaneous_contraction_audit.md`, now in F_p.
  - The **closed count** N = 2^|U|·∏_{T ∈ 𝒯₀} |V(T)|. Every factor is < p, so N ≢ 0 (mod p) iff N > 0.
- **Verified obstructions** (`dom_certificates.py`):
  - the joint top Nullstellensatz coefficient vanishes (p = 13);
  - the total witness count is 22 ≡ 0 (mod 11);
  - two dominoes can each be expandable but not together (p = 13);
  - a contracted cycle can be isolated under all 21 tail transpositions, while a 4-segment reversal escapes it (p = 13).
- **Exact remaining gap.** Some valid x-avoiding contracted cycle of C must have a feasible orientation graph. This is cycle selection again, now with an exact feasibility test.

## Update 5 (2026-11-25): fixed orientation up to global reversal is refuted (Astra FV log, audited)
- **Candidate statement.** Prescribe a direction for every admissible pair in Π. Then some ordering of the blocks works with those directions, or with all of them reversed.
- **Counterexample, verified (`orientation_refutation.py`).** p = 13, B = {1, 3, 4, 5, 7, 9, 10}, t = 1, x = 2, with blocks (3,5), (7,4), (9,10).
  - Successful block orders per orientation, in bit order 000 … 111: 0, 0, 1, 0, 1, 2, 1, 0.
  - Both global choices fail.
  - The mixed orientation 010 gives (1, 9, 10, 4, 7, 3, 5).
- **Census (`orientation_census.cpp`, reproduced in 1.8 s).** Failed / total:

  | p | 7 | 11 | 13 | 17 | 19 |
  |---|---|---|---|---|---|
  | failed / total | 0/8 | 0/364 | 16/4,688 | 180/551,000 | 6,076/7,186,240 |

- **Significance: minor.** The orientations must remain individually free. This is consistent with the orientation-graph criterion, under which the orientations are chosen per component. DOM and FV are unaffected.
