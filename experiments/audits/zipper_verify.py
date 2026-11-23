"""Independently construct the zipper ordering from sampled sequencings and verify the ordering of F_p^*\\C directly."""
import random, itertools, sys
sys.path.insert(0, "experiments/exploration")
from zipper_coverage import rand_graceful, seq

def zip_orderings(b, p):
    n = len(b)
    for j in range(n):
        a1, a2 = b[j], b[(j + 1) % n]; s = (a1 + a2) % p
        if s == 0: continue
        for k in range(n):
            if {k, (k + 1) % n} & {j, (j + 1) % n}: continue
            x, y = b[k], b[(k + 1) % n]
            if s not in (x, y): continue
            c = y if s == x else x
            C = {a1, a2, c}
            if len(C) < 3 or (a1 + a2 + c) % p == 0 or s in C or any((-u) % p in C for u in C): continue
            # contract (j,j+1) -> s ; delete (k,k+1); arc starts at k+2
            steps = []
            idx = (k + 2) % n; skip = {k, (k + 1) % n}
            cyc = []
            i = 0
            while i < n:
                if i == j: cyc.append(s); i += 2          # j+1 handled
                elif i in skip: i += 1
                else: cyc.append(b[i]); i += 1
            # rebuild linear order as an arc: rotate so that deleted block is at the end
            # position of deleted block in the contracted sequence: reconstruct explicitly
            lin = []
            m = n
            order = [(t % n) for t in range(k + 2, k + 2 + n - 2)]          # arc after the deleted pair, cyclic
            seen = set(); t = 0
            while t < len(order):
                u = order[t]
                if u == j: lin.append(s); t += 2; continue
                if u == (j + 1) % n: t += 1; continue
                lin.append(b[u]); t += 1
            yield C, lin

if __name__ == "__main__":
    rng = random.Random(3); ok = bad = 0
    for p in (23, 29):
        r = (p - 1) // 2
        for _ in range(40):
            al = rand_graceful(r, rng)
            if not al: continue
            for C, lin in zip_orderings(seq(al, p), p):
                A = set(range(1, p)) - C
                ps = list(itertools.accumulate(lin, lambda s, x: (s + x) % p))
                good = sorted(lin) == sorted(A) and len(set(ps)) == len(ps)
                ok += good; bad += not good
    print("zipper orderings verified directly: ok", ok, "bad", bad)
