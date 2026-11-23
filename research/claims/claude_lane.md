# Claude's own analytic lane (not audits)  — 2026-11-22

## L1. Minimal-hole lemma (proved)
For balanced P != N write h = maxP + maxN - |P| - |N| (unused points of the window [1-maxN, maxP]).
Then h >= 2, and h = 2 iff (up to swapping P,N) P=[1,M], N=[1,M+1]\{a,b}, a+b=M+1, a!=b.
Proof. Let gP = maxP-|P|, gN = maxN-|N| (missing elements below the max). h = gP+gN.
(0,0): both intervals, equal sums => equal. (0,1): P=[1,m], N=[1,n]\{c}, c<n: n(n+1)/2-m(m+1)/2=c in [1,n-1];
m<=n-1 gives >=n, m>=n gives <=0. (1,1): P=[1,m]\{x}, N=[1,n]\{y}; m=n => x=y; m<n => n(n+1)/2-m(m+1)/2=y-x<=n-2 < n.
(0,2): P=[1,m], N=[1,n]\{a,b}: a+b = n(n+1)/2-m(m+1)/2 in [3,2n-3] forces m=n-1, a+b=n. QED.
So the tight family is exactly the rigid extreme, and any proof of Z-asym must contain a proof for it.

## L2. Two-ruler reformulation (proved; corrected)
Let A = prefix sums of the positive order (excluding 0), B = prefix sums of the negative order, both in (0,S].
The walk always advances the lagging pointer, so the states are: for z in (B∪{0})\{S} as lagging pointer,
vertex next_A(z) - z > 0; for z in A\{S}, vertex z - next_B(z) < 0 (next_R(z) = least point of R greater than z);
plus the initial vertex 0. Hence
zigzag exists <=> rulers A,B with gap sets P,N, A∩B={S}, such that the forward distances to the next point of the
OTHER ruler are pairwise distinct over B∪{0} (below S), and pairwise distinct over A (below S).
Structured ruler orders (monotone, parity blocks, hi-lo interleaves, rotations) fail for all M>=6 in the a=1 family
(experiments/irc/shapes.py), so the rulers of real solutions are not of simple shape.

