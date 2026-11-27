# The coinvariant / alternation programme for Graham's conjecture — techniques and status (2026-11-27)

**Scope.** This summarizes the algebraic line started after the 2026-11-26 external audit (`external_audit_2026-11-26.md`): replace "construct an ordering" by "show a specific polynomial class is nonzero mod p". Code and data are in `experiments/linear_alternation/` (see its README for exact run logs).

**Status tags used throughout**
- **[run]** reproduced by code run in this repo (independent of the source of the claim where noted)
- **[hand]** argument re-derived or checked by reading, not by machine
- **[rep]** reported by an external session; not reproduced here
- **[open]** unproved

**Bottom line.** No proof of Graham's conjecture and no counterexample. The line reduces the conjecture to a clean nonvanishing statement (below), supplies an exact computational oracle, and gives several strictly stronger certificates for the case where the simplest one fails. For admissible primes (p > rank) every certificate computed so far succeeds, so the new machinery has not yet been needed.

---

## 1. Conventions
A set A ⊆ F_p^× of size n has a valid ordering if the partial sums s_1..s_n are distinct, i.e. every interval of the ordering not starting at position 1 has nonzero sum. All results below use this convention (intervals starting at the first element are exempt).

## 2. Technique 1 — the interval polynomial and its coefficient packet
For m ≥ 3 let F_m(x_1..x_m) = ∏ (x_i+…+x_j) over 1 ≤ i < j ≤ m, (i,j) ≠ (1,m). Then Alt_m(x_r F_m) = c_{m,r} · Δ_m with integers c_{m,r} (degrees match). Let g_m = gcd_r c_{m,r}.

**Theorem A (sufficient certificate) [hand].** If p ∤ g_m, every (m+1)-subset of F_p^× has a valid ordering. Proof: pick a_0 ≠ ΣA, put it first; the rest are distinct so Δ ≠ 0, some c_{m,r} ≢ 0 gives a permutation with F_m ≠ 0; singletons and the full tail are nonzero by choice.

**Linear alternation conjecture (LAC) [open].** For every m ≥ 3 every prime factor of g_m is ≤ m+1. LAC ⇒ Graham for all p and all sizes (no other gap).

**Data.**
- c_{m,r} for m = 3..10: brute force over all m! permutations, exact integers, independent of the C++ source — **[run]**, matches the reported vectors exactly.
- m = 11..14: **[rep]** only (C++/Boost code could not be built here); the reported rows pass internal checks (Σc = 0, reversal symmetry, recomputed gcd) **[run]**.
- g_3..g_14 = 1, 1, 2, 4, 6, 12, 6, 1, 4, 8, 4, 8; all prime factors ≤ m+1.
- Consequence if m ≤ 14 values are right: Graham holds for |A| ≤ 15 at every prime. This is **not new** below Hicks–Ollis–Schmitt (m ≤ 10) and Costa–Pellegrini (m = 11) and has not been checked against the 2026 Costa et al. claim (n ≤ 20), whose certificate mechanism the audit flagged as unsound.

## 3. Technique 2 — coinvariant algebra and Poincaré duality
R_n = Z[x_1..x_n]/(e_1..e_n), top degree N_n = C(n,2), top functional λ_n(f) = Alt(f)/Δ.
- c_{m,r} = λ_m(x_r F_m), so p ∤ g_m ⇔ [F_m] ≠ 0 in R_m ⊗ F_p (Poincaré duality). **[hand]**
- **Cyclic chord polynomial** Q_n = product of all nonadjacent chords of the n-cycle of partial sums; as polynomials Q_n = F_{n−1}(x_1..x_{n−1}) **[hand]**. Q_n is invariant up to sign under cyclic rotation of the labels, and only the socle of R_n is killed by all x_i, so [Q_n] ≠ 0 ⇔ [x_n Q_n] ≠ 0 **[hand]**.
- **CNC [open]:** [Q_n] ≠ 0 in R_n ⊗ F_p for every p > n. CNC ⇒ Graham at size n for any set, zero-sum or not. CNC at rank m+1 is weaker than LAC at rank m.
- **Higher alternation criterion [hand]:** if some homogeneous W with 1 ≤ deg W ≤ m has K_m(W) := Φ_W(−1,1,−1,…) ≢ 0 mod p, Graham holds at size m+1 (a root-counting argument on deletions of a hypothetical counterexample). K_m(x_r) = c_{m,r}; K_m(W) = Alt(W F_m)/Δ at the roots ζ,…,ζ^m of unity.
- **Equivalence with CNC:** λ_{m+1}(t^{m−d} W G_{m+1}) = −K_m(W). **[run]** 18 random cases, m = 3,4,5 (exact integers vs. complex roots of unity); argument by Lagrange interpolation **[hand]**. So "some higher-degree W works" ⇔ [Q_{m+1}] ≠ 0.

## 4. Technique 3 — splitting an edge (exact rank reduction)
Replacing one label u by u−t, t gives a ring map R_{n+1} → R_n[t]/(t(t−u)) (free over R_n on 1, t); every image is A + tB. The "value" A is an interval polynomial of rank n; the "jet" B is a first-order correction. Tested at every insertion cut.
- m=7, p=3 (where g_7 = 6 kills every linear certificate): all values A_j = 0, but cut 4 has a nonzero jet (10 Artin coordinates, coefficient 1 on u₂u₃²u₄²u₅³u₆⁵u₇⁶). **[run]**, using the externally written script. Shows jets can succeed where all linear packets fail. (p = 3 ≤ m+1, so a stress test, not a Graham instance.)
- **Coordinate-intersection theorem [rep, hand-consistent]:** (x)∩(y) = (xy, x^{n−1}) in R_n, with ((x)∩(y))/(xy) ≅ R_{n−2}[−(n−1)]. Dimension count 2(n−1)! − (n−2)! checked. Gives the "canonical residue" ρ ∈ R_{n−2} and T_{n;i,j} = Q_n ∏_{k≠i,j} x_k ≅ Gysin image of ρ.
- **Residual detection (Thm 4) [hand]:** if all linear packets vanish and p > m, a first-order packet B is nonzero iff some λ(x_a(x_b−x_c)B) ≠ 0 with a,b,c unmarked. (Uses uB = 0, zero row sums, zero trace; needs p ∤ (m−1)(m−2).)

## 5. Technique 4 — exact content recurrence
Define contents: g_m (linear), b_m (all-cut first-order matrix), d_m (individual quadratic kernels T_{m;i,j}).

| rank | g | b | d |
|---|---|---|---|
| 4 | 1 | 2 | 1 |
| 5 | 2 | 2 | 1 |
| 6 | 4 | 2 | 2 |
| 7 | 6 | 2 | 2 |
| 8 | 12 | 2 | 2 |

**[run]** ranks 4–8 (exact integer Artin-basis code from the external session, rerun here, ~29 s). The claimed identity d_{m+1} = gcd(g_m, b_m) **[rep proof; not re-derived]** holds in all four testable cases (m = 4..7). Rank 9 (to test d_9 = gcd(12,2) = 2) timed out; **[open]** needs a faster implementation. Unreconciled: ProofAtlas's quoted contents ("1,1,2,2,2,2,2 for ranks 3..9") look shifted by one rank relative to ours.

## 6. Technique 5 — binary (two-marked) partial alternation
Mark two edges a, b at cyclic distance d; alternate Q_n only over the other n−2 labels z, then use e_k(z) = (−1)^k h_k(a,b). The result P_{n,d}(a,b) is a binary form of degree n−3 — below the relation degrees n−1, n of B_n = K[a,b]/(h_{n−1},h_n).

**Theorem B [hand]:** P_{n,d} ≢ 0 mod p for some d ⇒ [Q_n] ≠ 0 in R_n ⊗ F_p ⇒ Graham at size n (p > n).
- Binary content β_n = gcd of all coefficients over d. **[run, independent third implementation]** β_4..β_9 = 1,1,2,2,6,2, and β_n | g_{n−1} because P_{n,d}(1,0) = ±c_{n−1,r} (checked entry by entry, n ≤ 9). So binary certificates strictly strengthen LAC (e.g. n = 9: g_8 = 12 but β_9 = 2, so p = 3 survives).
- Reflection law (symmetric n ≡ 0,3; antisymmetric n ≡ 1,2 mod 4), P_{n,n/2} ≡ 0 for 4 | n, (a+b) | P_{n,1}, (a−b) | P when antisymmetric: **[run]** n ≤ 9.
- Not checked: the Fourier-inversion coefficient formula, the CRT coefficient bound.

## 7. Technique 6 — two-arc Vandermonde decomposition
Splitting the cycle into two arcs between the marked edges gives an exact formula for the partial alternation as a sum over label allocations of exterior minors, with an integral unipotent Pascal translation between arcs. **[rep; unchecked]**. A universal factor a(a+ΣZ) | L_s (smallest minor) is claimed. The step where the argument stalls: other exterior minors have the same degree and can cancel the smallest minor's contribution.

## 8. Known barriers
- **Representation theory alone cannot prove saturation [hand]:** H = Σ_i Δ_5(z_i..z_{i+4}) (10 variables, indices cyclic) is nonzero, harmonic, dihedrally invariant, of the right degree, yet every monomial uses ≤ 4 variables, so every two-coordinate detector vanishes on it. Any proof must use the interval-product structure of Q_n.
- Positivity/Schubert/Hessenberg geometry: factors are not simultaneously dominant; positive characteristic-0 intersection numbers can still vanish mod large p. Rational nonvanishing is not enough — control of prime support (primes ≤ rank only) is the real content.
- Summing the kernels T_{n;i,j} in one ring gives Q_n·e_{n−2} = 0 — a useless aggregate; keep them separate.
- Adjacent-only subdivisions miss the surviving jet (it appeared only at cut 4).

## 9. What is established vs. open (one table)

| Item | Status |
|---|---|
| LAC ⇒ Graham for all p, n (Thm A) | hand |
| Coinvariant reformulation; CNC ⇒ Graham | hand |
| Higher-alternation criterion ⇔ CNC | hand + run (18 cases) |
| c_{m,r}, g_m for m ≤ 10 | run (brute force) |
| g_m, m = 11..14; "|A| ≤ 15 all p" | rep |
| Split ring; m=7 p=3 jet | run |
| Coordinate intersection; content recurrence d_{m+1} = gcd(g_m,b_m) | rep (recurrence run m=4..7) |
| Residual detection | hand |
| Binary certificate; β_n | g_{n−1}; table; symmetries | hand + run (n ≤ 9) |
| Two-arc identity and minors | rep |
| **LAC / CNC / any uniform transfer theorem** | **open** |

## 10. The remaining gap and plan
Precisely: show that for p > m+1, some certificate in the chain  c_{m,r} → jets/quadratic → binary P_{n,d} → full Q_n  is nonzero mod p. The sharpest scalar form (external report): d_m ∈ (g_m, r_m)·Z[1/(m+1)!], where r_m is the residual-difference content.

Suggested next steps, in order:
1. **Close the verification gaps:** build the C++ (needs Boost.Multiprecision) or write a gmpy2 port to confirm m = 11..14; finish rank 9 of the quadratic packets with a faster implementation.
2. **Binary data beyond n = 9 (done to n = 10; no new information).** n = 10 **[run]**: β_10 = 2, constant terms equal ±c_{9,r}, rounding error < 5e-5. n = 11 is beyond float64 reliability (rounding error up to 0.5), but is forced anyway: β_n | g_{n−1} and g_10 = 1, so β_11 = 1. More generally, since g_3..g_14 have only the primes 2 and 3, β_n for n ≤ 15 can only have those primes, so binary certificates cannot show anything new before n = 16. A real LAC test now requires **g_15 and beyond** (the C++ DP: ≈ 10 GB at m = 15, ≈ 40 GB at m = 16; Boost.Multiprecision needed), or exact-arithmetic binary computations at n ≥ 16.
3. **Hunt for the transfer identity** (the two-arc / exterior-minor route): find a triangular filtration under which one minor contributes a unit and the rest lie lower. This is where all analytic attempts have stalled.
4. Keep a falsification track: a prime p > n dividing β_n (and every stronger packet) would give a precise, finite case in which to search for a genuine counterexample or for a still stronger certificate.

## 11. Caveats
- Several results are quoted from external sessions; only those tagged [run] or [hand] were checked here.
- Literature IDs for Oct-2026 papers and the ProofAtlas record were not verified; overlap with ProofAtlas's unpublished working materials is unknown. Novelty is claimed for none of this.
- "No counterexample found" refers to algebraic transfer statements at small ranks; no systematic search for counterexamples to Graham or to LAC was run.

---

# Addendum (2026-11-28): exact rank transfer, the merged-edge algebra, and the rank-6 obstruction

This addendum covers the two rounds after §11. Everything stated as computed was reproduced by code in `experiments/linear_alternation/` (`transfer_checks.py`, `witness_checks.py`, `split_edge_checks.py`, `coverage_check.py`, `smith_check.py`, with `artin.py` and `modrank.py` as support).

## 12. The insertion operator and arbitrary-order Poincaré transfer

**Setup.** On the zero-sum hyperplane write Q_m(u) = Δ(y_0..y_{m−1}) / ∏u_i with y_0 = 0, y_j = u_0+…+u_{j−1}; deg Q_m = D_m = N_m − m. Goal: [Q_m] ≠ 0 in R_m ⊗ F_p for p > m.

**Theorem 1 (edge insertion; proved, checked m = 3..8).** Split the first edge w_0 = h + x_0. Then
Q_{m+1}(h,x) = ± W_m(x)(h+x_0) Q_m(h+x_0, x_1, …, x_{m−1}), W_m(x) = ∏_{j=2}^{m−1}(x_0+…+x_{j−1}).
Write T_m(q) = W_m(x)(h+x_0)q(h+x_0,x_1,…); then Q_{m+1} = T_m(Q_m). The proof is a cancellation of the two edge factors against the new vertex's chords (y_0 = 0, y_1 = w_0).

**Theorem 2 (divided-difference descent; proved).** The operator (F − s_{h,x_0}F)/(h − x_0) commutes with symmetric polynomials, hence descends to the coinvariant algebra. Setting h = 0 gives [T_m(q)] = 0 ⇒ [q(H_1 − H_0)] = 0 in R_m, with H_0 = ∏_{j=2}^{m−1}(y_0 − y_j), H_1 = ∏_{j=2}^{m−1}(y_1 − y_j). This has no conormal error (ordinary derivatives do not preserve the ideal; divided differences do).

**Theorem 3 (centered presentation; proved, checked m = 3..6).** With u_i = x_i + h/m, p_k(u) = c_{m,k} h^k, c_{m,k} = ((m+1) − (m+1)^k)/m^k, and R_{m+1} ≅ K[u,h]/(h^{m+1}, p_k(u) − c_{m,k}h^k, 1 ≤ k ≤ m) in characteristic 0 or > m+1. In particular e_2(u) = ((m+1)/(2m)) h², so the second-order quotient is a genuine deformation of R_m, not R_m[h]/(h³).

**Theorem 4 (Poincaré rank transfer; proved, checked m = 3, 4, every r).** For G homogeneous of degree N_m + r in x_0..x_{m−1} and 0 ≤ r ≤ m,
λ_{m+1}(h^{m−r}G) = (−1)^r ((m−r)!/m!) · λ_m(E_r G), E_r = e_r(∂_{x_0},…,∂_{x_{m−1}}).
(From Δ_{m+1}(z,h) = Δ_m(z) Σ_r (−1)^r e_r(z) h^{m−r}.) Taking the h-expansion of T_m(q) (coefficient of h^j is (W_m/j!) ∂_{x_0}^j(x_0 q)) gives an exact finite formula for every packet λ_{m+1}(h^{m+1−k} g T_m(q)), and by Poincaré duality [T_m(q)] = 0 iff all of them vanish. So the transfer problem is exactly a family of lower-rank functionals.

**Boundary lemma (proved).** Polynomials P, Q ∈ K[x]/(e_1) that agree on every coordinate hyperplane x_i = 0 have ∏x_i | P − Q, hence [P] = [Q] in R_m (m ≥ 3). The Vandermonde class is therefore determined by its exact boundary polynomials, each of which is recursively Q_{m−1}·f′(y_d).

### Witnesses (computed)
- **Rank 5:** q = Σ x_i(x_{i+1}²x_{i+2}² + x_{i−1}²x_{i−2}²) defeats value-only faithfulness, and the divided-difference packet detects it: λ_5(x_1² q (H_1 − H_0)) = −2.
- **Rank 6 (in characteristic 0 and mod 13):** a degree-9 signed dihedral combination of 22 orbit sums (rotation and the reversal i ↦ m−1−i each act by −1) has all zero-edge insertion packets zero (6 of 6), all degree-2 divided-difference packets zero (21 of 21), yet λ_6(x_0x_1^5 q) = −198 ≠ 0. Its second-order packet detects it: λ_7(h^4 x_0² x_1 T_6(q)) = −7646. Consequence: no transfer theorem based only on dihedral symmetry plus low-order packets can hold. (Convention settled — see §15: this is the true symmetry of Q_6. A polynomial built with the reflection i ↦ m−i carrying the same signs is not Q-equivariant, which is why it gave different numbers.)
- Over F_1009, the residual binary directions missed by value / first / second-jet packets are, per the report, 1/0/0 (rank 5), 4/4/0 (rank 6), 9/9/9 (rank 7); this table was not reproduced.

