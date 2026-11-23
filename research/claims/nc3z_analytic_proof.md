# NC3-Z: zero-sum three-element complements (proof supplied by GPT, 2026-11-22; AUDITED IN-SESSION by Claude, not yet by the referee gates)

**Theorem.** p prime, C ⊂ (Z/pZ)^× three distinct elements with ΣC = 0. Then A = (Z/pZ)^× ∖ C has an ordering with pairwise distinct partial sums. (p ≥ 11 by the construction; p = 7: C={1,2,4}, A={3,5,6}, order (3,5,6) has partial sums (3,1,0); p ≤ 5: no zero-sum triple.)

**Lemma 1 (normalisation).** p=2r+1, r ≥ 5: every zero-sum triple is, up to a unit, C_t = {−1, t, 1−t}, 3 ≤ t ≤ r−1. (Scale an element to −1; signed reps u,v ∈ [−r,r] with u+v ≡ 1 force u+v = 1 (u+v=−2r gives u=v=−r); one is positive, so {t,1−t}; t=2 repeats −1 so t ≥ 3; t=r handled by multiplying by 2: {−1,r,1−r}·2 = {−2,−1,3} = C_3.)

**Lemma 2 (Walecki closed cycle).** α = (1,r,2,r−1,3,…), δ_i = α_{i+1}−α_i = (−1)^{i+1}(r−i). B = (δ_1..δ_{r−1}, r, −δ_{r−1}..−δ_1, −r) uses every nonzero residue once; its vertices (up to translation by α_1) are (α_1..α_r, α_r+r..α_1+r) = the integers 1..2r, hence distinct mod 2r+1.

**Lemma 3 (simultaneous contraction).** Contracting disjoint consecutive blocks of a simple cyclic walk to their sums deletes interior vertices only, so the walk stays simple; the new label multiset is read off after contraction.

**Construction.** C_t, 3 ≤ t ≤ r−1, i = r−t, ε = (−1)^{i+1}. P = (δ_i, δ_{i+1}) = (εt, −ε(t−1)), sum ε. Q = (δ_{r−1}, r, −δ_{r−1}) = (η, r, −η), sum r. i ≤ r−3 so P and Q are disjoint. Contract both: labels lost {εt, −ε(t−1), η, −η}, gained ε (P's sum; ε ∈ {±1} = {η,−η}); r is kept. Net label set = F_p^× ∖ {−ε, εt, −ε(t−1)} = F_p^× ∖ εC_t, with 2r−3 = p−4 steps and simple cycle. Scale by ε and undo normalisation: ordering of F_p^× ∖ C.

**Remarks from the source.** Extends to odd composite n ≥ 11 when C contains a unit. GPT's own certificate: constructed and checked 11,526 zero-sum triples for 11 ≤ p ≤ 101, 0 failures.

**Claude's audit (in-session, no API).** (i) Lemma 1: re-derived, incl. the case analysis for u+v and t=r. (ii) Lemma 2: checked δ_i formula against the Walecki permutation; vertex set = 2r consecutive integers mod 2r+1. (iii) Label bookkeeping re-derived: net removed set is exactly εC_t, no label duplicated. (iv) Block disjointness: P ends at position i+1 ≤ r−2 < r−1. (v) Independent implementation written from the proof text (experiments/audits/nc3z_independent.py): all 2,926 zero-sum triples for 11 ≤ p ≤ 61, 0 failures. Verdict: the proof is correct as written. Status stays `candidate` until the referee gates (≥2 referee accepts) run; promotion is not done by the author/auditor model.
