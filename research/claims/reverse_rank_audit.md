# Audit: reverse-rank core selection round (Claude, 2026-11-24)
The submission was pasted in chat. Script `experiments/audits/reverse_rank/rr.py`; rerun output `rr.out`.

- **Lemma 1, separating threshold (max mᵢ < min Mᵢ): ACCEPTED.** The proof is correct (the differences increase and change sign once), with 0 violations on 20,000 random instances.
- **Degree ≤ 2, no long cycles, at most one double edge (Thm 1): ACCEPTED as a candidate.**
  - Under t < K, the candidate layers sit strictly below 0 and strictly above t.
  - Order preservation along each path is correct.
  - The two-frontier double-edge argument mirrors the protected-path greedy.
- **Thm 2 (constant pair sum, t ≤ S/2) and Thm 3 (t < K, t + 2H ≤ P + Q): ACCEPTED as candidates.**
- **Rerun matches exactly:** constant 27,152; core structure 15,828; compact 412 (0 failures); shifted greedy 18,269 with 9 incompatible.
- **16-element obstruction and its repair: VERIFIED.** The repaired word has 16 distinct partial sums and span 585 < 791.

## Scope: these theorems are for clustered sets, not dense ones
All the new results need the compact-core condition t < K. Here t = ½Σ|dᵢ| and K = min Mᵢ.

**Data.** For values spread over [1, 200], the fraction of balanced, inverse-pair-free sets satisfying t < K is: 100% at k = 2, 40% at k = 3, and **0% for every 4 ≤ k ≤ 12**. The submitted tests reach many elements only by shifting every value by +10000, which clusters the set near a common level.

**Why.** The reverse-rank differences of a spread-out set have magnitudes comparable to the window, so t grows like k·(window)/4 while K ≤ max. A dense set in F_p lifts to values spread over (−p, p), so t < K fails for every k beyond a constant.

**Conclusion.** Like peak removal and protected paths (whose limit is the run-count lemma), this route covers a regime of bounded effective index (clustered sets) and does not reach the dense case. The open problem is unchanged: compatible-core selection for **non-compact** cores, with unequal sign counts.