## 13. The merged-edge algebra (exact quadratic presentation)

Let u = h + x_0, v = h x_0, H_0 = 1, H_1 = u, H_j = uH_{j−1} − vH_{j−2} (complete homogeneous polynomials in the two split variables), and A_m = K[u,v]/(H_m, H_{m+1}).

**Theorem 5 (presentation; proved, relations checked m = 3..7).** R_{m+1} ≅ B_m[h]/(h² − uh + v) with B_m = A_m[z_1..z_{m−1}]/(e_j(z) − (−1)^j H_j(u,v), 1 ≤ j ≤ m−1). B_m is free over A_m of rank (m−1)!; the extension is free of rank 2; B_m/(v) = R_m. No jet truncation is needed: every order of the deformation is retained.

**Theorem 6 (exact annihilator of the merged edge; proved, checked through the top degree for m = 3..8 by modular linear algebra).** In A_m (hence in B_m and in the quadratic extension), Ann(u) = (K_m), K_m = H_m/u for m odd and H_{m+1}/u for m even. (Proof: H_{m+1}(0,v) = (−v)^{(m+1)/2} ≠ 0 for m odd, symmetric in the other parity.)

**Parity consequence.** K_m(u,0) = u^m = 0 in R_m for m even, and u^{m−1} ≠ 0 for m odd. So specialising v = 0, the annihilator disappears in even lower rank and leaves exactly (u^{m−1}) in odd lower rank. A uniform cancellation argument that ignores rank parity cannot work.

**Theorem 7 (two-equation transfer; proved).** Reduce the insertion factor W(h) = ∏_{j=2}^{m−1}(y_j − h) modulo h² = uh − v as A + Bh, with A_1 = 1, B_1 = 0 and
A_j = y_j A_{j−1} + v B_{j−1},  B_j = (y_j − u)B_{j−1} − A_{j−1}.
Then T_m(q) = 0 iff qA = qB = 0 in B_m/(K_m). At v = 0: A_0 = ∏_{j=2}^{m−1} y_j (degree m−2) and B_0 = [∏(y_j − u) − ∏ y_j]/u (degree m−3), division exact.
- **Even m:** T_m(q) = 0 ⇒ qA_0 = qB_0 = 0 in R_m (pairing with R², R³).
- **Odd m:** T_m(q) = 0 ⇒ qA_0, qB_0 ∈ (u^{m−1}), hence uqA_0 = uqB_0 = 0 (pairing with R¹, R²).

### Coverage of the lower-rank detector (computed, F_1000003)
Packet = Π(A_0R² + B_0R³) (even) or Π(uA_0R¹ + uB_0R²) (odd); Π = projection onto the dihedral character pairing nontrivially with Q_m (computed: χ_Q(rot) = χ_Q(rev) = (−1)^{m−1}).

| lower rank | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|
| packet dim / full projected test space | 1/1 | 2/2 | 9/9 | 9/29 | 47/87 |

**Integral saturation (computed):** packet lattice vs full projected lattice has relative index 1 (rank 4), 2 (rank 5), 108 = 2²·3³ (rank 6); rank-6 Smith invariants 1,1,1,1,2,2,2,2,108 versus 1,1,1,1,1,2,2,2,2. So through lower rank 6 the packet spans the full test space after inverting 2 and 3, i.e. the descent holds for every polynomial of the right degree and symmetry in every characteristic greater than the rank. Ranks 7 and 8 are not covered by these packets alone.

### Rank-5 unrestricted-descent counterexample (verified)
In lower rank 5 take q = w_1(w_0^4 + 4w_0²e_2(w) + 3e_2(w)²). After splitting, q = w_1K_5 with K_5 = u⁴ − 4u²v + 3v², so uq = w_1H_5 = 0 and T_5(q) = 0 in R_6, while q = w_0^4 w_1 ≠ 0 in R_5 (three nonzero Artin terms). So unrestricted fixed-cut faithfulness fails even with every jet order retained. q lacks the dihedral symmetry, so this does not touch the Vandermonde kernel or the symmetric transfer.

### Chord factors beyond the merged edge (stated; not independently checked)
For a block S of k consecutive edges, L_S is the first Chern class in the Grassmannian algebra G_{k,n}, and multiplication by it is the raising derivation on Λ^k V_n; the surviving annihilator under restriction to a zero root is {b ∈ ker E : e_1 ∧ b ∈ im E}. This generalises Theorem 6 (k = 2), but for larger k the surviving annihilators are more complicated than the parity obstruction.

### Common deformation across all cuts (stated; not independently checked)
Splitting at any edge d gives (t² − ut + v)∏(t − w_i) = (t − u)t^{m+1}, so e_k(w) = (−1)^{k+1} v H_{k−2}(w_d, v) and v = −e_2(w) is the same parameter for every cut; for a polynomial q the relation error at cut d takes the form q_d = q_0 + vE(w_d, v, w) with E common to all cuts.

## 14. Updated blockers and targets
- **The remaining theorem:** show [T_m(Q_m)] = 0 ⇒ [Q_m] = 0 for all m, uniformly over Z[1/(m+1)!]. Equivalent forms: Q_mA = Q_mB = 0 in B_m/(K_m) ⇒ Q_m = 0, using the shared parameter v across all m cuts.
- **What cannot work:** (i) any argument using only dihedral symmetry plus values, first jets and adjacent divided differences (rank-6 witness); (ii) unrestricted fixed-cut faithfulness (rank-5 counterexample); (iii) any parity-blind cancellation (Theorem 6); (iv) the packets A_0, B_0 alone beyond lower rank 6 (coverage 9/29 at rank 7, 47/87 at rank 8).
- **Open mechanism:** a denominator-free interpolation in the cut variable that combines the all-cut equations, using the recursive boundary structure of Q_m (the boundary lemma) that the counterexamples lack. The differences between cut parameters are zero divisors, so ordinary Lagrange interpolation is not available; exterior-power or divided-difference substitutes are the natural candidates.
- **Computation still missing:** the F_1009 binary-direction table; first-order normal packets of the rank-6 witness; the chord-factor and common-deformation statements; rank-9 quadratic packets (d_9); g_15 and beyond.

---

## 15. Reflection convention, deformation annihilators and simultaneous interpolation (2026-11-28)

**Reflection convention (computed, m = 4..8).** For zero-sum edge vectors, Q_m(w) transforms under the dihedral group by
- rotation i ↦ i+r: sign (−1)^{r(m−1)};
- reflection i ↦ c−i: sign (−1)^{c(m−1)}.

So reversing the edge sequence (c = m−1) acts by (−1)^{m−1}, as does a rotation by one step, while the reflection i ↦ −i (c = 0) acts trivially. The rank-6 witness built with the reflection i ↦ r−1−i carrying sign (−1)^{r+1} is equivariant under this character for all 12 group elements; the variant built with i ↦ r−i and the same signs fails on all six reflections, i.e. it is not a Q-equivariant polynomial. Hence the witness values −198 and −7646 are the ones for the Vandermonde symmetry type.

**Theorem 8 (annihilators of the deformation parameter; proved, checked m = 3..8).** In A_m = K[u,v]/(H_m,H_{m+1}) (and by freeness in B_m and in the quadratic extension), Ann(v) = (H_{m−1}) and Ann(H_{m−1}) = (v). Multiplication by H_{m−1} therefore embeds R_m = B_m/(v) into B_m with a degree shift: an exact upward Poincaré-type map.

**Theorem 9 (deformation filtration; proved, layers checked m = 3..8).** v^b H_{m−b} = 0 for 0 ≤ b ≤ m and v^m = 0; the standard monomials are u^a v^b with a + b ≤ m−1 (m(m+1)/2 of them), the b-th layer of A_m has dimension m−b, and in B_m the b-th layer is ≅ R_m/(u^{m−b}) shifted by 2b.

**Theorem 10 (simultaneous trace interpolation; checked m = 3, 4, 5, every r).** Let E_r : R_m[t]_{<r} → ⊕_d R_m/(w_d^r), F ↦ (F(w_d) mod w_d^r)_d. Writing b = m−r, a tuple (f_d) lies in the image iff Σ_d w_d^{b+k} f_d = 0 for k = 0..r−1, and dim im E_r = r·m!/2 (computed: 3, 6 at m = 3; 12, 24, 36 at m = 4; 60, 120, 180, 240 at m = 5). The image is a maximal isotropic subspace for ⟨f,g⟩ = Σ_d λ(w_d^b f_d g_d) (power sums vanish in R_m); the proof of equality uses the base case rank E_1 = m!/2 via the Cohen–Macaulay squarefree quotient and induction on r. The statement is thus a denominator-free substitute for Lagrange interpolation across the cut variables. (The proof was not re-derived here; the dimension formula was checked directly.) A realisation statement — every compatible tuple at deformation order b comes from a common polynomial correction in (e_2..e_m)^b — is stated but not checked, and lower layers can interact with higher ones.

**Simultaneous saturation (computed).** Let V_m be the space of χ_Q-equivariant polynomials of degree D_m, spanned by signed dihedral orbit sums; let T_m be the (representative-level) transfer polynomial and L_m the class in R_m. Saturation means ker T_m ⊆ ker L_m, i.e. rank T = rank (T, L). Over F_1000003:

| rank m | D_m | orbit sums | rank T | rank L | joint rank | saturation |
|---|---|---|---|---|---|---|
| 4 | 2 | 2 | 1 | 1 | 1 | holds |
| 5 | 5 | 16 | 6 | 2 | 6 | holds |
| 6 | 9 | 185 | 54 | 9 | 54 | holds |

Rank 7 (2,829 orbit sums; reported rank 452 = 452 over F_11, F_13, F_1009, with the earlier boundary packet missing 20, the independent-lift deformation 19, and the full simultaneous deformation 0 of the 29 target directions) is not reproduced in this table; see the README for the status of the rank-7 run.

**Degree sensitivity (computed).** Rank 4, q = 5·O_{(0,1,2,3)} + O_{(0,0,1,5)} with O the orbit sums for the permutation-sign character: q = 40 z_1 z_2² z_3³ ≠ 0 in R_4 but T_4(q) = 0 in R_5 (and, by rotation covariance, at every cut). So saturation cannot be proved at the socle degree and descended by duality; the deficiency D_m must enter. (With the χ_Q character the same exponents give q = 0 in R_4, so no counterexample; the sign character is the relevant one at socle degree because λ transforms by the sign.)

**Status.** Simultaneous interpolation (Thm 10) is proved in all ranks per the report and dimension-checked here; simultaneous saturation at degree D_m is verified at ranks 4–6 and is the remaining open theorem in general. The next analytical problem is the interaction of the maximal-isotropic interpolation spaces with the multiplication ideals generated by the insertion factors.

---

## 16. The universal marked-root algebra and global compatibility (2026-11-28)

**The point.** The layer-by-layer trace interpolation (Thm 10) is valid but incomplete: the full deformation has additional compatible directions created by cancellations between layers. The report packages the entire simultaneous system in one algebra.

**Definition.** Let Z(T) = Σ_{j=0}^{m−1} H_j(u,v) T^{m−1−j} and P(T) = (T−u)Z(T). The marked-root algebra is
C_m = A_m[w_0..w_{m−1}] / (∏(T−w_i) = P(T)),
i.e. A_m[w] modulo e_k(w) = (−1)^{k+1} v H_{k−2}(u,v) for 1 ≤ k ≤ m (with H_m = H_{m+1} = 0 in A_m). Setting w_d = u recovers the cut-d merged-edge algebra B_{m,d} = C_m/(w_d − u).

