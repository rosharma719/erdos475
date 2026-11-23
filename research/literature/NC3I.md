I couldn't confirm the principal gap. I never saw the text of HOS Lemma 4.5, so its exact hypotheses are UNVERIFIED and NC3I still depends on a statement I haven't checked. The search tool hit its usage limit after two successful queries, before I could open the arXiv full text. I did find one unrefereed source that seems to give a route to NC3I without Lemma 4.5.

## CONFIRMED sources (seen this session)

**1. Hicks, Ollis, Schmitt (HOS), "Distinct partial sums in cyclic groups: polynomial method and constructive approaches."** J. Combin. Des. 27 (2019) 369–385, arXiv:1809.02684. The bibliographic details are confirmed (Journal of Combinatorial Designs. 2019; 27: 369–385; arXiv listing: 18 pages Subjects: Combinatorics (math.CO)).
- The paper is framed around **Alspach's** conjecture, not Graham's: "We consider the following conjecture of Alspach: for any cyclic ...". The abstract says the constructive results are "by direct construction, the latter is nonconstructive and uses the polynomial method".
- The abstract I saw had the math symbols stripped out, so I could not read the exact ranges. **Lemma 4.5 itself was not seen.**

**2. dsmic/graham-p-minus-3 (GitHub; not peer-reviewed).** This matters for the contract in two ways.
- **Possible error in the ledger's account of HOS.** The repo says the p−3 result in HOS covers only sets with nonzero sum: "Sum ≠ 0, size p − 3: J. Hicks, M. A. Ollis, J. R. Schmitt, Distinct partial sums in cyclic groups: polynomial method and constructive approaches, J. Combin. Des. 27 (2019), arXiv:1809.02684, Theorem 4.6, proved for Alspach's version." It also notes that some summaries attribute "p − 3 ≤ |A| ≤ p − 1" to Hicks–Ollis–Schmitt without the restriction to sum ≠ 0.
  - A complement {x, y} gives a zero-sum A only when y = −x. So the case this would leave unpublished is exactly C = {±x}, which is the base object NC3I needs.
  - The ledger's line "HOS prove |A| ≥ p−3" / "published covers c ≤ 2" should be re-checked against the HOS text.
- **A direct route to NC3I.** The repo states "Let m be odd and x ∈ ℤ_m coprime to m. Then ℤ_m ∖ {0, x, −x} has an ordering with pairwise distinct partial sums." It adds that putting any element a last and dropping it "settles Alspach's conjecture for all sets of size p − 4 whose complement contains a pair ±x."
  - The logic checks out given that theorem. B = ℤ_p^*∖{±u} sums to zero, so a valid ordering of B is a valid cycle (last partial sum 0, the earlier ones distinct and nonzero). Rotate so v is last and drop it. This gives a valid ordering of A = ℤ_p^*∖{u, −u, v}, with nonzero partial sums as well.
  - The theorem is unrefereed, and I did not see its proof. Only its statement is confirmed.

**3. Costa et al., "Some new results about a conjecture by Brian Alspach,"** arXiv:2003.05939. They say "Working with the methods developed by Hicks, Ollis and Schmitt, based on the Alon's combinatorial Nullstellensatz, we prove the validity of such conjecture for subsets A of size 12." This covers small |A| only; it is not relevant to |A| = p−4.

## Hypotheses to flag for the contract

- **A is never zero-sum here.** ΣA = −(u − u + v) = −v ≠ 0. So "rotation validity for a zero-sum set" applies only to the intermediate cycle of B = ℤ_p^*∖{±u}, or to the full rotational sequencing. It never applies to A. The prover should state precisely where rotation is used.
- **Cycle-level validity.** Contracting the window (δ_{r−1}, r, −δ_{r−1}) into its sum r keeps validity because the new points are a subset of the old ones. That is the ledger's contraction lemma, not something from HOS. It needs the full sequence of ℤ_p^* to be a valid cycle (an R-sequencing), so the rotational-sequencing claim also has to be checked in HOS.
- **Lemma 4.5 is UNVERIFIED.** I could not confirm:
  - the claimed statement ("graceful permutation of [1..r] with a prescribed last difference d");
  - the claimed exceptions (d, r) ∈ {(2,4), (2,5), (2,8)};
  - whether the difference is prescribed at the first or the last end;
  - whether d is signed or an absolute value.

  None of these should be used as established. Since p ≤ 37 (r ≤ 18) is already checked by computer, the listed exceptions would not matter if the statement is right.
- **Unconfirmed attribution.** The ledger's quote that HOS called a full p−4 solution "seems unlikely" is unconfirmed.

## Recommendations
1. Fetch arXiv:1809.02684 v1/v2 and record Lemma 4.5, Theorem 4.6 and the definition of rotational terrace/sequencing word for word.
2. Treat the dsmic theorem as an independent, unrefereed alternative. If its proof checks out for prime m, NC3I follows in about three lines (rotate and drop) without Lemma 4.5.