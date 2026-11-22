# Polynomial conjecture CN

Status: see proof_graph.yaml node `CN`.

Exploratory. Reopen only with a genuinely new algebraic idea. The non-zero-sum coefficient correspondence is flagged: proof cites finite checks k=5..8.

_Import the exact statement, hypotheses, proof and source from the ledger. Keep what was proved separate from what was only checked for finitely many cases._

## General derivation of the non-zero-sum correspondence (submitted for audit; replaces finite checks k=5..8)
Write V(y) = Σ_σ sgn(σ)·y^{σ(δ)}. Then
y^{(m−1)𝟙 − e_d} = Σ_σ sgn(σ)·[y^{(m−1)𝟙 − e_d − σ(δ)}] I.
Since (m−1)𝟙 − σ(δ) = (σw₀)(δ), where w₀ reverses the exponent vector, this equals
sgn(w₀)·Σ_τ sgn(τ)·[y^{τ(δ) − e_d}] I = sgn(w₀)·c_k(d), for every k.
The k = 5–8 computations are confirmation, not the proof. Status: `candidate` until the referee pass accepts
(check that δ, m, I and the coefficient-extraction notation match the ledger's definitions).


---
## From ledger: CN round (theorems proved by Claude, unaudited; CN itself OPEN, parked)

### CN round, executed by Claude (GPT unavailable): theorems, proofs, gaps

Notation: m = k − 1, I\_m(y) = ∏*{1≤i≤j≤m, 2≤j−i+1≤m−1} (y\_i + ⋯ + y\_j), V(y) = ∏*{i\<j}(y\_j − y\_i), and Alt(y\_d · I\_m) = c\_k(d) · V.

**Theorem 1 (CN reduction).** If c\_k ≢ 0 mod p, then every A ⊆ ℤ\_p∖{0} with |A| = k has a valid ordering.

*Proof.* There are two cases.

1. *ΣA = 0.* Apply CN to V(x)·∏(sums of the cyclic intervals avoiding position k − 1, of length 2 to k − 2). Use the domains {α} for x₀, A∖{β} for x\_b, and A for the rest. The relevant coefficients are f\_k(b) = (factor whose primes are all ≤ k) · c\_k(b). A nonzero value forces a permutation of A with every cyclic interval nonzero.
2. *ΣA ≠ 0.* Pick a₁ ≠ ΣA and set B = A∖{a₁}. Apply CN to V(y)·I\_m(y) with the domain B∖{β} for y\_d and B for the rest. Its deficit-1 coefficients are sgn(w₀)·c\_k(d) by the general identity in the non-zero-sum reduction above; the k = 5–8 exact checks are confirmation only. A nonzero value gives an ordering of B with no zero block, since singletons and the full block are automatic. Then (a₁, ordering of B) is valid. ∎

**Theorem 2 (structure of c\_k).** In each item the degrees match exactly: deg(y\_d · I\_m) = C(m, 2).

- (i) c\_k does not depend on the choice of representative for each complementary pair. The changes are multiples of e₁, and Alt(e₁H) = e₁Alt(H) = 0 when deg H < C(m, 2).
- (ii) Σ\_d c\_k(d) = 0, because Alt(e₁ · I\_m) = e₁ · Alt(I\_m) = 0.
- (iii) c\_k(m + 1 − d) = (−1)^{C(m,2)} c\_k(d). Reversal fixes I\_m and has sign (−1)^{C(m,2)}. So c\_k is symmetric for k ≡ 1, 2 mod 4 and antisymmetric for k ≡ 3, 0 mod 4.
- (iv) *Evaluation identity.* For every m-set Y in any field, Σ\_{orderings π of Y} sgn(π) · π(d) · I\_m(π) = c\_k(d) · V(Y). Hence every choice of evaluation domain carries the same information.
- (v) The Schubert coordinates ∂*{w₀s\_i} I\_m are the partial sums Σ*{d≤i} c\_k(d) (Monk's rule). They were checked exactly for k = 4–8.

**Theorem 3 (computation).** For k = 5–13, gcd(c\_k) = 1, 2, 4, 6, 12, 6, 1, 4, 8. So CN\_k holds for k ≤ 13, and Graham holds for |A| ≤ 13 at every prime. This is not new: CDFV prove |A| ≤ 20. k = 14 is running.

**Negative results** (each one rules out a proof strategy):

- (a) *Domain isolation is impossible.* By (iv), every Y ⊆ F\_p gives c·V(Y). The minimum number of surviving orderings is ≥ 14 at (p, m) = (7, 5), 32 at (11, 6), 208 at (11, 7), 252 at (13, 7), and 960 at (13, 8) (exhaustive over subsets containing 1). No unique-survivor configuration exists. The standard involutions (reversal, negation, μ\_m-rotation) give only the symmetries (iii), or a factor m.
- (b) *Schubert route:* by (v), the coordinates carry the same large primes (17, 73, 661, …).
- (c) *Smooth combinations:* the number of {−1, 0, 1}-combinations of the independent entries that are k-smooth is 22 / 26 at k = 7, 18 / 80 at k = 8, 2 / 80 at k = 9, and **0 / 242, 0 / 242, 0 / 728, 0 / 728** at k = 10, 11, 12, 13. Fourier norms are non-smooth for k ≥ 8. Moments and alternating or binomial sums are non-smooth.
- (d) *Randomness test:* among primes k < p < 200, the zero counts of c\_k mod p match the random expectation (e.g. k = 9: 4 observed vs 3.1 expected; k = 13: 4 vs 3.6), apart from the forced middle zero in the antisymmetric cases.

**GAP (the whole of CN).** There is no structural handle on c\_k mod p. The evidence says CN is true "for statistical reasons": the expected number of failures, summed over all k, converges. But c\_k behaves like an arithmetically random vector. A proof would need hidden structure that none of (a)–(d) detects, for example a weight-preserving sign-reversing involution on block-zero-free orderings of a well-chosen Y. **Assessment:** the CN route is unlikely to give a proof. It gives a clean equivalent target and per-k certificates.

