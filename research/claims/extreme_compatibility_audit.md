# Audit: unequal-extreme rectification and extreme-compatibility round (Claude, 2026-11-24)
The submission was pasted in chat. Script: `experiments/audits/extreme_compatibility/`.

## Accepted (hand-checked)
- **Unequal-extreme rectification: ACCEPTED.** Dilate an unpaired element to M = (p−1)/2.
  - If P = Q, then b_{n−k} + b_{n−k+1} = p. The cut is then at p/2, so the lift is the centred one, with P = M (present) and Q < M ((p+1)/2 absent). Contradiction.
  - **Consequence: Graham ⇐ (symmetric construction, proved) + BS for unequal-extreme integer sets.**
  - Caveat (also in the submission, verified by script): an extreme-contraction induction can leave the unequal class. For example {−5, −4, −3, 1, 5, 6} reduces only to equal-extreme, non-symmetric sets.
- **Separated (arc-translation) expansion criterion: ACCEPTED.** The second insertion translates an arc, and validity means disjointness plus diameter.
- **Arbitrary-arc maximum-pair insertion criterion: ACCEPTED.** Only max(S + M) − min T can exceed 2M, because the other cross term is ≤ W − M < M.
- **q_M(V) ≤ 1 absorption theorem: ACCEPTED.** The neighbours of the minimum lie in (0, M), and at most one of them has an occupied M-translate. Otherwise reflect about the maximum.
  - The density refinement |V| > 2s + 2q_M is also accepted.

## Verified computationally (rerun)
- **Fixed-core separated-expansion obstruction:** {−4, −3, −2, −1, 2, 3, 5} with core (1, −3, −2, −1, 2, 3) has no expansion with span ≤ 9. The alternative core gives (5, −4, −3, −1, 2, 3, −2), span 8.
- **Exhaustive check of both induction targets** (each smaller cycle within its own diameter): rerun through magnitude 10 matches exactly, **8,655 (A) + 11,170 (B) = 19,825 instances, 0 failures.** Magnitude 11 (claimed 22,061 + 28,480) was not rerun.

## Status
- **Strongest new reduction:** Graham ⇐ BS for unequal-extreme sets. This is proved.
- **Open:** Targets A and B. Both are "vertex-set flexibility" (choose the smaller cycle so the required translations ±x, ±y, M are compatible). This is the cycle-choice problem, supported by data, with no proof mechanism yet.
