# Audit: imbalance-carrying constructions and the GAP B counterexample (Claude, 2026-11-24)
The submission was pasted in chat. Script: `experiments/audits/imbalance_core/`. The rerun passes every assertion.

## Verified
- **GAP B as stated is FALSE.** The flexible-pairing core W for X = {57, 59, 60, 64, 65, 66, 67, 77}, Y = {26, 57, 67, 68, 69, 73, 76, 79} (t = 61, H = 66, K = 67) comes with an exact greedy transcript.
  - Every insertion of ±83 into distinct gaps either collides (215) or has span ≥ 172 > 166.
  - All three final-expansion switches fail.
  - The alternative core W′ succeeds, with span 150.
  - **Conclusion:** the core must be *selected*. Repairing a prescribed core cannot work.
- **Singleton-group compatible insertion:** proof read and accepted. Checked on 5,984 + 828 cases.
- **Block-extrema theorem** (monochromatic blocks, each jumping over the previous span): ACCEPTED.
  - It carries imbalance between blocks.
  - The family B_m = (4A_m ∖ {8}) ∪ {1, 2, 5} is verified for m ≤ 300, including both compatibility operations.
- **Block-extrema barrier** |X| − |Y| ≤ 2 + 2√D: ACCEPTED. The extras total ≤ D, and each magnitude appears at most twice, so E ≤ 2√D.
- **Dense triple lifting (constant modulus 3): ACCEPTED.**
  - Core vertices ≡ 0, first-layer vertices ≡ 1, second-layer vertices ≡ 2 (mod 3), and the greedy choice keeps each layer injective.
  - Verified for r ≤ 300 symmetric cores and 59 asymmetric cores.
  - Density is linear but small (r = 300: n/D ≈ 1.7%).

## Scope
- All the dense results **construct sets around a chosen core**.
- The reformulated GAP A, "a compatible decomposition of an arbitrary given dense set", is equivalent in difficulty to the conjecture itself.
- GAP B (coordinated core selection) is the cycle-choice problem.
- No change to the assessment in the 2026-11-24 progress review: progress is on constructed families, and the generic dense case is open.
