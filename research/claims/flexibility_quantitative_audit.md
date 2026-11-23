# GPT quantitative flexibility note (bounded-swap theorem false; counting/probability/relocation theorems) — AUDITED IN-SESSION by Claude (own code)
Audit script: experiments/audits/gpt_flex_note_independent.py.
VERIFIED
- (1) Counterexample B={±1,±2,±3}, z=1, a=(1,3,−2,−3,−1,2), vertices (0,1,4,2,−1,−2): valid for every prime 13≤p≤101; no valid single adjacent swap and no valid simultaneous batch of ≤3 disjoint swaps; the occupied external vertex 4 cannot be removed. (Confirms: repair of an arbitrary cycle fails even for k=6, any large p.)
- (2) Deterministic bound (#valid single swaps ≥ max{0,k−2−2Z_2−Z_{≥3}}): 0 violations over 272,700 rooted cycles (p=11 k=4..8; p=13 k=4..8). (Z_{≥3} read as the number of zero-sum subsets of size 3..k−1.)
- (3) Probability bound (uniform valid rooted cycles, first step fixed, sets varying): exact fractions exceed the bound at every (p,k) tested: k=4: p=23 0.935 vs 0.571 (and 0.714 sharper), p=47 0.9745 vs 0.903, p=61 0.9812 vs 0.933; k=5: p=37 0.868 vs 0.417 (0.5 sharper). Bound is vacuous when p≤~k²+k²; no violations.
- (4) Unique-difference relocation theorem: 9,852 relocations with m_V(a_i)=1 tested (p=11,13), 0 invalid; counting bound k−2−⌊E_+/2⌋ held in all 272k cycles.
- (5) Relocation counterexample (6,−4,−10,−6,10,4) avoiding external residue 2: no single-step relocation preserving the first step yields a valid cycle avoiding 2, for every prime 29≤p≤101.
- Hole-transport examples: 2-swap (1,−2,3,2,−4)→(1,3,−2,−4,2) removes −1; 3-swap (1,3,2,4,5,−4,−11)→(1,2,3,5,4,−11,−4) removes 10 and every proper sub-batch fails: verified for all primes 17≤p≤199.
NOT audited: the exact dependency-path 'iff' characterization and the exhaustive outcome tables (p=13,k=6 and p=17,k=7); the sharpened k²−5k+6 proof.

# p ≥ 41 ADVERSARIAL TESTS of EC/MC (Claude; experiments/p41/cyc_avoid.cpp + run_tests.py) — responding to METHOD_REVIEW item 1
Randomized exhaustive-capable C++ search for a rooted valid cycle (first step z) avoiding a forbidden vertex r, restarts with node caps 2e4..2e7; 'none' means the full search space was exhausted. Families: symmetric, coset unions, near-complete (zero-sum complements of size 6..10), symmetric + zero-sum triple, dense random zero-sum. Per set: 2 roots; 6 external r (EC) and 6 internal r (MC).
Positive controls (all passed at every prime): C1 every set has a rooted cycle with no forbidden vertex; C2 forbidding the first-step vertex reports 'none'; C3 the exceptional 4-set {z,−z,z/2,−z/2} reports 'none' when forbidding z/2 (exhaustive).
Results: p=41 (40 sets/family, 5,554 queries), 43 (4,170), 47 (4,182), 53 (3,472), 59 (2,734), 61 (2,796): total 22,908 queries; EC: 0 failures; MC for |B|≥5: 0 failures; undetermined 0. The only 'none' answers are the |B|=4 exceptional family {±11,±24} at p=59 (r=z/2), exactly the known exception.
Caveat: sampled (not exhaustive) sets and queries; random-restart DFS can only certify 'found'; 'none' is exhaustive.
