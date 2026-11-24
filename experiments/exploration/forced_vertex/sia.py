from itertools import combinations, permutations
from collections import Counter
import random
def vertices(p, w):
    h = 0; V = [0]
    for a in w[:-1]:
        h = (h + a) % p; V.append(h)
    if (h + w[-1]) % p: return None
    if len(set(V)) != len(w): return None
    return V
def seek(p, B, t, x, strict=False):
    B = set(B); y = (t-x) % p; forbidden = B | {0}
    if strict: forbidden |= {x, y}
    E = {frozenset((u, v)) for u, v in combinations(B-{t}, 2) if (u+v) % p not in forbidden}
    if not E: return "no pair"
    def dfs(w, R, h, V, ok):
        if not R: return w if h == 0 and ok else None
        for a in sorted(R):
            z = (h+a) % p
            if z == x: continue
            if z in V and not (len(R)==1 and z==0): continue
            out = dfs(w+(a,), R-{a}, z, V|{z}, ok or frozenset((w[-1],a)) in E)
            if out: return out
        return None
    w = dfs((t,), B-{t}, t, {0,t}, False)
    if w is None: return "no walk"
    assert len(w) == len(B) and set(w) == B and w[0] == t
    V = vertices(p, w); assert V is not None and x not in V
    i = next(i for i in range(1,len(w)-1) if frozenset((w[i],w[i+1])) in E)
    u,v = w[i:i+2]; s = (u+v) % p; C = (B-{u,v}) | {s}; w2 = w[:i] + (s,) + w[i+2:]
    V2 = vertices(p, w2); assert set(w2) == C and w2[0] == t and V2 is not None and x not in V2
    z = V2[i]; assert (z+u)%p not in set(V2)|{x}
    if strict: assert x not in C and y not in C
    return "ok"
def exhaustive_cases(p):
    for k in range(3,p-2):
        for T in combinations(range(2,p),k-1):
            B = {1,*T}
            if sum(B)%p: continue
            for x in range(2,p):
                y = (1-x)%p
                if y>x and x not in B and y not in B: yield B,x
def sampled_cases(p,rng):
    for k in range(3,p-3):
        seen = set(); tries = 0
        while len(seen)<100 and tries<20000:
            tries += 1; x = rng.randrange(2,p); y = (1-x)%p
            if x==y or y==0: continue
            x,y = sorted((x,y)); pool = set(range(2,p))-{x,y}
            T = rng.sample(sorted(pool),k-2); a = (-1-sum(T))%p
            if a not in pool or a in T: continue
            B = frozenset([1,a,*T]); key = (B,x)
            if key not in seen: seen.add(key); yield B,x
expected = {7:(1,1), 11:(43,39), 13:(192,186), 17:(3366,3358), 19:(1093,1085), 23:(1555,1546)}
rng = random.Random(475)
for p in expected:
    cases = exhaustive_cases(p) if p<=17 else sampled_cases(p,rng)
    o = Counter(); s = Counter()
    for B,x in cases:
        o[seek(p,B,1,x)] += 1; r = seek(p,B,1,x,strict=True); s[r] += 1
        if r != "ok": assert len(B) in (3,4) and r == "no pair"
    assert (o["ok"], s["ok"]) == expected[p] and sum(o.values()) == o["ok"]
    print(p,dict(o),dict(s))
p = 17; C = {4,5,8,9,12,13}
for t in (5,12):
    W = [((t,)+tail, vertices(p,(t,)+tail)) for tail in permutations(C-{t})]
    W = [(w,V) for w,V in W if V is not None]; assert len(W)==14
    K = set.intersection(*(set(V) for w,V in W)); assert K == {0,t}
    bad = {(a,b) for a,b in combinations(sorted(set(range(p))-{0,t}),2) if all(a in V or b in V for w,V in W)}
    assert bad == ({(1,4),(9,13)} if t==5 else {(4,8),(13,16)})
    print("model ok", t, bad)
