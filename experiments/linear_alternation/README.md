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
