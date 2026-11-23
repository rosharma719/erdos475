# Next round: small-a tight pairs need offset c <= 2M/3; build the c=1 family explicitly

Verified (Claude): your 3-shape c=M obstruction (A,B,C) and your (24,2) c=1 certificate.
New lemma (Claude, L19): for a tight half-walk with offset c, (2M+3)/3 <= c < M is impossible (counting: in a window
of spread <= 2M+2-c the pairs (x,x+c) are disjoint, so |D| <= c). So offsets are c in [1,(2M+2)/3] or c=M, and your
obstruction kills c=M for floor(M/2) > 2a+7.

c=1 structure: D has M points, no two adjacent, spread <= 2M+1, so v_j = t+2j+E_j with defect E <= 3. With one gap of 3,
D = E ∪ O, E = {0,2,...,2k}, O = {2k+3, 2k+5, ...}. Writing i' = k - i for E-points and j for O-points:
an even label 2t is a move of t inside E or inside O; an odd label 2s+3 is a cross move with i'+j = s (always upward
from E to O). So a c=1 half-walk is a Hamiltonian path on two columns where within-column moves are labelled by
differences, cross moves by SUMS, each label in [2..M] used once, with the triple 0,a,M+1 (prefix allowed).
TASK: give an explicit two-column family (case split by parities of M, a) for all small a (say 2 <= a <= M/4+4),
prove it, and verify it for M <= 400. Combined with c=M (B-shape) for large a, and a=1 (spiral), this would close the
tight family. If c=1 is awkward, any c <= 2M/3 is allowed.
