# Cycle-selection round: verifiers (GPT, 2026-11-25; audited in research/claims/cycle_selection_audit.md)

Standard-library Python 3.10+. Scripts import each other and read data next to themselves, so run them from this directory:

    gunzip -k width12_data.json.gz bridge_data.json.gz bridge_small_moduli.txt.gz
    for f in check prefix_avoidance_certificate five_hole_certificate extensions barrier \
             general_check width12_verify offset_verify bridge_verify bridge_regression equal_sums; do python3 $f.py; done

Total runtime is about 15 s. The expected outputs are in the audit file. `note.tex` is GPT's LaTeX source for one of the bundled notes.
