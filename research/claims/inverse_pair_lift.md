# Inverse-pair lift for G\* in the dense case (Claude, 2026-11-24)
Code: `experiments/exploration/inverse_pair_lift/invpair.c`.

**Idea.** Dense sets contain many inverse pairs x ∈ P ∩ N. Remove one, with x ≠ max P and x ≠ max N so the window is unchanged. Take a G-walk of the reduced instance, rooted at max P, and reinsert +x and −x at two distinct later positions i < j. The segment between them shifts by ±x.
If this always worked, the G\* induction would reduce to sets without inverse pairs.

**Data (values ≤ 9, at most 11 elements; 11,334 (instance, x) pairs; 2,554,971 reduced walks).**
- **Robust version ("every reduced walk extends"): FALSE.** 315,606 walks (12%) admit no insertion.
- **Existential version ("some reduced walk extends"):** fails for 18 (instance, x) pairs. All are small symmetric sets with a single reduced walk, for example P = N = {1, 2, 3} with x = 2.

**Conclusion.** The lift works only with a well-chosen reduced walk. That is the recurring "cycle-choice" obstruction (see `ledger.md` induction-route item (c), and the arbitrary-cycle expansion counterexample in `bs_handoff_submission.md`). So this does not give a proof mechanism for the dense case.
