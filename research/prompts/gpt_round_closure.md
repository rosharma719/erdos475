# Round: close Asymmetric Zigzag (or find the exact obstruction)

Context you already have: symmetric interval classification (doubling), skewed-tight hole bound, no single-edge lift for M>=10.
Our exact SAT decider finds a zigzag for EVERY asymmetric pair tested: tight family M<=14 (48/48), two-omission h<=16 (all), merge h<=15 (all). No counterexample exists in any family. Failures occur only for symmetric sets (P=N), and all small ones are explained by your doubling theorem.

Stop proving things about rigid/local structures. Do ONE of these, in order of preference, and report which:

A. UNIFORM CONSTRUCTION via the doubling cycle for general P != N with equal sum.
   Idea to test: for P=[1,M], N=[1,M+1]\{a,b}, a+b=M+1, a symmetric zigzag of [1,M] need not exist (2M+1 not prime / 2 not primitive).
   So do not contract the symmetric cycle. Instead use the forced-map technique on the ASYMMETRIC pair directly:
   the energy identity gives defect Delta; classify, for each (M,a), the successor permutations with total defect exactly Delta
   that are single cycles, find the family of (u,v) hole positions actually realised (we found holes hug the far ends:
   u,v >= M - sqrt(4M-2) for a=1), and PROVE existence of one cycle for all M by giving an explicit permutation
   (e.g. doubling map composed with a fixed bounded modification near the holes), with cycle-count control via a
   multiplicative-order or Jacobsthal-type argument. A proof valid only for large M is acceptable: we close small M by SAT.

B. REDUCTION: prove arbitrary balanced pair -> tight pair (GAP-2) by a monotone operation (merge two steps, split a step)
   that preserves zigzag existence. State exact lemma and which of our found zigzags it is consistent with.

C. If you believe a counterexample exists, name the family and the first M, with a derivation, so we can SAT-check it.

Deliverable: complete argument + standalone stdlib verifier. Mark every unproved step UNPROVED. No literature restatement.
We will supply: SAT witnesses for tight M=3..14 (research/data/zasym_witnesses.md, being generated), list of failing symmetric sets.
