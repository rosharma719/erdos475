# Linear alternation packet (Hicks–Ollis–Schmitt coefficients c_{m,r})

Source: uploaded by the repo owner from an external session (2026-11-26); not produced by the repo engine.

- `linear_alternation.cpp` — exterior-algebra DP (needs Boost.Multiprecision; m=14 ≈ 2.4 GB). **Not compiled or run here** (no Boost in this container).
- `results_reported.txt` — reported c_{m,r} and gcds for m=3..14. (The m=14 line has a stray trailing comma, so the file was not copied verbatim from the program's output; it still has 14 entries.)
- `brute_check.py` — independent brute force over all m! permutations, exact integers, straight from the definition (no shared code with the C++).

## Verified here
- m=3..10: `brute_check.py` reproduces `results_reported.txt` exactly (vectors and gcds); outputs in `brute_out.txt`.
- m=3..14 (reported data only): sum = 0, reversal symmetry, recomputed gcd = reported gcd, and every prime dividing g_m is ≤ m+1.

## Not verified here
- m=11..14 values (only the C++ run supports them; internal consistency checks pass).
- That the C++ DP is correct beyond m=10 (it matches brute force on the m ≤ 10 values reported).

## Logic
Theorem 3 (p ∤ g_m ⇒ every (m+1)-subset of F_p^× is orderable) is sound under the repo's convention that intervals starting at position 1 are exempt: put a_0 first, with Σ−a_0 ≠ 0. Since every prime dividing g_m is ≤ m+1 < p, this gives |A| ≤ 15 for all p, *provided m=11..14 are right*. Overlaps with Hicks–Ollis–Schmitt (≤ m=10) and Costa–Pellegrini (m=11); it is not new below that. The all-m statement ("LAC": every prime factor of g_m ≤ m+1) is unproved.

## Split-jet / coinvariant programme (second upload, 2026-11-26)
- `split_jet_check.py` (uploaded) — exact reduction in R_7 ⊗ F_3 (Artin-basis normal forms). Rerun here: output in `split_jet_out.txt` matches the report's table (all value packets A_j = 0; only cut j=4 has a nonzero jet, 10 coordinates, coefficient 1 on u2·u3²·u4²·u5³·u6⁵·u7⁶). This confirms the script reproduces the report; it does not test the reductions behind the script.
- `check_sec5_identity.py` (written here, independent) — tests λ_{m+1}(t^{m−d}·W·G_{m+1}) = −K_m(W) for random monomials W, m=3,4,5 (18 cases): exact integer alternation vs. complex roots-of-unity evaluation. All agree.
- Read-through (not machine-checked): Q_n = F_{n−1} as polynomials, cyclic-rotation invariance of Q_n up to sign, socle argument ([Q_n]≠0 ⇔ [G_n]≠0), the Ann(xy)=(h_{n−2}) route, Sym² decomposition and the D(d) matrix algebra all look correct. Note p=3 ≤ m+1 at m=7, so the split-jet run is a stress test, not an instance of Graham.
- Still open (as the report says): the first-order transfer theorem (A_j=0 ∀j, V_m≠0 ⇒ ∃j B_j≠0). No evidence beyond the single m=7, p=3 run.
- ProofAtlas overlap and the higher-degree-W criterion's novelty are unchecked.

## Quadratic packets / content recurrence (third upload, 2026-11-26)
- `exact_quadratic_packets.py` (uploaded) — exact integer linear (A), first-order (B) and quadratic-kernel (T) contents. Ranks 4–8 rerun here (`quad_out_to8.txt`, 29 s for n ≤ 8):

| rank n | A (= g_n) | B matrix content (= b_n) | T matrix content (= d_n) |
|---|---|---|---|
| 4 | 1 | 2 | 1 |
| 5 | 2 | 2 | 1 |
| 6 | 4 | 2 | 2 |
| 7 | 6 | 2 | 2 |
| 8 | 12 | 2 | 2 |

  The A column matches the c_{m,r} gcds from the brute force (g_4..g_8 = 1,2,4,6,12). The table matches the report's table, and the recurrence d_{m+1} = gcd(g_m, b_m) (report Thm 3) holds for m = 4..7 (d_5..d_8 = 1,2,2,2). That is a numerical check of 4 instances, not a proof of Thm 3.
- Rank 7 cut 4 is the only cut whose B content is not divisible by 3 (matrix content 2 vs 6), consistent with the earlier split-jet run.
- Read-through of the report's analytics: Thm 4 (residual detection) re-derived by hand and sound (needs p ∤ (m−1)(m−2)); the §9 harmonic example (cyclic sum of 5-variable Vandermondes) checks out; Thm 1's dimension count (2(n−1)! − (n−2)!) is consistent. The proofs of Thm 1 and Thm 3 were not re-derived line by line.
- Unreconciled: the report quotes ProofAtlas quadratic contents "1,1,2,2,2,2,2 for ranks 3..9", while the table above gives d_4..d_8 = 1,1,2,2,2 — apparently shifted by one rank (different indexing). Unchecked.
- Open and unchanged: d_m ∈ (g_m, r_m)·Z[1/(m+1)!]. No uniform proof; no counterexample.

## Binary alternation reduction (fourth report, 2026-11-27) — no files were attached, so this is an independent reimplementation
- `binary_alternation_check.py` (written here from the report's definition; third, independent method): evaluates P_{n,d}(1,ζ^j) = Alt_z(Q_n)/Δ(z) on z = μ_n∖{1,ζ^j} with numpy over all (n−2)! permutations, fits P(1,T) (degree n−3) and rounds (rounding error ≤ 3e-8). Output: `binary_out.txt`, n = 4..9 (0.3 s total).
- **Reproduced exactly:** P_{6,2} = [2,8,−8,−2], P_{7,2} = [40,−18,−236,−18,40], P_{8,2} = [−1662,−2478,13716,13716,−2478,−1662], P_{9,1} = [−366468,−1536312,−1976146,0,1976146,1536312,366468]; binary contents β_4..β_9 = 1,1,2,2,6,2.
- **Reproduced structural claims (n ≤ 9):** reflection law (symmetric for n ≡ 0,3 mod 4, antisymmetric for n ≡ 1,2); P_{n,n/2} ≡ 0 for n = 4, 8; (a+b) | P_{n,1}; (a−b) | P when antisymmetric; boundary relation: the constant terms P_{n,d}(1,0) are exactly ±{c_{n−1,r}} (e.g. n=8: 966, 1662, 1338, 0; n=9: 366468, 92412, 144324, 314556), so β_n | g_{n−1} (1|1, 1|1, 2|2, 2|4, 6|6, 2|12).
- **Read-through:** Theorem 1's logic is sound — partial alternation descends R_n → B_n = K[a,b]/(h_{n−1},h_n) and deg P = n−3 < n−1, so P ≢ 0 ⇒ Q_n ≠ 0 in R_n⊗F_p. Q_n|_{b=0} = F_{n−1} checked by chord counting. det(I−C) = n on the reflection representation: correct.
- **Not checked:** the Fourier-inversion formula for q_{n,d,k}, the CRT coefficient bound, Theorem 3 (two-arc shuffle identity), the L_s factor formulas and the "two universal factors" proposition, and the Artin-reduction implementation referenced for rank 8–9 (not provided). The report's "uniform primitive-minor isolation" remains open, as it says.
- **Significance:** for every rank computed, all primes dividing β_n are ≤ n, so this adds no new coverage of admissible Graham instances; it matters only if LAC fails at some rank (β_n | g_{n−1} makes it a strict strengthening). The rank-9 quadratic-packet run (`exact_quadratic_packets.py 9`) was killed by its 1700 s limit without finishing, so d_9 = gcd(12,2) is still unverified directly.

## Binary alternation, n = 10, 11 (2026-11-27)
- `binary_range.py` (run with `PYTHONPATH=. python3 binary_range.py 10 11`), output `binary_out_10_11.txt`. n = 10: β_10 = 2, P_{10,d}(1,0) = ±c_{9,r}, rounding error < 5e-5. n = 11: float64 rounding error up to 0.5, coefficients not reliable, but β_11 = 1 is forced by β_n | g_{n−1} and g_10 = 1.
- Consequence: g_3..g_14 involve only primes 2 and 3, so no binary content for n ≤ 15 can exceed those primes. A meaningful LAC test needs g_15+ or exact-arithmetic binary computations at n ≥ 16.

## Arbitrary-order transfer report (2026-11-28) — independent checks
Scripts (written here): `transfer_checks.py`, `witness_checks.py` (run with `PYTHONPATH=. python3 witness_checks.py`; `transfer_checks` prints its own checks on import).
- **Thm 1 (edge insertion), Q_{m+1}(h,x) = ±W_m(x)(h+x_0)Q_m(h+x_0,x_1..)**: exact integer check, m = 3..8, 20 random zero-sum points each. All agree.
- **Thm 3 (centered power sums p_k(u) = ((m+1)−(m+1)^k)/m^k h^k)**: derived by hand (binomial expansion with p_j(x) = −h^j) and checked on roots of unity, m = 3..6 (error ~1e-15).
- **Thm 4 (Poincaré transfer λ_{m+1}(h^{m−r}G) = (−1)^r (m−r)!/m! λ_m(E_r G))**: exact check with random polynomials G, m = 3, 4, every r = 0..m (values include 1, −5, 6, 3, 2). All agree.
- **Rank-5 detection**: λ_5(x_1² q (H_1−H_0)) = −2 for q = Σ x_i(x_{i+1}²x_{i+2}² + x_{i−1}²x_{i−2}²). Reproduced.
- **Rank-6 witness** (22 signed dihedral orbit sums, degree 9): reproduced with the reflection i ↦ r−1−i carrying sign (−1)^{r+1} and rotation sign (−1) per step: λ_6(x_0x_1^5 q) = −198; λ_7(h^4 x_0² x_1 T_6(q)) = −7646; all 21 degree-2 divided-difference packets vanish; all 6 zero-edge insertion packets vanish. (With the reflection i ↦ r−i instead, the values are −7406 and −9328 and the vanishing fails, so the convention matters.) −198 ≢ 0 mod 13.
- Not reproduced: the F_1009 span table (residual binary directions per rank/jet order) and the first-order normal packets of the witness.
- Boundary lemma (§8 of the report): if P, Q ∈ K[x]/(e_1) agree on every coordinate hyperplane then ∏x_i = e_m divides P−Q, so [P] = [Q] in R_m (m ≥ 3). Argued by hand; correct.

## Merged-edge algebra report (2026-11-28, second) — independent checks
Scripts: `artin.py` (exact coinvariant ring, Artin normal forms), `modrank.py`, `split_edge_checks.py`, `coverage_check.py`, `smith_check.py` (run with `PYTHONPATH=.`).
- Thm 5 presentation relations e_j(z) = (−1)^j H_j(u,v), H_m = 0 at roots of unity: m = 3..7, errors ≤ 5e-15 (H_{m+1} = ±1 there since e_{m+1} = ±1; it vanishes only in the coinvariant quotient).
- Thm 6 Ann(u) = (K_m) in K[u,v]/(H_m,H_{m+1}): equal graded dimensions in every degree through the top, m = 3..8, over F_1000003.
- Rank-5 counterexample: T_5(q) reduces to 0 in R_6; q ≡ w_0^4 w_1 ≠ 0 in R_5.
- Coverage table reproduced exactly: 1/1, 2/2, 9/9, 9/29, 47/87 for lower ranks 4..8 (χ_Q(rot) = χ_Q(rev) = (−1)^{m−1} computed).
- Smith data reproduced exactly: relative index 1, 2, 108 for ranks 4, 5, 6; rank-6 invariants [1,1,1,1,2,2,2,2,108] vs [1,1,1,1,1,2,2,2,2].
- Not reproduced: chord-factor (Grassmannian) annihilator statement, common-deformation identities, the F_1009 binary-direction table.
