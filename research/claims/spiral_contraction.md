# Spiral contraction (SC / SC2): coverage audit and structure (Claude, 2026-11-24)
This is the rank-1 direction from `STRATEGY.md`. GPT's report was pasted in chat. Its certificate bundle (4.1 MB) was **not** received here, so the coverage claims were re-derived with independent code: `experiments/exploration/spiral_contraction/sc.c`, written from the definitions in the task prompt.

## Why SC2 would prove the conjecture
**Half-walk.** W = (δ, +M, −δ^rev, −M) for symmetric ±S ⊆ F_p^×, with δ a signed ordering of S ∖ {M}, distinct partial sums D, span(D) ≤ M − 1 and M + span(D) ≤ p − 1. Its vertex set is D ∪ (D + M), so W is a valid cycle mod p (lemma L6 / symmetric walk).

**Contraction.** Merge disjoint adjacent pairs of steps (cyclically). If the resulting block sums are distinct and nonzero, they form a valid cycle, because its vertices are a subset of W's.

**SC2.** Every zero-sum A ⊆ F_p^× is, up to dilation, a contraction of some half-walk using blocks of length ≤ 2.

**SC2 for all p ⇒ Graham for every prime.** SC2 covers the zero-sum case, and the one-element reduction handles the rest.

## Independent verification (exhaustive over all S and all admissible δ)
| p | half-walks | zero-sum orbits | covered by blocks ≤ 2 | runtime |
|---|---|---|---|---|
| 19 | 31,021 | 804 | **804 (100%)** | 0.1 s |
| 23 | 724,801 | 8,384 | **8,384 (100%)** | 7 s |

The per-size tables match GPT's exactly.
- **Stronger than GPT claimed.** Blocks ≤ 2 suffice for **every** size at p = 19 and 23, not only for dense sets.
- **p = 29** (331,184 orbits, GPT certificates): not independently re-run. The exhaustive matching enumeration is too large for this code.

## Structure: the minimal number of merges is nearly extremal
Let r_min be the minimum number of merged pairs over all certificates and dilations. GPT's asymmetry bound gives r ≥ lb := ⌈q(A)/3⌉, raised by 1 if needed to fix parity (r ≡ |A| mod 2). That bound is accepted: each merge changes q by ≤ 3.

| p | r_min = lb | r_min = lb + 2 | larger |
|---|---|---|---|
| 19 | 772 | 32 | 0 |
| 23 | 7,540 | 844 | 0 |

So **r_min ≤ lb + 2 always**, and equality holds for 90–96% of orbits. Equality with q = 3r forces the unmatched asymmetric elements to split into zero-sum triples, by GPT's equality corollary (accepted).

## GPT's other claims
- **Near-complete proof (|A| ≥ p − 5 via ≤ 2 merges of the alternating walk): ACCEPTED** (read).
  - The adjacency lemma for alternating δ is right.
  - The 3-complement normalisation u + v = −1 gives consecutive magnitudes.
  - The 4-complement uses the "bad pair" graph argument.
  - The |A| ≥ p − 5 range is already proved in this repo by Walecki contractions (NC3-Z, 4-complement). This is a cleaner re-proof inside the SC2 framework.
- **The example C = {7, 8, 10, 14, 18} at p = 19** (the old fixed-Walecki regression) is resolved by SC2: consistent with the 804/804 run.
- **The linear lower bound** r ≥ (1/12 − o(1))p for random half-density sets is accepted (concentration of q).

## Status and the precise gap
- SC2 is exhaustively true at p = 19 and 23 (independent), and at p = 29 per GPT's certificates (not re-run).
- **GAP (the whole conjecture, now in a concrete combinatorial form).**
  1. *Algebraic step:* choose a symmetric expansion of A, splitting about q/3 elements t = u + v.
  2. *Geometric step:* realise all the prescribed pairs (their magnitude graph has max degree 2) as adjacent steps of one admissible half-walk.
- The near-extremality data suggests looking for a proof that uses (close to) the minimal triple decomposition.

## Update (2026-11-24): compact SC2 refuted at p = 59; refined picture
GPT follow-up round, pasted in chat. The inline verifier was rerun here (`v59.py`), and the scope check is new (`imb.py`).

- **Imbalance obstruction: CORRECT (hand-checked).** In a compact half-walk the two layers D and D + M are separated. Only the two blocks containing a layer-crossing edge (±M) can need recentering, at most one each way. So Σ⟨block⟩ ∈ {−p, 0, p}, which gives I(A) := min_λ |Σ⟨λa⟩|/p ≤ 1 for every compact spiral contraction, with blocks of any length.
- **Counterexample: VERIFIED.** A = Q₅₉ (quadratic residues, |A| = 29, zero-sum) has centered sum ±177 under every dilation, so I = 3. Compact SC2 and compact SC (any block lengths) are **false**.
- **Modular half-walk lemma** (D distinct mod p, D ∩ (D + M) = ∅): trivially correct. The certificate δ (19 steps, 11 pair merges) contracts to exactly Q₅₉: VERIFIED.
- **Contraction-graph theorem and triple-packing bound** r ≥ max(⌈q/3⌉, ⌈(q − T)/2⌉): CORRECT. The component cases re-derived: two-vertex path d = 0; zero-sum triple d = 0; other paths and cycles 2d ≥ q.
- **The p = 101 example** U = [1, 33] ∖ {23, 33}, A = U ∪ ±[34, 43]: zero-sum, q = 31, T = 0 verified. So r ≥ 17 = lb + 6, and the "lb + 2" rule is **false** (my 19/23 data only reflected small p).
- **Correction accepted.** Attaining the parity-adjusted bound does not imply q = 3r, so the 90–96% is not a triple-decomposition rate.

### New observation (Claude): the obstruction is rare and arithmetic
| p | I(A) over 400 random zero-sum sets of size (p − 1)/2 | I(Q_p) |
|---|---|---|
| 29 | 0 (399), 1 (1) | 0 |
| 41 | 0 (400) | 0 |
| 59 | 0 (400) | **3** |
| 83 | 0 (400) | **3** |
| 101 | 0 (400) | 0 |

- For p ≡ 3 (mod 4), I(Q_p) equals the class number h(−p) in both cases checked (h(−59) = h(−83) = 3). This is consistent with Dirichlet's formula for the residue/non-residue excess on (0, p/2).
- So compact-SC2 failures come from **multiplicatively structured sets with few distinct dilations**. There are infinitely many such failures, growing like √p. Random sets have I = 0.

### Revised targets
1. **SC2-I (compact):** every zero-sum A with I(A) ≤ 1 is a compact ≤2-block spiral contraction.
   - This keeps the *explicit* valid cycle with no collision analysis, and it covers essentially all random sets.
   - Consistent with all data: p ≤ 23 exhaustive, GPT's p = 29 certificates, and the p = 31 sample.
2. **Sets with I(A) ≥ 2** (every dilation unbalanced by ≥ 2p): a structured, rare class (quadratic-residue-like). Classify them, then treat them separately, for example by modular half-walks (MSC2) or algebraic constructions.
3. **Caution on MSC2.** A modular half-walk is no longer an explicit construction: finding δ with distinct D mod p and D ∩ (D + M) = ∅ is itself a Graham-type sequencing problem. MSC2 loses the "no collision analysis" advantage. Prefer SC2-I plus a structural treatment of I ≥ 2.
