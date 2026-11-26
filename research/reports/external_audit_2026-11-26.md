# External research audit and proposed path (2026-11-26)

**Provenance.** Pasted into the session by the repo owner. Written from the public `main` branch (README, ledger, proof graph, 2026-11-24 STRATEGY, several claim files) plus the literature. The author could not list branches or clone, did not rerun any computation, and did not check every candidate proof. The literature table and arXiv IDs below are **unverified here**. In particular, IDs `2610.34424` and `2610.40712` should be checked before anything cites them. Nothing below is a repo-certified result. See "Review notes" at the end.

## 1. Objectives (keep them separate)
- **Complete:** all primes, or a counterexample.
- **Effective:** explicit thresholds, leaving a finite check that can actually be run.
- **Structural:** a uniform mechanism that explains why valid orderings exist.

Per the report: Pham–Sauermann (Feb 2026), combined with earlier work, gives the conjecture for all sufficiently large p, so #475 is "decidable, resolved up to a finite check". Kuang–Wang and Nguyen–Tran–Vu (Oct 2026) reportedly extend this to large subsets of arbitrary finite abelian groups. The repo's own estimates put the NTV-type thresholds at about 2^(1.6e12), or about 2^(9.4e10) after optimization. These are proof-architecture costs, not true thresholds, and are far outside brute force. Effective-constant extraction alone will not finish the problem.

## 2. Core diagnosis
- Every surviving induction (free-point contraction/expansion, bounded-span integer lifting, spiral coarsening) ends at one unproved step: **find a smaller valid cycle compatible with the next operation**. Selecting one cycle and then repairing it keeps failing.
- Balance identity: after j contractions, |B_j| = n−j and |R_j| = j (j reversal constraints), so slack stays p−n. Recursive contraction gains nothing, and the problem just moves from ordering labels to avoiding points.
- Literature successes (absorption; anticoncentration plus local repair) engineer a **distribution or family** of intermediate objects. They do not prove that a single convenient one exists.
- Stronger auxiliary conjectures (FV, IRC, universal spiral) have repeatedly turned out to be as hard as, or false relative to, Graham. Treat a failure of an auxiliary conjecture as information, never as a failure of Graham.

## 3. Proposed tracks (priority order)
1. **Minimal-counterexample structure (Contract A).**
   - Let A be a minimum zero-sum counterexample. For every admissible pair e={x,y} with t=x+y∉A∪{0}, set B_e=(A∖e)∪{t}. Minimality gives valid rooted cycles, and failure of expansion forces **every** rooted cycle of B_e to visit both x and y.
   - This holds simultaneously for all e, and it is much weaker than FV, which asks for avoidance for every smaller set.
   - Study the contraction incidence graph Γ(A): edge xy exists iff x+y∉A∪{0}, coloured by x+y. Colour classes are matchings.
   - Simultaneous expansion of r disjoint pairs is an SDR problem with 2-element choice sets (Hall; pseudoforest condition per component).
   - Hall-deficiency potential D(C) = r − ν(C). Seek exchanges that lower D(C), or a structural description of positive-deficiency local minima.
   - Experiment: enumerate all valid cycles of contracted sets for small p, and record the deficiency distribution, exchange-graph components, restricted sumset size, inverse-pair count, additive energy and Fourier bias.
2. **Complement-5 (Contract B).** Prove that F_p^× ∖ H has a valid ordering for every zero-sum |H|=5.
   - Case I (inverse pair): H={u,−u,v,w,−v−w}. This needs compatible 2-hole and 3-hole gadgets, and the compatibility is the real work.
   - Case II (no inverse pair): H is minimal zero-sum and normalizes to {1,a,b,c,−1−a−b−c}, a 3-parameter family.
   - Method: a library of parametrized Walecki/modular symmetric contraction gadgets, plus a symbolic covering proof of the parameter domain (piecewise-affine conditions with equalities L(a,b,c,p)=kp, k bounded). Optimize coverage of the parameter space, not the count of solved primes.
   - Real goal: a reusable absorption operation, and eventually |H| ≤ εp ⇒ rearrangeable with explicit ε.
