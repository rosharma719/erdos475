# Integer two-path lemma for k holes, IT(k) (Claude, 2026-11-26)

## Statement
Let T be a zero-sum set of k nonzero integers and M = max_{t ∈ T} |t|. Put S = {±1, …, ±M} ∖ T.

**IT(k)** asserts that there are simple paths P and Q with these properties:
- both lie in [0, M];
- both start at 0 and end at the same vertex E > 0;
- steps(P) ⊔ (−steps(Q)) = S exactly, i.e. Q read backwards uses labels −q.

## Where it comes from
Astra's reduction, from a round whose files are not yet pushed, proves:

IT(5) + an integer-dilation counting step ⇒ C5 (complement-5) at every prime p ≥ 61.

Astra checked IT(5) for all 2,154 integer 5-sets through M = 14.

## Data (Claude, `experiments/exploration/complement5/integer_two_path.c`, exhaustive, 0 failures)
T ranges over all zero-sum k-sets with max |t| = M. Sets containing ± pairs are included.

| k | M range | sets | failures |
|---|---|---|---|
| 2 | 2–13 | 12 | 0 |
| 3 | 3–13 | 72 | 0 |
| 4 | 4–10 | 164 | 0 |
| 5 | 5–12 | 1,088 | 0 |
| 6 | 6–10 | 1,138 | 0 |
| 7 | 7–10 | 2,174 | 0 |

## Why IT(k) for all k matters
- **From IT(k) to complement-k.** Suppose the dilation-and-closure step generalises from k = 5 to arbitrary k, needing kM < p so that the integer sum is 0. Choose λ by Minkowski / Dirichlet with max |λh| ≲ p^{1−1/k}. Then IT(k) gives Graham for F_p^× ∖ H whenever |H| = k ≲ log p / log log p.
- **What that buys.** This is the dense-end mirror of Kravitz's sparse theorem: an explicit dense-regime result at every prime. It also gives C5 at all primes, combined with Astra's p ≤ 113 census.
- **What it does not buy.** The range log p / log log p ≲ |H| ≲ εp, and the middle densities, remain without any explicit mechanism.

## Status
The universal assertion is false. A 31-hole example with M = 31 rules out even a closed walk, and the k = 2 base case needs M ≥ 2. The reported finite censuses stand. A revised conjecture with M ≥ 2k still suffices for the prime application. [Counterexamples, verifier, and corrected reduction](integer_two_path_cut.md)
