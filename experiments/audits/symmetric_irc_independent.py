"""Independent audit (own implementation from the proof text) of GPT's symmetric-IRC construction and the minimal-zero-sum IRC theorem."""
import itertools, random, sys
def primes(a, b): return [q for q in range(a, b + 1) if q > 1 and all(q % d for d in range(2, int(q ** .5) + 1))]

def sym_walk(S):
    S = sorted(S, reverse=True); M = S[0]
    delta = [(1 if i % 2 == 0 else -1) * x for i, x in enumerate(S[1:])]       # b2, -b3, b4, ...
    return delta + [M] + [-x for x in reversed(delta)] + [-M]

def verts(w):
    s = 0; V = [0]
    for x in w[:-1]: s += x; V.append(s)
    return V

def check_int(S):
    w = sym_walk(S); V = verts(w)
    assert sorted(w) == sorted(list(S) + [-x for x in S]), ("multiset", S)
    assert sum(w) == 0
    assert len(set(V)) == len(w), ("distinct integer vertices", S, w, V)
    S2 = sorted(S, reverse=True); bound = S2[0] + (S2[1] if len(S2) > 1 else 0)
    assert max(V) - min(V) == (bound if len(S2) > 1 else S2[0]) , ("range", S, V)
    return w, V

# (1) exhaustive over all nonempty S ⊆ [1..16]
n = 0
for m in range(1, 17):
    for k in range(1, m + 1):
        for T in itertools.combinations(range(1, m), k - 1):
            check_int(list(T) + [m]); n += 1
print(f"(1) integer symmetric walks: all {n} nonempty subsets S of [1..16] verified (distinct vertices, range = b1+b2)")

# (2) all symmetric subsets of F_p^* for primes <= 31 (every subset of positive reps), checked MOD p directly (valid cyclic ordering)
def valid_mod(w, p):
    s = 0; seen = {0}
    for x in w[:-1]:
        s = (s + x) % p
        if s in seen: return False
        seen.add(s)
    return (s + w[-1]) % p == 0
tot = bad = 0
for p in primes(3, 31):
    r = (p - 1) // 2
    for mask in range(1, 1 << r):
        S = [i + 1 for i in range(r) if mask >> i & 1]
        w = sym_walk(S); tot += 1
        if not valid_mod(w, p) or sorted(x % p for x in w) != sorted({x % p for x in S} | {(-x) % p for x in S}): bad += 1
print(f"(2) every symmetric subset of F_p^* for all primes p<=31 (including the full group): {tot} sets, invalid {bad}")

# (3) random symmetric sets, primes up to 997, mod p
rng = random.Random(9); tot = bad = 0
for _ in range(20000):
    p = rng.choice(primes(41, 997)); r = (p - 1) // 2; m = rng.randint(1, min(r, 60)); S = rng.sample(range(1, r + 1), m)
    w = sym_walk(S); tot += 1
    if not valid_mod(w, p): bad += 1
print(f"(3) random symmetric sets, primes 41..997: {tot}, invalid {bad}")

# (4) minimal zero-sum IRC theorem: P,N sets with equal sums, signed collection has no proper nonempty zero-sum subcollection
def minimal(P, N):
    a = list(P) + [-q for q in N]; n = len(a)
    for mask in range(1, (1 << n) - 1):
        if sum(a[i] for i in range(n) if mask >> i & 1) == 0: return False
    return True
def sign_rule(P, N):
    pos, neg = sorted(P, reverse=True), sorted(N, reverse=True); cur = 0; steps = []; V = [0]
    while pos or neg:
        if cur >= 0 and not (cur == 0 and steps):
            if cur == 0: x = pos.pop(0)
            else: x = -neg.pop(0)
        elif cur < 0: x = pos.pop(0)
        else: x = -neg.pop(0)
        steps.append(x); cur += x; V.append(cur)
    return steps, V
cnt = bad = 0
for V in (8, 9, 10, 11, 12):
    allsets = [frozenset(c) for k in range(1, V + 1) for c in itertools.combinations(range(1, V + 1), k)]
    by = {}
    for s in allsets: by.setdefault(sum(s), []).append(s)
    for g in by.values():
        for P in g:
            for N in g:
                if len(P) + len(N) > 11 or not minimal(P, N): continue
                steps, Vs = sign_rule(P, N); cnt += 1
                ok = (sum(steps) == 0 and len(set(Vs[:-1])) == len(steps) and max(Vs[:-1]) - min(Vs[:-1]) <= max(P) + max(N) - 1)
                bad += not ok
print(f"(4) minimal zero-sum signed collections (values<=12): {cnt} pairs (P,N); sign-rule walk valid with range <= maxP+maxN-1: failures {bad}")
