# NC3 inverse-pair case (CANDIDATE; proposed by external review, system-checked locally, NOT audited)

**Proposition.** p odd prime, C = {u, −u, v} ⊆ F_p^×, v ≠ ±u. Then A = F_p^× ∖ C has a valid ordering.

**Proof (sketch as proposed).** p = 2r+1, r ≥ 9. Dilate by ν with νv = r; νu = ±d, d ∈ {1..r−1}. HOS Lemma 4.5 gives a graceful permutation α of [1..r] with last absolute difference d (exceptions (d,r) ∈ {(2,4),(2,5),(2,8)}; reverse to convert a prescribed first difference into a last one). With δ_i = α_{i+1} − α_i the rotational sequencing is (δ_1..δ_{r−1}, r, −δ_{r−1}..−δ_1, −r), which contains the consecutive block (δ_{r−1}, r, −δ_{r−1}) whose set is {±d, r} = νC. Deleting it leaves a consecutive arc of a valid cyclic sequencing of F_p^×, so its partial sums are distinct. Dilate back. p ≤ 37 by exhaustive verification.

**Depends on:** HOS Lemma 4.5 (exact statement/hypotheses not yet checked against the paper), FINITE_P_LE_37.
**Checks the system ran:** construction verified end-to-end at p = 19, 23 (all d) and p = 29 (12/13 d).
