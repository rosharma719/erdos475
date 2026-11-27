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

## Weyl-algebra / signed-walk report (2026-11-29)
Scripts: `walk_checks.py` (run with `PYTHONPATH=.`), `weyl_det_check.py`.
- Triangular-flow summation: 1841 margin pairs OK. Walk formula and DP recursion for κ: 493 pairs, 0 mismatches. Boundary vector from the walk DP reproduces c_m for m = 3..10 up to global sign.
- [D^a,U_i] b_h = T_{i,a}(h) b_{h+i−a} checked; modular height truncation holds for p = 11, 13, 17, 19.
- Counterexamples reproduced exactly: U = {2,7} → 19 − 19z²; U = {13,14,15,16} → [293541560, 41340, −9464, 41340, 293541560], gcd of first two = 13780 = 2²·5·13·53.
- Sign correction: with odd α, β the matrix H = YX − XY has tr(H) ≠ 0; H = XY + YX = −Σ α_iβ_a [D^a,U_i] has tr(H^k) = 0 (k = 1..4) and (H^k)_00 = ε(k) Σ κ(A,I) α_Iβ_A (verified for U = (2,3), (2,3,4)).
- Not reproduced: exact rank-17 c_{17,1}, c_{17,2}, contents at m = 15, 16, 17.

## Pairing-matrix / intra-rank propagation report (2026-11-29)
Scripts: `pairing_matrix_checks.py [M]`, `pairing_counterexamples.py`, `harmonic_and_cofactor.py` (all with `PYTHONPATH=.`).
- P_{m,d,j}: rank-lowering identity and generating-function descent verified m = 4..8; quadratic-packet contents reproduced m = 3..9.
- Counterexamples reproduced exactly: rank 5 matrix (rows 0; −7,0,7; −2,4,−2; 5,0,−5; 0) and rank 6 (zero first row, penultimate (0,−144,216,−216,144,0)).
- V_m(ℓ) harmonic and e_1(∂)V_m = 0 for m = 4,5,6 (all coefficients).
- Cofactor decomposition into diagonal / off-diagonal parts, m = 3..8.
- Not reproduced: two-copy Weyl normal-symbol identity, translated determinant identity, rank-8 restricted family counts, rank ≥ 15 contents.

## Witt-differential report (2026-11-29)
Scripts: `witt_checks.py`, `collision_checks.py`, `qcontent_check.py` (all with `PYTHONPATH=.`).
- Exponent-one insertion κ({1}∪A′,I) = Σ_J κ(A′,J)[e_I](e_1∧ − d)e_J: 138 cases, 0 mismatches. Self-adjointness κ(A,I)I! = κ(I,A)A!: 1927 pairs. Homotopy ι_1 d + d ι_1 = ν id verified. Merge recurrence: 154 sets, 0 mismatches. κ({1..m},{1..m}) = 0 for m = 2..7.
- F_{m,r}(1) = 0 and F′_{m,r}(1) = ±(−1)^r Σ_{j≤m−r} c_{m,j} verified for m = 3..7 (global sign (−1)^{m−1}).
- Content of [Q_m]: m = 4..7 → 1, 1, 2, 2 (rank 8 run in `qcontent_m8.txt`, if it finishes).
- Not reproduced: F_{m,r} example table, rank-9 content, merge-closure argument.

## Schur/Witt merge-vector report (2026-11-29)
Scripts: `schur_checks.py`, `merge_matrix_check.py`, `schur_tables.py` (log `schur_tables_out.txt`), `openpath_checks.py`. (`qcontent_check.py 8 8` gave content 2 for [Q_8].)
- E_{m,d,μ} = ±κ(I_μ,J_d): m = 3..6, no mismatch; packet gcds m = 5,6,7: d=1: 4, 28, 14; combined: 2, 4, 2; merge-image: 4, 2, 1.
- m = 6: b_6 = (−1,2,−1,−3,2,4); det A = 18208418112 = 2⁶·3³·43·191·1283; A b_6 = (10,52,74,102,92,88); dim W = P(m−1) − 1 for m = 4..12.
- Open-path polynomial L_k: integral, symmetric, degree k−2, reflection law (k = 3,4,5); collision recurrence exact for k = 3,4.
- Not reproduced: ranks ≥ 9 tables, block-form theorem, two-zero determination.

