"""Does maximising TRUE adjacent-swap mobility force avoidance?  Search all zero-sum sets of sizes 5,6 (sampled) at p=41,43,47 for (B,z,r) where EVERY mobility-maximising
rooted cycle visits r although some valid rooted cycle avoids r. True mobility = number of non-root adjacent swaps whose swapped cycle is valid (swap performed and checked)."""
import itertools, random, sys
def verts(a, p):
    s = 0; V = [0]
    for x in a[:-1]: s = (s + x) % p; V.append(s)
    return V
def mob(a, p):
    k = len(a); g = 0
    for i in range(2, k):
        b = list(a); b[i - 1], b[i] = b[i], b[i - 1]; g += len(set(verts(b, p))) == k
    return g
def run(p, k, nsets, seed):
    rng = random.Random(seed); found = []; tested = 0
    while tested < nsets:
        B = rng.sample(range(1, p), k)
        if sum(B) % p: continue
        tested += 1
        for z in B:
            cyc = []
            for suf in itertools.permutations([x for x in B if x != z]):
                a = (z,) + suf
                if sum(a) % p == 0:
                    V = verts(a, p)
                    if len(set(V)) == k: cyc.append((a, V, mob(a, p)))
            if not cyc: continue
            best = max(c[2] for c in cyc); opt = [c for c in cyc if c[2] == best]
            for r in range(1, p):
                if r == z: continue
                if all(r in c[1] for c in opt) and any(r not in c[1] for c in cyc):
                    found.append((sorted(B), z, r, best, len(opt), len(cyc)))
    return tested, found
for p, k, n in ((41, 5, 3000), (41, 6, 800), (43, 5, 3000), (47, 5, 3000), (47, 6, 600)):
    t, f = run(p, k, n, p * 10 + k)
    print(f"p={p} k={k}: zero-sum sets tested {t}; (B,z,r) where ALL true-mobility maximisers visit r but an avoider exists: {len(f)}", f[:2], flush=True)
