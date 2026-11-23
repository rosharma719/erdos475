# Audit: "tight half-walk offsets" submission (Claude, 2026-11-23)

The submission is verbatim in `tight_halfwalk_offsets_submission.md`. It answers the c=1 round (`prompts/gpt_round_offsets.md`, L18/L19 in `claude_lane.md`).
Code: `experiments/audits/tight_offsets/`.

## Part 2: divisibility theorem for offsets. ACCEPTED (proof checked, plus exhaustive check)
**Claim.** M distinct integers with no two differing by c fit in L = 2M+3−c consecutive positions (1 ≤ c ≤ M) iff c divides one of M, M+1, M+2, M+3.

**Checks.**
- The formula for α_c(L) (residue chains mod c; a path on ℓ vertices has independence number ⌈ℓ/2⌉) matches brute force for all L ≤ 14.
- The iff holds for all 1 ≤ c ≤ M ≤ 3000, with 0 mismatches.
- All four tables in the submission (M = 24, 40, 100, 400) are reproduced exactly.

**Necessity.** The algebra for both q = 2h+1 and q = 2h was re-derived and is correct.

**Sufficiency gap, now closed.** The submission's sufficiency step ("alternating blocks") is only sketched. A complete version follows from the formula for α. Suppose c | M+j.
- j ∈ {0, 1}: then L = (2h+1)c + (3−2j). If c > 3−2j this gives α = (h+1)c ≥ M.
- j ∈ {2, 3}: then L = 2hc + (c+3−2j). If c ≥ 2j−3 this gives α = M+3−j ≥ M.
- c ≤ 3: α ≥ ⌈L/2⌉ ≥ M directly.

**Consequence.** The theorem strictly refines the offset-window part of L19, and the two are consistent: divisors of M..M+3 that lie in ((2M+2)/3, M) do not exist.
This is a packing condition only. It is necessary for a tight half-walk, not sufficient.

## Part 1: parity obstruction to the single-gap c=1 form. PARTLY CORRECT
- **(1) R ≤ 2·min(n0, n1), with R = ⌊(M−1)/2⌋ odd lengths. ACCEPTED.** This is valid for every c=1 half-walk.
- **Odd M, odd a. ACCEPTED, and holds in general.** The proof extends to any translate t of the single-gap form. Upper-column points all exceed lower-column points.
  - If the lower column is even, it contains 0 and M+1, so the odd a would have to exceed M+1.
  - If the lower column is odd, it contains a, so 0 would have to exceed a.
- **Even M, odd a < M/2 "excluded". TRUE ONLY IF min D = 0.**
  - The argument takes E = {0, 2, …, 2k}, a normal form copied from the round prompt. The half-walk lemma (L6) normalises the *start vertex* D_0 = 0, not min D.
  - With min D = t (even, t ≤ 0) the same argument gives only a ≥ M/2 + t.
  - Explicit counterexamples to the unnormalised claim, each a valid ordering of the tight pair with range ≤ 2M+2 and distinct partial sums mod p = 2M+3 (`witness.py`):

| M | a | D (single gap, t) | path on D |
|---|---|---|---|
| 10 | 3 | {−2, 0} ∪ {3, 5, …, 17}, t=−2 | 13, 9, 15, 17, 7, −2, 5, 0, 3, 11 |
| 14 | 3 | {−4, −2, 0} ∪ {3, …, 23}, t=−4 | 17, 13, 19, 11, 21, 23, 9, −4, 7, −2, 5, 0, 3, 15 |
| 14 | 5 | {−4, −2, 0} ∪ {3, …, 23}, t=−4 | 19, 13, 11, −2, 7, −4, 3, 0, 5, 15, 23, 9, 21, 17 |

  - Exhaustive over all translates for even M ≤ 14 and odd 3 ≤ a < M/2: forms exist only at (10, 3), (14, 3) and (14, 5), each with t < 0. None exist at (8, 3), (12, 3) or (12, 5).

**Corrected statement.** In the single-gap c=1 form with lowest vertex t, even M and odd a force a ≥ M/2 + t. Odd M with odd a is impossible.
So the single-gap form is not dead for even M, but it needs the column to extend below the start vertex.

**Status.** Part 2 is a candidate (proof complete, finite check M ≤ 3000). Part 1 is a candidate in its corrected form. The single-gap family for even M is still open: the data at M ≤ 14 is sparse, so no conclusion either way.
