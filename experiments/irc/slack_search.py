"""Hill-climb on integer instances to MINIMISE slack = (maxP+maxN-1) - (minimum achievable range).  slack<0 would refute IRC; slack=0 are the tight cases."""
import random, subprocess, sys, os, collections
BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "irc_solve")
proc = subprocess.Popen([BIN], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
def feasible(P, N, R):
    proc.stdin.write(f"{len(P)} {len(N)} {' '.join(map(str,P))} {' '.join(map(str,N))} {R}\n"); proc.stdin.flush()
    return int(proc.stdout.readline())
def slack(P, N, maxdrop=8):
    bound = max(P) + max(N) - 1; v = feasible(P, N, bound)
    if v != 1: return -1 if v == 0 else None            # -1: IRC violated; None: undetermined
    s = 0
    while s < maxdrop:
        v = feasible(P, N, bound - s - 1)
        if v == 1: s += 1
        elif v == 0: break
        else: return None
    return s
def mutate(P, N, rng, V):
    P, N = set(P), set(N)
    for _ in range(100):
        which = rng.choice([P, N]); other = N if which is P else P
        r = rng.random()
        if r < .4 and len(which) > 1: which.discard(rng.choice(sorted(which)))
        elif r < .8: which.add(rng.randint(1, V))
        else:
            x = rng.choice(sorted(which)); which.discard(x); which.add(max(1, x + rng.randint(-3, 3)))
        # rebalance by adding one element to the lighter side if possible
        sp, sn = sum(P), sum(N)
        if sp != sn:
            d = abs(sp - sn); light = P if sp < sn else N
            if 1 <= d <= V and d not in light: light.add(d)
        if P and N and sum(P) == sum(N) and 2 <= len(P) + len(N) <= 11: return sorted(P), sorted(N)
        P, N = set(P), set(N)
    return None
def climb(rng, V, iters):
    P = sorted(rng.sample(range(1, V), rng.randint(2, 4))); N = P[:]
    cur = slack(P, N)
    best = (cur if cur is not None else 99, P, N)
    for _ in range(iters):
        m = mutate(P, N, rng, V)
        if not m: continue
        s = slack(*m)
        if s is None: print("UNDET", m, flush=True); continue
        if s < 0: print("!!! IRC VIOLATION", m, flush=True); return ("VIOLATION", m)
        if s <= (cur if cur is not None else 99): P, N, cur = m[0], m[1], s
        if s < best[0]: best = (s, m[0], m[1])
    return best
if __name__ == "__main__":
    rng = random.Random(int(sys.argv[2])); V = int(sys.argv[1]); res = collections.Counter(); ex = {}
    for t in range(int(sys.argv[3])):
        b = climb(rng, V, 150)
        if b[0] == "VIOLATION": break
        res[b[0]] += 1; ex.setdefault(b[0], (b[1], b[2]))
    print(f"V<={V}: best slack reached over restarts: {dict(sorted(res.items()))}; examples {ex}")
