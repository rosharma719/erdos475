# Asymmetric Zigzag (Z-asym) — GPT round 1 (stop rule reached) + Claude audit and adversarial tests
**Target:** Z-asym ⇒ (with proved symmetric walk + one-element reduction) Graham for every prime. NOT proved, no counterexample.
## GPT results — AUDITED IN-SESSION (experiments/audits/zasym_round_independent.py, own code)
- Two-ruler merge equivalence (exact; start at (0,0), advance X if X−Y ≤ 0, premature ties fail, final return not counted): verified — existence by merge over (σ,τ) vs direct zigzag DFS agree on 751 balanced pairs in [1..7] (0 mismatches).
- **Two-sided slack theorem:** P≠N balanced ⇒ |P| ≤ max N − 1 and |N| ≤ max P − 1 (hence ≥1 spare vertex on each side of the window). Verified on all 360,452 balanced asymmetric pairs in [1..12]: 0 violations; 1-line proof (Σ ≥ m(m+1)/2 vs ≤ D(D+1)/2, equality forces P=N=[1,D]).
- **Classification of exactly-one-hole-per-side pairs:** up to P↔N, P=[1,M], N=[1,M+1]∖{a,b}, a+b=M+1. Verified: all 60 such pairs in [1..12] are of this form.
- **Staircase family** P={q}∪[h−q+1,h], N=[h−q+2,h+1], explicit zigzag (h,−(h+1),h−1,−h,…,q): valid for all (h,q), 1≤q≤h/2, h≤129.
- Mechanism counterexamples verified: (I) canonical descending/descending + ONE relocation on ONE ruler fails for P={1,2,3,4}, N={2,3,5} (0 of the 14 attempts work; relocating on both rulers works: (4,−3,−5,2,1,3,−2)); (II) the strict outside-window rooted lift has no admissible first step for P=[1,8], N=[1,9]∖{4,5}, yet the given 15-step zigzag is valid.
- GPT's large-h annealing (P=[1,h]∖{1,4}, N=[1,h]∖{2,3}, ≤2 ascents) found no witness for h=20..80: UNDETERMINED, not a counterexample.
## Claude adversarial tests (p-free; own zigzag solver, controls: [1..7] none, {1,2,3} none, [1..5],[1..6] found)
- Merge family P=[1,h], N=[1,h]∖{a,b}∪{a+b} (both role orders), h=6..10: 164/164 found.
- Tight family (exactly one hole per side) M≤10: 24/24 found. M=11: 27/29 found, 2 UNDETERMINED at the 60M-node cap: (M,a,b)=(11,1,11), (11,2,10). Re-running with an 8-billion-node budget and a bounded cache: experiments/irc/tight_M11_a1.out, tight_M11_a2.out (results below once finished).