## L3. Label-preserving moves and parity (proved)
Swapping the successors of two same-side sources t,t' (delta=t-t') turns their labels L1,L2 into L1+delta, L2-delta;
no single swap preserves labels. Two swaps (t,t'),(r,r') on one side preserve labels iff r'=r-delta... precisely
r - r' = -delta, L(r) = L(t)+delta, L(r') = L(t')-delta. In a single affine piece f(x)=2x+c this forces 4*delta=0,
so moves need >=2 pieces with 4*delta = c_{t'}+c_r-c_t-c_{r'}.
Any product of an even number of transpositions preserves the parity of the cycle count, so such double swaps can
only change the number of cycles by an even amount.
Observation (exhaustive, M=5,6, a=1): covers of BOTH parities exist for the same holes, so parity is not an invariant
of the labels; a joining argument therefore needs odd moves as well, which must change the holes.

## L4. Size of the cover space (exhaustive, a=1)
All label-exact zigzag-sign cycle covers (any holes): M=6: 71, M=7: 162, M=8: 369 (about x2.2 per step);
Hamiltonian among them: 19, 51, 56. Covers deviate from doubling at about M of 2M sources and use 4-10 affine pieces.
Exponentially many covers, with a single-cycle fraction of 0.15-0.3, far above the 1/(2M) of a random permutation.
This is the quantitative fact a counting proof would have to establish.

## L5. The tight family is an artefact of the integer reduction (strategic, proved)
In Graham's setting a pair (P,N) comes from a prime p with maxP+maxN <= p-1, and an ordering is valid as soon as its
partial sums are distinct mod p; range <= p-1 suffices. For the tight pair maxP+maxN = 2M+1 is odd, so p >= 2M+3 and
range up to 2M+2 = maxP+maxN+1 is allowed, without any sign rule. Z-asym/IRC demand range <= 2M, which is what makes the
tight family rigid (window filled except 2 holes). At p = 2M+3 the set A has size p-4 (near-complete regime).
General version: Graham's conjecture follows from
  IRC+ : every balanced pair has an ordering with distinct partial sums and range <= maxP+maxN when maxP+maxN is even,
         and <= maxP+maxN+1 when it is odd,
together with the symmetric IRC theorem. IRC+ drops the zigzag rule and gains 1–2 units of room; with 4 holes instead
of 2 the tight family is no longer rigid. Next target (mine): generalise the symmetric walk (delta, M, -delta^rev, -M),
which is non-zigzag, to asymmetric pairs using that room.

## L6. Half-walk lemma (proved)
Let S be a set of positive integers, c in S, and delta a signed ordering of S\{c} (each element once, either sign)
with partial sums D_0=0, D_1, ..., D_{m-1}. If the D_k are distinct and D ∩ (D+c) = ∅, then
W = (delta, +c, -delta^rev, -c) is a valid cycle for ±S: its proper vertices are D_0..D_{m-1}, then
c+D_{m-1}, ..., c+D_0. Range = c + spread(D). Any two consecutive same-sign steps of W may be contracted to their
sum (deletes one vertex, keeps validity, range does not increase).
(The symmetric IRC walk is the special case delta = descending alternating path, c = max S.)

## L7. THEOREM: the a=1 tight family satisfies IRC, for every M (proved)
P=[1,M], N={2,...,M-1,M+1}. Take S=[1,M], c=M, delta = (+1,-2,+3,-4,...,±(M-1)) (spiral).
D = {0,1,-1,2,-2,...} = M consecutive integers, so D ∩ (D+M) = ∅ and L6 applies. The last two steps of W are
(-1, -M); contracting them gives -(M+1). Labels: positives [1,M]; negatives [1,M]\{1,M} ∪ {M+1} = N.
Range = M + (M-1) = 2M-1 <= maxP+maxN-1. So this pair (the most rigid Z-asym case, where the zigzag route only
gave Artin-conditional results) has an explicit valid ordering for every M, hence for every prime p >= 2M+3.
Verified independently M=4..15 (junction.py).

## L8. Structure forced for a>=2 (CORRECTED: (i) holds only under spread(D)<=M+2; GPT found c=1 half-walks, e.g. M=5,a=2)
In any L6-construction for the tight pair with range <= 2M+2: (i) c=M (since |D|=M forces c>=M when spread(D)<=M+2);
(ii) the contracted pair must be internal to delta: two consecutive equal-sign steps of sizes a,b, i.e. a jump of
M+1 through an intermediate vertex; (iii) up to reflection and translation D is
 (A) {0} ∪ [2,M-1] ∪ {M+1}            (range 2M+1), or
 (B) {-1,0} ∪ [2,M-2] ∪ {M+1}, or its mirror (range 2M+2),
with the jump 0 -> w -> M+1, w in {a,b}. Both ranges are <= p-1 for every admissible prime p >= 2M+3.
For (A) with a>=4 this reduces to a two-path graceful problem: on [0,n]\{w-2}, n=M-3, find two disjoint paths
starting at {n,1} or {n-1,0} covering everything with edge lengths exactly {1..n}\{a, n+4-a}.
Exact search finds L6-constructions for every a>=2 and M<=12 (halfwalk.py). OPEN: explicit family for all M.

## L8 data: explicit half-walks (template A/B) for every a>=2, M<=13 (experiments/irc/tmpl2.py)
Path on D (vertex order of delta; translate so that the first vertex is 0):
 9: a2 [4,10,2,0,7,3,8,5,6]  a3 [4,5,7,2,8,0,3,10,6]  a4 [2,7,5,6,3,10,4,0,8]
10: a2 [5,8,4,9,3,11,2,0,7,6]  a3 [4,8,6,7,2,9,0,3,11,5]  a4 [2,8,3,11,4,0,9,6,7,5]  a5 [2,9,0,5,11,3,6,4,8,7]
11: a2(B) [-1,7,4,8,3,9,0,2,12,5,6]  a3 [4,9,5,12,3,0,10,2,8,6,7]  a4 [2,9,3,12,4,0,10,5,8,6,7]  a5 [2,10,0,5,12,3,9,6,4,8,7]
12: a2(B) [0,2,13,5,8,-1,9,4,10,3,7,6]  a3 [5,9,4,10,2,11,0,3,13,6,8,7]  a4 [3,11,5,10,0,4,13,2,9,6,8,7]  a5 [2,11,0,5,13,3,10,4,8,7,9,6]  a6 [3,11,2,13,6,0,10,9,4,8,5,7]
13: a2(B) [3,6,10,-1,9,4,11,5,14,2,0,8,7]  a3 [6,10,5,11,4,12,2,14,3,0,9,7,8]  a4 [5,10,7,8,6,12,3,11,0,4,14,2,9]  a5 [2,12,0,5,14,3,11,4,10,6,9,7,8]  a6 [3,12,2,14,6,0,11,4,7,8,10,5,9]
Recurring shape: a short "header" through the outliers (0, M+1) and the extreme core points carrying the labels
M-1, M-2, M-3, a, b, followed by an inward zigzag on a core interval with one vertex removed. Lemma used: the inward
zigzag s,t,s+1,t-1,... on [s,t] with the low vertex x removed uses every label 1..t-s except t+s+1-2x.

## L9. Single-zigzag template is too narrow (exhaustive within template, experiments/irc/header_zig.py)
Half-walk = header (outside points of shape A + jump) + ONE inward zigzag on a core [s,t] with one vertex removed:
solutions only at (M,a)=(16,6),(17,6) among all 2<=a, M<=24. The general family must combine >=2 zigzag blocks
(each block uses a consecutive label range; removed vertices delete single labels) or be recursive in M.
Note: GPT's "common-pair insertion" reformulation (P=C∪{a,b}, N=C∪{a+b}) is the same problem: the half-walk lemma is
exactly a way of inserting all common pairs ±C at once (as a mirrored half-walk), with the core ({a,b},{a+b}) realised
as the internal jump.

## L10. General pairs: the mirrored overlay construction (proved framework)
Given balanced P,N (any sets), choose orders of P and N, lay both as interval partitions of [0,W] and overlay the cut
points; the pieces form a multiset S with every P-element and every N-element a union of consecutive pieces
(common elements c in P∩N may be kept whole as their own pieces). If the pieces are distinct, build
W = (delta, c, -delta^rev, -c) over S where each overlay component (maximal chain of overlapping P- and N-blocks) is a
consecutive same-sign run of delta in overlay order. Merge every P-block among the positive steps and every N-block among
the negative steps. The result is an ordering of +P ∪ -N.
Validity needs ONLY the surviving vertices (block boundaries) to be distinct: D at P-block boundaries for the first half,
c+D at N-block boundaries for the second, with no cross collision. This is strictly weaker than requiring the full
symmetric walk to be valid, which is what the earlier GSW coverage tests demanded (coverage fell to 0/30 at p=37, k=22).
L7 (tight a=1) and L8 (tight a>=2) are the special case S=[1,M], one component {a,b | a+b}.
NEXT TEST: coverage of dense zero-sum sets (p=37..47, k ~ 0.5p-0.8p) by the relaxed (surviving-vertex) condition, mod p.
If it covers the dense regime where GSW failed, this becomes the general route.

## L11. TWO-CLUSTER LEMMA — RETRACTED AS A NEW CONJECTURE (tautological in its relaxed form)
RETRACTION (2026-11-22): any valid cycle, rotated to end with -d, has the form (A,+c,B,-d) with A,B self-avoiding and
V(A)∩(V(B)+d)=∅. So relaxed TC (cross-condition + Graham range) is EQUIVALENT to IRC+ itself; the 'evidence' below is
only evidence for IRC+. The non-trivial 'clean' version (both arcs inside one window of length <= d-1) FAILS: exhaustive
search (twocluster.py) finds none for tight a=2, M=4..8. Do not use TC as a target. Original text kept below for the record.
Lemma. Let P,N be balanced, c = max P >= d = max N (else negate), Delta = c-d, T = (P\{c}) ∪ -(N\{d}).
Suppose T is split into two sequences A, B with A a path 0 -> e1 and B a path e1+Delta -> 0 (endpoints automatic:
sum T = -Delta), such that (i) A has distinct vertices, (ii) B has distinct vertices, (iii) V(A) ∩ (V(B)+d) = ∅.
Then W = (A, +c, B, -d) is a valid ordering of +P ∪ -N: its vertices are V(A) (cluster 0), then c+e1 = d+(e1+Delta),
then d+V(B) (cluster d). If moreover all of V(A) ∪ V(B) lies in an interval of length <= d-1, (iii) is automatic and
range(W) <= 2d-1 <= maxP+maxN-1 (IRC). Graham needs only range(W) <= maxP+maxN (+1 if that is odd).
NOTE: the arcs A and B may share vertices; only the shifted cross-condition (iii) is needed.
Conjecture TC: every balanced pair admits such a split (with the Graham range bound).
Evidence (exact DFS, experiments/irc/twocluster2.py): all tight pairs M<=11 (every a); 150/150 random dense balanced
pairs with elements <=14; 118/120 at elements <=18 (2 timeouts, 0 failures). No failure found.
Special cases: L7 and L8 are TC with A and B mirror images; GPT's 13.1 (p+q>W) is TC with monotone arcs.

## L12. Outward arcs (explicit gadget; partial)
A walk is OUTWARD if every new vertex is a new max or new min. Outward walks are automatically self-avoiding:
continuing in the same direction from the current extreme is always allowed; reversing needs |step| > current spread.
(Spiral = all reversals with increasing magnitudes; spread = largest step.) Restricting TC to arcs that are outward
from one of their ends (experiments/irc/outward2.py): works for all tight M<=6 and most M=7,8, but fails exhaustively
at (M,a)=(7,3). So two outward arcs are not always enough; arcs need at least one more level of structure.
Reduction note: if (P\{c} ∪ {Delta}, N\{d}) had a valid ordering of range <= d-1, cutting it at +Delta would give TC;
that is too strong in the dense case (it would need maxP''+maxN'' <= maxN), which is why the arcs must be allowed to overlap.

## L13. Toward an all-M proof of the B-shape lemma (a>=2)
- Audit: all 90 GPT B-certificates (M=4..21) re-lifted with own code (experiments/irc/audit_B.py): 90/90 valid tight
  cycles, range 2M+2. Data in research/data/B_certs.py.
- Stable frame: for fixed a the certificates share a frame around the jump that translates with M, e.g.
  a=2: (6, M-4, 5, M-3, 3, M-2, 0, 2, M+1, 4) for M=18..21; a=3: (5, M-3, 0, 3, M+1, 2, M-2, 4) for M=18..21.
  The rest is an irregular middle part.
- Frame/core split with a classical graceful core: the inner interval [s,s+n-1] carries labels 1..n-1 as a graceful
  path, entered by a connecting edge of label n; the frame carries labels n+1..M-1. The core end is then covered by
  Cattell's theorem (Discrete Math 2007): every vertex of P_n can receive every label allowed by parity, except leaves of
  P_{4k}. Frames with strictly decreasing labels do not exist (frame_search.py); unrestricted frames exist for n=a-1
  when a is small relative to M (frame2.py: e.g. (14,5) with n=4) but not for a near M/2.
- Induction "shift the top half by +1 and attach the new vertex at an end" (exact rule that grows a zigzag) rarely
  applies to the certificates (grow.py); consecutive certificates differ by such a shift plus a small local change, so a
  proof by induction needs one extra local move.

## L14. B-shape solutions are inward zigzags with O(1) local defects (data; experiments/irc/edgedfs.py)
Edge-by-edge search assigning labels from the top down (fixed jump edges 0-a, a-(M+1), smallest low endpoint first)
gives canonical B-paths whose label->edge tables are, in M-relative coordinates, IDENTICAL across M for fixed a in the
top part, and then an inward zigzag (x, M-x-c) with consecutive labels, interrupted by a bounded number of fix-ups
(an edge into M+1 from the middle, the jump edge 0-a, and an end gadget). Example a=6, M=28:
 1:-1~M-2 2:-1~M-3 3:0~M-3 4:2~M-2 5(b):6~M+1 6:2~M-4 7:3~M-4 8:3~M-5 9:4~M-5 10:4~M-6 11:5~M-6 12:5~M-7
 13:M-14~M+1 14:7~M-7 ... 21:10~M-11 22(a):0~6 23:11~M-12 24:11~M-13 25:12~M-13 26:M-14~M-12 27:12~13
(entry "k:x~y" = edge of length M-k). Tables for a=4..10 at M=28..40: research/data/B_canonical_tables.txt.
Greedy ordering fails for a=2,3 and for some parities, so the uniform family needs a case split, but the structure
(zigzag + O(1) gadgets) is the shape of an explicit all-M proof.
Also audited: GPT two-merge family (k=7..399, 0 failures); GPT forced bridge J (candidate edge lists checked by hand).

## L15. Universal header + zigzag ladder (data) — CORRECTED: only (M+1,a,0,M-3,-1,M-2) is common to all a; the continuation 2,M-4,3,M-5 holds only for some a (GPT: for a=4,5,7,8,9 it would repeat the label b). ALSO SUPERSEDED for small a by L18 (B-shape impossible when floor(M/2)>2a+7).
Canonical descending-label B-paths for a=4..11, M=24..33 all contain the header
(M+1, a, 0, M-3, -1, M-2, 2, M-4, 3, M-5) and are otherwise ladders of inward zigzag blocks joined by links whose labels
continue the consecutive run; label gaps occur only at skipped vertices/shifted boundaries, and b=M+1-a fills one.
This is the template for an explicit all-M construction (handed to GPT: prompts/gpt_round_ladder.md).
GPT round (multimerge, rainbow spanning tree): checked, correct, but both avoid the dense Hamiltonicity problem.

## L16. Template test: header + long right zigzag + searched left part (experiments/irc/template.py)
Fixing the header (M+1,a,0,M-3,-1,M-2,2) and forcing a LONG inward zigzag after 2 leaves a left part that the search
cannot complete except with a short tail (a=10: M=22 needs a 12-vertex left part; M>=26 times out). So the long run must
sit on the LEFT of M+1 as a ladder of blocks (as in L15), not as a single zigzag after 2. Consistent with L15; the ladder
parametrisation (block sizes, attachment point, end gadget) is the remaining design problem (GPT prompt gpt_round_ladder.md).

## L17. General pairs: SYNCHRONIZED-WALK form of the mirrored overlay half-walk (proved equivalence; experiments/irc/syncwalk.py)
Let c ∈ P∩N, P\{c} = P1 ⊔ P2, N\{c} = N1 ⊔ N2. Let X be a walk 0->e with steps +P1, -N1 and K a walk 0->e with steps
+N2, -P2. Then (X, +c, -K^rev, -c) is a valid ordering iff X and K are self-avoiding and V(X) ∩ (V(K)+c) = ∅.
(Unstructured, this is just a rotation of any cycle containing ±c — tautological.)
STRUCTURED version (= mirrored overlay half-walk with merges, L10): additionally X and K are CO-MONOTONE, i.e. both are
coarsenings of one walk delta (between consecutive X-vertices, and between consecutive K-vertices, delta moves
monotonically). Then W comes from (delta, c, -delta^rev, -c) by merging; only block-boundary vertices must be distinct.
Covers symmetric IRC (X=K), tight a=1 (spiral), tight a>=2 (B-shape: X has +a,+b, K has +(M+1)), GPT's two-merge and
multimerge families. Restrictiveness: only 29% of cross-valid (X,K) pairs are co-monotone (12,694/44,402, small cases).
Evidence: all 51 random balanced pairs with a common element (3-5 elements per side, values <=12) have a structured
solution with the Graham range; tight M<=6 all a. Small cases only — larger tests need a non-brute-force search.
Lemma (proved): for the tight family with a>=2, delta cannot be an OUTWARD walk (every new vertex a new extreme): the
merged run (a,b) must come last with spread < b before it, but all magnitudes up to M-1 are used earlier.
OPEN: (i) pairs with P∩N = ∅ (pivot must be a piece); (ii) existence of co-monotone pairs in general.

## L18. GPT's length obstruction: the c=M half-walk FAILS for small a (verified)
Total edge length forces M(M-1)/2 <= 2*sum_{x in D\{a}}|x-m| - 1 (triangle inequality through a centre m, after
merging 0-a-(M+1) into the monotone edge 0-(M+1)). Own computation with the optimal centre (M<80): the B-shape is
impossible exactly when floor(M/2) > 2a+7 (first case M=24, a=2; 420 cases, all predicted by GPT's inequality), and the
A-shape already fails from (M,a)=(12,2). Since A and B are the only shapes with c=M and spread <= M+2 (L8), the c=M
half-walk cannot cover the tight family for a << M. Consistent with my data: canonical search returned None for a=2,3.
Consequences: (i) the "B-only lemma" is false in general; (ii) for a >= (floor(M/2)-7)/2 it may still hold;
(iii) small a needs another offset (c=1 has room: the same bound is far from tight there) — testing c=1 at M=24..30.
a=1 is unaffected (spiral, junction merge, L7).

## L19. Which offsets c are possible at all (proved) + GPT's 3-shape obstruction (verified)
GPT extended L18 to all three c=M shapes A, B, C={0}∪[3,M-1]∪{M+1,M+2}; own check (optimal centre, M<120, a>=3 for C
since 2∉C): every case with floor(M/2)>2a+7 is excluded. GPT's c=1 certificate for (M,a)=(24,2) verified with own code:
valid tight cycle, range 50.
Lemma (offset window). A tight half-walk with offset c needs |D|=M, D∩(D+c)=∅ and spread s <= 2M+2-c. If
(2M+3)/3 <= c < M then s+1 <= 2c, the pairs (x,x+c) inside the window are disjoint, and an independent set has size
<= c < M. Hence c ∈ [1,(2M+2)/3] or c = M. Combined with L18: for small a the offset must satisfy c <= ~2M/3; c=1 is
the natural choice (length bound slack ~ M^2/2).
