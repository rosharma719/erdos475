# Audit: "bounded-span reduction" and "independent-switch closure" submission (Claude, 2026-11-24)

The submitted scripts are in `experiments/audits/bounded_span_and_switches/`, unchanged, together with the rerun output `bs.out`.

## §1 Balanced integer lift: CORRECT, ALREADY IN THE REPO
This is the integer reduction proved in `integer_range.md`: subtract p from the k largest representatives, giving P + Q ≤ p − 1. Nothing new.

## §2 Bounded-span sequencing conjecture: ALREADY IN THE REPO (it is IRC with the bound weakened by 1)
- **The submission's version:** span ≤ P + Q.
- **Repo IRC (`integer_range.md`, node `IRC`):** span ≤ P + Q − 1. This is stronger, and has held in 1,888,173 instances (values ≤ 18, n ≤ 9).
- **IRC+ (`claude_lane.md` L5):** span ≤ P + Q when P + Q is even, P + Q + 1 when it is odd. This is the weakest form that still implies Graham.

The submitted conjecture sits between IRC and IRC+, so it is implied by IRC. It is the existing Programme C target, not a new reduction.
Tightness is already known: span ≤ P + Q − 2 fails, for example P = N = {5, 6}.

**Rerun.** `bounded_span_audit.py` reproduces the table exactly: max |b| ≤ 11, 103,129 sets, 0 failures. The solver is correct: rotating so the minimum vertex is 0 justifies searching inside [0, P + Q].
This is weaker evidence than the repo's IRC data, since it tests a looser bound on smaller values.

## §4 Sign-greedy walk: CORRECT, KNOWN
- The bounded non-simple walk is the zigzag rule from `integer_range.md`.
- Zigzag failing on {±1, ±2, ±3} is the exceptional family a·{1, 2, 3} of Z\*.
- The example (1, −2, 3, 2, −1, −3) checked: partial sums 1, −1, 2, 4, 3, 0, span 5 ≤ 6.

## §5 Independent-switch closure theorem: ACCEPTED as a candidate (hand check)
**Setting.** Repair is done only by pairwise non-adjacent adjacent-transpositions that keep the contracted edges' origins fixed. In that setting the forced closure R is necessary, and switching exactly R is sufficient under the four conditions:
- no contracted incidences;
- no overlapping switches;
- the values f(R) are distinct;
- f(R) ∩ K = ∅. This condition was lost in the submitted text but is present in the code.

**Not checked.** The remark that a closure decomposes into paths that can be executed backwards, keeping every intermediate cycle valid.

## §6 Switch-budget examples: REPRODUCED
`core_search.cpp` was rerun. Its built-in check confirms that the output uses every label of A once and has distinct partial sums mod p. It was not re-implemented independently.
- **p = 1009**, U = {107, 146, 381, 531, 853} (|A| = 1003): FAIL with cap 1 (725,760 candidates). PASS with cap 2: l = 118, sign +, d = 863, e = 628, D = (756, 107), E = (253, 853, 531), switches at 268 and 803.
- **p = 2003**, U = {386, 1154, 1446, 1472, 1551} (|A| = 1997): FAIL with cap 3 (1,441,440 candidates). PASS with cap 4: l = 218, sign −, d = 452, e = 557, D = (1154, 1301), E = (1472, 702, 386), switches at 1991, 799, 1986, 1595.

So no fixed switch budget suffices for the symmetric-core repair route. These are finite examples, not a theorem.

## Verdict
- **Rediscoveries:** §§1, 2 and 4 duplicate existing repo material. The submission's recommendation, "prioritize bounded-span integer sequencing", amounts to "prove IRC (or IRC+)", which is already open gap G1 in `integer_range.md`.
- **Candidates:** the closure theorem (§5) and the switch-budget examples (§6) are new and are banked here.
