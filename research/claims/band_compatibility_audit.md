# Audit: band-compatibility round (flexible pairing for Targets A and B) (Claude, 2026-11-24)
The submission was pasted in chat. No verifier was attached; the family and the compactness numbers were checked inline.

## Accepted
- **Theorem 1 (compatible extreme contraction in the compact band).** The case analysis (all-upper / lower at P / lower elsewhere) was read.
  - The key point is that the contraction deletes exactly one expansion vertex, so simplicity is automatic. The span bound uses t < K ≤ Q and H ≤ P′. Accepted as a candidate.
- **Theorem 2 (±M insertion except for ≤ k − 1 explicit magnitudes).** Accepted.
  - Case I translates the first edge 0 → a. Case II translates the edge (ℓ, t).
  - Each time only one new vertex can hit the upper layer U.
- **Theorem 3 (congruence elimination: M ≢ r, 2r mod g).** Accepted.
- **Family X_s, Y_s (all values ≡ 2 mod 5):** verified for s = 1..7. Equal sums, t = 40s² < K, T/D ≈ 2s; s = 3 gives n = 24, D = 1059, matching the table.

## Scope: compact band forces sparsity (proved, Claude)
**Lemma.** If |X| = |Y| = k and the compact-band condition 0 < t < K holds, then **n = 2k < 4√D.**

*Proof.*
- Under reverse-rank pairing, the k₊ positive differences are distinct positive integers summing to t. The same holds for the k₋ negative ones, with k₊ + k₋ = k. So t ≥ ⌈k/2⌉(⌈k/2⌉ + 1)/2 > k²/8.
- t depends only on the high/low partition, so this also applies to flexible pairing.
- Compactness gives t < K ≤ min(P, Q) ≤ D/2. Hence k² < 4D. ∎

**Consequence.** In F_p terms the compact-band regime covers only |A| = O(√p). The arbitrarily large T/D comes from translating every magnitude away from 0 (narrow band [L, 2L)), not from density. The family has n = 56 at D = 4579.
So the claim to address "dense instances with closely spaced extrema" applies only to clustered, sparse sets.

**Status.** GAP A (multiscale bands) and GAP B (removing the exceptional magnitudes) are open. The dense regime is open.
