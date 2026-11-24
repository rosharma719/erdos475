# Rooted-window IRC (G*), the max-root lift, and the tight family (Claude, 2026-11-24)

Code and data: `experiments/exploration/rooted_window/`. Programme C (IRC).

## Definitions
A balanced pair (P, N) consists of finite sets of positive integers with ΣP = ΣN. P ∩ N may be nonempty.
For r ∈ P, **G(P, N, r)** means: some ordering of +P ∪ −N starts with +r, has distinct partial sums, and has every vertex in the window (−max N, max P].
G implies IRC for (P, N), since range ≤ max P + max N − 1.

## G*: conjecture with exact finite evidence
**Conjecture G\*.** G(P, N, r) holds for every balanced pair and every root r ∈ P, except for (P, N, r) in the explicit list E:
- (E1) P = N = {x, y}, r = min.
- (E2) |P| = |N| = 3, P = {r, c−r, c}, N = {b, c−b, c}, with r < min(b, c−b), or P = N and r ≠ c.
- (E3) P = N = d·{1, 2, 3, 4, 5}, r = d.

**Evidence (`anyroot.c`).** Every balanced pair with values ≤ 15 and |P| + |N| ≤ 15: 9,679,849 instances and 63,251,161 (instance, root) pairs.
- There are 297 failures, and every one lies in E (`G_failures_V15.txt`). Whether every member of E actually fails was not checked.
- Rooting at r = max P has **0 failures**, including when max N > max P.

So the root-at-max statement H (G(P, N, max P) for all pairs) has no counterexample in the data.
- The zigzag analogue Z1 (`integer_range.md`) fails on an infinite family. Dropping the zigzag rule removes every failure.
- H covers the tight family (it implies IRC for it). At M = 11 the tight family was previously left undetermined after 60 million search nodes.

## Lemma (max-root lift), proved
Let p1 = max P, y ∈ N with y ≠ p1, and t = p1 − y.

**Case t > 0.** Suppose t ∉ P, and set P′ = (P ∖ {p1}) ∪ {t}, N′ = N ∖ {y}. If G(P′, N′, t) holds, then G(P, N, p1) holds.

*Proof.* Replace the first step +t of the smaller cycle by the two steps +p1, −y. The new vertex list is 0, p1, followed by the old vertices from t onward.
- Every old vertex is ≤ max P′ < p1, because max P′ ∈ {t, p2} and t < p1. So p1 is a new vertex.
- Every old vertex is > −max N′ ≥ −max N, because N′ ⊆ N.
- The multiset of steps is exactly +P ∪ −N. ∎

**Consequence.** Assume G\* for smaller instances.
- G(P, N, max P) follows whenever some admissible y exists (t > 0, t ∉ P, and the reduced instance not in E).
- For values ≤ 13, no admissible y exists in 36,877 of 1,300,819 instances (2.8%). These include all singletons and many symmetric pairs (`stuck_pos.py`).
- The case t < 0 needs the negative-root window [−max N, max P), which differs at the endpoints. It is not used here.

**GAP (the open step).** The reduced root t is generally a *middle* element of P′, not its maximum. So an induction on G\* must also prove G at middle roots. For a middle root the first vertex r is not extremal, and the same merge-the-first-step lift gives no freshness guarantee.
An induction would need (i) a lift that produces middle roots, and (ii) a direct argument for the stuck instances where no admissible y exists. Neither is known.

## The tight family reduces to a rooted symmetric problem (proved)
The tight pair in negated form is P = [1, M+1] ∖ {a, b}, N = [1, M], with a + b = M + 1 and 2 ≤ a < b.
Apply the lift with y = b: t = a ∉ P. This reduces the problem to G(S, S, a) with S = [1, M] ∖ {b}, a symmetric set rooted at a middle element.

**Computation (`tightsym.c`).** G(S, S, a) found for every 2 ≤ a ≤ M/2 and M ≤ 16, within 4.9·10^5 nodes per case. Previously M = 11 was undetermined at 6·10^7 nodes.

**Half-walk template (proved sufficient).** Let δ be a signed ordering of [1, M−1] ∖ {b} that starts with +a, with vertex set D (D_0 = 0). Suppose:
- the D_i are distinct, 1 ∉ D, M ∉ D, M+1 ∉ D, and D ∩ (D + M) = ∅;
- {0, M+1} ∪ D ∪ (D + M) spans ≤ 2M+2.

Then W = (+(M+1), −b, δ_2, …, δ_last, +M, −δ^rev, −M) is a valid ordering of the tight pair, with range ≤ 2M+2. This range is IRC+ for maxP + maxN = 2M+1 odd, and it is enough for Graham at every p ≥ 2M+3.
`path2.py` finds the template for all 2 ≤ a < (M+1)/2 and M ≤ 20, except a = 3 with M ≥ 18, which are undetermined at a 2·10^6 node cap. Each solution is checked by direct validation.

