# Audit: FV half-path rank reduction (Astra, 2026-11-25; claims/fv_half_path_rank.md)

## Verdict
- **Half-path rank criterion: correct** (proof checked).
- **Prime reduction: correct** (proof checked).
- **Verifier: reproduces exactly.**
- **Lemma L: open.** It is a strict pigeonhole strengthening of FV.

## 1. Half-path rank criterion (checked)

**Vertex count.** The cycle has vertices 0, t, the r interior vertices of the first half, c, and the s interior vertices of the second half. That is r + s + 3 = n vertices, with d = n − 3.

**Why a nonzero product gives an FV ordering.**
- A product of r + s generic vectors is nonzero exactly when the interiors are pairwise distinct and avoid J = {0, t, c, x}.
  - Vectors with indices in J are 0.
  - Any d distinct vectors with indices outside J are independent: assign them to distinct basis vectors to see a nonzero minor.
- Choosing c ∉ {0, t, x} makes c a legal vertex.
- So any nonzero product of an A-path generator with an E-path generator yields an FV ordering.

**Why the rank inequality gives a nonzero product.** The pairing ∧^r × ∧^s → ∧^d is perfect, and the annihilator of P_A has dimension D − ρ_A. So ρ_A + ρ_E > D forces P_E ⊄ Ann(P_A). By bilinearity, some pair of generators then has a nonzero product.

**Strength of the condition.** This is a dimension (pigeonhole) condition, so it is much stronger than what FV needs, which is only P_A ∧ P_E ≠ 0. Example: when the ground set has exactly d points, the vectors form a basis and wedges are monomials e_S. L then says the A-interior r-sets plus the E-interior s-sets outnumber all r-subsets. Each half must then realise, on average, more than half of all its possible interior sets.

## 2. Prime reduction (checked)

**Statement.** If FV fails at size n at some prime p, it fails at size n at some prime in D_n ∪ {q_n}.

**Encoding a failure.**
- The tail is a path from 0 to t with steps a_i = −(labels).
- Every permutation is obstructed by a Boolean row orthogonal to z = (a, −x):
  - a zero block (a repeated vertex) gives last coordinate 0;
  - a prefix equal to x gives last coordinate 1.
- Take R to be the set of all such rows. Then every vector in ker R obstructs every permutation.

**Ranks transfer between Q, F_p and F_q.**
- For p ∉ D_n, Boolean minors of order ≤ n are nonzero mod p. Pad with an identity block to reach order n. Hence rank_Q R = rank_Fp R.
- Each admissibility form w lies outside rowspace_Fp(R), because wz ≠ 0 while Rz = 0. So some augmented (b+1)-minor is nonzero over Q.
- That minor has absolute value ≤ 2H_n < q_n. So w also lies outside rowspace over F_{q_n}.

**Choosing a counterexample at q_n.**
- Each admissibility form cuts a proper hyperplane out of the kernel.
- M_n = C(n+1, 2) + 3 forms are needed, and I recounted this: (n² + n + 6)/2. Each form is a signed sum of ≤ 2 Boolean rows.
- Since q > M_n, some kernel point avoids every hyperplane.
- That point is an admissible counterexample over F_{q_n}: zero-sum by construction, every permutation still obstructed.
- The Hadamard-type bound H_n = (n+1)^{(n+1)/2} / 2^n on Boolean determinants is standard.

**Consequence.** For each fixed n, FV is a finite computation. The cost grows like q_n^{n−2} with q_n ≈ 2H_n ≈ n^{n/2}, so this is practical only for n ≤ 8. It gives nothing for unbounded n. It is the FV analogue of the fixed-|A| rectification results for Graham.

## 3. Verifier (`half_path_rank.py`, reproduced)

| p | 7 | 11 | 13 | 17 | 19 | 29 (n = 6) |
|---|---|---|---|---|---|---|
| certified / total | 4/4 | 248/248 | 1260/1260 | 25200/25200 | 106288/106288 | 70356/70356 |

- The p = 13 worked example gives ranks (12, 9) against D = 20.
- **Soundness.** The rank lower bounds come from 0/1 substitutions computed over F_2. An odd minor at a 0/1 point is the value of an integer polynomial minor, so that polynomial is nonzero. The bounds are therefore valid.

## 4. New results (Claude): FV holds at every prime for |B| = 7 and |B| = 8

**Code.** `experiments/exploration/forced_vertex/fv_fixed_size.c`.
- For each zero-sum B with t = 1 (normalising by dilation), it computes K = the intersection of the vertex sets over all valid t-rooted orderings.
- FV fails iff K contains some x ∉ {0, t, t/2}.
- **Sanity check.** With the t/2 exclusion removed, it finds the known exception B = {1, 6, 7, 12} at p = 13, where 7 = t/2 is forced.

**n = 7.**
- Boolean minors of order ≤ 7 have absolute value ≤ H_7 = 32, so D_7 ⊆ {primes ≤ 31}. Then q_7 = 67.
- The earlier FV census (`fv.c`) covers every size at p ≤ 31. I re-ran n = 7 at p = 11–31 with this code: 0 failures.
- **p = 67, n = 7: 1,232,819 sets, 0 failures.**
- **Hence FV holds for every |B| = 7 at every prime.**

**n = 8.**
- H_8 = 9^{4.5} / 256 ≈ 76.9, so D_8 ⊆ {primes ≤ 73}. Then q_8 = 157 (the least prime > 153.8).
- 0 failures at every prime from 29 to 73:

  | p | 29 | 31 | 37 | 41 | 43 | 47 | 53 | 59 | 61 | 67 | 71 | 73 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|
  | sets | 30,622 | 50,348 | 181,744 | 375,145 | 522,836 | 965,524 | 2,184,436 | 4,481,116 | 5,592,614 | 10,390,904 | 15,195,736 | 18,217,681 |

- p = 157: PENDING.

## 5. Assessment of L

**What L is.** L is the only open step. It asserts a counting (pigeonhole) strengthening of FV for every n ≥ 7. The prime list in L is D_n ∪ {q_n}, which already contains every prime up to about n^{n/2}. So the restriction to finitely many primes does not make L easier for general n.

**What a proof of L needs.** A lower bound on the dimension of the exterior span of path interior sets, i.e. a rank bound for "path matroid"-type configurations. That is a genuine algebraic-combinatorics problem and not obviously easier than FV itself.

**Cheapest falsification test.** Run `half_path_rank.py` at p = 23 (all n) and at larger p for the dense sizes n ≈ p − 4, where the pigeonhole requirement is tightest.
