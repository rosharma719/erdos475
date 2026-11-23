# Frontier log
Director appends one block per round. Programme split target: A 60% / B 30% / C 10%.

- Programme A: global dense-set flexibility / avoidance (bridge to a uniform argument)
- Programme B: near-complete constructions (p−4 as proving ground)
- Programme C: IRC and structural alternatives (do not rely on refuted universal zigzag Z*)

## 2026-11-22 LSA1 (20261122T155310) -> broaden
NEXT: broaden

RATIONALE:
- **Two different approaches have now stalled on LSA1 at the same obstruction.** The first was dilation/index (Theorems B and C, index ≤ 2). The second was size induction (|A| = 5, 6). Both referees accepted the proofs, and both submissions explicitly fail to engage the balance identity (pitfalls 6 and 9). Both break at the three-jump step (pitfall 11). Under the two-approach rule, the tactic of extending FP_ALL case by case is stalled.
- **Neither result moves global coverage.** Index ≤ 2 forces k(k+1)/2 ≤ 2p, so k ≲ 2√p, which is a sparse regime. Sizes 5 and 6 lie inside CDFV_LE20 and SMALL_SETS_LE12. FP_ALL is an auxiliary strengthening used for the merge induction. Proving it only in regimes where the conjecture is already published gives Programme A nothing. The open gap is the middle and dense densities, roughly √p ≪ k < p−4, and nothing here touches it.
- **Bank the gains first.** These are referee-clean after the cosmetic fixes:
  - FP_ADJACENCY_EQUIV (Lemma 0): fix the (a₂,a₁) rotation.
  - ENDPOINT_LEMMA_E.
  - FP_INDEX_ONE_MERGED.
  - FP_SIZE_5_6.
  
  Lemma 0 has the highest impact on the frontier (8). It turns FP into "A has a valid cycle in which a₁ and a₂ are cyclically adjacent". That is a constraint on a permutation, not on a merged set.
- **New target and method: attack the adjacency form of FP directly in the dense regime with an algebraic method.**
  - Encode valid cycles with a₁ and a₂ adjacent as a permutation polynomial, i.e. the prefix-sum distinctness Vandermonde with a₁ and a₂ fused into one block.
  - Use the CN_NONZERO_SUM_CORRESPONDENCE machinery to find a nonvanishing coefficient.
  - This is genuinely different from both stalled tactics. It is global rather than local repair, so it does not pass through the three-jump/balance identity.
  - It can also feed LIFT_MERGE_CHAIN and PATH_AVOID, which are the dense-set mechanisms that are actually missing.
- **Kill criterion.** If the fused-block coefficient can be shown to vanish identically for some explicit family at density ≥ c·p, record that obstruction. In that case escalate FP_ALL toward `abandon` as a route to the full conjecture, and redirect effort to the Programme C hedge.

## 2026-11-22 NC3C (20261122T161323) -> continue
NEXT: continue

RATIONALE:
- **This round tells us nothing about NC3C mathematically.** Both submissions were empty: no statement, no proof, no resolvable dependencies. So neither counts as one of the two allowed approaches, and NC3C is not stalled. It is unattempted.
- **The referees exposed two real gaps that block any NC3C proof:**
  - The contract's case split is not a partition. C = {x, −x, y} falls under both (i) and (iii). This is exactly the open NC3_PARTITION node.
  - HOS Lemma 4.5 has not been checked for complements of size 3 (Pitfall 3).
- **Next round, narrowed contract, in this order:**
  1. **Fix the statement.** For all primes p > 37, every 3-element C ⊂ F_p^*, and A = F_p^* \ C, A has an ordering with distinct partial sums. The zero-sum convention must be stated explicitly when ΣA = −ΣC = 0. Primes p ≤ 37 are covered by FINITE_P_LE_37 and must be cited as the base.
  2. **Close NC3_PARTITION with a true disjoint partition:**
     - (I) C contains an inverse pair;
     - (II) no inverse pair and ΣC = 0;
     - (III) no inverse pair and ΣC ≠ 0.
  3. **Attempt case (I) first,** using the mechanism below.
- **Global caveat.** NC3C is Programme B, a proving ground. Large p is already covered non-effectively, so NC3C closes no middle-density regime by itself. The justification for continuing is the mechanism's transfer value to FP_ADJACENCY_EQUIV (impact 8).

OBSTRUCTION_BREAKING:
- **Obstructions to overcome:**
  - The non-partitioning case split.
  - Unverified applicability of HOS 4.5 to |C| = 3 (Pitfall 3).
  - Circularity risk in invoking the p−3 result (Pitfall 8).
- **New mechanism: a splitting lift that avoids HOS 4.5 in case (I).**
  - Choose u, v ∈ C with a := u + v ∈ A, i.e. u + v ∉ C ∪ {0}.
    - For C = {x, −x, y}, the pair (x, y) works unless y = −2x.
    - In that exceptional subcase use (−x, y) instead: −x + y = −3x, which lies in A for p > 3.
  - Set A⁺ = (A \ {a}) ∪ {u, v}. Then |A⁺| = p − 3, with complement {a, w}.
  - The published NEAR_COMPLETE_P3 result gives A⁺ a valid ordering.
  - By CONTRACTION, any valid ordering in which u and v are adjacent and σ = a ∉ A⁺ \ {u, v} yields a valid ordering of A. The non-membership holds by construction.
- **Remaining required lemma: adjacency strengthening of the p−3 construction.** One must show the rotational sequencing in that proof can be arranged with a prescribed pair adjacent. Both the exact published statement and its construction must be quoted, so the Pitfall 8 audit can be carried out.
- **Kill criterion.** If the adjacency strengthening fails for a structural reason, such as rotational symmetry forcing u and v apart, the round must document that obstruction precisely. That result would directly inform FP_ADJACENCY_EQUIV, and NC3C would then be broadened, not retried.
