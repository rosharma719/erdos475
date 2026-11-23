"""Independent audit (own code) of GPT's c=5 / geometric-swap / coset-escape note."""
import itertools, sys, random
from math import comb, gcd

def primes(a, b): return [q for q in range(a, b + 1) if q > 1 and all(q % d for d in range(2, int(q ** .5) + 1))]
def order(h, p):
    y, k = h % p, 1
    while y != 1: y = y * h % p; k += 1
    return k
def walecki_B(p):
    r = (p - 1) // 2; a, lo, hi, tl = [], 1, r, True
    while lo <= hi:
        if tl: a.append(lo); lo += 1
        else: a.append(hi); hi -= 1
        tl = not tl
    d = [a[i + 1] - a[i] for i in range(r - 1)]
    return [x % p for x in d + [r] + [-x for x in reversed(d)] + [-r]], r

def part_a():
    for p in (11, 13, 17, 19, 23, 29, 31):
        Z = sum(1 for C in itertools.combinations(range(1, p), 5) if sum(C) % p == 0)
        formula = (comb(p - 1, 5) - (p - 1)) // p
        orbs = len({min(tuple(sorted(t * x % p for x in C)) for t in range(1, p)) for C in itertools.combinations(range(1, p), 5) if sum(C) % p == 0})
        bur = (formula + (4 * (p - 1) // 5 if (p - 1) % 5 == 0 else 0)) / (p - 1)
        print(f"(a) p={p}: zero-sum 5-sets {Z} vs formula {formula}; orbits {orbs} vs Burnside {bur}", flush=True)
    p = 47; print(f"(a) p=47 formula orbits: {((comb(46,5)-46)//47 + 4*46//5*0)/46:.2f} (no 5|46)")

def part_b():
    for p in (19, 23, 29, 31, 37, 41, 43, 47):
        B, r = walecki_B(p); n = p - 1
        pairs = {(B[i] + B[(i + 1) % n]) % p for i in range(n)}
        want = {1 % p, (-1) % p, 2, (r - 1) % p, (r + 1) % p}
        # blocks of 4j+1 consecutive steps inside one half sum to the middle label
        ok = True
        for j in (1, 2):
            L = 4 * j + 1
            for i in range(0, r - 1 - L + 1):
                if sum(B[i:i + L]) % p != B[i + 2 * j]: ok = False
        print(f"(b) p={p}: consecutive-pair sums {sorted(pairs)} ⊆ {{±1,2,r±1}}: {pairs <= want}; 4j+1-block-sum=middle: {ok}", flush=True)
    # isolated deletions <=4 in valid c=5 contractions (p=29)
    p = 29; B, r = walecki_B(p); n = p - 1
    V = [0]
    for x in B[:-1]: V.append((V[-1] + x) % p)
    mx = 0
    for D in itertools.combinations(range(n), 5):
        ds = set(D); iso = sum(1 for d in D if (d - 1) % n not in ds and (d + 1) % n not in ds)
        keep = [V[i] for i in range(n) if i not in ds]
        labs = [(keep[(j + 1) % len(keep)] - keep[j]) % p for j in range(len(keep))]
        if len(set(labs)) == len(labs): mx = max(mx, iso)
    print(f"(b) p=29: max #isolated deleted vertices over valid 5-deletions = {mx} (claimed <=4)")
    for p in (19, 23, 29, 31, 37, 41, 43, 47):
        B, r = walecki_B(p); n = p - 1
        V = [0]
        for x in B[:-1]: V.append((V[-1] + x) % p)
        cnt = 0
        for D in itertools.combinations(range(n), 5):
            ds = set(D); keep = [V[i] for i in range(n) if i not in ds]
            labs = [(keep[(j + 1) % len(keep)] - keep[j]) % p for j in range(len(keep))]
            cnt += len(set(labs)) == len(labs)
        print(f"(b) p={p}: valid 5-deletions {cnt}, 15p-63 = {15*p-63}", flush=True)

def part_c():
    # geometric swap theorem: all non-root adjacent swaps valid iff q(h)=h^2-h+1 not in H
    bad = tot = 0
    for p in primes(11, 61):
        for k in range(3, p):
            if (p - 1) % k: continue
            for h in range(2, p):
                if order(h, p) != k: continue
                H = {pow(h, j, p) for j in range(k)}
                z = 1; steps = [pow(h, j, p) for j in range(k)]
                def valid(st):
                    s = 0; seen = {0}
                    for a in st[:-1]:
                        s = (s + a) % p
                        if s in seen: return False
                        seen.add(s)
                    return True
                assert valid(steps)
                allok = all(valid(steps[:i] + [steps[i + 1], steps[i]] + steps[i + 2:]) for i in range(1, k - 1))
                allbad = not any(valid(steps[:i] + [steps[i + 1], steps[i]] + steps[i + 2:]) for i in range(1, k - 1))
                qin = (h * h - h + 1) % p in H
                tot += 1
                if qin and not allbad or (not qin) and not allok: bad += 1
    print(f"(c) geometric swap theorem: (p,h) cases {tot}, violations {bad}", flush=True)

def cyclo(k):
    import sympy
    x = sympy.symbols('x'); return sympy.Poly(sympy.cyclotomic_poly(k, x), x), x

def part_d():
    import sympy
    gs = {}
    for k in range(5, 17):
        Phi, x = cyclo(k)
        q = sympy.Poly((x * x - x + 1) ** k - 1, x)
        R = q.rem(Phi)
        g = 0
        for c in R.all_coeffs(): g = gcd(g, int(c))
        gs[k] = abs(g)
    print("(d) g_k:", gs, "(claimed 5,1,14,24,9,11,11,39,39,4,2,136)", flush=True)
    viol = 0; tot = 0
    for k in range(5, 17):
        for p in primes(5, 700):
            if (p - 1) % k: continue
            exists = False
            for h in range(2, p):
                if order(h, p) != k: continue
                H = {pow(h, j, p) for j in range(k)}
                if (h * h - h + 1) % p not in H: exists = True; break
            tot += 1
            if exists != (gs[k] % p != 0): viol += 1; print("   mismatch", k, p, exists, gs[k] % p)
    print(f"(d) generator-criterion equivalence cases {tot}, violations {viol}", flush=True)

def part_e(trials=3000, seed=1):
    rng = random.Random(seed); built = ok = bad = 0
    for _ in range(trials):
        p = rng.choice(primes(23, 97)); 
        divs = [m for m in range(2, p) if (p - 1) % m == 0 and 3 <= m and (p - 1) // m >= 2]
        if not divs: continue
        m = rng.choice(divs); d = (p - 1) // m
        h = next((x for x in rng.sample(range(2, p), p - 2) if order(x, p) == m), None)
        if h is None: continue
        H = {pow(h, j, p) for j in range(m)}
        reps = {}; 
        for x in range(1, p):
            key = min(x * y % p for y in H); reps.setdefault(key, []).append(x)
        cosets = list(reps.keys()); t = rng.randint(1, d)
        chosen = rng.sample(cosets, t); U = [rng.choice([x for x in range(1, p) if min(x * y % p for y in H) == c]) for c in chosen]
        rng.shuffle(U)
        T = sum(U) % p; X = T * pow(h - 1, -1, p) % p
        P = [0]
        for u in U: P.append((P[-1] + u) % p)
        v = [(X + P[i]) % p for i in range(t)]
        if 0 in v or len({min(vi * y % p for y in H) for vi in v}) != t: continue
        W = {vi * y % p for vi in v for y in H}
        w = [(X + P[i] + U[i + 1]) % p for i in range(t - 1)] + [(pow(h, -1, p) * (X + P[t - 1]) + U[0]) % p]
        if any(wi in W for wi in w): continue
        steps = [u * pow(h, j, p) % p for j in range(m) for u in U]
        s = 0; V = [0]
        for a in steps[:-1]: s = (s + a) % p; V.append(s)
        assert len(set(V)) == len(steps) and (s + steps[-1]) % p == 0, "geometric block not a valid cycle?!"
        built += 1
        # every vertex except 0 and the first step's vertex is removable by one adjacent swap (non-root)
        removable = set()
        for i in range(1, len(steps) - 1):
            st = steps[:i] + [steps[i + 1], steps[i]] + steps[i + 2:]
            s2 = 0; V2 = [0]
            for a in st[:-1]: s2 = (s2 + a) % p; V2.append(s2)
            if len(set(V2)) == len(st): removable |= set(V) - set(V2)
        need = set(V) - {0, steps[0] % p}
        if need <= removable: ok += 1
        else: bad += 1; print("   coset-escape counterexample:", p, h, U)
    print(f"(e) coset-escape: random instances satisfying the hypotheses {built}; all swaps/vertices OK {ok}; violations {bad}", flush=True)

def part_f():
    p = 47; B, r = walecki_B(p); n = p - 1
    V = [0]
    for x in B[:-1]: V.append((V[-1] + x) % p)
    cov = set()
    for D in itertools.combinations(range(n), 5):
        ds = set(D); keep = [V[i] for i in range(n) if i not in ds]
        labs = [(keep[(j + 1) % len(keep)] - keep[j]) % p for j in range(len(keep))]
        if len(set(labs)) == len(labs):
            cov.add(min(tuple(sorted(t * x % p for x in set(range(1, p)) - set(labs))) for t in range(1, p)))
    total = ((comb(46, 5) - 46) // 47) // 46
    print(f"(f) p=47: Walecki alone covers {len(cov)} zero-sum 5-set orbits of {total} (GPT: Walecki+geometric+index2 cover 283/634)", flush=True)

if __name__ == "__main__":
    for part in sys.argv[1:]: globals()["part_" + part]()
