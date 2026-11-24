# Audit: peak-removal / optimal-span round (Claude, 2026-11-24)
The submission was pasted in chat and is summarised here. Check script: `experiments/audits/peak_removal/check5.py`.

- **Thm 1, separation from 0: ACCEPTED.**
  - Statement: X, Y are sets of distinct positive integers with ΣX ≠ ΣY. Then some orderings have disjoint nonempty partial sums.
  - The proof (minimise common sums, then their total) checks out by hand.
  - Exhaustive check for |X|, |Y| ≤ 4 and values ≤ 9: 61,854 pairs, 0 failures.
- **Peak removal: ACCEPTED.**
  - Construction: W = (X′, −b, a, −Y′^rev). Its vertices are the two path vertex sets plus h = T − a − b.
  - It is simple whenever h < 0, or h > 0 and h avoids both paths.
  - Span = T − min(a, b) − min(0, h). This follows directly from Thm 1.
- **Optimal span: ACCEPTED.**
  - Statement: if P ≠ Q and T < P + Q, then the minimum span is max(P, Q).
  - This covers only the regime where the positive mass is below P + Q, which is sparse.
- **Examples: verified.**
  - (2, 3, 4, 5, −13, 29, −9, −8, −7, −6) has span 30.
  - (8, −6, 1, −4, 7, −2, −3, −1) has span 9.
- **3-path counterexample (endpoints 2/4/6, steps {1, 2}, {3, 4}, {5, 6}): correct.** Each path's only interior vertex is 0 or 1. This duplicates `bs_handoff_audit.md`'s finding that k-path separation is false.
- **Not checked:** the exact extreme-expansion theorem, the large-inverse-pair padding theorem, and the protected two-path data (4,067 cases, not rerun).
- **Verdict.** These are useful tools for sparse and moderate mass, roughly T ≤ P + Q + min(P, Q). The dense regime T ≫ P + Q, where the top elements have no gap (see `bs_handoff_audit.md`), is untouched. The conjecture is still open.
