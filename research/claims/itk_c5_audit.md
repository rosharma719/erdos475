# Audit of Astra's IT(k) / C5 round (complete) (Claude, 2026-11-26; branch codex/itk-counterexample @ 46842af, fast-forwarded into claude/amazing-maxwell-wfz06f)

## Hand-checked, correct
1. **IT(k) cut counterexample** (`integer_two_path_cut.md`).
   - Setup: k = M = 31, with T = {−18..−1} ∪ {5..15} ∪ {30, 31}.
   - Every step 16..29 must cross the cut [0,15] | [16,31] upward. Only the 13 negative labels −19..−31 can cross downward. A closed walk crosses the cut equally often in each direction, so no closed walk exists.
   - **My unrestricted IT(k) is false.** It had been tested only for M ≤ 13 and k ≤ 7, where k ≪ M.
2. **One-step extension.** Set P′ = (0) ‖ (q − Q) and Q′ = (0) ‖ (q − P).
   - Both paths stay simple, and their common endpoint is q − y > 0.
   - The labels become I_q ∖ T.
   - The converse also holds for q > M: both ±q present forces the first edge 0 → q on both paths.
3. **Closure.** Go P, then +r, then r + rev(Q), then −r.
   - The two halves lie in the disjoint intervals [0, r−1] and [r, 2r−1].
   - The labels are I_r ∖ T, which is F_p^× ∖ λH.
4. **Dilation for k = 5.**
   - Some integer coordinate sum occurs more than 7r⁴/24 times. This follows from the variance (5(r² − 1)/12) and Chebyshev's inequality.
   - 7r⁴/24 > (2r + 1)³ for r ≥ 30.
   - Pigeonhole over the p³ translation orbits of the sum hyperplane then gives an integer difference ≡ λH. That difference is zero-sum with height ≤ r − 1.
   - Hence the result holds for every p ≥ 61.
5. **General-k dilation.**
   - Condition (1) gives a slice larger than p^{k−2}.
   - Rescaling by d = ⌈2k/m⌉ ≤ 4 gives height in [2k, 4k) ⊂ [2k, r − 1].
   - Bernoulli's inequality gives the closed-form range p ≥ max{8k + 1, k·2^{k−1} + k − 1}.
6. **Graceful-segment refutation** (`c5_two_blocks.md`). W = {1, 3, 7, −2, −4, −5} sums to 0, so it cannot be a run of consecutive differences.
   - The C5 gadget only needs ΣW = s ≠ 0, so this does not affect C5.
   - Separately, the paired orbit {1, 3, 11, 17, 26} at p = 29 has no six-window at all (exhaustive, no cutoff). The two-block lemma replaces the six-window.

## Verifiers re-run here
- `verify_integer_two_path_cut.py`:
  - the 31-hole obstruction has net crossing in [1, 5] for every placement;
  - the 11-hole example has minimum width 9 over all 120 orders.
- `verify_interval_lift.py --height 14`: every integer 5-set has a seed at every height M ≤ 14 (2,154 sets).
- `verify_two_blocks.py`: every orbit is certified at every prime p ≤ 61. At p = 61 that is 1,493/1,493 orbits (89,532 sets).
- `verify_interval_lift.py --primes 67 … 113`: every orbit is certified at every one of these primes, from p = 67 (2,021/2,021) to p = 113 (10,600/10,600). All counts match Astra's table.
- **Hence C5 is confirmed for every prime p ≤ 113.**

## Status after this round
- **C5 holds for every prime p ≤ 113.** The certificates cover all 7,174,166 zero-sum five-sets.
- **C5 for all primes ⇐ IT(5) at every height M ≥ 15.** Heights M ≤ 14 are verified exhaustively.
  - IT(5) (the "boundary seed assertion"): every zero-sum integer 5-set T has two paths in [0, M], both from 0 to a common y > 0, whose labels are exactly I_M ∖ T.
  - The cut obstruction cannot occur for k = 5 once M ≥ 10, since the dense hypothesis M ≥ 2k then holds.
- **Complement-k at every prime p ≥ max{8k + 1, k·2^{k−1} + k − 1} ⇐ the dense integer two-path conjecture (M ≥ 2k).**
  - That conjecture would give an explicit dense-regime theorem for |H| ≲ log₂ p.
  - This is better than the log p / log log p I had estimated.

**Next proof target:** IT(5) for M ≥ 15. It is a single p-free statement about five integers, and its proof finishes C5 at every prime.

## IT5 checkpoints 1–7 (Astra; merged from codex/itk-counterexample), audited by Claude
- **Hand-checkable family, verified independently for N = 1..59, all valid.** The family is M = 26N − 1 with T = {−M, 2N, 6N−1, 8N, 10N}. Each instance was checked by rebuilding both paths and recomputing their labels.
- **Paired holes with a unit triple, proved and checked by building the paths.** The family is T = {±h, 1, c−1, −c}. All 2,072 cases with 3 ≤ c < 40 and h < 60 are valid.
- **Affine rays, re-checked independently.** 45 certified rays: `it5_affine.py --manifest` replays them all.
  - I rebuilt the paths myself at n = 0..40, 100, 333 and 1000: 1,980/1,980 valid.
  - The ray argument (affine comparisons with slopes that preserve their sign) is accepted.
- **Refutation of the common nested tail on the balanced 1+4 region: correct.** In that region the forced alternating tail visits the first intermediate prefix vertex.
- **Status.** IT5 is proved for:
  - the paired unit-triple family;
  - the arithmetic nested-tail class at the heights checked: 1,515 of 26,435 normalised inputs at M = 15..30;
  - 45 infinite rays;
  - one explicit infinite family.

  The general case is open. The balanced 1+4 region (2 ≤ a < b < c < d < M/3) needs a different construction.
