# Pitfalls (given to every referee; each is a permanent regression pattern)

1. **Finite checks are not proofs.** A statement verified for p ≤ N or k ≤ K is `finite_verified` at best. (Seen: CN coefficient correspondence "proved" with finite checks k=5..8.)
2. **Rational vs finite characteristic.** Rank/closure/independence arguments over Q do not transfer to F_p. Any use of rational rank must be re-proved mod p, including for small p. (Seen: March 2026 paper's rational-rank closure.)
3. **Hypothesis-dependent lemmas.** A lemma proved under a gap/size hypothesis must not be applied outside it. (Seen: three-jump lemma failed under its initial gap hypothesis.)
4. **Universal conditions need dense counterexample search.** Conjectured structural conditions must be tested on dense and symmetric sets. (Seen: zigzag Z* refuted by dense symmetric examples.)
5. **Undefined or non-monotone potentials in descent arguments.** A descent/induction must define the potential on every state reached and show strict decrease in every case. (Seen: Atomicium candidate.)
6. **Accumulating avoidance constraints.** Repeated merge/absorb steps consume freedom; a balance identity shows plain merging is inadequate for dense sets. Any induction must show the avoidance set stays smaller than the available freedom at every step.
7. **Quantifier and boundary drift.** Check small primes (p = 2, 3, 5, 7), |A| = 0/1/2, and A containing elements with a − a' = 0 or a + a' = 0 explicitly.
8. **Circularity.** The claim being proved, or a statement equivalent to it for the same parameters, must not appear among its own dependencies.
9. **Rooted/avoid hypotheses accumulate.** Any induction with a rooting or avoidance condition must show the condition re-establishes itself at the next level (balance identity: slack p−k at every level).
10. **Arbitrary-obstacle lemmas are false.** Finishing/grasshopper lemmas that avoid an *arbitrary* forbidden set of comparable size fail (modular grasshopper: only |M| ≤ 0–3 at p=11,13; one-step finishing blocked by k points). Use the walk's own visited-set structure.
11. **Hypothesis thresholds matter.** Three-jump lemma with D > d only is FALSE (jumps 1,6,7; F1={1,13}, F2={7}); D > 2c needed. Re-derive any statistic computed against a wrong hypothesis.
12. **Non-explicit or infeasible thresholds do not finish.** An argument valid only for p > P0 with P0 unspecified leaves primes up to P0 uncovered. An EFFECTIVE P0 plus exhaustive verification would suffice logically, but the thresholds known (≥ ~e^(10^10)) are computationally prohibitive: a practical, not a mathematical, obstruction.
13. **A checker accepting a configuration is not a counterexample** until the configuration is shown reachable (Atomicium C0.3); and a checker rejecting is not a refutation of the theorem (CDFV ℚ-rank).
14. **Dense symmetric sets are the hard case** (Z* refuted by [1..h], h=7,8,10; near-complete sets defeat the shell absorber). Test every general lemma there first.
15. **Fixed-position/forced-prefix patterns fail.** Dilation and position freedom is essential in graceful-permutation constructions (91/228 patterns fail at r=14 with fixed position).
