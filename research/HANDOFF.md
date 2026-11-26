# Handoff (read this first; it replaces re-reading the whole corpus)

Last updated 2026-11-26 by Claude.

## Goal
Graham's rearrangement conjecture (Erdős #475): every A ⊆ F_p^× has an ordering with distinct partial sums.

## Proved or verified
- **Every prime p ≤ 43:** Graham holds for all sets (exhaustive).
- **|A| ≥ p − 5:** proved via Walecki contractions (candidate status; the selection lemma was checked computationally to p ≤ 47).
- **FV, for |B| ≤ 8 at every prime:** proved by the prime reduction plus finite checks (`claims/fv_half_path_rank_audit.md`). FV is one-point avoidance: for zero-sum B, a root t ∈ B and a forbidden point x, some valid ordering starting with t avoids x.
- **FV implies Graham.**
- **C5, |A| = p − 6:** holds for every prime p ≤ 113 (`claims/itk_c5_audit.md`).
- **C5 at every prime ⇐ IT5 at heights M ≥ 15.** Heights M ≤ 14 are verified.

## The single open target (IT5)
Let T be five nonzero integers with sum 0 and M = max |t| ≥ 15. Find two simple paths in [0, M] with these properties:
- both start at 0;
- both end at the same y > 0;
- the steps of P, together with the negated steps of Q, are exactly {±1, …, ±M} ∖ T.

Progress so far is in `claims/it5_log.md`:
- the paired holes with a unit triple are proved;
- 45 infinite rays and one explicit family are proved;
- **open:** the general case, especially the balanced 1+4 region.

## Where things are
- `ledger.md`: chronological log.
- `claims/*.md`: one file per result, with an audit.
- `experiments/`: the verifiers.
- **Branch:** `claude/amazing-maxwell-wfz06f`. Astra (GPT) pushes to `codex/itk-counterexample`.

## Rules
- Every claim gets an independent re-check before it is recorded as proved.
- Long runs must write checkpoints, so a usage cutoff loses nothing.
