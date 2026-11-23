"""Symmetric sets A={±a_1..±a_m}.  Half-cycle form: (s_1..s_m, -s_1..-s_m) with s_j=±a_{σ(j)}; prefix sums P_0=0..P_m=T.
Valid  <=>  the 2m points {P_j} ∪ {T-P_j}, j=0..m-1, are pairwise distinct.   Does a half-cycle exist for EVERY symmetric A?"""
import itertools, sys, random

def half_cycle(classes, p, rng, cap=400000):
    m = len(classes); n = [0]
    # DFS over (class order, sign); maintain prefix points P (list) and need final T: check at the end (T depends on all steps)
    best = []
    def rec(P, used, steps):
        n[0] += 1
        if n[0] > cap: return None
        if len(steps) == m:
            T = P[-1]; pts = set(P[:-1]); refl = {(T - x) % p for x in P[:-1]}
            if len(pts) == m and len(refl) == m and not (pts & refl): return list(steps)
            return False
        cand = [(c, sg) for c in classes if c not in used for sg in (1, -1)]
        rng.shuffle(cand)
        for c, sg in cand:
            v = (P[-1] + sg * c) % p
            if len(steps) < m - 1 and v in P: continue
            P.append(v); used.add(c); steps.append(sg * c)
            r = rec(P, used, steps)
            if r: return r
            P.pop(); used.discard(c); steps.pop()
            if r is None: return None
        return False
    return rec([0], set(), [])

def run(p, rng):
    r = (p - 1) // 2; tot = fail = und = 0
    for m in range(2, r + 1):
        for classes in itertools.combinations(range(1, r + 1), m):
            tot += 1
            res = half_cycle(classes, p, rng)
            if res is None:
                res = half_cycle(classes, p, rng, cap=8_000_000)
            if res is None: und += 1
            elif res is False:
                fail += 1
                if fail <= 6: print("  NO half-cycle:", p, classes, flush=True)
    print(f"p={p}: symmetric sets (m>=2) {tot}, no half-cycle {fail}, undetermined {und}", flush=True)

if __name__ == "__main__":
    for p in map(int, sys.argv[1:]): run(p, random.Random(1))
