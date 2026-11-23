"""Which local patterns are realised by valid cycles?  For zero-sum A (5<=|A|<=p-2) enumerate ALL valid cycles (cyclic; reversal is
also valid for zero-sum sets, so we treat cycles as cyclic sequences and check both orientations).
Pattern kinds:  P1: ordered pair (x,y) consecutive;  P2: two disjoint ordered pairs (x,y),(u,v) each consecutive (zipper shape);
                P3: ordered triple consecutive.
Report every FAILURE (unrealised pattern) and test candidate explanations."""
import sys, itertools, collections
sys.path.insert(0, "experiments/exploration")
from cycle_space import valid_cycles, canon

def all_cycles(A, p):
    cs = set(canon(c) for c in valid_cycles(list(A), p))
    cs |= {canon(c[::-1]) for c in cs}
    return cs

def run(p, kmin, kmax, show=6):
    stats = collections.defaultdict(lambda: [0, 0])      # kind -> [patterns, failures]
    fails = collections.defaultdict(list)
    for k in range(kmin, kmax + 1):
        for A in itertools.combinations(range(1, p), k):
            if sum(A) % p: continue
            cyc = all_cycles(A, p)
            if not cyc: print("NO CYCLE", A); continue
            n = k
            P1, P2, P3 = set(), set(), set()
            for c in cyc:
                pairs = [(c[i], c[(i + 1) % n]) for i in range(n)]
                P1.update(pairs)
                for i in range(n):
                    P3.add((c[i], c[(i + 1) % n], c[(i + 2) % n]))
                    for j in range(i + 2, n):
                        if (j + 1) % n == i: continue
                        P2.add((pairs[i], pairs[j]))
            for x in A:
                for y in A:
                    if x != y:
                        stats["P1"][0] += 1
                        if (x, y) not in P1:
                            stats["P1"][1] += 1; fails["P1"].append((A, x, y, (x + y) % p, (x + y) % p in A))
            pairsall = [(x, y) for x in A for y in A if x != y]
            for a in range(len(pairsall)):
                for b in range(a + 1, len(pairsall)):
                    (x, y), (u, v) = pairsall[a], pairsall[b]
                    if len({x, y, u, v}) < 4: continue
                    if (x + y) % p == 0 or (u + v) % p == 0: continue
                    stats["P2"][0] += 1
                    if ((x, y), (u, v)) not in P2 and ((u, v), (x, y)) not in P2:
                        stats["P2"][1] += 1; fails["P2"].append((A, (x, y), (u, v)))
            for x, y, z in itertools.permutations(A, 3):
                if (x + y + z) % p == 0 or (x + y) % p == 0 or (y + z) % p == 0: continue
                stats["P3"][0] += 1
                if (x, y, z) not in P3:
                    stats["P3"][1] += 1; fails["P3"].append((A, x, y, z))
    print(f"p={p} sizes {kmin}..{kmax}:", {k: tuple(v) for k, v in stats.items()})
    p1 = fails["P1"]; print(" P1 failures that are NOT inverse pairs:", sum(1 for f in p1 if f[3] != 0))
    cat = collections.Counter(); unexplained = []
    for A, (x, y), (u, v) in fails["P2"]:
        s1, s2 = (x + y) % p, (u + v) % p
        rest = [a for a in A if a not in (x, y, u, v)]
        tags = []
        if (s1 + s2) % p == 0: tags.append("s1+s2=0")
        if s1 == s2: tags.append("s1=s2")
        if (s1 + s2 + sum(rest[:0])) % p == 0: pass
        if s1 in rest or s2 in rest: tags.append("s_i in rest")
        if not tags: unexplained.append((A, (x, y), (u, v)))
        cat[tuple(tags) or ("UNEXPLAINED",)] += 1
    print(" P2 failure categories:", dict(cat))
    for f in unexplained[:6]: print("   unexplained:", f)
    for kind, lst in fails.items():
        print(f" {kind} failures (first {show}):")
        for f in lst[:show]: print("   ", f)
    return fails

if __name__ == "__main__":
    p, kmin, kmax = map(int, sys.argv[1:4]); run(p, kmin, kmax)
