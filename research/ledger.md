# Erdős #475 — Research Ledger

Nov 21, 2026 · @Rohan Sharma

## Problem and goal

**Graham's rearrangement conjecture (1971; Erdős–Graham 1980; Erdős Problem #475).** For every prime p, every nonempty set A ⊆ ℤ\_p ∖ {0} has an ordering a₁, …, a\_k whose partial sums a₁, a₁+a₂, …, a₁+⋯+a\_k are pairwise distinct (a *valid ordering*).

**What "solved" means here:** a proof for *all* primes p. Large p is already settled (see Status); the open content is an argument covering every prime, either a uniform proof or an explicit threshold plus a finite verification below it.

**Useful symmetries:** if a₁,…,a\_k is valid for A, then g·a₁,…,g·a\_k is valid for gA (g ∈ ℤ\_p^×). For zero-sum A, a valid ordering stays valid under cyclic rotation (partial sums shift by a constant).

## Status (literature)

| Range | Result | Effective? |
| --- | --- | --- |
| \|A\| ≤ log p / log log p | Kravitz, Integers 24 (2024), arXiv:2407.01835 | yes |
| \|A\| ≤ exp((log p)^{1/4}) | Bedert–Kravitz, Isr. J. Math. 273 (2026), arXiv:2409.07403 | constants not explicit |
| C\_α ≤ \|A\| ≤ p^{1−α} | Pham–Sauermann, arXiv:2602.15797 (Feb 2026) | inequalities explicit, no numerical p |
| \|A\| ≥ p^{1−c} | Bedert–Bucić–Kravitz–Montgomery–Müyesser | not explicit |
| \|A\| ≥ (1−o(1))p | Müyesser–Pokrovskiy, Invent. Math. 240 (2025) | not explicit |
| \|A\| ≥ n₀, any finite abelian G | Kuang–Wang arXiv:2610.34424; Nguyen–Tran–Vu arXiv:2610.40712 | n₀ not explicit |
| small \|A\| for all p | sizes ≤ 12 (cited in Kuang–Wang); Alspach–Liversidge ≤ 9 | yes |
| all cyclic groups of order ≤ 25 | Archdeacon et al., JCMCC vol. 98 | computational |

**Bottom line:** the conjecture is proved for all sufficiently large p (Pham–Sauermann + earlier work). No numerical threshold exists in print. All-primes remains open.

