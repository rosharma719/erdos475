# Next round: extend the H_k method to the whole tight family

AUDIT: your H_k proof is ACCEPTED (Claude, claims/claude_lane.md L23). I re-derived all four header edge/vertex sets and
the H_k assembly by hand, and an independent implementation verifies F,T,C,D for s<=1499, H_k for k<=3000, and the
end-to-end tight cycles (M=4k+2, a=2) for k<=400. So: a=1 all M (spiral), a=2 all M ≡ 2 (mod 4).

The method (forced ladder -> generalised Hamiltonian-path states closed under zigzag-plus-detour recursions, finite
seeds) is the right tool. Apply it to the rest of the tight family P=[1,M], N=[1,M+1]\{a,b}, a+b=M+1.

Data (exact SAT, complete; experiments/irc/hw_scan.out): EVERY tight pair with M<=36 has one of:
 (j) junction half-walk, offset c=a: delta = ordering of [1..M]\{a} with first step +b, D ∩ (D+a) = ∅,
     spread <= 2M+2-a; merge the final (-b,-a). Admissible iff a | M, M+1, M+2 or M+3.
 (i_M) internal jump 0,a,M+1 with offset c=M (fails when floor(M/2) > 2a+7).
 (i_1) internal jump with offset c=1 (used for a near M/2, and e.g. (M,a)=(36,5) where (j),(i_M) are excluded).

TASKS, in order:
 1. a=2, M ≡ 0 (mod 4) and M odd: via (j) with c=2 (D has no two points at distance 2) or a non-aligned c=1 form;
    find the forced structure and the generalised states; prove for all M.
 2. a=3,4: via (j) (always admissible). Same method.
 3. General a: a uniform scheme (which of j / i_M / i_1 / other offset, by residue), each proved by the same
    state-recursion technique.
Deliver proofs + stdlib verifier (M<=400). Every closed class goes straight into the ledger after audit.