**Computed (graded linear algebra over F_1000003).**
- dim C_m = (m(m+1)/2)·m!: 36 (m = 3), 240 (m = 4); Hilbert series symmetric with socle degree N_m + 2m − 2 (7, 12). Graded dimensions: m = 3: 1,3,6,8,8,6,3,1; m = 4: 1,4,10,19,29,37,40,37,29,19,10,4,1.
- With a_d = w_d − u, η_d = ∏_{i≠d}(u − w_i) and g = Z(u) = Σ_j H_j u^{m−1−j}: a_dη_d = 0, η_dη_e = 0 (d ≠ e), η_d² = gη_d, Σ_d η_d = g. Verified for m = 3 and m = 4.
- m = 3: Ann(a_d) = (η_d) and Ann(η_d) = (a_d) (Thm 1 of the report); (e_2,…,e_m)C = vC and C/(v) has dimension m·m! = 18 (the report's "ρ(I) = vC" and C/(v) ≅ R_m[u]/(u^m)); rank Φ = 27 = (m!/2)(dim A_m + dim gA_m) = 3·(6+3); dim v·im Φ = 12 = (m!/2)(dim vA_m + dim vgA_m) = 3·(3+1). The "separate-layer" count (m!/2)·dim vA_m is 9, so exactly 3 = (m!/2)·dim vgA_m extra compatible directions come from inter-layer cancellation, as the report predicts.
- m = 4: dimension, socle degree and the η-identities verified; the annihilator and (e_2..e_m)C = vC checks were still running when this was written (log: `experiments/linear_alternation/marked_root_m4_out.txt`).
- In A_m, u^k H_{m−1} = v^k H_{m−1−k} for 0 ≤ k < m, in particular u^{m−1}H_{m−1} = v^{m−1} (used for the sufficient identity below): verified m = 3..8.

**Statements from the report (proofs not re-derived here).**
- (Thm 1) Ann(a_d) = (η_d), Ann(η_d) = (a_d) in C_m; the adjoint of Φ : C → ⊕B_{m,d}, F ↦ (F|_{w_d=u}), is Ψ(f) = Σ η_d f_d; ΨΦ = ΦΨ = g.
- (Thm 2) Over the universal parameter ring Φ and Ψ are simultaneously diagonalisable as diag(I, gI) and diag(gI, I) in free bases (the cokernel of Ψ is the Cohen–Macaulay squarefree skeleton ring of rank m!/2); the normal form survives specialisation to the coinvariant setting.
- (Thm 3) Global trace interpolation: f ∈ im Φ iff Σ η_d f_d ∈ gC_m; with deformation order, f ∈ v^b im Φ iff f ∈ v^b⊕B_{m,d} and Σ η_d f_d ∈ v^b g C_m.
- (Thm 4) ρ(I) = vC_m (I = (e_2..e_m)) and C_m/(v) ≅ R_m[u]/(u^m); the compatible polynomial lifts of a lower-rank class q_0 are exactly q_0 + vF, F ∈ C_m.
- (Dimension formula) dim vM = (m!/2)(dim vA_m + dim vgA_m) for M = im Φ; the independent-layer count omits (m!/2)·dim vgA_m directions. Reported dimensions in the target degree and dihedral component (separate / extra / full): rank 5: 4/0/4; rank 6: 44/6/50; rank 7: 374/102/476; rank 8: 3,099/1,087/4,186; rank 9: 24,031/8,879/32,910 (the extra share rises from 12% to 27%). Not reproduced here — the unprojected m = 3 identity above is the only direct check.
- (Thm 5) Global weighted kernel: T_d(q) = 0 for all d iff ρ(q) ∈ Ann_{C_m}(J_W), J_W = Σ_d η_d(uα_d, uβ_d)C_m, where W_d(h) = α_d + β_d h mod h² − uh + v.
- (Thm 6) Duality: simultaneous saturation at degree D_m is equivalent to the weighted detector F_m = {u^{m−1}(F mod v) : H_{m−1}F ∈ J_W} filling R_m^m (or its χ·sgn component); the relevant dual degree is s_C − D_m = 3m − 2, linear in m.
- Sufficient target: v^{m−1}(R_m^m)^{χ·sgn} ⊆ J_W (using u^{m−1}H_{m−1} = v^{m−1}, verified above).

**Rank-7 saturation status.** The rank-7 run launched earlier (`saturation_check.py 7 7`) was terminated before producing a result, so rank 7 is not reproduced here; saturation is verified at ranks 4, 5, 6 only. The report states it reran rank 7 over F_11, F_13, F_1009 and found rank T_7 = rank (T_7, L_7) = 452.

**Status.** Global compatibility is solved in the report's formulation (Thms 1–4 above); weighted noncancellation (J_W-containment) is open. The structure to exploit: η_dη_e = 0, η_d² = gη_d, Ση_d = g.

---

## 17. Weighted noncancellation as a relative problem; the monomial model; a characteristic-11 obstruction (2026-11-28)

**Reformulation (stated in the report; standard algebra).** Let M_m = C_m/J_W, a graded module over the parabolic algebra A_m = K[u,v]/(H_m,H_{m+1}) (the cohomology of Gr(2,m+1), socle generator s_A = v^{m−1}, socle degree m−1 in the weighted grading). A finite module M over a local Artinian Gorenstein (self-injective) algebra satisfies sM ≠ 0 iff M has a free direct summand; in the graded case dim (sM)_{d+deg s} counts graded free summands generated in degree d. Hence the sufficient containment v^{m−1}(R_m^m)^{χ·sgn} ⊆ J_W is equivalent to: **M_m^{χ·sgn} has no graded free A_m-summand generated in degree m.** (Not all weighted generators need act injectively and M_m need not vanish; only the full parabolic deformation must fail to survive in one graded component.)

**Monomial-weight model (checked).** Replace the insertion weight W_d(h) by h^{m−2}: T_d^{model}(q) = (h+x)h^{m−2}q. Then T_d^{model}(q) = 0 for all d implies q = 0 in R_m for every homogeneous q of degree < N_m, with no symmetry assumption. Proof (short; read): multiply by h² and use h^{m+1} = 0, so h^m x q = 0; since Ann(h^m) = (h) in the upper ring (free over K[h]/(h^{m+1})), x q ∈ (h), i.e. w_d q = 0 in R_m for every cut; q lies in the socle, which sits in degree N_m. **Computed:** at m = 3, 4, 5, for every degree k < N_m, the transfer map on all monomials of degree k has the same rank as the joint map (transfer, class in R_m), so the kernel of the all-cut transfer is contained in the ideal (e_1..e_m); all cases hold (e.g. m = 5: transfer ranks 1, 4, 10, 20, 35, 55, 73, 81, 71, 46 in degrees 0..9). The actual weight has the same top coefficient, but monicity alone cannot be used: W̃(h) = h^{m−4}(h² − uh + v) is monic of the right degree yet vanishes identically in the split algebra. Extracting the leading coefficient of the true insertion weight with legitimate operations is exactly the missing step.

**Trace polynomial identity (proved, verified symbolically for m = 2..12).** With g(u,v) = Σ_j H_j u^{m−1−j}: **v·g = u^{m+1} − H_{m+1}**, hence v g = u^{m+1} in A_m (telescoping via vH_j = uH_{j+1} − H_{j+2}). So multiplication by g is tied to powers of the hyperplane class.

**Characteristic-11 obstruction (computed).** At m = 7, g = 7u⁶ − 15u⁴v + 10u²v² − v³. Multiplication by g from (A_7)_3 (basis u³, uv) to (A_7)_9 (basis u³v³, uv⁴) has matrix [[165, −198], [48, −54]] (images of u³, uv as rows), determinant 594 = 2·3³·11 and Smith form diag(3, 198). So this map loses rank mod 11 although 11 > m+1 = 8: some constituent maps have torsion at primes outside the localisation Z[1/(m+1)!]. The report finds that saturation nevertheless survives in characteristic 11 at rank 7 (marked transfer rank 562 in characteristic 11 versus 612 in characteristics 13, 101, 1009, joint ranks equal) — not reproduced here. A proof therefore has to establish that the relative saturation survives rank changes, not that all constituent maps keep their rational ranks.

**Vertex-polynomial identity (proved, read).** With f(t) = ∏_j (t − y_j): f(y_d + h) = (−1)^{m−1} v W_d(h), because h(h−u) = −v. Multiplying the transfer by v therefore removes the cut-dependent endpoint factors but loses information: reported rank-7 tests over F_1009 give 29/29 target directions for the original transfers, 9/29 for the v-multiplied ordinary transfer and 0/29 for the v-multiplied marked transfer (not reproduced here). The divided endpoint factors must be kept.

**Adjacent-cut identity.** With W̃_d(t) = ∏_{j ∉ {d,d+1}}(t − y_j): (t − y_d) W̃_d(t) = (t − y_{d+2}) W̃_{d+1}(t) (both are the product over all vertices except y_{d+1}). Trivially true; it provides a division-free way to exchange factors between adjacent cuts and is proposed as the main source of new weighted identities. It has not yet been combined with the global compatibility and Gysin maps.

**Marked-root saturation (stronger conjecture).** Allowing independent marked-root inputs F(u,v,w) = u^k O_a(w) (0 ≤ k ≤ m−1), the report finds marked transfer rank = joint rank at ranks 4–6 (characteristics 11, 101) and 7 (characteristics 11, 13, 101, 1009), ranks 2/10/83/562-or-612 etc. This is **not reproduced here**: it needs a normal form for C_m beyond m = 4, which was not built.

**Updated hierarchy of targets.** Actual Vandermonde descent (weakest sufficient, open) ⇐ universal dihedral simultaneous saturation (verified ranks 4–6 here) ⇐ highest-layer containment v^{m−1}R^m ⊆ J_W (reported through rank 7) ⇔ no degree-m free A_m-summand in M_m^{χ·sgn}. Degree-independent saturation is false (rank-4 counterexample, §15).

**Open.** (A) a relative Lefschetz / free-summand argument for M_m^{χ·sgn}; (B) recover the monomial model inside the actual transfer, using the adjacent-cut identity with the global compatibility maps. Literature context (Maeno–Numata–Wachi strong Lefschetz elements of type A, which require pairwise-distinct coefficients and so exclude the 0/1 interval forms; Thorup's splitting algebras; Pham–Sauermann for large primes) is quoted from the report and was not checked.

---

## 18. Coefficient extraction fails below the socle; Catalan structure of the trace operator; cofactor identities; boundary-packet contents (2026-11-28)

**Adjacent-cut identities (trivial algebra, read).** With P_d(t) = ∏_{j≠d}(t − y_j) and W̃_d(t) = ∏_{j∉{d,d+1}}(t − y_j): w_d W̃_d(t) = P_{d+1}(t) − P_d(t), hence Σ_d w_d W̃_d = 0 and Σ_{d=i}^{j−1} w_d W̃_d(t) = (y_j − y_i)∏_{k∉{i,j}}(t − y_k). These cannot simply be carried into the cut quotients because the cuts evaluate t at y_d + h with different quadratic relations.

**Degree-independent extraction is false below the socle (computed).** At rank 5, with the trivial dihedral character (χ_Q = +1 for odd m), take q = Σ c_a O_a over the 12 orbit sums of degree 8 listed in the report (exponents 00017, 00026, 00035, 00044, 00116, 00125, 00134, 00143, 00152, 00161, 00224, 00233, with coefficients −410, −1605, −3640, −5110, −639, −1470, −3290, −3640, −1204, −933, 560, 280). Exact reduction: **T_d(q) = 0 for every cut** (cut 0 computed; the others follow by rotation covariance), while in R_5
q = −980 (w_2w_3³w_4⁴ − w_2²w_3³w_4³ + w_1w_3³w_4⁴ + 2w_1w_2w_3²w_4⁴ + w_1w_2²w_3w_4⁴ + w_1w_2²w_3²w_4³) ≠ 0
(reproduced term by term). Since the degree is below the socle (8 < 10), the monomial-model theorem (§17) forces the model transfers not all to vanish, so actual-weight vanishing does not imply monomial-weight vanishing even with the right symmetry.

**Saturation by degree (computed, ordinary simultaneous saturation; missing directions = rank(T,L) − rank T on χ_Q-equivariant polynomials):**

| degree | D_m | D_m+1 | D_m+2 | D_m+3 | D_m+4 | D_m+5 |
|---|---|---|---|---|---|---|
| rank 5 (D=5) | 0 | 0 | 0 | 1 | 0 | 1 |
| rank 6 (D=9) | 0 | 0 | 0 | 2 | 2 | 0 |

So saturation holds in the target degree and slightly above it at ranks 5 and 6, but it is not a consequence of a degree-independent cancellation theorem: the deficiency D_m (or the structure of Q_m) must be used.

**Rank 8 (reported, not reproduced).** A Schubert/Monk-formula verifier reportedly shows that at rank 8 (D_8 = 20, characteristics 11 and 101) ordinary simultaneous saturation fails — 27 of 87 lower-rank directions undetected (ranks of T_8 and (T_8, L_8): 2650/2677 over F_11, 2652/2679 over F_101) — and the stronger marked-root saturation fails with all 87 undetected, with an explicit degree-20 dihedral witness (2,390 compressed terms; lower normal form has 1,289 terms including 7·w_4²w_5⁵w_6⁶w_7⁷ mod 11). The bundle was not attached and my Artin-basis code cannot reach R_9 in degree ~26, so this is unconfirmed here. If correct, simultaneous saturation (the strategy of §15–17) is dead as a route and any proof must use properties specific to Q_m.

**Catalan structure of the trace operator (computed).** For g_m = Σ_j H_j u^{m−1−j} in A_m = K[u,v]/(H_m,H_{m+1}) with λ(v^{m−1}) = 1:
- λ(g_m u^{m−1−2k} v^k) = Catalan(m−k): verified for m = 3..9, all admissible k (exact rationals).
- Multiplication by g_m, (A_m)_d → (A_m)_{d+m−1}, is the matrix (C_{m−i−j}); with a = ⌊d/2⌋+1, b = ⌊(m−1−d)/2⌋+1 its rank is min(a,b) in characteristic 0 and min(a, b, max(0, a+b−1−m+(p−1)/2)) in characteristic p > m+1 (Catalan C_k ≡ 0 mod p iff k ≥ (p+1)/2, plus the shifted Catalan Hankel determinant). **Verified on 819 (m,p,d) cases** (m = 3..14, p ∈ {11,…,37} with p > m+1, and characteristic ≈ 0): 0 mismatches. This explains the rank loss mod 11 at m = 7, d = 3 (rank 1 of 2): the previous round's integral Smith data.

**Vandermonde cofactor identities (computed, exact rationals, m = 3..7).** For upper vertices Y_0..Y_{n−1} (n = m+1), edges x_i = Y_{i+1} − Y_i (cyclic) and q_i the lower kernel after deleting vertex i (lower cycle listed in index order):
Σ_i (−1)^i Y_i^k q_i (1/x_{i−1} + 1/x_i) = 0 for 0 ≤ k < m, and = (−1)^m Q_{m+1} for k = m.
(This is the report's 𝒟_k with the signs written out; it follows from cofactor expansion of the Vandermonde determinant, divided by the product of upper edges, and the identity ∏(lower edges)/∏(upper edges) = (x_{i−1}+x_i)/(x_{i−1}x_i).) The report adds that these identities force q = c·Q_m among polynomials of the right symmetry (the Vandermonde matrix has a one-dimensional nullspace); not reproduced.

**Boundary-packet nonvanishing for the actual kernel (computed).** For even m, Q_{m+1} = 0 ⇒ Q_m A_0 = 0 in R_m (§13, Thm 7 and its corollary), A_0 = ∏_{j=2}^{m−1} y_j. Using the alternation functional with Q_m = F_{m−1}, the content c_m = gcd_g λ_m(Q_m A_0 g) over degree-2 monomials g is
m = 4: 1; m = 6: 2; m = 8: 6; m = 10: 1 (all pairings nonzero: 10/10, 21/21, 36/36, 55/55).
So Q_8A_0 ≠ 0 in R_8 ⊗ F_p for every prime p > 3 (in particular p = 11, as reported), and by the boundary descent Q_9 ≠ 0 mod p for all p > 9; similarly Q_{11} ≠ 0 for every p > 11 (all p). These are consistent with, but do not extend, the |A| ≤ 15 coverage. A larger check needs an exterior-algebra dynamic programme for this packet (m = 12 already needs 12! ≈ 4.8·10⁸ permutations; the first useful rank is m = 16).

**Revised assessment.** (i) Degree-independent coefficient extraction: disproved (rank 5, degree 8). (ii) Universal degree-specific simultaneous saturation: reported disproved at rank 8; verified here only through ranks 4–6. (iii) The actual kernel is not obstructed: the boundary packet is nonzero through m = 10 at every prime, and the cofactor identities give constraints unavailable to arbitrary lifts. Next attempts should target the actual Vandermonde boundary packets (A_0 and the corresponding quadratic/cubic packets) and use the cofactor identities, rather than universal faithfulness of the transfer.

---

## 19. The "boundary-content conjecture" is LAC (2026-11-28)

A later report proposes the narrower target B_m = Q_m ∏_{j=1}^{m−1} y_j = Q_{m+1}|_{h=0} (degree N_m − 1, one below the socle), with boundary coefficients c_{m,j} = λ_m(w_j B_m) and content δ_m = gcd_j c_{m,j}, and conjectures that δ_m ≠ 0 has no prime divisor > m+1 (so B_m ≠ 0 ⇒ Q_{m+1} ≠ 0 ⇒ Graham at size m+1).

**Identification (computed, m = 4..9; also immediate algebraically).** In R_m, B_m = ± F_m, the interval polynomial of §2: Q_m = F_{m−1}(w_1..w_{m−1}); F_m = F_{m−1}·y_{m−1}·∏_{i=2}^{m−1}(w_i+…+w_m), and in R_m (zero total sum) each w_i+…+w_m = −y_{i−1}. Direct alternation computation of λ_m(w_j B_m) and λ_m(w_j F_m) over all m! permutations gives identical vectors for even m and exactly negated vectors for odd m (e.g. m = 7: (966, 1662, 1338, 0, −1338, −1662, −966) vs the negative of §2's), with contents 1, 2, 4, 6, 12, 6 for m = 4..9, sum zero and reversal law c_{m+1−j} = (−1)^{N_m}c_j. Hence δ_m = g_m and the table of boundary contents (ranks 3..14: 1, 1, 2, 4, 6, 12, 6, 1, 4, 8, 4, 8) is the g_m table of §2 (ranks 11–14 still rely on the external C++ run). **The new conjecture is LAC in different notation; its numerical support is the same data, not independent evidence, and it does not extend the verified range.**

**What the report adds (the notation, not new coverage).**
- Confluent Vandermonde form: B_m = det(y_i^{j+1})_{1≤i,j≤m−1} / ∏w_i, since det(y_i^{j+1}) = ∏y_i² · Δ(y_1..y_{m−1}) and Δ(y_0 = 0, y_1, …) = ∏y_i · Δ(y_1..): verified algebraically (equals Q_m∏y_j).
- A signed-prefix exterior recursion P(S) = Σ_{i∈S} ± P(S∖{i}) ∧ v(s(S)) with v(t) = Σ_{r=2}^m t^r e_r: this is the same subset dynamic programme as §2.1 (state count about C(2m−1, m−1) ≈ 4^m).
- A normalised version G(S) = P(S)/(Δ(S)∏a_i), integral and symmetric, with a "symmetric remainder recursion" G_k(E) = t^{k−1}(A_k(t) mod F_k(t)), and a partial-flag divided-symmetrisation formula for c_{m,j} (cross-block Vandermonde denominators of block sizes (j−1, 1, m−j)). These are stated with proof sketches; not checked here.
- Remark: an individual coefficient cannot suffice (c_{7,1} = −966 = −2·3·7·23, but the vector has content 6).

**Status.** The open problem is unchanged: prove LAC (p > m+1 ⇒ p ∤ g_m). The new integral recursion for G_k is a possible route to a relation between g_m and g_{m+1}; no such relation has been found.

---

## 20. Near-top Artin coefficients, Pascal recurrence, two-coefficient content (2026-11-28)

This round reformulates LAC (§19) as arithmetic of the near-socle class B_m ∈ R_m^{N_m − 1}, which is an (m−1)-dimensional space, rather than of the whole (m!-dimensional) algebra.

**Artin coefficients (computed).** The monomials M_i = (w_1^0 w_2^1 ⋯ w_m^{m−1})/w_i, 2 ≤ i ≤ m, form the Artin basis in degree N_m − 1, and λ_m(w_j M_i) = δ_{j,i} − δ_{j,i−1}. Writing B_m = Σ_i b_{m,i} M_i: c_{m,1} = −b_{m,2}, c_{m,j} = b_{m,j} − b_{m,j+1} (2 ≤ j < m), c_{m,m} = b_{m,m}, and b_{m,i} = −Σ_{j<i} c_{m,j}. Consistent with all stored c-vectors for m = 3..14, and gcd(b) = gcd(c) = g_m. **Direct integral Artin reduction of B_m = Q_m∏y_j in R_m (m = 4..7)** gives a normal form supported exactly on the M_i with coefficients ±b_{m,i} (e.g. m = 7: 966, 2628, 3966, 3966, 2628, 966, gcd 6; m = 6: 28, 68, 88, 68, 28 — gcd 4). So the "intrinsic" content of the boundary class is g_m (the LAC quantity) in any basis.

**Pascal recurrence (computed).** Let v(t) = Σ_{i=2}^m t^i/i! e_i, P_k(x_1..x_k) = Σ_σ sgn σ · v(x_σ1) ∧ v(x_σ1+x_σ2) ∧ … ∧ v(x_σ1+…+x_σk), and κ(A,I) the coefficient of (x^A/A!) e_I (A, I increasing sets of distinct positive integers; κ = 0 unless ΣA = ΣI; κ({a},{i}) = δ_{a,i}). The recurrence
κ(A,I) = Σ_ℓ (−1)^{ℓ−1} Σ_{|C|=k−1, ΣC = ΣI − i_ℓ} det(binom(a, c))_{a∈A, c∈{0}∪C} · κ(C, I∖{i_ℓ})
matches the definition computed directly from polynomial arithmetic on all 254 pairs tested (k = 1, 2, 3, I ⊆ {2..7}), 0 mismatches; it is integral, so valid in every characteristic. The complementary contraction
c_{m,r+1} = Σ_{A,I ⊆ U_m, |A|=|I|=r, ΣA=ΣI} (−1)^{r + ΣI^c} κ(A,I) κ(A^c, I^c), U_m = {2..m}
reproduces the boundary vector exactly for m = 3..8, up to a global sign (+ for odd m, − for even m — a normalisation convention). Likewise |c_{m,1}| = |κ(U_m,U_m)| and the c_2 formula Σ_a (−1)^a κ(U_m∖a, U_m∖a) hold in magnitude (up to the same global sign) for m = 3..8.

**Complementary minors (computed).** For the Pascal matrix (7×7, all |A| = |D| ≤ 4), det P_{A,D} = det P_{D^c,A^c} exactly (no sign), so near-full Pascal minors can be replaced by small complementary ones. (Jacobi's identity with the signed inverse binom matrix.)

**Two-coefficient content (computed from the stored vectors, m = 3..14).**

| m | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gcd(c_1, c_2) | 1 | 1 | 2 | 4 | 6 | 12 | 12 | 2 | 8 | 24 | 4 | 8 |
| full content g_m | 1 | 1 | 2 | 4 | 6 | 12 | 6 | 1 | 4 | 8 | 4 | 8 |

At every tested rank the first two coefficients alone have no prime factor > 3; gcd(c_1,c_2) is a multiple of g_m (so the two-coefficient conjecture "p > m+1 ⇒ (c_1, c_2) ≢ (0,0) mod p" would imply LAC). It is the same data as the g_m table (m ≥ 11 resting on the external run), not independent evidence. Individual coefficients are not enough (c_{7,1} = −966 = −2·3·7·23).

**Statements not checked here:** the proof sketches of the Pascal recurrence in general k, the symmetric-remainder/flag-pairing reformulations, and any proof strategy built on top of them (which would need a noncancellation invariant surviving the signed sums — the report notes this is Step 3 and remains open).

**Status.** The proof obligation is unchanged: LAC (equivalently, the integral content of B_m / its Artin coefficient vector has no prime factor > m+1). The new representation is purely integer-combinatorial (Pascal minors on subsets of {2..m}), which is a candidate setting for an inductive or cofactor argument; none has been found.

---

## 21. Unique-matching expansion and the component expansion of the boundary polynomial (2026-11-29)

**Expansion of κ (computed).** For increasing sets A = {a_1<…<a_k}, I = {i_1<…<i_k} with ΣA = ΣI, sum over nonnegative integer k×k matrices M with row sums i_r and column sums a_s that have a **unique perfect matching** π_M:
κ(A,I) = Σ_M sgn(π_M) · ℓ(D_M) · W(M), W(M) = ∏ a_s! / ∏ m_rs!,
where D_M is the DAG obtained by contracting the matching edges (vertex r ↔ row r/column π_M(r); edge r → r′ when m_{r,π(r′)} > 0, r′ ≠ r) and ℓ is its number of linear extensions (edge orientation does not matter for this count). Verified against the Pascal recurrence (§20), which was itself verified against the direct definition: **493 pairs (A,I), k = 1..4, I ⊆ {2..7}, 0 mismatches**. The mechanism: the signed sum over row/column orderings of the multinomial terms is a determinant of 0/1 rows (1,…,1,0,…,0) that vanishes unless the row "first-positive-entry" positions are all distinct, forcing a triangular support with a unique diagonal matching; every matrix with several perfect matchings cancels exactly.

**Component expansion (computed, m = 3..6).** With U = {2..m}, n = m−1 and Ĉ_m(z) = Σ_r C(n,r) c_{m,r+1} z^r (binomials are units mod p > m+1, so Ĉ_m ≢ 0 ⇔ C_m ≢ 0):
Ĉ_m(z) = Σ_M sgn(π_M) ℓ(D_M) W(M) ∏_{H ∈ components of D_M} ((−z)^{k_H} + (−1)^{s_H}),
over square matrices with row and column margins both U, k_H = |H|, s_H = Σ_{vertices in H} (margin). Reproduces the boundary polynomial exactly for m = 3, 4, 5, 6 (up to the global sign (−1)^{m−1}, a normalisation), summing over 2, 14, 378, 39,802 unique-matching tables respectively.

**Consequences (checked).**
- The constant and linear coefficients are c_{m,1} = (−1)^S Σ_M μ(M) and n·c_{m,2} = (−1)^{S+1} Σ_M μ(M) Σ_{i ∈ isolated vertices of D_M} (−1)^i, S = Σ_{i=2}^m i, with μ(M) = sgn(π_M)ℓ(D_M)W(M) (algebraic consequence of the expansion; consistent with the magnitudes of c_1, c_2 checked in §20).
- **Identity-matching contribution.** The only unique-matching table with matching = identity is diag(2,3,…,m) (verified for m = 3, 4, 5; follows because identity matching makes off-diagonal flows balanced, hence zero on an acyclic graph). Its weight is μ = n!, every vertex is isolated, and it contributes n! ∏_{i=2}^m ((−1)^i − z) to Ĉ_m — verified symbolically for m = 3..6. At m = 3 this is 2(z²−1); the only other surviving table contributes −3(z²−1); they sum to 1 − z² = Ĉ_3(z). So the canonical diagonal term is cancelled by other matchings: one cannot extract it by evaluating z.

**Syzygy limitation (stated; not checked here).** The exterior syzygies Σ_{i∈I} ± A_i K(I∖i) = 0 are satisfied by the degenerate family K̃(∅) = 1, K̃({i}) = e_i, K̃(I) = 0 for |I| ≥ 2 (all boundary contractions vanish), so any backward-propagation proof must use the creation operator in the raising recursion, not just the syzygies.

**Rank 17 (reported, not reproduced).** A memory-efficient modular version reportedly completes rank 17 in characteristics 19 and 23 with the boundary vector surviving (rank 17 mod 19: (12,5,17,15,4,7,10,3,6,3,10,7,4,15,17,5,12)). Not reproducible with the code in this repository (the subset dynamic programme has ~4^m states); the integral data in this repo are brute force to m = 10 and the external run to m = 14.

**Status.** The remaining theorem is unchanged (LAC / boundary primitivity). The graph formulation is exact and verified, and the consecutive-margin condition U = {2..m}, not yet used analytically, is the structure a sign-reversing involution or a flow-switching argument would have to exploit.

---

## 22. Signed height walks, the Weyl-algebra form, and the exterior determinant representation (2026-11-29)

**Triangular-flow summation (computed).** For ordered margins i_1..i_k, a_1..a_k with surplus h_r = Σ_{j≤r}(i_j − a_j), the sum of W(M) = ∏a_s!/∏m_rs! over upper-triangular nonnegative integer matrices with positive diagonal and these margins equals ∏_r [C(i_r + h_{r−1}, i_r) − C(h_r, i_r)] (zero if some h_r < 0). Verified on all 1,841 margin pairs with k ≤ 3, entries ≤ 5.

**Signed-height walks (computed).** With T_{i,a}(h) = C(h+i, i) − C(h+i−a, i) for the step h → h+i−a (forbidden if the new height is negative):
κ(A,I) = Σ_{σ,τ} sgn(σ)sgn(τ) ∏_r T_{i_σ(r), a_τ(r)}(h_{r−1}).
Verified on all 493 pairs (k ≤ 4); the "remove the last transition" dynamic programme F(A,I) = Σ_{i,a} (−1)^{pos(i)+pos(a)} T_{i,a}(h − i + a) F(A∖a, I∖i) agrees with the Pascal κ on the same pairs, and the complementary contraction built on it reproduces the boundary vector exactly for m = 3..10 (up to the global sign (−1)^{m−1} seen before). This is the simplest independent implementation so far (about 12 s for m ≤ 10).

**Weyl algebra (computed + algebra).** With U b_h = (h+1) b_{h+1}, D b_h = b_{h−1}, [D,U] = 1, U_i = U^i/i!: [D^a, U_i] b_h = T_{i,a}(h) b_{h+i−a} — checked for h ≤ 8, i, a ≤ 5.
**Modular truncation (computed):** for p ∈ {11, 13, 17, 19}, h < p and 2 ≤ i,a ≤ p−2, every step to h + i − a ≥ p has T ≡ 0 (mod p); so modulo p walks live in heights 0..p−1 (a finite-dimensional representation, V_p = F_p[t]/(t^p)).

**Exterior determinant representation — with a sign correction.** Take odd (anticommuting) generators α_i, β_a (i, a ∈ U = {2..m}), X = Σα_iU_i, Y = Σβ_aD^a, so X² = Y² = 0. The report writes H = YX − XY and also H = Σ α_iβ_a [D^a, U_i]. With odd coefficients these are **not** the same: computed with a Grassmann implementation, tr(XY) = −tr(YX) ≠ 0, tr(H) ≠ 0 for H = YX − XY, whereas **H = XY + YX = −Σ α_iβ_a [D^a, U_i] has tr(H^k) = 0 for k = 1..4** (and the argument is truncation independent: H^k = (XY)^k + (YX)^k since cross terms vanish, and tr(XY)^k = −tr(YX)^k). So the correct matrix is the commutator form (up to the harmless overall sign), and then det(I − zH) = 1 by Newton's identities (denominators ≤ m only). The coefficient extraction then holds: for H = Σ α_iβ_a[D^a, U_i], **(H^k)_{00} = ε(k) Σ_{|A|=|I|=k} κ(A,I) α_Iβ_A, ε(k) = (−1)^{k(k−1)/2}** — verified coefficient by coefficient for U = (2,3), k ≤ 2 and U = (2,3,4), k ≤ 3. Since det(I − zH) = 1, the adjugate identity gives det(I − zH^+) = Σ_k z^k (H^k)_{00}, where H^+ deletes the height-0 row and column.
The boundary polynomial is then C_m(z) = [α_Uβ_U] det(I + zH_+^+) det(I − H_−^+), with H_− built from X ↦ Σ(−1)^iα_iU_i. By hand: the sign factors ε(k)ε(l)(−1)^{kl} (k + l = n) are the constant ε(n), the shuffle signs for sorting I ∪ I^c and A ∪ A^c cancel because ΣI = ΣA, and (−z)^k(−1)^{ΣI^c} is exactly the contraction weight, so this reproduces the verified complementary-contraction formula up to a global sign. The product itself was not recomputed as determinants.

**Negative results (computed, exact).**
- Arbitrary distinct margins are not enough: κ({a,b},{a,b}) = 2 − C(b,a), so κ({2,7},{2,7}) = −19 and the contraction polynomial for U = {2,7} is 19 − 19z², identically zero mod 19 although 19 > 8.
- The two-coefficient shortcut fails for shifted consecutive margins: for U = {13,14,15,16} the contraction polynomial is 293541560 + 41340z − 9464z² + 41340z³ + 293541560z⁴, and gcd of the first two coefficients is 13780 = 2²·5·13·53, so both vanish mod 53 (53 > 17) while the middle coefficient does not. Reproduced exactly.
So the proof must use the margins 2, 3, …, m, and the full vector (not just two coefficients) is the right target.

**Rank 17 (reported, not reproduced).** The report gives exact c_{17,1}, c_{17,2} (about 63 digits each) with gcd 48 = 2⁴·3, matching modular values mod 19 and 23, and two-coefficient contents 32, 192, 48 at m = 15, 16, 17. Not reproducible here (the subset dynamic programmes need ~4^m states); our integral data stand at brute force to m = 10 and the external run to m = 14.

**Status.** Remaining theorem unchanged: for p > m+1 the boundary vector (equivalently C_m(z), equivalently the g_m content) is nonzero mod p. New usable structure: a finite-dimensional Weyl-algebra/exterior-determinant model, exact flow summation, and a certified list of what cannot hold for general margins. The proposed first target is to exploit the consecutive powers of the Weyl generators inside the height-zero cofactors.

---

## 23. The pairing matrix P_{m,d,j}, exact rank descent, and counterexamples to intra-rank propagation (2026-11-29)

**Definition.** With Q_m = F_{m−1}(w_1..w_{m−1}), y_k = w_1+…+w_k (y_0 = 0): P_{m,d,j} = λ_m(Q_m w_j^d e_{m−d}(y)), 1 ≤ d ≤ m−1 (degree check: (N_m − m) + d + (m − d) = N_m). Row d = 1 is the boundary vector (e_{m−1}(y) = ∏_{k≥1} y_k).

**Computed (exact alternation, m = 3..8, rank 9 for the packet table):**
- **Rank-lowering identity:** P_{m,m−1,j+1} − P_{m,m−1,j} = (−1)^{m−1} m c_{m−1,m−j}, with c_{m−1,·} the first row of P_{m−1}. Holds exactly for m = 4..8.
- **Generating-function descent:** (−1)^m (1 − z) Σ_{r=0}^{m−1} P_{m,m−1,r+1} z^r = C′_{m−1}(1)(1 − z^m) − m ε_m z C_{m−1}(z), ε_m = (−1)^{C(m−1,2)}, C_{m−1}(z) = Σ_j c_{m−1,j}z^{j−1}. Holds exactly for m = 4..8; this is the report's identity (1−z)x^{m−2}𝒢_m = ((m−1)/(m−2)!)[…] once x^{m−2}𝒢_m = ((m−1)(−1)^m/(m−2)!)·Σ_r P_{m,m−1,r+1}z^r is substituted. Hence: **if the penultimate row of P_m is constant then C_{m−1} = 0**, and iterating down to C_3 = 1 − z² gives a contradiction. So the induction reduces to: *first row of P_m zero ⇒ penultimate row constant*, for the actual Q_m.
- **Quadratic packets:** boundary / Hessian H_{ij} = λ(Q_m w_iw_j e_{m−2}(y)) / split A_{ij} = λ(Q_m w_iw_j ∏_{k=2}^{m−1} y_k) / reflected divided-difference J content:
  m = 3: 1/1/1/1; 4: 1/3/1/2; 5: 2/1/2/2; 6: 4/2/2/2; 7: 6/2/2/6; 8: 12/2/6/6; 9: 6/1/1/1 — **reproduced exactly** (J = A_{ij} − (−1)^{m−2+⌊(m−1)/2⌋}A_{ρ(i)ρ(j)}, ρ fixing edge 1 and reversing the rest). Notably at m = 9 both quadratic packets are primitive although the boundary content is 6.

**Counterexamples to intra-rank propagation (computed, exact).** The implication "first row zero ⇒ penultimate row constant" is false for general polynomials of the right degree and symmetry:
- Rank 5: q = Σ_i w_i(w_{i+1}²w_{i+2}² + w_{i−1}²w_{i−2}²) (the §12 witness) has P_5(q) with rows d = 1..5 equal to (0,0,0,0,0), (0,−7,0,7,0), (0,−2,4,−2,0), (0,5,0,−5,0), (0,0,0,0,0): first row zero, penultimate row (0,5,0,−5,0) not constant. Reproduced entry by entry (valid mod every prime > 6).
- Rank 6: q = f·∏_{i=1}^6 (w_i + w_{i+1}) (cyclic), f = 5O_{(3,0,0,0,0,0)} − 26O_{(1,1,1,0,0,0)} + 35O_{(1,1,0,1,0,0)} (signed dihedral orbit sums, rotation and reversal acting by −1): P_{6,1,•}(q) = 0 and P_{6,5,•}(q) = (0, −144, 216, −216, 144, 0). Reproduced exactly. This q retains all six factors w_i + w_{i+1} (every non-diameter chord of Q_6), so retaining the non-diameter chord factors does not suffice either.
(Reported, not reproduced: the rank-8 restricted-family ranks 24/3/6.)

**Harmonic vertex-insertion polynomial (computed).** V_m(ℓ) = λ_m(Q_m ∏_{i=0}^{m−1}(y_i + L)), L = Σℓ_jw_j, has degree ≤ m in ℓ. Computing all of its coefficients exactly for m = 4, 5, 6 (46, 210, 898 nonzero monomials): the Laplacian Σ_j ∂²/∂ℓ_j² V_m and e_1(∂)V_m vanish identically, as the report states (e_1 because Σw_j = 0; the Laplacian because the coefficient involves e_1(∂)² − 2e_2(∂) and e_2(w) = 0). The gradient at ℓ = −(indicator of the first d edges) is a rotated copy of the boundary vector by the product rule. The report's higher-order detection theorem (vanishing of all Taylor coefficients through order m−2 at a vertex forces q = 0, via harmonicity) was not re-derived.

**Cofactor decomposition (computed, m = 3..8).** Splitting the contraction formula c_{m,r+1} = Σ_{I,A} (−1)^{r+ΣI^c}κ(A,I)κ(A^c,I^c) into the diagonal part (A = I) and the off-diagonal part (A ≠ I): for m = 3, 4 the boundary vector is purely diagonal; from m = 5 the off-diagonal part is nonzero only in the middle positions (m = 5: −30 at position 3 against diagonal 26; m = 6: ∓320 at positions 3, 4; m = 7: 8392 at positions 3, 5; m = 8: contents of off-diagonal and diagonal parts both 4). The first two coefficients c_1, c_2 are always purely diagonal. The off-diagonal contents (30, 320, 8392, 4) show no small-prime structure on their own; the cancellation between diagonal and off-diagonal parts is where the work is.

**Not reproduced.** The two-copy Weyl covariance identities, the normal-symbol polynomial G_{m,r}(x) = Σ_d (d(−1)^{r+d−1}/(d−1)!) P_{m,d,r+1}x^{d−1}, the translated-determinant identity 𝒢_m(z,ts) = [α_Jβ_J] det(I + zH_1^+(t,s)) det(I − H_2^+(t,s)), and the reported integral contents through rank 17 (rank 18 not claimed).

**Status.** Intra-rank propagation for the actual Q_m is open; generic propagation and propagation under retention of the non-diameter chord factors are disproved by exact witnesses (reproduced). The exact descent (rank-lowering identity + generating-function identity) is verified; it makes "first row zero ⇒ penultimate row constant" (equivalently the constant and highest-x coefficients of 𝒢_m) the single remaining implication.

---

## 24. The Witt differential on the exterior coefficients; collision derivatives (2026-11-29)

Here κ(A,I) is the Pascal-recurrence coefficient with **all** positive exponent indices allowed (including 1), v(t) = Σ_{i≥1} (t^i/i!) e_i.

**Exponent-one insertion (computed).** Let d be the graded derivation on the exterior algebra with d(e_c) = Σ_{a<b, a+b=c+1} (C(c,a) − C(c,b)) e_a∧e_b (equivalently d v(t) = v(t)∧v′(t), checked by coefficient comparison). The first-order coefficient of x_1 in P_k(x_1..x_k) equals (e_1∧ − d)P_{k−1}(x_2..x_k) (the report's "x_1P_k = …" has to be read as this leading-order statement, since the right side does not depend on x_1). In κ terms: κ({1}∪A′, I) = Σ_J κ(A′,J)·[e_I](e_1∧ − d)e_J. **Verified on 138 cases (k = 2, 3), no mismatch.**

**Adjoint and self-adjointness (computed).** With ⟨e_A,e_I⟩ = δ_{A,I}∏a!, the adjoint merges exponents: d*(e_a∧e_b) = (b−a)e_{a+b−1} (checked algebraically: (C(c,a) − C(c,b))a!b!/c! = b − a for c = a+b−1). κ(A,I)∏_{i∈I} i! = κ(I,A)∏_{a∈A} a!: **verified on 1,927 pairs (k ≤ 4, entries ≤ 8, including exponent 1).**

**Homotopy (computed).** ι_1 d + d ι_1 = ν·id with excess ν(J) = Σ(j−1); hence ι_1 D + D ι_1 = (1 − ν)id for D = e_1∧ − d. Verified on every e_J with |J| ≤ 4, entries ≤ 8. For the consecutive set U_m = {2..m}: ν(U_m) = C(m,2) and 1 − ν = −(m−2)(m+1)/2, a unit mod every prime p > m+1.

**Diagonal merge recurrence (computed).** For A without exponent 1:
κ({1}∪A,{1}∪A) = (1 − ν(A))κ(A,A) − ⟨d*e_A, M d*e_A⟩/∏_{a∈A} a!,
M(e_J) = Σ_I κ(J,I)e_I, with d*e_A computed as the adjoint of d (so no sign convention is assumed). **154 sets A (|A| = 2..4, entries 2..9): 0 mismatches**, including A = U_3, U_4, U_5. Together with κ({1..m},{1..m}) = 0 (verified for m = 2..7) this gives the exact recurrence (1 − C(m,2))κ(U_m,U_m) = ⟨d*e_{U_m}, M d*e_{U_m}⟩/∏_{a=2}^m a!, which lowers exterior degree by one, at the price of merged (non-consecutive) exponent sets. Terms whose merged exponent a+b−1 equals an existing index vanish, and modulo p only merges with m+1 ≤ a+b−1 ≤ p−1 survive.

**Collision-derivative identity (computed, m = 3..7).** For S_m = {1..m} and 1 ≤ r ≤ m−1 put
F_{m,r}(q) = Σ_{A,I ⊆ S_m, |A|=|I|=r, ΣA=ΣI} ε(A,A^c)ε(I,I^c)(−1)^{ΣI^c} q^{ΣI} κ(A,I)κ(A^c,I^c)
(ε = shuffle sign of concatenating the sorted subset and sorted complement). Then F_{m,r}(1) = 0 for every r, and F′_{m,r}(1) = ±(−1)^r Σ_{j=1}^{m−r} c_{m,j}, the sign being the global sign (−1)^{m−1} (derivative vectors, m = 3..7: (−1,1), (−1,0,1), (4,−2,−2,4), (28,−68,88,−68,28), (966,−2628,3966,−3966,2628,−966), i.e. the partial sums of the boundary vector, b_{m,i} of §20). Since the c_{m,j} sum to zero, C_m ≡ 0 (mod p) iff (q−1)² divides every F_{m,r}(q) mod p: a simple-root formulation of boundary primitivity.

**Content of [Q_m] (computed).** gcd over all degree-m monomials g of λ_m(Q_m g): m = 4: 1; m = 5: 1; m = 6: 2; m = 7: 2 (reproducing the report's 1, 2, 2 for ranks 5–7). Ranks 8 and 9 (report: 2 and 1) not reproduced here. The boundary content is a stronger sufficient quantity than this direct one (e.g. m = 5: 1 vs 2; m = 7: 2 vs 6).

**Not reproduced.** The report's examples of F_{m,r} polynomials (typeset table lost), the rank-7 insertion-identity count (236 identities), and any statement about closing the merge recursion on consecutive sets.

**Status.** All of the new identities hold in the cases checked; none closes the induction. The merge recurrence is exact but leaves the set of consecutive exponents (the merged sets are not consecutive), and the simple-root form needs a statement about common double roots at q = 1. Open as before: p > m+1 ⇒ boundary vector (equivalently the g_m content) nonzero mod p.

---

## 25. Schur endpoint packets, the Witt merge vector, and the open-path generating polynomial (2026-11-29)

**Schur endpoint pairing (computed, m = 3..6).** For a partition μ ⊢ m−d with at most m−1 parts, E_{m,d,μ} = λ_m(w_1^d Q_m s_μ(y_1..y_{m−1})) (Schur polynomial via Jacobi–Trudi in the prefix vertices) equals ±κ(I_μ, J_d), where I_μ = {j + μ_{m−j}}_{j=1}^{m−1} (μ padded with zeros) and J_d = {1..m}∖{d}. **All 4, 7, 12, 19 tests for m = 3, 4, 5, 6: no mismatch**; the sign is uniformly (−1)^{C(m+1,2)} on our orientation (the report states (−1)^{C(m+1,2)−1}: an orientation convention). This extends the diagonal pairings κ(J_d,J_d) to the whole exterior packet.

**Packet contents (computed, m = 5..7; m = 8 in progress).**
| m | 5 | 6 | 7 | 8 (report) | 9 (report) |
|---|---|---|---|---|---|
| d = 1 Schur packet gcd (P(m−1) tests) | 4 | 28 | 14 | 12 | 18 |
| combined gcd over all d, μ | 2 | 4 | 2 | 12 | 6 |
| merge-image gcd (gcd of A b_m) | 4 | 2 | 1 | 2 | 6 |
Ranks 3–4 give 1, 1 (d = 1 packet: 2 and 3 tests). Ranks 5–7 reproduce the report exactly; rank 8 (14 × 14 matrix, κ on 7-element sets) was still running at write-up time (`experiments/linear_alternation/schur_tables_out.txt`). The d = 1 packet of the report (ranks 3–11: 1, 1, 4, 28, 14, 12, 18, 44, 44) is reproduced through rank 7. All of these contents have only the prime factors 2, 3, 7 and 11 at these ranks (7 | 28, 14; 11 | 44 appears in the report's higher ranks) — each ≤ m+1 or inside the admissible range, never a prime > m+1 dividing the full packet.

**The Witt merge vector and the compressed operator (computed, m = 6; dimensions m = 4..12).**
- dim W_{m−2}^{N_m} (sets of m−2 distinct indices ≥ 2 with excess Σ(a−1) = N_m) = P(m−1) − 1: verified by enumeration for m = 4..12 (2, 4, 6, 10, 14, 21, 29, 41, 55). The single-element-at-the-minimum argument: the unique minimal-excess set of size m−1 is U_m.
- m = 6: with basis (2,3,4,10), (2,3,5,9), (2,3,6,8), (2,4,5,8), (2,4,6,7), (3,4,5,7), the merge vector d*e_{U_6} (restricted to indices ≥ 2) is **b_6 = (−1, 2, −1, −3, 2, 4)**, coefficients (b−a) over the merges with a+b−1 > m exactly as described; the compressed matrix A_{I,J} = κ(J,I) has **det A = 18,208,418,112 = 2⁶·3³·43·191·1283** and **A b_6 = (10, 52, 74, 102, 92, 88)** (content 2). All three reproduced exactly. So A is singular modulo 43, 191, 1283 (all > m+1 = 7) while the specific vector b_6 is not in its kernel: kernel avoidance, not invertibility, is the right target.
- The exponent-1 components of M(e_{U_6}) are κ(U_6, {1}∪K) = −(A b_6)_K and κ(U_6,U_6) = −28, i.e. M(e_{U_m}) = κ(U_m,U_m) e_{U_m} ∓ e_1∧A b_m, as claimed (sign convention aside).
- **Vector-valued merge criterion (consequence):** M(e_{U_m}) = 0 ⇔ A_{m−2}^{N_m} b_m = 0 (and κ(U_m,U_m) = 0 is then automatic by (1 − N_m)κ(U_m,U_m) = ⟨b_m, A b_m⟩/∏a!). b_m is nonzero: the pair (m−1, m) always survives with merged index m+1 (< p for p > m+1) and coefficient ±1, and no other merge produces that set.

**Open-path generating polynomial (computed, k = 3, 4, 5).** Φ_k(t;x) = Alt_x Δ(0, s_1, …, s_k, t), s_j = x_1+…+x_j, S = s_k. Checked at random integer points: L_k = Φ_k / (Δ(x)∏x_i · S · t(t−S)) is integer-valued, symmetric in the edges, homogeneous of degree k − 2 (so the factors Δ(x), ∏x_i, S, t, t−S do divide Φ_k and the reduced degree is k − 2), and Φ_k(S−t; x) = (−1)^{C(k+1,2)+1} Φ_k(t; x) (m = k+1) — reflection law confirmed. **Collision recurrence:** ∂_hΦ_k(t;h,x)|_{h=0} = (−1)^{k−1} Alt_x[Δ(y_0..y_{k−1},t) Σ_i (t − y_i) f′(y_i)], f(t) = ∏(t − y_i): exact for k = 3 (−528000) and k = 4 (−873698918400), by exact polynomial interpolation in h (note: one needs degree up to C(k+2,2) in h; with too few nodes the identity appears to fail).

**Content of [Q_m] (computed):** m = 4..8: 1, 1, 2, 2, 2 (rank 8 now reproduced; rank 9 in the report: 1).

**Not reproduced.** The rank-9..11 packet and merge-image tables (the report lists d = 1 packet 18, 44, 44; merge image 6, 16, 4; combined gcd 6, 4 at ranks 9, 10), the block-form theorem for M with the insertion/self-adjointness constraints (derived there by algebra; not re-derived), the two-zero determination of L_k, and the unfinished rank-18 boundary run.

**Status.** Route A (prove A_{m−2}^{N_m}b_m ≠ 0 mod p for p > m+1) is a cleaner target than the scalar contraction: b_m is explicitly nonzero, the matrix dimension is P(m−1) − 1, and invertibility of A fails already at m = 6 (singular mod 43, 191, 1283) so a kernel-avoidance argument specific to b_m is required. Route B (open-path collision induction) has verified exact identities but no noncancellation argument for the symmetric collision weight under edge alternation. Neither closes the induction.

---

## 26. The Grassmannian two-root reduction (2026-11-29)

**Schur expansion of the open-path determinant (computed, m = 3..6).** For k = m−1 edges, P_k(t;x) = Φ_k(t;x)/(Δ(x)∏x_i) satisfies
P_k(t;x) = Σ_{d=1}^m (−1)^{m+d} t^d Σ_{|A|=k, ΣA=ΣJ_d} κ(J_d, A) s_{λ(A)}(x), λ(A)_j = a_{k+1−j} − (k+1−j), J_d = {1..m}∖{d}.
Verified at random rational points for m = 3, 4, 5, 6 with global sign +1 (exactly the report's formula). Proof sketch (re-derived): expanding the (m+1)×(m+1) Vandermonde along the t-row and using that the vertex 0 row is (1,0,…,0) leaves Alt det(s_i^{a}), a ∈ J_d; Alt det(s^{J_d}) = ∏J_d! · [e_{J_d}]P^{ext} = Σ_A κ(J_d,A) det(x^A) by the factorial adjointness κ(A,J)∏J! = κ(J,A)∏A!, and det(x^A) = Δ(x)∏x_i s_{λ(A)}. (My first test failed only because of an off-by-one in my own partition map.)

**Grassmannian truncation (read).** For p > m+1 and w = p − m, the Schur terms with λ_1 > w come with a rightmost factorial divisible by p and drop out; the survivors are the Schur basis of G_{k,w} = K[e_1..e_k]/(h_{w+1},…,h_{w+k}). Hence the complete endpoint Schur packet vanishes mod p iff P_k = 0 in G_{k,w}[t]. The total-sum factor S t (t − S) can be cancelled because deg L_k = k − 2 is below the first relation degree and t(t−S) is monic in t. With w ≥ 2, setting all but two complementary roots to zero (e_j ↦ (−1)^j h_j(a,b)), a nonzero two-root specialisation 𝓛_m(t,a,b) mod p implies Q_m ≠ 0 mod p. Algebra of the substitution: s_λ(x) ↦ (−1)^{|λ|}s_{λ′}(a,b); only sets A ⊆ {1..m+1}, i.e. A_{d,r} = {1..m+1}∖{r, m+1+d−r}, survive, with λ′ = (m−r, r−d) (checked by hand), and
P̃_m(t,a,b) = Σ_{d=1}^m t^d Σ_{r=d}^{⌊(m+d)/2⌋} q_{m,d,r} s_{(m−r,r−d)}(a,b) = −(a+b)t(t+a+b)𝓛_m(t,a,b), q_{m,d,r} = κ(J_d, A_{d,r}).
The number of coefficients is ⌊(m+1)²/4⌋ (checked against the (d,r) count for m = 3..15).

**Projected merge relation (computed, m = 3..8).** For d = 1, with q_{m,r} = q_{m,1,r}: Σ_r (−1)^{r−1} q_{m,r} = 0 (m odd), Σ_r (−1)^{r−1}(m+2−2r) q_{m,r} = 0 (m even). Verified exactly. Example m = 7: (q_{7,1}, …, q_{7,4}) = (966, 3430, 4650, 2186), 966 − 3430 + 4650 − 2186 = 0, gcd(3430, 4650, 2186) = 2. So the diagonal coordinate κ(U_m,U_m) is determined by the ⌊(m−1)/2⌋ off-diagonal ones: the projected Witt vector g_m = (q_{m,r})_{r≥2} is the whole certificate (and q_{m,r} = −(A_{m−2}^{N_m}b_m)_{C_{m,r}}, C_{m,r} = (U_m∖{r, m+2−r}) ∪ {m+1}, as observed at m = 6).

**Contents (computed, m = 3..11; exact via the signed-walk DP).**

| m | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|
| projected Witt gcd, g_m = gcd_{r≥2} κ(J_1, A_{1,r}) | 1 | 2 | 4 | 4 | 2 | 2 | 6 | 16 | 4 |
| full two-root packet gcd, entries κ(A_{d,r}, J_d) | 1 | 1 | 4 | 4 | 2 | 12 | 6 | 4 | (4 in report) |

The report's two columns coincide with these: the "projected Witt" column uses κ(J_d, A) and the "full packet" column uses the Schur-pairing convention κ(A, J_d) (computing both conventions for all (d, r): κ(J_d,A) gives full gcd 1, 1, 4, 4, 2, 2, 6, 16; κ(A,J_d) gives 1, 1, 4, 4, 2, 12, 6, 4). The two conventions differ by the factor ∏J_d!/∏A!, a unit mod every prime p > m+1 (all indices ≤ m+1), so their sets of "bad primes" above m+1 agree; only the small-prime content differs. Every computed gcd has no prime factor above 3. Ranks 12–15 (report: projected 16, 8, 64, 8) were not computed here.

**Rank-7 closed form (computed).** In S = a+b, Z = a−b, T = 2t+a+b:
𝓛_7 = −(1/8)(13461 S⁴ − 8595 S²T² + 2889 S²Z² + 140 T⁴ − 245 T²Z² + 78 Z⁴) — reproduced exactly (random rational (t,a,b), 5 samples). The denominators from centering are powers of two. The parity/dihedral structure in T and Z² is as the report states (even in Z, definite parity in T).

**Collision weight (algebra).** Σ_i (t − y_i) f′(y_i) is the sum of residues at the roots of (t − z) f′(z)²/f(z) — true by the residue at a simple root; its expression through power sums p_r(y) is exact but the compatibility between vertex-symmetric multiplication and the two-root projection of edge symmetric functions is not established, so the collision recurrence (verified exactly in §25) does not yet yield an induction.

**Status.** The object to analyse is the binary symmetric polynomial 𝓛_m(0,a,b) ↔ g_m; it has ⌊(m−1)/2⌋ independent coefficients (mod the relation above), is p-independent, and passes the exact arithmetic checks computed here (through rank 11; the report states rank 15). The open problem is a uniform recurrence or arithmetic invariant for it.

---

## 27. Where the programme stands, and the missing step (2026-11-29)

### 27.1 Checks of the latest report (all reproduced)
- **Two-marked-edge certificate.** V_m(a,b) = 𝓛_m(−b,a,b) gives ∂_xQ_{m+1} = (a+b)V_m(a,b): divided symmetrization of Q_{m+1}(x_1..x_{m−1},a,b) (last vertex −b), evaluated at x with e_j(x) = (−1)^j h_j(a,b), equals (a+b)V_m with ratio 1 to 1e-15 at m = 4, 5, 6. Hence V_m ≢ 0 (mod p) ⇒ Q_{m+1} ≠ 0, and R_m ≢ 0 ⇒ Q_m ≠ 0, where R_m(a,b) = 𝓛_m(0,a,b) = −C_1(a,b)/(a+b)², C_1 = Σ_r q_{m,1,r}s_{(m−r,r−1)}(a,b); V_m = P̃_m(−b,a,b)/((a+b)ab).
- **Contents of R_m and V_m (exact):** m = 4..12: content(R_m) = 1, 4, 4, 2, 2, 6, 16, 4, 16; content(V_m) = 1, 4, 28, 6, 2, 12, 16, 8, 8 — rank 8–12 values agree with the report's ρ = 2, 6, 16, 4, 16 and η = 2, 12, 16, 8, 8. Rank 13: projected gcd 8; **the last two coordinates have gcd 152 = 8·19 and the vector mod 19 is (13, 10, 17, 8, 7, 0, 0)**, exactly as reported (so the two-coordinate shortcut genuinely fails at rank 13 mod 19 while the full binary packet survives). Higher ranks (14–17) not recomputed.
- **Extra-vertex descent (exact):** G_{k,ℓ}(T;X) = S Σ_{u∈X} [∏_ν (t_ν − S + u)/f_X′(u)] G_{k−1,ℓ+1}((S,T); X∖u), G_{1,ℓ} = 1, verified for k = 2, 3, 4, ℓ = 1, 2; and G_{k,1} = S·L_k.
- **Non-decomposability (exact):** for x = (1,2,4), the Plücker coordinates of the prefix two-vector modulo v(7) are p_23 = 0, p_24 = 96, p_25 = 1680, p_34 = 1008, p_35 = 15120, p_45 = 47040 and p_23p_45 − p_24p_35 + p_25p_34 = 241920 = 2⁸·3³·5·7 ≠ 0.
- **Not reproduced:** the two-slice descent identity 𝓛_m = z^{m−3}𝓗_{m−2} + t z^{m−2}𝓗_{m−2} and the A_q/B_q column-sector formula (symbolic through rank 5 per the report); combined contents ζ_m and ranks 14–17.

### 27.2 What is established
1. **Reduction.** For a zero-sum set (general sets reduce to these), Graham at size m+1 ⇐ [Q_{m+1}] ≠ 0 in R_{m+1} ⊗ F_p for p > m+1 (via λ_{m+1}(Q_{m+1} f) ≠ 0 for some f, then the alternation argument). Everything below only strengthens or localises this.
2. **Certificates, from strongest to weakest sufficient condition:** the linear packet (g_m, LAC) ⇒ binary certificates R_m / V_m (strictly smaller, p-independent, ⌊(m−1)/2⌋ independent integer coordinates after the projected merge relation) ⇒ [Q] ≠ 0. These are exact integer objects with rich verified structure (Pascal recurrence, unique-matching/component expansion, signed-height walks, Weyl/exterior determinants, Witt differential with contracting unit 1 − C(m,2), Schur/Grassmannian truncation, rank-descent identities).
3. **Numerical coverage.** Exhaustive search p ≤ 43; linear packet g_m for m ≤ 14 (m ≤ 10 brute-forced here, m = 11–14 external): Graham for every |A| ≤ 15 at every prime; boundary/binary contents computed here through rank 13 (and reported through 17) with no prime factor above 3 anywhere. Large primes: literature (Pham–Sauermann et al.).
4. **Structure that is a theorem, not data:** the exact identities of §§12–26 (insertion, rank-lowering P_{m,m−1,j+1} − P_{m,m−1,j} = (−1)^{m−1}m c_{m−1,m−j}, collision derivatives, the two-marked-edge and Schur-expansion formulas).

### 27.3 The missing step, stated exactly
The programme has been reduced, without loss, to **one arithmetic statement about explicit integer polynomials**:

> **(★)** For every m ≥ 3 and every prime p > m+1, the binary polynomial R_m(a,b) (equivalently the vector g_m = (q_{m,1,r})_{r≥2}, equivalently the content of the boundary class B_m) is not ≡ 0 (mod p) — or, at least, R_m and V_{m−1} are not both ≡ 0 (mod p).

All the exact identities give a *way to compute* these integers (and a rank-lowering recursion R_m = B_{m−2}(−a−b,0) + (a+b)A_{m−2}(−a−b,0) in terms of the "almost-full" and "full" column sectors of the lower determinant); **none gives a mechanism that prevents the signed sums from being divisible by a large prime.** Formally missing: a noncancellation theorem — an invariant or an inductive relation between consecutive ranks (for example a Bézout-type identity D·g_m ∈ ideal(g_{m−1}, …) with D having only prime factors ≤ m+1, or kernel avoidance A_{m−2}^{N_m}b_m ≠ 0 mod p, or a closed recurrence on the binary packet) that forces the content to have no prime factor > m+1.

### 27.4 Why the natural routes do not close it (all verified here unless marked)
- **Universal saturation / transfer theorems are false** (rank-5 degree-8 witness, rank-6 witness; rank-8 failure of simultaneous saturation is reported, not reproduced). Intra-rank propagation "first row zero ⇒ penultimate row constant" fails for general polynomials of the right degree and symmetry (rank-5 and rank-6 witnesses), even retaining all non-diameter chord factors.
- **Representation theory / harmonicity / symmetry alone cannot work** (cyclic sum of 5-variable Vandermondes; matrix A singular mod 43, 191, 1283 at rank 6 while b_6 ∉ ker).
- **The consecutive margins 2, …, m must be used:** arbitrary margins fail (κ({2,7},{2,7}) = −19; U = {13,14,15,16} gives two coordinates vanishing mod 53).
- **A single coefficient, two coefficients, or the last two coordinates do not suffice:** c_{7,1} = −966 = −2·3·7·23; shifted margins; rank 13 last two coordinates vanish mod 19.
- **The recursion is exact but sign-cancelling:** the diagonal merge recurrence lands on non-consecutive exponent sets; the collision recurrence and the open-path descent need a compatibility between vertex-symmetric multiplication and two-root projection that has not been proved; the prefix exterior vectors are not decomposable (Plücker obstruction above), so determinantal closure is unavailable; the identity-matching term is cancelled by other matchings (m = 3: 2(z²−1) − 3(z²−1) = 1 − z²).

### 27.5 Honest bottom line
No proof of Graham's conjecture and no counterexample. We have a verified chain reducing the conjecture to (★) and a large toolkit for computing and structurally describing the polynomials in (★). The finite-characteristic gap is closed only for |A| ≤ 15 (and p ≤ 43), plus whatever the asymptotic literature covers for large p. Closing (★) requires a new noncancellation idea; the evidence (contents only ever 2^a3^b) is suggestive but is not a proof.

---

## 28. Why a one-vertex induction cannot close the binary certificate (2026-11-29)

**Setting.** R_{q+2}(a,b) = B_q(−u,0;a,b) + u A_q(−u,0;a,b), u = a+b, where A_q, B_q are the full-column and almost-full-column Schur sectors of the lower second moment G_{q,2}(T;X) (§27, Section 5 of that report). An induction that recovers A_q, B_q from the preceding one-vertex moment G_{q,1}(t;X) = S_X L_q(t;X) alone would need the sectors to be determined by Schur branching, homogeneity, divisibility by S_X, reflection covariance, and the leading-coefficient identity t_1^{q−1}G_{q,2}(t_1,t_2;X) = G_{q,1}(t_2;X).

**Schur-slice flexibility (extraction formulas computed, q = 3..8).** Perturb G_{q,2} by P(X) = S_X s_λ(X), independent of the extra vertices (so the preceding one-vertex moment is untouched), with |λ| = 2q − 3. After the complementary-root substitution the effect on the binary certificate is E(P) = [z^{q−1}] (a+b+z) s_μ(a,b,z), μ = λ′. Verified by explicit Jacobi–Trudi/Pieri computation:
- μ = (q−2, r, q−1−r), ⌈(q−1)/2⌉ ≤ r ≤ q−2: **E(P) = s_{(r,q−1−r)}(a,b)**;
- μ = (q−1, q−2, 0): **E(P) = 2s_{(q−1)} + 2s_{(q−2,1)}**.
These vectors span the whole space of binary symmetric polynomials of degree q−1 (⌊(q−1)/2⌋ + 1 Schur functions; the factor 2 is invertible in odd characteristic). Hence the listed structural constraints leave the binary certificate completely free: one can change R_{q+2} by an arbitrary symmetric polynomial of degree q − 1 while keeping the preceding one-vertex packet and every listed identity. (That the perturbation is independent of the extra vertices, divisible by S, and homogeneous of the right degree is immediate; reflection covariance and the exact class of such perturbations in the true moment hierarchy are as stated in the report and were not re-derived.)

**Worked example (checked).** q = 4 (rank 6): R_6 = 28a³ + 60a²b + 60ab² + 28b³ = 28s_{(3)} + 32s_{(2,1)}, R_5 = −4(a+b)² (both reproduced from the exact packets). With E(S_X s_{(3,2)}) = s_{(2,1)} (μ = (2,2,1)) and E(S_X s_{(2,2,1)}) = 2s_{(3)} + 2s_{(2,1)} (μ = (3,2,0)), replacing G_{4,2} by G_{4,2} − 14P_2 − 4P_1 makes the extracted certificate zero (s_{(3)}: 28 − 28 = 0; s_{(2,1)}: 32 − 28 − 4 = 0) with the first moment unchanged.

**What this establishes.** It is not a counterexample to (★) (R_m ≢ 0 mod p); it is an obstruction to proving (★) by induction using only the preceding one-vertex certificate and generic structural properties — the same pattern as the earlier failures of universal saturation and intra-rank propagation. The mixed moments M_{q,i}(X) = Alt_X[Δ(0,s_1..s_q)∏_{j<q}(−s_j) e_i(s_1..s_{q−1})]/(Δ(X)∏x_j) carry the information the one-vertex packet loses; the exact identity R_{q+2} = (−1)^q u^{q−1}R_{q+1}(1,0) + (−1)^{q−1} Σ_{i=1}^{q−1} u^{q−1−i} z^{q−1}Ω_3(M_{q,i}) (reported) isolates the known lower-rank contribution from the genuinely new mixed-moment terms (not re-derived here; Ω_3 is the three-root Schur projection). The report's rank-17 observation (all three natural specialisations of R_{17}(1,b) vanish mod 47 while the polynomial does not) was not reproduced; I have no access to the rank-17 packet here.

**Status.** Unchanged: (★) is open. A proof must control the collective arithmetic of the mixed moments M_{q,i} using something specific to the signed prefix determinant (Witt-differential insertion identities are the candidate), not just Schur, symmetry, homogeneity and reflection structure.

---

## 29. Modular height barrier and the midpoint (rank-halving) identity (2026-11-30)

**Signed-height recurrence.** F(A,I) = Σ_{i∈I,a∈A} (−1)^{pos(i)+pos(a)} w_{a,i}(g,h) F(A∖a, I∖i), h = ΣI − ΣA (current height), g = h − i + a (height before the last step), w_{a,i}(g,h) = C(g+i,i) − C(h,i), negative heights contributing 0 (this is the walk DP of §22; F = κ with the first argument the x-exponents).

**Height barrier (computed + proof re-read).** If all exponents lie in {1..p−1}, every upward step from g < p to h ≥ p has weight ≡ 0 (mod p): by Lucas, with p ≤ h < g+i < 2p, C(g+i,i) ≡ C(g+i−p, i) = 0 because g+i−p < i, and C(h,i) ≡ C(h−p,i) = 0 because h−p < i. Verified exhaustively for p = 5, 7, 11, 13 (10, 35, 165, 286 crossings with all i, a ∈ [1,p−1]): no weight with a crossing is nonzero mod p. Hence modulo p the recurrence is exactly the recurrence restricted to heights 0..p−1 (the report's p-adic strengthening, higher powers of p for higher multiples, was not tested).

**Reversed-step identity (computed, exact).** For h = g + i − a, w = C(g+i,i) − C(h,i) and w′ = C(h+a,a) − C(g,a) satisfy w·g!·i! = h!·a!·w′ (since g+i = h+a). Verified for g ≤ 14, i, a ≤ 8. It telescopes along a walk.

**Midpoint (rank-halving) identity (computed).** For equal-weight sets A, I and a split A = A_1 ⊔ A_2, I = I_1 ⊔ I_2 with |A_1| = |I_1| = k and h = ΣI_1 − ΣA_1 ≥ 0:
K(A,I) = Σ ε(A_1,A_2)ε(I_1,I_2) · (∏_{a∈A_2} a!)/(h! ∏_{i∈I_2} i!) · F(A_1,I_1) F(I_2,A_2),
ε = sign of the shuffle that sorts the concatenation. **Verified over ℚ (all heights, exact rationals) on 32 random cases with r = 2..5 and every split size k = 1..r−1: 0 mismatches.** Modulo p with the barrier restriction (0 ≤ h < p, all exponents in 1..p−1): 26 cases at p = 7 and 14 cases at p = 11, 0 mismatches, including cases where terms with h ≥ p were dropped (3 and 6 respectively). So a rank-r coefficient is a bilinear pairing of two half-rank walk packets with no factorial divisible by p. The identity is an exact rational identity valid at any split size, not only k = ⌊r/2⌋.

**Two-hole sets and the coefficient transform (computed, m = 3..10).** With U = {2..m}, r = m − 1, J_j = {1..m+1} ∖ {j+1, m+1−j} (so J_j = A_{1,j+1} and k_j = K(U,J_j) = κ(U,J_j) = q_{m,1,j+1} of §26):
u²R_m(a,b) = −Σ_{j=0}^{⌊r/2⌋} k_j v^j h_{r−2j}(a,b), u = a+b, v = ab,
and, expanding h_n = Σ_ℓ (−1)^ℓ C(n−ℓ,ℓ) u^{n−2ℓ}v^ℓ, the coefficient of u^{r−2−2ℓ}v^ℓ in R_m is C_{m,ℓ} = −Σ_{j=0}^ℓ (−1)^{ℓ−j} C(r−ℓ−j, ℓ−j) k_j. Verified for m = 3..10 including divisibility of the sum by u². **m = 7:** k = (966, 3430, 4650, 2186) gives R_7 = −966u⁴ + 1400u²v − 156v² exactly as reported (A_7 = −k_0, B_7 = −156). The transform is integral and unitriangular, so content(R_m) = gcd(k_0, …, k_{⌊r/2⌋}); checked: 1, 1, 4, 4, 2, 2, 6, 16 for m = 3..10 (consistent with the R_m contents of §27). For even m the projected-row gcd (r ≥ 2) and content(R_m) can differ by a factor dividing m, as seen at m = 4.

**Not reproduced.** The report's counts (6,562 midpoint checks over several characteristics, 196 vanishing high-height states), its normalisation remark about an older verifier comment (the specific numerical example was lost in transmission), and the p-adic strengthening.

**The remaining obstacle, as the report states it.** Each k_j is a pairing ⟨V_U, W_{J_j}⟩_p of half-rank walk packets indexed by exponent subsets and midpoint heights; the missing theorem is that V_U ∉ (span{W_{J_0}, …, W_{J_{⌊r/2⌋}}})^⊥ for every p > m+1. Nondegeneracy of the ambient pairing does not imply this (isotropic vectors exist over finite fields), so a statement about these specific packets is needed; candidate routes are exterior rank propagation (do the symmetric two-hole packets span a space containing a dual witness?), the truncated Weyl algebra on F_p[t]/(t^p) (the barrier justifies the finite-dimensional representation), and a midpoint-height filtration looking for an extremal height whose component cannot cancel. All three are open; none has been tried beyond the reformulation.

**Status.** New exact tools: a modular truncation theorem and a rational midpoint factorisation, both verified. The open statement is still (★): for p > m+1, R_m (equivalently k_0, …, k_{⌊r/2⌋} jointly) is not ≡ 0 mod p.

---

## 30. Exterior rank descent, surjectivity of the nuisance maps, and the one-hole operator criterion (2026-11-30)

**Exterior rank-descent identity (computed, m = 4, 5, 6, untruncated).** With K_A = Σ_B κ(A,B)e_B (A = vertex exponents, B = edge exponents, positive indices), E the raising derivation (Ee_i = e_{i+1}), U = {2..m}:
K_U = Σ_{a=2}^m (−1)^a E^a(e_0 ∧ K_{U∖a}).
The e_0-components of the right side cancel exactly and the positive part equals K_U. (Mechanism: expand det(s_j^c) along the last vertex S, S^c ↔ E^c, the lower determinant alternated over one more variable ↔ e_0∧.)

**Surjectivity of the nuisance maps (computed).** With T_2(v) = E²(e_0∧E³v), T_3(v) = E³(e_0∧E²v) on Λ^{m−2}V (V = span{e_0..e_{m+1}}, E e_{m+1} = 0), weight w = Σ_{a=2}^m a: the combined image is the whole weight-w part of Λ^{m−1}V, checked over F_p for (m,p) = (5,7), (7,11), (9,11), (10,13), (11,13), (14,17), (15,17) (target dimensions 4, 7, 10, 12, 14, 21, 24). Hence the desired lower row cannot be isolated from the upper row by this linear map alone, as the report states. (The proof via three-variable Schur duals was not re-derived; Smith invariants for the small ranks 5, 6 were not reproduced.)

**Coupled version (computed; sources restricted to positive exponents).** With the exact coupling (7), T̃_2(q) = E²(e_1∧E²q), T̃_3(q′) = E³(e_0∧E³q′), q, q′ in the positive exterior space, weights w−5 and w−6: ranks reproduce the report's table exactly — (m,p) = (5,7): 4, 4, 3; (7,11): 7, 7, 7; (9,11): 10, 10, 9; (10,13): 12, 12, 12; (11,13): 14, 14, 13; (14,17): 21, 21, 21; (15,17): 24, 24, 23; (17,19): 30, 30, 29; (17,23): 30, 30, 30 (columns: weight-space dimension, rank(T_2+T_3), coupled rank). **The coupled image has codimension exactly one precisely when p = m+2, and is everything otherwise** — in all nine tested pairs. (With sources allowed to contain e_0, the coupled image was full even at p = m+2; the positive-exponent restriction is what produces the codimension, because genuine determinant rows have no exponent-zero components.) So even imposing the genuine coupling between the two lower rows leaves enough freedom to cancel the desired certificate; the induction must use more.

**Weyl-operator formulation (computed, m = 3, 4, 5).** With V_p = F_p[x]/(x^p), e_h = x^h/h!, T_{a,i} = [D^a, X^i/i!] (weights C(g+i,i) − C(g+i−a,i), checked in §22; [D,T_{a,i}] = T_{a,i−1}, [X,T_{a,i}] = −aT_{a−1,i} by direct algebra), and W(A,I) = Σ_{σ,τ} sgnσ sgnτ ∏_j T_{a_σ(j), i_τ(j)}:
- W(U,U) is diagonal on e_h with eigenvalue **W_m(h) = Σ_{d=1}^m d·C(h,d−1)·K(J_d,J_d)**, J_d = {1..m}∖{d}: verified exactly for h = 0..7, m = 3, 4, 5, with either product order;
- **W({1..m−1},{1..m−1}) = 0** (the consecutive set starting at 1): verified, eigenvalue 0.
- **Alternation identity (11):** Alt_{S_m}[x_m^d det(s_j^c)_{j≤m−1,c∈J_d}] = (−1)^{m−d}K(J_d,J_d)Δ(x)∏x_j: verified at random rational points for all d, m = 3, 4, 5.
So if any K(J_d,J_d) ≢ 0 (mod p), every zero-sum m-set has an ordering with nonzero prefix determinant.

**Observation (new, derived here).** W_m(h) is a polynomial in h of degree ≤ m−1 < p, so it vanishes at every h ∈ F_p iff it is the zero polynomial iff all K(J_d,J_d) ≡ 0. Hence **W(U,U) ≠ 0 over F_p ⇔ some one-hole diagonal coefficient K(J_d,J_d) is nonzero mod p.** The report's "standard polynomial" criterion (12), s_{2m−2}(D²..D^m, X²..X^m) ≠ 0 on F_p[x]/(x^p), is therefore equivalent (via the report's reduction, not re-derived) to non-vanishing of the *diagonal* one-hole packet, a different packet from the boundary vector. Its content (computed): gcd_d K(J_d,J_d) for m = 3..11 = 1, 1, 4, 4, 2, 12, 18, 16, 8 — no prime factor above 3 (single entries do carry large primes: c_{7,1} = K(J_1,J_1) = 966 = 2·3·7·23). K(J_m,J_m) = 0 always (m = 3..8 shown; m = 9..11 consistent with the printed digit counts).

**Not reproduced.** Surjectivity proofs, equation (6)–(7) (explicit common-component decomposition of the two lower rows), the equivalence with the standard polynomial (12) and its Amitsur–Levitzki context, equation (9) (the adjoint-lowering identity; only its consequence (10) was tested), and the 190 modular height configurations.

**Status.** (★) is open. This round adds a clean, exact reformulation (the one-hole diagonal packet / the operator W(U,U), i.e. the polynomial W_m(h)), additional obstructions to rank-descent induction (surjectivity and the p = m+2 codimension-one phenomenon), and verified supporting identities. A uniform proof that gcd_d K(J_d,J_d) has no prime factor > m+1 (equivalently that W_m ≢ 0 as a polynomial over F_p) is still missing.

---

## 31. Experiment: how small a subpacket of the diagonal one-hole packet certifies (2026-11-30)

**Question.** By §30, W(U,U) ≢ 0 over F_p ⇔ some K(J_d,J_d) ≢ 0 (mod p), where W_m(h) = Σ_d d·C(h,d−1)·K(J_d,J_d) is its eigenvalue on e_h. Evaluating at h = 0 and h = 1 gives W_m(0) = K(J_1,J_1) and W_m(1) = K(J_1,J_1) + 2K(J_2,J_2); so for odd p the pair (K(J_1,J_1), K(J_2,J_2)) vanishes mod p iff W(U,U) annihilates both e_0 = 1 and e_1 = x. Is that two-entry subpacket already certifying (no prime p > m+1 divides both)?

**Result (computed, m = 3..11; exact via the signed-walk DP; log `experiments/linear_alternation/witness_search_out.txt`).**

| m | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|
| gcd(K(J_1,J_1), K(J_2,J_2)) | 1 | 1 | 4 | 4 | 2 | 12 | 18 | 16 | 8 |
| gcd of first three entries | 1 | 1 | 4 | 4 | 2 | 12 | 18 | 16 | 8 |
| full gcd over d (§30) | 1 | 1 | 4 | 4 | 2 | 12 | 18 | 16 | 8 |
| primes > m+1 dividing K(J_1,J_1) alone | – | – | – | – | 23 | 30539 | 9989341 | 21966239 | 3019, 13647452681 |

So through rank 11 **the first two entries already carry the whole content** (no prime factor above 3 in any of them), while the first entry alone fails at ranks 7–11 (c_{m,1} = K(J_1,J_1) has large prime factors 23, 30539, 9989341, 21966239, 3019, 13647452681). For every prime p with m+1 < p ≤ 2000 the smallest index d with K(J_d,J_d) ≢ 0 (mod p) is d = 1 except at m = 7, p = 23, where d = 2 is needed (checked for m = 3..11). Rank 12 was still running when this was written.

**What this is and is not.** It is exploratory evidence for a narrower target than the full packet: "W(U,U) does not kill both 1 and x modulo any prime p > m+1", equivalently gcd(K(J_1,J_1), K(J_2,J_2)) has no prime factor > m+1 (for p odd). It is **not** a proof, and two-coefficient shortcuts have failed before in neighbouring settings (shifted margins {13..16}; the last two coordinates of the projected Witt packet at rank 13 vanish mod 19). Here the two entries are the first two (not the last two), the margins are consecutive from 2, and the data stop at m = 11, so no extrapolation is justified. A proof would need to show directly that W(U,U)·1 and W(U,U)·x cannot both vanish in F_p[x]/(x^p) — an explicit pair of vacuum-type matrix elements of the alternating commutator product, which is a smaller object than the whole operator.

---

## 32. The sparse cyclic difference operator and the reciprocity criterion (2026-11-30)

**Setting.** r = m−1, U = {2..m}, w = ΣU, p > m+1 prime. W(U,U) is the alternating commutator product of §30; its eigenvalue on e_h is W_m(h) = Σ_d d·C(h,d−1)·K(J_d,J_d). The report replaces the dense staircase matrix B (B_ij = 1 for i ≤ j, −1 for i > j; symmetric ordering e^{uD}e^{vX} = e^{uv/2}e^{uD+vX}) by its sparse inverse.

**Sparse inverse (computed).** With B_θ = B + θ·11ᵀ and λ = (1−θ)/(1+θ): B_θ⁻¹ = ½C_λ, C_λ = 1 on the diagonal, −1 on the superdiagonal, last row (λ, 0, …, 0, 1), and det B_θ = 2^{r−1}(1+θ). Verified exactly for r = 2..7 and five values of θ.

**Complementary-exponent duality (computed).** Define c_T(J) = [t^J] Alt_t Δ_J(Tt) in F_p[t_1..t_r]/(t_i^p), J ⊆ {0..p−1} increasing, J^∨ = {p−1−j} (sorted). Then c_T(J) = det(T)^{p−1} c_{T^{−1}}(J^∨). Verified on 36 random (T,J) pairs at p = 5, 7 with r = 2, 3 (no mismatches; most values nonzero). This pins down the reading of the report's notation (coefficient of t^J in the alternation).

**Main equivalence (computed, 7 cases).** With A = U^∨ = {p−m−1..p−3} (size r), f_{m,p}(λ) = c_{C_λ}(A) (degree ≤ p−3) and ε = (−1)^{r+w}:
Φ(θ) := (1+θ)^{p−1} f(λ) + ε(1−θ)^{p−1} f(1/λ) = Σ_{d=1}^m d·K(J_d,J_d)·((θ−1)/2)^{d−1} (mod p).
Checked for (m,p) = (3,5), (3,7), (3,11), (4,7), (4,11), (4,13), (5,7) at every θ ∈ F_p∖{±1} (λ ≠ 0): the two sides agree **exactly (ratio 1)**, with many nonzero values. Hence W(U,U) ≠ 0 over F_p ⇔ f_{m,p}(λ) + ελ^{p−1}f_{m,p}(1/λ) ≢ 0 (the report's theorem (3)), at least in these cases.

**Componentwise structure (computed over Z).** Writing f_A = Σ_{b∈A} f_{A,b} (terms whose last-row exponent is b; each of degree ≤ b):
- Reciprocity (6): f_{A,b}(λ) = (−1)^{r−1+L−b} λ^b f_{A,b}(1/λ), L = ΣA: **37 (A,b) cases, 0 mismatches** (35 nontrivial; sets A of sizes 3–5 with entries ≤ 7, including 0).
- Rank-lowering (5): [λ^M]f_A = (−1)^{r−1+L−M} f_{A∖{M}}(0), M = max A: 11 sets, 0 mismatches.
- Consequently G_{m,p}(λ) = f + ελ^{p−1}f(1/λ) = Σ_b (1 − (−λ)^{p−1−b}) f_{A,b}(λ) (algebra: ε(−1)^{r−1+L−b} = −(−1)^b since L ≡ w mod 2).

**Abstract cancellation model (arithmetic checked).** F_M = (1+λ³)(1 − ελ^{p−6}), F_{M−1} = −(1−λ²)(1 − ελ^{p−6}) have the right degrees (M = p−3), F_M(0) = 1, satisfy the reciprocity signs, and (1−λ²)F_M + (1+λ³)F_{M−1} = 0. So reciprocity plus the extreme-coefficient identity cannot by themselves force nonvanishing; a proof must use further relations among the genuine flow components. (These are abstract polynomials, not determinant coefficients.)

**Centered eigenvalue polynomial (computed, m = 3..11).** W_m(−h−1) = ±W_m(h) as polynomials, signs −, +, +, −, −, +, +, −, − for m = 3..11 (period 4); in the centered variable z = 2h+1, W_m is even or odd. The two highest nonzero coefficients (denominators cleared) have no prime factor > m+1 for every m = 3..11; the leading coefficient alone acquires large primes from m = 9 (569 at m = 9, 1974029 at m = 10, 4608319 at m = 11) and cannot be a uniform witness — as reported. Degrees of W_m: 1, 2, 2, 3, 5, 6, 6, 7, 9 (m = 3..11).

**Diagonal one-hole contents.** gcd_d K(J_d,J_d), m = 3..12: 1, 1, 4, 4, 2, 12, 18, 16, 8, 16 (rank 12 now computed here: 16; the first two entries again carry the whole content, and K(J_1,J_1) alone has the large prime factors 29 and 12953077208391719881 at m = 12, with witness index 2 at p = 29). The report lists 8, 32, 32 for ranks 13, 14, 15; not recomputed.

**Not reproduced.** The proofs of the sparse-flow rank-lowering identity and of the Fourier-automorphism symmetry (the symmetry itself was verified numerically above); the exact normalisation relating Φ to the standard polynomial (we verified the identity against W_m(h) directly); eq. (8)/(9) in the lost-symbol form; the counts of 90 + 374 identity checks; ranks 13–15 gcds.

**Status.** The conjecture (★) is unchanged and open. New exact facts: the dense Weyl calculation is equivalent to the sparse cyclic polynomial f_{m,p} and a reciprocity-failure statement, with an explicit rank-lowering identity and component-wise reciprocity; and an explicit abstract model shows these structures alone do not force nonvanishing. The remaining task is a joint relation among the flow components f_{A,b}, b ∈ A, specific to the genuine determinant, that rules out Σ_b(1 − (−λ)^{p−1−b})f_{A,b} ≡ 0 — still missing.

---

## 33. Singular-point multiplicity, a sharper cancellation obstruction, and the multivariate flow lemma (2026-12-01)

This round is mostly a strategy memo; the statements below were checkable and were checked.

**t-form of the eigenvalue polynomial (computed).** Put H_{m,p}(t) = G_{m,p}(−t), G = f_{m,p}(λ) + ελ^{p−1}f_{m,p}(1/λ) (§32). Then
H_{m,p}(t) = Σ_{h=0}^{p−1} W_m(h)t^h = Σ_{d=1}^m d·κ_{m,d}·t^{d−1}(1−t)^{p−d} (mod p), κ_{m,d} = K(J_d,J_d).
The binomial-sum identity Σ_{h<p} C(h,k)t^h ≡ t^k(1−t)^{p−1−k} (mod p) holds for all k < p at p = 5, 7, 11, 13; and G(−t) (computed from the sparse cyclic polynomial of §32) equals the right-hand side at every nonzero t ∈ F_p for (m,p) = (3,7), (4,11), (4,13), (5,7). Since the d-th summand vanishes to order exactly p−d at t = 1 and d < p, **ord_{t=1} H_{m,p} = p − max{d : κ_{m,d} ≢ 0 (mod p)}**, so (T) is equivalent to a bound on the multiplicity of the root t = 1 of the genuine cyclic-flow polynomial (this is the setting where C_λ degenerates to the rank-(r−1) cyclic difference matrix with kernel spanned by the all-ones vector).

**Sharper abstract-cancellation theorem (computed).** Let P_n^η = {q : deg q ≤ n, q(t) = η t^n q(1/t)}, N = p−1, and let g_2 ∈ P_{N−2}^{−ε}, g_3 ∈ P_{N−3}^{−ε}. The map (g_2,g_3) ↦ (1−t²)g_2 + (1−t³)g_3 into P_N^ε has image exactly {H ∈ P_N^ε : H(1) = 0}: verified over ℚ by rank for N = 4..14 and both signs (image dimension equals dim P_N^ε minus the one condition for ε = +1, and equals dim P_N^{−1} for ε = −1, where H(1) = 0 is automatic); the image lies in the target by direct reciprocity check, so equal dimension means equality. The kernel contains (g_2,g_3) = ((1+t+t²)q, −(1+t)q) since (1−t²)(1+t+t²) = (1−t³)(1+t) (checked). **Consequence:** two abstract reciprocal components suffice to cancel every other component; a proof of (T) cannot rest on degree bounds, componentwise reciprocity, a nonzero extreme coefficient, or the known parity/vanishing constraints alone.

**Multivariate flow polynomial and the diagonal-flow lemma (computed).** F_A(t_1..t_r) = [x^A] Alt_x det((x_i − t_i x_{i+1})^{a_j}), x_{r+1} = x_1. Verified by direct expansion on A = (2,3,5), (1,3,4), (2,4,5), (1,2,3,4), (2,3,4,6) and every 0 ≤ k ≤ min A:
[t_1^k⋯t_r^k] F_A = (−1)^{rk} r! ∏_{a∈A} C(a,k),
nonzero mod p for p > max A (elementary: equal transfers force the two exponent permutations to coincide). **Caveat (mine):** the univariate polynomial f_A(λ) is the specialisation t_i = 1 (i < r), t_r = −λ, which sums *all* flow monomials with weights; the diagonal coefficients are single terms among many, so their nonvanishing does not by itself constrain f_A. The "projection faithfulness" the memo proposes (vanishing of the reciprocal univariate projection forces a diagonal-flow coefficient to vanish) is exactly the unproved step and, as stated, would need an argument that recovers an individual coefficient from a sum of weighted ones.

**Shifted families.** The rank-lowering identity applied to A = {p−m−1..p−3} removes its maximum; complementing again gives {3..m}, not {2..m−1}. So the natural induction passes through shifted intervals U_{r,c} = {c, …, c+r−1} (and probably holed sets), not through the preceding instance of the target.

**Not checked.** The parity/multiplicity table (lost in transmission); the symplectic-automorphism and sl_2 arguments; the claimed relevance of Dzhumadil'daev–Yeliussizov path decompositions (not read); the comparison with the ProofAtlas program.

**Status.** (★)/(T) remains open. Verified new facts: the t-form identity and multiplicity formula, the exact image theorem for two reciprocal components, and the diagonal-flow lemma. Still missing: a joint relation among the genuine flow components (or a faithfulness statement linking the univariate projection to the multivariate polynomial) that rules out ord_{t=1}H_{m,p} = p.

---

## 34. Attempt to close the gap: two structural searches, both negative (2026-12-01)

**Search 1 — cross-rank structure of the eigenvalue polynomials W_m (computed, m = 3..11).** In the centered variable z = 2h+1, with W_m(h) = Σ_d d·C(h,d−1)·κ_{m,d} (exact):
W_3 = z; W_4 = (3z²+1)/4; W_5 = 3z²+1 = 4·W_4; W_6 ∝ z(5z²−26); W_7 ∝ z(21z⁴ − 17330z² + 63677); W_8 ∝ 147z⁶ − 533645z⁴ + 17803649z² + 6183801; W_9 ∝ 111524z⁶ − 116873785z⁴ + 2923472606z² + 1029196599; W_10, W_11 odd in z with coefficients up to 10²¹.
The relation W_5 = 4W_4 is a small-rank coincidence. For m ≥ 6 the only common factor between any two of these polynomials (checked for all pairs m, m−s, s ≤ 4, by exact polynomial gcd and division) is z, which comes from parity (odd-type ranks), so there is **no cross-rank factorisation or recursion** between the W_m. The hope that the polynomials build on each other (which would have given an induction) is false.

**Search 2 — the shifted intervals produced by the rank-lowering identity (computed).** Let D(r,c) = κ(I_{r,c}, I_{r,c}), I_{r,c} = {c, …, c+r−1}. Exact finite-difference analysis:
- r = 2: D = 1 − c (degree 1; agrees with κ({a,b},{a,b}) = 2 − C(b,a) at b = a+1).
- r = 3: D = −c⁴/4 + … (degree 4 in c, fourth difference constant −6 on 15 data points; values 0, 1, −6, −36, −110, −255, −504, −896, …).
- r = 4: degree 10 in c (15 data points, differences of order 11 vanish).
- Degrees 1, 4, 10 = C(r+1,3) (r = 2, 3, 4); r = 5 not resolved with 12 points (degree ≥ 11, presumably 20).
- D(r,1) = 0 (the known vanishing for the interval starting at 1) and D(r,c) ≠ 0 for 2 ≤ c ≤ 14 (r = 2..4).
- The values at c = 2..8 carry large primes with no product pattern (e.g. D(4,4) = 2·397, D(4,7) = 2²·3·7·7901, D(5,3) = 2²·569, D(5,7) = 2²·3·7²·18502153), so there is **no closed product formula** in c.
So the family needed for an induction through shifted intervals consists of values of explicit polynomials in c of degree C(r+1,3) with huge, structureless coefficients. That is consistent with the earlier picture: the individual coefficients are not controllable, and only the collective content (gcd over d) behaves.

**Honest conclusion.** The conjecture (★) remains open. Nothing found here, or in any earlier section, proves that the content of the diagonal one-hole packet (equivalently R_m, equivalently W_m ≢ 0 mod p) has no prime factor above m+1. What the programme has produced is (i) a chain of exact reductions to this one arithmetic statement, (ii) several equivalent finite formulations (binary polynomials R_m, V_m; the diagonal one-hole packet; the Weyl operator W(U,U); the sparse cyclic polynomial; the multiplicity of a root at t = 1), (iii) extensive verified numerical evidence (only the primes 2 and 3 ever occur, through rank 12–13 verified here and 17 reported), and (iv) a catalogue of proof strategies that are *provably insufficient* (universal saturation, intra-rank propagation, one-vertex induction, reciprocity plus degree bounds, linear rank descent, cross-rank factorisation). Closing the gap requires a genuinely new ingredient specific to the signed alternating structure of these determinants.

---

## 35. The deformed exterior algebra, the hypersurface F_m, and rank lifting with at most one exceptional parameter (2026-12-01)

**The algebra (computed).** Odd generators ξ_1..ξ_m, η_1..η_m, tensored with the normally ordered Weyl algebra ([D,X] = 1); u_k = Σ_{i≥k} ξ_i X^{i−k}/(i−k)!, v_k = Σ_{a≥k} η_a D^{a−k}/(a−k)!, Z_m(c) = Σ_k c_k u_k v_k, F_m(c) = top (ξ_1⋯ξ_mη_1⋯η_m) coefficient of Z_m(c)^m. Verified exactly (rational arithmetic, symbolic Weyl normal ordering):
- cross-relation (1): v_k u_l = −Σ_{s≥0} u_{l+s}v_{k+s}/s! (m = 3, all k, l);
- expansion (2): Z_m(c*) = Σ_{i,a} ξ_iη_a [D^a/a!, X^i/i!] at c* = (1/k!) (m = 3, 4);
- **the top coefficient is always a pure scalar** (no X^iD^j with (i,j) ≠ (0,0)), so F_m is an ordinary polynomial; F_2 = c_1(c_1−2c_2), F_3 = −(3/2)c_1(c_1−2c_2)(c_2−2c_3), F_4 = (1/3)c_1(c_2−2c_3)(c_1² − 3c_1c_2 − 6c_1c_3 + 18c_1c_4 + 18c_2c_3 − 36c_2c_4) all reproduced at random rational points;
- cyclicity τ(fg) = τ(gf) for even elements (16 random trials, m = 3, 4; all equal);
- gradient formula (5): ∂F_m/∂c_d = m·τ(u_dv_d Z^{m−1}), checked against exact derivatives (m = 3, 4);
- **recursion (9):** F_m(c_1..c_m) = F_m(c_1..c_{m−1}, 0) + (−1)^{m−1} m c_m F_{m−1}(c_1..c_{m−1}) (m = 3, 4, 5);
- F_m(c*) = 0 for m = 2..7.

**Factorial-point gradients (computed; primitive integer vectors, m = 2..7).** ∇F_m(c*) ∝ (1,−2); (−1,2,0); (1,−6,12,0); (1,−6,12,0,0); (−7,−26,240,−480,0,0); (483,3314,−24840,41280,50400,−100800,0); each has content 1 over ℤ[1/m!] (the scaled integer vector has gcd 1), so ∇F_m(c*) ≢ 0 modulo every prime p > m+1 for m ≤ 7 — consistent with (7)–(8) and with T_m ≠ 0.

**Rank lifting (consequence of (9); computed).** With c′ = (1/k!)_{k<m} and t the last parameter: ∇F_m(c′,t) = (ℓ_m + (−1)^{m−1} m t·g_{m−1}, 0), ℓ_m = ∇L_m(c′), g_{m−1} = ∇F_{m−1}(c′). Verified for m = 3..8 (including the last component and F_m(c′,t) constant in t). Exceptional t (where the gradient vanishes) exists only if ℓ_m ∥ g_{m−1}. **Computed:**

| m | ℓ_m ∥ g_{m−1}? | gcd of 2×2 minors of (ℓ_m, g_{m−1}) | exceptional t | factorial value 1/m! |
|---|---|---|---|---|
| 3 | yes (ℓ = −¾·g) | – | t₀ = 1/4 | 1/6 |
| 4 | no | 1 | none | – |
| 5 | yes (ℓ_5 = 0) | – | t₀ = 0 | 1/120 |
| 6 | no | 1 | none | – |
| 7 | no | 7 | none | – |
| 8 | no | 1 | none | – |

So in every case computed the factorial parameter is not exceptional (at m = 3, 5 an exceptional value exists but differs from 1/m!; at m = 4, 6, 7, 8 there is none, and the minor gcds 1, 1, 7, 1 have no prime factor above m+1). This is exactly the "leakage" condition (11) of the report, ℓ_m ≠ ((−1)^m/(m−1)!)g_{m−1}, evidenced here for m ≤ 8; it is equivalent to ∇F_m(c*) ≠ 0 and hence to T_m ≠ 0 (Theorem 1), so proving it is the original problem again (the rank-lifting theorem itself, "all but at most one t is smooth if rank m−1 is smooth", is rigorous and verified, but does not exclude t = 1/m!).

**Gauge counterexample (computed).** p = 7, A = {4,5}: f_1(t) = F_A(1,t) ≡ t + 3t² + 6t³ + 3t⁴ + t⁵; its reciprocal antisymmetric projection f_1(t) − t⁶f_1(1/t) vanishes identically; in the gauge z = (1,4) (t_1 = z_1/z_2, t_2 = t z_2/z_1) the projection equals 5 + 3t + 4t⁵ + 2t⁶ ≠ 0 — reproduced exactly. So vanishing of the identity-gauge reciprocal projection does not force vanishing of other gauges for A = {4,5} (a consecutive set starting at 4, not the shifted target set). The character-orthogonality averaging formula (12), f̄(t) = r!Σ_k (−1)^{rk}(∏_{a∈A}C(a,k))t^k, is consistent with the diagonal-flow lemma verified in §33 (not separately recomputed).

**Individual-pattern identities (computed).** (13): P_r({0}∪A, {0}∪B) = S_{r−1}(A,B) for the D-first alternating pattern P and S = P + (−1)^rQ (Q = X-first): verified on three cases (r = 3, 3, 4). (15): if S_{m−2}({2..m−1},{2..m−1}) = Σ a_kX^kD^k then P_{m−1}({1..m−1},{1..m−1}) = Σ_k a_k/(k+1)² X^{k+1}D^{k+1}: verified for m = 4, 5 (all ratios exactly 1).

**Not reproduced.** The hypersurface-smoothness equivalence proof details beyond the consistency checks above, the explicit statement that the full consecutive standard polynomial vanishes for the scalar argument, the counts "rank-16 gcd(κ_{16,1}, κ_{16,2}) = 96", and the lost gradient table (our primitive gradient vectors are listed above for m ≤ 7).

**Status.** (★) is unchanged and open. New exact structure: a single-element nilpotence formulation (Z_m(c*)^{m−1} = 0), the hypersurface F_m with the exact recursion (9), and the leakage condition (11); in all computed ranks (m ≤ 8) the factorial point is smooth, with no exceptional parameter at all for m = 4, 6, 7, 8. A proof of (11) in general would complete the induction; it is the same arithmetic content as before.

---

## 36. Removing the lowest generator pair: Bernoulli extension and the four-component recurrence (2026-12-01)

**Setting.** In the deformed exterior algebra of §35 (Z_m = Σ u_iv_i/i!, with Z_m^{m−1} ≠ 0 ⇔ T_m ≠ 0), put P = u_1, Q = v_1, n = m−1, U_j = u_{j+1}, V_j = v_{j+1} (the copy of the rank-n algebra), C = Z_n = Σ_{j=1}^n U_jV_j/j!, B = Σ_j U_jV_j/(j+1)!.

**Exact structure (computed, m = 3, 4, 5).**
- PQ + QP = −C, P² = Q² = 0, [P,C] = [Q,C] = 0, Z_m = PQ + B.
- S = PQ + ½C satisfies S² = ¼C².
- **Bernoulli rank extension (3):** B − ½C = −Σ_{k≥1} (B_{2k}/(2k)!) L^{2k−1}C, L(U_iV_j) = U_{i+1}V_{j+1}. Verified in the algebra (and by hand: the coefficient identity is Σ_{r=0}^i C(i+1,r)B_r = 0), so Z_m = S − (1/12)Z_{m−2}^{shifted} + (1/720)Z_{m−4}^{shifted} − …

**Four-component recurrence (computed, m = 3..6).** Writing Z_m^k = A_k + PU_k + V_kQ + PH_kQ (A_k, H_k even; U_k, V_k odd; all in the lower-rank algebra) with the super-derivations δ_P = [P,·]_super, δ_Q = [Q,·]_super:
A_{k+1} = A_kB + V_k δ_QB, U_{k+1} = U_kB + H_k δ_QB, V_{k+1} = −δ_PA_k + V_k(B−C), H_{k+1} = A_k + δ_PU_k + H_k(B−C), with A_0 = 1, U_0 = V_0 = H_0 = 0.
Verified by rebuilding Z_m^k = A_k + PU_k + V_kQ + PH_kQ from the recursion and comparing with direct multiplication in the full algebra: **exact for every k = 0..m−1 at m = 3, 4, 5, 6**. Consequences checked: H_1 = 1, H_2 = 2B − C, H_3 = 3B² − 2BC − CB + C² + δ_Pδ_QB (m ≥ 4), and Z_m^{m−1} ≠ 0 together with H_{m−1} ≠ 0 at each rank. (With the Bernoulli correction switched off, B = C/2: H_n^{(0)} = 2^{1−n}C^{n−1} for n odd and 0 for n even, from S² = C²/4, so the odd and even rank inductions behave differently.)

**Boundary identity (12) (computed).** For Y = u_{m−1}v_{m−1} + ½u_mv_m: Y² = 0 and Y·f·Y = u_{m−1}u_mv_{m−1}v_m E_uE_v f for f = u_av_b, all a, b (m = 4: 16 cases, m = 5: 25 cases, no mismatch).

**New exact numerical identity (computed, m = 3..11).** Σ_{d=1}^m (−1)^{d−1} κ_{m,d} = 0 (equivalently W_m(−1) = (−1)^{...}·…; it is identity (6) of the report), i.e. the one-hole diagonal coefficients satisfy one fixed alternating linear relation at every rank tested.

**Adjacent-gradient transversality table (computed; exact match with the report).** With G_{m,d} = Σ_{e≥d} (−1)^{e−d}(e!/(e−d)!) κ_{m,e}, the gcd of all 2×2 minors of (G_m, G_{m−1} padded with 0): m = 4: 4; 5: 0 (parallel); 6: 64; 7: 2240; 8: 192; 9: 3024; 10: 9216; 11: 2816. Every nonzero gcd has only prime factors ≤ m+1 (2240 = 2⁶·5·7, 3024 = 2⁴·3³·7, 2816 = 2⁸·11). Rank 5 is the genuine exceptional (proportional) case, as reported.

**Centered parameters (algebra).** b_i = Σ_{j≤i} (−1/2)^{i−j}c_j/(i−j)! turns the factorial point into Σ b_it^i = 2sinh(t/2), so b_{2j} = 0 and b_{2j+1} = 1/(2^{2j}(2j+1)!); the Fourier involution then acts by b_i ↦ (−1)^{i+1}b_i. (Consistency of the claimed parity support of the gradient with the eigenvalue parity of §32 was not separately re-derived.)

**Not reproduced.** The proof of the factorization theorem (Z_m^k = A_uι_{u_1}Z_m^k), the lowest-pair detection corollary (7) (only consistent), the marked-moment formula (13) and its vanishing at ranks 6–7, and the recurrence check at ranks 7–8.

**Status and the exact target.** Conjecture (14): in the rank-n algebra, C^{n−1} ≠ 0 ⇒ H_n ≠ 0 (mod every p > n+2), where H_n is produced by the recurrence above with B = (½ − L/12 + L³/720 − …)C. By (9) this is literally the induction step "rank n certificate ⇒ rank n+1 certificate", i.e. the problem is unchanged; what is new is that all interfering terms are now explicit expressions in C, its raising derivation L, and the super-derivations δ_P, δ_Q (δ_P² = δ_Q² = 0, δ_Pδ_Q + δ_Qδ_P = −ad_C). Open.

## 37. Single-transfer operator on the smaller exterior algebra (report of 2026-11-27, late)

Scripts: `experiments/linear_alternation/transfer_checks.py`, `transfer_ops.py`, `transfer_claims.py` (exact rational arithmetic; Phi^{-1} by triangular peeling on the (0,0) Weyl coefficient).

**Reproduced (exact, n = 2..5, i.e. algebra ranks m = 3..6 for the identities; n = 3..5 for the operator claims):**
- Component reconstruction (Thm 1): U_k = R_v H_k, V_k = R_u H_k, A_k = (R_uR_v + K) H_k, with E^s the s-th power of the raising derivation and ordinary exterior wedge. The wrong-order variants fail where the test is non-degenerate (k = 2, 3), so the formulas are pinned down.
- Transfer identity: T(f) = (R_u + delta_P)R_v f + K f + f*(B - C) satisfies T(H_k) = H_{k+1} for all k (n up to 5). So H_k = T^{k-1}(1).
- T preserves the balanced grading B_{n,k} -> B_{n,k+1}.
- Terminal vanishing (6): T(B_{n,n-1}) = 0 (n = 3,4,5).
- Terminal surjectivity (5): rank of T: B_{n,n-2} -> B_{n,n-1} is n-1 = dim M_n and the image has zero e_n row (n = 3,4,5).
- Pivot (8): coefficient of e_{n-1} in T(a_n) equals -C(n,2)/(n+1)! (-1/8, -1/20, -1/72).
- Obstruction example: h = 24U1V1 + 12U2V2 + 5U3V3 has T_3(h) = 0; ker T on B_{3,1} is exactly one-dimensional, spanned by it.
- P_n = T^{n-2}: B_{n,1} -> M_n has rank n-1 and P_n(H_2) != 0, P_n(q_n) != 0 for n = 3,4,5. rank{P(H_2), P(q_n)} = 2, 1, 2 for n = 3, 4, 5 (the n = 4 proportionality matches the report's non-injective rows). Smith invariants of the 2-column map: n=3 {1,16}, n=5 {1,4320} (primes 2,3,5 only).

**Not reproduced:** Smith table for ranks 6-8 (run for n = 6, 7 started, not finished at time of filing); seed rigidity (9) (the discrepancy operator E_n is not defined in the paste, so it cannot be tested as written); the proofs of Thm 1, (5), (6), (8) beyond the small-rank checks.

**Status.** Everything checkable is consistent. The step "P_n(H_2) != 0 mod p for all p > n+1" is the same open statement (14) in a more explicit linear-algebra form; no proof of it, or of Graham's conjecture, is claimed.
