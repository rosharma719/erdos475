# Parallel track: the general (non-tight) conjecture — dense regime first

Data (Claude L24): after the best dilation, a random zero-sum A ⊂ Z_p^* of density α has lift (P,N) with asymmetric
remainder r = |P\N|+|N\P| ≈ 0.45k at α=0.5, 0.27k at α=0.65, 0.22k at α=0.8, 0.12k at α=0.9 (p=53). So dense sets are a
symmetric core plus a small balanced remainder; and the number of free residues is p-1-k.

TASK (dense regime): prove a splice theorem strong enough for remainders of this size: given the symmetric core C
(which has the explicit half-walk (δ,c,-δ^rev,-c) with vertices D ∪ (D+c)) and a balanced remainder (P0,N0), insert
the remainder into the core walk — e.g. around crossing steps, into the free residues mod p, or by merging remainder
elements with core pieces (half-walk merges) — so the result has distinct partial sums mod p.
State the exact quantitative condition (in terms of r, the free room p-1-k, and the structure of C) under which your
splice works, prove it, and test it on random dense A for p<=101 with a stdlib verifier. Earlier relevant results:
threaded splicing (core + remainder with b+H <= M-1), small-block absorption (13.4), multimerge.

UPDATE (Claude L25, stronger target): SPL — insert the remainder steps into the FIXED explicit symmetric core walk
W_C=(b2,-b3,b4,...,b1,...,-b1) (any rotation, any insertion positions/order). Exact search: every tested dense/middle set
works (p=53 at α=0.5..0.9, p=101 at α=0.9; remainders up to 14). Prove SPL, ideally by an explicit insertion rule:
the core vertices are a lower cluster D ⊂ [0,b2] and an upper cluster b1+D; inserting remainder steps shifts the rest of
the walk by the running remainder sum, so the rule must place each shifted segment into free residues mod p.

UPDATE 2 (Claude L27): the splice can be taken in AVOID form. W = core walk with one remainder step x1 inserted before the
final −c, then the remaining remainder steps after the core walk. Validity ⇔ the remainder ordering U=(x1,...,x_r) from
0 has all nonzero partial sums outside V_C (the core walk's vertex set, a lower cluster D ⊂ [0,b2] plus b1+D), and
top+x1 ∉ V_C ∪ V(U). Exact tests p=53: 12/12 at α=0.5,0.65,0.8. So the target theorem is OBSTACLE-AVOIDANCE:
a zero-sum set R of size r has an ordering avoiding a forbidden set F of this two-cluster form whenever
r + |F| <= (some explicit fraction) p, using the free choice of rotation (which vertex is 0) and x1. Prove it.
