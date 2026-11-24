# Audit: overlapping quotient-block lifting round (Claude, 2026-11-24)
The submission was pasted in chat. Script: `experiments/audits/overlap_lifting/`. The rerun reproduces every claim.

## Accepted
- **Weighted-overlap lifting theorem + peeling test: ACCEPTED.**
  - An earlier block j contributes internal vertices with pairwise distinct residues mod g (a repeat would need a consecutive run ≡ 0). So at most min(|C_j| − 1, |R_i ∩ R_j|) of them can block block i.
  - A single-sign block dodges ≤ |C_i| − 1 points by the grasshopper lemma (IMO 2009 P6).
  - Peeling from the end is an exact test for the ordering condition.
- **Mixed-sign capacity ≥ 1 (reflection condition): ACCEPTED.** Reversing a block reflects its internal vertices about the edge midpoint. The condition "no two disjoint subsets with equal sums mod g" makes the two versions disjoint.
- **Forest-overlap exact criterion (tree recursion): ACCEPTED.** Separate subtrees share no residues.
- **Overlapping family with ±1 (g = 2k + 1):** VERIFIED for k = 4..100, with span D − 1 and T/D → ∞.
- **Incompatible forest core:** VERIFIED. The exhaustive minimum span is 10,965 against D = 10,289.
- **No-quotient obstruction A = {−7, −6, −5, −4, 2, 3, 4, 6, 7}: VERIFIED** by exhaustive search over g ∈ [2, 7]. A has the valid ordering (−7, −6, 2, 3, −4, 6, 7, −5, 4), with span 14 = D.

## Significance
**A firm negative result.** Universal minimal quotient contraction is **false**: some sets have no admissible quotient core at all, under the stated admissibility rules. This ends the quotient architecture as a route to the full conjecture.
**What survives.** The positive tools (weighted overlap, reflection capacity, forest DP) are fixed-core tests and lifting tools for structured families.

**Remaining.** The submission's own recommendation, contraction without a common modulus with direct collision control, brings back the general cycle-choice problem (`inverse_pair_lift.md`, `simultaneous_contraction_audit.md`). The dense regime is open.
