# A reduction of FV to ranks of two half-path spaces

The open claim below concerns two independently computed ranks. A strict inequality between them and a binomial coefficient gives a full FV ordering. For each cardinality, the claim need only be proved at an explicit finite set of primes. The symmetric case of FV is used as given in the problem.

## The half-path spaces

Fix FV data \(p,B,t,x\) with \(B\ne-B\). Put \(n=|B|\), \(m=n-1\), \(k=\lfloor m/2\rfloor\), \(\ell=m-k\), \(r=k-1\), \(s=\ell-1\), and \(d=r+s=n-3\). Here \(n\ge3\), since a zero-sum pair is symmetric. Write \(D=\binom d r=\binom d s\).

Choose \(A\subset B\setminus\{t\}\) of size \(k\), and put

\[
E=B\setminus(\{t\}\cup A),\qquad c=t+\sum A.
\]

Only choices with \(c\notin\{0,t,x\}\) enter the test. The two paths have respective endpoints \(t,c\) and \(c,0\), and use the labels \(A\) and \(E\). The endpoint \(0\) of the second path is forced by \(\sum B=0\). The common forbidden set for the **interiors** is \(J=\{0,t,c,x\}\).

Take \(K=\mathbb Q(z_{v,j}:v\in\mathbb F_p\setminus J,\ 1\le j\le d)\) with algebraically independent indeterminates, and set

\[
w_v=(z_{v,1},\ldots,z_{v,d})\in K^d\quad(v\notin J),\qquad
w_v=0\quad(v\in J).
\]

For either half, let \(L\) be its label set and \(u\) its start. Define its spaces from the subset sums of \(L\) by

\[
\begin{aligned}
H_{u,L}(\varnothing)&=K \quad\text{in exterior degree zero},\\
H_{u,L}(S)&=\left(\sum_{a\in S}H_{u,L}(S\setminus\{a\})\right)
                      \wedge w_{u+\sum S} &&(\varnothing\ne S\subsetneq L),\\
P(u,L)&=\sum_{a\in L}H_{u,L}(L\setminus\{a\}).
\end{aligned}
\]

For a subspace \(H\), the notation \(H\wedge w\) denotes its image under wedging with \(w\). In particular, \(P(u,L)=K\) when \(|L|=1\). The two ranks used below are

\[
\rho_A=\dim_K P(t,A),\qquad \rho_E=\dim_K P(c,E).
\]

**Half-path rank criterion.** If \(\rho_A+\rho_E>D\), then \((p,B,t,x)\) has an FV ordering.

**Proof.** For a half with \(h\) labels, \(P(u,L)\) is spanned by the exterior products of the \(h-1\) interior vertex vectors in their order of traversal. Indeed, the last label of any prefix \(S\) can be any \(a\in S\). The preceding prefix contributes a generator from \(H_{u,L}(S\setminus\{a\})\), and the next vertex is always \(u+\sum S\). Induction gives the first two lines of the recurrence. The final endpoint contributes no interior vector, giving the last line.

A repeated interior vertex makes its product zero by alternation. An interior visit to \(J\) makes it zero because the corresponding vector is zero. Conversely, any \(j\le d\) distinct allowed vertices have independent vectors. A \(j\)-rowed minor of their coordinate matrix is a nonzero polynomial, as witnessed by assigning these vectors to distinct basis vectors. This also gives the empty product convention when \(d=0\).

Exterior multiplication is a perfect pairing between \(\bigwedge^r K^d\) and \(\bigwedge^s K^d\) into \(\bigwedge^d K^d\simeq K\). In the subset bases, each basis monomial pairs with exactly its complementary monomial, with coefficient \(1\) or \(-1\). Thus the annihilator of \(P(t,A)\) has dimension \(D-\rho_A\). The strict inequality puts some element of \(P(c,E)\) outside this annihilator. By bilinearity at least one pair of path generators has nonzero product. Their \(r+s\) interior vertices are all distinct and avoid \(J\). Prepending \(0\to t\) and joining the paths at \(c\) gives the required ordering. The only repetition is the final return to \(0\). \(\square\)

