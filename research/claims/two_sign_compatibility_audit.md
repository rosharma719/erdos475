# Audit: two-sign compatibility theorems (Claude, 2026-11-24)
The submission was pasted in chat. Script: `experiments/audits/two_sign_compatibility/` (Python construction plus compiled exhaustive search).

## Reproduced exactly
- **Constructive Theorems A and B** (≤ 2 elements of one sign): every two-sign instance with values ≤ 20 — **22,829 (A) and 60,007 (B), 0 failures.** The script asserts validity and bounded span for both the big and the smaller cycle.
- **Exhaustive check of the unrestricted induction targets through magnitude 15: 5,231,247 (A) + 6,456,900 (B) = 11,688,147 nonsymmetric instances, 0 counterexamples.** The rerun took 17 s and matches the per-magnitude table.
- **Fixed-order q = 2 obstruction** (V = (0, 1, 6, 9, 11, 8, 2), insert ±7): 30 collisions, and the remaining spans are 16, 17 and 18, all > 14. **Verified.**

## Assessment
- **Theorems A and B: accepted as candidates.**
  - The case analysis (strict crossing, equal-peak bridge, moderate mass, Q > b) was read. The key mechanisms check out: translating a whole monotone path by ±M into an empty range, and the two-sided contraction choice at the large positive step.
  - The case split is long. Exhaustive verification of the implemented construction up to values 20 is the main evidence that no case is missing.
- **Scope.** "≤ 2 elements of one sign" is index ≤ 2, the sparse end. These results are the **base case** of the induction: a minimal counterexample to Target A or B needs ≥ 3 elements of each sign (after removing ±M for B).
- **Significance of the data.** Targets A and B together imply BS by induction, and hence Graham (with `extreme_compatibility_audit.md`). They now hold in 11.7M instances. This is the strongest evidence yet that the induction statements are true, but evidence is not proof.

**Open.** Targets A and B for ≥ 3 elements of each sign (multi-peak cycles). This needs path-endpoint relations, because unrestricted k-path separation is false.
