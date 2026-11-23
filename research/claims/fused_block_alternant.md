# Fused-block alternant for FP adjacency (Claude, 2026-11-23)

Contract: LSA1 / frontier entry 20261122T155310, "attack the adjacency form of FP directly in the dense regime with an algebraic method".
Code: `experiments/exploration/fused_alternant/`.

## Setup and exact identity (proved)
Let A ⊆ ℤ_p^* be zero-sum, |A| = k = n + 2, and let (a1, a2) be a merge pair (z = a1 + a2 ∉ A ∪ {0}). Let B = A ∖ {a1, a2}, listed as y_1..y_n.
For an ordering π of B, write u_0 = 0 and u_j = y_{π(1)} + … + y_{π(j)}. Then u_n = −z.

The cyclic ordering (a1, a2, π) has partial sums a1, z + u_0, …, z + u_n = 0. They are pairwise distinct iff
  P(π) := ∏_{0≤i<j≤n} (u_j − u_i) · ∏_{j=1}^{n−1} (u_j + a2) ≠ 0.
The boundary cases u_0 and u_n are automatic, since a1, a2 ≠ 0.

**Lemma (alternant criterion).** Over ℤ[y, a], Alt_y P = V(y) · G_n(y; a), where G_n is a symmetric integer polynomial of degree 2n − 1 in y.
Hence Σ_π sgn(π) P(π) = V(B) · G_n(B; a2) in F_p.
So if G_n(B; a2) ≢ 0 mod p, then A has a valid cycle in which a1 is immediately followed by a2. By Lemma 0 (FP_ADJACENCY_EQUIV) this gives FP(A; a1, a2).

The criterion is an exact evaluation, so no Nullstellensatz degree condition is needed. The same holds with any weight w(u) inserted.

G_n always contains the factors e_n(B) (because y_j = u_j − u_{j−1} divides P) and e_1(B) = −z (because the factor u_n − u_0 = e_1(B) divides P).

## Closed forms for small n (exact symbolic polynomial identities, sympy; `fused.py`)
- n = 2: G = −e_1 e_2.
- n = 3: G = e_1 e_3 (2a + e_1).
- n = 4: G = 4 e_1² e_4 (2a + e_1).

With e_1 = −z and a = a2, we get 2a + e_1 = a2 − a1 ≠ 0. **Corollary:** FP(A; a1, a2) holds for every merge pair, for |A| = 5 and |A| = 6, at every prime p ≥ 5.
This gives a one-line independent proof of FP_SIZE_5_6.

These are identities between integer polynomials, not finite checks. A referee should still re-derive them independently, for example by computing Alt by hand for n = 3.

## n ≥ 5: G_n depends on the set (finite evidence, `fnum.py`)
G_n / (e_n e_1^{n−2} (2a + e_1)) is no longer a constant; it varies across random integer inputs for n = 5 and n = 6. So for |A| ≥ 7 the fused-block coefficient is **not** A-independent. There is no analogue of the single CN constant c_k.

## How often the criterion fails mod p (exhaustive over scaling orbits, all merge pairs; `crit.c`, `crit2.c`)
| p | sizes | pairs | G ≡ 0 (criterion fails) | rate | 1/p | weighted joint criterion fails | FP false |
|---|---|---|---|---|---|---|---|
| 13 | 5–11 | 454 | 20 | 0.044 | 0.077 | 0 | 0 |
| 17 | 5–14 | 7,094 | 396 | 0.056 | 0.059 | 0 | 0 |
| 19 | 5–12 | 26,884 | 1,340 | 0.050 | 0.053 | 0 | 0 |

p = 19, sizes 13–16, did not finish within this round's time limit.

The weighted joint criterion fails only when Σ sgn·P·w vanishes for every w ∈ {1, u_1, …, u_{n−1}}. It never fails in the data.

Reading the data:
- **Kill signal for the unweighted route.** For |A| ≥ 7, G_n(B; a2) mod p behaves like a uniformly random residue. It vanishes in about a 1/p fraction of instances, including dense ones (for example p = 17, |A| = 14: 4/24). So the single alternant cannot prove FP. This is the same "arithmetically random" behaviour recorded for c_k in the CN round (`polynomial_cn.md`, negative result (d)).
- **Weighted joint criterion.** It holds in every instance checked. But proving it means showing that the polynomials {Alt(P·w)/V : w ∈ W} have no common zero on the variety {y_i distinct, nonzero; a ≠ 0, a ≠ −e_1, …} over F̄_p.
  - For fixed n this is a Nullstellensatz certificate over ℤ. It holds for all p outside a finite, explicit set of bad primes, which are the primes dividing the certificate's integer content.
  - The dense regime has p ≈ n, so one needs every bad prime to be ≤ n + 2, for every n. That is the same unstructured integer question as CN_ALL_K (parked).
  - This route therefore converts FP into a per-size integer certificate with no known handle on its prime factors. It does **not** escape the CN wall.

## Verdict
- **Bank:** the alternant criterion (exact), the n ≤ 4 closed forms, and the new short proof of FP_SIZE_5_6. These are candidates awaiting the referee.
- **Route status:** a dead end as a route to the full conjecture. The kill criterion from the 2026-11-22 LSA1 entry is met in its intended sense: the fused-block coefficient is set-dependent and vanishes mod p at the random rate, and the robust (weighted) version reduces to a CN_ALL_K-type problem.
- **Recommendation:** do not re-open without a structural idea about the prime factors of per-size certificates, for example a sign-reversing involution or an explicit factorisation of G_n for n ≥ 5. One cheap lead remains unexplored: is G_n always a polynomial in e_1, e_n, a and a few other elementary symmetric functions with small-prime content? Computing G_5 symbolically takes more than 2 minutes in sympy; use a faster interpolation over ℚ.
