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

## 6. Proof-direction data (Claude, 2026-11-25)

Scripts are in `experiments/exploration/forced_vertex/`: rankstat, halfstat, splitfrac, allsplit.

**L at p = 23 (new).** Every instance at n = 7–16 is certified with 0 inconclusive (1,756,860 instances). n = 17–19 is still running.

**The rank test is very lossy, and the choice of split is where it loses.**
- `splitfrac.py`: the fraction of admissible balanced splits that the rank inequality certifies can be as low as 1/52 (p = 13, n = 9) or 1/15 (p = 17, n = 7).
- `halfstat.py`: "some split has both ranks > D/2" fails for a few instances (3 out of 350 at p = 13, n = 7). No instance has every split certified. A proof of L would therefore have to locate rare good splits.
- `rankstat.py`: one half is never full-rank in the odd-n cases (r = s), apart from a single instance at p = 17, n = 11.
- **Diagnosis.** The inequality ρ_A + ρ_E > C(r+s, r) is exactly Lovász's exterior-algebra bound for cross-intersecting families. It ignores all path structure.

**The exact split statement is robust (`allsplit.py`).** Call a balanced split *good* if some A-path and some E-path have disjoint interiors. Every split certified by L is good, but most good splits are not certified by L.
- The fraction of good splits never drops below 5/7 at p ≤ 17, n = 5–11, and it rises with n: 0.80, 0.71, 0.76, 0.89, 0.95, 0.97, 0.98 for n = 5…11 at p = 17.
- Worst cases the rank test misses entirely: at p = 13, n = 9, 52/52 splits are good while L certifies 1. At p = 17, n = 11, 207/207 are good while L certifies 24.

**Revised target (SPLIT).** For every admissible instance, more than half of the admissible balanced splits are good. Any positive fraction would already imply FV.
- Data: the minimum fraction is ≥ 0.71 at all p ≤ 17.
- A failing split means the A-interior and E-interior families are cross-intersecting. The natural proof is then a counting or averaging argument over splits, exploiting the path structure, rather than a per-split dimension bound.

**Why splits fail (`failclass.py`).** Every failing split has one half that is poor:
- either one half has **no** simple path at all (one side empty, never both);
- or both families are tiny and cross-intersecting. Typical examples have (1, 3), (2, 2), (1, 7), (8, 1) and (4, 20) paths.

| p, n | A empty | E empty | cross-intersecting |
|---|---|---|---|
| 13, 7 | 85 | 85 | 98 |
| 17, 9 | 364 | 364 | 288 |
| 17, 11 | 11 | 11 | 174 |

**Consequence for a proof.** The obstruction lives in half-paths that are *scarce*: few paths from u to v with a fixed label set avoiding J. A proof of SPLIT needs two ingredients:
- (i) a lower bound on half-path counts that holds for most splits;
- (ii) a lemma that rich families (with path structure) cannot be cross-intersecting.

A union bound over shared vertices proves (ii) only when rs ≪ p, i.e. in the sparse regime n ≲ 2√p. The dense regime needs a structural argument.

## 7. Minimum number of FV orderings (`fvcount.c`, t = 1, minimum over B and admissible x)

| n | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|
| min #FV orderings | 1 | 5 | 4 | 48 | 95 |

- **Stability in p.** The minimum is independent of p once p ≥ 11, except at n = 7 (stable from p ≥ 17) and n = 8 (stable from p ≥ 13).
- **Where the minimum is attained.** At even n the minimiser is symmetric, e.g. {±1, ±7, ±8} and {±1, ±7, ±8, ±9} mod 23. At odd n it is nearly symmetric. Symmetric sets are exactly the case already proved by explicit construction.

## 8. Companion target: FV over ℤ, and transfer to every large prime (Claude)

**Transfer lemma (proof).** This uses the same kernel argument as Astra's prime reduction, but over ℚ.
- Suppose FV fails at size n at a prime p ∉ D_n. Then R (the set of Boolean rows orthogonal to z modulo p) has the same rank over ℚ as over F_p.
- Each admissibility form w lies outside rowspace_{F_p}(R). Hence rank_ℚ [R; w] ≥ b + 1, so w lies outside rowspace_ℚ(R).
- Choose a rational z′ ∈ ker_ℚ R that avoids the finitely many hyperplanes cut out by these forms. Scaled to integers, z′ gives distinct nonzero integer labels with an integer x.
- Every permutation is still obstructed, because R z′ = 0 exactly. So z′ is an FV counterexample over ℤ.

**Consequence.** FV over ℤ at size n implies FV at size n at every prime p ∉ D_n, in particular at every p > H_n = (n+1)^{(n+1)/2} / 2^n. That gives an explicit sparse regime: n ≲ 2 log p / log log p.

**Equivalent form over ℤ (path avoidance, PA).**
- Let R ⊂ ℤ ∖ {0} be finite with σ = ΣR ≠ 0 and −σ ∉ R. Then for every y ∉ {0, σ} with 2y ≠ σ, some ordering of R has prefix sums 0, …, σ that are pairwise distinct and all different from y.
- To get this form, take R = B ∖ {t} and translate by −t, so that y = x − t.
- The exclusion 2y = σ is forced by reversal symmetry: reversing the order sends each prefix sum v to σ − v.

**Data (`fv_integers.c`).**
- 0 failures for all zero-sum sets in [−9, 9] at n = 3…8, in [−12, 12] at n = 6, and in [−11, 11] at n = 7, for every t and every admissible x.
- With the 2x ≠ t exclusion removed, the code correctly reports the forced midpoints of symmetric sets.

**Status.** Proof of PA: in progress.
