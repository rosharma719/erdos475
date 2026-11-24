# Rooted symmetric cycles and one-merge near-symmetric pairs (Claude, 2026-11-24)
Code: `experiments/exploration/rooted_symmetric/`. Programme C.

Throughout, S is a finite set of positive integers, M = max S, and b₂ > b₃ are the two largest elements of S ∖ {M}.

**RS+(S, r)** means: ±S has a valid cycle whose first step is +r and all of whose vertices lie in [−M, M].

## Theorem 1 (rooting criterion), proved
Let r ∈ S ∖ {M}. Suppose δ is a signed ordering of S ∖ {M} (each element once, either sign) such that:
- its partial sums D (D₀ = 0) are distinct;
- span(D) ≤ M − 1;
- the step of δ equal to −r lands on min D.

Then RS+(S, r) holds.

*Proof.* W = (δ, +M, −δ^rev, −M) is a valid cycle of ±S. Its vertex set is D ∪ (D + M), and the two parts are disjoint because span(D) < M. This is the half-walk lemma L6.

Say δ_k = −r with D_k = min D. Then in −δ^rev the step +r leaves the vertex M + D_k. Rotate W to start there and translate by −(M + D_k). The vertex set becomes (D − D_k − M) ∪ (D − D_k), which lies in [−M, max D − D_k] ⊆ [−M, M − 1]. ∎

## Theorem 2 (two explicit templates), proved
Let R = S ∖ {M, r}, listed in decreasing order as d₁ > d₂ > … > d_j, and let A_i = d₁ − d₂ + … ± d_i (A₀ = 0).

**(a) Spiral-after-root.** If r ∉ {A₁, …, A_j}, then δ = (−r, +d₁, −d₂, +d₃, …) satisfies Theorem 1.
- *Proof.* By the descending-alternating lemma (`symmetric_irc.md`), the A_i are distinct and lie in [0, d₁], with A_i > 0 for i ≥ 1. So D = {0} ∪ {−r + A_i}.
- These vertices are distinct, and the hypothesis says none of them is 0.
- min D = −r, reached by the step −r.
- span(D) = max(r, d₁) ≤ b₂ ≤ M − 1. ∎

**(b) Outward spiral.** If r ∈ {b₂, b₃}, take the elements of S ∖ {M} in increasing order e₁ < … < e_m with alternating signs. Choose the first sign so that the step of magnitude r is a down step.
- *Proof.* Each step is longer than the current span e_{i−1}, so it lands on a new extreme. Hence all vertices are distinct, and span = e_m = b₂ ≤ M − 1.
- The global minimum is the landing point of the last down step. The last down step has magnitude e_m or e_{m−1}, i.e. b₂ or b₃.
- Case m = 1: δ = (−r). ∎

## Corollary 3 (IRC+ for one-merge near-symmetric pairs), proved
Let r ∈ S ∖ {M} satisfy (a) or (b). Let y ∉ S with r + y > M, and set
  P = (S ∖ {r}) ∪ {r + y}, N = S ∪ {y}.
Then (P, N) has a valid cycle with range ≤ max P + max N. This is IRC+, and it gives Graham for every prime p > max P + max N.

*Proof.* Take the RS+ cycle and replace its first step +r by (+(r + y), −y). This is the max-root lift of `rooted_window_irc.md`.
- The new vertex r + y exceeds M, which is at least every old vertex, so it is fresh.
- All other vertices lie in [−M, M], and the range is ≤ r + y + M ≤ max P + max N. ∎

**Why this matters.** S is arbitrary, so the family includes dense pairs with no top gap and with unbounded index (number of sign changes). This is the regime where every earlier route stalled; previously only symmetric sets were proved there.
**Limitation.** Neither template covers the tight family, which is S = [1, M] ∖ {b} rooted at a small a. Interval-like S makes A cover almost every value, so (a) fails, and a small root is never b₂ or b₃.

## Coverage, finite information only
- **Templates alone** (`rs3.py`, values ≤ 12, all S and r ≠ M): (a) covers 62% of cases; (a) ∪ (b) ∪ split-spiral variants cover 87%.
- **Every uncovered case still satisfies RS+** (`rs4.py`, values ≤ 9): of 188 uncovered cases, 84 have some half-walk satisfying Theorem 1 and the other 104 need a general walk.
- So RS+ seems to be true in general, but half-walks alone cannot prove it.

**Next target.** Prove RS+ for every root. A proof needs a template beyond half-walks for about half the hard cases, starting with S = [1, M] ∖ {b} and small r, which is exactly the tight family.

## Addendum (2026-11-24): the smallest root
For r = min S (all S with values ≤ 14 and 2–11 elements, 16,263 sets), templates (a) and (b) plus the split-spiral variants leave **5,195 (32%) uncovered** (`rs5.py`).
- The first family is S = {1, k, k+1, k+2} with r = 1. Here R = {k+1, k}, the alternating sums are {k+1, 1}, and r = 1 collides.
- Together with `rs4.py` (half the hard cases have no half-walk at all), this shows that small roots need a construction that is **not** of the form (δ, +M, −δ^rev, −M).
- No such construction is known. This is the open core of the spiral route, and it contains the tight family.

## Addendum 2 (2026-11-24): the tight family in half-walk form
For S = [1, M] ∖ {b} with root a, Theorem 1 asks for a path P on [0, M−1] with:
- exactly one hole;
- steps [1, M−1] ∖ {b}, each used once;
- the edge a → 0 into the minimum.

Results:
- **Exhaustive search (`hw.py`)** finds such paths for every 2 ≤ a ≤ 4 and every M tested (up to M = 21 for a = 4). So the tight family is solvable inside the proved Theorem 1 template, and the general walks that small roots of other sets need are not required here.
- **Observed shape.** a → 0, then an inward zigzag (0, M−1, 1, …) whose lows skip a and whose highs skip M−2, then a detour to M−2, one hole, and an irregular tail.
- **Simple families fail.** A pure skip-zigzag (`zz.py`) and "zigzag + one detour + one hole" (`fam.py`) each cover only a few (M, a). An explicit all-M formula needs a tail gadget that depends on M and a mod small numbers.
- **Status:** not proved. This is the most concrete closable gap: an explicit graceful-type path construction.
