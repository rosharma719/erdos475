## (a) Current plan

IT5 asks for two simple paths from zero to the same positive endpoint in [0,M], using every signed step in ±[1,M] outside five zero-sum holes T when the second path is read backwards. Work at exact height M=max |t|. All heights through 14 are proved by prior certificates. For M≥15, negate T if needed to include −M. Negation exchanges the two paths. The exhaustive case split is as follows.

| Case | Status |
|---|---|
| Both outer signs are holes | proved when the asymmetric triple contains a unit; other triples open |
| One outer hole and an interior opposite pair | proved when the asymmetric triple contains a unit; other triples open |
| Inverse-free, 1+4 signs | proved on the arithmetic class below, including six certified unbounded rays; otherwise open |
| Inverse-free, 2+3 signs with −M on the two-element side | proved on the arithmetic class, including 34 certified unbounded rays; otherwise open |
| Inverse-free, 2+3 signs with −M on the three-element side | proved on the arithmetic class, including five certified unbounded rays; otherwise open |

The cut-stretch construction below is proved for every certificate satisfying its stated interval test. The five case rows describe the remaining generality.

## (b) Proved

Negation preserves IT5. If P,Q certify T, the combined multiset for Q,P is the negative of that for P,Q, hence is exactly the complement of −T.


**Stretch at an internal width.** Suppose a certificate for T of height M is given and 1≤d<M. On each path choose a prefix ending at x and a suffix beginning there. For that path choose [A,B] of width d with x=A or x=B. Both paths must choose the same side, but their intervals may differ. Require all suffix vertices in [A,B], all prefix vertices in [0,A] or [B,M], and the opposite boundary absent from the prefix. Require a prefix edge to run between the two outside intervals exactly when its magnitude exceeds d. For every integer t≥0 the holes obtained by adding 2t to the magnitude of every hole larger than d and leaving the other holes fixed have an IT5 certificate at height M+2t.

**Proof.** Leave the lower prefix vertices fixed and translate the upper prefix vertices by 2t. Translate the entire suffix by t. For an anchor x=A bridge the gap by following A, B+2t, A+1, B+2t−1, A+2, …, B+t+1, A+t, then follow the translated suffix from its initial A+t. For x=B reflect this prescription in the map v↦A+B+2t−v, giving a bridge from B+2t to B+t. When t=0 use the original path. All vertices lie in [0,M+2t]. The translated suffix lies in [A+t,B+t]. Apart from its final vertex the bridge avoids that interval. Its only possible intersection with the transformed prefix beyond the starting anchor would be the opposite outside endpoint, which the hypothesis excludes. For t>0 the prefix and translated suffix are disjoint. The two paths still begin at zero (if A=0 it belongs to the lower prefix) and end at the original common endpoint plus t. Each old step of magnitude above d increases in magnitude by 2t, with its sign unchanged; every other old step is unchanged. The new bridge takes precisely the magnitudes d+1 through d+2t, in descending order and alternating signs. The two bridges have identical signed lists because their anchor sides agree. Reading the second backwards supplies the opposite signed copy of every new magnitude. This proves the label identity and simplicity for every t.


**Paired holes with a unit in the asymmetric triple.** Up to negation these are exactly T={−h,h,1,c−1,−c}, with c≥3 and h distinct from 1,c−1,c. Every admissible h is allowed.

**Proof.** First take h<c. Begin P at (0,c) and Q at (0,1,c). From their shared vertex c attach the same tail to both paths. Use the magnitudes in {2,…,c−2} except h in decreasing order, taking the first jump down, the next up, and alternating thereafter. If the first magnitude is v, the tail stays in [c−v,c]⊆[2,c] and is simple. Indeed every new vertex after the first edge lies strictly between the ends of the preceding edge since the sign alternates and the magnitude decreases, giving nested intervals with no vertex revisited. An empty tail is also valid. The two initial pieces supply +c,−1,−(c−1); all other required magnitudes occur in both signs on the shared tail. The tail avoids both 0 and 1, and its endpoint is positive. When h>c, first use the same construction at height c without omitting a tail magnitude. To add a symmetric magnitude q from c+1 through h−1, replace the pair by (0) followed by q−Q and (0) followed by q−P, with pointwise reflection. The reflected vertices are positive; the exchange preserves old combined labels and the two initial jumps add ±q. The new endpoint q−y is positive. At the end both paths lie in [0,h−1] and use exactly the required labels for height h with both ±h absent. This covers every placement of an opposite pair for this triple type.


