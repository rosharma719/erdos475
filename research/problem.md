# Erdős #475 — Graham's rearrangement conjecture

(Source: research/ledger.md, Problem and goal. Statement is now taken from the ledger.)

For every prime p, every nonempty A ⊆ Z_p \ {0} has an ordering a_1..a_k whose partial sums
a_1, a_1+a_2, ..., a_1+...+a_k are pairwise distinct (a *valid ordering*). Partial sums need NOT be nonzero
(the last may be 0 for zero-sum A). The stronger "sequencing" (distinct, nonzero except possibly last) implies it.

## What "solved" means
A proof for ALL primes p: either uniform, or an explicit threshold plus finite verification below it.
Large p is settled non-effectively (Pham–Sauermann et al.; threshold >= ~e^(10^10) by the ledger's rough estimate,
so computation cannot close the gap). Exhaustively verified: all primes <= 37. Hence any threshold-based argument
needs an EXPLICIT, non-asymptotic mechanism (ledger: "Dense flexibility lemma" round).

## Notation
k = |A|; complement size c = |Z_p^* \ A| = p-1-k. c = 3 <=> |A| = p-4 (contract NC3C; published covers c <= 2).
Symmetries: scaling by g in Z_p^x; cyclic rotation for zero-sum A.