3. **Sound symbolic certification (Contract C).**
   - The CDFV (Costa–Della Fiore–Fontana–Vena) rational row-span test only gives d·u ∈ rowspan_Z(M). That does not imply u·a=0 in groups with torsion.
   - The reported numerical rank, branch-completeness and zero-sum handling issues are separate problems.
   - Fix: exact arithmetic; integer-lattice (Smith/Hermite) membership for all-group claims; over F_p use rowspan over F_p, and track exceptional primes of the minors.
   - Architecture: untrusted certificate generator plus a small deterministic verifier. This is independently publishable.
4. **Quantitative cycle flexibility (Contract E).**
   - Define q_{B,t}(x) = Pr(x ∉ V(C)) over a distribution on rooted valid cycles. Σ_x q = p−|B|, and q(x) = q(t−x) under reflection symmetry.
   - Use the variance from the uniform value as a structure/randomness diagnostic: unstructured sets via Pham–Sauermann-style repair, structured sets via explicit constructions.
   - Test adversarially before investing in a proof. The inequality q ≥ c(p−|B|)/p is not asserted.
5. **Hall-deficiency switching (Contract D)**, subsumed by track 1.

De-prioritized or closed: asymptotic constant extraction; larger exhaustive primes (p=47 is about 13x the p=43 workload; N_p ≈ 2^(p−1)/(p(p−1))); compact-spiral universal construction (refuted); prescribed-cycle local repair (parked); universal CN coefficient identity (parked); IRC as the main route (stronger than needed).

## 4. Process recommendations
- Statuses to distinguish: conjectured / experimentally supported / proof candidate / model-reviewed / expert-reviewed / machine-verified / refuted. Two model referees can share a blind spot (for example the torsion error), so `analytically_verified` should not mean more than the evidence behind it.
- The proof graph needs **AND–OR** structure, and every node needs a machine-readable domain such as `p≥p0, n≤f(p), ΣA=0, A=−A`, so uncovered parameter ranges can be detected.
- A round counts as successful only if it yields: a new rigorous theorem, a validated counterexample to a precisely stated mechanism, a strictly weaker sufficient conjecture with a credible proof mechanism, a structural classification, or an independently checkable certificate. A reformulation, or more random tests of an already well-tested conjecture, does not count.
- Every contract needs an explicit stop rule.
- Falsification hierarchy: (1) Graham, (2) global contraction criterion, (3) restricted FV/DOM, (4) quantitative flexibility, (5) local switching. A failure at a lower level is never reported as a failure of a higher one.
- Counterexample search targets: near-complete sets with asymmetric holes, residue/coset sets, dense asymmetric integer intervals, perturbations of extremal symmetric sets, many short zero-sum subsets, high additive energy, few admissible contractions. Also estimate Z(A)/(n−1)! rather than only success or failure.
- FV scope: restricted FV needs only `x,y∉B, x≠y, x+y=t`, and some rooted cycle of B avoids x. The full-set case B=F_p^× needs separate justification (one omitted vertex per cycle is not automatically a counterexample to FV).

## 5. Complete-resolution architectures
- **A (preferred):** a minimal counterexample is rigid, and rigid sets have explicit orderings.
- **B:** overlapping effective ranges (symbolic n≤K; rectification/repair K<n≤f(p); cycle selection up to p−g(p); hole absorption above). The danger is that the thresholds never overlap at useful p.
- **C:** a computer-assisted classification of structural types of counterexample, which would need an effective complexity reduction the repo does not yet have.

Organizing question: *what additive structure forces every valid cycle of a smaller set to be incompatible with every possible expansion of a hypothetical minimum counterexample?*

## 6. Review notes (added on filing; not part of the pasted report)
- The determinant "Proposition" (p > n^{n/2} ⇒ every n-set works) was read through once. The row-space and Hadamard step looks right: d invertible mod p gives u·a=0 from du∈rowspan_Z(M). It then relies on an integer sequenceability theorem for the lifted set preserving exactly the same zero-sum subsets. That theorem and the exact interval/cyclic conventions have not been checked here. It also gives only an astronomically weak cutoff, and the report itself says novelty is unclaimed. Treat it as a candidate, not an audited claim.
- The complement-5 case split (inverse pair vs minimal zero-sum 5-set) is elementary and correct as stated.
- The 2^(1.6e12) and 2^(9.4e10) figures and the "74 nodes: 51/5/2/8/8" census are restated from existing repo files and were not recomputed.
- The report cites "our previous work" (exhaustive verification through p=43, 5-element asymmetric remainders). Check `research/ledger.md` before relying on those statements.