**Arithmetic criterion for synchronized prefixes and a common nested tail (all five cases).** Put U={−t : t∈T and −t∉T}, K=max{|u| : u∈U}, and F={|t| : t∈T and |t|≤K}. Test all orders of U and all their nonempty proper cuts. From zero, use the first part as P's steps and the negatives of the second part as Q's steps. Require each prefix simple and in [0,K], and their common endpoint y positive. Let V be the union of the two prefixes' vertices before y. Partition [1,K] outside F into descending maximal consecutive runs. For each of the two choices of sign, test the following inequalities. At the beginning of a run h,…,l let the current vertex be z and current sign ε. Put n=h−l+1. Take the integer intervals with endpoints (z,z+ε⌊n/2⌋) and (z+εh,z+ε(h−⌊(n−1)/2⌋)). Require both inside [0,K] and disjoint from V. Continue from the last even or odd vertex according to n, flipping ε exactly when n is odd. Acceptance of any prefix and sign implies IT5 at the original height. The test uses at most 480 ordered cuts and two signs, and at most six runs per sign, independently of M. It describes an explicit arithmetic class of five-sets.

**Proof.** The two prefix sums agree because U sums to zero. Their combined signed steps are precisely U. Append the same jumps of descending magnitude in [1,K] outside F to each path, alternating signs throughout. In a consecutive run the vertex after 2i steps is z+εi, and after 2i+1 steps it is z+ε(h−i), by grouping adjacent terms. The two integer intervals are exactly all visited vertices, so the tests are necessary and sufficient for these tails to remain in bounds and avoid both prefixes before y. The alternating tail is simple by strict nesting, as proved above. The endpoint cannot be zero since zero is in V. Each magnitude outside F occurs once with each sign. If K<M, both outer holes are ±M, and the reflection-and-exchange extension from the preceding proof supplies ±(K+1),…,±(M−1). If K=M, no extension is required. This accounts for every label and both endpoints. Conversely any construction of precisely this stated form passes the inequalities using its prefix and initial sign, so rejection describes the exact remaining cases for this construction, not a failure of IT5.


**Affine certificates at unbounded height.** Fix an accepted inverse-free input B and its ordered prefixes. Write T(n)=B+2nD coordinatewise for an integer direction D of sum zero having the same entry signs and the same strict magnitude order as B. Require the base magnitudes and their consecutive gaps to be at least two at the bottom and between magnitudes, respectively. Keep the prefix steps attached to the same signed input coordinates. Form the signed comparison list consisting of the common prefix endpoint, each prefix coordinate and its distance from M, every within-prefix coordinate difference, each tail interval's lower bound and distance from its upper bound to M, and both bounds of each interval minus each forbidden prefix vertex. For every comparison require that its value at n=1 has moved weakly away from zero in its sign at n=0, keeping an initial zero fixed. Then T(n) has a certificate for every integer n≥0.

**Proof.** Increments are even, so every consecutive run keeps its length parity; the ordering and positive gaps ensure the same runs exist for all n. The run formulas in the preceding proof show by induction that all their endpoints, and hence all listed comparisons, are affine integer functions of n. Ordering the two ends of a run interval is consistent for all n since its direction is fixed and its length stays positive. The single slope test preserves every initial sign and equality. Therefore every prefix remains simple and within bounds, every forbidden vertex stays outside every tail interval, and the final two-path construction still works. This also proves every row with a direction in the finite manifest, using exact integer arithmetic. Since all direction magnitudes are positive and strictly ordered, even the minimum magnitude and every gap tend to infinity.

**Hand-checkable inverse-free certificate.** For every integer N≥1 let M=26N−1 and T={−M,2N,6N−1,8N,10N}. Start P=(0,M), Q=(0,8N,14N−1,16N−1,M), and append to both the same alternating descending tail from M. For clarity, its missing vertices can be computed without searching. Start with L=0, R=M, current side high. At each magnitude k=M−1,…,1 the current interval has width k+1. If the current side is high, increment L; otherwise decrement R. For a present magnitude jump to that new frontier and switch sides, an edge of length k. For a missing magnitude skip that frontier and keep the side. Pairing consecutive updates in each present run gives the following states just before skipping.

| k | L | R | Current side | Skipped vertex |
|---:|---:|---:|---|---:|
| 10N | 8N−1 | 18N | high | 8N |
| 8N | 9N | 17N+1 | low | 17N |
| 6N−1 | 10N | 16N | low | 16N−1 |
| 2N | 12N−1 | 14N | low | 14N−1 |

The fronts move inwards, so none of the skipped vertices is later visited. Zero is also outside the tail. This excludes all three intermediate Q vertices, and the prefix labels in the combined orientation are +M,−8N,−(6N−1),−2N,−10N. The shared tail supplies both signs of all remaining magnitudes. This is a primitive class since gcd(2N,6N−1)=1. For N≥2 the magnitudes are pairwise at distance at least three.

## (c) Refuted

