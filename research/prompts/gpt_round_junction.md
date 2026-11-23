# Next round: the JUNCTION half-walk with offset c = a (simplest closing route for small a)

Verified this round: your lift classification (86 certificates, 0 mismatches), the branch audit's divisibility theorem.

New construction (Claude, L20). delta = signed ordering of [1..M]\{a}, FIRST step +b (b=M+1-a), partial sums D distinct,
D ∩ (D+a) = ∅, spread(D) <= 2M+2-a. Then W=(delta,+a,-delta^rev,-a) ends with (-b,-a); merge to -(M+1): valid ordering
of the tight pair, range <= 2M+2. No internal jump; the merge is at the seam. (a=1 is the spiral theorem.)
Exact SAT (complete) finds such half-walks for a=2,3,4 at M=24,30,40,50, and a coverage scan M=8..27 covers EVERY tight
pair by: junction c=a whenever a | M,M+1,M+2 or M+3; otherwise internal c=M.
For a=2 the vertex sets look like unions of adjacent pairs {x,x+1} spaced by 3 (no two points at distance 2), e.g. M=20:
D = {0,1,4,7,8,11,14,15,18,19,22,23,26,27,31,32,35,36,39,40}.

TASK: prove (J): for a=2,3,4 and every M (and for general a with a | M+j), give an explicit delta (pairs/blocks
structure, case split by M mod 2a or so) with full proof that the labels are [1..M]\{a}, D is distinct with no two
points at distance a, and spread <= 2M+2-a. Verifier for M<=400. Together with a=1 this settles all a<=4 for every prime.
