# Audit: effective threshold via NTV specialised to Z_p (Claude, 2026-11-24)
The submission was pasted in chat. It was checked against the NTV PDF text, extracted locally from arXiv:2610.40712v1, and the arithmetic was recomputed.

## Verified
- **Z_p simplifications.**
  - The only subgroups are {0} and Z_p, so Lemma 3.3's reservoir alternative and Case 2(a) disappear.
  - Section 6's dense condition is the δ^28500 term, and in Z_p δ = n/p ≥ n^(−ε). So the allowed range becomes ε < 1/28500, against ε < 1/57000 in general.
- **Local-repair constants.**
  - Lemma 4.2: P(B₀) ≤ 2^(40D+3)·q.
  - Lemma 4.4: 2n(5D)^(2D)·**2^(26D²)**·F. The exponent was confirmed from the derivation 2^(D(15D+1))·2^(10D²) ≤ 2^(26D²).
  - The split criterion A_D·q + B_D·n·F < 1/2 (E5) is legitimate.
- **Arithmetic.**
  - Original parameters (ε = 10⁻⁵, D = 4·10⁵): L > 1.6000·10¹² and L > 1.3867·10¹².
  - Retuned (ε = 1/30000, D = 60000): at L = 9.4·10¹⁰ the two exponents are −733,313 and −394,839,998.
  - The bound is about max(40x/ε², 26x²/(ε²(x − 1))) with x = εD, minimised at x = 2 (about 104/ε²). So this architecture's sparse threshold cannot drop much below about 8·10¹⁰ bits.
- **Theorem B.1 (very dense sets, imported from Müyesser–Pokrovskiy via Bedert–Bucić–Kravitz–Montgomery–Müyesser): verbatim "of sufficiently large order"**, for |S| ≥ |G| − |G|^(1 − 2^(−20)). **Non-explicit; this is the blocking ingredient.**
- **(E11) arithmetic** at 2^(10¹⁰⁵) and 2^(10¹⁰⁶): verified. The underlying requirement q ≥ p^(−1/10¹⁰²) in MP Thm 4.9 was **not** verified (MP paper not read).

## Result (conditional)
Using NTV's numbered lemmas as published, every A ⊆ Z_p^× with **2^(9.4·10¹⁰) ≤ |A| < p − p^(1 − 2^(−20))** is rearrangeable.
- The sparse branch is a closed explicit chain.
- The dense branches rely on NTV Lemma 5.7 as stated; its imported constants (MP Lemma 3.4) are not audited.
- The near-complete band is blocked by Theorem B.1.

## Assessment
- **This is the first explicit large-size range for Erdős #475.** It is publishable-type progress.
- **It cannot finish the conjecture.** Even a fully explicit C leaves every size below about 2^(9.4·10¹⁰) open, which is uncheckable.
- **Natural next target.** An explicit near-complete theorem for |F_p^× ∖ A| ≤ p^(1−c), by contracting the sparse complement inside an explicit rotational (Walecki or graceful) sequencing, as in the repo's |C| ≤ 5 proofs. This would remove the MP dependency and make the global threshold explicit.
