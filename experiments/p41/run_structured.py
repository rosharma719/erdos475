"""Adversarial STRUCTURED tests of EC/MC at larger primes (p<=127): intervals ±[1..h], annuli ±[a..b], rank-2/3 GAPs, unions of intervals,
cyclotomic coset unions.  Same positive controls (C1,C2) and exceptional-family control (C3) as run_tests.py."""
import random, subprocess, sys, itertools, collections, os
from concurrent.futures import ThreadPoolExecutor
BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cyc_avoid128")

def sym(p, xs): return sorted({x % p for x in xs if x % p} | {(-x) % p for x in xs if x % p})

def gen_sets(p, rng, kmax=42, dense=False):
    out = []; r = (p - 1) // 2
    if dense:
        kmax = p - 7
        for h in range(max(4, r // 3), r - 2): out.append((sym(p, range(1, h + 1)), f"interval(h={h})"))
        for a in range(2, r // 2, 2):
            out.append((sym(p, range(a, r + 1)), f"annulus[{a},{r}]"))
        for _ in range(10):
            a = rng.randint(2, r // 2); b = rng.randint(r // 2 + 4, r)
            out.append((sym(p, range(a, b + 1)), f"annulus[{a},{b}]"))
        return [(S, n) for S, n in out if len(S) <= kmax]
    for h in range(3, r + 1):
        if 2 * h <= kmax: out.append((sym(p, range(1, h + 1)), f"interval(h={h})"))
    for _ in range(14):
        a = rng.randint(2, r - 6); b = min(r, a + rng.randint(5, kmax // 2 - 1))
        out.append((sym(p, range(a, b + 1)), f"annulus[{a},{b}]"))
    for _ in range(14):
        A, B = rng.randint(1, 4), rng.randint(1, 4); u = rng.randint(2, p - 2)
        S = sym(p, [a + b * u for a in range(-A, A + 1) for b in range(-B, B + 1)])
        if 5 <= len(S) <= kmax: out.append((S, f"GAP2(A={A},B={B},u={u})"))
    for _ in range(8):
        A, B, C = 1, rng.randint(1, 2), rng.randint(1, 2); u, w = rng.sample(range(2, p - 1), 2)
        S = sym(p, [a + b * u + c * w for a in range(-A, A + 1) for b in range(-B, B + 1) for c in range(-C, C + 1)])
        if 5 <= len(S) <= kmax: out.append((S, f"GAP3(B={B},C={C})"))
    for _ in range(10):
        h1 = rng.randint(2, 8); c = rng.randint(h1 + 3, r - 8); h2 = rng.randint(2, 8)
        S = sym(p, list(range(1, h1 + 1)) + list(range(c, c + h2 + 1)))
        if 5 <= len(S) <= kmax: out.append((S, "two-intervals"))
    return out

def queries(p, B, rng, nroots=3):
    Bs = set(B); out = []
    ext = [r for r in range(1, p) if r not in Bs]; small = sorted(ext, key=lambda x: min(x, p - x))[:8]
    for z in rng.sample(B, min(nroots, len(B))):
        out += [("C1", z, 0, B), ("C2", z, z, B)]
        for r in set(rng.sample(small, min(3, len(small))) + rng.sample(ext, min(3, len(ext)))): out.append(("EC", z, r, B))
        inn = [x for x in B if x != z]
        for r in rng.sample(inn, min(5, len(inn))): out.append(("MC", z, r, B))
    return out

def run_batch(p, qs):
    if not qs: return []
    lines = [f"{p} {len(B)} {' '.join(map(str, B))} 1 {z} {r}" for (_, z, r, B) in qs]
    res = subprocess.run([BIN], input="\n".join(lines) + "\n", capture_output=True, text=True, timeout=7200)
    return [int(x) for x in res.stdout.split()]

def main(p, seed, dense=False):
    rng = random.Random(seed); allq = []; meta = []
    for B, name in gen_sets(p, rng, dense=dense):
        for q in queries(p, B, rng): allq.append(q); meta.append((name.split("(")[0].split("[")[0], q[0], len(B), name))
    ctrl = []
    for z in rng.sample(range(1, p), 6):
        half = z * pow(2, -1, p) % p; B = sorted({z, (-z) % p, half, (-half) % p})
        if len(B) == 4: ctrl.append(("C3", z, half, B))
    chunks = [allq[i::8] for i in range(8)]; idxs = [list(range(len(allq)))[i::8] for i in range(8)]
    with ThreadPoolExecutor(8) as ex: outs = list(ex.map(lambda c: run_batch(p, c), chunks))
    results = [None] * len(allq)
    for ids, o in zip(idxs, outs):
        for i, v in zip(ids, o): results[i] = v
    c3 = run_batch(p, ctrl); stat = collections.defaultdict(collections.Counter)
    for (fam, kind, k, nm), v in zip(meta, results): stat[(fam, kind)][v] += 1
    print(f"=== p={p}: queries {len(allq)}; C3 controls (expect 0): {c3}")
    for fam in sorted({m[0] for m in meta}):
        print(f"{fam:12s} " + " | ".join(f"{kd}: found {stat[(fam,kd)][1]} none {stat[(fam,kd)][0]} undet {stat[(fam,kd)][-1]}" for kd in ("C1", "C2", "EC", "MC")), flush=True)
    for (fam, kind, k, nm), q, v in zip(meta, allq, results):
        if (kind == "C1" and v != 1) or (kind == "C2" and v != 0) or (kind in ("EC", "MC") and v != 1):
            print("  NOTE", "UNDET" if v == -1 else "NONE", kind, nm, "k=%d" % k, "z=%d r=%d" % (q[1], q[2]))
if __name__ == "__main__": main(int(sys.argv[1]), int(sys.argv[2]), len(sys.argv) > 3)
