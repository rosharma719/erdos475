# c=5 diagnostics, marked-edge matching, geometric swap theorem, coset escape (GPT 2026-11-22) — AUDITED IN-SESSION by Claude (own code)

Source note: GPT 'erdos475_c5_to_cycle_flexibility.md' (c5_classify.cpp, c5_target_independent.py, coset_escape_verify.py not used for the audit).
Audit script: experiments/audits/c5_and_coset_independent.py (parts a-f); exploration: experiments/exploration/move_chain_rates.py.

VERIFIED (own implementation)
- (a) Zero-sum 5-set counts Z_5(p)=(C(p−1,5)−(p−1))/p and Burnside orbit counts: exact match p=11..31 (e.g. p=31: 4596 sets, 154 orbits); p=47 formula gives 634 orbits.
- (b) Walecki consecutive-pair sums ⊆ {±1, 2, r−1, r+1} (p=19..47); a block of 4j+1 consecutive steps in one half sums to its middle step (j=1,2); number of valid 5-vertex deletions = 15p−63 for p=19,23,29,31,37,41,43,47 (exact match); max isolated deleted vertices over valid 5-deletions at p=29 is 3 (≤4 as claimed). The formula is still unproved for all p.
- (c) Geometric swap theorem (all non-root adjacent swaps of the geometric cycle on zH valid iff h²−h+1∉H): 442 (p,h) cases, 0 violations (p≤61, orders 3..p−1).
- (d) g_k=gcd of coefficients of ((x²−x+1)^k−1) mod Φ_k: {5:5,6:1,7:14,8:24,9:9,10:11,11:11,12:39,13:39,14:4,15:2,16:136} exact match; criterion 'some generator h of the order-k subgroup has h²−h+1∉H ⇔ p∤g_k': 285 (k,p) cases for p≤700, 0 violations.
- (e) Coset-escape theorem: 711 randomly generated (p,H,t,U) instances satisfying the hypotheses (v_i in distinct cosets, w_i∉W): every vertex except 0 and the first-step vertex is removed by some valid non-root adjacent swap; 0 violations.
- (f) p=47: the fixed Walecki cycle alone covers 220 of 634 zero-sum 5-set orbits (matches GPT's Walecki column); GPT's combined 283/634 for Walecki+geometric+index-2 was not re-run.
HAND-CHECKED: the swap algebra behind coset escape (w_i = X+P_i+u_{i+1}, boundary w_{t−1}=h^{-1}(X+P_{t−1})+u_0; W is H-invariant so w_i∉W ⇒ new vertex ∉V); the minimal-zero-sum theorem (every ordering valid ⇒ one adjacent swap removes any internal vertex). Minimal-zero-sum and the p=41 index-5 certificates were not run computationally.
CONCLUSIONS: the theorems are correct; they cover coset-structured sets (size Θ(p) possible) and tiny families, not general sets. The c=5 fixed-family programme is limited (cyclotomic coverage depends on the divisors of p−1; refuted as universal at p=47).

MOVE-CHAIN QUANTIFICATION (Claude, random zero-sum sets, random valid rooted cycles, every internal vertex as target; success = a single adjacent swap, or a hole-transport chain of ≤3 simultaneous non-consecutive swaps, removes it):
 p=23: density 0.22: 83% / 89%; 0.35: 68% / 81%; 0.48: 46% / 72%; 0.61: 37% / 61%; 0.74: 21% / 43%; 0.87: 11% / 24%.
 p=31: density 0.16: 84% / 89%; 0.35: 63% / 85%; 0.48: 50% / 78%; 0.61: 38% / 67%; 0.74: 22% / 48%; 0.87: 10% / 25%.
 (single swap / chain≤3.) From a FIXED cycle, bounded chains fail for most targets once density exceeds ~0.7; MC therefore needs flexibility in the CHOICE of starting cycle (geometric/coset cycles are robust: every swap valid), not only local repair of a given cycle.

## Swap-robust cycles are NOT always available (Claude, exhaustive, experiments/exploration/swap_robust.py)
Question: for every zero-sum B and root z, is there a valid rooted cycle all of whose internal vertices can each be removed by one valid non-root adjacent swap (as on geometric cycles)?
Answer: no. Fraction of (B,z) with such a cycle: p=11: k=5 64%, k=6 100%, k=7 100%, k=8 75%; p=13: k=5 68%, k=6 100%, k=7 100%, k=8 77%, k=9 33%. (MC still held in all these cases via longer chains / other cycles.) So single-swap robustness is the wrong invariant for dense sets; a proof of MC must use multi-move or cycle-selection arguments there.
