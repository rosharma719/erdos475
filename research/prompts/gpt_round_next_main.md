# Next round — back to the critical path (F(α,β) in general is NOT needed)

Audit of your F round (Claude): both extremal rays verified by independent code (a, b < 2000, 0 failures); the cone
condition beta <= 3alpha+2, alpha <= 3beta-4 matches exhaustive search for alpha+beta <= 15 (no solvable instance
outside it); the ten-band P-recursion header audit is the same pattern as H_k and reads correctly (not re-run in full).
Good work — but note: only the DIAGONAL F(k+1,k+1) = H_k is used by the conjecture (a=2, M ≡ 2 mod 4). General F(α,β)
was Claude's exploratory reduction and is off the critical path. Please stop extending the F table.

The conjecture now needs exactly three things. Work on 1 first; 2 and 3 in parallel if you have capacity.

1. TIGHT FAMILY, remaining cases (prompts/gpt_round_extend_hk.md). Proved: a=1 all M; a=2, M ≡ 2 (mod 4).
   Exact SAT finds a construction for every tight pair with M <= 36:
     junction c=a (delta = ordering of [1..M]\{a}, first step +b, D ∩ (D+a)=∅, spread <= 2M+2-a, merge the final -b,-a),
     admissible iff a | M, M+1, M+2 or M+3 (always for a <= 4);
     internal c=M (B-shape; impossible if floor(M/2) > 2a+7);
     internal c=1 (needed e.g. at (36,5) and near a = M/2).
   Use your state-recursion technique (forced ladder -> finitely many generalised states closed under
   zigzag+detour -> seeds). Priority: a=2 with M ≡ 0 (mod 4) and M odd; then a=3,4 via the junction; then general a.

2. GENERAL SETS, middle densities (Claude L27–L28). AVOID reduction: with C = P∩N (best dilation) and its explicit
   symmetric core walk W_C, insert one remainder step x1 before the final −c and the rest after the walk; valid iff the
   remainder ordering's partial sums avoid the core vertex set V_C (lower cluster D ⊂ [0,b2] and b1+D), plus one extra
   point. Exact tests p=53: 12/12 at α=0.5, 0.65, 0.8. This step preserves the occupancy (|R|+|F|)/p exactly, so an
   induction GO(θ) on |R| needs only (a) a placement lemma (the core walk of R can be chosen — dilation, pivot,
   rotation — to avoid the obstacle set F) and (b) an empty-core base case. Prove (a) for occupancy θ <= 1/2.

3. GENERAL SETS, near-complete (α > 0.85): free insertion of the remainder into the fixed core walk (SPL) worked 10/10
   at α=0.9 where AVOID fails 5/12. Find the distributed insertion rule.
Deliver proofs + stdlib verifiers; mark every unproved step UNPROVED.

ADDENDUM for item 1 (a=2, all M) — Claude L31: use the JUNCTION with c=2 on the explicit two-phase pair shape
   D = {4i,4i+1 : i<L} ∪ {4L+2+4j, 4L+3+4j : j<U} (+ one singleton at an end if M is odd),
translated so the start st has st+(M-1) ∈ D; labels [1..M]\{2}, first step +(M-1), merge the final (-(M-1),-2).
Exact SAT finds such paths for every M = 10..40 with L ∈ {1,2,3}. Labels ≡ 2 (mod 4) can only cross the phase shift,
which should force a ladder exactly as in your aligned c=1 theorem. Do the forced-structure analysis and the
state recursion; that proves a=2 for every M.

ADDENDUM 2 (Claude L32): a=3 junction (c=3) works on the explicit shape
   {6j,6j+1,6j+2 : j<m} , gap 5 , then an alternating run of t=M-3m points (step 2),
for every M=12..30 (m ∈ {2,3,4}). The step-2 run is a single column, as in your aligned c=1 ladder — do the forced-ladder
analysis on it. a=4: solutions use the period-8 tiles "xxxx...." and {0,2,3,5} mod 8; find the shape.
