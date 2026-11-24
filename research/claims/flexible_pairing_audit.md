# Audit: flexible-pairing round (Claude, 2026-11-24)
The submission was pasted in chat; no verifier file was attached. The explicit examples were checked inline.

## Accepted
- **Flexible-pairing theorem (|X| = |Y|, 0 < t < K ⇒ span ≤ P + Q): ACCEPTED.**
  The two-frontier argument was checked by hand:
  - A new edge from x has upper candidate x + M_new. Every older edge on the opposite path has upper candidate ≤ x + H < x + K. So only the opposite path's most recent edge can collide, which rules out one high magnitude.
  - The core-endpoint collision rules out one low magnitude, independently.
  - Each edge consumes one high and one low magnitude.
  - There is at most one lower expansion, at t − M.
  - Span: t + H < K + H ≤ P + Q, and M + H ≤ P + Q, because H < min(P, Q).
- **Inverse-pair and tied-median extension:** accepted as a candidate (read, not re-derived).
- **Congruence-separated theorem: ACCEPTED.** Assume every magnitude is ≡ r (mod g) with r, 2r ≢ 0 (mod g), and t + H ≤ P + Q. Then core vertices are ≡ 0, upper vertices ≡ r, and the lower vertex ≡ −r.
- **Examples verified:**
  - noncompact (every value ≡ 1 mod 6): span 463 ≤ 476;
  - 16-element repair: span 587 < 791;
  - obstruction instance: span 24 ≤ 31;
  - family X_s, Y_s: t = 8s² and D = 16s − 1, exactly as stated.

## Scope
Every theorem here uses a two-monotone-path core, whose span is at least t. So it needs t ≤ D − H, the same two-climb ceiling as the run-count lemma in `protected_paths_audit.md`.
The submission's own family X_s, Y_s, with t/D → ∞, confirms this: dense sets need cores with Ω(n) climbs.
The congruence theorem relaxes compactness but not this ceiling.

**Remaining.** A non-monotone, many-climb core with collision control. The only proved many-climb mechanisms are the spiral constructions (symmetric walk, `rooted_symmetric.md`). The natural next target is a contraction whose core is a spiral, rather than two monotone paths.
