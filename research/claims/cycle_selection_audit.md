# Cycle-selection round: audit (Claude, 2026-11-25)

Source: `Erdos475_Cycle_Selection_and_Verification.pdf` (GPT). It bundles four notes and 16 embedded files. The scripts, the seed table, `note.tex` and the gzipped data are in `experiments/checks/cycle_selection/`.

All counting conventions below are the source's. **Notation.** A is zero-sum. U is the set of unpaired labels (those whose negatives are absent). L = max |u| over centered representatives after a dilation. N = 2M + 1 is the modulus. A contraction replaces a, b ∈ A with t = a + b ∉ A ∪ {0}. A *rooted witness* is a t-rooted cycle of the contracted set that avoids a, so expanding t gives a valid cycle of A.

## Verifiers: all 10 reproduce exactly

The verifiers were run from a separate copy (standard library only, assertions on).

| Script | Output (matches the claim) | Time |
|---|---|---|
| `check.py` | symmetric prescribed splits p = 3..23: 0, 0, 12, 240, 768, 6144, 16128, 101376 | 1 s |
| `prefix_avoidance_certificate.py` | gcd(C, E) for h = 1..9: 1, 2, 18, 96, 7500, 194400, 1882384, 2832334848, 239990252544; all prime factors ≤ 2h + 1 | 2 s |
| `five_hole_certificate.py` | 2,047 exhaustive outer-padding cases (N = 63..83), 470 full-padding checks (N ≤ 1001) | <1 s |
| `extensions.py` | depth 1–4 frontiers: 3, 9, 36, 144 choice paths | <1 s |
| `barrier.py` | p = 53: closed defect-one component (10 states, 10 edges, 0 exits), barrier 2; p = 61: 14 states, no legal merges | <1 s |
| `general_check.py` | 576 variable-radius checks | <1 s |
| `width12_verify.py` | 5,786 direct witnesses, 46 exact obstructions, 90,720 doubled witnesses; (bad, dense) = (46, 4307) | 2.5 s |
| `offset_verify.py` | 4,416 cycles and contractions; all 46 offset seeds | <1 s |
| `bridge_verify.py` | old double 90,720, bridge 42,900, new double 9,264, terminal 2,268; **missing 0 profiles**; 145,106 small-modulus cycles | 3 s |
| `bridge_regression.py` | 86,580 full bridge cycles and contractions | 2.5 s |

The data must be gunzipped next to the scripts first: `width12_data.json`, `bridge_data.json`, `bridge_small_moduli.txt`.

## Theorems: status after hand-checking

### T1. Gap-capacity theorem (any number of unpaired labels, any radius). **Proof checked; correct.**

**Statement.** Let U have integer sum 0 in centered coordinates. All other labels come in pairs. Let d₁ < … < d_k be the paired magnitudes above L, d₀ = L, and cap_i = d_i − d_{i−1} − 1. Suppose the positive labels of U can be packed into the gaps with per-gap sum ≤ cap_i, and the negative magnitudes can be packed independently in the same way. Then **A has a valid ordering**, with an admissible contraction marked.

**Checked:**
- The width after appending gap-i mass is ≤ d_{i−1} + cap_i < d_i, so the inward jump d_i crosses both paths and lands on a fresh extreme.
- The endpoint difference equals the running sum of U, which is 0 at the end.
- The closure P, ±D, Q backward, ∓D lies in disjoint translated intervals of span < 2D < N.
- The marked pair (last outward label a, inward jump d_i) has |sum| = d_i − a ∈ (d_{i−1}, d_i). That magnitude is unoccupied and exceeds L, so the contraction is admissible.

The construction gives a valid cycle of A directly.

**Five-label corollary (checked).** Two distinct gaps suffice: one of capacity ≥ L, the other of capacity ≥ max(L, ⌊(4L − 2)/3⌋).
- 1-vs-4 sign split: the mass per sign is ≤ L.
- 2-vs-3 split: put the larger of the three in the L gap. The other two sum to ≤ ⌊2T/3⌋ with T ≤ 2L − 1.

**Weakly sum-free, no inner padding:** one gap of capacity ≥ ⌊(T − 1)/2⌋ suffices.

### T2. Radius-12 five-unpaired theorem. **Proved, computer-assisted; certificates verified here.**

