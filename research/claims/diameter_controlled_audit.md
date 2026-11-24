# Audit: diameter-controlled contraction and cardinality-free insertion (Claude, 2026-11-24)
The submission was pasted in chat. No verifier was attached; the key claims were checked inline.

## Accepted (hand-checked)
- **Theorem 1 (safe contraction under P′ + Q′ < P + y and P′ + Q′ + y ≤ P + Q).**
  - The candidates t± are P + y > W apart, so at most one is occupied.
  - If neither is occupied, failure of both would force P + y > 2D − W ≥ D, which is impossible.
  - If t₊ is occupied, then H − t₊ ≤ W − P, so adding t₋ gives span ≤ W + y ≤ P + Q. The t₋ case is symmetric, using t₋ + P = z + c ∈ V.
  - **Every bounded smaller cycle expands.** This is a genuinely safe induction step under the diameter conditions.
- **Rules A and B.** Direct corollaries. Rule B's formula D(B) = P − y + Q assumes y ≠ Q.
- **Theorem 2 and the family X = {1, …, k−1, 2k+1}, Y = {1, …, k+1}.** The contraction gives exactly ±[1, k], and both inequalities hold. Verified for k = 3..29.
- **Theorem 3 (insert ±M as (M, −Q, −M) for M > P and M ≥ Q + h).**
  - The new vertices u + M and h + M both exceed v = P + h, and u + M ≤ 2M.
  - Valid for all sign cardinalities.
- **Theorem 4 (safe band) and the equal-extreme extension.** Read, not re-derived.
- **Minimum-span obstruction:** VERIFIED. The cycle (2, −1, 4, 1, −2, 3, −4, −3) has optimal span 7. Every insertion of ±5 either collides or has span 11–12, never ≤ 10. So "pick a minimum-span core" is not enough.

## Scope
- **The safe rules need a dominant top.**
  - Rule A needs P₂ + Q₂ ≤ P.
  - Rule B needs some y with Q/2 < y < P − P₂.
  - The high-mass family has P = 2k+1 against P₂ = k − 1.
- These are top-gap conditions, like `bs_handoff_audit.md`'s top-gap lift. They give arbitrarily large T/D, but only when the top element stands far above the rest.
- **The open regime is unchanged:** dense sets whose extreme magnitudes are closely spaced (no top gap). The submission's own frontier says the same.
