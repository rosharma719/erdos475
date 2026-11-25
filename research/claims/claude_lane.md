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

## L20. Junction half-walk with offset c=a; exact SAT for half-walks (experiments/irc/halfwalk_sat.py, hw_scan.py)
Construction (proved validity): delta = signed ordering of [1..M]\{a} with FIRST step +b (b=M+1-a); D distinct,
D ∩ (D+a) = ∅. Then W = (delta, +a, -delta^rev, -a) ends with (-b,-a); merging gives -(M+1) and exactly the tight pair
P=[1,M], N=[1,M+1]\{a,b}. Range = a + spread(D) <= 2M+2 required. (a=1 is the spiral theorem L7 with roles of c swapped.)
Packing (divisibility theorem, branch audit): c=a is admissible only if a | M, M+1, M+2 or M+3 — always true for a<=4.
Exact SAT (complete; UNSAT = no such half-walk) finds junction c=a half-walks quickly: a=2,3,4 for M=24,30,40,50
(<=15 s each). Coverage scan (first admissible of: junction c=a; internal c=M; internal c=1,2,3), M=8..27, every a:
EVERY tight pair covered (j_a when a | M..M+3, else internal c=M). Scan continuing to M=45, where c=M is excluded for
small a (floor(M/2) > 2a+7), to test the small offsets there.
Target theorem: (J) for every a>=2 with a | M+j (0<=j<=3) a junction c=a half-walk exists; (B) remaining a are large
enough for c=M, or need c=1,2,3 internal.

## L21. GPT's aligned c=1 ladder (a=2) and H_k; zigzag structure of H_k (experiments/irc/hk.py)
GPT: for a=2, c=1, aligned single-gap D, the odd labels force a ladder; M=0 mod 4 impossible, M=4k+2 equivalent to
H_k = Hamiltonian path on {-k-1..-1}∪{2..k+1} from k+1 with labels 2..2k+1 (witnesses k<=19; proof read, correct).
Own search: H_k = inward zigzag k+1,-k,k,-(k-1),... (labels 2k+1, 2k, ... consecutive) + a tail that contains the outlier
-(k+1). Tail sizes grow (~k/3 for k=4..19), so H_k is not "zigzag + bounded gadget". The full zigzag uses labels 2k+1..3 on
all vertices except -(k+1) and misses label 2; the outlier can only attach from a negative inner vertex x with label
k+1-|x| in [k/2,k]. So H_k reduces to a half-size graceful problem on the inner block with one prescribed end and one
missing label — a natural recursion (Cattell-type) to formalise.
Scan (hw_scan.out): every tight pair M<=33 covered by junction c=a / internal c=M / internal c=1.

## L22. Recursion for H_k: a proved infinite family (experiments/irc/frec.py, fchain.py)
Generalised problem F(al,be): Hamiltonian path on [-al,be]\{0,1} with labels {2,...,al+be-1} (all but the maximum),
starting at the top be ("T") or bottom -al ("B"). H_k = F(k+1,k+1,T). Reflection x -> 1-x: F(al,be,B) ≅ F(be-1,al+1,T).
REDUCTION LEMMA (proved). If s = al+be ≡ 1 (mod 3), r = (s-1)/3, then
  be, -(al-1), be-1, -(al-2), ..., be-r+1, -(al-r)   (inward zigzag, labels s-1 down to s-2r+1)
  -> -al (detour, labels r and r+1 = s-2r-1, s-2r)
  -> an F(al-r-1, be-r, B) path (labels 2..s-2r-2),
is a solution of F(al,be,T). Proof: the zigzag labels are consecutive; -(al-r) -> -al has label r, -al -> -(al-r-1) has
label r+1, and r+1 = s-2r and r = s-2r-1 exactly when 3r = s-1; the inner vertex set is [-(al-r-1), be-r]\{0,1}
and its label set {2..(al-r-1)+(be-r)-1} = {2..s-2r-2} is what remains. The inner sum is s' = s-2r-1 = r.
COROLLARY (proved, with finite base). F(al,be,T) is solvable whenever the chain s -> (s-1)/3 -> ... stays ≡ 1 (mod 3)
until it reaches a sum <= 30 whose instance is solvable (exact DFS). In particular H_k for k = 4, 6, 19, 181, ...,
and so the tight pairs (M=4k+2, a=2) for those k, for every prime p >= 2M+3. Verified constructively for k=181 (M=726).
GAP: s ≡ 0, 2 (mod 3). The zigzag-from-top rule with a gadget of <=2 extra vertices gives no reduction there
(frec2.py: 87 of 100 instances with s in [10,24] have none). Need reduction gadgets for the other residues.

