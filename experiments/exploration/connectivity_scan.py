import itertools, sys, collections
sys.path.insert(0, "experiments/exploration")
from cycle_space import valid_cycles, canon, neighbors
def comps(A, p):
    cl = list(set(canon(c) for c in valid_cycles(A, p))); idx = {c: i for i, c in enumerate(cl)}; par = list(range(len(cl)))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for c in cl:
        for d in neighbors(c):
            d = canon(d)
            if d in idx: par[f(idx[c])] = f(idx[d])
    return len(cl), len({f(i) for i in range(len(cl))})
p = int(sys.argv[1]); lo = int(sys.argv[2]); tot = disc = empty = 0; worst = []
for k in range(lo, p - 1):
    for A in itertools.combinations(range(1, p), k):
        if sum(A) % p: continue
        if A[0] != min(A) or 1 not in A and False: pass
        n, c = comps(list(A), p); tot += 1
        if n == 0: empty += 1
        if c > 1: disc += 1; worst.append((A, n, c))
print(f"p={p} zero-sum sets size>={lo}: {tot}, no valid cycle: {empty}, disconnected valid-cycle spaces: {disc}")
for w in worst[:8]: print(" ", w)
