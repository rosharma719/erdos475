# GPT rounds: doubling rigidity (symmetric interval) + skewed-tight hole bound (2026-11-22)
Status: candidates, audited by independent code (experiments/irc/audit_doubling.py running, audit_skew.py done). NOT promoted.
- T1 symmetric [1..M] zigzag iff 2M+1 prime & 2 primitive root: SAT decider agrees M=1..12 (exact). Proof (square-energy + rearrangement) is a valid short argument.
- T2 contraction for (M+1)%3==0 & T1 holds: conditional subcase only.
- Conjecture R (<=2 ascents per ruler) refuted at P=[1,7], N={1,3,4,5,7,8} (GPT 472,320 pair check; my re-run pending in audit_doubling.py).
- T3 skewed tight P=[1..M], N={2..M-1,M+1}: (M-u)^2+(M-v)^2 <= u+3v-2-2[v=1] <= 4M-2. Exhaustive enumeration of ALL zigzags M=3..9 (5,8,14,19,51,56,135): 0 violations; holes hug far ends.
- T4 no single-edge M->M+1 lift for M>=10 (arithmetic checked by hand: u+v=M+1 vs M^2-10M+5<=0).
- Energy minimiser P={1,5},N={1,2,3}: unique min (1,-2,-1,5,-3), E=15, not zigzag: confirmed.
Takeaway: tight family needs nonlocal construction; no counterexample; SAT sweeps (tight/twoomit/merge) all FOUND through h=15-16.

## Round 3 (GPT direct even-M map for a=1) — my audit, experiments/irc/audit_even.py
- f(s)=2s+M (s<=0), 2s-M-3 (s>0 even), 2s-M+1 (s>0 odd) on V=[-M+1,M]\{M-1}: verified a zigzag-sign cycle cover with EXACT step sets P=[1,M], N={2..M-1,M+1} for all even M<=600.
- Cycle structure is NOT mostly one cycle: single cycle only at M=4,8,10,20,28,32,34,64,80,158,206,332,350 (13 of 299 even M<=600); looks like random-permutation behaviour. M=2^k: one cycle iff X^(k+1)+X+1 primitive (matches 4,8,32,64 yes; 16,128 no).
- M=20 certificate reproduced.
- Consequence: arithmetic cycle-cover maps give existence only conditional on Artin-type facts. A proof needs cycle JOINING with step multisets preserved (GPT's own sec.5 caveat) or a non-arithmetic (recursive) construction. Bounded-edit-of-doubling impossible (T4 bound, K>=2M/k-3).

## Cycle-joining probe (experiments/irc/switch_join.py, sw run)
GPT even-M cover (a=1) at M=6,12 (3 cycles): number of label-preserving k-switches (reassign labels among k same-side sources, target set preserved) for k=2..5 is ZERO. The cover is rigid (it sits at the energy-extremal assignment for its holes), so local joining is impossible, consistent with the energy identity. Any proof must move to covers with different hole pairs (u,v)/larger defect, i.e. the joining move must change the holes, not permute labels.

## Round 4 audit (GPT all-in-one file) — experiments/irc/audit_round4.py
- Scaled escape family P=L[1,7]+{3}, N=L[1,7]+{1,2}: valid zigzag, range<=maxP+maxN-1 for L=4..399. (L<=3 gives non-sets.)
- Fixed scaffold M=16 a=1: exactly 1 negative bijection (independent recursion) -> matches.
## Minimal-hole lemma (mine, proved by hand)
holes = maxP+maxN-|P|-|N|. For balanced P!=N: holes>=2, with equality iff (up to swap) P=[1,M], N=[1,M+1]\{a,b}, a+b=M+1. So the tight family is exactly the minimal-hole (most rigid) asymmetric case.
## Literature decision (2026-11-22)
Pham–Sauermann arXiv:2602.15797 (+Bedert–Kravitz small sets, BBKMM |S|>=p^{1-c}) settle all sufficiently large p, but p_0 is never stated; constants (C_alpha ~ 2^{O(1/alpha^2)}, alpha<=c tiny, BK needs log p >= (log C_alpha)^4) make p_0 astronomically large. A finite check down to p_0 is impossible. A uniform argument is the only route to all primes.
## Recursion probe (experiments/irc/restrict_probe.py)
a=1 tight family, exhaustive: deleting the new labels from ANY zigzag at M+2 never leaves a zigzag at M (M=5->7: 0/51, 6->8: 0/56, 7->9: 0/135); same for M+1 (0/19, 0/51, 0/56, 0/135). Insertion-type recursion that keeps the old step order is impossible in this family; any recursion must reorder globally.
