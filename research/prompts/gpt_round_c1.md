# Next round (after your half-walk round) — and a correction from Claude

Corrections:
1. You are right: c=M is forced only under spread(D) <= M+2. Your c=1 example (M=5,a=2) is checked.
2. Claude's 'two-cluster conjecture TC' is WITHDRAWN: in its relaxed form it is just a rotation of any valid cycle, i.e.
   equivalent to IRC+ itself; its clean form fails for tight a=2. Do not use it. Please flag any statement of yours that is
   equivalent to the target after rotation/translation — that trap is easy to fall into.

Task (pick the route you judge closer; report which):
 (B) Prove the B-only lemma: for all M>=4, 2<=a<(M+1)/2, there is a Hamiltonian path on {-1,0}∪[2,M-2]∪{M+1}
     with edge lengths exactly [1,M-1] containing 0,a,M+1 consecutively.
 (C1) Prove the c=1 route: D has no two consecutive integers, spread <= 2M+1, so it is <=4 step-2 progressions.
     Suggested normal form: D = {0,2,...,2k} ∪ {2k+3,...} (one gap of 3). Then even steps stay inside a parity class and
     odd steps cross classes (upward from the lower class). In class coordinates this is a two-ruler problem; give an
     explicit family (case split by parity of M, a) with full proof.
Either closes the tight family for every prime p >= 2M+3. Deliver: proof + stdlib verifier for M<=300.
Then, separately: what is the analogue of the half-walk for a pair with TWO merged blocks (P=S, N=S with two disjoint
merges), as a first step towards general pairs?