## The finite set of primes

Let \(\mathcal D_n\) consist of the primes dividing any **nonzero** determinant of an \(n\times n\) matrix with entries \(0,1\). Define

\[
H_n=\frac{(n+1)^{(n+1)/2}}{2^n},\qquad
M_n=\binom{n+1}{2}+3,\qquad
q_n=\text{the least prime greater than }\max\{2H_n,M_n\}.
\]

**Prime reduction.** If FV fails at cardinality \(n\), it fails at that cardinality at some prime in \(\mathcal D_n\cup\{q_n\}\).

**Proof.** Write the negatives of the \(m=n-1\) nonroot labels as \(a_1,\ldots,a_m\). Then \(t=\sum_i a_i\). Traversing the tail backwards identifies FV with a simple path from \(0\) to \(t\) using these \(a_i\), avoiding \(x\) at every vertex. In one direction, reverse the path and negate its steps to recover the tail following \(0\to t\). The path's distinct vertices are precisely the proper vertices of that rooted cycle.

Suppose an admissible instance fails at \(p\notin\mathcal D_n\). Write \(z=(a_1,\ldots,a_m,-x)\). Let \(R\) be the integer matrix of all rows in \(\{0,1\}^n\) orthogonal to \(z\) modulo \(p\). For every permutation of the \(a_i\), at least one obstruction is recorded by \(R\). A repeated vertex gives a nonempty consecutive block of sum zero, whose indicator row has last coordinate zero. A visit to \(x\) gives a prefix of sum \(x\), whose indicator row has last coordinate one. In any characteristic, every vector in the kernel of the same integer matrix therefore retains an obstruction for each of those permutations.

Admissibility of a kernel vector is equivalent to simultaneous nonvanishing of the \(M_n\) forms

\[
a_i,\quad a_i-a_j\ (i<j),\quad t+a_i,\quad t,\quad x,\quad x-t,\quad 2x-t,
\qquad t=\sum_i a_i.
\]

Here \(t+a_i\ne0\) keeps the root distinct from the label \(-a_i\). In the coordinates \(z\), each form has a row \(w\) that is a signed sum of at most two Boolean rows. For instance, up to sign the row for \(2x-t\) is the all-ones row plus the last coordinate row.

Every nonzero square minor of \(R\) stays nonzero modulo \(p\). A smaller Boolean square matrix embeds into an \(n\times n\) one with the same determinant by adjoining an identity block. Hence \(R\) has the same rank \(b\) over \(\mathbb Q\) and \(\mathbb F_p\). For every admissibility row \(w\), \(wz\ne0\) but \(Rz=0\) modulo \(p\). The augmented matrix with row \(w\) thus has an integer \((b+1)\)-minor nonzero modulo \(p\), and in particular nonzero over \(\mathbb Q\).

All square Boolean minors of order at most \(n\) have absolute value at most \(H_n\). To see this, pad to order \(n\) and call the resulting matrix \(N\). Adjoin a first row and column of ones around the block \(\mathbf1-2N\), with \(\mathbf1\) the all-ones matrix. Subtracting the first row from each other row gives determinant \((-2)^n\det N\). Before subtraction its rows all have norm \(\sqrt{n+1}\). Orthogonalizing the rows bounds the absolute determinant by the product of their norms, giving the stated bound. By linearity in \(w\), all the augmented minors have absolute value at most \(2H_n\).

At \(q=q_n\) the rank of \(R\) is still \(b\), and each of the indicated augmented minors stays nonzero. Thus every \(w\) cuts a proper hyperplane out of \(\ker_{\mathbb F_q}R\). This kernel has some dimension \(h\ge1\). Each hyperplane has \(q^{h-1}\) points, since one nonzero linear equation determines one coordinate from the others. Their union has size at most \(M_nq^{h-1}<q^h\). Take \(z'\) outside the union in that kernel. Its coordinates define admissible \(B',t',x'\) of size \(n\) over \(\mathbb F_q\), and every permutation still has its recorded obstruction. This is a counterexample at \(q_n\). \(\square\)

