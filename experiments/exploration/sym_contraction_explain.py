"""For zero-sum orbits at small p: find representations A = contraction of the symmetric walk W_S; report the minimal |S| and structure."""
import itertools, sys, collections
def sym_walk(S):
    S = sorted(S, reverse=True); M = S[0]
    d = [(1 if i % 2 == 0 else -1) * x for i, x in enumerate(S[1:])]
    return d + [M] + [-x for x in reversed(d)] + [-M]
def run(p):
    r = (p - 1) // 2; best = {}                      # canonical orbit -> (m, S, kept, dil)
    def canon(A): return min(tuple(sorted(t * x % p for x in A)) for t in range(1, p))
    zs = {}
    for k in range(4, p - 4):
        for A in itertools.combinations(range(1, p), k):
            if sum(A) % p == 0:
                c = canon(A)
                zs.setdefault(c, None)
    orbits = set(zs)
    # enumerate walks by increasing |S|
    for m in range(2, r + 1):
        for S in itertools.combinations(range(1, r + 1), m):
            w = sym_walk(S); n = len(w); V = [0]
            for x in w[:-1]: V.append(V[-1] + x)
            V = [v % p for v in V]
            for sub in range(1, 1 << n):
                kk = bin(sub).count("1")
                if kk < 4 or kk > p - 5: continue
                idx = [i for i in range(n) if sub >> i & 1]
                labs = [(V[idx[(j + 1) % kk]] - V[idx[j]]) % p for j in range(kk)]
                if 0 in labs or len(set(labs)) != kk: continue
                c = canon(labs)
                if c in orbits and c not in best: best[c] = (m, S, kk, n - kk)
    cnt = collections.Counter(v[0] for v in best.values()); dele = collections.Counter(v[3] for v in best.values())
    print(f"p={p}: orbits {len(orbits)}, represented {len(best)}; minimal |S| histogram {dict(sorted(cnt.items()))}; deleted-vertex count histogram {dict(sorted(dele.items()))}")
    # relation between |A| and minimal 2|S|
    byk = collections.defaultdict(list)
    for c, (m, S, kk, d) in best.items(): byk[len(c)].append(m)
    print("  per |A|: average minimal |S| (2|S| vs |A|):", {k: round(sum(v) / len(v), 2) for k, v in sorted(byk.items())})
    ex = [(c, v) for c, v in best.items() if len(c) == 6][:3]
    for c, (m, S, kk, d) in ex: print("  example A=", c, "S=", S, "kept", kk, "deleted", d)
if __name__ == "__main__":
    for p in map(int, sys.argv[1:]): run(p)
