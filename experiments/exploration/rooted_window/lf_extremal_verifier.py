from itertools import combinations
from fractions import Fraction
def excluded(A, r):
    if r < 0: return excluded({-x for x in A}, -r)
    P = sorted(x for x in A if x > 0); N = sorted(-x for x in A if x < 0)
    if P == N and len(P) == 2: return r == P[0]
    if len(P) == len(N) == 3:
        c = P[-1]
        if P == N and r != c: return True
        if c == N[-1] and sum(P[:2]) == c and sum(N[:2]) == c and r < N[0]: return True
    return P == N == [r, 2*r, 3*r, 4*r, 5*r]
def valid(w, A, r):
    if len(w) != len(A) or set(w) != A or w[0] != r: return False
    if r < 0: return valid(tuple(-x for x in w), {-x for x in A}, -r)
    h = 0; seen = {0}
    for x in w[:-1]:
        h += x
        if h in seen or not min(A) < h <= max(A): return False
        seen.add(h)
    return h + w[-1] == 0
def walks(A, r):
    if r < 0:
        for w in walks({-x for x in A}, -r): yield tuple(-x for x in w)
        return
    lo, hi = min(A), max(A)
    def dfs(w, R, h, seen):
        if len(R) == 1:
            x = next(iter(R))
            if h + x == 0: yield w + (x,)
            return
        for x in R:
            v = h + x
            if lo < v <= hi and v not in seen: yield from dfs(w + (x,), R - {x}, v, seen | {v})
    yield from dfs((r,), A - {r}, r, {0, r})
def audit(A, r):
    best = Fraction(0); choice = None
    for x, y in combinations(sorted(A), 2):
        t = x + y; B = A - {x, y}
        if t in B: continue
        if t: B.add(t)
        if len(B) < 2: continue
        roots = sorted(B) if (not t and r in (x, y)) else [t if r in (x, y) else r]
        def check(w):
            j = w.index(r); return valid(w[j:] + w[:j], A, r)
        def lifts(w):
            if t:
                j = w.index(t); return any(check(w[:j] + pair + w[j+1:]) for pair in ((x, y), (y, x)))
            return any(check(w[:i] + (u,) + w[i:j] + (v,) + w[j:]) for i, j in combinations(range(len(w)), 2) for u, v in ((x, y), (y, x)))
        for s in roots:
            if excluded(B, s): continue
            num = den = 0
            for w in walks(B, s):
                den += 1; num += lifts(w)
            if den:
                f = Fraction(num, den)
                if f > best: best = f; choice = (x, y, s, num, den)
    return best, choice
tests = [({-5,-4,-3,-2,1,2,5,6}, 2, Fraction(1,7)), ({-9,-8,-6,-2,-1,7,9,10}, 7, Fraction(5,9)),
         ({-12,-11,-9,-7,2,4,6,8,9,10}, 9, Fraction(59,76)), (set(range(-4,5))-{0}, 2, Fraction(1,37)),
         (set(range(-7,8))-{0}, 1, Fraction(16,183))]
for A, r, e in tests:
    res, cert = audit(A, r); assert res == e, (A, r, res, e); print(sorted(A), r, res, cert)
print("all 5 verified")
