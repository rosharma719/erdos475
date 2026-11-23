"""Adversarial tests of EC/MC (and controls) at primes >= 41.  Positive controls:
 C1: every set has a rooted valid cycle with NO forbidden vertex (Graham sanity + solver sanity);
 C2: forbidding the first-step vertex z must report 'none' (0);
 C3: the k=4 exceptional family {z,-z,z/2,-z/2} must report 'none' when forbidding z/2.
Families: symmetric, coset unions, near-complete (zero-sum complement of size 6..10), symmetric+zero-sum triple, dense random zero-sum."""
import random, subprocess, sys, itertools, collections, os
from concurrent.futures import ThreadPoolExecutor
BIN = os.path.join(os.path.dirname(__file__), "cyc_avoid")

def prim_root(p):
    for g in range(2, p):
        if len({pow(g, i, p) for i in range(p - 1)}) == p - 1: return g

def fam_symmetric(p, rng):
    r = (p - 1) // 2; m = rng.randint(4, r); W = rng.sample(range(1, r + 1), m)
    return sorted([w for w in W] + [p - w for w in W]), "symmetric"

def fam_coset(p, rng):
    g = prim_root(p); divs = [m for m in range(2, p - 1) if (p - 1) % m == 0]
    m = rng.choice([d for d in divs if (p - 1) // d >= 2] or [2]); d = (p - 1) // m
    h = pow(g, d, p); H = [pow(h, j, p) for j in range(m)]
    t = rng.randint(1, max(1, min(d - 1, 36 // m))); idx = rng.sample(range(d), t)
    A = sorted({pow(g, i, p) * x % p for i in idx for x in H}); return A, f"cosets(m={m},t={t})"

def fam_nearcomplete(p, rng):
    while True:
        c = rng.randint(6, 10); C = rng.sample(range(1, p), c)
        if sum(C) % p == 0: return sorted(set(range(1, p)) - set(C)), f"complement(c={c})"

def fam_symtriple(p, rng):
    while True:
        r = (p - 1) // 2; m = rng.randint(3, r - 3); W = rng.sample(range(1, r + 1), m)
        S = {w for w in W} | {p - w for w in W}
        u, v = rng.sample([x for x in range(1, p) if x not in S], 2); w = (-u - v) % p
        if w and w not in S and w not in (u, v): return sorted(S | {u, v, w}), "symmetric+triple"

def fam_dense(p, rng):
    while True:
        k = rng.randint(18, p - 8); B = rng.sample(range(1, p), k)
        if sum(B) % p == 0: return sorted(B), f"dense(k={k})"

FAMS = [fam_symmetric, fam_coset, fam_nearcomplete, fam_symtriple, fam_dense]

def queries_for(p, B, rng, nroots=2, next_=6, nint=6):
    Bs = set(B); out = []
    zs = rng.sample(B, min(nroots, len(B)))
    ext = [r for r in range(1, p) if r not in Bs]
    for z in zs:
        out.append(("C1", z, 0, B)); out.append(("C2", z, z, B))
        for r in rng.sample(ext, min(next_, len(ext))): out.append(("EC", z, r, B))
        inn = [x for x in B if x != z]
        for r in rng.sample(inn, min(nint, len(inn))): out.append(("MC", z, r, B))
    return out

def run_batch(p, qs):
    lines = [f"{p} {len(B)} {' '.join(map(str, B))} 1 {z} {r}" for (_, z, r, B) in qs]
    res = subprocess.run([BIN], input="\n".join(lines) + "\n", capture_output=True, text=True, timeout=3600)
    return [int(x) for x in res.stdout.split()]

def main(p, nsets, seed):
    rng = random.Random(seed); allq = []; meta = []
    for fam in FAMS:
        for _ in range(nsets):
            B, name = fam(p, rng)
            if sum(B) % p or len(B) > 62: continue
            for q in queries_for(p, B, rng): allq.append(q); meta.append((name.split("(")[0], q[0], len(B)))
    # controls C3
    ctrl = []
    for z in rng.sample(range(1, p), 6):
        half = z * pow(2, -1, p) % p
        B = sorted({z, (-z) % p, half, (-half) % p})
        if len(B) == 4: ctrl.append(("C3", z, half, B))
    chunks = [allq[i::8] for i in range(8)]; idxs = [list(range(len(allq)))[i::8] for i in range(8)]
    with ThreadPoolExecutor(8) as ex:
        outs = list(ex.map(lambda c: run_batch(p, c), chunks))
    results = [None] * len(allq)
    for ids, o in zip(idxs, outs):
        for i, v in zip(ids, o): results[i] = v
    c3 = run_batch(p, ctrl)
    stat = collections.defaultdict(lambda: collections.Counter())
    for (fam, kind, k), v in zip(meta, results): stat[(fam, kind)][v] += 1
    print(f"=== p={p}: sets/family {nsets}, queries {len(allq)}")
    print("controls C3 (expect all 0 = unavoidable):", c3)
    for fam in sorted({m[0] for m in meta}):
        row = []
        for kind in ("C1", "C2", "EC", "MC"):
            c = stat[(fam, kind)]; row.append(f"{kind}: found {c[1]} none {c[0]} undet {c[-1]}")
        print(f"{fam:18s} " + " | ".join(row), flush=True)
    bad = [(m, q) for m, q, v in zip(meta, allq, results) if (m[1] == "C1" and v != 1) or (m[1] == "C2" and v != 0) or (m[1] in ("EC", "MC") and v == 0)]
    for m, q in bad[:10]: print("  ANOMALY", m, q[1], q[2], q[3])

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
