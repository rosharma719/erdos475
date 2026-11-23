# State of play — Erdős #475 project (2026-11-22, end of session 1)

Legend: **P** published · **C** candidate (proof supplied, audited in-session by Claude with independent code, referee gates NOT yet run) · **F** finite evidence only · **O** open.

## Established (candidates, audited in-session)
| Result | Source | Audit |
|---|---|---|
| One-element reduction: Graham for size k ⇐ zero-sum k-sets (2≤k≤p−3) | GPT, Claude re-proved | hand proof; exhaustive p≤23 (4.3M sets); transfer verified p≤13 |
| NC3-Z: zero-sum 3-complements (⇒ all |A|=p−4) | GPT | hand proof; own code 2,926 triples 11≤p≤61 |
| Zero-sum 4-complements (⇒ all |A|=p−5) | GPT | own code, all zero-sum 4-complements 11≤p≤47; selection lemma partly hand-checked |
| Zipper lemma, quadratic/cyclotomic constructions, double-transversal criterion | GPT | own code (3.1M cases / >190k orderings) |
| Geometric swap theorem, g_k criterion, coset escape (MC for coset-structured sets) | GPT | own code (442 / 285 / 711 cases) |
| Index-two theorem, contraction lemma, merge-chain lift, three-jump (corrected) | ledger | in ledger, not re-audited here |
| Symmetric sets ⇔ folded graceful cycle (exact reduction); SUPERSEDED by: every symmetric A=−A has an explicit valid cycle, all primes (Symmetric IRC walk) | Claude / GPT | hand proof; 65,535 integer sets; all symmetric sets p≤31; 20,000 random to p=997 |
| Minimal zero-sum IRC (sign rule) | GPT | 3,142 collections |

## Evidence only (all clean through p=23–29)
ADJ-ALL (every pair with x+y≠0 adjacent in some valid cycle); BR_3; two-pair with no coincidences; EC and MC (rooted cores); FOLD (every symmetric set has a half-cycle, p≤29); pure lift-induction Q(A)≠∅ (p≤13, p=17 sizes 5..8).

## Negative results (do not retry without a new idea)
Merge-chain/balance identity; arbitrary-obstacle lemmas; one-move local repair of arbitrary cycles; fixed-Walecki coarsening (p=19 C={7,8,10,14,18}); low-index cyclotomic coverage not universal (p=47); single-swap-robust cycles do not always exist; BR_m for m≥4 false; edge subdivision forces M=fold(2e); Z* false; bounded chains from a FIXED cycle fail in dense sets (≈10–25% at density 0.87).

## What the full conjecture still needs
Everything above covers |A| ≥ p−5, p ≤ 37 (verified), sparse sizes ≤ 12/20 (published, CDFV flagged), coset-structured sets, and symmetric sets only in evidence. The dense middle range is open for every p between the verified range and the (infeasible) effective threshold ≳ e^(10^10). The missing idea is a flexibility/induction mechanism for generic dense sets that avoids the balance identity — likely a theorem about the CHOICE of starting cycle (global), not local repair.

## Next steps
1. Run referee gates on the near-complete candidates (≈$1; $8.81 of $20 API budget spent).
2. GPT: quantitative flexibility over cycle choice; coset-core + absorber lemma; stop rule after two empty rounds.
3. Claude: audits, move-set data, FOLD induction attempts, possible finite verification of p=41 using the zero-sum reduction (feasible but hours of CPU, low proof value).
