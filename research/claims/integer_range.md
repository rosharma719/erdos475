# Integer / zigzag reformulation, IRC (Z* REFUTED)

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
