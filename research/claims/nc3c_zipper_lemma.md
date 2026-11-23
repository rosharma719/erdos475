# NC3C generic case: two-pair zipper lemma (supplied by GPT; AUDITED IN-SESSION; a sufficient condition, not a solution)

**Lemma.** p odd prime, C={a,b,c} ⊂ F_p^× distinct, a+b+c ≠ 0, a+b ∉ C ∪ {0}. Suppose a rotational sequencing B of F_p^× has two disjoint cyclic consecutive blocks of labels: (a,b) (either order) and (a+b,c) (either order, a+b here a separate original label). Then F_p^× ∖ C has a valid ordering.

**Proof.** Contract (a,b) to a+b (stays simple). Cut out the consecutive block (a+b,c); the complementary cyclic arc is a linear ordering with p−4 steps; its label multiset is F_p^× ∖ {a,b,c} (the new a+b replaces the original a+b removed with c). Partial sums = vertex differences along a sub-collection of distinct vertices, hence distinct. ∎

**Applicability.** If C has no inverse pair, some pair {a,b} ⊂ C has a+b ∉ C (else a+b=c, a+c=b ⇒ 2a=0).
**GAP.** A rotational sequencing with the two disjoint adjacencies for some choice of {a,b} and some dilation, for EVERY generic C (ΣC≠0, no inverse pair).

**Claude's audit + data (no API).** Lemma re-derived: correct. Direct verification: 3,725 orderings built from sampled HOS graceful sequencings at p=23,29, 0 invalid. Coverage: 400 random graceful-permutation sequencings (with reversal/complement) realise the zipper pattern for ALL generic dilation-orbits: 57/57 at p=23, 100/100 at p=29. The single explicit Walecki sequencing covers only 26/57, 35/100, 38/117, 47/176, 53/222, 56/247 orbits (p=23,29,31,37,41,43): so the generic case is almost certainly true, but needs a parametric family of graceful permutations, not one fixed sequencing. (experiments/exploration/zipper_coverage.py, zipper_walecki.py, experiments/audits/zipper_verify.py)