**Statement.** Suppose |U| = 5 and some dilation makes U centered with integer sum 0, L ≤ 12, and weakly sum-free (no a + b = c among distinct members). Then with **arbitrary** symmetric padding, at **every** odd N, A has a rooted witness, hence a valid ordering. For p ≥ 53, integer-zero follows from modular-zero, since 12 + 11 + 10 + 9 + 8 = 50 < p.

**Structure:**
- 62 remainders and 5,832 low configurations.
- 5,786 have width-L two-path certificates.
- The other 46 are exact two-path obstructions in tight coordinates. They are closed by four mechanisms:
  - doubling (×2), 90,720 + 9,264;
  - symbolic joining words valid for all M ≥ 2L, 42,900;
  - the terminal-gap argument, 2,268, plus 792 integer exceptions;
  - direct checks for L ≤ M < 2L, 145,106 completions.
- The verifier exhausts every top mask with 0 missing profiles.

**Checked by hand:** the joining criterion (page 2), the symbolic interval complement [1, L + h − 1] ∪ (M + [h + 1, L]), and the terminal word W = (−D, v, u, H, D, −rev(H), q).

**Consequence:** any five-unpaired minimal counterexample has a remainder whose every centered dilation has radius > 12.

### T3. Prefix-avoidance lemma (h ≤ 9) and atom attachment. **Proof checked; correct, given the verified coefficients.**

**Lemma.** Take ≥ 2h + 1 distinct nonzero labels and ≤ h forbidden values at each proper rank. Some ordering avoids all of them.

**Proof.** Kós-style antisymmetrisation: the alternating sum is C(b)·V, since lower-degree parts vanish. Two lengths (2h and 2h + 1, with b₂ = 2h in the second) have gcd(C, E) smooth over primes ≤ 2h + 1 < p. Greedy steps first, then the certificate on a translate.

**Attachment theorem.** Let Z be a rooted cycle with holes H, h = |Z| + |H| ≤ 9, and D a disjoint atom (minimal zero-sum) with |D| ≥ 2h + 2. Then D can be inserted at any edge w, keeping the holes unvisited.

**Collision accounting checked:**
- b ∉ U ∪ (U − w).
- A prefix can never hit w, by atomicity.
- New vertices are pairwise distinct, again by atomicity.
- At most h forbidden values per rank.

**Application.** For |Z| ≤ 8, any atom of size ≥ 2|Z| + 4 can be attached while keeping x avoided.

**Limit (correct).** It needs an atom larger than about 2/3 of the core. The five-hole family has none, since an atom has size ≤ (p − 1)/2 once p > 67.

### T4. Dissociated-block theorem, 16k > 7n. **Proof checked line by line; correct.**

**Statement.** Let |A| = n, ΣA = 0, and S ⊆ A with |S| = k ≥ 5 dissociated. Suppose t = ΣS ∉ A ∪ {0} and B = (A ∖ S) ∪ {t} has a valid cycle. If 16k > 7n, then A has a valid cycle.

**Steps checked:**
- **Separator.** The family of proper subsets with sums in V meets every maximal chain, and has ≤ n − k − 1 members.
- **Union bounds.** Use 1/C(k, j) ≤ 2/(k(k − 1)) for 2 ≤ j ≤ k − 2. If a singleton is missing, conditioning gives b + c ≥ k − 1; a missing co-singleton gives a + c ≥ k − 1. Both together force 2r ≥ k − 3, a contradiction. So every rooted cycle contains S or t − S.
- **Reversal blockers.**
  - Two-edge and three-edge reversals must move a vertex, since labels are distinct and the characteristic is odd.
  - Four consecutive S-vertices force two distinct blockers.
  - Pieces share no blocker, since u + v + s′ = u′ + v′ + s compares distinct 3-subsets.
  - A run of L vertices needs ⌊2(L − 1)/3⌋ blockers.
  - There are at most r + 1 runs (0 and t are adjacent) and at most r + 1 blockers. Hence 7(r + 1) ≥ 2k, a contradiction.

**Strength.** This strengthens the earlier 9k ≥ 4n + 1. Dissociation forces 2^k ≤ p, so this constrains only sets with n < (16/7)·log₂ p.

### T5. Prescribed split of a symmetric core. **Proof checked; check.py confirms p ≤ 23.**

