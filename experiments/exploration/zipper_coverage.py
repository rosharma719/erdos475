"""Zipper-lemma gap test: for generic C (sum != 0, no inverse pair) is there a rotational sequencing of F_p^* with disjoint
consecutive blocks (a,b) and (a+b,c) (either order each)? Sample HOS rotational sequencings (from random graceful permutations)
and record which dilation-orbits of C they cover."""
import random, itertools, sys

def rand_graceful(r, rng, cap=4000):
    for _ in range(200):
        x = rng.randint(1, r); used = 1 << x; diffs = 0; path = [x]; cnt = [0]
        def rec():
            cnt[0] += 1
            if cnt[0] > cap: return None
            if len(path) == r: return True
            l = path[-1]
            c = [z for z in range(1, r + 1) if not used >> z & 1 and not diffs >> abs(z - l) & 1]
            rng.shuffle(c)
            for z in c:
                nonlocal_used[0] |= 1 << z; nonlocal_diffs[0] |= 1 << abs(z - l); path.append(z)
                res = rec()
                if res: return True
                path.pop(); nonlocal_used[0] &= ~(1 << z); nonlocal_diffs[0] &= ~(1 << abs(z - l))
                if res is None: return None
            return False
        nonlocal_used = [used]; nonlocal_diffs = [diffs]
        def rec_wrap():
            nonlocal used, diffs
            return rec()
        # rebind used/diffs to cells
        used_cell, diffs_cell = nonlocal_used, nonlocal_diffs
        def rec3():
            cnt[0] += 1
            if cnt[0] > cap: return None
            if len(path) == r: return True
            l = path[-1]
            c = [z for z in range(1, r + 1) if not used_cell[0] >> z & 1 and not diffs_cell[0] >> abs(z - l) & 1]
            rng.shuffle(c)
            for z in c:
                used_cell[0] |= 1 << z; diffs_cell[0] |= 1 << abs(z - l); path.append(z)
                res = rec3()
                if res: return True
                path.pop(); used_cell[0] &= ~(1 << z); diffs_cell[0] &= ~(1 << abs(z - l))
                if res is None: return None
            return False
        if rec3(): return list(path)
    return None

def seq(al, p):
    r = len(al)
    d = [al[i + 1] - al[i] for i in range(r - 1)]
    return [x % p for x in d + [r] + [-x for x in reversed(d)] + [-r]]

def orbit(C, p):
    return min(tuple(sorted((u * c) % p for c in C)) for u in range(1, p))

def covered_by(b, p, out):
    n = len(b)
    for j in range(n):
        a1, a2 = b[j], b[(j + 1) % n]
        s = (a1 + a2) % p
        if s == 0: continue
        for k in range(n):
            if {k, (k + 1) % n} & {j, (j + 1) % n}: continue
            x, y = b[k], b[(k + 1) % n]
            if s == x: c = y
            elif s == y: c = x
            else: continue
            C = {a1, a2, c}
            if len(C) < 3 or (a1 + a2 + c) % p == 0 or s in C: continue
            if any((-u) % p in C for u in C): continue
            out.add(orbit(C, p))

def generic_orbits(p):
    orbs = set()
    for C in itertools.combinations(range(1, p), 3):
        if sum(C) % p == 0 or any((-u) % p in C for u in C): continue
        orbs.add(orbit(C, p))
    return orbs

if __name__ == "__main__":
    rng = random.Random(7)
    for p in map(int, sys.argv[2:]):
        r = (p - 1) // 2; cov = set(); tot = generic_orbits(p); seen = 0
        for it in range(int(sys.argv[1])):
            al = rand_graceful(r, rng)
            if al is None: continue
            seen += 1
            for al2 in (al, al[::-1], [r + 1 - x for x in al]):
                covered_by(seq(al2, p), p, cov)
        print(f"p={p}: generic nonzero-sum no-inverse-pair orbits={len(tot)}, covered by zipper in {seen} sampled graceful sequencings: {len(cov & tot)}; uncovered sample: {sorted(tot - cov)[:4]}", flush=True)
