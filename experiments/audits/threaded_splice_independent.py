"""Independent audit (own code) of the threaded-splicing theorems (symmetric core + arbitrary balanced remainder; asymmetric 3-step core)."""
import itertools, random
def verts(w):
    s = 0; V = [0]
    for x in w[:-1]: s += x; V.append(s)
    assert s + w[-1] == 0
    return V
def minimal_partition(steps):
    rem = list(steps); comps = []
    while rem:
        found = None
        for k in range(2, len(rem) + 1):
            for ids in itertools.combinations(range(len(rem)), k):
                if sum(rem[i] for i in ids) == 0: found = ids; break
            if found: break
        assert found, "unbalanced remainder"
        comp = [rem[i] for i in found]
        assert not any(sum(c) == 0 for q in range(1, len(comp)) for c in itertools.combinations(comp, q))   # minimal (smallest-k search guarantees it)
        comps.append(comp); rem = [x for i, x in enumerate(rem) if i not in set(found)]
    return comps
def comp_cycle(comp):
    """sign-rule cycle of a minimal zero-sum component, rotated to start at its maximum vertex -> negative-rooted; returns (steps, h, j)."""
    rem = sorted(comp, key=abs); cur = 0; walk = []
    while rem:
        cand = [x for x in rem if x < 0] if cur > 0 else [x for x in rem if x > 0]
        x = max(cand, key=abs) if cand else None
        assert x is not None
        walk.append(x); rem.remove(x); cur += x
    V = verts(walk); assert len(set(V)) == len(V)
    i = V.index(max(V)); rot = walk[i:] + walk[:i]; q = verts(rot)
    assert max(q) == 0 and len(set(q)) == len(q)
    h = -min(q); j = q.index(-h); return rot, h, j
def sym_core(S):
    S = sorted(S, reverse=True); M = S[0]
    d = [(1 if i % 2 == 0 else -1) * x for i, x in enumerate(S[1:])]
    return [M] + d + [-M] + [-x for x in reversed(d)]
def thread(base, M, comps):
    base = list(base); hs = []
    for c in comps:
        r, h, j = comp_cycle(c); hs.append(h); ix = base.index(M)
        base = base[:ix] + r[:j] + [M] + r[j:] + base[ix + 1:]
    return base, hs
def check(P, N, S, trial_kind):
    M = max(S); Ss = sorted(S, reverse=True); b = Ss[1] if len(Ss) > 1 else 0
    rem = [x for x in P if x not in S] + [-x for x in N if x not in S]
    comps = minimal_partition(rem) if rem else []
    hs = [comp_cycle(c)[1] for c in comps]; H = sum(hs)
    # Lemma 1.1 bounds
    for c, h in zip(comps, hs):
        U = max(x for x in c if x > 0); D = max(-x for x in c if x < 0); W = sum(x for x in c if x > 0)
        assert h <= min(U + D - 1, W), ("Lemma 1.1", c, h)
    if not (b + H <= M - 1): return None
    w, hs2 = thread(sym_core(S), M, comps)
    full = [x for x in P] + [-x for x in N]
    assert sorted(w) == sorted(full), "step multiset"
    V = verts(w); assert len(set(V)) == len(w), ("collision", P, N, S, w)
    assert max(V) - min(V) == M + b + H, ("range", max(V) - min(V), M + b + H)
    assert max(V) - min(V) <= max(P) + max(N) - 1
    # corollary 3.2 test
    return True
rng = random.Random(11); ok = 0; skipped = 0; cor = 0
for _ in range(6000):
    M = rng.randint(40, 160); S = {M} | set(rng.sample(range(2, 30), rng.randint(0, 3)))
    if M in set(range(2, 30)) and False: continue
    P = set(S); N = set(S)
    # random balanced remainder with values < 25, avoiding S
    for _try in range(30):
        Pr = set(rng.sample([v for v in range(1, 25) if v not in S], rng.randint(0, 5))); Nr = set(rng.sample([v for v in range(1, 25) if v not in S], rng.randint(0, 5)))
        sp, sn = sum(Pr), sum(Nr)
        if sp == sn: break
        d = abs(sp - sn); lighter = Pr if sp < sn else Nr
        if d not in S and d not in lighter and d < 40 and d > 0: lighter.add(d)
        if sum(Pr) == sum(Nr): break
    else: continue
    if sum(Pr) != sum(Nr): continue
    P |= Pr; N |= Nr
    if len(Pr) + len(Nr) > 11: continue
    res = check(sorted(P), sorted(N), S, "core")
    if res: ok += 1
    else: skipped += 1
    b = sorted(S, reverse=True)[1] if len(S) > 1 else 0
    if sum(Pr) <= M - b - 1:
        assert res, "Corollary 3.2 said OK but theorem 3.1 budget failed"; cor += 1
print(f"Theorem 3.1: {ok} random (P,N) with symmetric core + arbitrary balanced remainder satisfying b+H<=M-1: construction valid, range = M+b+H ≤ maxP+maxN−1; instances outside the budget skipped: {skipped}; Corollary 3.2 cases {cor}")
# Theorem 4.1: asymmetric 3-step core, remainder positive weight < x
ok4 = 0
for _ in range(4000):
    x = rng.randint(20, 120); y = rng.randint(1, x - 1)
    for _try in range(40):
        Pr = set(rng.sample(range(1, 18), rng.randint(0, 4))); Nr = set(rng.sample(range(1, 18), rng.randint(0, 4)))
        if Pr & {x, y} or Nr & {x + y}: continue
        sp, sn = sum(Pr), sum(Nr)
        if sp != sn:
            d = abs(sp - sn); L = Pr if sp < sn else Nr
            if d < 18 and d not in L: L.add(d)
        if sum(Pr) == sum(Nr) and sum(Pr) < x and not (Pr & {x, y}) and not (Nr & {x + y}): break
    else: continue
    P = Pr | {x, y}; N = Nr | {x + y}
    if len(P) != len(Pr) + 2 or len(N) != len(Nr) + 1: continue
    rem = list(Pr) + [-v for v in Nr]; comps = minimal_partition(rem) if rem else []
    w, hs = thread([x, y, -x - y], x, comps); V = verts(w); H = sum(hs)
    assert sorted(w) == sorted(list(P) + [-v for v in N]) and len(set(V)) == len(w)
    assert max(V) - min(V) == x + y + H <= max(P) + max(N) - 1, (P, N)
    ok4 += 1
print(f"Theorem 4.1: {ok4} random asymmetric 3-step-core instances: valid, range = x+y+H ≤ maxP+maxN−1")
print("example (GPT): P={50,7,1,5}, N={57,2,4}: ", end="")
w, hs = thread([50, 7, -57], 50, minimal_partition([1, 5, -2, -4])); V = verts(w); print(w, V, "range", max(V) - min(V))
