# Complement five by exchanging the sums of two blocks

## A counterexample at arbitrarily large orders

Take \(W=\{1,3,7,-2,-4,-5\}\). The six absolute values are distinct, the largest is \(7\), and \(1+3+7=2+4+5\). For any seven consecutive entries of a permutation, the sum of the six signed differences is the last entry minus the first. The entries are distinct, so that sum is nonzero. Thus no ordering of \(W\) occurs in any position of any graceful permutation. One concrete prime instance is \(p=1009,\ r=504\). The same obstruction works as \(r\) tends to infinity, satisfying either small-magnitude hypothesis in the question for any fixed positive constant.

For a C5 window \(H\cup\{s\}\) the total is \(s\ne0\). The counterexample therefore refutes the stated graceful-segment lemma and leaves C5 open.

There is also an obstruction inside the intended six-window construction. For \(p=29\) and \(H=\{1,3,11,17,26\}\), **no** choice of \(\lambda,s,\alpha\) gives a six-window in \(B_\alpha\). The finite proof below resolves the sample miss reported for this orbit.

**Exhaustion for this obstruction.** In every dilation the holes include an opposite pair. Six labels lying wholly within a single ordinary half of \(B_\alpha\) have distinct magnitudes, so a candidate window must include a connector \(r\) or \(-r\). At \(r=14\) it includes at most one. Read differences outwards on both sides of the connector, negating the differences read on the left. The two lists must be prefixes of the same signed difference sequence. At \(-r\) this is the beginning of \(\alpha\), and at \(+r\) it is the beginning of the reversed \(\alpha\).

The verifier tries every dilation, extra label outside the dilated holes, and permutation of the resulting six labels. For each connector position it checks agreement where the two lists overlap and takes the longer list as a required prefix. After discarding invalid or repeated magnitudes there are 1,776 distinct candidate prefixes. Translating their prefix sums into \([0,13]\), with all vertices distinct, gives 142 placements. From each, the verifier tries every unused next vertex whose difference magnitude is unused, until it reaches a permutation or exhausts the search. None completes. Every genuine window gives one of the tested placements, and the search has no node or time cutoff.

## A replacement with two shorter segments

Write \(p=2r+1\), and use the cyclic label sequence \(B_\alpha\) from the problem. The following conjecture permits inverse pairs in \(H\).

**Two-block lemma (open).** For each zero-sum five-set \(H\subset\mathbb F_p^\times\), there exist a unit \(\lambda\), a partition \(\lambda H=X\sqcup Y\) with \(|X|\in\{1,2\}\), and distinct nonzero labels \(a,b\notin\lambda H\) such that \(b-a=\sum X\). Some graceful \(\alpha\) has \(X\cup\{a\}\) and \(Y\cup\{b\}\) as disjoint cyclic blocks of steps. The lengths are \(2+5\) or \(3+4\). Each block may occur in any order.

**Reduction.** Since \(\sum Y=-\sum X\), the first block has sum \(a+\sum X=b\) and the second has sum \(b+\sum Y=a\). Contract both. Their step positions are disjoint, so the contraction keeps their endpoints and deletes exactly \(|X|+|Y|=5\) interior vertices. This remains valid when the blocks share an endpoint. The other labels are precisely \(\mathbb F_p^\times\setminus(\lambda H\cup\{a,b\})\). Restoring \(b,a\) as the two block sums gives every member of \(\mathbb F_p^\times\setminus\lambda H\) exactly once. The resulting vertices form a subsequence of a simple cycle. Rescaling by \(\lambda^{-1}\) proves C5.

The arithmetic choice can always be made before asking for graceful completion when \(p\ge13\). Choose any two holes with nonzero sum \(\sigma\), which exist since any given hole has at most one opposite. In the paired case one can take a member of the inverse pair and a member of its complementary triple, so the two opposite holes are in different blocks. At most twelve values of \(a\) lie in \((\{0\}\cup H)\cup((\{0\}\cup H)-\sigma)\). Every other choice gives distinct \(a,b=a+\sigma\) outside \(\{0\}\cup H\). The open requirement is simultaneous occurrence of the two blocks in one graceful cycle.

## The two blocks can be prescribed locally for every sufficiently large prime

After dilation, it is possible to prescribe a **single simple integer path** in \([1,r]\) with distinct difference magnitudes that would produce both contracted blocks if extended to a graceful permutation. Seven differences suffice for inverse-free holes and six suffice for paired holes.

**Dilation.** List four holes as \(h_1,\ldots,h_4\). Put \(m=\lfloor(p-1)^{1/4}\rfloor\) and partition the residues \(0,\ldots,p-1\) into \(m\) intervals of length at most \(\lceil p/m\rceil\). The \(m^4+1\) points \(j(h_1,\ldots,h_4)\), \(0\le j\le m^4<p\), occupy \(m^4\) boxes. Subtract two in the same box. The resulting nonzero multiplier gives integer lifts of the four holes of absolute value at most \(\lceil p/m\rceil\). Take the fifth lift to be minus their sum. Thus all five lifts sum to zero over the integers and have magnitude at most \(M=4\lceil p/m\rceil=O(p^{3/4})\). For all sufficiently large \(p\), \(r>30M+1\). In particular these lifts are the unique centered representatives.

