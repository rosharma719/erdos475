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
