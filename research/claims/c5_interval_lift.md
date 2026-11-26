# Complement five from two paths in an integer interval

The following reduction dispenses with graceful completion. It leaves one open assertion about integer five-sets.

For a path \(P=(v_0,\ldots,v_k)\) of distinct integers, let \(D(P)\) denote the multiset of its signed steps \(v_i-v_{i-1}\). Write \(I_M=\{-M,\ldots,-1,1,\ldots,M\}\).

**Boundary seed assertion (open).** Let \(T\) be a five-element set of nonzero integers with ordinary sum zero and \(M=\max_{t\in T}|t|\). There are two simple paths \(P,Q\) in \([0,M]\), both starting at \(0\) and ending at the same \(y>0\), with

\[
D(P)\uplus(-D(Q))=I_M\setminus T .
\]

The right side has multiplicity one at each label. The paths may share vertices with each other. The assertion only asks for paths at the exact height \(M\) of the holes.

## A one-step extension

Suppose such paths have been found in \([0,q-1]\) with combined label multiset \(I_{q-1}\setminus T\). Write \(q-Q\) for the list obtained by applying \(v\mapsto q-v\) to every vertex. Define

\[
P'=(0)\mathbin{\|}(q-Q),\qquad Q'=(0)\mathbin{\|}(q-P).
\]

Both paths are simple because their reflected parts lie in \([1,q]\). They begin with \(0,q\) and have common endpoint \(q-y>0\). Their combined label multiset is

\[
\{q\}\uplus(-D(Q))\uplus\{-q\}\uplus D(P)=I_q\setminus T.
\]

Thus one seed gives paths for **every** larger interval, with both signs of each new magnitude and with the same holes. Exchanging the two paths compensates for reflection of the signed steps.

In fact this extension is reversible whenever \(q>M\). A simple path starting at zero in \([0,q]\) cannot use the step \(-q\), since its target would be the already visited zero. Its only possible step of magnitude \(q\) is \(0\to q\), as its first edge. Consequently the presence of both signed labels forces both paths to begin with this edge. Delete the initial zero of each path, reflect in \(v\mapsto q-v\), and exchange the paths. This gives the original label condition in \([0,q-1]\). The new endpoint is positive. Otherwise both old paths would have ended at \(q\) immediately after their first edge, whereas their combined number of steps is \(2q-5>2\) (any zero-sum integer five-set has \(M\ge4\)). Thus searching larger intervals for the same holes gives exactly the same existence question as searching at their height.

## Closing the cycle

Let \(p=2r+1\). Suppose the integer lifts of some dilation \(\lambda H\) form a zero-sum five-set \(T\subseteq I_{r-1}\) having a boundary seed. Apply the extension for \(q=M+1,\ldots,r-1\), with zero applications when \(M=r-1\). Denote the resulting paths in \([0,r-1]\) by \(P,Q\). Traverse \(P\), a step \(+r\), the translated reversed path \(r+\operatorname{rev}(Q)\), and a step \(-r\) back to zero. The common endpoint \(y\) makes the first connecting edge \(y\to y+r\). The second is \(r\to0\). The vertices of the first path lie in \([0,r-1]\) and those of the second in \([r,2r-1]\). Hence all vertices before the return to zero are distinct modulo \(p\). The signed steps are precisely \(I_r\setminus T\), whose residues are \(\mathbb F_p^\times\setminus\lambda H\). Dilation by \(\lambda^{-1}\) gives the required ordering.

## The dilation exists at every remaining prime

Let \(r\ge30\) and \(p=2r+1\) be prime. List \(H=(h_1,\ldots,h_5)\). There are more than \(p^3\) points of \(\{0,\ldots,r-1\}^5\) with the same **integer** coordinate sum.

Indeed, choose five independent uniform coordinates in that interval and let \(S\) be their sum. Its mean is \(5(r-1)/2\), and its variance is \(5(r^2-1)/12\), by the sums of the first \(r-1\) integers and of their squares. The event \(|S-\mathbb ES|\ge r\) contributes at least \(r^2\) times its probability to the variance. Consequently more than \(7/12\) of the \(r^5\) box points have sums in an open interval of length \(2r\), which contains at most \(2r\) integers. Some sum \(s\) therefore occurs more than \(7r^4/24\) times. For \(r\ge30\),

\[
7r/24\ \ge\ 35/4\ >\ (61/30)^3\ \ge\ (2+1/r)^3.
\]

This gives \(7r^4/24>(2r+1)^3=p^3\).

