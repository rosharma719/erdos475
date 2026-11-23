"""Directed search at larger p: for zero-sum A and prescribed adjacencies find a valid cycle by randomized DFS from the forced prefix.
ADJ: prefix (x,y) for every x≠y in A with x+y≠0.   TWO: prefix (x,y) and forced consecutive (u,v) (placed by DFS constraint) for random
coincidence-free two-pair patterns.  Failures are retried with a much larger node cap (they would be undetermined, not counterexamples)."""
import random, itertools, sys, time

def dfs(A, p, prefix, pairs, rng, cap):
    """cycle = prefix + remaining; forced consecutive pairs (u,v) in `pairs` must appear adjacent (in the linear order, not wrapping)."""
    A = list(A); k = len(A); n = [0]
    nxt = {u: v for u, v in pairs}; prv = {v: u for u, v in pairs}
    seq = list(prefix); used = set(seq); S = [0]
    for x in seq: S.append((S[-1] + x) % p)
    seen = set(S[:-1]) if False else set(S)       # S includes 0..; distinctness over S_0..S_{k-1}
    if len(seen) != len(S): return None
    def rec():
        n[0] += 1
        if n[0] > cap: return None
        if len(seq) == k: return True
        last = seq[-1]
        cand = [a for a in A if a not in used]
        if last in nxt: cand = [nxt[last]] if nxt[last] in cand else []
        else: cand = [a for a in cand if a not in prv]            # a forced successor can only follow its predecessor
        rng.shuffle(cand)
        for a in cand:
            t = (S[-1] + a) % p
            last_step = (len(seq) == k - 1)
            if last_step:
                if t != 0: continue                     # closing step must return to 0 (zero-sum => automatic)
                seq.append(a); used.add(a); S.append(t)
                return True
            if t in seen: continue
            seen.add(t); S.append(t); seq.append(a); used.add(a)
            r = rec()
            if r: return True
            seq.pop(); used.discard(a); S.pop(); seen.discard(t)
            if r is None: return None
        return False
    r = rec()
    return (list(seq) if r else (None if r is None else False))

def zero_sum_sets(p, k):
    for A in itertools.combinations(range(1, p), k):
        if sum(A) % p == 0: yield A

def run_adj(p, ks, cap=20000, seed=1):
    rng = random.Random(seed); tot = fail = undet = 0; t0 = time.time()
    for k in ks:
        for A in zero_sum_sets(p, k):
            for x in A:
                for y in A:
                    if x == y or (x + y) % p == 0: continue
                    tot += 1
                    r = dfs(A, p, (x, y), [], rng, cap)
                    if r is None or r is False:
                        r2 = dfs(A, p, (x, y), [], rng, cap * 50)
                        if not r2:
                            if r2 is None: undet += 1
                            else: fail += 1; print("  ADJ FAIL", p, A, (x, y), flush=True)
    print(f"ADJ p={p} sizes {list(ks)}: pairs {tot}, definite failures {fail}, undetermined {undet}, {time.time()-t0:.0f}s", flush=True)


def run_two(p, ks, samples_per_set=40, seed=2, max_sets=400, cap=20000):
    rng = random.Random(seed); tot = fail = undet = 0; t0 = time.time(); nsets = 0
    for k in ks:
        sets = list(zero_sum_sets(p, k)); rng.shuffle(sets)
        for A in sets[:max_sets]:
            nsets += 1
            for _ in range(samples_per_set):
                x, y, u, v = rng.sample(A, 4)
                s1, s2 = (x + y) % p, (u + v) % p
                rest = set(A) - {x, y, u, v}
                if 0 in (s1, s2) or (s1 + s2) % p == 0 or s1 == s2 or s1 in rest or s2 in rest: continue
                tot += 1
                r = dfs(A, p, (x, y), [(u, v)], rng, cap)
                if not r:
                    r2 = dfs(A, p, (x, y), [(u, v)], rng, cap * 50)
                    if not r2:
                        if r2 is None: undet += 1
                        else: fail += 1; print("  TWO FAIL", p, A, (x, y), (u, v), flush=True)
    print(f"TWO p={p} sizes {list(ks)}: sets {nsets}, coincidence-free patterns {tot}, definite failures {fail}, undetermined {undet}, {time.time()-t0:.0f}s", flush=True)

def _main():
    mode = sys.argv[1]
    if mode == "sampled":
        p = int(sys.argv[2]); run_sampled(p, range(int(sys.argv[3]), int(sys.argv[4]) + 1)); return
    mode = sys.argv[1]; p = int(sys.argv[2]); lo, hi = int(sys.argv[3]), int(sys.argv[4])
    (run_adj if mode == "adj" else run_two)(p, range(lo, hi + 1))


def sampled_sets(p, k, n, rng):
    out = []
    while len(out) < n:
        A = rng.sample(range(1, p), k)
        # force zero-sum by resampling one element
        for _ in range(200):
            if sum(A) % p == 0: break
            rest = [a for a in range(1, p) if a not in A[:-1]]
            A[-1] = rng.choice(rest)
        if sum(A) % p == 0 and len(set(A)) == k: out.append(tuple(sorted(A)))
    return out

def run_sampled(p, ks, nsets=12, seed=5, two=True):
    rng = random.Random(seed); t0 = time.time(); a_tot = a_bad = t_tot = t_bad = und = 0
    for k in ks:
        for A in sampled_sets(p, k, nsets, rng):
            for x in A:
                for y in A:
                    if x == y or (x + y) % p == 0: continue
                    a_tot += 1
                    if not dfs(A, p, (x, y), [], rng, 20000):
                        r2 = dfs(A, p, (x, y), [], rng, 1000000)
                        if not r2:
                            if r2 is None: und += 1
                            else: a_bad += 1; print("  ADJ FAIL", p, A, (x, y), flush=True)
            if two:
                for _ in range(60):
                    x, y, u, v = rng.sample(A, 4)
                    s1, s2 = (x + y) % p, (u + v) % p; rest = set(A) - {x, y, u, v}
                    if 0 in (s1, s2) or (s1 + s2) % p == 0 or s1 == s2 or s1 in rest or s2 in rest: continue
                    t_tot += 1
                    if not dfs(A, p, (x, y), [(u, v)], rng, 20000):
                        r2 = dfs(A, p, (x, y), [(u, v)], rng, 1000000)
                        if not r2:
                            if r2 is None: und += 1
                            else: t_bad += 1; print("  TWO FAIL", p, A, (x, y), (u, v), flush=True)
    print(f"SAMPLED p={p} sizes {list(ks)}: ADJ pairs {a_tot} fail {a_bad}; TWO patterns {t_tot} fail {t_bad}; undetermined {und}; {time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    _main()