**The common nested tail cannot cover the balanced 1+4 region.** Let T={−M,a,b,c,d}, with 2≤a<b<c<d<M/3 and a+b+c+d=M. The first path's prefix must include +M, since the second path could only contribute this label by taking −M into the already visited zero. The other prefix has only positive steps, so its endpoint y is at least 2; if the first prefix uses any negative step, y≤M−2. Since M−1 is present in the common tail, such an interior y cannot be its start. Hence the prefixes are (0,M) and an increasing four-step path from 0 to M. From M the common tail is forced to use −(M−1), +(M−2), … down through magnitude d+1. Its odd-numbered vertices are 1,2,… up to at least d because M−d−1≥2d. Thus it visits whichever of a,b,c,d was the first intermediate vertex of the increasing prefix. This rules out the entire normal form. The examples T=n·{−46,10,11,12,13}, n≥3, have all five magnitudes mutually separated by at least three. This is a refutation of the construction only.

## (d) Data

The standard-library program `experiments/exploration/complement5/it5_samples.py` selects the lowest deterministic hash scores in each sign/pair stratum, separately for minimum gap below 3 and at least 3 among distinct magnitudes. It stores one signed copy of each fully present magnitude on each path, tries four sign patterns, and verifies every positive witness. The node cap applies per individual path search. An inconclusive row is never a counterexample. JSONL records flush after each input, and restarting rechecks stored paths, skips completed rows, and retries inconclusives only at a higher budget.

Checkpoint 1. All 32 selected inputs at height 15 have verified witnesses. Exact command from the repository root:

```sh
python3 experiments/exploration/complement5/it5_samples.py --lo 15 --hi 15 --output experiments/exploration/complement5/it5_samples.jsonl --per-stratum 4 --budget 120 --seconds 20
```

Checkpoint 2. The selected domain has 599 distinct inputs at M=15 through 30. At per-path budgets 120, 1800, and 10000, respectively 592, 598, and 598 have verified witnesses. The single remaining input under those four sign patterns was (−25,−21,9,18,19). Exact commands:

```sh
python3 experiments/exploration/complement5/it5_samples.py --output experiments/exploration/complement5/it5_samples.jsonl --per-stratum 4 --budget 120 --seconds 75
python3 experiments/exploration/complement5/it5_samples.py --output experiments/exploration/complement5/it5_samples.jsonl --per-stratum 4 --budget 1800 --seconds 60
python3 experiments/exploration/complement5/it5_samples.py --output experiments/exploration/complement5/it5_samples.jsonl --per-stratum 4 --budget 10000 --seconds 45
```

Checkpoint 4. The direct arithmetic test and a separate step-by-step construction agree on all accepted normalized inputs at height 15. Of 376 inputs, 63 pass (51 paired, 11 inverse-free 2+3, one inverse-free 1+4). The program records every input, accepting prefix, and result, then checks the actual paths. Exact command:

```sh
python3 experiments/exploration/complement5/it5_nested.py --lo 15 --hi 15 --seconds 25 --output /private/tmp/it5-nested-census
```

Checkpoint 5. The 1+4 refutation is by the parameterized proof in (c). The arithmetic test computed 26,059 further normalized inputs in heights 16…30, with 1,452 accepted, using the following resumable command:

```sh
python3 experiments/exploration/complement5/it5_nested.py --lo 16 --hi 30 --seconds 45 --output /private/tmp/it5-nested-census
```

Checkpoint 6. Across the full normalized census, 46 accepted inverse-free bases have minimum magnitude and minimum gap at least two. The verifier found certified strictly separating directions of height at most 24 for 45 of them (six 1+4, 34 with −M on the two-element side, five with −M on the three-element side). One base, (−27,2,4,7,14), had no direction found under that cap and prefix. The checked manifest contains every base and direction. Exact discovery and replay commands:

```sh
python3 experiments/exploration/complement5/it5_affine.py --manifest experiments/exploration/complement5/it5_rays.jsonl --census /private/tmp/it5-nested-census --seconds 45
python3 experiments/exploration/complement5/it5_affine.py --manifest experiments/exploration/complement5/it5_rays.jsonl
```

Checkpoint 7. Allowing one flipped common sign produces the missing height-25 certificate; all 599 sampled inputs are now verified. The first program now also supports complete enumeration and ties the result to the actual signed pattern. Exact commands for the completed sample and bounded full-census run:

```sh
python3 experiments/exploration/complement5/it5_samples.py --output experiments/exploration/complement5/it5_samples.jsonl --per-stratum 4 --budget 120 --flip-one --seconds 45
python3 experiments/exploration/complement5/it5_samples.py --all --output /private/tmp/it5-all-15-30.jsonl --budget 120 --flip-one --seconds 60
```

## (e) Next step

For the balanced 1+4 region 2≤a<b<c<d<M/3, let the two paths place some symmetric labels in different orders before sharing a tail, and test those placements against the frontier inequalities.
