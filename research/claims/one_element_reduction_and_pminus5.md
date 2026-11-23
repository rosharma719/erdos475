# One-element zero-sum reduction; |A|=p−4 for all A; zero-sum 4-complements and |A|=p−5 (GPT 2026-11-22; AUDITED IN-SESSION by Claude; referee gates pending)

## Lemma 1 (one-element balancing)
p odd prime, A ⊆ F_p^×, 2 ≤ k=|A| ≤ p−3, s=ΣA ≠ 0. Then some x∈A has y=x−s ∈ F_p^×∖A, so A'=(A∖{x})∪{y} is a zero-sum k-set.
Proof: otherwise x−s∈A for every x∈A∖{s}. If s∉A, A is closed under −s, so A=F_p (contradiction). If s∈A, each element ns of A forces s,2s,..,ns∈A, so A={s,2s,..,ks}; ΣA=s forces k(k+1)/2≡1, i.e. (k−1)(k+2)≡0, so k∈{1,p−2}: excluded. ∎

## Theorem 2 (reduction to zero-sum, same cardinality)
If every zero-sum k-subset of F_p^× has a valid ordering, so does every k-subset, 2≤k≤p−3 (k=1 trivial; k=p−2, p−1 via a geometric full cycle). Proof: rotate a valid cycle of A' to start with y, replace y by x; all partial sums shift by x−y. ∎

## Corollary: every |A|=p−4 has a valid ordering, given NC3_ZEROSUM (complement of a zero-sum set of size p−4 is a zero-sum triple; inverse-pair/generic cases disappear).

## Theorem 3 (zero-sum 4-complements, p ≥ 11): Walecki 2+2+3 simultaneous contraction
Pair-position lemma (pairs with sum ±1 occur consecutively in B except explicit exceptions R_2, R_3); four-element selection lemma (some partition C=X⊔Y with ΣX=−ΣY≠0, no pair of type R_2, not both of type R_3); contract P_+→1, P_−→−1, Q→r simultaneously ⇒ valid cycle of F_p^×∖s^{-1}C; undo dilation. Corollary: every |A|=p−5 has a valid ordering (via Theorem 2).

## Claude audit (no API; experiments/audits/reduction_and_pminus5.py)
- Lemma 1 re-derived by hand; EXHAUSTIVE check for p ≤ 23 (≈4.3M nonzero-sum sets with 2≤k≤p−3): a balancing replacement always exists, 0 exceptions.
- Theorem 2 transfer verified end-to-end at p=7,11,13 (every nonzero-sum set: ordering built from a zero-sum cycle, 0 invalid).
- Theorem 3: independent implementation (own search over partitions/dilations/block positions; not GPT's script): ALL zero-sum 4-complements for 11 ≤ p ≤ 47 constructed and verified, 0 failures; the selection-lemma conditions were satisfiable for every one. The selection lemma's hand proof was checked for its number-theoretic inputs (orders of −2 and −3 mod p are ≥5 for p ≥ 11) but not verified line by line; computational support extends only to p ≤ 47.
- p=19 obstruction (C={7,8,10,14,18}): re-run, confirmed: 222 distinct-label 13-vertex contractions of the fixed Walecki cycle, none equals A under any dilation; an explicit valid cycle of A exists. Kept as regression: experiments/regression/walecki_obstruction_p19.py.
## Caveat from the source
Non-zero-sum orderings satisfy Graham's condition (distinct nonempty partial sums); they need not satisfy Alspach's stronger condition with the empty sum distinct.
