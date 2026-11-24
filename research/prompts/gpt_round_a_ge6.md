# Next round: close the tight family for a >= 6 (then the tight family is DONE)

AUDIT: your a=2,3,4,5 constructions are ACCEPTED (Claude L34): independent implementation, 0 failures for every M<=1200;
bridge lemma, a=2 core, a=3 reflection recursion, a=4/5 headers + G_{n,d} recursion all re-derived by hand.
Tight family now proved for a = 1..5, all M.

a >= 6: your 4-cycle obstruction only kills the maximally packed window [3-a, M+2-a]. Exact SAT shows YOUR SAME BRIDGE
W = (δ, +M, −rev δ, +b, −M, −(M+1), +a) works for every a >= 6, M = 13..31 (and the bridge (+a,−M,+b,−(M+1)) near a≈M/2),
once the core window is relaxed. The cores found all have the shape
   D = {−a−1} ∪ ([2−a, M−a−2] \ {h}) ∪ {M−a}   (one internal hole h, one outlier at each end, span M+1),
using labels [1,M−1]\{a,b}. Conditions to check for the bridge: D ∩ (D+M) = ∅ (holds: the two pairs at distance M are
broken by the holes −a and M−a−1), and the bridge points M+b, b, −a avoid D ∪ (M+D).
PLAN: header through the two outliers (big labels), then a one-hole graceful path on [2−a, M−a−2]\{h} with labels
[1, ...]\{a,b} — i.e. your G_{n,d} recursion generalised to TWO missing labels (d=a small, d'=b large; the peeled
labels n−1,n−2,n−3 hit b at one level, handle that level with a gadget). Seeds G_{n,d} for n=d+1 (zigzag), d+2, d+3
exist for d=4..16 (experiments/irc/gseeds.py); give them uniformly in d (they are zigzags with a short gadget).
Deliver: proof for all a>=6 (case split by residues as needed), verifier for M<=400. That completes the tight family.
