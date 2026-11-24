# Audit of the bounded-span (BS) handoff, plus the top-gap lift (Claude, 2026-11-24)

The submission is verbatim in `bs_handoff_submission.md`. Code is in `experiments/audits/bs_handoff/`.

## Audit
- **Two-path separation lemma: ACCEPTED (hand check of the interior case).**
  - Take an interior swap at a shared vertex v. It moves v to v′, strictly between v's neighbours on that path.
  - Minimality plus maximality of Φ give u₂ ≤ v′ < u₁, and symmetrically u₁ ≤ v″ < u₂. Contradiction.
  - The upper-endpoint case is argued more briefly but follows the same pattern.
- **BS when either sign has at most 2 elements: ACCEPTED.** Proof read; the script reruns exactly: 32,232 exhaustive cases (20,029 / 11,333 / 870) and 1,000 random cases (527 / 465 / 8).
  - **Not new in strength.** `integer_range.md` already proves the index ≤ 2 case (|N| ≤ 2) with the stronger IRC bound P+Q−1. The case |P| ≤ 2 follows by negation.
  - The strict-crossing lemma is a correct, self-contained tool.
- **Safe-contraction criterion: ACCEPTED** (elementary).
- **Both obstructions: REPRODUCED.**
  - The arbitrary-cycle expansion example.
  - The adjacent-swap compression trap at span 9, together with its trajectory through span 10.
- **k ≥ 3 path separation is FALSE** (`kpath.py`). Example: paths from 9 with steps {4, 9}, from 12 with {3, 7}, from 0 with {11}. Tops are distinct and no bottom lies on another path, yet no ordering separates all three, because each path is forced onto another path's top in a cycle. Random test: 4 failures in 3,000 three-path instances. Any multi-run extension must handle top collisions globally.

## New lemma: top-gap lift for every root (proved; 3,001 lifted walks verified by `gaplift.py`)
Let p₁ > p₂ be the two largest elements of P and q₁ > q₂ the two largest of N. Assume:
- p₁ > q₁,
- p₁ − p₂ > q₂,
- t = p₁ − q₁ ∉ P.

Set P′ = (P ∖ {p₁}) ∪ {t} and N′ = N ∖ {q₁}. Then for every r ∈ P ∖ {p₁}, G(P′, N′, r) implies G(P, N, r). Here G is the rooted-window property of `rooted_window_irc.md`.

*Proof.* Take a G-walk of (P′, N′) rooted at r. Its step +t is not the first step (r ≠ t), so it starts from some vertex v ≠ 0. Replace +t by (+p₁, −q₁) if v ≤ 0, and by (−q₁, +p₁) if v > 0. Exactly one new vertex appears.
- **v ≤ 0.** The new vertex v + p₁ ≤ p₁ is in the window.
  - If t > p₂, then max P′ = t and v + p₁ > −q₂ + p₁ > t. Here −q₂ < v because v > −max N′ = −q₂, and p₁ − q₂ > p₁ − q₁ = t.
  - If t < p₂, then max P′ = p₂ and v + p₁ > p₁ − q₂ > p₂.
  - In both cases the new vertex lies above every old vertex, so it is fresh.
- **v > 0.** The new vertex v − q₁ > −q₁ is in the window.
  - v ≤ max P′ − t, since v + t is an old vertex.
  - If max P′ = t, then v ≤ 0, a contradiction; so this case cannot occur.
  - If max P′ = p₂, then v − q₁ ≤ p₂ − t − q₁ = p₂ − p₁ < −q₂. So the new vertex lies below every old vertex (> −q₂) and is fresh.
- The window grows from (−q₂, max P′] to (−q₁, p₁]. The multiset of steps is +P ∪ −N. ∎

**Consequence.** By the max-root lift (root p₁) together with this lemma (all other roots), an induction on G\* closes whenever the pair has a **top gap**: p₁ − p₂ > q₂ (or the mirror condition, negating everything). The remaining instances are exactly those **with no gap at the top on either side**:
  p₁ − p₂ ≤ q₂ and q₁ − q₂ ≤ p₂.
This is the generic dense case, the same place where every earlier route stopped.

## Status
The full conjecture is NOT proved. The open obligation is G\* (or BS/IRC) for pairs with no top gap on either side.
