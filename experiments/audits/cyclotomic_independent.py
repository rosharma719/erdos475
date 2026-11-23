"""Independent audit of GPT's cyclotomic claims (written from the statements, not from GPT's scripts).
(1) Double-transversal criterion: for every prime p<=P1, every h of order m>=2, every base block (u_0..u_{d-1}) [exhaustive for small p],
    'B is a rotational sequencing of F_p^*'  <=>  both coset families are complete transversals.  Direct check vs criterion.
(2) Quadratic theorem: for every prime p<=P2 and every ordered generic triple satisfying the stated hypotheses, build B=(u,v,uh,vh,...),
    check it is a rotational sequencing, locate (u,v) and (s,w) as disjoint consecutive pairs, zipper, verify the ordering of F_p^* minus C.
    Also report what fraction of generic dilation classes the quadratic corollary covers."""
import itertools, sys

def order(x, p):
    y, k = x % p, 1
    while y != 1: y = y * x % p; k += 1
    return k

def is_seq(B, p):
    if sorted(B) != list(range(1, p)): return False
    S = list(itertools.accumulate(B, lambda s, x: (s + x) % p))
    return len(set(S)) == p - 1 and S[-1] == 0

def criterion(p, h, block):
    m = order(h, p); d = (p - 1) // m
    H = {pow(h, j, p) for j in range(m)}
    U = sum(block) % p; X = U * pow(h - 1, -1, p) % p
    P = 0; c1 = []; c2 = []
    for u in block:
        c1.append(frozenset(u * x % p for x in H))
        c2.append(frozenset((X + P) * x % p for x in H) if (X + P) % p else None)
        P = (P + u) % p
    full = set(range(1, p))
    ok1 = len(set(c1)) == d and set().union(*c1) == full
    ok2 = None not in c2 and len(set(c2)) == d and set().union(*[c for c in c2 if c]) == full
    return ok1 and ok2

def part1(p):
    bad = n = 0
    for h in range(2, p):
        m = order(h, p)
        if m < 2 or (p - 1) % m: continue
        d = (p - 1) // m
        if d > 3 and p > 13: continue
        for block in itertools.product(range(1, p), repeat=d):
            B = [(u * pow(h, j, p)) % p for j in range(m) for u in block]
            n += 1
            if is_seq(B, p) != criterion(p, h, block): bad += 1
    return n, bad

def orbit(C, p): return min(tuple(sorted(t * x % p for x in C)) for t in range(1, p))

def part2(p):
    m = (p - 1) // 2; qr = {x * x % p for x in range(1, p)}; nr = lambda z: z % p and z % p not in qr
    cov = set(); built = bad = 0
    for C in itertools.combinations(range(1, p), 3):
        if sum(C) % p == 0 or any((-x) % p in C for x in C): continue
        for u, v, w in itertools.permutations(C):
            s = (u + v) % p
            if s == 0 or s in C: continue
            q = v * pow(u, -1, p) % p; t = w * pow(s, -1, p) % p; h = q * t % p
            if not (nr(q) and nr(1 + q) and nr(t) and nr(1 + t)): continue
            if order(h, p) != m: continue
            B = [(x * pow(h, j, p)) % p for j in range(m) for x in (u, v)]
            assert is_seq(B, p), ("not a sequencing", p, C)
            n = len(B); i = 0
            assert B[0] == u and B[1] == v
            k = B.index(s); assert B[(k + 1) % n] == w and k not in (0, 1) and (k + 1) % n not in (0, 1)
            lin = [s] + B[2:]                    # contract (u,v)->s
            kk = k - 1                           # index of the original s in lin
            arc = lin[kk + 2:] + lin[:kk]        # delete original (s,w) = lin[kk], lin[kk+1]
            ps = list(itertools.accumulate(arc, lambda a, b: (a + b) % p))
            ok = sorted(arc) == sorted(set(range(1, p)) - set(C)) and len(set(ps)) == len(ps) and len(arc) == p - 4
            built += 1; bad += (not ok); cov.add(orbit(C, p))
    allc = {orbit(C, p) for C in itertools.combinations(range(1, p), 3) if sum(C) % p and all((-x) % p not in C for x in C)}
    return built, bad, len(cov), len(allc)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "part1":
        for p in (7, 11, 13): print("criterion iff p=%d: instances %d, mismatches %d" % ((p,) + part1(p)), flush=True)
        sys.exit()
    for p in (23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101):
        b, bad, c, a = part2(p)
        print(f"quadratic theorem p={p}: constructed {b}, invalid {bad}; generic classes covered by the quadratic corollary {c}/{a}", flush=True)
