# Next round: write down the explicit all-M B-shape family (zigzag + bounded gadgets)

Audit of your last round: two-merge family OK (k=7..399), forced bridge J OK, C1 identities OK.

Key new data (Claude, claims/claude_lane.md L14, tables in research/data/B_canonical_tables.txt):
assigning labels from the top down (fixed jump edges 0-a and a-(M+1)), the canonical B-path for fixed a has the SAME
label->edge table in M-relative coordinates for every large M, and its middle is an inward zigzag
x ~ M-x-c with consecutive labels, broken only by O(1) gadgets (an extra edge into M+1, the jump edge 0-a, end piece).
Example a=6, M=28 (k:x~y means an edge of length M-k):
 1:-1~M-2 2:-1~M-3 3:0~M-3 4:2~M-2 5(b):6~M+1 6:2~M-4 7:3~M-4 8:3~M-5 9:4~M-5 10:4~M-6 11:5~M-6 12:5~M-7
 13:M-14~M+1 14:7~M-7 15:7~M-8 ... 21:10~M-11 22(a):0~6 23:11~M-12 24:11~M-13 25:12~M-13 26:M-14~M-12 27:12~13

TASK: turn this into a theorem. For each residue class of (M mod 2, a mod 2) (and small exceptional a), define the path
explicitly as: header + inward zigzag segments + the gadgets (with positions given as functions of M and a), and PROVE that
the edge lengths are exactly {1,...,M-1} and the vertex set is exactly {-1,0}∪[2,M-2]∪{M+1} with 0,a,M+1 consecutive.
Handle finitely many small (M,a) by the 90 certificates. Deliver: proof + stdlib verifier checking the formula for all
M<=400 and all a. This closes the tight family for every prime.
