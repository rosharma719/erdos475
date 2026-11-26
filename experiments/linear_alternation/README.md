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
