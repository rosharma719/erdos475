# Local computation data for LSA1 (verified by exhaustive search on this machine; scripts in experiments/exploration/)

Setup: A ⊆ Z_p^* zero-sum. A *valid cycle* is a cyclic order of A whose partial sums S_0=0,S_1,...,S_{k-1} are pairwise distinct (rotation-invariant for zero-sum A). Moves between valid cycles: (R) reverse a contiguous segment, (L) relocate one element. A move is *valid-to-valid* if both ends are valid cycles.

| p | family | #valid cycles | components under (R),(L) valid-to-valid moves | admissible pairs never adjacent in any valid cycle |
|---|---|---|---|---|
| 7 | Z_p^*\{±1} (|A|=4) | 2 | 1 | 0 / 2 |
| 11 | Z_p^*\{±1} (|A|=8) | 274 | 1 | 0 / 6 |
| 13 | Z_p^*\{±1} (|A|=10) | 4332 | 1 | 0 / 8 |
| 11 | ALL 57 zero-sum sets, |A|>=5 | — | all connected | no set lacks a valid cycle |
| 13 | ALL 193 zero-sum sets, |A|>=6 | — | all connected | no set lacks a valid cycle |

Interpretation / candidate conjectures (UNPROVED):
- CONN: for every zero-sum A (|A|>=5) the valid-cycle graph under (R),(L) valid-to-valid moves is connected.
- ADJ (= FP∀ via Lemma 0): for every admissible merge pair (a1,a2) some valid cycle has a1,a2 adjacent.
CONN alone does not give ADJ; it would give a path structure to build ADJ inductively, or a handle on how the set of valid cycles can be explored.

Limits of the data: p<=13 only (enumeration explodes beyond). Ledger-level FP∀ evidence goes to p<=19 (exhaustive) and dense random p<=23. The data does not touch p>=41, which is where an explicit non-asymptotic mechanism is needed.

Code-execution advice: the server sandbox can enumerate valid cycles for p<=13 quickly; for p=17 and above use randomized DFS / constructive families rather than full enumeration.

## Lift-closure experiment (local, exhaustive; experiments/exploration/lift_closure.py)
Q(A) := valid cycles of A obtainable by lifting a Q-cycle of a merged set B'=A∖{a1,a2}∪{a1+a2} (z=a1+a2 ∉ A∪{0}); base: ALL valid cycles for |A|<=4.
Pure lift-induction ("build every cycle only by lifting previously built cycles, over ALL legal pairs") works:
- p=7,11,13: the ONLY zero-sum set with Q(A)=∅ is the full group Z_p^* (it has no legal pair, |A|=p-1 is outside the FP range |A|<=p-2).
- p=13: all 254 zero-sum sets with 5<=|A|<=p-2 have Q(A)≠∅.
- p=17, sizes 5..8 (2158 sets): Q(A)≠∅ always.
- For EVERY legal pair (a1,a2) of every set tested, some Q-cycle of B' lifts (min fraction of legal pairs with a lifted cycle = 1.0).
So the induction hypothesis "A has a lift-derived cycle, for every legal pair" holds at these sizes: a restricted-cycle form of FP∀ that is itself closed under lifting by construction. The open problem is a structural description of Q (or any invariant containing Q's lifting behaviour) that can be proved to persist for all p.

## Local-pattern realizability (local exhaustive, Claude, no API; experiments/exploration/pattern_realizability.py, block_realizability.py, ladder_availability.py)
Cycles = valid cycles of zero-sum A (reversal-closed). "Block t=(x_1..x_m) realised" = t consecutive (cyclically) in some valid cycle. Necessary: every contiguous sub-sum of t nonzero.
- **BR_2 (ADJ-ALL):** every ordered pair (x,y), x+y≠0, is realised — INCLUDING illegal pairs (x+y∈A). Exhaustive: p=11 sizes 5..9 (1540 tuples), p=13 sizes 7..10. The ONLY adjacent-pair failures are inverse pairs (x+y=0): 0 non-inverse failures at p=11,13. Strictly stronger than FP∀ (legal pairs only).
- **BR_3:** every ordered triple with all contiguous sub-sums nonzero is realised: p=11 sizes 5..9 (5140 tuples), p=13 sizes 7..10 (28,296 tuples): 0 failures.
- **BR_m, m>=4 is FALSE** in general (needs complement-aware conditions): p=11 m=4: 880/11040 admissible tuples unrealised (k=6,7,8); p=13 m=4: 3096/106080 (k=7..10; still 72/15552 at k=10=p−3). Small example: A={1,2,3,4,5,7}, t=(1,3,2,4) mod 11: remaining {5,7} cannot complete (partial sums collide).
- **Two disjoint pairs (zipper shape):** p=13 sizes 7..10: 360 failures of 80,160; EVERY failure has a block-sum coincidence (s_i ∈ rest, s1=s2 or s1+s2=0); no unexplained failure. p=11: 60 unexplained, all at k=6 (tiny contracted set).
- **Top-down contraction ladder** (cycle of A⁺=A∖{z}∪{a,b} with (a,b) and (x,y) adjacent contracts to a cycle of A with (x,y) adjacent, no free-point condition): one ladder step is available (a split z=a+b with a,b∉A, no coincidence) for only ~0% (c=2), 5–15% (c=3..8) and up to ~90% (c≈p/2) of random dense (A,{x,y}) at p=17..41. So a single ladder step does NOT reach the dense regime; it helps only when the complement is rich.

Conjecture ADJ-ALL (BR_2) and BR_3 are candidate local-flexibility statements; the induction obstruction is that closing BR_2 under merging needs BR_2+ (two simultaneous adjacencies), which needs BR_3+... with coincidence conditions that are exactly the dense-set difficulty.
