# Audit: compatibility Theorems A–D in the moderate-mass regime (Claude, 2026-11-24)
The submission was pasted in chat. No verifier was attached, so the examples were checked inline.

## Accepted
- **Theorem A** (P ≠ Q, T ≤ P + Q, any cardinalities: compatible extreme contraction). Proof checked by hand.
  - *Step 1.* If every P − y (y ≠ Q) lay in X, then 2R ≥ (m − 2)P + Q > 2Q ≥ 2R for m ≥ 3.
  - *Steps 2–3.* The cycle W = (C, P, −y, −E^rev) has vertex set C-path ∪ {T} ∪ E-path, with span T ≤ D. After contracting (P, −y) → c, the span is R + c ≤ Q + c ≤ D(A′), because −Q survives.
  - The m ≤ 2 cases were read.
- **Theorem B** (T ≤ P + Q: compatible ±M insertion).
  - *Case I.* The only negative vertex is h = T − P − Q < 0, and the span is P < M. The single-edge insertion theorem applies.
  - *Case II.* The peak T is the only vertex above P, so q_M ≤ 1 and the q_M theorem applies.
  - *Cases III–IV* (equal extremes) were read. The Case IV base cycle (−4, 1, 4, −2, 3, 2, −1, −3) is verified: span 8, and removing ±4 leaves span 5 ≤ 6.
- **Theorem C** (higher mass under three inequalities). Proof checked.
  - The protected vertex h = R − y is avoided because the E-path starts with Q′ > h.
  - The C-path faces at most r − 1 forbidden heights, so the grasshopper lemma applies.
  - Example verified: expanded span 10 ≤ 13, contracted span 10 ≤ 10.
- **Theorem D** (higher mass with sign-count imbalance). Read.
  - Example verified: smaller span 21 ≤ 21; after inserting ±13 the span is 25 ≤ 26.

## Scope
- Theorems A and B cover T ≤ P + Q for **all** sign cardinalities. So Targets A and B (the induction statements) now hold throughout the moderate-mass regime.
- C and D reach slightly past it, under explicit conditions.
- All four constructions use two climbs (one increasing run of C plus the peak step), so they are capped by the run-count lemma (`protected_paths_audit.md`).
- GAP A and GAP B (high mass) are therefore still the dense regime, which needs many peaks.
