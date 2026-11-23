# Next GPT prompt (round after "bounded-swap theorem is false")

**Read first (frontier — do NOT rederive or restate):** research/STATE.md, research/METHOD_REVIEW.md, research/claims/*.md.
Established (audited by independent code, referee gates pending): one-element zero-sum reduction; |A|=p−4, p−5; NC3-Z; zipper/cyclotomic/double-transversal; geometric swap theorem; coset escape; symmetric ⇔ folded graceful cycle. Closed negative results: merge-chain/balance identity, arbitrary-obstacle lemmas, one-move repair, bounded adjacent-swap repair from an arbitrary cycle (your counterexample), swap-robust cycles not always available (exhaustive p=11,13), fixed-Walecki/low-index cyclotomic coverage, edge-subdivision induction.
Target of everything: a complete analytic proof of Erdős #475 for all primes. Near-complete sizes are a sliver; the dense middle range is the real problem.

## TASK A (bounded, do first; one round): primary-source quantitative map of the large-p theorems
Our strategic decision "an effective threshold is infeasible" rests on an unaudited rough estimate. Read the actual papers (Pham–Sauermann arXiv:2602.15797; Müyesser–Pokrovskiy; Bedert–Kravitz; Kravitz arXiv:2407.01835; Bedert–Bucić–Kravitz–Montgomery–Müyesser; Hicks–Ollis–Schmitt arXiv:1809.02684 incl. the EXACT statement and hypotheses of Lemma 4.5; Costa–Della Fiore–Fontana–Vena). For each regime of |A|:
1. exact theorem statement + hypotheses (quote it), and where the constants are or are not explicit;
2. the bottleneck lemma that makes the threshold non-explicit or astronomically large;
3. the proof ARCHITECTURE (random greedy / absorption / regularity / Nullstellensatz): which step would have to be replaced by an explicit argument;
4. whether any of our audited tools (contraction, zero-sum reduction, coset/cyclotomic cycles, geometric swaps) could plausibly replace an absorber or a random step, with a precise statement of what would be needed.
Mark anything you could not read in the primary source as UNVERIFIED. Deliverable: a table + a one-paragraph verdict on whether ANY regime admits an explicit non-asymptotic proof architecture.

## TASK B (main, open-ended with stop rule): EC by cycle SELECTION, not repair
EC: for zero-sum B with a valid cycle, z∈B and r∉B∪{0} there is a valid cycle with first step z avoiding r (MC: any r∉{0,z}, |B|≥5). Repair from an arbitrary cycle is dead; prove EXISTENCE of a good cycle.
Step 0 (≤1 page): reduction audit — list every invariance/transformation that preserves validity (dilation, rotation, reversal, translation of the vertex set, one-element replacement, complement, merge/contraction, rooting change) and say which cases of EC/MC they collapse. Prove any new reduction.
Then attack by an EXTREMAL/GLOBAL argument: choose a valid rooted cycle optimizing a potential (e.g. number of vertices in a prescribed region, additive-energy defect E₊(V), number of dependency-graph edges from your last note) and show an optimal cycle cannot have r as a vertex; use multi-move trades (segment/interval trades, not only adjacent swaps) if needed. Alternatives allowed if you justify why they escape the balance identity.
STOP RULE: two genuinely different mechanisms, each tried to the point of a precise obstruction (a concrete minimal counterexample to the mechanism, with p, B, z, r). Then report and stop; do not drift to new reformulations.

## RULES (from the methodological review)
- Every NEW conjecture must state: what it implies, what implies it, and what is new beyond "Graham for these sets". Otherwise label it a restatement.
- Finite tests are for FALSIFICATION. Test your claims at p ≥ 41 (first unverified prime) on adversarial families (symmetric, coset unions, near-complete, arithmetic progressions, dense random); give a positive control for each search; uniform-in-p lemmas must come with an explicit finite exceptional-prime list.
- Mark gaps explicitly (GAP-n: exact missing statement). No "similarly/clearly" outside a declared gap.
- Report coverage accounting: for each result, which (p, |A|) region it proves, using only proved statements.
- Do not promote anything to "proved" that is not a complete proof; the referee gates will do that.
- Deliverables: proofs, scripts that I can re-run independently, exact counterexamples, and a ≤10-line summary of what is established vs open.
