"""Independent audit (own code) of GPT's counterexamples to energy-minimisation / swap-maximisation as selection rules for EC, and of the minimal-zero-sum MC theorem."""
import itertools, collections
def verts(a, p):
    s = 0; V = [0]
    for x in a[:-1]: s = (s + x) % p; V.append(s)
    return V
def rooted(B, p, z):
    out = []
    for suf in itertools.permutations([x for x in B if x != z]):
        a = (z,) + suf
        if sum(a) % p == 0:
            V = verts(a, p)
            if len(set(V)) == len(B): out.append((a, V))
    return out
def energy(V, p):                       # sum_d m(d)(m(d)-1), m(d)=#{x in V: x+d in V}
    Vs = set(V); m = collections.Counter()
    for x in V:
        for d in range(1, p):
            if (x + d) % p in Vs: m[d] += 1
    return sum(c * (c - 1) for c in m.values())
def mobility(a, p):
    k = len(a); good = 0
    for i in range(2, k):
        b = list(a); b[i - 1], b[i] = b[i], b[i - 1]
        good += len(set(verts(b, p))) == k
    return good
def check(p, B, z, r, mode):
    cyc = rooted(sorted(B), p, z); assert sum(B) % p == 0
    key = (lambda c: energy(c[1], p)) if mode == "energy_min" else (lambda c: -mobility(c[0], p))
    best = min(key(c) for c in cyc); opt = [c for c in cyc if key(c) == best]
    avoid = [c for c in cyc if r not in c[1]]
    print(f"{mode}: p={p} B={sorted(B)} z={z} r={r}: valid rooted cycles {len(cyc)}, optimum value {abs(best)}, #optimizers {len(opt)}, "
          f"all optimizers visit r: {all(r in c[1] for c in opt)}, avoiders exist: {bool(avoid)} ({len(avoid)})")
check(41, {10, 21, 25, 31, 36}, 10, 5, "energy_min")
check(41, {6, 7, 9, 28, 35, 38}, 6, 3, "energy_min")
check(41, {3, 5, 13, 28, 33}, 3, 8, "mobility_max")
# minimal zero-sum sets: every ordering valid and every internal vertex removable by a swap  (p=23,29 exhaustive over minimal sets of size 5..7)
for p in (23, 29):
    n = tested = bad = 0
    for k in (5, 6, 7):
        for B in itertools.combinations(range(1, p), k):
            if sum(B) % p: continue
            if any(sum(S) % p == 0 for r in range(1, k) for S in itertools.combinations(B, r)): continue
            n += 1
            z = B[0]; a = (z,) + tuple(x for x in B if x != z)
            for suf in itertools.islice(itertools.permutations(B[1:]), 40):
                a = (z,) + suf
                assert len(set(verts(a, p))) == k            # every ordering valid
                for i in range(2, k):
                    b = list(a); b[i - 1], b[i] = b[i], b[i - 1]
                    tested += 1; bad += len(set(verts(b, p))) != k
    print(f"minimal zero-sum sets p={p}: sets {n}; swaps tested {tested}; invalid swaps {bad}")
