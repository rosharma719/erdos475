# Audit: two-frontier greedy proof of the protected two-path theorem (Claude, 2026-11-24)
The submission was pasted in chat. Its script and the rerun output are in `experiments/audits/protected_greedy/`.

## Verdict: ACCEPTED as a candidate theorem
The core argument was checked by hand:
- **Frontier invariant.** Advance the lower frontier, with ties going to the shorter path. Every non-frontier vertex then stays ≤ the lower frontier, so a new vertex only has to avoid the other frontier, h, and (for the longer path) u.
- **At most two forbidden destinations.** Every longer-path step is < Q = u − h. So if y < h, then y + e < u. If y ≥ h, then h cannot be hit.
- **Two-step traps** (checked):
  - The shorter path can get stuck only if Q is unused, since y − x = Q.
  - The longer path can get stuck only if d = P − Q is unused (case y ≥ h). The other case would need x − y = P, which is impossible because max E < Q < P.
- **Final steps are safe.** The endpoints are u < v, and the longer path avoids u.

The initialization case split (consuming Q and d early, and the exceptional case d = h ∈ E) is intricate. It is checked exhaustively by the script, and its hand proof was read but not re-derived line by line.

**Rerun, exact match:**
- protected paths, exhaustive for P ≤ 12: 28,743 instances (754 of them with d = h ∈ E);
- random: 18,421;
- h > Q extension: 7,560;
- equal-extreme theorem: 19,079;
- 0 failures in all four;
- insertion obstruction reproduced: 21 collisions, 8 at span 10, 1 at span 9.

**Consequence (candidate).** BS holds whenever P ≠ Q and T ≤ P + Q + min(P, Q). Together with `protected_paths_audit.md`'s run-count lemma, this is the full reach of any one-bridge, two-climb construction. The equal-extreme partial theorem (h ≠ M, d ∉ Y ∖ {M, b}, T ≤ 2M + b) is also accepted as a candidate.

## What generalises: the k-frontier invariant (proved, Claude)
Take k increasing segments. Segment i has base b_i, a set S_i of distinct steps, and top t_i = b_i + ΣS_i. Let F be a set of forbidden heights. Assume all bases and tops are pairwise distinct and outside F.

**Greedy rule.** Repeatedly advance the active segment with the lowest frontier f_i, using an unused step s ∈ S_i whose destination f_i + s avoids:
- the other current frontiers;
- the other segments' tops;
- F.

**Invariant.** Every placed vertex that is not a current frontier is ≤ the lowest frontier. This is the same argument as for k = 2: the lowest frontier only moves up, and every other frontier is above it.

**Consequence.** Any completed run of the greedy produces pairwise distinct vertices avoiding F. At each move at most 2(k − 1) + |F ∩ (f_i, t_i)| destinations are forbidden. So greedy can fail only in a segment's last ≤ 2(k − 1) + |F| steps, in a "tail trap".

**Why k ≥ 3 needs more than this.** The 3-path counterexamples (`bs_handoff_audit.md`, and the endpoints 2/4/6 example) are exactly tail traps on segments with only 1–2 steps. In the dense regime, segments have O(1) steps (rise ≤ span ≈ 2M while steps average about M/2). So every step lies in the tail regime, and per-move counting alone cannot work. A multi-bridge theorem must therefore get its tail-trap analysis from the arithmetic, as the two-path proof does with Q and d, and not from counting.

## Updated gap
- **Sparse and moderate regime** (P ≠ Q, T ≤ P + Q + min(P, Q)): BS is now a candidate theorem.
- **Dense regime** (T ≫ P + Q): open. It needs about T/(P + Q) bridges, and with them a tail-trap theory for segments with O(1) steps, or a spiral construction as in `rooted_symmetric.md`.
