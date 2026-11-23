import sys, itertools
sys.path.insert(0, "experiments/exploration")
from zipper_coverage import seq, covered_by, generic_orbits
def walecki(r):
    a, lo, hi, tl = [], 1, r, True
    while lo <= hi:
        if tl: a.append(lo); lo += 1
        else: a.append(hi); hi -= 1
        tl = not tl
    return a
for p in map(int, sys.argv[1:]):
    r = (p - 1) // 2; cov = set()
    al = walecki(r)
    for al2 in (al,):
        covered_by(seq(al2, p), p, cov)
    tot = generic_orbits(p)
    unc = sorted(tot - cov)
    print(f"p={p}: generic orbits {len(tot)}, covered by the single Walecki sequencing {len(cov & tot)}, uncovered {len(unc)} e.g. {unc[:3]}", flush=True)