## Grassmannian two-root report (2026-11-29)
Scripts: `tworoot_checks.py`, `tworoot_tables.py` (log `tworoot_tables_out.txt`), `tworoot_swapped.py` (both κ conventions).
- Schur expansion of P_k(t;x) verified m = 3..6 (global sign +1). Packet size ⌊(m+1)²/4⌋ for m = 3..15. Projected merge relation exact m = 3..8; q_{7,1,r} = (966, 3430, 4650, 2186).
- Projected Witt gcd m = 3..11: 1,2,4,4,2,2,6,16,4. Full packet (κ(A,J_d) convention) m = 3..10: 1,1,4,4,2,12,6,4. κ(J_d,A) convention gives full gcd 1,1,4,4,2,2,6,16.
- Rank-7 centered polynomial 𝓛_7 reproduced exactly.
- Not reproduced: ranks 12–15 of the tables, the Grassmannian ideal-cancellation proof (read only).

## Two-marked-edge / extra-vertex report (2026-11-29)
Scripts: `rv_contents.py` (R_m, V_m and contents), `rv_big.py` (ranks 11–13; log `rv_big_out.txt`), `twomarked_checks.py`.
- ∂_xQ_{m+1} = (a+b)V_m verified numerically m = 4,5,6 (ratio 1 + O(1e-15)). Extra-vertex descent verified k = 2..4, ℓ = 1,2. Plücker obstruction numbers reproduced exactly.
- Contents: R_m, m = 4..12: 1,4,4,2,2,6,16,4,16; V_m: 1,4,28,6,2,12,16,8,8. Rank 13: projected gcd 8, last two coordinates gcd 152 = 8·19, vector mod 19 = (13,10,17,8,7,0,0).
- Not reproduced: two-slice descent / A_q,B_q formulas, ranks ≥ 14 contents, combined ζ_m table.

## Schur-slice flexibility report (2026-11-29)
Script: `flexibility_checks.py` (pure Python; `python3 -I flexibility_checks.py`).
- Extraction formulas E(S_X s_λ) = s_{(r,q−1−r)} (μ = (q−2,r,q−1−r)) and 2s_{(q−1)} + 2s_{(q−2,1)} (μ = (q−1,q−2,0)) verified q = 3..8; they span the binary Schur basis. Rank-6 worked example arithmetic and R_5 = −4(a+b)², R_6 = 28s_(3) + 32s_(2,1) reproduced.
- Not reproduced: mixed-moment identity for R_{q+2}, rank-17 specialisations mod 47.

## Height-barrier / midpoint report (2026-11-30)
Script: `midpoint_checks.py` (`PYTHONPATH=. python3 midpoint_checks.py`).
- Barrier: p = 5,7,11,13 all upward crossings ≡ 0. Reversed-step identity exact. Midpoint identity: exact over Q (32 cases, k = 1..r−1) and mod p with h<p (40 cases). Coefficient transform and R_7 = −966u⁴ + 1400u²v − 156v² reproduced; gcd(k_j) = content(R_m), m = 3..10.
- Not reproduced: counts of checks in the report, p-adic strengthening.

## Exterior rank descent / Weyl one-hole report (2026-11-30)
Scripts: `exterior_checks.py`, `weyl_eigen_checks.py`, `diag_onehole.py`.
- K_U = Σ(−1)^a E^a(e_0∧K_{U∖a}) exact (m = 4,5,6). T_2+T_3 surjective at 7 tested (m,p). Coupled image reproduces all 9 table rows with positive-exponent sources; codim 1 iff p = m+2.
- W(U,U) eigenvalue W_m(h) = Σ d C(h,d−1) K(J_d,J_d) exact (m = 3,4,5); W({1..m−1}) = 0; Alt F_d identity exact. gcd_d K(J_d,J_d), m = 3..11: 1,1,4,4,2,12,18,16,8.
- Not reproduced: Smith invariants m = 5,6; proofs of surjectivity/injectivity; (6)–(7); eq. (9).

## Witness-search experiment (2026-11-30)
Script: `witness_search.py` (log `witness_search_out.txt`; rank 12 may still be running / incomplete). For m = 3..11: gcd(K(J_1,J_1),K(J_2,J_2)) = full gcd of the diagonal one-hole packet = 1,1,4,4,2,12,18,16,8 (no prime > 3); K(J_1,J_1) alone has large primes at m = 7..11; smallest witness index over primes ≤ 2000 is 1 except (m,p) = (7,23) where it is 2.