**How large is "sufficiently large"? (Claude's rough estimate, not a theorem.)**

- *Starting point.* Pham–Sauermann need |S| ≥ C\_α with C\_α ≥ (10⁴·2^{40D})^{1/α}, where D = ⌈3/α⌉.
- *Optimistic choice.* Even taking α = 1/2, which is far larger than the unspecified c the large-set side allows, gives C\_α ≳ 2⁵⁰⁰.
- *Small-set side.* Covering |S| < C\_α requires exp((log p)^{1/4}) ≥ 2⁵⁰⁰ (Bedert–Kravitz, ignoring their own constants), i.e. log p ≳ 10¹⁰.
- *Conclusion.* The present chain of results gives a threshold of at least about e^{10¹⁰}. Closing the gap by computation is hopeless; it needs new proofs with far better constants, or a uniform argument.

## Verified computations

| p | Nonempty subsets | Scaling orbits checked | Burnside count | Result |
| --- | --- | --- | --- | --- |
| 5–23 | all | all | — | all valid |
| 29 | 2²⁸ − 1 | 9,587,579 | 9,587,579 | all valid |
| 31 | 2³⁰ − 1 | 35,792,567 | 35,792,567 | all valid (new) |

**Method (Claude, 2026-11-21):** C program `graham2.c`. Enumerates every subset mask, keeps the minimum of each multiplicative orbit, finds a valid ordering by randomized DFS with restarts (node budget doubling; never gave up on any set), and re-checks every ordering found independently. Non-zero-sum sets are checked directly, so no rotation argument is needed. Largest search: about 4.2 million nodes (p = 31). Each p runs in minutes on 2 cores.

**Cross-checks of GPT's p = 29 certificate:** 9,256,396 zero-sum subsets and 331,185 zero-sum orbits are both exact, but both include the empty set (nonempty: 9,256,395 sets). The certificate zip itself has not been seen by Claude.

**Combined:** every prime ≤ **37** is verified (Archdeacon et al. ≤ 25, plus 29, 31 and 37 here). Priority for 29, 31 and 37 is unchecked.

**Next feasible:** p = 41 (2⁴⁰ subsets, ≈ 2.7·10¹⁰ orbits, \~14× the p = 37 work). Feasible on a multi-core machine with `graham4`; a zigzag-first checker would be faster.

**All abelian groups of order ≤ 27 (Claude, `seqgrp.c`).**

- *Scope.* All 42 groups: 2 ≤ |G| ≤ 27, every invariant-factor decomposition, cyclic and non-cyclic.
- *What is checked.* Every nonempty S ⊆ G∖{0} must have a **sequencing**: partial sums pairwise distinct and nonzero except possibly the last. This is the strong (Alspach–Liversidge) sense, and it implies Graham's valid ordering.
- *Result.* 0 failures; the largest groups (order 27) have 67,108,863 subsets each.
- *Significance.* This extends Archdeacon et al.'s cyclic ≤ 25 to all abelian groups ≤ 27, and independently backs the ℤ\_t (t ≤ 21) input used by arXiv:2608.10015.

**p = 37: DONE (Nov 22).** `graham4` necklace generation in 64 groups (`p37n/g*.log`): 1,908,881,899 orbit representatives, 0 failures. This equals the Burnside count 1,908,881,900 minus the empty set, so coverage is complete. Graham's conjecture holds for p = 37.

## Proof candidates and gaps

### Atomicium all-primes candidate

Repository Atomicium-org/graham-rearrangement-certificates, commit 23cb1d03. A French manuscript plus finite checkers for local blocks R, C0.3, H0-B⁺, U0simple, C0.1 and C0.2. It self-describes as a proof candidate, not peer-reviewed.

- **Gap in Lemma C0.3 (manuscript \~L2792–2852), confirmed by Claude's reading.** The normalization trichotomy (lem:trichotomie-normalisation) only compares K′ with its normalization K″. The surgery step K → K′ is never compared with K. Case 3 ("no coordinate of Ξ⁺ descends") then assumes Ξ⁺(K″) = Ξ⁺(K), so a strict increase is unhandled.
- **Checker (checkers/C03/c03\_certificate\_checker.py \~L345–387):** GPT reports that it accepts an abstract configuration whose active support grows from 2 to 3 labels as "neutral".
- **Status:** a real hole in the text. It is not yet a counterexample: no genuine surgery reaching such a configuration has been exhibited.
- **Partial repair (GPT):** a crossing-count lemma repairing the local interval inequality in C0.2. Not yet audited by Claude.
- **Structural problems found by Claude (2026-11-21), deeper than C0.3:**
  - *Undefined potential coordinates.* κ\_rest ("complexités secondaires"), 𝒮 ("spectre accessible") and d\_cert ("distance certifiée") are named but never defined (§§Potentiel composite, Potentiel raffiné). So Ξ and Ξ⁺ are not well-defined, and no descent claim that uses them can be checked.
  - *Normalization trichotomy is unsound as written.* A "descending step" may decrease any of Θ\_R, Θ\_cor, Ξ or Ξ⁺ "depending on context", and the proof stops at the first non-editorial step. A decrease of one potential at one step does not give a strict decrease of a single well-founded potential over the whole sequence.
  - *The paper is openly conditional* (§Introduction): "if these four bricks are proved formally with the indicated descents, the theorem follows." It is a proof programme, not a proof; C0.3 is one symptom.

### March 2026 preprint (arXiv:2603.20961): zero-sum sets through size 22

- **GPT's claim:** the deposited search misses a branch. Mod 29, splitting 8 into 9, 28 in the cycle (1,2,3,4,5,6,8) gives partial sums 1, 3, 6, 10, 15, 21, 1, 0. The repeat comes from a length-6 zero-sum block whose short complement (28,1) wraps around the cut.
- **Claude:** arithmetic confirmed. Not yet checked against the preprint's code. The set itself has a valid ordering, so this is a gap in their search procedure, not a counterexample.
- **GPT also reports** a case where the program's rational-rank test fails to transfer mod 29. Not audited.
- **What the paper actually claims (Costa–Della Fiore–Fontana–Vena).** Thm 1.4: every A ⊆ G∖{0} with |A| ≤ 20 is sequenceable, for *every* abelian G. Thm 1.5: zero-sum A with |A| ≤ 22. Thm 1.6 (CMPP): zero-sum A, no inverse pairs, |A| ≤ 23. The method is a computer search that closes a branch when eᵢ or eᵢ−eⱼ lies in the **rational** row span of the collected zero-sum incidence vectors, computed with floating-point numpy.matrix\_rank. Code: Zenodo 10.5281/zenodo.18997904, which is not reachable from Claude's environment.
- **Q-rank closure is unsound in groups with torsion (verified by Claude, 2026-11-22).** Explicit example, k = 9:
  - nine zero-sum blocks, each an interval of length ≤ 4 in an ordering at most 3 adjacent swaps from the identity, on positions {1,5,6}, {3,6,7,8}, {1,4,5,7}, {1,2,3,4}, {2,4,6}, {0,1,2}, {2,3}, {0,3,4,5}, {3,5,8};
  - their 0/1 matrix has determinant −17, so over ℚ every eᵢ is in the row span and the test would close the branch ("aᵢ = 0");
  - yet in ℤ₁₇ the distinct nonzero values a = (10, 9, 15, 2, 8, 14, 11, 3, 1) satisfy all nine relations.
  - Further examples were found with k = 10, p = 17 and k = 10, p = 19.
  - This shows the method's closure rule is invalid whenever p divides a certificate's denominator. It has not been shown to be reached by the authors' actual tree. The theorem may still be true: Claude's exhaustive checks find no counterexample in any small group.
- **Downstream dependency:** Costa–Della Fiore–Feng–Liu (arXiv:2608.10015, Cor. 1.6, ℤ\_{tp} for 2 ≤ t ≤ 21) cite this paper for strong sequenceability of ℤ\_t. That input is independently covered by Claude's exhaustive group checks (all abelian groups of order ≤ 27).
- **Deposited code audit (treeSearch.py, sha256 d3dbceb4…; Claude, 2026-11-22).**
  - *(i) Length cap.* The interval cap j − i ≤ ⌊n/2⌋ is applied unconditionally, including in the non-zero-sum case, where no complement argument justifies it. This contradicts the paper ("only the full interval is excluded"). Allowing long intervals, the tree still closes for n ≤ 7; n = 20 is unchecked.
  - *(ii) Known blocks skipped.* Intervals whose relation is already known are skipped. That leaves the case where an ordering's only collision is a known block uncovered. Such nodes occur 28 times (n = 8, zero-sum) and 41 times (n = 8, non-zero-sum). The smallest is n = 4: ordering (1,2,3,4) with a₂ + a₃ = 0 already known. Branching honestly on known blocks with the paper's swap rule leaves cycling, unclosed branches even at n = 4.
  - *(iii) Missing total-sum relation.* Zero-sum mode never adds Σaᵢ = 0 to the relations; adding it would close the n = 4 example.
  - *(iv) Floating-point ℚ-rank.* GPT confirmed `is_solution` accepts the det −17 system.
  - *Verdict.* The deposited search does not prove Thms 1.4–1.5 as written. The gaps may be repairable; no counterexample is known.

### Effective cutoff work (GPT)

- **Claim:** every size-23 set is valid for p > 1,089,457,290, from Kravitz's integer sequencing theorem plus a determinant bound, with a formula at each fixed size.
- **Claude:** not audited.
- **Limitation:** no all-sizes numerical cutoff. Even with one, checking all sets of size about 23 mod primes up to 10⁹ is infeasible, so finite verification cannot close the gap; a proof is needed.

## Open problems / frontier

1. **C0.3 decision.** Prove that every successful global surgery satisfies Ξ⁺(K′) ≤ Ξ⁺(K), or exhibit a genuine surgery raising it (concrete p, set, cycles M\_N ↔ M\_P). This decides whether Atomicium's candidate can stand.
2. **Effective large-p theorem.** Extract a numerical threshold from Pham–Sauermann and the results it combines, or confirm none exists anywhere (talks, follow-ups).
3. **Explicit n₀** for Kuang–Wang / Nguyen–Tran–Vu (large sets in all abelian groups).
4. **Audit of GPT's side results:** the C0.2 crossing-count lemma, the size-23 cutoff, the preprint's rational-rank transfer failure.
5. **Computation:** p = 37 exhaustive check (optional; establishes a record, not a proof route).

### Induction route (GPT round 2 plan) — data

- *Reduction to zero-sum sets.* Correct (Claude checked). A legal pair x, y with x + y ∉ A ∪ {0} exists for 5 ≤ |A| ≤ p − 2 (Dias da Silva–Hamidoune).
- *(a) Some pair works.* Every zero-sum A, 5 ≤ |A| ≤ p − 2, p ≤ 31, has some legal pair with a successful direct expansion. That covers 1,155,694 orbits at p = 31.
- *(b) Every pair works.* For p ≤ 29, for every legal pair, A has a simple cycle with x and y consecutive: 15,066,547 pairs at p = 29, no failures. A candidate strengthened induction hypothesis.
- *(c) A given B-cycle often fails.* From a given cycle of B, direct expansion fails for 21% of B-cycles at p = 11 and 32% at p = 13; the worst pair fails on 46%.
- *(d) The swap repair can be trapped.* The repair v → r + s − v is trapped in some cases. Exhaustive example: p = 11, A = {2..9}, pair (4,6), B-cycle steps (10,3,7,9,8,2,5); its orbit has 6 walks, none simple. At p = 13, 547 of 11,090 failures are unrepaired within 12 swaps.
- *Conclusion.* The induction needs a cycle-choice argument or a richer repair move with a termination proof.

**GPT round 3 + Claude (2026-11-22).**

- *Trap verified.* GPT's p = 29 trapped configuration (x, y) = (14, 22), z = 7: block-reversal and block-swap moves reach only t and its reversal. Claude ran GPT's verifier and it passed.
- *Reformulation accepted.* GPT recast (b) as one-vertex avoidance h ∈ H(B, z), using the tail-reversal symmetry V ↔ z − V (checked).
- *New: a single cycle suffices.* Claude found that **one** cycle covers all splits at once. Property (S): for every zero-sum B ⊆ ℤ\_p^\*, 4 ≤ |B| ≤ p − 3, and every marked z ∈ B, some simple cycle through the edge 0 → z contains no legal pair {h, z − h} in its vertex set. Equivalently, it expands *every* legal split of z at once, so m(B, z) = 1.
- *Evidence.* (S) holds exhaustively for p ≤ 31: 17,026,322 marked scaling-orbit pairs at p = 31, 0 failures, 0 undetermined. Exhaustive set-cover for p ≤ 13 and sampled for p = 17 likewise give m = 1 throughout. (S) is a candidate self-strengthening induction hypothesis.

**GPT round 4 + Claude (2026-11-22).**

- *GPT claim (unaudited; verifier not received):* (S) holds for all primes when 4 ≤ |B| ≤ 6, together with the recursive statement (R) at sizes 5–6. Method: symbolic linear-relation branching, plus direct checks of primes up to the Hadamard bound (53 for k = 5, 211 for k = 6).
- *Size-4 base (checked by Claude).* GPT's argument covers the case −z ∈ B: put −z in the middle. Claude checked that the other case is immediate: if −z ∉ B, every order (z, a, b, c) works.
- *Six-element obstruction (verified for p = 11, 13, 17, 19, 23, 101, 1009).* B = {1, 2, 3, −1, −2, −3}, z = 1. For each of the three legal pairs, some (S)-cycle of the compressed set fails to expand. Arbitrary smaller witnesses therefore do not lift.
- *Mod-11 full-history obstruction.* GPT's witness (1, 9, 3, 7, 6, 2, 5) checked as an (S)-cycle.
- *(R) with only the first pair prescribed (Claude, Rtest.c).* The first pair is fixed; the initial (S)-order and all later contractions are free. Exhaustive over scaling orbits: 0 failures and 0 undetermined for p = 11, 13, 17, 19, 23 (2,188,662 instances at p = 23). p = 29 is running.

**GPT round 5 + Claude analytic round (2026-11-22).**

- *Audited.* GPT's inline size-5/6 verifier passes over ℚ and every prime up to the Hadamard bound (75 / 3,997 nodes). Index-one construction (R) holds on the p = 73 example and on 8,733 random instances. The one-cycle-lifts-all-splits property holds exhaustively for p ≤ 23 (678,514 triples).
- *Cut model.* Lift the cycle to \[0, T\] with positive lengths. Conditions: cuts injective mod p, and no legal cuts with c + d ≡ −z.
- *Wrapping-lift symmetry (Claude).* In the index-one picture, a wrapping split w = x + y (x + y = w + p) puts the two candidate new cuts u + x, u + y at mirror positions about the midpoint of w's interval. The forbidden set C ∪ ρ(C) is invariant under the reflection ρ(c) = T − c. So if w's interval is centred at T/2 the two choices fail together; the lift must place w off-centre.
- *Negative result for target (A) (Claude).*
  - For symmetric sets D = {±a₁..±a\_r} with the mark scaled to z = 1, there is **no order-type rule** (a fixed signed-rank pattern) producing an (S)-cycle for all magnitudes once r = 5 (tested for primes < 30).
  - Universal patterns exist for r ≤ 4.
  - So, unlike index one, the multi-trip / signed case cannot be handled by an inequality/interlacing argument alone. Constructions must depend on arithmetic, which points to counting or choice arguments (target C).
- *Wrapping pairs (Claude).* A legal wrapping pair need not exist in an index-minimizing dilation: (1, 2, 3, 4, 5, 7) mod 11 has index 2 and none. This happens in 10–30% of index-≥ 2 sets for p ≤ 17.
- *Computation.* (R)-first-pair at p = 29: 3 of 16 groups done, 0 failures. p = 37: 42 of 64 groups done, 1,486,696,923 orbits, all valid.

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

**Three-jump lemma — CORRECTED Nov 22 (the original statement was false).**

*Statement (corrected).* Let b < c < d be positive integers. Let F = F₁ ∪ F₂, where each Fᵢ has all gaps between consecutive points at least D, with **D > 2c** (D > 2d suffices). Let t be a position with t + b + c + d ∉ F. Then some ordering of b, c, d has landing points (after one and after two jumps) outside F. *Original version (D > d only) is FALSE:* jumps 1, 6, 7 from t = 0 with F₁ = {1, 13}, F₂ = {7} block all six orderings. Exhaustively, every failure under D > d alone has this shape: d = b + c and F ⊇ {t+b, t+d, t+c+d}, with t+b and t+c+d in one family (gap 2c).

*Proof.*

1. *Notation.* Let P\_e = t + e be the first landings and Q\_{ef} = t + e + f the second landings. Since D > 2c > d, any window of length < D holds at most one point of each family.
2. *At most two of each in F.* The three P's lie in a window of length d − b < D, so each family contains at most one of them, and at most two lie in F. The same holds for the three Q's.
3. *When an ordering fails.* Starting with e fails if P\_e ∈ F, or if both of the Q's containing e lie in F (a trap). Since at most two Q's lie in F, at most one e is trapped.
4. *The only failing pattern.* All three orderings fail only if one element is trapped and the other two are blocked. Say b is trapped and c, d are blocked: Q\_bc, Q\_bd, P\_c, P\_d ∈ F.
5. *Placing the points.* P\_c and P\_d are distance d − c < D apart, so they lie in different families; write P\_c ∈ F₁ and P\_d ∈ F₂. Q\_bc is distance b from P\_c, so Q\_bc ∉ F₁ and hence Q\_bc ∈ F₂. Its distance from P\_d is |b + c − d| < D, so Q\_bc = P\_d and d = b + c. Similarly Q\_bd is distance b from P\_d, so Q\_bd ∈ F₁, at distance 2b from P\_c.
6. *Other cases (the original proof wrongly called them symmetric).* **c trapped:** P\_b, P\_d ∈ F lie in different families, and the same placement argument forces d = b + c, with Q\_cd in P\_b's family at distance 2c from it. This needs 2c ≥ D, which the corrected hypothesis excludes. **d trapped:** P\_b ∈ F₁ and P\_c ∈ F₂. Q\_bd is at distance d < D from P\_b, so it lies in F₂, at distance b + d − c ∈ (0, D) from P\_c, which is impossible. **b trapped:** gives 2b ≥ D > d = b + c > 2b, impossible. ∎

*Role.* This is the end-game for index 3 when trip-2 elements all exceed trip-3 elements.

**Impact of the correction.** The "lemma hypotheses hold in \~96% of index-3 instances" statistic was computed against the false hypothesis (D > d). It must be recomputed with D > 2c; until then the index-3 near-complete claim is **withdrawn**. Found by the exhaustive k-family grasshopper test (`int/kfam.c`), which also shows that k families need more than k + 1 jumps in general: m = 4, k = 3 has 1,073 failures (J ≤ 10), and m = 5, k = 3 has 104. Under D > maxjump alone, m = 4 with k = 2 had 0 failures (J ≤ 12).

**The remaining index-3 failures are all one mechanism: a carry at the trip 2 → 3 transition.**

- *What happens.* A large element b is blocked when it would land in trip 3. The greedy then finishes trip 2 with smaller elements, and b is carried into the end-game.
- *Why it hurts.* The lifts of trip 2's tail vertices sit near 3p, exactly where the end-game happens, and they are spaced by gaps smaller than b. That breaks the lemma's hypothesis.
- *Example.* p = 17, reps (14, 11, 9, 8, 5, 3, 1): the greedy path is 14, 11, then 8 (9 blocked at 34 = 2p), then 5 (9 blocked at 42 ≡ 25). The end-game {9, 3, 1} faces forbidden points 42, 48, 50.
- *Status.* An exhaustive last-4 search always succeeds; a proof must handle the transition zone.

**Modular grasshopper is false at useful strength (Claude, exhaustive p = 11, 13).**

- *Statement tested.* Partial sums of an ordering of R ⊆ ℤ\_p∖{0} (|R| = n) must be distinct and avoid an arbitrary forbidden set M ⊆ ℤ\_p∖{0} with ΣR ∉ M (final 0 allowed).
- *Result.* This holds for all R, M only when |M| ≤ 0–3. Mod 13, the tolerated |M| for n = 2, 3, …, 12 is 1, 0, 1, 1, 2, 2, 3, 3, 2, 1, 0.
- *Consequence.* Any high-index argument must use the structure of the walk's own visited set; avoiding an arbitrary forbidden set of comparable size is impossible.

### Integer / zigzag reformulation (Nov 22)

**Reduction (proved).** Take any dilation of a zero-sum A ⊆ ℤ\_p∖{0}, positive reps summing to Tp. Replace the T largest reps r by r − p. This gives an integer zero-sum set P ∪ (−N) with P, N ⊂ ℤ\_{>0} and max P + max N ≤ p − 1. Any ordering whose integer partial sums S₀,…,S\_{n−1} are distinct and span range ≤ p − 1 is a valid cycle mod p. The index T equals |N|. P = N exactly when A = −A.

**IRC (conjecture, p-free).** For all finite P, N ⊂ ℤ\_{>0} with ΣP = ΣN, some signed ordering has distinct partial sums with range ≤ max P + max N − 1. IRC implies Graham for every prime. It holds in 1,888,173 instances (values ≤ 18, n ≤ 9). The bound is tight: range ≤ max P + max N − 2 fails, e.g. P = N = {5,6}.

**Zigzag walks.** Rule: S < 0 ⇒ next step positive; S > 0 ⇒ next step negative; the first step is positive. Every zigzag walk stays in (−max N, max P\], so range is automatic. A zigzag walk is determined by the pair (σ, τ) of orders of P and of N.

**Two-ruler criterion (proved).** Lay σ on ruler X and τ on ruler Y, both of length W = ΣP, with cut sets X₁… and Y₁…. The walk is valid iff (i) the interior cuts are disjoint; (ii) the distances from each Y-point (including 0) up to the next X-point are pairwise distinct; (iii) the distances from each X-cut up to the next Y-point are pairwise distinct. Equivalently: two X-cuts in different Y-segments never differ by the difference of those segments' right ends, and symmetrically.

**Zigzag Conjecture Z\*.** Every (P, N) has a zigzag walk, except P = N ∈ {{a, b, a+b}, d·{1,2,3,4}}.

- 0 non-symmetric failures in 36,795,364 instances (values ≤ 22, n ≤ 10).
- Symmetric failures up to 22 / |B| ≤ 5 are exactly those two families (115 sets).
- Random Graham instances (p ≤ 5000, n ≤ 60): all solved, except two very dense ones (n = 55 at p = 67; n = 60 at p = 73) that are *undetermined* (search budget). Dense near-complete families are all solved up to n = 19; at n = 21–23 many are undetermined, none proved impossible.
- The two exceptional families are covered separately (size ≤ 6 proved; d·{1,2,3,4} has explicit non-zigzag cycles).

**Rooted strengthening Z1.** A zigzag walk starting with +max P exists, except also the family P = {a, b, a+b, 2a+b}, N = {a, a+b, 2a+2b} (16 failures in 5,268,069 rooted instances, all in this family).

**Proved pieces.**

- *b = 1 and b = 2 (index ≤ 2) zigzag theorem.* Put max P first. Then condition (ii) is automatic: every gap is less than p₁. Condition (iii) is vacuous for b = 2. What remains is avoiding one point with prefix sums (one-obstacle grasshopper). This is much shorter than the mod-p index-2 proof.
- *Lift lemma.* If y ∈ N, y < p₁ and p₁ − y ∉ P, a zigzag walk of (P∖{p₁} ∪ {p₁ − y}, N∖{y}) that starts with p₁ − y lifts to a walk of (P, N) starting with p₁. The point p₁ lies above every positive point of the smaller instance. Corollary: induction on Z1 works whenever min N < p₁ − p₂, and dually whenever q₁ > p₁ + q₂.
- *b = 3 with min N < max P* reduces (τ = (q₃, ·, ·), σ starting p₁) to a two-trip problem with trips of unequal length: the index-2 dodge setting. **Gap:** this is not yet written out; the extra constraint g(Y₁) ≠ g(Y₂) must be handled.

**Negative findings (rules that do not work).**

- Fixed sorted orders: σ or τ fixed fails 2–8%.
- Largest-first zigzag greedy fails 9–33% even with an 8-element exhaustive end-game.
- Prescribing an arbitrary first element fails in small structured cases (44 / 34k at n = 8).
- σ descending except a free tail of E positives, τ free: E = 4 gives 222 failures and E = 5 gives 3 at n ≤ 11. The tail must grow with n.

**Open gaps (explicit).**

- G1: prove Z\* (or IRC) in general. This is the whole conjecture.
- G2: settle the dense regime (|A| close to p) computationally or by construction.
- G3: b = 3 zigzag theorem (supersedes the index-3 residual cases).
- G4: an inductive hypothesis that closes under the lift (the start-point avoidance problem).

### Round: structure of zigzag solutions (Nov 22, afternoon)

**Index-3 coverage recomputed with the corrected three-jump lemma** (gaps > max(d, 2c)): the end-game lemma applies in 10,104 / 10,919 random index-3 instances (92.5%). The residue is 708 gap failures and 397 instances where the end-game starts before trip 3. The rule itself still never failed. Index 3 stays open as a theorem.

**Canonical walk W₀** (σ and τ both descending; the zigzag walk is then unique):

- It works in \~30–60% of random instances.
- Failure mechanism: a value shared by P and N meets itself (+c then −c), or near-coincidences do.
- *Alternating-series theorem (proved):* if, after removing the first positive and the last negative step, the sorted merged values strictly alternate N, P, N, P, … and all the derived gaps d\_t are positive, then the walk alternates sign every step and |S\_t| strictly decreases. So it is valid.

**Run-split class.** Let σ and τ each have at most k ascents (concatenations of ≤ k+1 decreasing runs).

- Exhaustive small cases (n ≤ 10): (σ ≤ 2, τ ≤ 2) gives 0 failures in 1,663,538 instances. (σ ≤ 1, τ ≤ 2) gives 0 failures for n ≤ 9. (σ ≤ 1, τ free) gives 0 failures for n ≤ 10.
- Random instances (p ≤ 300, n ≤ 24): minimal k ≤ 2 always, k ≤ 1 in \~99%. Undecided beyond n ≈ 25 (search limits).
- **Conjecture R:** a zigzag walk exists with σ, τ each having ≤ 2 ascents. **Status: unproved.**
- No canonical split was found. Many splits work, and a working split nearly always contains p₁ in the second run.
- Rotations of the descending orders fail (18,094 / 114,332), single relocations fail (\~2.5%), and spiral walks fail (\~50%).

**Why rooted induction stalls (analysis).** The only lifts that are automatically safe insert a point outside the window of the smaller instance. That means expanding +d into (+p₁, −y) from a point S ∈ (−min(p₁ − p₂, y), 0\], or dually (−q₁, +x). Each lift therefore needs a rooting condition on the smaller walk, and rooting conditions accumulate across levels. A single rooted hypothesis closes only when y < p₁ − p₂ or q₁ > p₁ + q₂.

**Calibration.** The dense zigzag case is a signed, closed analogue of linear realizations of multisets (Buratti–Horak–Rosa, open since 2007). A full proof of Z\* should be expected to need a genuinely new flexibility mechanism (absorbers or a structural induction), not a refined greedy.

**Dense search update:** 48 of the 58 hard near-complete instances (n = 21–23) are now solved; 10 remain undetermined at 4·10⁸ nodes; none is proved impossible.

### Round: absorbers for the zigzag end-game (Nov 22, noon)

**Design** (`int/absorb*.c`). Reserve R. Run the core walk (largest-first zigzag greedy, skipping collisions) on everything outside R until the required sign is exhausted. Then finish exhaustively with all remaining elements.

**Which reserve?** n = 10–20, p ≤ 200, r = 6, failures per 1000:

- none: 416
- smallest overall: 91
- smallest on each side: 95
- half small, half large: 152
- **largest on each side: 29**
- best of 30 random reserves: 3

**Mechanism (the key finding).** Reserving the top k of P and of N confines the core walk to (−q\_{k+1}, p\_{k+1}\]. The shell (p\_{k+1}, p₁\] ∪ (−q₁, −q\_{k+1}\] is therefore guaranteed empty when the finish starts. Big reserved jumps can land there, or anywhere in the core. This is the "insert a point beyond the window" lift from the induction analysis, now arising globally rather than one step at a time.

**Scaling** (top-k reserve, k = 4 unless stated; all counts are genuine dead ends, not search cut-offs):

- *Sparse, p ≤ 3000:* 1 / 500 failures for n = 12–30; **0 / 300** for n = 30–60 (also 0 / 300 with k = 6).
- *Dense, p ≤ 120, n = 12–30, by k:* k = 2: 32 / 500; k = 3: 14; k = 4: 7; k = 5: 7.
- *Randomized core walks* (up to 100 attempts) leave 7–8 / 500. The persistent failures are all **near-complete**, |A| ≈ p − 4 to p − 7 (e.g. p = 19, n = 15).
- *By n at p ≤ 120:* the failure rate rises with density, from 1–3% at n ≤ 29 to 16% at n = 54–59. With n = 42–53, k = 8 gives 4 / 200 genuine failures plus 14 search cut-offs.

**Reading.** The shell absorber is the right mechanism at low and moderate density. Near-complete sets defeat it, because the core walk must visit almost every core slot and the shell is only about k wide.

**Proposed proof architecture (all of it unproved):**

- (I) *Shell-absorber theorem* for density below a threshold. This needs a rigorous end-game counting lemma: the finish has many orderings, the shell is empty, and core collisions must be bounded.
- (II) *Near-complete regime* |A| ≥ p − C via explicit constructions (the literature has C = 3).
- (III) The middle densities, where the absorber fails a few percent with a fixed core rule. Needs either core flexibility or a growing reserve.

**Gap:** none of (I)–(III) is proved.

### Round: the sparse counting lemma (Nov 22, 1 pm)

**1. The arbitrary-obstacle finishing lemma is impossible (proved).** Under the zigzag rule the first finishing step from s has at most k options (s + p\_i, or s − q\_j). A visited set V can block them all with k points. Any finishing lemma must therefore use where the core walk ends, or the structure of its trace.

**2. Steering helps only mildly.** Core walks ending near 0 fail \~7–8% versus 14–18% farther out (3000 dense instances).

**3. The canonical walk is not random-like.** In sparse instances (p ≤ 3000), most W₀ failures come from *long* zero-sum intervals: 398 of 660 have length ≥ 5, against 155 from shared values (length 2). So W₀ cannot be the core of a counting argument.

**4. Random zigzag walks are random-like.** Uniform σ and τ with the sign rule give a mean collision count of ≈ 1.25 · n²/(2p):

- p ≈ 2500, n = 20: success 0.905, mean 0.099
- p ≈ 2500, n = 40: success 0.670, mean 0.403
- p ≈ 2500, n = 60: success 0.402, mean 0.929
- p ≈ 250, n = 20: success 0.410, mean 0.862

Key structural fact: an interval of a zigzag walk equals a block of σ minus a block of τ. So a collision is an equality of block sums of two independent random permutations.

**5. Structured sets.** Random zigzag success, best over 30 dilations:

- random sets: ≥ 0.90 for every set tested
- 2-dimensional GAP subsets: worst set 0.4–0.6
- **AP subsets: worst set 0.00**. Such a set is e·X with X small integers. Its zero-sum subsets come from X and are dilation-invariant, so every dilation has many.

**Conclusion.** A rigorous sparse lemma splits into three cases:

- (a) short-AP sets: Kravitz's positives-then-negatives argument (known);
- (b) unstructured sets: block-sum anti-concentration via inverse Littlewood–Offord, then a random-walk count (LLL or second moment);
- (c) rank ≥ 2 GAP structure: exactly the rectification barrier treated by Bedert–Kravitz.

The zigzag frame does not obviously bypass (c). Done rigorously, this route mainly re-derives known small-set results, possibly with better effectivity. **The novelty, and the obstruction to an all-p proof, sits in the dense and near-complete regime.**

### CORRECTION (Nov 22, 1 pm): Z\* is false as stated; IRC survives

**Z\* fails for dense symmetric sets.** Plain exhaustive search (no pruning, `int/zigB.c`) shows that P = N = \[1..h\] has **no zigzag walk for h = 7, 8, 10**; walks exist for h = 5, 6, 9.

- Symmetric zigzag failures with values ≤ 16 and |B| ≤ 8 are exactly {a, b, a+b} and d·\[1..h\] for h ∈ {4, 7, 8}.
- The earlier scan had |B| ≤ 5, which missed h = 7, 8.
- For B = \[1..h\], every point of the window must be visited, so the walk is a rigid Hamiltonian cycle.
- Status for h ≥ 11: undetermined (search limits).
- Z\* must be restricted, either to an explicit exception list or away from the dense regime. The "36.8M instances, 0 non-symmetric failures" evidence stands, but it covers only n ≤ 10.

**IRC holds in every dense case tested** (`int/ircfast.c`, randomized DFS, all solved within seconds):

- full intervals \[1..h\] for h = 4–18;
- the 10 near-complete instances (n = 22–23) that zigzag search could not decide;
- the two very dense random instances (n = 55 at p = 67; n = 60 at p = 73).

**Revised picture.** IRC (range ≤ max P + max N − 1, no sign rule) is the robust p-free conjecture. Zigzag is a sparse-regime tool. In the dense regime, the sign rule is what fails, not the integer statement.

**Literature check.** Near-complete sets are covered only for p − 3 ≤ |A| ≤ p − 1 (cited by Kravitz, arXiv:2407.01835). The "t" of arXiv:2608.10015 is the multiplier in ℤ\_{tp}, unrelated. Target |A| ≥ p − C for C > 3 remains frontier.

### Round: uniform polynomial-method reformulation (Nov 22, 2 pm)

**Setup (proved).** Let A be zero-sum, |A| = k. A cyclic order is valid iff every cyclic interval of length 2 to k − 2 has nonzero sum. Lengths 1 and k − 1 are automatic, and complementary intervals give equivalent conditions. Take one interval from each complementary pair and set G(x) = V(x) · ∏ (interval sums). Then deg G = k(k − 2), which is k below the CN maximum k(k − 1).

- The natural full-degree polynomials have **identically zero top coefficient for every k ≥ 3**: V(x)V(s) and its zero-sum variant (`int/ck.py`, `ck2.py`).
- G admits the monomials x\_a⁰ · x\_b^{k−2} · ∏\_{others} x^{k−1}. Their coefficients c(a, b) are **circulant**: c(a, b) = f\_k(b − a mod k). They are palindromic up to a period-4 sign pattern, and rows sum to 0. Near-balanced monomials give the same values.

**Reduction (proved).** Fix x₀ = 0 and alternate over the other m = k − 1 positions. The degrees match exactly, so up to factors whose primes are all ≤ k, f\_k(d) = c\_k(d), where c\_k(d) is the coefficient of V(y) in Alt\_{S\_m}(y\_d · I(y)). Here I(y) = ∏ (y\_i + ⋯ + y\_j) over intervals of \[1..m\] of length 2 to m − 1.

- c\_k is **intrinsic**: it does not depend on which interval represents each complementary pair, because the changes are multiples of e₁, which the alternation kills.
- *Root-system form:* with y\_i = α\_i (simple roots of A\_m), I = ∏ of all positive roots except the simple roots and the highest root.
- *Coinvariant form:* CN fails at p iff I lies in the ideal (e₁, …, e\_m) mod p in degree C(m, 2) − 1, using the perfect pairing R\_{N−1} × R₁ → R\_N for p > m.

**Theorem (conditional on the data below).** If gcd(c\_k) has no prime factor > k, then every zero-sum A ⊆ ℤ\_p∖{0} with |A| = k has a valid cyclic ordering, **for every prime p**.

**Data** (`int/Ed2.c`, (k − 1)! terms per k):

| k | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gcd(c\_k) | 1 | 2 | 4 | 6 | 12 | 6 | 1 | 4 |

k = 13 is running. **All gcds divide 12.** Individual entries carry large primes (e.g. k = 10: 9989341, 5446271).

- No single coefficient has a product formula. This includes the top coefficients of G · ∏(x\_i ± x\_{i+1}) and G · ∏(x\_i − x\_{i+2}).
- Fourier norms are smooth only for k ≤ 7.

**Conjecture CN.** For all k ≥ 4, gcd(c\_k) divides 12 (weak form: it has no prime factor > k).

- CN implies the zero-sum case of Graham at every prime. Non-zero-sum sets still need a reduction.
- CN is *stronger* than Graham: it certifies all k-sets at once.
- **Gap:** no proof. The "divides 12" pattern suggests a structural identity, for example an integer combination of the c\_k(d) equal to a divisor of 12 times a smooth number.

**Update (Nov 22, 2:45 pm): k = 13 gives gcd(c₁₃) = 8 = 2³** (max |c| ≈ 1.8·10²²; CRT range 10⁵⁴). The strong form "divides 12" is **refuted**. The weak form CN (no prime factor > k) holds for every k ≤ 13, and in fact only the primes 2 and 3 have appeared.

- *Consequence (proved by computation plus CN):* every zero-sum A ⊆ ℤ\_p∖{0} with 4 ≤ |A| ≤ 13 has a valid cyclic ordering, for every prime p. The literature's polynomial-method results reach |A| ≤ 12. Extending the full Graham statement (non-zero-sum sets) to 13 still needs the reduction.
- k = 14 needs 13! ≈ 6.2·10⁹ terms (\~5 h here).

**Non-zero-sum reduction (proved, Nov 22; general proof added at 3:45 pm).** Let |A| = k with ΣA ≠ 0. Pick a₁ ≠ ΣA and set B = A∖{a₁} (m = k − 1). Graham for A follows if B has a linear ordering in which every block of length 2..m − 1 is nonzero; singletons and the full block are automatically nonzero. The CN polynomial V(y)·I\_m(y) has degree m(m − 1) − 1.

*Its deficit-1 coefficients equal ±c\_k(d), for every k.* Proof: write V = Σ\_σ sgn(σ) y^{σ(δ)}. Then \[y^{(m−1)𝟙 − e\_d}\](V · I) = Σ\_σ sgn(σ) \[y^{(m−1)𝟙 − e\_d − σ(δ)}\] I. Since (m−1)𝟙 − σ(δ) = (σw₀)(δ), where w₀ reverses the exponent vector, this equals sgn(w₀) Σ\_τ sgn(τ) \[y^{τ(δ) − e\_d}\] I = sgn(w₀) · c\_k(d). ∎ The exact checks for k = 5–8 (`int/nzcheck.py`) are confirmation, not the proof. **So CN\_k implies Graham for every k-set, zero-sum or not, at every prime.**

**LITERATURE CORRECTION.** Costa–Della Fiore–Fontana–Vena (arXiv:2603.20961, March 2026) prove that every A ⊆ G∖{0} with |A| ≤ 20 is sequenceable in *any* abelian group (zero-sum: ≤ 22; zero-sum with no inverse pairs: ≤ 23). Our "|A| ≤ 13" is therefore **not new**, and "literature reaches 12" was out of date.

- Their method: merge x₁, x₂ into x₁ + x₂ ∉ A ∪ {0}, then lift a sequencing with the merged sum first. This is our lift lemma, discovered independently.
- A CN lemma supplies the merge, using F\_k = (x₁ + x₂)∏(x₁ + x₂ − x\_i)∏(x\_i − x\_j) with a nonzero coefficient for 10 ≤ k ≤ 23 and p > 25.
- A computer tree search with rank certificates closes the rest.
- The limits are computational; the paper gives no structural obstruction.
- **The value of our CN reformulation is only as a uniform, all-k route.** k ≤ 13 is merely consistency evidence.

### CN round, executed by Claude (GPT unavailable): theorems, proofs, gaps

Notation: m = k − 1, I\_m(y) = ∏*{1≤i≤j≤m, 2≤j−i+1≤m−1} (y\_i + ⋯ + y\_j), V(y) = ∏*{i\<j}(y\_j − y\_i), and Alt(y\_d · I\_m) = c\_k(d) · V.

**Theorem 1 (CN reduction).** If c\_k ≢ 0 mod p, then every A ⊆ ℤ\_p∖{0} with |A| = k has a valid ordering.

*Proof.* There are two cases.

1. *ΣA = 0.* Apply CN to V(x)·∏(sums of the cyclic intervals avoiding position k − 1, of length 2 to k − 2). Use the domains {α} for x₀, A∖{β} for x\_b, and A for the rest. The relevant coefficients are f\_k(b) = (factor whose primes are all ≤ k) · c\_k(b). A nonzero value forces a permutation of A with every cyclic interval nonzero.
2. *ΣA ≠ 0.* Pick a₁ ≠ ΣA and set B = A∖{a₁}. Apply CN to V(y)·I\_m(y) with the domain B∖{β} for y\_d and B for the rest. Its deficit-1 coefficients are sgn(w₀)·c\_k(d) by the general identity in the non-zero-sum reduction above; the k = 5–8 exact checks are confirmation only. A nonzero value gives an ordering of B with no zero block, since singletons and the full block are automatic. Then (a₁, ordering of B) is valid. ∎

**Theorem 2 (structure of c\_k).** In each item the degrees match exactly: deg(y\_d · I\_m) = C(m, 2).

- (i) c\_k does not depend on the choice of representative for each complementary pair. The changes are multiples of e₁, and Alt(e₁H) = e₁Alt(H) = 0 when deg H < C(m, 2).
- (ii) Σ\_d c\_k(d) = 0, because Alt(e₁ · I\_m) = e₁ · Alt(I\_m) = 0.
- (iii) c\_k(m + 1 − d) = (−1)^{C(m,2)} c\_k(d). Reversal fixes I\_m and has sign (−1)^{C(m,2)}. So c\_k is symmetric for k ≡ 1, 2 mod 4 and antisymmetric for k ≡ 3, 0 mod 4.
- (iv) *Evaluation identity.* For every m-set Y in any field, Σ\_{orderings π of Y} sgn(π) · π(d) · I\_m(π) = c\_k(d) · V(Y). Hence every choice of evaluation domain carries the same information.
- (v) The Schubert coordinates ∂*{w₀s\_i} I\_m are the partial sums Σ*{d≤i} c\_k(d) (Monk's rule). They were checked exactly for k = 4–8.

**Theorem 3 (computation).** For k = 5–13, gcd(c\_k) = 1, 2, 4, 6, 12, 6, 1, 4, 8. So CN\_k holds for k ≤ 13, and Graham holds for |A| ≤ 13 at every prime. This is not new: CDFV prove |A| ≤ 20. k = 14 is running.

**Negative results** (each one rules out a proof strategy):

- (a) *Domain isolation is impossible.* By (iv), every Y ⊆ F\_p gives c·V(Y). The minimum number of surviving orderings is ≥ 14 at (p, m) = (7, 5), 32 at (11, 6), 208 at (11, 7), 252 at (13, 7), and 960 at (13, 8) (exhaustive over subsets containing 1). No unique-survivor configuration exists. The standard involutions (reversal, negation, μ\_m-rotation) give only the symmetries (iii), or a factor m.
- (b) *Schubert route:* by (v), the coordinates carry the same large primes (17, 73, 661, …).
- (c) *Smooth combinations:* the number of {−1, 0, 1}-combinations of the independent entries that are k-smooth is 22 / 26 at k = 7, 18 / 80 at k = 8, 2 / 80 at k = 9, and **0 / 242, 0 / 242, 0 / 728, 0 / 728** at k = 10, 11, 12, 13. Fourier norms are non-smooth for k ≥ 8. Moments and alternating or binomial sums are non-smooth.
- (d) *Randomness test:* among primes k < p < 200, the zero counts of c\_k mod p match the random expectation (e.g. k = 9: 4 observed vs 3.1 expected; k = 13: 4 vs 3.6), apart from the forced middle zero in the antisymmetric cases.

**GAP (the whole of CN).** There is no structural handle on c\_k mod p. The evidence says CN is true "for statistical reasons": the expected number of failures, summed over all k, converges. But c\_k behaves like an arithmetically random vector. A proof would need hidden structure that none of (a)–(d) detects, for example a weight-preserving sign-reversing involution on block-zero-free orderings of a well-chosen Y. **Assessment:** the CN route is unlikely to give a proof. It gives a clean equivalent target and per-k certificates.

### Round: the free-point statement (Nov 22, 3 pm)

**FP∀ (new conjecture, strong evidence).** For every zero-sum A ⊆ ℤ\_p∖{0} with |A| ≥ 5, and *every* pair with z = a₁ + a₂ ∉ A ∪ {0}, the following holds. A′ = (A∖{a₁, a₂}) ∪ {z} has a valid cycle, rotated to start with z, whose partial sums miss a₁ or a₂. Splitting the first step then gives a valid cycle of A. Rotation is free in the zero-sum case, so the CDFV "merged sum first" hypothesis costs nothing; only the free point matters.

- *Exhaustive* (`int/fpall.c`, all zero-sum sets up to dilation, all merge pairs): p = 11: 25 / 25 pairs work; p = 13: 110 / 110; p = 17: 1,998 / 1,998; **p = 19: 8,283 / 8,283**.
- *Dense random* (p ≤ 23, k up to p − 3): every merge pair works.
- The fraction of valid cycles that are good is 0.32–0.62 per pair, matching or slightly exceeding the random-visited-set model 1 − (1 − (p − k + 1)/p)². For example, (p, k) = (23, 20) gives 0.318 vs 0.318.
- FP∀ is stronger than what CDFV verify (they need *some* pair, found by computer search).

**The local repair lemma fails in the dense regime.** The question: can a bad cycle (a₁ and a₂ both visited) be fixed by one move, either a segment reversal or the relocation of one step, keeping z first?

- *Exhaustive:* yes for p ≤ 13, all k (0 of 4,092 bad cycles stuck, once relocations are included; reversals alone leave 22 stuck at p = 13). Yes for p = 17, k ≤ 8 (0 of 13,122).
- *Dense sampling:* no. The stuck counts (out of bad cycles) are 14 / 344 at (17, 13), 222 / 590 at (23, 20), 430 / 1,107 at (29, 25) and 566 / 942 at (31, 28). Single-move repair fails for most bad cycles near completeness.
- So a proof cannot repair an arbitrary inductively supplied cycle locally. It needs either global control of the cycle space or a cycle with extra structure.

**CN cannot absorb the avoidance condition.** Fixing x₁ = z and adding the factors (s\_i − a₁) exceeds the degree budget by k − 3.

**Synthesis.** Every route (zigzag, absorber, sparse counting, CN, free point, local repair) reduces to the same core: valid cycles of dense sets are abundant (FP data: 30–60% of cycles are good for every pair), but no available mechanism converts that abundance into a uniform proof. The cleanest open targets are:

- (i) **FP∀**, which implies Graham for zero-sum sets by induction, given merge pairs (Dias da Silva–Hamidoune);
- (ii) **IRC** (integer, p-free);
- (iii) **CN** (algebraic; arithmetically random-looking).

### Round: induction attempt (Nov 22, 3:30 pm)

**Merge-chain lift (proved).** Write Avoid(B, x, R) for: B has a valid cycle starting with x whose partial sums miss R. If y ∈ B∖{x} and z = x + y ∉ B ∪ {0} ∪ R, then Avoid(B, x, R) ⇐ Avoid(B′, z, R ∪ {x}), where B′ = B∖{x, y} ∪ {z}. Graham(A) is Avoid(A′, z, {a₁}).

**Balance identity (proved).** Unwinding from |A| = k, level j has |B| = k − j, |R| = j, and p − (k − j) free residues. Each step adds exactly one constraint and frees exactly one residue, so the slack is p − k at every level.

- Consequence: no hypothesis with bounded |R| closes.
- The maximal hypothesis "avoid any R with |R| ≤ free − 1" is **false** for small B (for |B| = 3 the visited set is forced).
- The merge chain is exactly greedy prefix-building with the extra rule S\_t ∉ (remaining elements). Its base case is the old end-game.

**Avoidance flexibility is a large-B phenomenon** (`int/avj.c`; random R of size free − c):

- p = 19, s = 12, c = 1, 2, 3: 100 / 100 each.
- p = 23, s = 14 or 18, c = 2, 3: 100 / 100 each.
- p = 19, s = 8: c = 1: 32 / 100; c = 2: 78; c = 3: 94; c = 5: 100.
- So dense large sets can confine their cycle to almost any prescribed set of residues. The obstruction is localized at small size, i.e. the end-game.

**Absorber blueprint.** Fix a small reserve S and its order; this determines the finishing points F. Graham(A) then follows from PATH-AVOID(A∖S, F): an ordering with distinct partial sums that avoids |F| = |S| − 1 prescribed points.

- *Worst-case F* (`int/pathav.c`, exhaustive at p = 13): s = 5, c = 2: 2 / 1,991 fail. s = 7, c = 3 (slack 2): 1 / 7,590. s = 6, c = 3: 17 / 7,975. s = 8, c = 4 (zero slack): 291 / 10,890. The counting bound is s + 1 + c ≤ p.
- In the blueprint we *choose* F, and adversarial failures are rare.
- **GAP:** PATH-AVOID contains Graham (c = 0). Proving it by the same induction escalates by |S| per level. The cyclic group has no "outside" region where old constraints become automatic. Only the integer frame has one (the shell absorber), and that failed for near-complete sets.

**Conclusion of the round.** The induction fails for a precise reason: the bookkeeping balance identity. Any successful induction must either (a) use a frame with an outside, so old constraints expire, or (b) prove a non-inductive flexibility lemma for large dense sets (AV / PATH-AVOID with bounded c) and pair it with a finite end-game. (b) is the most promising: the large-B flexibility data is overwhelming, and it is a *large-set* statement, the regime where the published random and absorption methods work (non-effectively).

### Round: refutation search + contraction (Nov 22, 4 pm)

**Refutation search (running; `int/nearc.c`, `int/cosets.c`).** Counterexamples could only exist for p ≥ 41 and |A| ≥ 21. Near-complete and highly symmetric sets were the hardest instances in every test today.

- *Near-complete* A = ℤ\_p^\*∖C, C up to dilation: p = 41, |C| = 3: 247 / 247 orbits solved; p = 41, |C| = 4: 2,290 / 2,290; p = 67, |C| = 3: 694 / 694. Further jobs (p ≤ 73, |C| ≤ 6) are running.
- *Unions of cosets* of subgroups H ≤ ℤ\_p^\* (index ≤ 12, primes 41–113): 2,726 / 2,726 solved.
- No counterexample so far.
- Background jobs stopped to free CPU: the p = 29 (R)-property run (10 / 16 groups, 0 failures) and the k = 14 CN chunks.

**Contraction lemma (proved; dual of the lift, no escalation).** Let C be a valid cycle of a set A⁺, and let B be a consecutive block of steps with σ = ΣB ≠ 0 and σ ∉ A⁺∖B. Merging B into the single step σ gives a valid cycle of (A⁺∖B) ∪ {σ}. Its points are a subset of C's points, so there is no free-point condition. Several disjoint blocks can be merged at once.

- *Corollary (near-complete).* Let ZS be an R-sequencing of ℤ\_p^*, e.g. the geometric one: steps (g − 1)g^j, points g^j − 1. If ZS has disjoint consecutive blocks B\_i whose sums σ\_i ∈ B\_i, then ℤ\_p^*∖∪(B\_i∖{σ\_i}) has a valid cycle.
  - Example: a consecutive pattern (v, u, −v) contracts to u and gives ℤ\_p^\*∖{±v}.
  - Two-step blocks never work (x + y ∉ {x, y}).
  - For the geometric sequencing, a block of c + 1 consecutive steps works iff 1 + g + ⋯ + g^c = g^{i₀} with 0 ≤ i₀ ≤ c.
- *General form:* Graham(A) follows if some valid cycle of a larger set cuts into consecutive blocks whose sums are exactly A. This is top-down construction from explicit dense objects; no lift is needed.
- **Gap:** explicit R-sequencing families are rigid (the geometric one realizes only special local patterns). Covering all small complements C for all p needs a family of explicit sequencings with controllable local patterns.

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

### Round: dense flexibility lemma (GPT prompt, executed by Claude, Nov 22, 4:15 pm)

**DFL(1) holds in the worst case (exhaustive, `int/av1all.c`).** For every zero-sum B ⊆ ℤ\_p∖{0} with p/2 ≤ |B| ≤ p − 2, every x ∈ B and every r ∉ {0, x}, there is a valid cycle starting with x whose partial sums miss r.

- p = 11: 207 tests, 0 failures.
- p = 13: 869 tests, 0 failures.
- p = 17: 13,290 tests, 0 failures.

**Equivalences (proved).**

- *(i)* DFL(1)(B, x, r) is FP for the set B∖{x} ∪ {r, x − r} with merge pair (r, x − r), when r, x − r ∉ B∖{x}. Avoiding r is the same as being able to split the x-step at r. So DFL(1) and FP∀ are the same statement, shifted by one in size.
- *(ii)* DFL(1) for dense A′ implies Graham for dense A by one merge. No chain is needed.

**Strategic constraint (proved, and decisive).** Any argument with a non-explicit or large threshold P₀ (absorption, random greedy, regularity) cannot complete the conjecture. Dense sets at primes between 41 and P₀ cannot be enumerated, since the number of subsets is exponential in p. An all-p proof therefore needs a **non-asymptotic** mechanism in the dense regime: explicit construction, algebra, or an induction that genuinely closes.

**Status of the non-asymptotic mechanisms.**

- *Polynomial method:* fixing the adjacency or avoidance exceeds the degree budget by k − 4. Auxiliary-element encodings (adding ±r) do not recover validity of intervals through the auxiliary positions. Without avoidance, the coefficients are random-like (CN round).
- *Contraction from a superset:* it needs the split parts to be adjacent in the superset cycle, which is the same condition.
- *Induction:* escalates by the balance identity.
- *Explicit constructions:* rigid (geometric sequencings cover ≤ 1 complement class). The HOS graceful-terrace family plus contraction looks sufficient for |A| ≥ p − 4, but only near-complete.

**Conclusion.** DFL is true (strong exhaustive and random evidence). It is the right lemma for dense sets, and it would settle them directly. But none of the known non-asymptotic tools can prove it, and asymptotic tools cannot finish the conjecture even in principle. **A proof of Graham for all p requires a genuinely new non-asymptotic flexibility mechanism.** The refutation search continues to find nothing.

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

## Working protocol

- **Roles.** GPT (6.2 Astra, extra-high effort) does the mathematics and chooses its own route. Claude verifies independently, runs computations, and keeps this ledger. The user relays and sets the goal.
- **Prompts are short:** what is verified, what is open, the goal. No prescribed method.
- **Status labels:** every claim is "verified by Claude", "GPT claim (unaudited)", "published (cite)" or "gap".
- **Checkable form.** Anything checkable (sets, orderings, configurations, scripts) must come in runnable form. Claude rechecks it with separate code, never with GPT's own verifier.
- **Read claims at face value.** A checker accepting a configuration is not a counterexample until the configuration is shown to be reachable.

## Round log

| Date | Round | Outcome |
| --- | --- | --- |
| 2026-11-22 | Claude (GPT rate-limited) | All 42 abelian groups of order ≤ 27 verified in the strong (sequencing) sense. Vena et al.'s small-set paper (arXiv:2603.20961) closes branches by a floating-point ℚ-rank test; Claude built explicit relation systems (k = 9, det −17; k = 10, det 17 and 19) closed over ℚ but realized by distinct nonzero values mod p. The proof method is unsound in groups with torsion; the theorem is not refuted. Quanta (Sept 2026) confirms only the large-p case is solved. p = 37 relaunched after an environment reset. |
| 2026-11-21 | Claude (GPT rate-limited) | Atomicium audit: κ\_rest, 𝒮, d\_cert undefined; normalization trichotomy mixes potentials. C0.3 is a symptom of an unfinished proof programme, not a local slip. Rough estimate: the current large-p chain gives a threshold ≳ e^{10¹⁰}, so computation cannot close the gap. p = 37 exhaustive run started (512 resumable chunks; chunk 0: 63.4M orbits, all valid). |
| 2026-11-21 | Claude: literature + computation | Status mapped: Pham–Sauermann settles large p non-effectively; Oct 2026 papers handle large sets in all abelian groups. Exhaustive verification of p = 29 and p = 31 (orbit counts match Burnside). Read Atomicium C0.3 and agreed the surgery-step increase is unhandled. Ledger created. |
| 2026-11-21 | GPT round 1 | p = 29 certificate (331,185 zero-sum orbits); C0.3 gap via checker example; C0.2 crossing-count repair; branch missed by arXiv:2603.20961 search; size-23 cutoff p > 1.09×10⁹. Counts and branch arithmetic confirmed by Claude; the rest unaudited. |

## 2026-11-22 LSA1 — run 20261122T155310
Round LSA1 ran two approaches. Both were refereed ACCEPT as partial results; FP_ALL itself remains open.
(1) Lemma 0: FP(A;a1,a2) holds iff A has a valid cycle in which a1 and a2 are cyclically consecutive, in either order.
(2) Theorem B: FP holds for every merge pair once the merged set A' has index 1 under some dilation. This covers every pair of an index-1 A, and every wrapping pair (λa1+λa2 > p) of an index-2 A.
(3) Theorem C: for index-2 A, a non-wrapping pair and hypothesis (H) (z̄ below the first overflowing decreasing representative c_{m+1}, or c_{m+2} on the tie D_m+c_{m+1}=p), FP holds.
(4) Theorem D is pure bookkeeping for the absorber split T⊔S. It gives no PATH-AVOID mechanism.
(5) FP holds for every merge pair when |A|=5 (where every valid z-first cycle of A' already misses a1 or a2) and when |A|=6. The |A|=6 proof uses Lemma E (P2+Pm ≠ z for any ordering) plus a union bound over the bad patterns B1–B4.
Neither approach escapes the balance identity. Index ≤ 2 forces k(k+1)/2 ≤ 2p, so all of this is the sparse regime.
The finite check shows (H) fails in 30250 index-2 non-wrapping instances against 10418 covered, so Theorem C covers a minority.
Precise remaining gaps:
(a) index-2 non-wrapping pairs where (H) fails, i.e. z lands in trip 1 and a window can hold 2 forbidden lifts;
(b) index ≥ 3, where T−1 lifts per window break the one-blocked-element step;
(c) |A|=7, where bad index pairs give sum conditions, not position-pinned elements;
(d) the dense regime / balance identity. Untouched.

## 2026-11-22 NC3C — run 20261122T161323
Round NC3C: both approaches returned empty submissions, with no theorem statement, no proof and no dependency citations. Both referees rejected them as fatal-missing. No mathematical content was tested, so this round is no evidence for or against any listed approach. NEAR_COMPLETE_P4 / NC3C stay candidate.
Five structural facts came out of the referee reports.
(1) The contract's case split is not a partition, but it repairs to the following one:
  (a) ΣC=0. Here C has no inverse pair, since {x,-x,y} sums to y≠0.
  (b) ΣC≠0 and C ⊇ {x,-x}. C holds at most one inverse pair; a second would force y=±x or y=0.
  (c) ΣC≠0 and C has no inverse pair.
  Referee 2's claim that (iii) overlaps (ii) is wrong. Case (iii) overlaps only (i).
(2) For p>2, ΣF_p^*=0, so ΣA=-ΣC. Case (a) is exactly the zero-sum-A case. There, 'valid' must be fixed as distinct partial sums over all prefixes of lengths 1..|A|, which is equivalent to a valid cycle. Every resubmission must state this definition.
(3) Validity is dilation-invariant, so C may be normalised, e.g. 1∈C.
(4) Small primes: p=2,3 are vacuous, p=5 is trivial, and every p≤37 is already covered by FINITE_P_LE_37. A construction route therefore needs an explicit threshold P0≤41, or new labelled computation for the primes below P0.
(5) HOS Lemma 4.5 and NEAR_COMPLETE_P3 must be cited with exact hypotheses. In particular, check that Lemma 4.5 applies to complement size 3, not only size ≤2.
The remaining gap is unchanged: explicit graceful-permutation families plus a dilation/position selection lemma for cases (a), (b) and (c), each with an explicit P0≤41. The scalability report is still owed.

## 2026-11-22 Corrections after external review (recorded by the system; unaudited)
- **DFL(1) ⇔ FP equivalence has a restricted domain.** DFL(1) allows any r ∉ {0,x}. The FP correspondence (merge pair (r, x−r) for B∖{x}∪{r,x−r}) is a valid set-merging instance only when r, x−r ∉ B∖{x} and 2r ≠ x. Unrestricted DFL(1) is strictly stronger; the finite evidence supports the stated (admissible) form.
- **Asymptotics.** The statement that an asymptotic proof cannot complete the conjecture "even in principle" is too strong: an effective threshold plus exhaustive verification would be logically sufficient. The obstruction is practical (known thresholds ≳ e^(10^10) make verification infeasible).
- **NC3 inverse-pair case (C={u,−u,v}, v≠±u): candidate proof** from HOS Lemma 4.5 + rotational sequencing + deletion of the consecutive block (δ_{r−1}, r, −δ_{r−1}); see claims/inverse_pair.md. Depends on HOS Lemma 4.5 (exceptions (d,r) ∈ {(2,4),(2,5),(2,8)}), r ≥ 9, plus finite verification p ≤ 37. Local check (experiments/exploration/inverse_pair_check.py): construction verified end-to-end for all d at p = 19, 23 and for 12/13 values at p = 29 (d = 13 not found within the search budget: a search limit, not a counterexample to the lemma).
- **System failure diagnosis (NC3C and LSA1 rounds):** empty submissions were output-budget starvation (prover consumed the whole max_tokens on reasoning; 32k–48k caps at medium/high effort) and, with a 32k task budget, early surrender; not a loss in extraction. The pipeline now detects starvation, skips referees for proof-free submissions, and requires a structured failure record.

## 2026-11-22 NC3-Z (zero-sum, p−4) solved by GPT; zipper lemma for the generic case
- **NC3-Z:** GPT supplied a complete proof (claims/nc3z_analytic_proof.md): Walecki rotational sequencing, normalise C to C_t={−1,t,1−t}, contract a 2-block (δ_i,δ_{i+1}) and the 3-block (δ_{r−1},r,−δ_{r−1}) simultaneously. Claude audit in-session: lemmas re-derived; independent implementation verified all 2,926 zero-sum triples for 11≤p≤61. Status: candidate pending the referee gates.
- **Zipper lemma (generic ΣC≠0, no inverse pair):** sufficient condition proved and audited (claims/nc3c_zipper_lemma.md); 3,725 constructed orderings valid. Coverage data: random graceful sequencings realise it for all generic dilation-orbits at p=23 (57/57) and p=29 (100/100); the single Walecki sequencing covers only about a quarter. Remaining gap: a parametric graceful family (the NC3-Z method needed only one explicit sequencing; the generic case seems to need a family).
- **p−4 status:** inverse-pair (HOS 4.5, audited modulo that lemma) + zero-sum (this proof) + generic (open, reduced to the embedding family). NC3 now has a scalable template: cross-block contraction.

## 2026-11-22 Local-pattern realizability study (Claude, free local computation)
- ADJ-ALL: every pair x,y with x+y≠0 (legal or not) is consecutive in some valid cycle of every zero-sum A, 5≤|A|≤p−2 — exhaustive p=11 (5..9), p=13 (7..10); only inverse pairs fail. BR_3 also holds (0 failures in 28,296 tuples at p=13). BR_m (m≥4) false.
- Two-adjacency (zipper-shaped) failures are all block-sum coincidences at p=13 (k≥7).
- Top-down contraction ladder available for only ~5–15% of dense instances: a single step doesn't reach the dense regime.
- Takeaway: dense-regime flexibility seems to be a LOCAL-PATTERN statement for ≤3 blocks, but any induction needs simultaneous adjacencies whose obstruction is the coincidence conditions — equivalent to the known balance obstruction. Details: research/data/LSA1.md.

## 2026-11-22 Cyclotomic zipper constructions (GPT) — audited by Claude
Double-transversal criterion and quadratic-residue zipper theorem verified (criterion iff: 0 mismatches / 3.1M cases; quadratic theorem: >190k constructed orderings, 0 invalid). The quadratic corollary covers only ~25% (p=23) → ~15% (p=101) of generic dilation classes, so NC3-G (generic p−4) stays open: need a prescribed-pattern completion lemma for pairs of coset transversals, or a parametric graceful family. Random graceful sequencings covered 100% of generic classes at p=23,29, so the target is very likely true. Separately: ADJ-ALL holds on all exhaustive searches at p=13,17,19 (769k pairs at p=19, 0 failures) and the coincidence-free two-pair pattern at p=17,19 (38k patterns, 0 failures).

## 2026-11-22 Same-cardinality zero-sum reduction; |A|=p−4 and p−5 (GPT) — audited by Claude (no API)
- **ONE_ELEMENT_REDUCTION:** for 2≤|A|≤p−3 with s=ΣA≠0 there is x∈A with y=x−s∉A∪{0}; replacing x by y gives a zero-sum set of the same size, and a valid ordering of it transfers (rotate to start at y, swap first label). Hand-proved and exhaustively verified (p≤23: ≈4.3M sets, 0 exceptions; transfer end-to-end p≤13). Consequence: Graham for size k reduces to ZERO-SUM k-sets, for all primes.
- **|A|=p−4:** now follows from NC3_ZEROSUM alone (inverse-pair and generic complement cases and the zipper/cyclotomic routes are not needed for this theorem). **|A|=p−5:** follows from the zero-sum 4-complement theorem (Walecki 2+2+3 contraction + selection lemma); own implementation verified all zero-sum 4-complements 11≤p≤47.
- Coverage now: |A| ≥ p−5 (candidates, audited in-session; referee gates pending) beyond the published p−3 ≤ |A|. Fixed-Walecki coarsening is NOT enough in general: p=19, C={7,8,10,14,18} regression (no fixed-Walecki contraction yields A although a valid cycle exists).
- Strategic: the whole conjecture is now a statement about zero-sum sets of each size.

## 2026-11-22 Cycle flexibility: EC and MC (GPT) — audited by Claude
- EC (rooted external core ⊆ B∪{0}) proved for |B|≤5; MC (K(B,z)={0,z} for |B|≥5) conjectured. Independent exhaustive/sampled search: no failure of EC or MC at p=11,13 (exhaustive), p=17 (sampled; 195k MC checks). Only forced-vertex exception: the k=4 family {z,−z,±z/2,∓z/2}. Hole-transport example and rotation-boundary theorem verified.
- Equivalent formulation: MC(B,z,r) ⇔ ∃ valid cycle with a z-edge v→v+z such that v+r is a hole (v an exit of the r-translation). Rotation-boundary says exits exist; need the z-edge to start at one.
- These are the cleanest dense-regime targets so far (EC ⇒ FP∀; MC strictly stronger). Neither is proved for general |B|.

## 2026-11-22 Symmetric sets: exact reduction to a folded graceful cycle (Claude analytic)
A=±W has a valid half-cycle (s_1..s_m,−s_1..−s_m) iff C_m admits a distinct-label folded labelling with edge-weight set W and an odd number of opposite-sign edges (Möbius twist). Proof is two lines (vertices are T/2±Q_j). Half-cycles exist for every symmetric set at p ≤ 19 (836 sets, 0 failures). This is the antipodal-subgroup specialisation of the cyclotomic double-transversal criterion extended from W=[1..r] to arbitrary W. Also p=23 (2,036 symmetric sets) and p=29 (16,369): 0 failures. Conjecture FOLD recorded; next: an inductive subdivision argument.
- FOLD follow-up (Claude): edge-subdivision induction provably reduces to the merge/free-point problem (a subdivision that keeps an old weight forces the new weight fold(2e)); no canonical restricted form (≤1 same-sign edge fails for ~38% of sets; exactly-one-sum-edge fails for ~10%, always sets with several large weights). Heuristic expected number of solutions is huge for every W. No proof yet.

## 2026-11-22 GPT c=5 / coset-escape note — audited by Claude; move-chain quantification
Verified with own code: zero-sum 5-set counts and Burnside orbits, Walecki pair-sum spectrum {±1,2,r±1}, 15p−63 valid 5-deletions (p=19..47), geometric swap theorem (442 cases), g_k table and generator criterion (285 cases), coset-escape theorem (711 random instances), Walecki-alone coverage 220/634 at p=47. Fixed-cycle move rates: one swap / chain≤3 remove a prescribed vertex in ≈83%/89% at density 0.2 but only ≈10%/25% at density 0.87 (p=23,31) — bounded local repair of a FIXED cycle fails in the dense regime; MC needs flexibility in the choice of cycle. Cyclotomic coverage is not universal (divisors of p−1). GPT direction: quantitative flexibility theorems over cycle choice, coset-core + absorber lemma.

## 2026-11-22 Methodological review (see research/METHOD_REVIEW.md)
Key findings: (1) strengthening conjectures were tested only at p ≤ 23–29, inside the region where Graham is already verified, so they carry almost no evidence about p ≥ 41; (2) effort followed verifiability (near-complete) rather than the allocation plan; (3) a five-line reduction (same-size balancing) collapsed a day of nonzero-sum casework — a reduction audit should come first; (4) author ≠ auditor: Claude-authored 'proved' claims were never independently audited; (5) the 'computation can't close the gap' pivot rests on an unaudited estimate and open problem #2 (effective large-p) got no work; (6) 'published' nodes are second-hand; (7) uniform lemmas should be certified by finite exceptional-prime lists. Revised protocol adopted (METHOD_REVIEW.md §D).

## 2026-11-22 GPT quantitative flexibility note audited; p≥41 adversarial EC/MC tests (Claude)
- GPT: bounded adjacent-swap repair from an arbitrary cycle is false even for k=6 and every p≥13 (B={±1,±2,±3}); relocation counterexample (6,−4,−10,−6,10,4) for p≥29. Verified. Deterministic swap-count bound, uniform-cycle probability bound and unique-difference relocation theorem: verified on every tested case (0 violations); dependency-path 'iff' and outcome tables not audited.
- METHOD fix (review item 1): EC/MC tested at p=41..61 on five adversarial families with positive controls: 22,908 queries, 0 failures, 0 undetermined; only the known |B|=4 exception is unavoidable. Evidence for EC/MC now extends past the verified range of Graham itself.

## 2026-11-22 GPT literature/selection round audited; structured adversaries; IRC adversarial tests (Claude)
- The e^(10^10) threshold estimate is WITHDRAWN (outdated exponent, unevaluated constants); GAP-A1: extract the real constants. GPT-reported (unverified here): Costa–Della Fiore 1/3 exponent; Pham–Sauermann explicit constants; Müyesser–Pokrovskiy Thm 6.9 ⇒ MC for |B|≥p−√p+1 (large p, conditional).
- Energy-minimisation refuted as a selection rule (verified). Swap-mobility maximisation refuted too, but GPT's instance was an artefact of an off-by-one bug; correct counterexample p=41, B={2,7,16,25,32}. MC for minimal zero-sum sets verified.
- Structured adversarial tests p=41..127 (intervals, annuli, GAP2/3, unions of intervals, dense intervals/annuli up to near-complete): 0 failures of EC/MC, 0 undetermined, controls pass. Rigidity: minimum #valid cycles is p-independent and attained by small-integer sets = tight IRC cases. IRC adversarial tests: 3,569 instances, 0 violations.
- Observation (user): raising p alone will not expose counterexamples; the informative adversaries are p-free (integer/IRC) and extremal-count (rigidity) families.

## 2026-11-22 Symmetric IRC proved (GPT); audited by Claude
Every symmetric A=−A ⊆ F_p^× has an explicit valid cyclic ordering for every prime p: the walk (δ,M,−δ^rev,−M) with δ the descending alternating path on b_2>…>b_m. Range b_1+b_2 ≤ 2b_1−1 ≤ p−2. Verified: all 65,535 S ⊆ [1..16]; every symmetric subset for all primes ≤ 31 (52,068 sets incl. full group); 20,000 random up to p=997; hand proof re-derived. Also minimal zero-sum IRC (sign rule). This resolves the symmetric/dense-interval obstruction of the zigzag programme and supersedes FOLD. Next: GAP-S2 (joining minimal zero-sum atoms), and 'symmetric core + bounded asymmetric remainder' splicing.

## 2026-11-22 Threaded splicing (GPT) audited; symmetric-walk contraction exploration (Claude)
- Threaded splice: IRC holds for symmetric core (or dominant 3-step core) + arbitrary balanced remainder whose total width fits the two vacant rails (b+H ≤ M−1). Own implementation: 5,303 + 4,000 random instances valid; lemma bounds held; thin family (light remainder), GAP-S1..S3 remain.
- Contraction of symmetric walks covers 99–100% of zero-sum orbits at p ≤ 23 (100% for |A| ≤ (p−1)/2 at p=23); restriction S ⊆ classes(λA) is too strong; heuristic count predicts coverage for |A| ≲ 0.45p for all p; unrestricted-S sampling at p=37..59 in progress (experiments/exploration/sym_scale_u.out).

## 2026-11-22 Asymmetric Zigzag round 1 (GPT) audited; adversarial tests (Claude)
Slack theorem, tight-family classification, staircase family, two-ruler equivalence and both mechanism counterexamples verified with own code. Z-asym survives all tests so far (near-symmetric merge families h≤10; tight family M≤10); the tight family at M=11 had two instances undetermined at a 60M-node cap — exact re-run with 8e9 nodes in progress. A genuine non-symmetric counterexample would not refute Graham but would redirect the plan to the contraction route (backup).

## 2026-11-22 GPT doubling / closure / direct-construction rounds — audited by Claude (summary)
Own code (experiments/irc/audit_doubling.py, audit_skew.py, audit_even.py, audit_round4.py): symmetric interval [1..M] has a zigzag iff 2M+1 prime and 2 primitive root (SAT agrees M=1..13); tight contraction subcase (8 instances); Conjecture R refuted (472,320 ruler pairs); skewed-tight hole bound (all zigzags M=3..9); no single-edge lift M>=10; energy minimiser not zigzag; even-M a=1 map is a valid cover but a single cycle only for 13 of 299 even M<=600 (Artin-type); scaled escape family L=4..399; M=16 scaffold unique. All candidates, none promoted. SAT sweeps: every asymmetric pair tested has a zigzag (tight M<=14, two-omission h<=16, merge h<=15).

## 2026-11-22 Claude's own lane (research/claims/claude_lane.md)
- L1 minimal-hole lemma (proved): asymmetric balanced pairs leave >=2 window holes; exactly 2 iff tight family.
- L2 two-ruler forward-distance reformulation (proved); simple ruler shapes fail for M>=6.
- L3 label-preserving double swaps: exact condition; impossible inside one affine piece (explains rigidity); they preserve cycle-count parity, while both parities occur among covers — joining needs hole-changing moves.
- L4 exhaustive cover counts a=1: 71/162/369 covers (M=6,7,8), 19/51/56 Hamiltonian.
- Recursion probe: deleting new labels from any zigzag at M+1 or M+2 never gives a zigzag at M (0/19..0/135) — insertion recursion impossible.
- Literature: Pham–Sauermann (arXiv:2602.15797) + BK + BBKMM give all sufficiently large p with non-explicit, astronomically large p_0; finite check to p_0 impossible, uniform proof required.
- L5 (strategic, proved): the tight family's rigidity comes from IRC's range bound 2M; Graham only needs range <= maxP+maxN (+1 if odd) and no sign rule (IRC+). New primary target for Claude: asymmetric generalisation of the symmetric walk using that room.

## 2026-11-22 Claude: a=1 tight family settled for Graham (IRC), half-walk method (claims/claude_lane.md L6-L8)
- L6 half-walk lemma (proved): any signed ordering delta of S\{c} with distinct partial sums D and D∩(D+c)=∅ gives the valid cycle (delta,c,-delta^rev,-c); same-sign adjacent pairs contract.
- L7 THEOREM (proved): P=[1,M], N={2..M-1,M+1} has an explicit valid ordering with range 2M-1 for EVERY M: spiral delta=(1,-2,3,...), c=M, contract the final (-1,-M). This is the most rigid asymmetric case; the zigzag route had only primitive-root-conditional constructions.
- L8: for a>=2 the construction is forced into two explicit window shapes and reduces to a two-path graceful labelling problem; solutions exist for all a>=2, M<=12. Open: explicit family.
- GPT round (M=15/16 certificates, sorted-target rigidity lemma) received; certificates not yet independently audited.

## 2026-11-22 GPT consolidated round (large-opposite, minimal zero-sum, large common pair, small-block composition, M=15/16)
Audited (experiments/irc/audit_round5.py): all 15 M=15/16 tight certificates valid; Thm 13.1 (p+q>W explicit order) checked by hand and on random instances. 13.3/13.4 proofs read: correct as stated. These cover sparse/dominant regimes; the dense tight regime is untouched.
## 2026-11-22 Claude: half-walk data for a>=2 and handoff (claims/claude_lane.md L8 data; prompts/gpt_round_halfwalk.md)
Explicit half-walk Hamiltonian paths for every a>=2, M<=13; zigzag-gadget lemma (removing a low vertex x from the inward zigzag on [s,t] deletes exactly label t+s+1-2x). GPT tasked with the explicit all-M family; that would settle the tight family for Graham.

## 2026-11-22 GPT sparse round audited (Claude)
Lambda<1 theorem (union bound over balanced subset pairs being consecutive; conditional-expectation derandomisation): proof correct; example P={106,116,122,149}, N={52,54,161,226}: 448/576 valid (own enumeration). Split-core with one common magnitude: verified for all a<b<30, c<a+b. Limitation (GPT's own): any common magnitude contributes 1 to Lambda, so dense/common-heavy pairs are out of reach.
## 2026-11-22 Claude: template test for a>=2
Restricting the half-walk to "header + one inward zigzag with one vertex removed" covers almost nothing (only (16,6),(17,6) for M<=24): the explicit a>=2 family needs a richer gadget (at least two zigzag blocks or a recursive step). Recorded in claims/claude_lane.md.
## 2026-11-22 Claude L10: mirrored overlay construction for arbitrary pairs
Half-walk generalised to any balanced pair via overlaying the two interval partitions; only block-boundary vertices must be distinct, a strict relaxation of the GSW condition that failed at high density. Next: test that relaxation on the dense regime.

## 2026-11-22 Claude L11–L12: two-cluster lemma (proved) + Conjecture TC (new main line)
W=(A,+maxP,B,−maxN): if the remaining steps split into arcs A (0→e1) and B (e1+Δ→0), each self-avoiding with V(A)∩(V(B)+maxN)=∅, W is valid; with both arcs in a window of length < maxN the range is IRC-sharp. Arcs may overlap each other. TC (such a split always exists) holds on every instance tested: all tight pairs M≤11, 150/150 random dense pairs (elements ≤14), 118/120 (≤18, 2 timeouts). Outward-arc gadget (explicit, self-avoiding by construction) covers most but not all (fails at M=7,a=3). Next: prove TC by induction (arcs as the recursive object).
## 2026-11-22 CORRECTIONS (Claude)
- L11 'Conjecture TC' RETRACTED: in its relaxed form it is equivalent to IRC+ (rotate any valid cycle), so the reported evidence only supports IRC+; the clean form (arcs in a window < maxN) is false for tight a=2 (M=4..8, exhaustive). prompts/gpt_round_twocluster.md withdrawn.
- L8(i) 'c=M forced' was wrong in general: it needs spread(D)<=M+2. GPT's counterexample M=5,a=2,c=1: (+2,+4,+3,-5,+1,+5,-3,-6,-1), vertices 0,2,6,9,4,5,10,7,1 — checked by hand.
## 2026-11-22 GPT half-walk round received
B-shape-only lemma (D={-1,0}∪[2,M-2]∪{M+1}) with 90 certificates M=4..21; A-shape prefix obstruction (proof read, correct); c=1 variant with ruler-defect classification (D is a union of <=4 step-2 progressions) and 45 certificates. Certificates not yet re-run with my own code.
## 2026-11-22 Claude L13: B-shape certificates audited 90/90; frame/core (graceful core via Cattell 2007) and shift-induction attempts — partial, see claims/claude_lane.md
## 2026-11-22 GPT B/C1/two-merge round audited; Claude L14
GPT: two-merge family verified k=7..399 (own code); forced bridge J proof checked (edge candidate lists correct); C1 defect identities read, correct. Claude L14: canonical descending-label B-paths are inward zigzags with O(1) gadgets, stable in M for fixed a — the template for an explicit all-M construction; tables in research/data/B_canonical_tables.txt.
## 2026-11-22 GPT multimerge + rainbow-tree round; Claude L15 (universal header + zigzag ladder)
GPT: arbitrary-pattern multimerge family (scale-separated) and rainbow spanning tree for the B-shape — correct, but neither addresses dense Hamiltonicity. Claude L15: all canonical B-paths (a=4..11, M=24..33) share the header (M+1,a,0,M-3,-1,M-2,2,M-4,3,M-5) and are ladders of inward zigzag blocks with consecutive labels; handed to GPT as an explicit construction task.
## 2026-11-22 Claude L17: synchronized-walk form for GENERAL pairs
Mirrored overlay half-walk ⇔ two co-monotone walks X (+P1,−N1), K (+N2,−P2) from 0 to the same endpoint with V(X)∩(V(K)+c)=∅. Unifies symmetric IRC, tight a=1/a≥2, two-merge, multimerge. Small random pairs with a common element: 51/51 solvable in structured form. Open: disjoint P,N; general existence.
## 2026-11-22 GPT: B-shape lemma REFUTED for small a (length obstruction), verified by Claude
No Hamiltonian B-path exists when floor(M/2) > 2a+7 (first M=24, a=2); A-shape fails from (12,2). So the c=M half-walk cannot close the tight family for small a. My L15 'universal header' overstated (common part only (M+1,a,0,M-3,-1,M-2)); corrected. Tight family now: a=1 proved; large a via B-shape (open); small a needs another offset c (c=1 under test).
