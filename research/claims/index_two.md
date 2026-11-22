# Index-two theorem (ledger, proved by Claude 2026-11-22; UNAUDITED)

### Theorem (index two) — proved by Claude, 2026-11-22

**Statement.** Let A ⊆ ℤ\_p^\* be zero-sum, and suppose some dilation λA has least positive residues summing to exactly 2p. Then A has a simple cycle (all proper partial sums distinct and nonzero), with any prescribed element first. Hence Graham's conjecture holds for A and for every set whose zero-sum reduction lands in this class.

**Proof.**

1. *Setup.* After dilation, the elements are integers p > a₁ > a₂ > ⋯ > a\_k > 0 with Σaᵢ = 2p. Let m be maximal with D\_m := a₁ + ⋯ + a\_m < p, and put D₀ = 0. Then k − m ≥ 2, since the remainder sums to more than p and each element is below p.
2. *Where collisions can occur.* Start with a₁, …, a\_m; the partial sums D₀ < ⋯ < D\_m are distinct residues. All later partial sums lie in \[p, 2p), so a later sum t collides with an earlier vertex only if t − p is a partial sum below p. Consequently the forbidden landing points form the set F = {p + (partial sums below p)}.
3. *Crossing step, case 1: D\_m + a\_{m+1} > p.* Append a\_{m+1}. This sum is fresh: it can equal p + D\_i only if a\_{m+1} > D\_i ≥ a₁ (for i ≥ 1) or the sum is exactly p (for i = 0), and both are excluded.
4. *Crossing step, case 2: D\_m + a\_{m+1} = p.* Append a\_{m+2} (still below p), then a\_{m+1}. That reaches p + a\_{m+2}, which is fresh because a\_{m+2} is smaller than every D\_i with i ≥ 1 and is nonzero. Here k ≥ m + 3.
5. *Dodging.* In both cases, consecutive points of F are separated by gaps that are all larger than every remaining element: the gaps are a₁, …, a\_m in case 1, plus a\_{m+2} in case 2. So any window (s, s + max Rem\] contains at most one point of F, and at each step at most one remaining element is blocked. While two or more elements remain, append any unblocked one. The last element lands on 2p ≡ 0, which closes the cycle and is not in F. ∎

**Exhaustive check.** The proof's algorithm (largest available element) succeeds for every zero-sum set and every index-2 dilation for p ≤ 13, with 0 failures.

**Index ≥ 3.** The same algorithm fails: in trip r up to r − 1 forbidden points can share a window, and it gets stuck with two elements left, both blocked. A two-ended variant (large elements placed from both ends) reduces but does not eliminate the failures; at p = 17, index 3, the alternating version fails 432 of 14,832 dilations. The full set ℤ\_p^\* (index (p−1)/2) always defeats both.

**Index 3: status (Claude, 2026-11-22).**

- *Empirical.* Greedy plus an exhaustive end-game on the last 4 elements never fails: exhaustive over all index-3 dilations for p = 17, 19, and on 60,000 random index-3 instances (p < 400, k ≤ 14). With the last 3 only, it fails once.
- *Proved pieces.*
  1. Trip 1 runs in pure descending order.
  2. In trip 2 at most one element is blocked per step, and the greedy order is descending up to disjoint adjacent swaps. A blocked element b cannot be blocked again at the next step: the two landing points differ by c < b, which is smaller than every trip-1 gap.
  3. Hence in trip 3 each window meets at most 1 trip-1 lift, and at most 2 trip-2 lifts (2 only while a carried-over element remains).
- *Open.*
  - The last 1–3 steps of the middle phase can be blocked.
  - The grasshopper end-game needs at most E − 1 forbidden points in the final arc, which holds when the elements have separated scales but not when they are nearly equal.
  - Not yet a theorem.
