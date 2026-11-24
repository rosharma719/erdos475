# Strategy review: which direction is most promising? (Claude, 2026-11-24)

This review is based on the full corpus: `ledger.md`, `proof_graph.yaml` (74 nodes: 51 candidate, 5 published, 2 finite-verified, 8 blocked, 8 refuted), 49 claim files, `obstructions/`, `data/` and `experiments/`.

## 1. What the corpus establishes

**Reductions (proved or candidate).**
- One-element reduction: Graham ⇐ zero-sum sets.
- Balanced integer lift (diameter < p).
- Unequal-extreme rectification: Graham ⇐ the symmetric theorem plus BS for sets with P ≠ Q.

**Proved coverage.**
- Symmetric sets: the explicit Walecki-type walk, valid for all p.
- |A| ≥ p − 5: NC3-Z and the 4-complement theorem, both via **Walecki contractions**.
- Index ≤ 2.
- Sparse and moderate regimes of the integer route: T ≤ P + Q, top gap, compact band, quotient-separated.
- Many explicit dense families.

**Data.**
- All p ≤ 37 exhaustive.
- G\* (rooted window): 63M roots.
- Targets A/B: 11.7M instances.
- EC/MC avoidance: p ≤ 13 exhaustive, structured adversarial families up to p = 127.

## 2. Directions that are provably capped (stop investing)

| Direction | Cap (proved in this repo) |
|---|---|
| Peak removal, protected paths, two-path greedy | Run-count lemma: two climbs ⇒ T ≤ P + 2Q (`protected_paths_audit.md`) |
| k-path greedy / separation | k-path separation false; dense ⇒ every step is a tail trap (`protected_greedy_audit.md`) |
| Compact-band / flexible pairing | n < 4√D (`band_compatibility_audit.md`) |
| Quotient-block lifting | n ≤ D/2 + 1; universal quotient contraction false (`quotient_blocks_audit.md`, `overlap_lifting_audit.md`) |
| Block-extrema paths | sign imbalance ≤ 2 + 2√D (`imbalance_core_audit.md`) |
| Repair of a prescribed cycle (swaps, windows, insertion, fixed core) | Refuted repeatedly (LOCAL_REPAIR_DENSE, BOUNDED_SWAP_REPAIR, GAP B counterexample, short-window trap) |
| Polynomial / CN coefficients | Behave arithmetically randomly (`polynomial_cn.md`, `fused_block_alternant.md`) |
| Dissociated modular repair | Only blocks of size ≤ log₂ p (`modular_repair_audit.md`) |

Every surviving induction scheme ends at the same unproved step: **choose a good smaller cycle**.

## 3. Ranking of live directions

### Rank 1 (proof route): spiral contraction, i.e. coarsening the family of symmetric walks
**Idea.** Take a valid cycle of a symmetric set ±S from the *proved* explicit family. Merge consecutive steps into blocks. **A contraction of a valid cycle is automatically valid** (the vertices are a subset). So if A (up to dilation) is the multiset of block sums, A is done. There is no collision analysis and no cycle choice for A: the whole problem becomes a combinatorial *covering* question about block sums of an explicit spiral.

**Why this is the most promising:**
1. **It is the only method with proved results in the dense regime.** NC3-Z (|A| = p − 4) and the 4-complement theorem (p − 5) are Walecki contractions.
2. **Its coverage is very high already, with almost no freedom used.** One fixed walk per S covers 8,283 / 8,358 zero-sum orbits at p = 23 (99.1%) and 100% of every size ≤ (p − 1)/2 (`symwalk_contraction.md`). It also covers 781/784 at p = 19 and 100% at p ≤ 17.
3. **The failures happen exactly where freedom was not used.** Fixed-Walecki coarsening fails (p = 19, C = {7, 8, 10, 14, 18}), but only one walk per S was tried. The proved family is much larger:
   - any descending-alternating δ;
   - the rooting criterion and templates of `rooted_symmetric.md`;
   - dilations;
   - the half-walk lemma L6 with any admissible δ.
4. **It works natively mod p**, so no integer lift is needed, and it targets dense sets directly.

