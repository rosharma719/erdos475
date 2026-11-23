# Methodological review (2026-11-22, end of session 1)

Grounded in: research/ledger.md (≈700 lines, ~16 numbered "rounds" in two days), the corrections recorded in it, proof_graph.yaml, and how this session ran.

## A. Errors of strategy and evidence (most serious first)

1. **Confirmation evidence is gathered where the conjecture cannot fail.** Graham is verified for p ≤ 37 (ledger), so every strengthening tested at p ≤ 23–29 (ADJ-ALL, BR_3, EC, MC, FOLD, pure lift-closure, move-chain rates) lives inside a region where the base statement is already known true. The ledger itself says counterexamples could only exist for p ≥ 41 and |A| ≥ 21, and its own history shows the dense regime breaking at modest parameters that earlier searches skipped (Z* looked fine at |B|≤5 and fails at h=7,8,10; the three-jump "96%" statistic was computed against a false hypothesis). Remedy: test strengthenings first at p ≥ 41 on ADVERSARIAL families (symmetric, coset unions, near-complete, APs, dense random), and report searches for counterexamples, not confirmations. Treat "0 failures at p ≤ 29" as nearly uninformative.

2. **Streetlight effect: effort followed what is easy to verify.** The planned split was A (dense flexibility) 60 / B (near-complete) 30 / C 10; actual effort was roughly the reverse because B yields finite-checkable constructions. p−4, p−5 are real but are a sliver and do not touch the middle range. Visible progress (new audited lemmas) was allowed to steer the allocation. Remedy: fix the allocation in config; require each round to state its expected effect on coverage of the target (the director rule exists but was not applied to human/GPT rounds).

3. **We missed a five-line reduction for a day.** The same-size one-element balancing lemma collapsed the entire non-zero-sum branch of NC3/NC4. Before it, rounds were spent on a two-pair zipper lemma, cyclotomic double-transversal constructions, coverage tables, and quadratic corollaries for the generic case. Remedy: a mandatory "symmetry/reduction audit" at the start of every programme — list all invariances and reversible transformations (dilation, rotation, reversal, translation of vertex sets, one-element replacement, complement, merge/contraction) and ask which cases collapse BEFORE constructing for them.

4. **Self-verification and uneven audits.** The ledger's protocol says Claude verifies GPT, but Claude's own claims (index-two theorem, balance identity, contraction lemma, three-jump lemma) were labelled "proved by Claude" and never audited by anyone else; the three-jump lemma was false as first stated. "Verified by Claude" must not apply to Claude-authored claims. Remedy: author ≠ auditor; the referee gates in the engine are the only path to analytically_verified; ledger labels must come from the graph, not prose.

5. **Strategic pivots on unaudited estimates (UPDATE: GPT's primary-source pass withdrew the e^(10^10) figure; real constants still unextracted).** "Computation cannot close the gap" rests on a rough chain estimate (≥ e^(10^10)) built from inequality shapes in abstracts; no one has read the proofs of Pham–Sauermann/Bedert–Kravitz/Müyesser–Pokrovskiy to extract actual constants or to see which step an explicit non-asymptotic argument would have to replace. Open problem #2 ("effective large-p theorem") in the ledger has had zero work in two days. Remedy: one focused literature task that reads the primary proofs and writes down the real quantitative dependencies and bottleneck lemma(s); decide on the effective route only after that.

6. **"Published" nodes are second-hand.** HOS Lemma 4.5, the p−3 result, CDFV ≤ 20, the 2026 arXiv items: statements were taken from the ledger/other models, never from the papers. A proof architecture is only as good as these. Remedy: for every `published` node store source, exact statement, and page; unverifiable ones are downgraded to `candidate`.

7. **"For all p" claims checked only up to p ≈ 50–100.** Selection lemmas (4-element selection, pair-position lemma, coset-escape hypotheses) were verified by finite computation plus partial hand proof. Arithmetic coincidences (orders of −2, −3, 2, small primes) are exactly where such lemmas fail. Remedy: a certificate method — reduce each uniform lemma to polynomial/multiplicative-relation equations whose failure set is a FINITE explicit list of primes, then cover that list by exhaustive computation; record the list.

8. **Reformulation churn.** The ledger's own synthesis says every route (zigzag, absorber, sparse counting, CN, free-point, repair) "reduces to the same core". New reformulations (FP∀, DFL, EC, MC, ADJ-ALL, FOLD, Q-closure) multiply statements that all presuppose Graham for the same sets, so none can be proved without proving existence. Remedy: every new conjecture must come with (i) what it implies, (ii) what it is implied by, (iii) a proof sketch of the step that is NOT already the original problem. Otherwise label "restatement".

## B. Errors in this session's execution (mine)

9. **Premature infrastructure.** I built the campaign controller, parallel branches, novelty comparison and views before one paid prover round had produced a single usable result; the first rounds failed on token starvation, refusals, a bad task budget, connection resets. About $8.8 of API spend produced only known-regime lemmas, while GPT + local computation produced all the mathematics. Remedy: validate the cheapest end-to-end loop on a known-solution task first; keep infrastructure proportional to demonstrated yield.

10. **Negative results trusted without positive controls.** Two of my own searches printed false "failures" (a closing-step bug in adj_search; a filter bug in the cyclotomic audit) and I caught them only because the output looked implausible. Remedy: every search script gets a known-positive control before its negatives are recorded.

11. **Graph/ledger drift.** The ledger became an append-only narrative; the proof graph is a second source of truth and was corrupted twice (finite check promoted a universal claim; partial accepts counted as audit passes). Remedy: the graph is canonical; the ledger entry is generated from graph deltas; a CI check (`check-graph`) must run before each commit-equivalent.

12. **Test data not adversarial or scale-matched.** Move-chain and flexibility statistics used uniformly random zero-sum sets; the known-hard instances are structured. Remedy: instance generators for structured families, run at p ≥ 41 with randomized search.

## C. What is working (keep)
Independent re-implementation of every supplied construction; audits saved as scripts; negative results written down (merge-chain, repair, fixed-Walecki, Z*, swap-robustness); the reduction/zero-sum discipline once found; refusing to promote candidates without gates.

## D. Revised protocol (adopted)
1. Reduction audit first. 2. Evidence at p ≥ 41, adversarial instances, positive controls. 3. Author ≠ auditor; graph is canonical. 4. Primary-source check for every published node. 5. Uniform lemma ⇒ finite exceptional-prime list + computation. 6. Every new conjecture states what is new beyond "Graham for these sets". 7. Fixed effort allocation across programmes, with kill criteria. 8. Infrastructure only after a demonstrated yield.
