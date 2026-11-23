# Symmetric sets: exact reduction to a folded graceful-cycle problem (Claude, analytic, 2026-11-22)

**Setting.** p=2r+1, W ⊆ [1..r] with |W|=m≥2, A=±W={±w : w∈W} (a symmetric, hence zero-sum, set of size 2m).

**Half-cycle form.** Cycles (s_1,...,s_m,−s_1,...,−s_m) with s_j ∈ {±w}, each class used once. With prefix sums P_0=0,..,P_m=T the vertices are P_0..P_{m−1}, T−P_0..T−P_{m−1}.

**Theorem (exact reduction).** Put Q_j=P_j−T/2 (so Q_m=T/2=−Q_0). The half-cycle is valid iff the 2m numbers ±Q_j (0≤j<m) are distinct, i.e. iff the Q_j are nonzero and lie in pairwise distinct ±classes. Hence:
A=±W has a valid half-cycle ⇔ there are distinct x_0..x_{m−1}∈[1..r], signs ε_0..ε_{m−1}∈{±1} and ε_m=−ε_0, x_m=x_0 (Q_j=ε_j x_j mod p) such that the classes of Q_j−Q_{j−1} (j=1..m) are exactly W.
Proof. Vertices P_j=Q_j+T/2 and T−P_j=T/2−Q_j, so the 2m vertices are T/2±Q_j; steps are s_j=Q_j−Q_{j−1}. Distinctness of T/2±Q_j (0≤j<m) ⇔ ±Q_j distinct. ∎
Combinatorially: a cyclic labelling of C_m by DISTINCT integers x_j∈[1..r] where each edge x_{j−1}x_j has weight |x_{j−1}−x_j| (same-sign type) or fold(x_{j−1}+x_j)=min(x_{j−1}+x_j, p−x_{j−1}−x_j) (opposite-sign type), the weights are exactly W, and the number of opposite-sign edges is ODD (Möbius twist from Q_m=−Q_0).

**Conjecture FOLD.** For every W⊆[1..r], |W|=m≥2, such a labelling exists (⇒ Graham for every symmetric set A=±W, at p). 
Relation: for W=[1..r] this is the antipodal case (H={±1}, d=r) of GPT's double-transversal criterion; FOLD is its extension to arbitrary subsets W, i.e. to all symmetric sets (the family where zigzag Z* failed: P=N=[1..h]).

**Data (Claude, no API).** Half-cycles found for EVERY symmetric A (m≥2): p=7 (4 sets), 11 (26), 13 (57), 17 (247), 19 (502): 0 failures, 0 undetermined. Equivalence checked on 832 found solutions (half→folded and folded→cycle): 0 violations (experiments/audits/folded_cycle_equivalence.py; search code experiments/exploration/symmetric_half_cycle.py). Also p=23 (2,036 symmetric sets) and p=29 (16,369 symmetric sets): 0 failures, 0 undetermined.
**Why it is interesting.** It converts the symmetric-set case of Graham into a graceful-labelling-with-folding problem on a cycle of length m, with m free labels in [1..r]; induction on m by subdividing an edge looks plausible when m is far below r (many free labels) and is exactly the dense difficulty when m≈r.

## Follow-up analysis (Claude, 2026-11-22)
**Negative lemma (proved).** In the folded picture, inserting one new vertex V into an edge Q_{j−1}→Q_j (step s) so that one of the two new steps keeps the old class e=|s| forces the other class to be fold(2e); hence "subdivide an edge and add one prescribed new weight M" works only for M=fold(2e). Any inductive step must therefore be a merge/lift pair (f_1,f_2)↔e=fold(f_1±f_2), which is the free-point problem again (the new vertex's class must be free); no escape from the balance obstruction by subdivision alone.
**No canonical restricted form.** Solutions with at most one same-sign (difference-type) edge — i.e. almost all edges sum-type — fail for 38% of symmetric sets (p=13: 21/57, p=17: 95/247, p=19: 193/502; typically small weights like {1,2,3}, which need difference-type edges). The opposite form (exactly one sum-type edge: a graceful-like path of m distinct labels with m−1 absolute differences and a closing fold(x_0+x_{m−1})) works for ~88–90% (p=13: 7/57 fail, p=17: 32/247, p=19: 62/502, p=23: 198/2036 fail, 28 undetermined) and fails exactly for sets with several large weights, which cannot be differences of labels ≤ r. So the number/placement of sum-type edges must depend on W: small weights ↔ difference-type, large weights ↔ sum-type.
**Heuristic count.** Expected number of folded labellings ≈ r!·m!·2^{m−1}/((r−m)!·r^m) ≫ 1 for all m (e.g. ≈ m!·2^{m−1} for m ≪ r), consistent with existence for every W; a proof would need an Ringel–Kotzig-type exact-weight argument.