## Sparse cyclic operator report (2026-11-30)
Scripts: `sparse_checks.py` (sparse inverse, centered polynomial), `duality_checks.py` (duality (2)), `sparse_theorem_check.py` / `sparse_theorem_check2.py` (Φ(θ) vs Weyl eigenvalue polynomial), `reciprocity_check.py` (componentwise reciprocity (6), rank-lowering (5)). Rank-12 diagonal gcd in `witness_search_out.txt`.
- Sparse inverse exact r = 2..7; duality (2) 36 cases; main equivalence ratio exactly 1 for (m,p) = (3,5),(3,7),(3,11),(4,7),(4,11),(4,13),(5,7); reciprocity (6) 37 cases, rank-lowering (5) 11 sets; W_m(−h−1) = ±W_m(h) for m = 3..11.
- Not reproduced: ranks 13–15 diagonal gcds, counts of checks in the report, proofs of the flow identities.

## Strategy-memo checks (2026-12-01)
Scripts: `memo_checks.py` (t-form identity, image theorem), `diagonal_flow_check.py`.
- G(−t) = Σ_d dκ_d t^{d−1}(1−t)^{p−d} verified (m,p) = (3,7),(4,11),(4,13),(5,7); binomial-sum identity for p = 5,7,11,13. Image of (g_2,g_3) ↦ (1−t²)g_2 + (1−t³)g_3 equals {H ∈ P_N^ε : H(1) = 0}, N = 4..14. Diagonal-flow lemma verified on 5 sets.
- Not checked: lost parity table, representation-theoretic and literature claims.

## Attempt to close the gap (2026-12-01)
Scripts: `wpoly_structure.py` (W_m(z) for m = 3..11, pairwise gcd/division), `shifted_intervals.py` (D(r,c) = κ(I_{r,c},I_{r,c}), finite differences).
- Result: no cross-rank factorisation among the W_m (only z from parity; W_5 = 4W_4 is a coincidence); D(r,c) is a polynomial in c of degree 1, 4, 10 for r = 2, 3, 4, with no product formula. Both negative.

## Deformed exterior algebra / hypersurface report (2026-12-01)
Scripts: `deformed_ext.py` (the algebra, relation (1), expansion (2), F_2..F_4), `hypersurface_checks.py` (gradient formula, recursion (9), c* gradients m ≤ 7), `leakage_check.py` (ℓ_m, g_{m−1}, 2×2 minors; log `leakage_m8.txt`), `gauge_counterexample.py`, `pattern_identities.py`, `cyclicity_check.py`.
- F_m top coefficient is a pure scalar; F_2, F_3, F_4 reproduced; recursion (9) exact; F_m(c*) = 0 (m ≤ 7); ∇F_m(c*) primitive content 1 (m ≤ 7).
- Leakage: ℓ_m ∥ g_{m−1} only at m = 3 (t₀ = 1/4) and m = 5 (t₀ = 0); minor gcds 1, 1, 7, 1 for m = 4, 6, 7, 8.
- Gauge counterexample (p = 7, A = {4,5}) reproduced exactly; identities (13), (15) verified.
- Not reproduced: rank-16 gcd 96; lost gradient table.

## Lowest-pair descent report (2026-12-01)
Scripts: `lowest_pair_checks.py` (PQ+QP = −C, S² = C²/4, Bernoulli extension, four-component recurrence reproducing Z^k for m = 3..6), `boundary_sandwich_checks.py` (identity (12), alternating κ sum, adjacent-gradient minors table).
- All algebraic identities verified; minors table 4,0,64,2240,192,3024,9216,2816 (m = 4..11) matches exactly; Σ(−1)^{d−1}κ_{m,d} = 0 for m = 3..11.
- Not reproduced: factorization proof, marked moments (13), recurrence at ranks 7–8.

## Single-transfer operator (§37)
`transfer_checks.py` (component reconstruction), `transfer_ops.py` (T on the exterior algebra; T(H_k)=H_{k+1}), `transfer_claims.py` (grading, terminal vanishing/surjectivity, pivot, P_n rank/Smith). Run `PYTHONPATH=. python3 transfer_claims.py 3 4 5`. n=6,7 were still running when filed.

## Insertion kernel / dual transfer (§38)
`dual_checks.py` (insertion form (1) vs T; dual coefficient identity; adjointness), `fit_kernel.py` (fit of T in the span of M E^a E^b; exposed the h <= n truncation error), `minor_table.py N` (maximal-minor gcd and 2x2 seed minors of P_n, kernel vector mod 17 at n=5).
