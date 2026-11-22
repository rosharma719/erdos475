# Contraction lemma (ledger, proved; UNAUDITED)

**Contraction lemma (proved; dual of the lift, no escalation).** Let C be a valid cycle of a set A⁺, and let B be a consecutive block of steps with σ = ΣB ≠ 0 and σ ∉ A⁺∖B. Merging B into the single step σ gives a valid cycle of (A⁺∖B) ∪ {σ}. Its points are a subset of C's points, so there is no free-point condition. Several disjoint blocks can be merged at once.

- *Corollary (near-complete).* Let ZS be an R-sequencing of ℤ\_p^*, e.g. the geometric one: steps (g − 1)g^j, points g^j − 1. If ZS has disjoint consecutive blocks B\_i whose sums σ\_i ∈ B\_i, then ℤ\_p^*∖∪(B\_i∖{σ\_i}) has a valid cycle.
  - Example: a consecutive pattern (v, u, −v) contracts to u and gives ℤ\_p^\*∖{±v}.
  - Two-step blocks never work (x + y ∉ {x, y}).
  - For the geometric sequencing, a block of c + 1 consecutive steps works iff 1 + g + ⋯ + g^c = g^{i₀} with 0 ≤ i₀ ≤ c.
- *General form:* Graham(A) follows if some valid cycle of a larger set cuts into consecutive blocks whose sums are exactly A. This is top-down construction from explicit dense objects; no lift is needed.
- **Gap:** explicit R-sequencing families are rigid (the geometric one realizes only special local patterns). Covering all small complements C for all p needs a family of explicit sequencings with controllable local patterns.
