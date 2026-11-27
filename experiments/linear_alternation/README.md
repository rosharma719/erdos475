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

## Reflection convention and simultaneous interpolation (2026-11-28, third)
Scripts: `reflection_convention_check.py` (+ `witness_data.py`), `simultaneous_checks.py` (+ `split_edge_checks_lib.py`), `saturation_check.py`.
- **Convention (computed, m = 4..8):** Q_m has character (−1)^{r(m−1)} on rotation i→i+r and (−1)^{c(m−1)} on reflection i→c−i. The rank-6 witness built with i→r−1−i (signs (−1)^{r+1}) is equivariant for all 12 elements; the i→r−i variant is not equivariant (fails all 6 reflections).
- Ann(v) = (H_{m−1}), Ann(H_{m−1}) = (v): OK for m = 3..8. Deformation layers m, m−1, …, 1 and v^m A = 0: OK for m = 3..8.
- Trace interpolation rank r·m!/2: OK for m = 3, 4, 5, all r.
- Rank-4 degree-sensitivity counterexample (sign character): nf(q) = 40·z_1z_2²z_3³, T_4(q) = 0 in R_5. With χ_Q instead, q = 0 in R_4.
- Simultaneous saturation ker T ⊆ ker L on χ_Q-equivariant degree-D_m polynomials: holds at ranks 4, 5, 6 (ranks of T: 1, 6, 54; joint rank equal).
- Not reproduced: the report's rank-7 numbers (452, 20/19/0 comparison) unless `saturation_rank7.txt` says otherwise; the realisation theorem; the proof of Thm 10.
- `saturation_rank7.txt`: log of the rank-7 saturation run (`python3 saturation_check.py 7 7`, 2400 s limit). Committed while in progress; it contains a rank-7 result line only if the run finished.

## Marked-root algebra report (2026-11-28, fourth)
Scripts: `marked_root_checks.py` (graded linear algebra for C_m, mod F_1000003), `marked_root_m4.py`, `phi_rank_check.py`.
- m = 3: dim C = 36, socle degree 7, η-identities, Ann(a_d) = (η_d), Ann(η_d) = (a_d), (e_2..e_m)C = vC, dim C/(v) = 18, rank Φ = 27, dim v·imΦ = 12 — all as in the report.
- m = 4: dim C = 240, socle degree 12, η-identities verified; annihilator and vC checks in `marked_root_m4_out.txt` (in progress at commit time).
- u^k H_{m−1} = v^k H_{m−1−k} in A_m for m = 3..8.
- Not reproduced: the extra-direction table (ranks 5–9), the diagonalisation theorem, weighted-kernel statements, rank-7 saturation (run was terminated).

## Weighted noncancellation report (2026-11-28, fifth)
Scripts: `trace_poly_checks.py`, `model_weight_check.py`.
- v·g = u^{m+1} − H_{m+1}: verified symbolically for m = 2..12.
- m = 7: g_7 = 7u⁶ − 15u⁴v + 10u²v² − v³; multiplication by g_7 on degree 3 → 9 has matrix [[165,−198],[48,−54]], det 594 = 2·3³·11, Smith diag(3, 198): reproduced exactly (rank loss mod 11).
- Monomial-weight saturation (T^model = (h+x)h^{m−2}q): holds in every degree < N_m for m = 3, 4, 5 over all polynomial representatives (no symmetry).
- Not reproduced: marked-root saturation table (needs a C_m normal form beyond m = 4), rank-7 ranks 562/612, v-multiplied transfer losses, the zero-sum reduction paragraph.

## Coefficient-extraction obstruction report (2026-11-28, sixth)
Scripts: `obstruction_checks.py`, `sat_lib.py`, `degree_table_check.py`, `content_lib.py`, `boundary_content.py`. Logs: `degree_table_rank6.txt`, `boundary_content_m10.txt`.
- Rank-5 degree-8 witness: reproduced exactly (nf(q) = −980·(six Artin monomials), T_5(q) = 0 in R_6).
- Saturation by degree: rank 5 → missing 0,0,0,1,0,1 (degrees 5..10); rank 6 → 0,0,0,2,2,0 (degrees 9..14).
- g_m Catalan pairing m = 3..9; rank formula min(a,b,max(0,a+b−1−m+(p−1)/2)) on 819 cases, no mismatch.
- Cofactor identities: exact, m = 3..7 (sign-explicit form).
- Boundary-packet content gcd_g λ(Q_m A_0 g): m = 4, 6, 8, 10 → 1, 2, 6, 1.
- Not reproduced: the rank-8 saturation failure and its witness (bundle not available), Q_8 ∉ 𝒜_8, Schubert-class coefficient, kernel-uniqueness proof.

## Boundary-content report (2026-11-28, seventh) — identification with LAC
- `boundary_identity_check.py`: for m = 4..9, c'_{m,j} = λ_m(w_j·Q_m∏y_j) equals c_{m,j} = λ_m(w_j F_m) (even m) or its negative (odd m); contents 1,2,4,6,12,6; sum 0; reversal law holds. So the "boundary-content conjecture" is LAC; its table is the g_m table.
- c_{7,1} = −966 = −2·3·7·23 confirmed.
- Not checked: the symmetric-remainder recursion and the partial-flag pairing formula.

## Pascal-recurrence report (2026-11-28, eighth)
Scripts: `pascal_checks.py`, `artin_boundary_check.py`.
- b_{m,i} = −Σ_{j<i} c_{m,j}: consistent m = 3..14; direct integral Artin reduction of B_m (m = 4..7) gives coefficients ±b_{m,i}, support exactly on the M_i.
- Pascal recurrence for κ(A,I) matches the direct definition on 254 pairs (k = 1..3); complementary contraction reproduces c_m for m = 3..8 up to global sign; c_1, c_2 formulas hold in magnitude; Jacobi complementary-minor identity exact on 7×7 Pascal.
- gcd(c_1,c_2), m = 3..14: 1,1,2,4,6,12,12,2,8,24,4,8; full content 1,1,2,4,6,12,6,1,4,8,4,8.

## Unique-matching expansion report (2026-11-29)
Script: `matching_expansion_check.py` (imports `pascal_checks.py`; prints their checks on import).
- κ(A,I) = Σ over unique-perfect-matching tables of sgn·ℓ(D)·W: 493 pairs, 0 mismatches.
- Component expansion of Ĉ_m(z) = Σ C(n,r) c_{m,r+1} z^r: exact for m = 3..6 up to global sign; tables 2, 14, 378, 39802.
- Identity-matching table is diag(2..m) only (m = 3,4,5); its contribution is n!·∏((−1)^i − z), cancelled at m = 3 by the other table (2(z²−1) − 3(z²−1) = 1 − z²).
- Not reproduced: rank-17 modular result; the syzygy-degenerate-family statement.
