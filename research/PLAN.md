# Critical path to a complete proof of Erdős #475 (adopted 2026-11-22; supersedes ad-hoc exploration)

**UPDATE (same day, after GPT's closure attempt): PRIMARY TARGET = ASYMMETRIC ZIGZAG (Z-asym).** For P≠N (finite sets of distinct positive integers, equal sums) there is a zigzag ordering (positive first; negative step when the sum is positive, positive when negative) with pairwise distinct partial sums. Z-asym + proved symmetric walk (P=N) + one-element reduction ⇒ Graham for every prime (chain re-checked by Claude). One p-free integer statement; evidence: GPT exhaustive 28,480 pairs ⊆[1..10]; Claude adversarial near-symmetric dense families h=6..10: 164/164 (larger families running; experiments/irc/). Prompt: research/prompts/gpt_round_zasym.md. The contraction family (GSW below) is the BACKUP: sampled coverage ≈100% for |A| ≲ 0.4p at p ≤ 47 but not certifiable above ~0.45p.

**Objective:** a complete, human-readable proof for ALL primes. Finite verification covers p ≤ 37 (extendable to ~43). A proof only has to work for p ≥ p0 with p0 small enough to close by computation; thresholds of the published large-p theorems are not usable, so we need our own EXPLICIT construction.

**The one construction family we are pursuing:** contraction of reflection-symmetric walks.
- PROVED (audited candidates): for any S, W_S=(δ,M,−δ^rev,−M) is a valid cycle of ±S; every symmetric A is solved; contraction of a valid cycle (delete vertices; labels distinct, nonzero) is valid.
- DATA: every zero-sum orbit is a contraction of a (generalised) symmetric walk at p=13,17,19,23 (100%, generalised walks needed for ~1% dense orbits at p=19,23); sampled coverage p=29..37 high. Heuristic count: ≥10^3 representations per orbit for |A| ≤ 0.45p for all p up to 401.
- CONJECTURE GSW: every zero-sum A (|A| ≥ 5) is, up to dilation, the label set of a vertex-deletion of W(S,δ), where δ is any signed ordering of S∖{M} with distinct prefix sums of range ≤ M−1. This would prove Graham for every size, explicitly.

**Milestones and gates**
- M1 (Claude, local): robust evidence for GSW at p=29..61 for all sizes, dense included, adversarial sets included; failures analysed (artefact of search vs real). GATE: if real failures appear at moderate p, restrict the statement and add families.
- M2 (Claude + GPT): extract a DETERMINISTIC RECIPE (algorithm from A to (S,δ,kept vertices)) that succeeds on 100% of tests for p up to ~127 on all families. Method: mine solutions (S vs classes(A), block structure, deletions), propose recipes, falsify at scale. GATE: two recipe families, each pushed to a concrete failing A, then pivot to M2' (probabilistic proof of GSW by second moment/Fourier on the explicit family; the expected count margin is 10^3+).
- M3 (GPT, audited by Claude): PROVE the recipe/estimate for all p ≥ p0 (p0 ≤ ~60).
- M4 (Claude, local C++): extend finite verification to p0−1 (p=41,43,… ) using the one-element reduction + this construction as certificates (each set gets an explicit certificate, so verification is cheap once a recipe exists).
- M5: assemble the proof; run the referee gates on every dependency; human review of the final chain.

**Dependencies already in hand:** one-element zero-sum reduction (all sizes 2..p−3 reduce to zero-sum), near-complete |A| ≥ p−5, symmetric sets, minimal zero-sum IRC, threaded splice (thin).
**Honest status:** the full conjecture is not yet in reach; this plan is the single path with a concrete, falsifiable statement and the data to back it. Kill criterion: if GSW fails at some moderate prime with an exhaustive certificate, or if no recipe and no equidistribution proof is found after the M2 gate, we report the established partial theorems and stop pursuing a full proof via this family.
