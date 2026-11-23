# Next round: the tight family is ONE two-hole linear-realization theorem — prove it

AUDIT of your last round (Claude L35):
- Zero-sum reduction: accepted. Pair-insertion lemma (r >= n unused inverse pairs => one insertable): proof checked, accepted.
- Uniform G_{n,d}: accepted. Citation-free bases (pure zigzags, also cover d=4,5, verified d<=150):
  n=d+1: (d,1,d−1,2,...); n=d+2: (d+1,d+2) || zigzag of [1,d] from 1 with its LAST vertex dropped;
  n=d+3: (d+2,1,d+3,d+1) || zigzag of [2,d] from 2 with its SECOND-TO-LAST vertex dropped (kills length 2).
- Literature: Pham–Sauermann (arXiv:2602.15797) + earlier work = Graham for sufficiently large p. Our target is all p.

CORRECTION (important): your normalized two-hole target V(M,H) = {0,M+1} ∪ ([3,M−1]\{H}), start a+1, is exact-SAT
UNSAT for EVERY H when a >= 14 (checked (14,30),(14,31),(15,32),(18,38)). It only works for 6 <= a <= 13. Drop it.

NEW NORMAL FORM (works for ALL a >= 2, uniform). Use the other bridge:
   W = (δ, +M, −rev δ, +a, −M, +b, −(M+1)),  b = M+1−a,  bridge vertices M+a, a, M+1.
Core: D = [−k, M−1−k] \ {1, a}, δ = path from 0 through D. For 0 <= k < M−a: D ∩ (D+M) = ∅ (span M−1), the bridge
vertices avoid D ∪ (M+D), and the span is max(2M−1, M+a+k) <= 2M+2. Shift by k:

   LR(M,a,k): a Hamiltonian path on [0,M−1] \ {k+1, k+a}, STARTING at k, with edge lengths exactly [1,M−1] \ {a, M+1−a}.

Evidence: with k = ⌊(M−a)/2⌋ exact SAT finds LR(M,a,k), and the full walk verifies, for EVERY 2 <= a <= M/2 and EVERY
M = 8..46. Good k form a wide window around (M−a)/2 (e.g. a=20, M=50: k = 6..24), so you may choose k by residue class.
Shape of solutions (largest-length-first): outer Walecki zigzag  k, M−1, 0, M−2, 1, M−3, ...  (lengths M−1−k, M−1, M−2, ...),
then a middle gadget around the two holes k+1, k+a. Note the label kills: the zigzag skips a length at every vertex gap,
so the gaps {k, k+1} (start + hole) and k+a must be arranged to kill exactly a and b = M+1−a, with the length M−1−k of the
first edge accounted for — that is the whole difficulty, and it sits in a window of width ~a around the centre.

TASK: prove LR(M,a,k(M,a)) for all a >= 2 (at least a >= 6), M >= 2a, with an explicit k. Warning: a naive outer peel
LR(M,a,k) -> LR(M+2,a,k+1) does NOT close, because the excluded big length b = M+1−a moves by 2 (the new instance must
use b and b+1 but omit b+2). So either (i) generalise the instance to "outer zigzag with prescribed kill positions"
(lengths killed = vertex gaps of the zigzag; you control where gaps fall) and prove the residual central instance of
width O(a) directly, or (ii) find a recursion in (M,a) jointly. Partial win: any explicit family covering all M for each
fixed a in a uniform way, plus the residual central gadget as a uniform-in-a construction.
Deliver: constructor, proof, stdlib verifier for M <= 400 checking the full signed walk W.

## ADDENDUM (after your LR/global round — accepted: occupancy identity, forbidden-sum path theorem, |B|<=5 absorption,
## M->M+2 single-edge obstruction)
Strong lead for the LR recursion: read the LR path BACKWARDS. Exact SAT: for every 5 <= a <= M/2−2 and M = 14..22,
LR(M,a,k) has a solution whose reverse STARTS with your G-step header (M−2, 0, M−1, 2) [0-indexed; lengths M−2, M−1, M−3],
precisely for k ≡ ⌊M/2⌋+1 (mod 2) (k=(M−a)/2-ish values included). So: define the two-missing-label, two-hole family
   T(n; a, c; ε): path on [0,n−1] minus two holes, lengths [1,n−1]\{a,c}, ENDING at e with holes e+ε and e+εa (ε=±1),
with c = (original b) fixed. The G-step (n−2, 0, n−1) || reflect(T(n−3)) maps T(n;a,c;ε) to T(n−3;a,c;−ε) as long as
c <= n−4. Prove: (i) the b-level gadget for c ∈ {n−3, n−2, n−1}, (ii) bases, (iii) separate bases for a ≈ M/2.
Literature note: 2610.34424 proves |S| >= n_0 (absolute, uncomputed) for ALL finite abelian groups; with Kravitz
(all p, |A| <= log p/loglog p) and |A| <= 20, the all-primes gap is finite but uncomputed. A constructive argument for
bounded |A| and all p is therefore exactly what is missing.
