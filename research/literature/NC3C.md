# Literature report for contract NC3C: ordering the complement of a 3-element set (|A| = p − 4)

**Limits of this report:** the search tool hit its usage limit after one query. Only one reference (§1) was checked against an online source in this session. Everything else comes from my memory. Each entry says which of these it is:
- **CONFIRMED**: the reference was checked online in this session.
- **UNVERIFIED (memory)**: I believe the paper exists, but I did not confirm the exact bibliographic details or statement.
- **UNVERIFIED-LEDGER**: the claim appears only in the ledger, not in anything I checked.

Before anyone builds on an UNVERIFIED result, they should look up its exact statement.

---

## 1. Directly on the principal gap

**[HOS] J. Hicks, M. A. Ollis, J. R. Schmitt, "Distinct partial sums in cyclic groups: polynomial method and constructive approaches," J. Combin. Des. 27(6) (2019) 369–385, doi:10.1002/jcd.21652. CONFIRMED (title, authors, venue, pages).**
- **What the paper treats (confirmed from the abstract snippet):** Alspach's conjecture. For cyclic Z_n and A ⊆ Z_n∖{0} with ΣA ≠ 0, A should have an ordering whose partial sums are distinct and **nonzero**. The abstract says one result is by direct construction (near-complete sets) and the other is non-constructive (Combinatorial Nullstellensatz, small |A|, prime n).
- **Exact ranges: UNVERIFIED.** The snippet was cut off. The ledger's reading is that it covers |A| ≥ p − 3; Kravitz (§4) cites p − 3 ≤ |A| ≤ p − 1. "Lemma 4.5", its exceptions (d, r) ∈ {(2,4), (2,5), (2,8)}, and the remark that p − 4 "seems unlikely" by truncation are UNVERIFIED-LEDGER. I could not see the full text. Someone should read the PDF and check the lemma number and the exception list before citing them.
- **Hypotheses that fail here:**
  - Alspach's version needs ΣA ≠ 0. For A = Z_p^*∖C we have ΣA = −ΣC, so zero-sum C (your case ii) is **outside** Alspach's conjecture. That case needs Graham's weaker version, where the last partial sum may be 0.
  - In case (i), Alspach's version (nonzero partial sums) is stronger than you need.

**Why truncation can never handle zero-sum C (elementary; my own check, not a cited result).** Take a valid cyclic ordering of all of Z_p^*. Rotating it keeps it valid, so you can move any block of consecutive steps to the end and delete it. The steps that remain still have distinct partial sums. So any C that appears as a consecutive block, in some dilation of some such ordering, is handled. But cyclic intervals of length 1 to p − 2 in such an ordering never sum to 0. A zero-sum C therefore never appears as a block. This is the ledger's obstruction (3), and it explains why case (ii) needs contraction instead.

**No published result for |A| = p − 4 is known to me.** I know of no published "selection lemma over dilations and positions" for terrace or graceful constructions. Both should be treated as open.

## 2. Constructions: terraces, graceful permutations, Walecki and twizzler

- **B. Gordon, "Sequences in groups with distinct partial products," Pacific J. Math. 11 (1961) 1309–1313. UNVERIFIED (memory), but standard.**
  - It shows Z_n is sequenceable iff n is even, using the zigzag sequencing 0, 1, −1, 2, −2, …
  - That zigzag is the Walecki-type graceful pattern.
  - It applies to the whole group, not to subsets of Z_p.
- **M. A. Ollis, "Sequenceable groups and related topics," Electron. J. Combin., Dynamic Survey DS10 (2002; later revisions). UNVERIFIED (memory) for the edition and sections.**
  - This is the standard reference for terraces, R-sequencings, harmonious groups, and operations on terraces.
  - It is the first place to look for "local terrace transformations."
- **M. A. Ollis, C. R. Willmott, "On twizzler, zigzag and graceful terraces," Australas. J. Combin. (c. 2011). UNVERIFIED (memory). I am not sure of the exact title, year, or volume.**
  - My recollection: it constructs terraces for Z_{2m} from graceful permutations, using the "twizzle" operation (re-orienting segments).
  - This matches the contract's "Walecki/twizzler type."
  - Check whether its families have **free parameters** (segment positions). Those would supply variable position.
- **R. E. L. Aldred, J. Širáň, M. Širáň, "A note on the number of graceful labellings of paths," Discrete Math. 261 (2003) 27–30. UNVERIFIED (memory).**
  - My recollection: an exponential lower bound, roughly (5/3)^n, on the number of graceful permutations, built by gluing local pieces.
  - **M. Adamaszek, "Efficient enumeration of graceful permutations," arXiv:math/0608513 (2006). UNVERIFIED** (memory), including any improved growth constants.
  - Relevance: an exponential family made from glued pieces is the natural source of "position freedom" for a selection lemma. The ledger's 91/228 failure rate at r = 14 shows that you need that freedom.
- **B. Alspach, D. L. Kreher, A. Pastine, "The Friedlander–Gordon–Miller conjecture is true," Australas. J. Combin. 67 (2017). UNVERIFIED (memory).**
  - My recollection: abelian groups whose Sylow 2-subgroup is trivial or non-cyclic are R-sequenceable.
  - Relevance: this gives full-set objects (orderings of G∖{e}) of the kind you truncate. It is not about subsets.

## 3. Methods that might carry over to complements of size c > 3

- **Linear realizations and the Buratti–Horak–Rosa (BHR) conjecture.**
  - P. Horak, A. Rosa, "On a problem of Marco Buratti," Electron. J. Combin. 16 (2009) #R20. UNVERIFIED (memory).
  - M. A. Ollis, A. Pasotti, M. A. Pellegrini, J. R. Schmitt: "New methods to attack the Buratti–Horak–Rosa conjecture" (Discrete Math., c. 2021) and "Growable realizations: a powerful approach to the BHR conjecture" (Ars Math. Contemp., c. 2022). UNVERIFIED (memory) for titles, venues and years.
  - **This is the closest published match to a "scalable local-pattern embedding."** As I recall it, a "growable" realization is a base realization that stays valid when a block is inserted at a designated place, which lets you induct over v.
  - **Hypothesis mismatch:**
    - BHR edges are *unsigned* (length ±x) and the path is Hamiltonian in K_v.
    - Your walks are *signed* (steps exactly the elements of A) and visit p − c vertices.
    - Transferring the method needs sign control. Expect extra failures on symmetric or dense sets (pitfall 14).
- **N. Alon, "Combinatorial Nullstellensatz," Combin. Probab. Comput. 8 (1999) 7–29.** Standard; this is the CN behind the HOS non-constructive part and the ledger's CN round.
- **N. Alon, "Additive Latin transversals," Israel J. Math. 117 (2000) 125–130. UNVERIFIED (memory) for the exact statement.**
  - Statement as I recall it: p prime, A ⊆ Z_p with |A| = k < p, and any sequence b_1, …, b_k (repeats allowed). Then some numbering of A makes the sums a_i + b_i pairwise distinct.
  - Possible use: as a matching tool in a selection lemma, e.g. assigning dilations or positions to windows.
  - **It does not control partial sums.** Do not use it as a sequencing result.
- **J. A. Dias da Silva, Y. O. Hamidoune, "Cyclic spaces for Grassmann derivatives and additive theory," Bull. London Math. Soc. 26

[note: truncated at 12k tokens in first run]
