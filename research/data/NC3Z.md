# Data for NC3Z (ledger + local)
Ledger (band data, int/lemZ*.c, r=16–26; evidence only): F1 embeds for a/r≈0.4–0.8; F2 for ≈0.15–0.5; F3 for ≈0.15–0.5; F4 for ≈0.45–0.85; union ≈ [0.15r,0.85r]; small/large parameters fail in all four families (possibly search artefacts at r>=25).
Parameter is ≈ |y/(2x)| mod p for the chosen special element x (r ≡ −1/2). A choice x is bad only if y/x is a small residue (parameter near 0 or r).
Zero-sum reduction (ledger, proved, unaudited): dilate so xν=±r; contract the 4-window (δ_{r−2},δ_{r−1},r,−δ_{r−1}) positions {1,3,4} or (−δ_1,−r,δ_1,δ_2) positions {1,2,4}; zero-sum holds automatically mod p and forces δ_2−δ_1 ∈ {r,−r−1}.
Coverage data (ledger, random graceful permutations): c=3 zero-sum classes p=23: 3/3, p=29: 4/4 (exhaustive), p=31: 5/5 (sampling).
Local: experiments/exploration/inverse_pair_check.py verified the inverse-pair block deletion end-to-end at p=19,23,29.
