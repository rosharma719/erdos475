# Round: finish the tight family with the HALF-WALK method (non-zigzag; this is what Graham needs)

New proved results (Claude, research/claims/claude_lane.md):
- Half-walk lemma: delta = signed ordering of S\{c}, partial sums D (D_0=0) distinct with D ∩ (D+c) = ∅  =>
  W=(delta, c, -delta^rev, -c) is a valid cycle for ±S, range c+spread(D). Adjacent same-sign steps can be merged.
- THEOREM (a=1, every M): spiral delta=(1,-2,3,...,±(M-1)), c=M, merge the final (-1,-M) -> -(M+1).
  P=[1,M], N={2..M-1,M+1}, range 2M-1. No zigzag rule needed; no number theory.
- For a>=2 (range <= 2M+2, which suffices for every admissible prime p >= 2M+3): c=M is forced, the merged pair must be
  an internal jump 0 -> w -> M+1 (w in {a,b}), and D is (A) {0}∪[2,M-1]∪{M+1} or (B) {-1,0}∪[2,M-2]∪{M+1} (or mirror).
  Equivalently: a Hamiltonian path on D with edge lengths exactly {1,...,M-1}, containing the consecutive triple (0,w,M+1).
  Explicit solutions for every a>=2, M<=13 are listed in claude_lane.md (L8 data).

TASK: give an explicit family of such Hamiltonian paths for ALL M and all 2<=a<(M+1)/2 (case split by parity/residue
of M and a is fine), with a complete proof that the edge lengths are exactly {1..M-1}. Graceful-path/zigzag gadgets:
the inward zigzag s,t,s+1,t-1,... on [s,t] uses labels t-s,...,1; removing its low vertex x deletes exactly the label
t+s+1-2x. The data show a short header through 0, M+1 and the extreme core points carrying labels M-1,M-2,M-3,a,b,
followed by a modified zigzag. Deliver proof + stdlib verifier for M<=200.

This closes the tight family for Graham. Then: use the same lemma (merging adjacent same-sign steps of half-walk cycles)
to attack the reduction from arbitrary balanced pairs; the zigzag rule should be dropped everywhere.
