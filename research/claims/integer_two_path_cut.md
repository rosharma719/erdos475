# A midpoint obstruction to the integer two-path lemma

The unrestricted IT(\(k\)) in the [original statement](integer_two_path_k.md) is false, even when \(M=k\), the retained labels sum to zero, and there are \(M\) of them. This obstruction concerns the integer construction. The modular complement conjecture and the \(k=5\) integer case remain open in general.

## Counterexample

Write \(I_M=\{-M,\ldots,-1,1,\ldots,M\}\). Take \(M=31\) and

\[
T=\{-18,\ldots,-1\}\ \cup\ \{5,\ldots,15\}\ \cup\ \{30,31\}.
\]

There are 31 holes, their largest magnitude is 31, and their sum is \(-171+110+61=0\). The remaining labels are

\[
S=I_{31}\setminus T
 =\{1,2,3,4\}\ \cup\ \{16,\ldots,29\}\ \cup\ \{-31,\ldots,-19\}.
\]

If the required paths existed, traversing \(P\) and then \(Q\) backwards would give a closed walk in \([0,31]\) with step multiset \(S\). Put \(f(x)=0\) for \(0\le x\le15\) and \(f(x)=1\) for \(16\le x\le31\). Each of the fourteen steps \(16,\ldots,29\) increases \(f\) by one in every possible placement. Smaller positive steps cannot decrease \(f\). Each of the thirteen negative steps decreases \(f\) by at most one. The total change in \(f\) is at least \(14-13=1\). On a closed walk it is zero by telescoping. This rules out even a walk with repeated vertices.

## What the cut proves

More generally, write \(n_+\) and \(n_-\) for the numbers of positive and negative labels in \(S\), and \(L_+\) and \(L_-\) for the respective numbers of magnitude strictly larger than \(M/2\). Every certificate requires

\[
L_+\le n_-,\qquad L_-\le n_+ .
\]

In fact these inequalities characterize whether each *individual* threshold cut can be balanced by choosing placements independently for the steps. For a cut \([0,c]\mid[c+1,M]\), every positive step has a placement crossing upwards. It is forced to cross exactly when its magnitude exceeds \(\max(c,M-c-1)\), the larger internal diameter. The corresponding statement for negative steps follows by reversal. The possible numbers of crossings of each sign comprise every integer from its forced count to its total count. Those two intervals overlap precisely when each forced count is at most the opposite total. Both forced counts are maximized at a midpoint cut, where the larger internal diameter is \(\lfloor M/2\rfloor\). Matching counts independently at each cut does not construct paths.

Those two scalar inequalities alone cannot repair IT(\(k\)). For instance, on \([0,8]\) take the five retained labels \(S=\{7,8,-4,-5,-6\}\) and let \(T=I_8\setminus S\). Both inequalities hold, but no closed walk exists. Give the vertices \(0,\ldots,3\) weight 0, vertex 4 weight 1, and vertices \(5,\ldots,8\) weight 2. Each of \(+7,+8\) increases weight by two. Each of \(-5,-6\) decreases it by two, and \(-4\) decreases it by at least one wherever placed. This gives a strictly negative total. There is also an empty-spectrum exception to the stated \(k=2\) base case at \(T=\{-1,1\}\), since a positive endpoint requires at least one edge on each path.

## An exact corrected width lemma

Let \(S\) be any nonempty zero-sum set of nonzero integer labels. The minimum width of an interval starting at zero that admits the two paths is the following finite minimum. For each cyclic ordering of \(S\), form its prefix sums, counting the cyclic starting vertex just once. Discard an ordering if the minimum occurs more than once, or any value occurs more than twice. Rotate the order to start at its unique minimum. For each repeated value record its two indices \(i<j\) among \(0,\ldots,|S|-1\). Keep the ordering if there is an integer \(u\) with \(1\le u<|S|\) and \(i<u<j\) for every recorded pair. Minimize the prefix-sum range over the retained orders. For a given order the index test is just one comparison of the largest lower bound with the smallest upper bound.

**Proof.** A pair of paths gives such a cyclic order by following the first forwards and the second backwards. The starting vertex \(0\) is the unique minimum since each path is simple. The common positive endpoint occurs just once in the cyclic list. Every repeated vertex occurs once on either side of that endpoint. Conversely, translate the rotated prefix sums so the minimum is zero and split at a qualifying index \(u\). Each part contains at most one occurrence of every vertex, including the shared endpoints. Reading the second part backwards gives the two required paths, both confined to the computed range. The minimum is always attained. For example, take one monotone path with all positive steps and another with all negatives negated. Their common endpoint is the sum of the positive labels.