## The one open lemma

**L.** For every \(n\ge3\), every prime \(p\in\mathcal D_n\cup\{q_n\}\), and every admissible nonsymmetric \((p,B,t,x)\) of cardinality \(n\), some \(k\)-subset \(A\subset B\setminus\{t\}\) has \(c\notin\{0,t,x\}\) and

\[
\dim P(t,A)+\dim P(c,E)>\binom{n-3}{\lfloor(n-1)/2\rfloor-1}.
\]

**Implication.** Assume L and take any FV counterexample. The prime reduction gives a counterexample of the same size at one of the primes in L. It is nonsymmetric by the established symmetric theorem. L supplies a split at that prime, and the half-path rank criterion supplies the forbidden-point-avoiding ordering, a contradiction. Thus \(\mathrm{L}\Rightarrow\mathrm{FV}\), including when \(x\in B\) or \(t-x\in B\).

## Exhaustive check of L

The test checks the inequality at **all** the listed primes, including those outside the required finite list for a given \(n\). Multiplication by \(t^{-1}\) gives the unique representative with \(t=1\) and relabels all vertex vectors bijectively. For each zero-sum nonsymmetric \(B\) containing \(1\), the verifier checks every admissible \(x\) individually. For odd \(p\), an asymmetric \(B\) has \(3\le n\le p-4\). Its complement in \(\mathbb F_p^\times\) is zero-sum by pairing opposites, and a zero-sum complement of size at most two is empty or an inverse pair. At \(p=2\) there are no admissible instances.

| Prime | Normalized instances | Rank inequality certified |
|---:|---:|---:|
| 2, 3, 5 | 0 | 0 |
| 7 | 4 | 4 |
| 11 | 248 | 248 |
| 13 | 1,260 | 1,260 |
| 17 | 25,200 | 25,200 |
| 19 | 106,288 | 106,288 |
| **Total** | **133,000** | **133,000** |

These checks and one additional run discharge the entire finite prime list through \(n=6\). Indeed, \(q_3,q_4,q_5,q_6\) are \(11,17,19,29\), respectively. Each Boolean determinant of order at most six is bounded in magnitude by \(H_6<15\), by padding to order six. The only additional check needed is \(p=29,\ n=6\), where all **70,356** normalized instances have rank certificates. Consequently the implication only needs the general inequality for \(n\ge7\). The supplied FV census also allows primes \(p\le31\) to be omitted from that implication.

For each candidate split, the script enumerates legal half paths separately. It substitutes binary vectors for the \(w_v\) and computes the exterior ranks by exact elimination over \(\mathbb F_2\). Every nonzero minor after substitution is an integer polynomial minor of the symbolic matrix with an odd value at those binary coordinates. It is therefore nonzero over \(K\). Even lower bounds obtained under different substitutions hold simultaneously for the two generic ranks. The random seed only controls the search for certificates. Every reported success is conclusive, and the program explicitly counts any inconclusive instance.

For example, at \(p=13\), take \(B=\{1,2,3,5,6,7,8,9,11\}\), \(t=1\), \(x=4\). The split \(A=\{3,6,8,11\}\) has \(c=3\), \(r=s=3\), and ranks at least \(12\) and \(9\). Since \(\binom63=20\), the inequality certifies this instance with one dimension to spare.

Run the self-contained Python verifier from the repository root.

```sh
python3 experiments/exploration/forced_vertex/half_path_rank.py 2 3 5 7 11 13 17 19
python3 experiments/exploration/forced_vertex/half_path_rank.py 29 --size 6
```

The remaining gap is a proof of the strict rank inequality for some balanced split in every instance of L.
