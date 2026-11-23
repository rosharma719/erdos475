"""Adversarial IRC tests (p-free).  IRC: finite sets P,N of positive integers, sum P = sum N: some ordering of the signed steps has distinct partial sums
S_0..S_{n-1} (S_n=0) and range <= max P + max N - 1.   Controls: P=N={5,6}: R=11 found, R=10 none; also tight-range cases must fail at R-1."""
import random, subprocess, sys, itertools, collections, os
from concurrent.futures import ThreadPoolExecutor
BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "irc_solve")

def fib(n): a, b, out = 1, 2, []; 
def fibs(m):
    a, b, out = 1, 2, []
    while len(out) < m: out.append(a); a, b = b, a + b
    return out

def balanced(rng, total, maxv, nmin, nmax):
    # random P, N sets with equal sum
    for _ in range(200):
        P = rng.sample(range(1, maxv + 1), rng.randint(nmin, nmax)); s = sum(P)
        # build N greedily to hit s
        pool = list(range(1, maxv + 1)); rng.shuffle(pool); N = []; t = 0
        for v in pool:
            if t + v <= s and len(N) < nmax: N.append(v); t += v
            if t == s: break
        if t == s and len(N) >= 1: return sorted(P), sorted(N)
    return None

def fam(rng, name, count):
    out = []
    for _ in range(count):
        if name == "sym-random":
            m = rng.randint(2, 11); S = sorted(rng.sample(range(1, 90), m)); out.append((S, S))
        elif name == "sym-2gen":                       # {a,b,a+b,...}-type
            a, b = rng.randint(1, 40), rng.randint(1, 40)
            if a == b: continue
            S = sorted({a, b, a + b}); S2 = sorted({a, b, a + b, 2 * a + b}); out.append((S, S) if rng.random() < .5 else (S2, S2))
        elif name == "geometric":
            r = rng.choice([2, 3]); m = rng.randint(3, 8); S = [r ** i for i in range(m)]; out.append((S, S))
        elif name == "fibonacci":
            m = rng.randint(3, 11); S = fibs(m); out.append((S, S))
        elif name == "z1-exceptional":                 # P={a,b,a+b,2a+b}, N={a,a+b,2a+2b}
            a, b = rng.randint(1, 30), rng.randint(1, 30)
            P = sorted({a, b, a + b, 2 * a + b}); N = sorted({a, a + b, 2 * a + 2 * b})
            if sum(P) == sum(N) and len(P) == 4 and len(N) == 3: out.append((P, N))
        elif name == "unbalanced":                     # one big step balanced by many small
            n = rng.randint(3, 10); N = sorted(rng.sample(range(1, 40), n)); out.append(([sum(N)], N))
        elif name == "two-vs-many":
            n = rng.randint(4, 11); N = sorted(rng.sample(range(1, 50), n)); s = sum(N); a = rng.randint(1, s - 1)
            if a != s - a: out.append((sorted({a, s - a}), N))
        elif name == "random-balanced":
            r = balanced(rng, 0, rng.choice([30, 60, 100]), 2, 9)
            if r: out.append(r)
        elif name == "multiples-clustered":            # values clustered near a base: near-collisions
            base = rng.randint(20, 80); m = rng.randint(3, 8); S = sorted({base + d for d in rng.sample(range(-6, 7), m)}); out.append((S, S))
    return out

def run(name, rng, count):
    inst = [(P, N) for P, N in fam(rng, name, count) if sum(P) == sum(N)]
    lines = [f"{len(P)} {len(N)} {' '.join(map(str,P))} {' '.join(map(str,N))} {max(P)+max(N)-1}" for P, N in inst]
    chunks = [lines[i::8] for i in range(8)]
    def go(c):
        if not c: return []
        r = subprocess.run([BIN], input="\n".join(c) + "\n", capture_output=True, text=True, timeout=7200); return [int(x) for x in r.stdout.split()]
    with ThreadPoolExecutor(8) as ex: outs = list(ex.map(go, chunks))
    res = [None] * len(lines)
    for i in range(8):
        for j, v in zip(range(i, len(lines), 8), outs[i]): res[j] = v
    c = collections.Counter(res)
    print(f"{name:20s} instances {len(inst):5d}: IRC found {c[1]}, NONE (counterexample candidates) {c[0]}, undetermined {c[-1]}", flush=True)
    for (P, N), v in zip(inst, res):
        if v != 1: print("   ", "NONE" if v == 0 else "UNDET", "P=", P, "N=", N, flush=True)

if __name__ == "__main__":
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1); cnt = int(sys.argv[1])
    for name in ("sym-random", "sym-2gen", "geometric", "fibonacci", "z1-exceptional", "unbalanced", "two-vs-many", "random-balanced", "multiples-clustered"):
        run(name, rng, cnt)
