## (a) Current plan

IT5 asks for two simple paths from zero to the same positive endpoint in [0,M], using every signed step in ±[1,M] outside five zero-sum holes T when the second path is read backwards. Work at exact height M=max |t|. All heights through 14 are proved by prior certificates. For M≥15, negate T if needed to include −M. Negation exchanges the two paths. The exhaustive case split is as follows.

| Case | Status |
|---|---|
| Both outer signs are holes | open |
| One outer hole and an interior opposite pair | open |
| Inverse-free, 1+4 signs | open |
| Inverse-free, 2+3 signs with −M on the two-element side | open |
| Inverse-free, 2+3 signs with −M on the three-element side | open |

The cut-stretch construction below is proved for every certificate satisfying its stated interval test. The five case rows describe the remaining generality.

## (b) Proved

Negation preserves IT5. If P,Q certify T, the combined multiset for Q,P is the negative of that for P,Q, hence is exactly the complement of −T.


**Stretch at an internal width.** Suppose a certificate for T of height M is given and 1≤d<M. On each path choose a prefix ending at x and a suffix beginning there. For that path choose [A,B] of width d with x=A or x=B. Both paths must choose the same side, but their intervals may differ. Require all suffix vertices in [A,B], all prefix vertices in [0,A] or [B,M], and the opposite boundary absent from the prefix. Require a prefix edge to run between the two outside intervals exactly when its magnitude exceeds d. For every integer t≥0 the holes obtained by adding 2t to the magnitude of every hole larger than d and leaving the other holes fixed have an IT5 certificate at height M+2t.

**Proof.** Leave the lower prefix vertices fixed and translate the upper prefix vertices by 2t. Translate the entire suffix by t. For an anchor x=A bridge the gap by following A, B+2t, A+1, B+2t−1, A+2, …, B+t+1, A+t, then follow the translated suffix from its initial A+t. For x=B reflect this prescription in the map v↦A+B+2t−v, giving a bridge from B+2t to B+t. When t=0 use the original path. All vertices lie in [0,M+2t]. The translated suffix lies in [A+t,B+t]. Apart from its final vertex the bridge avoids that interval. Its only possible intersection with the transformed prefix beyond the starting anchor would be the opposite outside endpoint, which the hypothesis excludes. For t>0 the prefix and translated suffix are disjoint. The two paths still begin at zero (if A=0 it belongs to the lower prefix) and end at the original common endpoint plus t. Each old step of magnitude above d increases in magnitude by 2t, with its sign unchanged; every other old step is unchanged. The new bridge takes precisely the magnitudes d+1 through d+2t, in descending order and alternating signs. The two bridges have identical signed lists because their anchor sides agree. Reading the second backwards supplies the opposite signed copy of every new magnitude. This proves the label identity and simplicity for every t.

## (c) Refuted

No new refutation in this run.

## (d) Data

The standard-library program `experiments/exploration/complement5/it5_samples.py` selects the lowest deterministic hash scores in each sign/pair stratum, separately for minimum gap below 3 and at least 3 among distinct magnitudes. It stores one signed copy of each fully present magnitude on each path, tries four sign patterns, and verifies every positive witness. The node cap applies per individual path search. An inconclusive row is never a counterexample. JSONL records flush after each input, and restarting rechecks stored paths, skips completed rows, and retries inconclusives only at a higher budget.

Checkpoint 1. All 32 selected inputs at height 15 have verified witnesses. Exact command from the repository root:

```sh
python3 experiments/exploration/complement5/it5_samples.py --lo 15 --hi 15 --output experiments/exploration/complement5/it5_samples.jsonl --per-stratum 4 --budget 120 --seconds 20
```

Checkpoint 2. The selected domain has 599 distinct inputs at M=15 through 30. At per-path budgets 120, 1800, and 10000, respectively 592, 598, and 598 have verified witnesses. The single remaining input under the four sign patterns is (−25,−21,9,18,19). Exact commands:

```sh
python3 experiments/exploration/complement5/it5_samples.py --output experiments/exploration/complement5/it5_samples.jsonl --per-stratum 4 --budget 120 --seconds 75
python3 experiments/exploration/complement5/it5_samples.py --output experiments/exploration/complement5/it5_samples.jsonl --per-stratum 4 --budget 1800 --seconds 60
python3 experiments/exploration/complement5/it5_samples.py --output experiments/exploration/complement5/it5_samples.jsonl --per-stratum 4 --budget 10000 --seconds 45
```

## (e) Next step

Construct interval-compatible prefixes and suffixes symbolically for outer paired holes and an arbitrary remaining triple; validate internal stretches independently on the stored witnesses.
