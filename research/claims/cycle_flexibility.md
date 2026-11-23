# Cycle flexibility: external-core conjecture (EC), minimal-core conjecture (MC), hole transport (GPT 2026-11-22; AUDITED IN-SESSION by Claude)

Setup: B zero-sum, z∈B, rooted valid cycles C(B,z) (first step z), K(B,z)=∩V(C) over them (V includes 0).
- **EC:** K(B,z) ⊆ B∪{0}  (every residue outside B∪{0} is avoidable by a rooted valid cycle). Implies the admissible-split free-point statement (FP∀) immediately. Unrestricted one-point avoidance is false.
- **MC (stronger, |B|≥5):** K(B,z) = {0,z}: ANY residue r∉{0,z}, even r∈B, is avoidable.
- **Proved in the note:** EC for k=2..5 (all primes), K(B,z)={0,z} for generic k=5; k=4 exceptional family B={z,−z,a,−a} with a=±z/2 has K={0,z,z/2}; rotation-boundary theorem (N_a(r)=#runs of V along 0,r,2r,.. ≥1); hole-transport lemma (disjoint nonconsecutive adjacent swaps chaining T_{i_j}=s_{i_{j+1}} ending in a hole move one vertex); inverse-pair segment insertion lemma (valid iff translated vertices avoid retained vertices). Precise GAPS stated: chains can terminate/repeat/need consecutive swaps; swap/reversal/relocation graph not always connected; existence of suitable block for segment insertion open.
- **Equivalent form (Claude):** MC(B,z,r) ⇔ some valid cycle C of B has a z-edge v→v+z with v+r∉V(C) (the z-edge must start at an 'exit' vertex of the r-translation). Rotation boundary guarantees exits exist; the difficulty is making the z-edge start at one.

## Claude audit (no API; experiments/audits/cycle_flex_independent.py)
Own DFS: for every zero-sum B (k>=3), root z∈B, residue r∉{0,z}, search for a rooted valid cycle avoiding r.
- p=11 sizes 3..10: EC checks 2010 fail 0; MC (k>=5, incl. r∈B) 3150 checks, 0 failures.
- p=13 sizes 3..11: EC 10,272, MC 18,348: 0 failures. Exceptions to K={0,z} (brute-force cores) occur ONLY at k=4 (p=11: 10 (B,z); p=13: 12; p=17: 16), none at 5<=k<=7.
- p=17 sizes 4..15 (200 random zero-sum sets per size, all roots, all r): EC 95,840, MC 195,360: 0 failures, 0 undetermined.
- Hole-transport example (p=11): (1,9,3,2,7)→(1,3,9,7,2) both valid, vertex sets {0,1,10,2,4}→{0,1,4,2,9} as claimed.
- Hand-checked: rotation-boundary theorem, hole-transport algebra (adjacent swap changes only s_i), k=4 inverse-pair rooted cycles.
- p=19 sizes 5..17 (60 random sets/size): EC 45,678 checks, MC 110,058: 0 failures. p=23 sizes 8..21 (12 sets/size): EC 15,248, MC 45,444: 0 failures. 0 undetermined.
Conclusion: EC and MC are strongly supported through p=17; no proof for general k.
