# Merge-chain obstruction
Tags: avoidance merge-chain LSA1 FP

Ordinary repeated merging in the free-point induction accumulates avoidance constraints faster than it creates
freedom (see the ledger's balance identity). A viable lemma must not be a plain iteration of the merge step.
(Replace this stub with the ledger's exact statement.)

Ledger detail: balance identity — unwinding Avoid(B,x,R) ⇐ Avoid(B',z,R∪{x}) from |A|=k, level j has |B|=k−j, |R|=j, free residues p−(k−j): each step adds one constraint and frees one residue, so slack = p−k at every level. The maximal hypothesis "avoid any R, |R| ≤ free−1" is false for small B (|B|=3 forces the visited set). Local one-move repair also fails in the dense regime. Tags: FP LSA1 avoidance.
