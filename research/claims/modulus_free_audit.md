# Audit: modulus-free contraction and zero-pair absorption (Claude, 2026-11-24)
The submission was pasted in chat. Check script: `experiments/audits/modulus_free/zp.py`.

## Accepted (proofs checked by hand)
- **Thm 1: contraction-resistant sets are exactly {±g, …, ±kg}. ACCEPTED.**
  - If the minima differed, the difference would be a smaller element. Closure under subtracting g forces arithmetic progressions, and equal sums force r = s.
  - This is the integer analogue of the merge-pair existence result (Dias da Silva–Hamidoune) already used in the ledger.
- **Thm 2: if P ≠ Q, some admissible contraction uses P or Q. ACCEPTED.**
  - Both blocking conditions are a ↦ a − Q (mod D). Inside [−Q, P], P ≡ −Q is the only collision mod D.
  - So A ∪ {0} is a union of full residue classes mod g = gcd(P, Q), restricted to [−Q, P].
  - Each class has positive mean, and the zero class has mean (P − Q)/2. That contradicts ΣA = 0.
  - A clean and genuinely useful algebraic fact.
- **Equal-extreme classification** (A = {±M} ∪ C ∪ (C − M), 2ΣC = M|C|): ACCEPTED (same argument). Example {1, 5, 6, 8, −2, −3, −7, −8} checked.
- **Thm 3** (insert ±a, a > max|b|, around one step, when W ≤ a + 1): ACCEPTED. Brute force over all zero-sum B with values ≤ 6, |B| ≤ 6, and every valid cycle (up to 300 per set): **16,026 cases, 0 failures.**
- **Thm 4** (|B| > 4s + 2 with W = a + s): ACCEPTED. At most s + (s + 1) vertices are unsafe, so by pigeonhole two consecutive safe vertices exist. The proof is direct.
- **Fixed-order sharpness example** ((−3, −2, −1, 2, 3, 1) with ±4): already reproduced in `protected_greedy_audit.md`.

## Scope of the two remaining targets
- **Target A** (unequal extremes): Thm 2 gives existence of the extreme contraction. Making expansion compatible is the cycle-choice problem.
- **Target B** (equal extremes): zero-pair absorption needs the smaller cycle to be compact.
  - The vertices of a cycle of span W number at most W + 1. So Thm 4's condition |B| > 4(W − M) + 2 forces **W < 4M/3**, and Thm 3 needs W ≤ M + 1.
  - Induction on BS only supplies W ≤ diam(B), which can be about 2M − 2 for dense B.
  - So Target B via zero-pair absorption needs a **strengthened** hypothesis (span ≲ 4M/3 for A ∖ {±M}). That hypothesis is not supplied by induction and is not known.

**Status.** The algebraic selection step is closed (Thms 1–2). Both geometric targets are still the cycle-choice / compression problem. The dense regime is open.