**Exact-span version (span 2M+1).** This forces D = [−b, a] ∖ {1, 1−b, y} with y ∈ {−b, a−1}.
- Solvable for a = 2 (all M ≤ 22 except M = 6) and for a ≳ M/4.
- Fails exhaustively for 3 ≤ a ≲ M/4 at M ≤ 17 (`exactD.c`).
- **Single-zigzag obstruction (hand argument).** For a = 2, one inward zigzag block cannot realise the template. Label counting forces connector length M−2 and deleted label 2, and no interval satisfies both. This matches L9: at least two blocks are needed.

## Status
- **Max-root lift:** proved, but conditional on G\*.
- **Tight-family reduction:** proved, together with its template.
- **G\* and H:** finite evidence only, with exact data as above.
- **Tight family for a ≥ 2:** still open as an explicit all-M construction; the computations now settle M ≤ 20.
- **Full conjecture:** not proved.

## Update (2026-11-24): adversarial tests and safe-reduction census (GPT round, audited by Claude)
- **G\* survives adversarial tests** (GPT-reported, finite):
  - all pairs with magnitudes ≤ 20 and total size ≤ 8 (4.98M rooted cases);
  - tight-interval perturbations;
  - random no-top-gap dense pairs;
  - all balanced lifts of Q₅₉ and its SC2-I perturbation (870 rooted cases).

  The spiral obstructions do **not** transfer to G\* on these instances. These runs were not repeated here.
- **The universal safe-reduction menu is FALSE: VERIFIED** (`safe_reduction_counterexample.py`, plus an independent DFS).
  - Counterexample P = {1, 2, 5, 6}, N = {2, 3, 4, 5}, r = 2: no top gap, nonsymmetric, T = 14 > 11 = max P + max N.
  - It has exactly 2 G-walks.
  - Over all 17 admissible reductions (opposite-sign contraction, same-sign contraction, inverse-pair removal) and every reduced root, the best lifting fraction is **1/7**. No reduction is safe.
- **Census** (exact, GPT; not re-run): safe reductions exist for 82% (magnitudes ≤ 5), 71% (≤ 6) and 76% (≤ 7, size ≤ 9) of rooted cases. All three menu items are needed.
- **Counting inequality** (proved): lift fraction ≤ |W(A, r)| / |W(B, s)|, because expansion is injective. Smallest observed best-fractions: 1/37 (symmetric P = N = {1, 2, 3, 4}) and 1/7 (nonsymmetric). Whether a uniform positive bound exists is open.
- **Consequence.** An induction for G\* cannot avoid choosing the smaller cycle with this menu. The cycle-choice obstruction is now confirmed directly for G\*. G\* itself remains open, and so does a counting route (a uniform positive lifting fraction, conjecture LF).

## Update 2 (2026-11-24): the counting route LF (GPT round, audited)
**Definition.** L(A, r) is the maximum, over admissible reductions ρ and compatible roots, of the fraction of valid reduced walks that lift.

**Verified** (`lf_extremal_verifier.py` reproduces all five extremal cases exactly, with certificates):

| Instance | Root | L | Best reduction |
|---|---|---|---|
| {−5, −4, −3, −2, 1, 2, 5, 6} | 2 | 1/7 | (−2, 6): 2 of 14 reduced walks lift |
| {−9, −8, −6, −2, −1, 7, 9, 10} | 7 | 5/9 | |
| {−12, −11, −9, −7, 2, 4, 6, 8, 9, 10} | 9 | 59/76 | |
| ±[1..4] | 2 | 1/37 | |
| ±[1..7] | 1 | 16/183 | |

**Census (GPT, not re-run).**
- The minimum over nonsymmetric no-top-gap pairs is 1/7 at magnitudes ≤ 7 (exhaustive). The magnitude-10 and 12 samples are capped at ≤ 10 steps.
- Dense samples at magnitudes 10–12 are mostly node-capped, so they are inconclusive.
- **No evidence of decay, and no evidence of a uniform bound.**

**Proved (hand-checked).**
1. *LF needs only nonemptiness of the smaller walk set:* ⌈η·D_ρ⌉ ≥ 1. Correct.
   - **Caveat (Claude).** "Weak LF" (L > 0) is nearly equivalent to G\* itself. Compressing a valid walk by a contraction always gives a simple walk of B that lifts back to it. Its only possible failure is leaving B's smaller window. So the content of the counting route is the uniform constant η.
2. *Compression-fiber bounds:* C_ρ / (M_ρ·D_ρ) ≤ L_ρ ≤ C_ρ / D_ρ, with M_ρ = 2 for contractions and k(k − 1) for inverse pairs.
3. *Hole criterion:* a window-preserving contraction lifts iff v + x or v + y is a hole, where |H| = h + 1 and h is the window slack.
4. *Inverse-pair arc criterion:* K + d ⊆ J ∪ H. **Chain decomposition:** the arc splits into at most h + 2 arithmetic chains of difference d, each ending at a distinct hole. When h = 0 there are exactly two chains, and |K| ≤ (h + 2)⌊(W − 1)/x⌋.

**Open gap.** The distribution of holes and arithmetic-chain arcs among valid rooted walks with a given step set. This is the counting estimate LF needs, in the bounded-slack (dense) regime.