**Inverse-free holes.** Write \(H\) after dilation as \(\{u,v,y_1,y_2,y_3\}\). No nonempty proper subset sums to zero: a vanishing triple has a vanishing complementary pair, a vanishing four-set has a zero singleton, and pairs are excluded. Set \(a=10M,\ b=a+u+v\), and take the seven signed differences

\[
  u,\ v,\ a,\ b,\ y_1,\ y_2,\ y_3 .
\]

The first three sum to \(b\), the last four to \(a\), and all seven magnitudes are distinct because \(8M\le b\le12M,\ b\ne a\). Starting at zero, the first three vertices \(0,u,u+v\) are distinct and in \([-2M,2M]\). The next is \(b\). The remaining four are \(2b\) plus the four successive prefix sums of the \(y_i\), including the empty sum. These are distinct, lie within \(3M\) of \(2b\), and exceed \(b\). The path has width at most \(29M\), so it translates into \([1,r]\). Its two consecutive blocks would lie in the forward half of \(B_\alpha\).

**Paired holes.** Write the centered lifts as \(\{\pm h,u,v,w\}\) with \(u+v+w=0\). Choose the sign of \(h\) so that \(h\ne-2u\), then interchange \(v,w\) if needed so that \(v\ne u+h\). Put \(a=10M,\ b=a+u+h\) and prescribe the six differences

\[
  a,\ u,\ h,\ -v,\ -w,\ -b.
\]

Again \(8M\le b\le12M,\ b\ne a\), and all six magnitudes are distinct. The interior vertices are \(a\) plus the five prefix sums of \((u,h,-v,-w)\). To check distinctness, the sums of its consecutive pairs are \(u+h,h-v,u\), the sums of its consecutive triples are \(u+h-v,h+u\), and the full sum is \(h+2u\). Each is nonzero by the sign and order choices and by \(h\notin\{\pm u,\pm v,\pm w\}\). The five interior vertices lie in \([6M,14M]\), while the two endpoints are \(0,u\). The path therefore translates into \([1,r]\). Its first three differences in the forward half give \((a,u,h)\). The reflected copy of its last four gives \((b,w,v,-h)\) in the other half. The two blocks occupy distinct positions in \(B_\alpha\), and their sums are \(b,a\).

Both constructions give a prescribed simple path with its required signs and enough room in the interval. Extending one such path to a graceful permutation at arbitrary \(r\) remains open. The two-block lemma also allows other placements.

## Exhaustive tests of the revised lemma

The domain is \(p=2r+1\) prime. The verifier covers every such \(r\le30\). The prime 2 has no five-set. The columns count all zero-sum five-sets in \(\mathbb F_p^\times\), their orbits under multiplication by units, and orbits certified by a pair of blocks with exchanged sums.

| \(r\) | \(p\) | Five-sets | Orbits | Certified |
|---:|---:|---:|---:|---:|
| 1, 2, 3 | 3, 5, 7 | 0 | 0 | 0 |
| 5 | 11 | 22 | 3 | 3 |
| 6 | 13 | 60 | 5 | 5 |
| 8 | 17 | 256 | 16 | 16 |
| 9 | 19 | 450 | 25 | 25 |
| 11 | 23 | 1,144 | 52 | 52 |
| 14 | 29 | 3,388 | 121 | 121 |
| 15 | 31 | 4,596 | 154 | 154 |
| 18 | 37 | 10,188 | 283 | 283 |
| 20 | 41 | 16,048 | 402 | 402 |
| 21 | 43 | 19,782 | 471 | 471 |
| 23 | 47 | 29,164 | 634 | 634 |
| 26 | 53 | 49,036 | 943 | 943 |
| 29 | 59 | 77,662 | 1,339 | 1,339 |
| 30 | 61 | 89,532 | 1,493 | 1,493 |
| **Total** | | **301,328** | **5,941** | **5,941** |

For the failed six-window orbit above, take \(\lambda=5\) and
\[
\alpha=(8,13,1,14,3,10,6,5,11,2,12,4,7,9).
\]
The two blocks of \(B_\alpha\) are \((15,5,17)\) and \((14,27,26,8)\). Their sums modulo 29 are \(8\) and \(17\). Contracting both removes precisely \(\{5,14,15,26,27\}=5H\).

Run \(\texttt{python3 experiments/exploration/complement5/verify_two_blocks.py}\) from the repository root with Python 3.10 or later. The standalone verifier embeds the witness permutations. It enumerates the smallest four entries of every zero-sum five-set and recovers the fifth from their sum. For every witness it checks gracefulness and inspects every pair of cyclic windows of the two allowed lengths. Since every label of \(B_\alpha\) occurs once, disjoint label masks certify disjoint positions. The cross-membership check verifies that each sum belongs to the opposite block. All 1,256 paired orbits and all 4,685 inverse-free orbits receive certificates.
