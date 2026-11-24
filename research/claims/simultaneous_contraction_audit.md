# Audit: simultaneous-contraction round (Claude, 2026-11-24)
The submission was pasted in chat. Check script: `experiments/audits/simultaneous_contraction/simc.py`.

- **Thm 1, reverse-rank contraction: ACCEPTED.**
  - Statement: for |X| = |Y|, X ∩ Y = ∅, the differences d_i = x_i − y_{k+1−i} are distinct and nonzero, sum to 0, and have diam = D − x₁ − y₁.
  - The proof is immediate (the differences are strictly increasing). Checked on 20,000 random instances.
- **Thm 2, exact simultaneous-expansion criterion: ACCEPTED.**
  - It is the standard orientation (pseudoforest) criterion. Each component must have #edges ≤ #non-forbidden vertices. Connectivity then forces either a tree with ≤ 1 forbidden vertex, or a unicyclic component with none.
  - No loops can arise, because a_i − b_i = x_i + y > 0.
  - The interval-location refinement (§3) is also correct.
- **Obstruction: VERIFIED.** B = (18, −12, 6, −4, 2, −10) from −9 has three edges whose candidate pair is {−50, 50}. The alternative ordering expands to (53, −47, 51, −49, 44, −56, 59, −41, 48, −52, −55, 45), which has distinct partial sums and span 107 < 115.
- **Thm 3, high-mass family: ACCEPTED.**
  - The greedy count checks: 6r + 1 even values in [4r, 16r] against at most 6r − 3 exclusions. Parity rules out inverse pairs, and every new vertex v_i − y_i is < 0 because y_i ≥ 4r > W.
  - **Caveat:** the family is built so that every expanded magnitude exceeds the core span W. It is the same "dominant padding" mechanism as the large-inverse-pair padding theorem. It shows that T/(P + Q) → ∞ is not an absolute barrier, but it says nothing about general dense sets.
- **8.49M-set exhaustive search: NOT REPRODUCED** (no code was supplied). The repo's own data covers the stronger rooted-window statement G\* for values ≤ 15 (`rooted_window_irc.md`, 9.68M instances), which implies span ≤ P + Q − 1.

## Structural limits of the proposed induction
1. **The contraction does not iterate.** Reverse-rank contraction needs equal sign counts and no inverse pairs. The contracted set B generally has unequal sign counts and may contain inverse pairs, so an induction needs a contraction for **general** sets ("general unequal-sign-count contraction", listed as open).
2. **The compatible-core selection conjecture is the cycle-choice obstruction again.** This is the same obstruction seen in merge pairs (`ledger.md`, induction-route item (c)), the arbitrary-cycle expansion counterexample, and `inverse_pair_lift.md`. Theorem 2 gives an exact test for a *given* core cycle, but no reason why some core cycle passes.

**Status.** The new contributions are exact tools: Thm 1, Thm 2 and the interval criterion. The dense case is still open.
