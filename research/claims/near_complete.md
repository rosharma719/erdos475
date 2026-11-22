# Near-complete: HOS base + contract NC3

Published baseline: p-3 <= |A| (c<=2). Target NC3C: |A|=p-4.

### Round: near-complete theorem programme (Nov 22, 4 pm)

**Refutation search update:** all near-complete orbits solved, no counterexample.

- p = 41: |C| = 3: 247; |C| = 4: 2,290; |C| = 5: **16,451**.
- p = 43, |C| = 3: 274.
- |C| = 3 for p = 59, 61, 67, 71, 73: 532, 571, 694, 782, 829.

**Base construction (Hicks–Ollis–Schmitt, arXiv:1809.02684).** A graceful permutation α of \[1..r\] (p = 2r + 1) gives the directed rotational terrace (α₁..α\_r, α\_r + r, …, α₁ + r). Its rotational sequencing of ℤ\_p^\* is b = (δ₁, …, δ\_{r−1}, r, −δ\_{r−1}, …, −δ₁, −r), where δ\_i = α\_{i+1} − α\_i are signed and |δ\_i| runs over {1..r − 1}.

- HOS prove |A| ≥ p − 3: omitted elements are made adjacent, then truncated.
- They remark that for p − 4 a complete solution "seems unlikely" with this method alone.

**New ingredient:** the contraction lemma.

- *Non-zero-sum* C: truncate a c-window equal to C·ν.
- *Zero-sum* C: a c-window can never sum to 0 (terrace points are distinct). Instead contract a (c + 1)-window W with ΣW ∈ W and C·ν = W∖{ΣW}. For c = 3, C occupies positions {i, i+1, i+3} or {i, i+2, i+3} of a 4-window.
- *± pairs* (C ∋ x, −x): use the special window (δ\_{r−1}, r, −δ\_{r−1}). This needs only a prescribed last difference, which is HOS Lemma 4.5 (exceptions (d, r) ∈ {(2, 4), (2, 5), (2, 8)}).
- p ≤ 37 is already fully verified, so only r ≥ 20 is needed.

**Coverage data** (`int/gc.c`, random graceful permutations):

- c = 3, p = 23: 67 / 67 non-zero-sum, 3 / 3 zero-sum (exhaustive enumeration of graceful permutations).
- c = 3, p = 29: 113 / 113 and 4 / 4 (exhaustive). Random sampling gives 112 / 113.
- c = 3, p = 31: 129 / 131 and 5 / 5 (sampling).
- The *only* classes random sampling misses are ±-pair classes, {1, 3, −3} and {1, 5, −5}, which the special window covers via Lemma 4.5.
- c = 4, 5 runs are in progress.

**Gap.** For generic C, a proof needs an explicit lemma: for every generic 3-set C there are a dilation ν and a graceful permutation of \[1..r\] (r ≥ 20) containing C·ν as three consecutive signed differences. Zero-sum C needs the analogous 4-window statement.

### Contract NC3: Graham for |A| = p − 4 (|C| = 3), all p (Nov 22, 4:15 pm)

Indexing note: |ℤ\_p^\*| = p − 1, so |A| = p − 4 means a **3-element** complement. HOS cover |C| ≤ 2.

- **Scope.** p ≤ 37 is fully verified, so only r = (p − 1)/2 ≥ 20 is needed.
- **Tools.** HOS rotational sequencing b = (δ₁..δ\_{r−1}, r, −δ\_{r−1}..−δ₁, −r) from a graceful α, plus dilation, truncation (non-zero-sum C), contraction (zero-sum C), and HOS Lemma 4.5 (one prescribed end difference).

**Zero-sum C = {x, y, −x − y}: reduction to coupled end patterns (proved).** Dilate so xν = ±r and contract a 4-window at a special position. The windows are (δ\_{r−2}, δ\_{r−1}, r, −δ\_{r−1}) with positions {1, 3, 4}, or (−δ₁, −r, δ₁, δ₂) with positions {1, 2, 4}. The zero-sum condition holds automatically mod p and forces δ₂ − δ₁ ∈ {r, −r − 1}. Up to reversal and complement, the needed first-two patterns form four one-parameter families:

- F1(a) = (a − r, a)
- F2(a) = (a, a − r)
- F3(b) = (b, b − r − 1)
- F4(b) = (r + 1 − b, −b)

The parameter is ≈ |y/(2x)| mod p for the chosen special element x, since r ≡ −1/2.

**Band data** (`int/lemZ*.c`, targeted search, r = 16–26):

- F1 embeds for a/r ≈ 0.4–0.8.
- F2 for ≈ 0.15–0.5.
- F3 for ≈ 0.15–0.5.
- F4 for ≈ 0.45–0.85.
- The union covers ≈ \[0.15r, 0.85r\]. Small and large parameters fail in all four families (the failures may be partly search artefacts at r ≥ 25).

**Selection (sketch, to be proved).** A choice x is bad only if y/x is a small residue, which puts the parameter near 0 or near r. All three choices are bad only for explicit tiny configurations, because y/x = t small makes x/y = 1/t typically not small.

**Open sub-contracts.**

- NC3-Z1…Z4: explicit graceful-permutation families realizing F1–F4 throughout their bands, for all r ≥ 20.
- NC3-S: the selection lemma with its exceptions.
- NC3-N: non-zero-sum generic C, which needs *two* prescribed end differences (a two-parameter pattern). Only about half of feasible patterns embed at r = 12 (150 / 320), so this needs its own selection-plus-band analysis. The ± pair cases are done by HOS Lemma 4.5.
- **Status:** Candidate (reduction proved; constructions and selection open).

* The literal fixed-position version is false: forced-prefix placement fails for 91 / 228 two-step patterns at r = 14.
* The dilation and position freedom is essential. A proof will need explicit Walecki/twizzler-type families with local modifications, as in HOS Lemma 4.5.
