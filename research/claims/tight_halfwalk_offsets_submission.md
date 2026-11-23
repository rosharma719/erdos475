## A necessary correction to the proposed C1 construction

I found a structural obstruction that rules out the suggested **single-gap, two-column normal form** for a substantial part of the small-\(a\) range.

Let \(D\) be a valid \(c=1\) half-walk vertex set of size \(M\), with edge lengths exactly \(2,\ldots,M\). Write \(n_0,n_1\) for its numbers of even and odd vertices.

Exactly

\[
R=\left\lfloor\frac{M-1}{2}\right\rfloor
\]

of the required edge lengths are odd. Each odd-length edge joins opposite parities, and a vertex in a Hamiltonian path has degree at most two. Therefore

\[
\boxed{R\le2\min(n_0,n_1).}
\tag{1}
\]

This is a necessary condition for **every** C1 construction, independent of its shape.

Now suppose \(D\) has the proposed single-gap form

\[
D=\{0,2,\ldots,2k\}
\cup\{2k+3,2k+5,\ldots\}.
\]

If \(M\) is even and \(a\) is odd, the marked vertex \(a\) belongs to the upper odd column. Consequently,

\[
n_0=k+1\le\frac{a-1}{2}.
\]

Combining this with (1) gives

\[
\boxed{\frac M2-1\le a-1,\quad\text{hence }a\ge M/2.}
\]

But the tight family requires \(a<(M+1)/2\), so for even \(M\), \(a\le M/2\). In fact, every **odd \(a<M/2\)** is excluded from this single-gap construction.

For odd \(M\) and odd \(a\), the same form is impossible for a different reason: \(0\) and \(M+1\) are even, while the intermediate marked vertex \(a\) is odd. A single parity-changing gap cannot place these three vertices in increasing order \(0<a<M+1\).

**Conclusion:** A uniform C1 proof needs at least two parity-changing gaps in these cases, or a different vertex-set geometry. The full defect allowance of three must be used, rather than assuming that one gap of size three is sufficient.

## Stronger result: an exact divisibility theorem for admissible offsets

The offset-counting lemma can be sharpened substantially.

**Theorem (proved).** Fix \(1\le c\le M\), and ask whether there can exist \(M\) distinct integers in an interval of length at most \(2M+2-c\), with no two differing by \(c\). This geometric packing condition is possible **if and only if**

\[
\boxed{
c\mid M\quad\text{or}\quad
c\mid M+1\quad\text{or}\quad
c\mid M+2\quad\text{or}\quad
c\mid M+3.
}
\tag{2}
\]

Thus every offset in a valid tight half-walk must divide at least one of four consecutive integers. This is stronger than the exclusion of \((2M+3)/3\le c<M\).

### Proof

The interval contains at most

\[
L=2M+3-c
\]

integer positions. Partition them into residue classes modulo \(c\). Each class forms a chain, with consecutive positions separated by \(c\), so no two neighboring chain positions may be selected.

Write \(L=qc+r\), where \(0\le r<c\). The maximum number of selectable positions is exactly

\[
\alpha_c(L)=
(c-r)\left\lceil\frac q2\right\rceil+
r\left\lceil\frac{q+1}{2}\right\rceil.
\]

If \(q=2h+1\) is odd, then \(\alpha_c(L)=(h+1)c\). The inequalities defining \(q\), together with \(\alpha_c(L)\ge M\), force

\[
(h+1)c\in\{M,M+1\}.
\]

If \(q=2h\) is even, then

\[
\alpha_c(L)=2M+3-(h+1)c.
\]

The same reasoning forces

\[
(h+1)c\in\{M+2,M+3\}.
\]

This proves necessity. Conversely, if \(c\) divides any of \(M,M+1,M+2,M+3\), selecting alternating blocks of \(c\) consecutive positions gives at least \(M\) admissible positions (with the short cases \(c=1,2\) checked directly). Hence the condition is also sufficient for the packing problem. \(\square\)

**Offsets surviving the exact packing test**

| \(M\) | Eligible offsets | Count |
|---|---|---:|
| 24 | 1, 2, 3, 4, 5, 6, 8, 9, 12, 13, 24 | 11 |
| 40 | 1, 2, 3, 4, 5, 6, 7, 8, 10, 14, 20, 21, 40 | 13 |
| 100 | 1, 2, 3, 4, 5, 6, 10, 17, 20, 25, 34, 50, 51, 100 | 14 |
| 400 | 1, 2, 3, 4, 5, 6, 8, 10, 13, 16, 20, 25, 31, 40, 50, 67, 80, 100, 134, 200, 201, 400 | 22 |

This is an exact classification of the **vertex-packing feasibility** of offsets, before imposing edge lengths or the marked triple. In particular, it does not prove that every listed offset supports a half-walk.
