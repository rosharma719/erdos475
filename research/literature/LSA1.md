I ran only 3 searches before hitting the search limit. Items marked **CONFIRMED** are ones whose abstract or page text I saw this session. Everything else is **UNVERIFIED** (from memory) and should not be treated as established.

## Bottom line for LSA1
- **Large p is settled, but only non-effectively, and by probabilistic or absorption methods.** None of the confirmed papers gives an explicit threshold or a non-asymptotic mechanism for the dense regime. That is the regime where FP∀ / DFL(1) must be proved for all p ≥ 41.
- **I found no published result that proves FP∀, DFL(1), Lemma 0 adjacency, or a PATH-AVOID-type flexibility lemma with an explicit range.** I also found no published result on valid-cycle connectivity.
- **The ledger's ≈e^(10^10) threshold is UNVERIFIED.** None of the abstracts I saw states a threshold.

## Confirmed results

1. **Pham & Sauermann, "On Graham's rearrangement conjecture", arXiv:2602.15797 (17 Feb 2026). CONFIRMED.**
   - What it proves: Graham holds when C_α ≤ |S| ≤ p^{1−α}, for any α ∈ (0,1). Quote: "We prove this conjecture for all subsets S⊆ℤ_p∖{0} with |S|≤p^(1-α) and |S| sufficiently large with respect to α".
   - Combined with earlier results, this settles all sufficiently large primes. The paper calls its method "inherently probabilistic", based on anticoncentration of sums of random subsets.
   - **Flag:** it needs |S| ≥ C_α and large p, and gives no explicit constant. It does not apply to the dense regime and cannot be made effective as stated. Excluded by the contract ("asymptotic_threshold_arguments").

2. **Bedert & Kravitz, "Graham's rearrangement conjecture beyond the rectification barrier", arXiv:2409.07403; Israel J. Math. (Springer DOI 10.1007/s11856-025-2871-6). CONFIRMED.**
   - Proves the conjecture for |A| ≤ e^{c(log p)^{1/4}}. That range comes from the citing paper arXiv:2503.18101, whose abstract says "this statement holds whenever |A|≤e^(c(log p)^(1/4))". Pham–Sauermann state the bound as exp((log p)^{1/4}).
   - The abstract says p is "a large prime".
   - **Flag:** small sets and large p only. Irrelevant to the dense regime.

3. **Kravitz, "Rearranging small sets for distinct partial sums", arXiv:2407.01835; Integers 24 (2024), A113. CONFIRMED.**
   - Quote: "We give a very short proof of this conjecture for sets A of size at most log p/log log p."
   - The method is rectification. A similar argument was given by Sawin in a MathOverflow comment (2015), as reported by arXiv:2503.18101.
   - **Flag:** sparse regime only.

4. **Bedert, Bucić, Kravitz, Montgomery & Müyesser, large-set result over ℤ_p. CONFIRMED only as described secondhand by Pham–Sauermann [2].**
   - The conjecture holds for |S| ≥ p^{1−c}, for a small constant c.
   - I did not get the exact title or arXiv id for the ℤ_p paper. A related paper by the same authors, "On Graham's rearrangement conjecture over F_2^n", arXiv:2508.18254, is a different group.
   - **Flag:** this covers the dense regime, but non-effectively, using absorption and expansion.

5. **Müyesser & Pokrovskiy (random Hall-type / absorption). CONFIRMED only via Pham–Sauermann's summary.**
   - The conjecture holds for |S| ≥ (1−o(1))p.
   - Title and arXiv id are not confirmed. **Flag:** non-effective.

6. **Bucić, Frederickson, Müyesser, Pokrovskiy & Yepremyan, "Towards Graham's rearrangement conjecture via rainbow paths", arXiv:2503.01825. CONFIRMED (citation, plus Pham–Sauermann's summary).**
   - Approximate version: all but o(|S|) of the partial sums are distinct. Asymptotic.

7. **Costa, Della Fiore, Feng & Liu, "Kneserized Anticoncentration and Reverse Absorption for Graham's Rearrangement Conjecture", arXiv:2608.10015. CONFIRMED (abstract and keywords).**
   - Composite moduli ℤ_{tp}: for fixed t with ℤ_t strongly sequenceable and p sufficiently large, every subset of ℤ_{tp}∖{0} has a valid ordering.
   - Its keywords include "local repair" and "reverse absorption", which overlap with LSA1's tags.
   - **Flag:** asymptotic in p. It may still be worth reading for the structure of its repair step, not for its threshold.

8. **Archdeacon, Dinitz, Mattern & Stinson, "On partial sums in cyclic groups", J. Combin. Math. Combin. Comput. 98 (2016), 327–342. CONFIRMED as a citation only.** Content not seen; source of the Alspach-type problem.

9. **Further citations listed in arXiv:2503.18101. CONFIRMED as references only; content not seen:**
   - Costa, Morini, Pasotti & Pellegrini, "A problem on partial sums in abelian groups", Discrete Math. 341 (2018), 705–712.
   - Costa, Della Fiore, Ollis & Rovner-Frydman, "On Sequences in Cyclic Groups with Distinct Partial Sums", Electron. J. Combin. 29 (2022), #P3.33.
   - Costa & Della Fiore, "Weak Freiman isomorphisms and sequencings of small sets", arXiv:2407.15785.
   - Alspach & Liversidge, "On strongly sequenceable abelian groups", Art Discrete Appl. Math. 3 (2020).

## UNVERIFIED (could not check this session; do not rely on these)
- **Hicks, Ollis & Schmitt, "Distinct partial sums in cyclic groups: polynomial method and constructive approaches", J. Combin. Des. (2019).** From memory: Combinatorial Nullstellensatz up to |A| ≤ 12, plus graceful/terrace constructions for near-complete A. This is likely the source of the ledger's "published covers c ≤ 2" and the "HOS graceful-terrace family". Exact ranges are unverified.
- **Bode & Harborth:** from memory, the near-complete cases |A| ∈ {p−1, p−2} (possibly p−3). Unverified.
- **Costa, Della Fiore, Fontana & Vena, arXiv:2603.20961:** the |A| ≤ 20/22/23 claims recorded in the ledger. I did not see this paper this session.
- **Dias da Silva & Hamidoune (1994), Erdős–Heilbronn:** the ledger uses this to get a legal merge pair. The statement is classical, but I did not check the exact form used.
- **Alon, "Combinatorial Nullstellensatz" (1999):** standard, not re-checked.

## Obstructions relevant to the principal gap
- I found no published structural obstruction. Every confirmed result is either sparse, or dense but non-effective.
- The ledger's "Strategic constraint" (non-explicit thresholds cannot finish the problem) is consistent with the literature: no confirmed source gives an explicit P₀.
- To make any of these methods usable, someone would have to extract explicit constants from Müyesser–Pokrovskiy or BBKMM absorption. As far as I found, that has not been published.

**Suggested follow-up searches** (I ran out of budget): Hicks–Ollis–Schmitt for the exact near-complete range; Müyesser–Pokrovskiy's title and id; the BBKMM ℤ_p arXiv id; and Ollis's dynamic survey "Sequenceable groups and related topics" (EJC) for terrace and graceful-permutation constructions with prescribed adjacencies.