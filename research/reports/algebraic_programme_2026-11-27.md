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
2. **Push the binary data further** with the vectorized code (n = 10, 11 are cheap) and look for the first rank where β_n has a prime factor > n — that would be the first real test of LAC.
3. **Hunt for the transfer identity** (the two-arc / exterior-minor route): find a triangular filtration under which one minor contributes a unit and the rest lie lower. This is where all analytic attempts have stalled.
4. Keep a falsification track: a prime p > n dividing β_n (and every stronger packet) would give a precise, finite case in which to search for a genuine counterexample or for a still stronger certificate.

## 11. Caveats
- Several results are quoted from external sessions; only those tagged [run] or [hand] were checked here.
- Literature IDs for Oct-2026 papers and the ProofAtlas record were not verified; overlap with ProofAtlas's unpublished working materials is unknown. Novelty is claimed for none of this.
- "No counterexample found" refers to algebraic transfer statements at small ranks; no systematic search for counterexamples to Graham or to LAC was run.
