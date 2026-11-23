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

## Update after your last round (audited)
Your even-M map is a correct cycle cover with exact labels, but it is a single cycle for only 13 of 299 even M<=600 (M=4,8,10,20,28,32,34,64,80,158,206,332,350).
So arithmetic maps alone give Artin-type conditional results. The next round must do ONE of:
 (1) Cycle JOINING: a label-preserving move on covers (change several sources' targets simultaneously so each label is used once) that merges two cycles; prove the cycle count can always be driven to 1, e.g. via a connected "switch graph" argument.
 (2) A RECURSIVE construction: from a zigzag for (M,a) build one for (M',a') with M' ~ 2M or M+k, by inserting a block of steps with a proved collision-free embedding (NOT the single-edge lift, which you showed impossible).
 (3) Show the cover family has a free parameter (several (u,v) holes / offset choices) and prove some member is single-cycle for every M without Artin-type input.
Data: research/data/zasym_witnesses.md (tight M<=14, holes (u,v)); many zigzags per (M,a) exist: for a=1, M=3..9 there are 5,8,14,19,51,56,135.
