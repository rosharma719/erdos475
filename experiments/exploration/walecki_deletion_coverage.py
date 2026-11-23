"""Cross-block contraction == deleting c vertices of a full rotational sequencing.  For zero-sum complements C of size c: which dilation
orbits of C are realised by deleting c vertices of the (fixed, dilation-closed) Walecki cycle?  (labels of the remaining cyclic walk must be distinct)"""
import itertools, sys
def walecki(r):
    a, lo, hi, tl = [], 1, r, True
    while lo <= hi:
        if tl: a.append(lo); lo += 1
        else: a.append(hi); hi -= 1
        tl = not tl
    return a
def orbit(C, p): return min(tuple(sorted(t * x % p for x in C)) for t in range(1, p))
def run(p, c):
    r = (p - 1) // 2; al = walecki(r)
    d = [al[i + 1] - al[i] for i in range(r - 1)]
    B = [x % p for x in d + [r] + [-x for x in reversed(d)] + [-r]]
    V = [0]
    for x in B[:-1]: V.append((V[-1] + x) % p)
    n = p - 1; cov = set()
    for dele in itertools.combinations(range(n), c):
        ds = set(dele); keep = [V[i] for i in range(n) if i not in ds]
        labs = [(keep[(j + 1) % len(keep)] - keep[j]) % p for j in range(len(keep))]
        if len(set(labs)) != len(labs): continue
        C = set(range(1, p)) - set(labs)
        cov.add(orbit(C, p))
    allc = {orbit(C, p) for C in itertools.combinations(range(1, p), c) if sum(C) % p == 0}
    print(f"p={p} c={c}: zero-sum complement orbits {len(allc)}, covered by deleting c vertices of ONE Walecki cycle (all dilations): {len(cov & allc)} ({100*len(cov&allc)/len(allc):.0f}%)", flush=True)
if __name__ == "__main__":
    for p in map(int, sys.argv[2:]): run(p, int(sys.argv[1]))
