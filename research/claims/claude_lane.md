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

## L8. Structure forced for a>=2 (proved)
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
