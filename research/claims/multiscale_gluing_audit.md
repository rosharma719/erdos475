# Audit: multiscale gluing, the no-cut dense family, and insertion exceptions (Claude, 2026-11-24)
The submission was pasted in chat. No verifier was attached; the dense family was rebuilt and checked inline.

## Accepted (hand-checked)
- **Thm 1, interval gluing: ACCEPTED.**
  - The replacement u → u + B₁ → (+a) → v + B₂ → v puts B's vertices in [u, u + w] ∪ [v, v + w].
  - These intervals are disjoint and otherwise empty by hypothesis.
  - Works for any zero-sum B, with any sign counts.
- **Thm 2, lattice gluing: ACCEPTED.**
  - A ⊆ gℤ and B has a cycle of span w < g. Vertices of A's cycle differ by ≥ g > w, so both intervals are free.
  - An edge away from the maximum keeps the span. D is unchanged because |b| < g ≤ |a|.
- **Thms 3A and 3B (compatibility preserved under lattice gluing): ACCEPTED as candidates.** The edge-counting argument was read.
- **Thm 4 (compact-band absorption for w < K − t), the lower-expansion repair lemma, and Thm 5 (no insertion exceptions when 2t + H < 2K): ACCEPTED as candidates.**
  - These inherit the compact-band sparsity: n < 4√D (`band_compatibility_audit.md`).

## Verified computationally
- **Dense no-cut family A_m** (sign pattern (+, −, −, +) per block of 4, with the signs of 1, 2, 4m−1 and 4m flipped): checked for **m = 3..200**.
  - The only zero cumulative magnitude cut is at r = 4m.
  - W = P ⊕ (−Q′^rev) is simple, with span 8m − 2 < D = 8m − 1.
  - Contracting the final two steps gives a bounded smaller cycle.
  - Inserting ±(4m + 1) around the step −4m is simple, with span ≤ 2M.
- n/D → 1/2, and the result disproves "every dense set decomposes into zero-sum magnitude bands." **ACCEPTED.**

## Scope
- **Gluing needs scale separation.** It requires a lattice (A ⊆ gℤ with w < g) or a compact band (w < K − t). Generic dense sets in F_p have neither.
- **The dense families are explicit and structured.** Both are interleaved alternating paths and symmetric cores, the same mechanism as the symmetric walk. They are genuine dense constructions, but not a general argument.
- **The submission's own GAP A, "imbalance-carrying multiscale decomposition," is the open dense case.** GAP B (a compatible insertion edge always exists) is supported by 301/301 repaired residuals but not proved. Both are open.