## L23. AUDIT: GPT's proof of H_k for all k >= 2 — ACCEPTED (candidate, ready for referee)
Generalised problem Q(s;d,e) on B_s = [-s,-1] ∪ [2,s+1]: start e, lengths [2,2s+1]\{d}. States F=(2,s-1), T=(2s+1,-s),
C=(2s,-s+1), D=(2s-1,-s+2). Recursions F_s -> F_{s-3}; T_s, D_s -> F_{s-4}; C_s -> F_{s-3}; 12 seeds; then
H_k = (k+1,-k,...,s+2,-(s+1), -(k+1), Q(s; s+j+1, -j)) with k = 2s+j+1, j in {s, s-1, s-2} by k mod 3.
Checked by hand: all four header edge sets (incl. connector) and vertex sets; the H_k assembly (zigzag lengths
2k+1..2s+3, detour lengths k-s = s+j+1 and k+1-j = 2s+2). Own independent implementation
(experiments/audits/hk/audit_hk.py): F,T,C,D valid for all s <= 1499; H_k valid for all k = 2..3000; end-to-end tight
cycles (M=4k+2, a=2, c=1 aligned ladder) valid with range <= 2M+2 for k = 2..400.
THEOREM (now proved, modulo referee): the tight pair P=[1,M], N=[1,M+1]\{2,M-1} has a valid ordering for every
M ≡ 2 (mod 4), M >= 10, hence for every prime p >= 2M+3. With L7: a=1 all M; a=2 all M ≡ 2 (mod 4).
This is the recursion of L22 made complete (four states instead of one).

## L24. Global plan for arbitrary sets: how symmetric are the lifted pairs? (experiments/irc/core_density.py)
For random zero-sum A ⊂ Z_53^*, minimising over dilations the asymmetric remainder r = |P0|+|N0| (P0=P\N, N0=N\P):
 density 0.20: r ≈ 8.2 of k=10 | 0.35: 11.6 of 18 | 0.50: 12.5 of 26 | 0.65: 11.2 of 33 | 0.80: 9.1 of 41 | 0.90: 5.4 of 46.
So after a good dilation, dense sets are NEAR-SYMMETRIC (core = P∩N carries most of the set; remainder ≈ (1-α)-proportion),
while sparse sets have lots of free room (p-1-k residues unused). This suggests a two-regime proof:
 (I) dense (α >= 1/2+ε): symmetric half-walk on the core (always exists: symmetric IRC) + splice the small remainder
     (threaded splicing / small-block absorption generalised to remainders of size ≈ free room);
 (II) sparse: an argument that uses the free room (Λ<1-type or a flexible greedy with proof);
 (III) the middle α ≈ 1/2 is where both are tight — the real crux.

