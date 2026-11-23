# GPT rounds: doubling rigidity (symmetric interval) + skewed-tight hole bound (2026-11-22)
Status: candidates, audited by independent code (experiments/irc/audit_doubling.py running, audit_skew.py done). NOT promoted.
- T1 symmetric [1..M] zigzag iff 2M+1 prime & 2 primitive root: SAT decider agrees M=1..12 (exact). Proof (square-energy + rearrangement) is a valid short argument.
- T2 contraction for (M+1)%3==0 & T1 holds: conditional subcase only.
- Conjecture R (<=2 ascents per ruler) refuted at P=[1,7], N={1,3,4,5,7,8} (GPT 472,320 pair check; my re-run pending in audit_doubling.py).
- T3 skewed tight P=[1..M], N={2..M-1,M+1}: (M-u)^2+(M-v)^2 <= u+3v-2-2[v=1] <= 4M-2. Exhaustive enumeration of ALL zigzags M=3..9 (5,8,14,19,51,56,135): 0 violations; holes hug far ends.
- T4 no single-edge M->M+1 lift for M>=10 (arithmetic checked by hand: u+v=M+1 vs M^2-10M+5<=0).
- Energy minimiser P={1,5},N={1,2,3}: unique min (1,-2,-1,5,-3), E=15, not zigzag: confirmed.
Takeaway: tight family needs nonlocal construction; no counterexample; SAT sweeps (tight/twoomit/merge) all FOUND through h=15-16.
