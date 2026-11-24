# Audit: modular block repair, short-window trap, torsion-aware certificates (Claude, 2026-11-24)
The submission was pasted in chat. Script: `experiments/audits/modular_repair/` (needs SymPy). The rerun passes every assertion.

## Verified / accepted
- **Theorems 1–3 (dissociated block repair as Boolean-lattice chain avoidance): ACCEPTED.**
  - Thm 1: the r rotation chains of a circular order have internally disjoint prefix sets, because a proper cyclic interval has a unique start.
  - Thm 2: the only minimum obstructions are the singleton layer and the complement layer.
  - Thm 3: union bound, m ≥ ⌈(uv − w)/2⌉.
- **Minimal-counterexample conditions I–III: ACCEPTED.**
  - |𝓕| ≤ n − r − 1, since A′ has n − r + 1 vertices and the two endpoints of the contracted step are excluded.
  - **Scope:** a dissociated set in F_p has 2^r distinct subset sums, so **r ≤ log₂ p**. These conditions therefore constrain only blocks of logarithmic size. For dense counterexamples (n ≫ log p), condition I (n ≥ 2r + 1) is automatic and conditions II–III are weak.
- **Short-window trap (p = 23, n = 19): VERIFIED.** All 16,568 block permutations of length 2–6 fail; the 7-block replacement works.
- **Rational-rank certificate flaw (det C = −29, denominator 29, p = 29): VERIFIED.**
  - **Already known in this project.** `ledger.md` (2026-11-22, "Q-rank closure is unsound in groups with torsion") gives a det −17 example at k = 9, plus further examples. The deposited treeSearch.py was audited too (unconditional length cap, skipped known blocks, missing total-sum relation, floating-point rank).
  - The new example is a second, independent instance. The conclusion is unchanged: CDFV Thms 1.4–1.5 are not established by the deposited search; no counterexample is known.
- **Torsion-aware certificate (p | m_u, the integer multiplier of u in the ℤ-row lattice) and the rank-increasing symbolic search: ACCEPTED as sound in outline.**
  - n = 2..6 reproduced: 1, 1, 6, 30 and 763 nodes, no surviving primes.
  - This is the same strategy as the GPT round-4 size-5/6 verifier and the CN round's per-k certificates, now implemented exactly.
  - Node counts grow fast (×25 from n = 5 to 6). Reaching CDFV's claimed range (|A| ≤ 20) this way is untested and likely infeasible without heavy pruning.

## Assessment
- The pivot back to the modular problem gives correct, useful tools for **fixed small sizes** and for **auditing the small-set literature**.
- It does not touch the dense regime: dissociated repair is logarithmic, and symbolic branching is exponential in n.
- **The most concrete achievable deliverable on this line:** a sound, torsion-aware re-verification of CDFV's small-set claims. This would settle whether their published bounds stand.
