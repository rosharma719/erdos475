# Cyclotomic zipper constructions (supplied by GPT 2026-11-22; AUDITED IN-SESSION by Claude; referee gates pending)

**Double-transversal criterion.** p odd prime, h of order m>=2, d=(p-1)/m, H=<h>, base block (u_0..u_{d-1}), U=Σu_i, P_i=Σ_{j<i}u_j, X=U/(h−1). B=(u_0..u_{d-1}, hu_0.., ..., h^{m-1}u_0..) is a rotational sequencing of F_p^× iff {u_iH} and {(X+P_i)H} are both complete coset transversals. (Vertices S_{dj+i}=(X+P_i)h^j−X.)
**Quadratic zipper theorem (d=2).** C={u,v,w}, ΣC≠0, s=u+v∉C∪{0}, q=v/u, t=w/s; q,1+q,t,1+t nonresidues and h=qt of order (p−1)/2 ⇒ F_p^×∖C has a valid ordering (B=(u,v,uh,vh,..) contains disjoint consecutive pairs (u,v),(s,w); apply the zipper lemma).

**Claude audit (no API).**
- Algebra re-derived by hand: S_{2j}=X(h^j−1), S_{2j+1}=(X+u)h^j−X; (X+u)/X=q(1+t)/(1+q) is a nonresidue; s/v=(1+q)/q is a residue so s=vh^j and the next label is sh/q=st=w; disjointness of the blocks (j=0 forces u=0; j=m−1 forces w=u).
- Independent implementation (experiments/audits/cyclotomic_independent.py): criterion iff verified with 0 mismatches over 3,131,988 (p,h,block) cases (p=7,11,13, d<=3 at p=17); quadratic theorem: every instance for 23<=p<=101 (total >190,000 triples-orderings) builds a valid ordering, 0 invalid.
- COVERAGE of the quadratic corollary alone (generic dilation classes): 14/57 (p=23), 16/100 (29), 22/117 (31), 23/176 (37), 33/222 (41), 42/247 (43), 80/301 (47), 70/392 (53), 133/495 (59), 55/532 (61), 119/651 (67), 149/737 (71), 99/782 (73), 190/925 (79), 280/1027 (83), 208/1190 (89), 176/1426 (97), 228/1552 (101): roughly 25% falling to ~15% — a sufficient condition covering a thin, non-uniform fraction.
- GPT's index-4 coverage figures (87/100 at p=29 etc.) were NOT independently reproduced here.
**Conclusion.** Correct theorem; not enough alone for NC3C (GPT says so too). Priority: this is an instance of cyclotomic complete mappings (Bors–Wang, Niederreiter–Winterhof).