**Statement.** Let B = −B, t ∈ B, and x, y ∉ B with x + y = t. Then there is a t-rooted B-cycle avoiding x.

**Construction.** Use the increasing alternating path P and its rotation Q. Insert (d − 1, 1), or (−1, d + 1), at the d step. The inserted vertex lies strictly inside the old extreme range, and Q's interior lies beyond T. So every symmetric core admits every external two-split. This strengthens the FV symmetric case to arbitrary prescribed summands.

### T6. Five-hole family and recursive extensions. **Constructions verified.**

- **Five holes.** A = (ℤ_N)^× ∖ {3, 4, 8, 16, −31}: for every odd N ≥ 63, A has a cycle beginning 1, 2. This resolves the obstruction example from the attachment note.
- **Recursive invariant (checked).** For each k ≥ 5 it gives an explicit k-hole family. Only particular hole sets are covered.

### T7. No fixed radius suffices (correct).
U = {1, T, 3T, −2T + 1, −2T − 2} with p > max(9T + 6, (T + 1)K) has no dilation of radius ≤ K. So T2 cannot be pushed to all five-label remainders by raising the cutoff alone.

## Where this leaves the problem

**Minimal counterexample, five-unpaired case.** Every remainder dilation has radius > 12, and the gap-capacity condition (two gaps, T1) fails in every dilation. That means the padding is dense above L, with no gap of capacity about L, in every coordinate system.

**The general open step is unchanged.** Every admissible contraction must be simultaneously blocked while all cores are dense and asymmetric, with no large atom and no large dissociated block. The next thing to prove is T1 with **small total capacity**: absorb U's mass across many small gaps, or across gaps in a different dilation, when no single gap holds L. Equivalently, replace the finite radius-12 tables by a construction whose radius grows with p.

## Update (2026-11-25): equal pair sums (Astra round, audited)

**Theorem.** Let A be zero-sum mod p with exactly five unpaired labels U and arbitrary symmetric padding. If two distinct pairs in U have equal sums, then A has an admissible contraction with a rooted witness, so A has a valid ordering. There is no radius bound.

**Proof checked by hand. It is correct.**

- **Normalisation.**
  - The two pairs are disjoint and share a sum s ≠ 0, so the fifth label is −2s.
  - Scaling by s⁻¹ makes both pairs integer pairs {−j, j + 1}. A wrapped sum would need two copies of −M.
  - Every j ≥ 3, because −2 occupies magnitude 2.
- **Path rule.** Each ordinary group (−ej, e(j + 1)) goes onto a single path as (σj, −σ(j + 1)). This leaves σ unchanged, and both paths stay at the −σ extreme.
- **Closure.** The last jump of Y is rotated to the front, giving span < 2M.
- **Vacant case.** Contract (−k, −2) → −(k + 2), so X gets −(k + 2) and Y gets −(k + 1). The inserted vertex u − k lies strictly between the old and new minima.
- **Occupied case.** Contract (−2, k + 2) → +k, with Y getting (−(k + 1), k + 2). The inserted vertex is m − 2, and the next X-jump has magnitude ≥ k + 3, landing ≤ m − 3.
- **Boundary case.** The groups occupy [M − 3, M − 2] and [M − 1, M]. After doubling, the five labels become {7, −5, 3, −1, −4}, and only magnitudes 2 and 6 are optional within radius 7. The four explicit path pairs cover these, and the separator closure handles everything beyond.

**Verifier** (`equal_sums.py`, reproduced, 10 s):
- through N = 35: vacant 270,336, occupied 270,336, boundary 8,190, total 548,862;
- higher asymmetry through N = 27: 1,208 / 1,208 / 392;
- 900 larger random cycles;
- the p = 211 and p = 503 obstructions have 10 distinct pair sums.

**Consequence.** Any five-unpaired minimal counterexample has U with all ten pair sums distinct, in addition to the earlier constraints:
- radius > 12 in every dilation;
- the gap-capacity condition fails in every dilation.

**Extension (construction checked, verified through N = 27).** U = {−2} together with pairs of sums ±1, with two more positive groups than negative, works with arbitrary padding.

**Assessment.** This is a correct, clean new sufficient condition. It is another family of the kind the FV prompt asked Astra to avoid. FV itself was not attacked.
