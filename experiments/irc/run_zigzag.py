import random, subprocess, itertools, collections, sys, os
from concurrent.futures import ThreadPoolExecutor
BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zigzag")
def run(insts):
    lines = [f"{len(P)} {len(N)} {' '.join(map(str,P))} {' '.join(map(str,N))}" for P, N in insts]
    chunks = [lines[i::8] for i in range(8)]
    def go(c):
        if not c: return []
        r = subprocess.run([BIN], input="\n".join(c) + "\n", capture_output=True, text=True, timeout=7200); return [int(x) for x in r.stdout.split()]
    with ThreadPoolExecutor(8) as ex: outs = list(ex.map(go, chunks))
    res = [None] * len(lines)
    for i in range(8):
        for j, v in zip(range(i, len(lines), 8), outs[i]): res[j] = v
    return res
def fam_merge(h, both):
    out = []
    full = list(range(1, h + 1))
    for a, b in itertools.combinations(full, 2):
        s = a + b
        if s in full: continue
        N = sorted(set(full) - {a, b} | {s})
        out.append((full, N))
        if both: out.append((N, full))
    return out
def fam_two_merge(h, rng, count):
    out = []; full = list(range(1, h + 1))
    for _ in range(count):
        a, b, c, d = rng.sample(full, 4)
        s1, s2 = a + b, c + d
        if s1 in full or s2 in full or s1 == s2: continue
        N = sorted(set(full) - {a, b, c, d} | {s1, s2}); out.append((full, N)); out.append((N, full))
    return out
def fam_random(V, rng, count):
    out = []
    while len(out) < count:
        P = sorted(rng.sample(range(1, V + 1), rng.randint(V // 2, V - 1)))
        N = sorted(rng.sample(range(1, V + 1), rng.randint(V // 2, V - 1)))
        if sum(P) == sum(N) and P != N: out.append((P, N)); continue
        # rebalance by swapping one element
        d = sum(P) - sum(N)
        for x in range(1, V + 1):
            if x in N: continue
            for y in N:
                if y + d == x and x not in N - {y} if False else False: pass
        # simple fix: replace an element of the heavier side by one lighter if possible
        heavy, light = (P, N) if d > 0 else (N, P); d = abs(d)
        cand = [(x, x - d) for x in heavy if x - d >= 1 and (x - d) not in heavy]
        if cand:
            x, y = rng.choice(cand); H2 = sorted(set(heavy) - {x} | {y})
            P2, N2 = (H2, light) if heavy is P else (P, H2)
            if sum(P2) == sum(N2) and P2 != N2: out.append((P2, N2))
    return out
if __name__ == "__main__":
    rng = random.Random(5); total = collections.Counter()
    for h in range(6, 15):
        insts = fam_merge(h, True)
        res = run(insts); c = collections.Counter(res); total.update(c)
        bad = [i for i, v in zip(insts, res) if v != 1]
        print(f"merge family h={h}: {len(insts)} pairs; zigzag found {c[1]}, NONE {c[0]}, undetermined {c[-1]}", flush=True)
        for P, N in bad[:3]: print("    ", "NONE/UNDET", "P=", P, "N=", N, flush=True)
    for h in (8, 10, 12):
        insts = fam_two_merge(h, rng, 150); res = run(insts); c = collections.Counter(res); total.update(c)
        print(f"two-merge family h={h}: {len(insts)} pairs; found {c[1]}, NONE {c[0]}, undet {c[-1]}", flush=True)
        for (P, N), v in zip(insts, res):
            if v != 1: print("    ", v, "P=", P, "N=", N, flush=True)
    for V in (12, 14, 16):
        insts = fam_random(V, rng, 400); res = run(insts); c = collections.Counter(res); total.update(c)
        print(f"random dense pairs V={V}: {len(insts)}; found {c[1]}, NONE {c[0]}, undet {c[-1]}", flush=True)
        for (P, N), v in zip(insts, res):
            if v != 1: print("    ", v, "P=", P, "N=", N, flush=True)
    print("TOTAL", dict(total))
