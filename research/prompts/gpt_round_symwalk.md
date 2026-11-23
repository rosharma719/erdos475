# Next GPT prompt: contractions of symmetric walks (SYMWALK)

**Frontier (do not rederive):** research/STATE.md, METHOD_REVIEW.md, claims/symmetric_irc.md (YOUR proved symmetric-IRC walk), claims/symwalk_contraction.md (data).
Fact (yours, audited): for S={b_1>…>b_m} the walk W_S=(δ,b_1,−δ^rev,−b_1) with δ=(b_2,−b_3,b_4,…) has distinct integer vertices V_S=T∪(T+b_1) (T the spiral of prefix sums in [0,b_2]) and range b_1+b_2.
Fact (trivial): deleting vertices of a valid cycle (contraction) keeps it valid provided the new step labels are distinct and nonzero. So every A that equals the label set of a contraction of W_S (some S⊆[1..(p−1)/2], some dilation) has an explicit valid ordering.

**DATA (Claude, local, exhaustive/sampled):** zero-sum orbits covered by such contractions: p=13 24/24; p=17 244/244; p=19 781/784; p=23 8,283/8,358 (100% for every |A| ≤ (p−1)/2); p=29 sampled: |A|=6..11 1800/1800 (|S|≤9 cap), 12: 299/300. Restricting S to the absolute-value classes of λA is TOO strong (p=37 |A|=10: 29/30; p=41 |A|=16: 70%); with S unrestricted see claims/symwalk_contraction.md for the larger-prime sampled coverage. Uncovered orbits at p=19,23 are all dense (|A| ≥ about p/2); listed in the log of sym_contraction_unc.
Example (p=23): A={2,6,9,10,11,15,16} = labels of W_S for S={11,10,9,7,6} with vertices idx 0,1,4,5,6,7,8 kept (blocks (−9,7,−6)→−8≡15 and (−10,−11)→−21≡2).

**TASK (single goal, with stop rule):** decide
 (SYMWALK≤) For every prime p and every zero-sum A⊆F_p^× with |A| ≤ (p−3)/2 [or the correct threshold you can justify], there are a dilation λ and S⊆{1..(p−1)/2} (S need NOT lie in the classes of λA: p=37, A={23,26,7,3,17,34,21,11,35,8} is NOT representable with S⊆classes(λA) but IS with dilation 2 and S={17,16,15,14,11,7,6,5,2}) such that A=λ^{-1}·(label set of a contraction of W_S).
Prove it by an explicit recipe (an algorithm producing S and the deleted vertices from A), or prove a weaker explicit sub-range, or find a counterexample (a specific p and A, with the exhaustive check over all S and all deletions as certificate).
Hints from the data, not constraints: the number of deleted vertices is Θ(|A|) for sets without inverse pairs (each ±b_i can survive as a single-step label on at most one side); small-integer structure of S seems irrelevant; dense sets near p/2 are where coverage first fails.
STOP RULE: two genuinely different recipe ideas, each pushed to a precise obstruction (a concrete A and why the recipe cannot place it).

**Rules:** state what the result implies (it would give Graham with an explicit certificate for all |A| ≤ p/2, i.e. the whole middle range) and what is new beyond "Graham for these sets"; test at p ≥ 41 on adversarial sets (including structured ones) with a positive control; mark gaps GAP-n; do not call anything proved unless complete; deliver re-runnable scripts and exact counterexamples if any.
