# Complement-5 (|A| = p − 6) via contractions of graceful cycles (Claude, 2026-11-25)

## Setup
- **Target.** A = F_p^× ∖ H with |H| = 5 and ΣH = 0. Graham for |A| = p − 6 reduces to this case by the one-element reduction.
- **Two classes of H.**
  - (i) H is inverse-free. Then A has 5 unpaired labels.
  - (ii) H = {±h} ∪ T, where T is a zero-sum triple. Then A has 3 unpaired labels.
- **The cycles.** Let r = (p − 1)/2 and let α be a *graceful permutation* of [1..r], i.e. the values |α_{i+1} − α_i| are exactly 1, …, r − 1. Set δ_i = α_{i+1} − α_i. Then

  B_α = (δ_1, …, δ_{r−1}, r, −δ_{r−1}, …, −δ_1, −r)

  is a valid cycle of F_p^×. Its vertices are α_1..α_r followed by α_r + r..α_1 + r, which is the interval [1, 2r]. The Walecki cycle used for p − 4 and p − 5 is the zigzag α = (1, r, 2, r − 1, …).
- **Contractions.** Contracting blocks of a valid cycle keeps it valid, because it only deletes vertices. Deleting 5 vertices from B_α gives a cycle on 2r − 5 = p − 6 labels. If the labels are distinct, the result is a valid cycle of F_p^× ∖ H′ for some zero-sum 5-set H′.

## Coverage
Code: `experiments/exploration/complement5/gcov.c` (and `gpat*.c` for patterns). It enumerates all 5-vertex deletions of randomly sampled graceful B_α and counts the dilation orbits of H that are hit.

| p | graceful cycles sampled | orbits covered | inverse-free orbits covered |
|---|---|---|---|
| 19 | 20 | 25/25 | 11/11 |
| 23 | 300 | 52/52 | 28/28 |
| 29 | 400 | 121/121 | 77/77 |
| 31 | 400 | 154/154 | 102/102 |

By contrast, the single Walecki cycle covers only 220 of 634 orbits at p = 47 (`c5_coset_escape_audit.md`). Allowing every graceful α removes that obstruction at every prime tested.

## Block patterns
Deleting 5 vertices splits the deleted steps into contiguous blocks, and the block sizes satisfy Σ(size − 1) = 5. Each pattern is tested on its own:
- At p = 23 and p = 31, **each** of 5+2, 4+3, 4+2+2, 3+3+2, 3+2+2+2 and 2+2+2+2+2 alone covers every orbit.
- The single 6-block misses a few:
  - p = 23: 2 orbits;
  - p = 29 (3,000 cycles): 1 orbit, the paired set {1, 3, 11, 17, 26};
  - p = 31 (400 cycles): 13 orbits, 2 of them inverse-free.

**Interpretation of the single 6-block.** It covers H exactly when some B_α contains H ∪ {s} as 6 consecutive labels, for some s. The block sum is then s automatically, because ΣH = 0. For inverse-free H this is a purely local condition on α: a 7-point stretch of α whose consecutive differences are exactly H ∪ {s}.

## What a proof needs
A **graceful-segment lemma**, stated for every r ≥ r₀: every set W of 6 nonzero integers with distinct magnitudes in [1, r − 1] can occur as the consecutive differences of some stretch of a graceful permutation of [1..r].
- **Local part (W fits in an interval).** A stretch with step set W, in some order, has to fit inside [1, r]. Its width is at most the sum of the |w|.
- **Completion part.** Complete the stretch to a full graceful permutation using the remaining differences.
- **Extra choices.** s is free, and the window can also sit in the second half or straddle the centre (r, ±δ_{r−1}). Class (ii) sets need the straddling windows.
- Multi-block patterns (e.g. five 2-blocks) relax the lemma to *five separated* pairs of consecutive differences, which is presumably far easier to complete.

**Status.** The architecture is validated computationally at p ≤ 31. A parametric proof (the completion lemma) is not yet done.

## Update: the single 6-block with more samples, and graceful completion
- **The single 6-block with 3,000 cycles.** It covers every orbit at p = 31 (154/154) and every inverse-free orbit at p = 29. The only orbit it misses is the paired set {1, 3, 11, 17, 26} at p = 29. So for inverse-free H, the simplest gadget (H ∪ {s} as 6 consecutive differences of a graceful α) works at every prime tested.
- **Completion from an arbitrary prescribed prefix usually fails** (`gcomp.c`).
  - Setup: W is 6 random signed differences with magnitudes up to r − 1. Every order of W and every start point is tried, followed by a depth-first completion (20k nodes).
  - Results: completed 1/40 at r = 12, 2/40 at 15, 3/40 at 20, 3/40 at 25, and 4/40 at 30.
  - Cause: large differences are rigid in a graceful permutation. r − 1 must join 1 and r; r − 2 must join (1, r − 1) or (2, r); and so on.
- **Dilation removes the large differences.**
  - The lemma only needs W = λH ∪ {s} for *some* unit λ. By Minkowski / Dirichlet simultaneous approximation, some λ makes every |λh| ≤ C·p^{4/5} = o(r).
  - With magnitudes ≤ r/3, prefix completion already succeeds in 21/30 trials at r = 30 under the same small node budget (`gcomp2.c`). Runs at r = 40 and 60 timed out at 15 minutes each without finishing: the brute-force search over all orders × starts × completions is too slow there, so they give no data.
- **Revised lemma (the target).** For r ≥ r₀, every 6-set W of signed differences with distinct magnitudes ≤ εr occurs as consecutive differences in some graceful permutation of [1..r], with free choice of order, start point and position.
- **Natural construction to try.** Run the zigzag through the large differences first; it uses them rigidly at the ends. Then place W in the central interval among the small differences. This needs a local graceful completion on the central interval.

## Note added after Astra's round (2026-11-26)
- **Astra's "counterexample" to the graceful-segment lemma.** It is W = {1, 3, 7, −2, −4, −5}, which sums to 0. It is valid against the lemma *as stated above*: six consecutive differences of a simple walk cannot sum to 0.
- **The C5 gadget never needs such a W.** There W = λH ∪ {s} sums to s ≠ 0. The lemma should have required ΣW ≠ 0. That restriction is necessary, and it was omitted by mistake.
- **Astra's other results are not yet in this repo.** They were written on the user's machine:
  - `research/claims/c5_interval_lift.md`: C5 for every prime p ≤ 113;
  - `research/claims/c5_two_blocks.md`: a revised two-block lemma;
  - `experiments/exploration/complement5/verify_interval_lift.py`;
  - a two-path interval reduction, verified for every integer 5-set through M = 14.

  They are unaudited until pushed.
