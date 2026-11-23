# GPT round: Task A (primary-source quantitative map) + Task B (EC cycle selection) — AUDIT (Claude)

## Task A (literature) — GPT-REPORTED, NOT verified by Claude (no primary-source access from this environment). Treat as leads.
- Costa–Della Fiore (Feb 2026, arXiv 2602.19989): small sets |A| ≤ exp(c (log p)^{1/3}), c unspecified (improves Bedert–Kravitz's exponent 1/4).
- Pham–Sauermann: explicit 2^24 in the anticoncentration theorem; C_α constrained by C_α ≥ (10^4·2^{40D})^{1/α}, D=⌈3/α⌉, C_α ≥ (D+1)2^D D^{14D²}, plus constants C_D,C_1 not evaluated.
- Müyesser–Pokrovskiy Thm 6.9: prescribed edge-colour set (≥ p−√p labels) AND vertex set AND endpoints ⇒ rainbow Hamilton path (n≥n0 non-explicit). GPT's corollary: for sufficiently large p and zero-sum B with |B| ≥ p−√p+1, any z∈B and any R ⊆ F_p∖{0,z}, |R| ≤ p−|B|, there is a valid rooted cycle avoiding R (conditional on the theorem statement and large p). The reduction from the theorem to the corollary was re-read by Claude and is logically sound GIVEN the quoted statement; the statement itself is unverified.
- HOS Lemma 4.5: exceptions exactly (d,r) ∈ {(2,4),(2,5),(2,8)} (Claude's own search for r≤13 agrees).
- The e^(10^10) threshold estimate in the ledger is WITHDRAWN as an unaudited estimate (GPT: it used the outdated 1/4 exponent and unevaluated constants). No numerical all-primes threshold is currently justified either way (GAP-A1).

## Task B — Claude audit (experiments/audits/extremal_selection_independent.py, mobility_selection_search.py)
- Energy minimisation does not force avoidance — VERIFIED: p=41, B={10,21,25,31,36}, z=10, r=5: 12 valid rooted cycles, min E_+=12 at 2 cycles, both visit 5, 4 avoiders exist; also B={6,7,9,28,35,38}, z=6, r=3 (44 cycles, 2 minimisers both visit 3).
- Swap-mobility maximisation: GPT's instance B={3,5,13,28,33}, z=3, r=8 is WRONG — its mobility formula uses v[i-1]+a[i+1] (off by one; the swap of steps i,i+1 changes the vertex to v[i]+a[i+1]). With true mobility (perform each swap and test validity) the maximum is 3, attained by 4 cycles, three of which avoid 8. The CLAIM is nevertheless true: genuine counterexample p=41, B={2,7,16,25,32}, z=32, r=16: 12 valid rooted cycles, max true mobility 3 at four cycles, all four visit 16, an avoider exists. Sampled search found 110/14/120/95/3 such (B,z,r) at (p,k)=(41,5),(41,6),(43,5),(47,5),(47,6).
- Minimal zero-sum MC theorem — VERIFIED: p=23 (1,144 sets), p=29 (7,004 sets): every sampled ordering valid, every swap valid (1.1M swaps, 0 invalid).
- Reflection identity K(B,z)=z−K(B,z): hand-checked.
LESSON: the off-by-one is exactly the kind of error independent code catches; GPT's earlier swap tables (p=13,k=6; p=17,k=7) used a different script and remain unaudited.
