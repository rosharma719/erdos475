# Free-point / avoidance (FP∀, DFL, balance identity)

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
