## (a) Current plan

IT5 asks for two simple paths from zero to the same positive endpoint in [0,M], using every signed step in ±[1,M] outside five zero-sum holes T when the second path is read backwards. Work at exact height M=max |t|. All heights through 14 are proved by prior certificates. For M≥15, negate T if needed to include −M. Negation exchanges the two paths. The exhaustive case split is as follows.

| Case | Status |
|---|---|
| Both outer signs are holes | open |
| One outer hole and an interior opposite pair | open |
| Inverse-free, 1+4 signs | open |
| Inverse-free, 2+3 signs with −M on the two-element side | open |
| Inverse-free, 2+3 signs with −M on the three-element side | open |

## (b) Proved

Negation preserves IT5. If P,Q certify T, the combined multiset for Q,P is the negative of that for P,Q, hence is exactly the complement of −T. No unbounded construction is claimed at this checkpoint.

## (c) Refuted

No new refutation in this run.

## (d) Data

The standard-library program `experiments/exploration/complement5/it5_samples.py` selects the lowest deterministic hash scores in each sign/pair stratum, separately for minimum gap below 3 and at least 3 among distinct magnitudes. It stores one signed copy of each fully present magnitude on each path, tries four sign patterns, and verifies every positive witness. The node cap applies per individual path search. An inconclusive row is never a counterexample. JSONL records flush after each input, and restarting rechecks stored paths, skips completed rows, and retries inconclusives only at a higher budget.

Checkpoint 1. All 32 selected inputs at height 15 have verified witnesses. Exact command from the repository root:

```sh
python3 experiments/exploration/complement5/it5_samples.py --lo 15 --hi 15 --output experiments/exploration/complement5/it5_samples.jsonl --per-stratum 4 --budget 120 --seconds 20
```

## (e) Next step

Extend the same four-per-stratum witness search through height 30 and look for a general construction when both outer signs are holes.
