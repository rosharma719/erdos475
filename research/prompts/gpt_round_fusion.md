# Next round: Strong Fusion — the single lemma that implies Graham for all p

AUDIT (Claude L37): ACCEPTED — four-block fusion theorem (Hall argument re-derived), two-triple corollary (independent
check 2156/2156, p<=23), maximal-atom switching lemma, the mod-19 examples. Integer-version remark correct.
Also accepted from the previous round: LR occupancy identity, forbidden-sum path theorem, |B|<=5 absorption.
Literature: 2610.34424 gives an absolute (uncomputed) n_0 for |S| >= n_0 in all finite abelian groups; with Kravitz and
|A| <= 20, the all-primes gap is finite but uncomputed. A size-free constructive argument is what is missing.

THE TARGET. Your fusion word, made induction-ready:
  SF: every zero-sum A ⊆ F_p^× that is not a minimal atom contains a minimal atom B, with Z = A\B, such that for EVERY
      valid cycle z of Z there are a rotation/reversal z' of z and an order (b1..bm) of B with
          (b1, z'1, b2, ..., bm, z'2, ..., z'n)  valid.
SF ⇒ Graham for every prime (induction on |A| + zero-sum reduction). Exhaustive evidence: 0 failures for p=11 (all sets),
p=13 (|A|<=8), p=17 (|A|<=7) — 1615 sets (experiments/audits/fusion/strong_fusion.py).
By your exact criterion (section 3 of your note), with c := z'1 and V_B the vertex set of the B-cycle (b1..bm):
   need (z'1 + V_B) ∩ V_Z' = {z'1}   and   b1 ∉ (z'1 + V_B) ∪ V_Z'.
So SF asks: for any valid Z-cycle (vertex set V, |V| = n), choose a B-atom and a "port" (a vertex of the Z-cycle after
rotation, i.e. any of the 2n choices) and a B-order so that the translated B-cycle meets V only at the port.
WORK PLAN:
(1) Counting version: |V| = n, B-cycle has m vertices; the number of (port, B-order) choices is 2n·(m−1)!·m (or fewer up to
    symmetry). Bound the number of bad choices using the fact that a collision z'1 + v_B = v_Z is a linear condition, and
    show bad < total when p is not too small relative to n·m — exploit freedom in choosing WHICH atom B (maximal atom
    partition + switching lemma).
(2) Find the precise regime where (1) fails (dense: n·m ≳ p) and handle it with a different port structure, e.g. insert
    B as two blocks at two ports (your 4-block word is one port; a 6-block word has two).
(3) Report any counterexample to SF found by search (p <= 19) — that would be equally valuable.
Deliver: proofs, stdlib verifier, explicit UNPROVED list.

## ADDENDUM (Claude L38) — sharper target: the MAX-ATOM rule
Edge form: rotate the Z-cycle so an edge u→u' (step w) comes first; the word inserts B as (b1, w, b2, ..., bm), new vertices
u+b1, u'+σ_1, ..., u'+σ_{m−1}. Valid iff they avoid V_Z and w ≠ −(b2+…+bj). (Cycle reversal = vertex set −V_Z.)
Proved counting lemma: bad (edge,order) pairs <= m!(m·r* + m − 1), r* = max_{t≠0}|V∩(V−t)|; so n > m·r* + m − 1 suffices.
EXHAUSTIVE: choosing B = a MAXIMUM-size atom (with A\B zero-sum) fuses with EVERY valid cycle of A\B in all 5264 zero-sum
sets tested (p=11, 13 all sizes incl. F_13^×; p=17 |A|<=8; p=19 |A|<=7). "Any atom" fails, always via inverse pairs
(and triples in the densest p=13 case). So prove SF-max. Hints: large m gives m! orders against the counting bound's
m·r*; use the switching lemma (in a max partition every exchange is atom-to-atom) and the minimality of B to bound how
many of the m partial-sum translates u'+σ_j can be forced into V simultaneously. Find the dense-regime mechanism
(|A| close to p) — the counting lemma does not reach it, yet SF-max still holds there (e.g. A = F_13^×).

## ADDENDUM 2 (after your near-balanced round — ACCEPTED: Thm 1 local swaps, Thm 2 Φ-extremal [u,v] bound, Thm 3, trap)
Your remaining gap ("atoms of very different sizes" + ">=3 atoms") is exactly SF-max above. Concretely, next:
(a) Two-atom SF-max: A = B ⊔ C atoms, |C| = u <= v = |B|, Φ-extremal so all mixed zero subsets have size in [u,v].
    Show: for EVERY cyclic order of C there is a port and a B-order making (b1,c1,b2..bv,c2..cu) valid. Your Thm-1
    boundary swaps act inside the B-block and never disturb the C-order — try a descent on zero mixed windows of
    lengths in [u,v] using swaps inside B only.
(b) Multi-atom: induct with SF-max — Z = A \ B (B a largest atom) has a valid cycle by induction; insert B into it.
    The difficulty is that Z's cycle is arbitrary; the descent must use only B-internal swaps and the port choice.

## ADDENDUM 3 — SF and SF-max are REFUTED (your p=19 counterexample verified independently; Claude L40)
Verified: A=F_19^×, B={1,18}, your Z-cycle; all 64 four-block words and all 9792 order-preserving insertions fail; own
random search obstructs all 26 atom classes. Difference-isolated pair lemma: accepted.
Data (own sampling, A=F_p^×): the fraction of random valid complementary cycles that DO admit four-block fusion is
~0.5 for pairs, rising to ~0.97 for the largest atoms (p=19). So the cycle must be BUILT, not given.
NEXT TARGET — a cycle-selection invariant. Find a property P of valid cycles such that
  (i) every minimal atom (any order) or a suitable order of it has P;
  (ii) if z is a valid Z-cycle with P and B is a suitable atom of A\Z... [i.e. A = Z ⊔ B], then some fusion of B into z
       is valid AND the fused cycle again has P.
Candidates to test (search for the weakest P that survives (ii) exhaustively for p <= 19, full sets included):
  - P_avoid(k): for every forbidden set F of size <= k (0 ∉ F) there is a port at which... (absorbs any atom of size <= k)
  - P_spread: max_{t≠0}|V∩(V+t)| small (then the proved counting lemma gives insertion; does insertion keep it small?)
  - P_many-ports: at least f(n) edges each admitting insertion of every remaining atom.
Report the best P with its exhaustive status; a P that works for all p <= 19 is the new induction candidate.
