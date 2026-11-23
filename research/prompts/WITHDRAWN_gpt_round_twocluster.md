# Round: prove the TWO-CLUSTER conjecture (TC); it implies Graham's conjecture (with the symmetric IRC theorem / one-element reduction)

Two-cluster lemma (proved, research/claims/claude_lane.md L11). P,N balanced positive sets, c=max P >= d=max N (else negate),
Delta=c-d, T = (P\{c}) ∪ -(N\{d}) (signed steps, sum T = -Delta). If T splits into sequences A, B with
 A a path 0 -> e1 with distinct vertices, B a path e1+Delta -> 0 with distinct vertices, V(A) ∩ (V(B)+d) = ∅,
then W=(A,+c,B,-d) is a valid ordering (distinct partial sums). If V(A)∪V(B) fits in an interval of length <= d-1 the range is
<= 2d-1 <= maxP+maxN-1. Graham needs range <= maxP+maxN (+1 if odd). The arcs A and B MAY share vertices.

TC: such a split always exists. Evidence: every tight pair M<=11, 150/150 random dense pairs (elements<=14), 118/120 (<=18, 2 timeouts), no failure.
No zigzag rule. Outward walks (each new vertex is a new max or min) are self-avoiding automatically; two outward arcs suffice
in most cases but fail at P=[1,7], N=[1,8]\{3,5}.

TASK: prove TC (or a version of it with the Graham range) by induction on |P|+|N|. Suggested shape: define the right
recursive object (a closed walk with a virtual step +Delta made of two self-avoiding arcs inside a window, with the shifted
cross-condition) and show it decomposes again by its own two largest opposite steps, OR give an explicit arc construction
(outward arcs with one level of nesting). Mark every unproved step UNPROVED; stdlib verifier.