**Next experiment (with a stop rule).** Recompute coverage at p = 19, 23 and 29 using the full proved family (all admissible δ for (δ, M, −δ^rev, −M), all S, all dilations), not one walk per S.
- **If coverage is 100% at p ≤ 23:** extract the block structure of the certificates (which S, which block lengths and positions) and conjecture an explicit *coarsening lemma*. That lemma is then the theorem to prove.
- **If a zero-sum orbit at p ≤ 23 is not a contraction of any proved spiral:** the route needs a new spiral family; record the obstruction and move to rank 2.

### Rank 2 (falsification target): G\* and Targets A/B on adversarial dense families
These carry the strongest data in the repo, and the open step is stated exactly. The cheap, high-information move is to try to break them at larger sizes (values 16–20, no-top-gap dense sets, tight integer families). A counterexample to G\* or to Target A/B would remove a whole class of induction strategies. More confirmations would add little.

### Rank 3 (finishable deliverable): sound verification and a consolidated write-up
1. A torsion-aware re-verification of CDFV's small-set claims (|A| ≤ 20; zero-sum ≤ 22). This settles a published result either way.
2. Run the referee gates on the 51 candidate nodes (this needs an API key as an environment variable).
3. One write-up separating proved / candidate / evidence, with the obstruction lemmas. Several items may be worth expert review: unequal-extreme rectification, protected two-path theorem, safe quotient lifting, rooted symmetric criterion, and the cap lemmas.

### Low priority: ideas with no mechanism yet
- **Rigidity / counting.** The minimum number of valid cycles is p-independent and is attained by ±[1..m] (the tight IRC sets). A counting lower bound would prove everything, but nothing in the corpus suggests how to get one.
- **Effective large-p thresholds.** The ledger's estimate was withdrawn, and no explicit threshold is justified. Only worth pursuing if a 2026 paper makes constants explicit.

## 4. Recommendation
Run the rank-1 experiment next. It is a single, well-defined computation with a clear stop rule. It builds on the only construction class that has ever produced dense-regime proofs, and it turns the problem from cycle choice into a covering question. Pursue rank 3 in parallel regardless, since it yields durable value whether or not the conjecture falls.

## 5. Update (2026-11-24): the true endgame is bounded size, so the dense regime is already settled
Primary sources were read from arXiv; erdosproblems.com returned 403 and was not read.
- **Nguyen–Tran–Vu, arXiv:2610.40712, Thm 1.5:** "There is an absolute constant C such that … for every finite abelian group G, any set S ⊆ G∖{0} of size at least C has a valid ordering." Also: "the constant C is independent of the ambient group G."
- **Kuang–Wang, arXiv:2610.34424, Thm 1.6:** the same statement, with an absolute n₀.
- **Neither gives a numerical value.** Their internal constants are non-explicit ("c_D sufficiently small", C ≥ 10²⁵, |G|^(−1/9500)-type bounds; taken from the fetch's summary of the full text, not verbatim).

**Consequence.** Graham holds for every |A| ≥ C at every prime. The dense regime that all integer, spiral and contraction routes targeted is **already proved** (non-effectively). The remaining problem is exactly:

> **(E) make C explicit, and (F) prove Graham for all |A| < C at every prime.**

**Tools for (F):**
- per-size certificates valid in every characteristic: CN c_k (done for k ≤ 13, `polynomial_cn.md`) and the torsion-aware symbolic search (`modular_repair_audit.md`);
- CDFV's |A| ≤ 20 claim for all abelian groups, which needs a sound re-verification (ledger 2026-11-22);
- the effective small-set theorems (Kravitz) for p large relative to k.

**The conjecture is finished if C can be pushed down to the verified small-size range (about 13–20) and that range is soundly certified.** The obstacle is (E): the proved C is non-explicit and almost certainly astronomically large.

**Revised ranking:**
1. Quantify (E): extract an explicit C from NTV, the cleaner "absolute C" proof, or at least its order of magnitude. Identify which lemma dominates and whether a structural argument could replace it for moderate sizes.
2. Push (F) upward: soundly re-verify CDFV (k ≤ 20), and extend the all-characteristic per-size certificates as far as feasible.
3. Dense-regime constructions are now of independent interest only. They no longer advance the all-primes problem.
