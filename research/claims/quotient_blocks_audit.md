# Audit: quotient-block lifting round (Claude, 2026-11-24)
The submission was pasted in chat. Script: `experiments/audits/quotient_blocks/`.

## Accepted
- **Interval-walk lemma: ACCEPTED.** All steps lie in [−Q, P] and the endpoints lie in [L, L + D]. Rule: positive if z ≤ L + Q, negative otherwise. Then z stays in [L, L + D]. A monotone tail heads toward an in-range endpoint.
- **Quotient-block lifting theorem: ACCEPTED.**
  - *Setup.* The blocks Cᵢ have distinct nonzero sums dᵢ ∈ gℤ, are minimal zero-sum mod g, and have pairwise disjoint proper-subset-sum residue sets Rᵢ.
  - *Claim.* Then **every** bounded simple cycle of B = {dᵢ} lifts. This is the first fully *safe* expansion in the programme: no core-selection problem arises.
  - *Proof check.* An internal vertex of block i is ≡ (prefix sum of Cᵢ) ∈ Rᵢ, and 0 ∉ Rᵢ. Core vertices are ≡ 0. Within a block, a repeat would need a zero consecutive run mod g. Across blocks, the Rᵢ are disjoint.
- **Induction corollary** (pair contraction with residue-distinct classes {±rᵢ}): ACCEPTED.
- **Triple-block family** (unequal sign counts, T/D and t/D both → ∞): ACCEPTED. The script verifies k = 1..100, and the table reproduces exactly.
- **Band solution of the X_s, Y_s obstruction family:** VERIFIED for s = 1..100. The s = 2 word has span 29 < 31.
- **Inverse-pair restriction** (g | a for every ±a ∈ A): ACCEPTED.

## Scope: a hard density ceiling (proved, Claude)
Combine the submission's capacity inequality n − b ≤ Σ(mᵢ − 1) ≤ g − 1 with:
- b ≤ D/g (b distinct nonzero multiples of g in an interval of length ≤ D that contains 0), and
- b ≥ 2 (B is zero-sum, so g ≤ D/2).

This gives
  **n ≤ g − 1 + D/g ≤ D/2 + 1** for 2 ≤ g ≤ D/2.
The maximum of g + D/g over that range is attained at the endpoints.

**Consequence.** For the integer lift of A ⊆ F_p we have D ≤ p − 1. So **quotient separation can never apply when |A| > (p + 1)/2**, and the densest half of Graham's problem is out of reach.
**Heuristic (not proved).** Below that density the true limit is probably far smaller. Erdős–Heilbronn / Olson-type bounds give |Rᵢ| ≳ mᵢ²/2 rather than mᵢ − 1, which would confine the method to n = O(√D), the sparse regime.

**Status.** The safe-expansion mechanism is a real new tool for structured (residue-clustered) sets. The dense regime is still open. The next obligation (expansion with overlapping residue supports) is exactly where the cycle-choice obstruction returns.