## L25. SPLICE CONJECTURE (SPL) — strong structured evidence (experiments/irc/splice_test.py)
For zero-sum A ⊂ Z_p^*, choose the dilation minimising the asymmetric remainder; let C = P∩N (core) and R = (+P0) ∪ (−N0)
(remainder). Take the EXPLICIT symmetric IRC walk on ±C, W_C = (δ, c, −δ^rev, −c) with c = max C and
δ = (b2, −b3, b4, …) — fixed cyclic step order, free rotation — and insert the remainder steps at any positions, in any
order. SPL: some insertion has pairwise distinct partial sums mod p.
This is a genuine restriction (the 2|C| core steps must occur in W_C's exact cyclic order), not a reformulation.
Evidence (exact DFS): p=53 α=0.9: 10/10; α=0.8: 10/10; α=0.65: 7/7; α=0.5: 7/7 (remainders up to 14; larger skipped);
p=101 α=0.9: 8/8 (remainders 8–10). No failure.
If SPL is proved, Graham follows for every zero-sum A with a nonempty core (dense and middle densities); the
one-element reduction turns any A into a zero-sum set of the same size. Sets with an empty core after every dilation
are sparse and would need the separate sparse-regime argument.

## L26. Cut-and-place induction FAILS (experiments/irc/cutplace.py)
Rigid version of SPL: take a valid ordering U of the remainder, cut it into two arcs, put arc1 at the end of δ and arc2 at
the end of −δ^rev (W = δ, arc1, +c, −δ^rev, arc2, −c). Success (exact, <=300 orderings of U, all cuts): p=53
α=0.9: 0/12; α=0.8: 3/12; α=0.65: 2/3. Free insertion (SPL, L25) succeeded on all of these densities. So the remainder
must be spread through the core walk, not placed as two blocks; an induction "Graham(remainder) => Graham(A)" via two
seams is false in general. A proof of SPL needs a distributed insertion rule.

## L27. AVOID REDUCTION: the remainder goes AFTER the core walk (experiments/irc/splice_pattern.py, avoid_form.py)
SPL solutions found by exact search put one remainder step x1 just before the core's final −c and all other remainder
steps after the core walk. In that form, with V_C = vertex set of the explicit core walk (any rotation) and top = the
vertex before −c:
  W valid  <=>  U = (x1, x2, ..., x_r) is an ordering of the remainder R whose nonzero partial sums avoid V_C,
                and top + x1 avoids V_C ∪ V(U).
So Graham(A) <= "Graham with a forbidden set" for the SMALLER set R (r ≈ 0.45k at α=0.5), with forbidden set the
structured core vertex set (lower cluster D ⊂ [0,b2] ∪ upper cluster b1+D).
Evidence (exact, p=53, 12 random sets each): α=0.5: 12/12, α=0.65: 12/12, α=0.8: 12/12, α=0.9: 7/12 (near-complete
sets have too little free room; the free-insertion SPL form still worked 10/10 there).
Consequence: across middle densities the conjecture reduces to an obstacle-avoidance statement for a sparser set.
Λ-type union bounds are too weak (expected collisions ≈ r|V_C|/p ≈ 3 at α=0.5), so the avoidance statement needs to
use the cluster structure of V_C and the freedom in the rotation and the choice of x1.

## L28. Obstacle-avoidance threshold + a recursion that preserves occupancy (experiments/irc/avoid_threshold.py)
Test: random zero-sum R (size r) in Z_53^*, forbidden F (0 ∉ F), occupancy θ = (r+|F|)/(p-1); 15 trials each.
 random F:  θ <= 0.6 always solvable (r=6,10,14); θ=0.7–0.8 fails only for r=6 (10/15, 8/15).
 two-cluster F (like V_C): θ <= 0.5 always solvable; θ=0.6–0.8 failures grow for small r (r=6: 14,12,5 of 15).
So avoidance looks safe up to occupancy ≈ 1/2 for these obstacle shapes; larger r is MORE robust.
(Arbitrary F is false — F ⊇ R blocks the first step — so any lemma must use structure or translation freedom.)
RECURSION GO(θ): "zero-sum R with obstacles F, occupancy <= θ, has an ordering avoiding F". The AVOID step (L27)
replaces (R, F) by (remainder R', F ∪ V_C), and |V_C| = 2|C| = |R| - |R'|, so OCCUPANCY IS EXACTLY PRESERVED while the
set shrinks. An induction on |R| at fixed θ therefore needs only:
 (a) placement: some dilation/rotation/pivot makes the explicit core walk avoid F (naive counting is too weak:
     |F|·|V_C| bad incidences against |V_C| rotations — needs structure);
 (b) base: sets with EMPTY core under every dilation (genuinely sparse/asymmetric) avoiding F — e.g. minimal
     zero-sum (13.2), Λ<1, or a new argument.
For Graham itself F = ∅ and θ = k/(p-1); dense sets have θ > 1/2, where the free-insertion form (not AVOID) is needed at
the top level only.

## L29. Rigid recursive GO fails (experiments/irc/go_recursive.py)
Full recursion GO(R,F) using at every level the EXPLICIT alternating core walk (pivot = max core element, top 6
dilations, all rotations), AVOID insertion, brute force only when |R| <= 8: success without any fallback is rare —
p=53: α=0.5 1/8, α=0.8 5/8; p=101: 0/8 at α=0.5 and 0.8 (thousands of levels with no admissible placement). (An earlier
8/8 count was produced by a brute-force fallback and is not evidence.) So the single AVOID step works (L27, remainder
solved freely), but the placement lemma (a) is FALSE for the rigid explicit core walk at deeper levels: the explicit walk
usually hits the inherited obstacles. A working recursion must use flexible symmetric walks (any half-walk on the core,
any pivot — the symmetric IRC family is large) or a different obstacle-tolerant core construction.

## L30. Flexible-core recursion also fails (experiments/irc/go_flex.py)
Same recursion as L29 but the core half-walk at each level is SEARCHED (any pivot among the 4 largest, any signed order
δ with D, c+D distinct and avoiding the inherited obstacles), 4 best dilations, AVOID insertion, brute force only at
|R|<=8, no fallback: p=53 α=0.5: 0/6, α=0.8: 2/6 (hundreds of levels with no admissible step).
Conclusion: the AVOID step works at the top level only because the remainder is then solved without structure. Recursing
it turns the problem into obstacle-avoidance for ever sparser sets, and the structured core walks cannot carry the
obstacles. The occupancy-preserving recursion GO(θ) is not a viable proof route in this form. The general (non-tight)
case still needs a genuinely new mechanism for sparse/middle sets with obstacles.

## L31. a=2 for ALL M: junction c=2 with a two-phase pair shape (experiments/irc/junction_shape.py, js2.py, js3.py)
Junction half-walk, offset c=2 (a=2, b=M-1): delta = ordering of [1..M]\{2}, first step +b, D with no two points at
distance 2, spread <= 2M. SAT solutions have D = "pairs" {x,x+1} spaced by 4 with one phase shift. Restricting to the
explicit shape
   D = {4i, 4i+1 : 0<=i<L} ∪ {4L+2+4j, 4L+3+4j : j<U}  (+ one singleton at an end when M is odd),
translated so that the path starts at a vertex st with st+b ∈ D, exact SAT finds a valid half-walk for EVERY
M = 10..40, with L ∈ {1,2,3} (L=1 up to M≈21, then L=2, L=3 at M=38,40). Each gives a valid ordering of the tight pair
(a=2) with range <= 2M+2.
Why this shape: with no distance-2 pairs, D is at most about half of each parity class; pairs at phase 0 and phase 2 make
labels ≡ 0,1,3 (mod 4) available inside a phase and labels ≡ 2 (mod 4) only across the phase shift.
Next: forced-structure analysis on this shape (as GPT did for the aligned c=1 ladder) -> generalised states ->
recursion. That would prove a=2 for all M (covering M ≡ 0 mod 4 and odd M, which H_k does not).

## L32. a=3 and a=4 junction shapes (experiments/irc/js_a3.py; SAT patterns)
a=3 (c=3, D has no two points at distance 3): the shape
   m blocks {6j, 6j+1, 6j+2} (j<m) , gap 5 , then an alternating run of t = M-3m points (step 2)
(or the run first) admits a valid junction half-walk for EVERY M = 12..30, with m ∈ {2,3,4}. The long part is a single
step-2 progression — the same column structure as GPT's aligned c=1 ladder, so the forced-ladder argument should carry
over.
a=4 (c=4, no two points at distance 4): SAT solutions are built from two density-1/2 tiles of period 8, the block
"xxxx...." and the tile {0,2,3,5} mod 8 ("x.xx.x.."), e.g. M=19: xxxx....xxxx....xxxx....xxxx......xxx;
M=21: xxxx....x.xx.x..x..x.xx.x..x.xx.x....xxxx. Shape family not fixed yet.
Pattern across a: D is made of period-2a tiles of density 1/2 avoiding difference a, with one or two phase changes.

## L33. a=2, M = 8t+5: explicit template with ONE free gadget (experiments/audits/a2/template5.py)
From GPT's certificates (M=61,69,77,85) I fixed, as exact linear formulas in t, every part except one middle gadget:
 H  = 0, M-1, M-2, M-9
 Z1 = 4i, M-9-4i (i = 1..A)
 T  = -M+4t+4, -M+4t-7, -M+4t+8, -M+4t-11
 Z2 = -(4J+5), then (-M+4j+1, -(4j+5)) for j = J-1..0, J = t-3
 Z3 = (M-8-4i, 4i-1) for i = 0..t-2, then M-8-4(t-1)
 G2 = M-(4t+10), -M+(4t-3), -M+4t, -M+(4t+5), -M+(4t-4), -M+(4t+9), -M+(4t-8)   (uniform, checked t=8,9,10)
 Z4 = -(4t-8), then (-M+4j, -4j) for j = t-3..1, then -M
With these fixed, a DFS fills the gap between Z1 and T for EVERY t = 7..16 (M = 61..133) with a gadget of 8–14 vertices
(A ≈ t-7..t-4). The gadget is not yet uniform: forcing A = t-5 (10 free vertices) works for t <= 11 only, so one of the
fixed segment lengths must be tuned with t. All the long zigzags are proved-consecutive label runs; making the gadget
uniform turns this into a proof of a=2 for M ≡ 5 (mod 8).

## L34. AUDIT: GPT's tight a=2,3,4,5 constructions — ACCEPTED; and the a>=6 route
Construction: W = (δ, +M, −rev δ, +b, −M, −(M+1), +a) (symmetric core walk on [1,M]\{a,b} + a four-step bridge).
Own implementation from the stated formulas (experiments/audits/a2to5/audit.py): 0 failures for a=2,3,4,5 at every
M up to 1200 (labels, distinct partial sums, range <= 2M+2, distinct mod 2M+3). Hand-checked: the bridge lemma
(vertices M+b, b, −a fall in empty regions), a=2 alternating core in [0,M−2], the a=3 reflection recursion
(D_M = {0,M−1,2} ∪ (M−3−D_{M−3})), and the a=4, a=5 headers with the one-hole graceful recursion
G_{n,d} = (n−1,1,n) || (n−1 − G_{n−3,d}). THEOREM (candidate): the tight pair is solved for every M when a ≤ 5.
So the tight family is now proved for a = 1, 2, 3, 4, 5 (all M).
a>=6. GPT's obstruction holds only for its maximally packed window [3−a, M+2−a]. With the window relaxed, exact SAT
(experiments/irc/bridge_sat.py, bridge_scan.py) finds the SAME bridge (+b,−M,−(M+1),+a) working for every a >= 6 and
every M = 13..31 except a near M/2, where the bridge (+a,−M,+b,−(M+1)) works. The cores found have the shape
   D = {−a−1} ∪ ([2−a, M−a−2] \ {h}) ∪ {M−a}     (one free internal hole h)
— an interval with one hole plus one outlier at each end. Seeds G_{n,d} for n = d+1 (plain zigzag), d+2, d+3 exist for every
d = 4..16 (experiments/irc/gseeds.py), so G_{n,d} extends to every d once those seeds are given uniformly.

## L35. Uniform normal form for the WHOLE tight family (X bridge + two-hole interval core); corrections to L34
CORRECTION to L34. The G-bridge core shape R1 = {−a−1} ∪ ([2−a,M−a−2]\{h}) ∪ {M−a} (= GPT's normalized V(M,H), start a+1)
is exact-SAT UNSAT for EVERY hole h when a >= 14 (checked (a,M) = (14,30),(14,31),(15,32),(18,38); works for 6<=a<=13,
experiments/irc/age6/r1scan.py). Also R1 is the UNIQUE G-bridge window with min D = −a−1. So "same bridge for all a>=6"
in L34 was wrong; in bridge_scan.out the X bridge was used for a >= 14 at EVERY M, not only near a ≈ M/2.
NEW NORMAL FORM (all a >= 2). Bridge X: W = (δ, +M, −rev δ, +a, −M, +b, −(M+1)), b = M+1−a, bridge vertices M+a, a, M+1.
Core: D = [−k, M−1−k] \ {1, a}, path from 0. Lemma (proved by hand): for 0 <= k < M−a, D ∩ (D+M) = ∅ (span M−1); bridge
points avoid D ∪ (M+D) (a, 1 are holes; a−M < −k; M+a > M−1−k); span = max(2M−1, M+a+k) <= 2M+2 since
k < M−a; so any such δ is a valid ordering for every p >= 2M+3. Shifting by k: the core is
   LR(M,a,k): Hamiltonian path on [0, M−1] \ {k+1, k+a}, starting at k, with edge lengths exactly [1, M−1] \ {a, M+1−a}.
(a "linear realization" with two holes; the holes sit next to the start and at distance a from it.)
EVIDENCE: with the single uniform choice k = ⌊(M−a)/2⌋, exact SAT finds LR(M,a,k) and the full signed walk verifies for
EVERY 2 <= a <= M/2 and EVERY M = 8..46 (experiments/irc/age6/lrgrid.py, lrgrid.out; a = M/2 checked separately). The set of
good k is a wide window around (M−a)/2 (e.g. a=20,M=50: k=6..24). Largest-label-first solutions are an outer zigzag
k, M−1, 0, M−2, 1, M−3, ... with a bounded middle gadget near the two holes (experiments/irc/age6/lrdfs.py).
So the tight family = one clean two-hole linear-realization theorem, uniform in a.
ALSO: one-hole G_{n,d} for ALL d >= 4 with explicit zigzag bases, no citation and no small seeds:
   n=d+1: (d,1,d−1,2,...);  n=d+2: (d+1,d+2) || zig(1..d from 1) minus its last vertex  [lengths 1,d+1,d−1..2];
   n=d+3: (d+2,1,d+3,d+1) || zig(2..d from 2) with its second-to-last vertex deleted   [lengths d+1,d+2,2,d−1, then d−2..3,1].
Verified d=4..150, n <= d+199 (experiments/audits/gnd/audit_gnd.py). GPT's bases B/C (via prescribed-start graceful lemma) also check.

## L36. Literature status (verified from TeX sources) + audit of GPT LR/global round + reversed-G evidence for LR
STATUS OF #475 (sources read in full or in theorem statements):
- arXiv:2610.34424 Thm (thm:asymptotic): an ABSOLUTE n_0 such that every S ⊆ G\{0}, G finite abelian, |S| >= n_0, is
  rearrangeable — NO condition on p. n_0 not computed. (Preprint, Oct 2026.)
- Kravitz arXiv:2407.01835: |A| <= log p/log log p, EVERY prime. Costa–Della Fiore–Fontana–Vena arXiv:2603.20961: |A| <= 20
  in any abelian group (zero-sum <= 22), computer-assisted. Verified computationally for all p <= 23 (ADMS 2016 / CMPP 2018).
- Pham–Sauermann arXiv:2602.15797: C_α <= |S| <= p^{1-α}, any p, C_α explicit but ~exp(10^15).
- teorth/erdosproblems database: #475 status "decidable" (= reduced to a finite but huge check), not "proved".
CONSEQUENCE: for all primes, the open set is exactly 21 <= |A| < n_0 together with log p/log log p < |A| — a finite but
uncomputed set of (p, A). "Finishing" #475 = either an explicit n_0 small enough to check, or a constructive all-primes
argument for the bounded-size window. Our constructive programme targets the latter (sizes are unrestricted in it).
AUDIT (GPT LR/global round): (1) occupancy identity [−k,2M−1−k]\{1}: correct (also noted in L35). (2) forbidden-sum graph
x~y iff x+y ∈ {±c} is a Hamiltonian path on F_p: correct (R_−R_+ = translation by −2c; degree-1 vertices ±c/2; p−1 edges,
connected). Zero-overlap cycle for minimal zero-sum |B| <= 5: proof checked, correct (n=4 matching argument valid). Narrow.
(3) Single-edge two-vertex expansion LR(M)->LR(M+2) impossible: accepted. (Claude also: the stretch invariant "no short
edge crosses the midpoint" is SAT-UNSAT for essentially all (M,a) — experiments/irc/age6/cutsat.py — so stretch recursions die.)
NEW EVIDENCE for an LR recursion: LR(M,a,k) has solutions whose REVERSE begins with GPT's G-step header (M−2, 0, M−1, 2)
for every 5 <= a <= M/2−2 tested, M = 14..22, exactly for k ≡ ⌊M/2⌋+1 (mod 2) (experiments/irc/age6/revg.py).
So LR reversed = two-missing-label G-recursion (peel n−1,1,n; reflect) ending at k, with the end-holes k+1, k+a carried
through the reflections; only a ≈ M/2 needs separate bases.

## L37. AUDIT: GPT atom-fusion round — ACCEPTED; Strong Fusion (SF) reduction of Graham to one lemma
Accepted (proofs re-derived by hand; own code experiments/audits/fusion/audit_fusion.py):
- Four-block fusion word (b1,c1,b2..bm,c2..cn) for disjoint minimal atoms when the only proper zero-sum subsets of B∪C are
  B, C, cross inverse pairs and their complements (Hall on K_{m,n} minus the 4 cross adjacencies; explicit m=3 / n=3 cases).
- Two disjoint minimal triples always fuse: 2156/2156 pairs, p in {7,...,23}, by own construction. Examples mod 19 verify.
- Maximal-atom switching lemma (in a max atom partition, every proper zero-sum subset of B∪C and its complement are atoms).
- Integer version via large-prime theorem: correct, and correctly flagged as giving no range control.
NEW (Claude): STRONG FUSION statement
  SF: every zero-sum A ⊆ F_p^× that is not a minimal atom contains a minimal atom B with Z = A\B zero-sum such that for
      EVERY valid cycle z of Z, some rotation/reversal of z and some order of B make (b1, z1, b2,...,bm, z2,...,zn) valid.
SF ⇒ Graham for all p (induction on |A|: Z has a valid cycle by induction, SF fuses ANY of them; atoms are valid in any
order; then the zero-sum reduction handles nonzero-sum sets). Exhaustive test (experiments/audits/fusion/strong_fusion.py):
0 failures for all zero-sum non-atom A with p=11, |A|<=9 (65 sets; all of them), p=13, |A|<=8 (234 sets), p=17, |A|<=7 (1316 sets).
SF is an "every cycle" statement, so it is the induction-ready form of GPT's fusion: the missing theorem is exactly SF.

## L38. Strong Fusion: edge-insertion form, counting lemma, and the MAX-ATOM rule (0 failures in 5264 sets)
EDGE-INSERTION FORM (exact). Rotating the Z-cycle to start at vertex u (successor u', step w = u'−u), the four-block word
is "replace edge u→u' by (b1, w, b2, ..., bm)". New vertices: u+b1 and u'+σ_j (σ_j = b1+...+bj, 1<=j<=m−1). Valid iff these
m points avoid V_Z and u+b1 ≠ u'+σ_j (⇔ w ≠ −(b2+...+bj)). Pair insertion (+c,w,−c) is m=2. Reversal of the Z-cycle
(step order reversed) has vertex set −V_Z; traversing the same vertex set backwards is NOT allowed (it uses −Z).
COUNTING LEMMA (proved). Let r(t)=|V∩(V−t)|, r* = max_{t≠0} r(t), n=|V|, m=|B|. Bad (edge, order) pairs are at most
  Σ_{j=1}^{m−1} j!(m−j)! Σ_{|S|=j} r(σ(S))  [σ(S)≠0 by minimality]  +  (m−1)! Σ_{b∈B} r(b)  +  (m−1)·m!   <=  m!(m·r* + m−1),
out of n·m! pairs. Hence: if n > m·r* + m − 1, B inserts into THAT cycle. (Covers spread-out vertex sets; not dense/structured.)
WHICH ATOM (exhaustive, experiments/audits/fusion/sf_which.py, sf_fast.py):
  - "every atom works" FAILS (e.g. p=13 A=(1,2,3,5,7,9,12), B={1,12}); all such failures at p<=19 are INVERSE PAIRS, plus
    triples in the dense p=13, |A|=10 case.
  - MAX-ATOM RULE: B = any atom of MAXIMUM size (with A\B zero-sum) fuses with EVERY valid cycle of A\B — 0 failures:
    p=11 all 65 sets, p=13 all 257 sets (incl. A=F_13^×), p=17 |A|<=8 (2074), p=19 |A|<=7 (2868). Total 5264.
  - SF itself (some atom) also 0 failures for p=17 |A|<=9, p=19 |A|<=7.
CONJECTURE SF-max: for every zero-sum non-atom A ⊆ F_p^× and every maximum-size atom B ⊂ A with A\B zero-sum, every valid
cycle of A\B admits the edge insertion of B. SF-max ⇒ Graham for all p.

## L39. AUDIT: GPT near-balanced fusion round — ACCEPTED (experiments/audits/fusion/audit_nearbal.py)
- Thm 1 (all proper zero-sum subsets of size ⌊n/2⌋ or ⌈n/2⌉ ⇒ valid cycle, any abelian group): local boundary-swap proof
  re-derived (even: swap kills I and its complement only; odd: (R),(L) both ⇒ a_s = a_{s+m−1}). Own repair code: 3345
  repairs on EVERY near-balanced set, p<=17, n<=8, all terminate valid. The 1/(m+1) counting proof (even case) also checked.
- Thm 2 (max-r then max-Φ partition ⇒ mixed zero subsets of B∪C have size in [|B|,|C|]): proof checked (convexity);
  exhaustive p=11,13, n=6..9: 626 atom pairs, 0 violations. Corollary: atoms with sizes differing by <=1 always fuse.
- Thm 3 (|B|>=3, |C|>=6, only short mixed relations ⇒ four-block word): six mixed 3-windows + four 2-windows enumerated and
  exclusion counts 4,3,3,5,5 verified; 3000 random layouts.
- Transposition trap mod 11 and both examples verified.
RELATION TO SF-max (L38): GPT's stated remaining gap — atoms of very different sizes, and >=3 atoms — is exactly what
SF-max covers (insert a LARGEST atom into EVERY valid cycle of the rest; 0 failures in 5264 sets). Thm 2 supplies the
structural input for the two-atom case of SF-max: in a Φ-extremal pair all mixed zero intervals have length in [u,v].

## L40. RETRACTION of SF / SF-max (L37, L38) — GPT counterexample VERIFIED; fusable-fraction data
GPT's counterexample checked by own code (experiments/audits/fusion/audit_sfcx.py): p=19, A=F_19^×, B={1,18},
Z=(11,4,9,8,10,3,13,16,14,2,15,12,6,7,5,17) is a valid cycle; all four-block fusions fail; all 9792 order-preserving
insertions of {1,18} into rotations/reversals fail. Atoms of F_19^×: 447 in 26 scaling classes (max size 6) — confirmed;
own random search finds an obstructing valid complementary cycle for ALL 26 classes. Hence SF and SF-max are FALSE
(my exhaustive tests stopped at |A|<=7 for p=19 and missed the dense full-set regime). The p=37 claims (every one of the
54,246 atoms obstructed) are consistent but not independently re-run.
Accepted (proof checked): GPT's difference-isolated lemma — C={c,−c}, b1 ∈ B with b1 ∉ (B\{b1}) − (B\{b1}): adjacent swaps
inside B move each colliding prefix sum s_j ∈ {−c, b1−c} out of that set (the two targets differ by b1), so
(b1,c,b2,...,bm,−c) is valid for a suitable order.
DATA (own sampling, A = F_p^×): fraction of random valid complementary cycles admitting four-block fusion of atom B:
  p=13: 0.58 (pairs) .. 1.0 (size 5); p=17: 0.53 .. 1.0 (size 6); p=19: 0.49 (pairs), 0.52-0.59 (3,4), 0.65-0.80 (5), 0.96-0.97 (6).
So fusion fails for a MINORITY of complementary cycles, more often for small atoms and growing p. Any fusion-based
induction must CHOOSE the complementary cycle (build it), i.e. carry an invariant through the construction.