In particular the corrected minimum width for \(S=\{7,8,-4,-5,-6\}\) is exactly 9. The obstruction gives the lower bound, and \(P=(0,7)\), \(Q=(0,5,9,1,7)\) attain it. The original IT(\(k\)) requested an upper bound of 8 here.

## Revised integer lemma to test

**Dense integer two-path conjecture.** Let \(T\) be a zero-sum set of \(k\ge2\) nonzero integers with exact height \(M=\max_{t\in T}|t|\). Assume \(M\ge 2k\). Then there exist simple paths \(P,Q\) in \([0,M]\), both from \(0\) to the same \(E>0\), satisfying \(D(P)\uplus(-D(Q))=I_M\setminus T\). Here \(D\) records signed steps with multiplicity.

This added hypothesis is sufficient for every threshold-cut test. Each sign has at least \(M-k\ge\lceil M/2\rceil\) retained labels, and at most \(\lceil M/2\rceil\) have magnitude greater than \(M/2\). Sufficiency for *paths* is conjectural. The choice of the constant 2 avoids this obstruction and preserves the prime application by the following theorem.

## General dilation and closure theorem

Let \(p=2r+1\) be prime, \(H\subseteq\mathbb F_p^\times\) a zero-sum \(k\)-set, and \(k\ge2\). Assume

\[
r\ge4k,\qquad r^k > [k(r-1)+1]\,p^{k-2}.
\tag{1}
\]

Then there is a dilation of \(H\) whose integer lifts \(T\) sum to zero and have exact height \(2k\le M\le r-1\). A sufficient closed-form range for (1) is

\[
p\ \ge\ \max\{8k+1,\; k\,2^{k-1}+k-1\}.
\tag{2}
\]

**Dilation.** Partition \(\{0,\ldots,r-1\}^k\) by ordinary coordinate sum. There are at most \(k(r-1)+1\) sums. Under (1), some slice has more than \(p^{k-2}\) points. Modulo \(p\) it lies in an affine sum hyperplane of size \(p^{k-1}\). The nonzero vector listing \(H\) spans a line acting on that hyperplane by translation, with \(p^{k-2}\) orbits. Two distinct slice points are in the same orbit. Their integer difference is congruent to a nonzero scalar times \(H\), has ordinary sum zero, and has exact height \(m\le r-1\). Its entries are nonzero and distinct because their residues are.

If \(m<2k\), multiply all entries by \(d=\lceil 2k/m\rceil\). The resulting height satisfies \(2k\le dm<2k+m<4k\le r\). In fact \(d\le4\), since \(k\) distinct nonzero integers require \(2m\ge k\). Thus this is another valid modular dilation. If \(m\ge2k\), keep the difference as found.

To see (2), Bernoulli's inequality gives

\[
\frac{r^{k-1}}{p^{k-2}}=
\frac{p}{2^{k-1}}(1-1/p)^{k-1}
\ \ge\ \frac{p-k+1}{2^{k-1}}\ \ge\ k.
\]

Multiplying by \(r\) and using \(kr>k(r-1)+1\) proves the strict inequality in (1).

**Closure.** Suppose this \(T\) has a certificate. For each \(q=M+1,\ldots,r-1\) replace \(P,Q\) by \((0)\mathbin{\|}(q-Q),(0)\mathbin{\|}(q-P)\), with subtraction applied vertexwise. All reflected vertices lie in \([1,q]\). The new paths are simple, end at \(q-E>0\), and add exactly \(+q,-q\) to the combined signed steps. After these extensions concatenate \(P\) with \(r+\operatorname{rev}(Q)\) and return to zero. The two paths lie in disjoint intervals \([0,r-1]\) and \([r,2r-1]\). The two joining edges have steps \(+r,-r\), giving a simple cycle with step set \(I_r\setminus T\). Scaling back in \(\mathbb F_p\) gives a cycle on the required labels \(\mathbb F_p^\times\setminus H\).

Thus the revised conjecture would prove the modular conclusion throughout (2), a range of order \(\log p\) holes. For \(k=5\), the [sharper five-coordinate slice bound](c5_interval_lift.md) supplies the initial dilation whenever \(p\ge61\), and then \(r\ge30\ge4k\) permits the same enlargement. The earlier finite proof covers every smaller prime. Hence this correction retains the entire C5 implication.

The [standalone verifier](../../experiments/exploration/complement5/verify_integer_two_path_cut.py) enumerates every placement of every retained step of the 31-hole counterexample. It checks the strict obstruction directly, as well as the threshold-cut formula for each possible cut. On the 11-hole example it independently tests all 120 orderings of the five retained labels. A closed walk anywhere in the interval would have prefix sums of width at most 8.