Modulo \(p\), the affine hyperplane with coordinate sum \(s\) contains \(p^4\) points. The line spanned by \((h_1,\ldots,h_5)\) acts on it by translations because \(\sum H=0\). Its orbits have \(p\) elements, giving \(p^3\) orbits. Two distinct box points of sum \(s\) lie in the same orbit. Their integer difference \(t\) satisfies

\[
  \sum t_i=0,\qquad |t_i|\le r-1,\qquad t_i\equiv\lambda h_i\pmod p
\]

for one nonzero \(\lambda\). Indeed the original points were distinct modulo \(p\), since the box side is smaller than \(p\). The \(t_i\) are nonzero and pairwise distinct because their residues are.

**All-primes implication.** The boundary seed assertion, the one-step extension, and closure prove C5 for every prime \(p\ge61\). The exhaustive two-block certificates cover the smaller primes. Thus the sole missing step in this reduction is the integer boundary seed assertion at unbounded \(M\). [Two-block proof and finite census](c5_two_blocks.md)

The small-prime qualification matters. At \(p=11\) the subgroup \(H=\{1,3,4,5,9\}\) has index two, so all its dilations are \(H\) or \(-H\). Their centered representatives have sums \(11\) and \(-11\), respectively. The two-block verification covers this orbit.

## Finite check of the open assertion

The standard-library verifier enumerates every zero-sum integer five-set of each indicated height. It assigns one signed copy of each fully present magnitude to both paths, splits the unpaired labels, and searches the paths independently from zero. It then recomputes the signed step multiset, checks the two paths, builds the cycle, and checks the same properties after four applications of the extension. An unsuccessful search under this restriction would be inconclusive. Every entry below has a positive witness.

| \(M\) | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Five-sets | 0 | 4 | 12 | 26 | 48 | 82 | 124 | 186 | 258 | 352 | 462 | 600 |
| Seeds verified | 0 | 4 | 12 | 26 | 48 | 82 | 124 | 186 | 258 | 352 | 462 | 600 |

Run \(\texttt{python3 experiments/exploration/complement5/verify_interval_lift.py --height 14}\) from the repository root.

## Direct certificates at primes from 67 through 113

For each orbit of five-set holes under dilation, the verifier constructs a seed for one dilation, lifts and closes it, then rescales the cycle back to the original representative. It checks that the cycle has \(p-6\) distinct vertices and that its \(p-6\) modular steps use every nonzero residue outside the original five holes exactly once.

| Prime | Orbits | Certified | Prime | Orbits | Certified |
|---:|---:|---:|---:|---:|---:|
| 67 | 2,021 | 2,021 | 97 | 6,564 | 6,564 |
| 71 | 2,436 | 2,436 | 101 | 7,455 | 7,455 |
| 73 | 2,662 | 2,662 | 103 | 7,928 | 7,928 |
| 79 | 3,426 | 3,426 | 107 | 8,935 | 8,935 |
| 83 | 4,009 | 4,009 | 109 | 9,469 | 9,469 |
| 89 | 5,002 | 5,002 | 113 | 10,600 | 10,600 |

Every orbit has a representative containing \(1\), obtained by multiplying by the inverse of any hole. The program enumerates these representatives as \(1<a<b<c<d<p\), with \(d\) recovered from the zero-sum condition. For each new representative it records every normalization of that set containing \(1\), so subsequent representatives are skipped exactly when their orbit has already been tested.

An independent count checks coverage. For \(p>5\), write \(N_j\) for the number of zero-sum \(j\)-sets of nonzero residues, with \(N_0=1\). For \(1\le j\le5\), translation puts exactly one \(j\)-set of sum zero in each translation orbit of \(j\)-sets of \(\mathbb F_p\), since translating by \(a\) changes the sum by \(ja\). Separating sets containing zero gives \(N_j=\binom pj/p-N_{j-1}\). A five-set's dilation stabilizer has order dividing five because it acts freely on the five elements. When \(5\mid p-1\), the cosets of the order-five subgroup give exactly one exceptional orbit of size \((p-1)/5\). Each coset sums to zero by the geometric-series identity. All other orbits have size \(p-1\). These counts reproduce the orbit total at each prime in the table, covering 6,872,838 five-sets.

The 70,507 certificates in this table and the 5,941 two-block certificates through 61 prove C5 for **all primes \(p\le113\)**, covering 7,174,166 five-sets in total. Both finite computations use only the Python standard library. From the repository root run

~~~sh
python3 experiments/exploration/complement5/verify_two_blocks.py
python3 experiments/exploration/complement5/verify_interval_lift.py --primes 67 71 73 79 83 89 97 101 103 107 109 113
~~~
