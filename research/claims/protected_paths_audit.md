# Audit: protected-path round, plus the run-count obstruction (Claude, 2026-11-24)
The submission was pasted in chat. Its script is in `experiments/audits/protected_paths/`, with the rerun output in `exhaustive.out`.

## Audit
- **Forbidden-height lemma: ACCEPTED, known.** Statement: if A has m distinct positive elements with total T, and F ⊂ (0, T) with |F| ≤ m − 1, then some ordering of A has no partial sum in F.
  - This is IMO 2009 Problem 6 (the grasshopper problem). The cited Math.SE thread "Dodging permutation sums" gives the standard induction.
  - The three-case proof given was read and is correct.
- **Unequal-cardinality theorem** (n ≥ m + 2 or m ≥ n + 1): ACCEPTED. It is a direct application of the lemma, and the forbidden-set counts check out.
- **Theorems A, B and C (reserved blocks): ACCEPTED as candidates.** The proofs were read for the counting; the edge cases rely on the script's assertions.
- **Localization theorem** (at most two collisions, one on each side of h): ACCEPTED as a candidate.
  - Below h, both prefixes up to t₂ have total t₂, so the equal-endpoint separation lemma applies.
  - Above h, the unequal-endpoint lemma applies.
  - The boundary-localization step was not independently checked.
- **Computation reproduced exactly:** 28,582 instances (P ≤ 12); 16,562 solved by proved constructions; 12,020 outside the sufficient tests, which are not failures. Every constructed cycle passed the script's validity assertions.

## Run-count obstruction, proved
**Lemma.** A valid cycle with span ≤ D has at least ⌈T/D⌉ maximal ascending runs, where T is the positive mass.
*Proof.* Each run climbs by at most D, and the climbs sum to T. ∎

**Consequence.** Peak removal and all its protected-path refinements have two climbs: X′, with rise T − P, and the step +P. So their span is ≥ T − Q, and they can reach span ≤ P + Q only when T ≤ P + 2Q.
- A dense set (n elements with values up to M) has T ≈ nM/2. A bounded-span cycle for it therefore needs Ω(n) runs.
- So the handoff's "GAP 2" (going beyond T ≤ P + Q + min(P, Q)) is not a boundary case: it is essentially the whole conjecture. Any finite-run method, including k-path separation (which is false for k ≥ 3 in any case), cannot reach it.
- The only constructions known to reach the dense regime are many-run spirals: the symmetric walk, and the rooted-symmetric and one-merge families (`rooted_symmetric.md`).

**Recommendation.** Put the effort into many-run spiral constructions, in particular RS+ for all roots. Protected paths should stay a tool for sparse regimes only.
