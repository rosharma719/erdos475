# Dense two-path conjecture at k ≈ M/2: first test (Claude, 2026-11-26)

## The question
The dense integer two-path conjecture (DIT) concerns zero-sum hole sets T with |T| = k and height M ≥ 2k. It claims there are two simple paths in [0, M] that use exactly I_M ∖ T.

Today DIT is applied only for k ≲ log₂ p. If it holds up to k ≈ M/2, and complement sets whose centred sum is a nonzero multiple of p can be closed, it would cover |A| ≳ 3p/4 at every prime.

## Results
1. **Exact search.** Exhaustive at k = M/2 for M = 8–11: all 29 + 38 + 186 + 258 sets have paths.
2. **Linear-programming test for counting obstructions** (`cutlp.py`).
   - **What it tests.** Each label is placed somewhere in [0, M], and every cut must be crossed equally often in each direction. If this LP is infeasible, no closed walk exists at all.
   - **Sanity check.** It correctly rejects both known counterexamples: the 31-hole cut example and the 11-hole weight example at M = 8.
   - **Random T: 0 obstructions.**
     - k = M/2 at M = 12, 20, 30, 40, with 300 samples each.
     - k = 0.6M, 0.8M and 0.9M at M = 20, 30, 40, with 200 samples each.
   - **Adversarial T built from runs: 0 obstructions.** Each T is up to three runs of consecutive holes plus up to two singletons (the shape of the known counterexample).
     - k ≤ M/2 at M = 16, 24, 32: 1,046, 1,148 and 878 sets.
     - k ≤ 0.75M at M = 24: 1,500 sets.
3. **Actual path search for M ≥ 14.**
   - The hand-written DFS (`cw.c`) is too weak: it is inconclusive at M ≥ 14, and with random label orders even at M = 12.
   - An exact SAT encoding (`twopath_sat.py`, CaDiCaL) is written. Its runs were still in progress at the time of writing.

## Reading
- No counting obstruction appears anywhere near the boundary k = M/2. The only known obstructions need k > M/2.
- Simplicity of the two paths at large M is untested so far. The SAT encoding is the tool for that.
- If SAT confirms paths at k = M/2 for M up to about 30, DIT at k ≤ M/2 becomes the main proof target.
