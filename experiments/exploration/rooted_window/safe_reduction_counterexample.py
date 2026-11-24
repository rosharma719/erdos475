from itertools import permutations, combinations
from fractions import Fraction
P = {1, 2, 5, 6}; N = {2, 3, 4, 5}; r = 2
A = P | {-n for n in N}
def valid(w, S, root):
    if not w or w[0] != root or len(w) != len(S) or set(w) != S: return False
    if root < 0: return valid(tuple(-x for x in w), {-x for x in S}, -root)
    lo, hi = min(S), max(S); v = 0; seen = {0}
    for x in w[:-1]:
        v += x
        if not lo < v <= hi: return False
        if v in seen: return False
        seen.add(v)
    return v + w[-1] == 0
def walks(S, root):
    for tail in permutations(sorted(S - {root})):
        w = (root,) + tail
        if valid(w, S, root): yield w
def lifts(w, x, y):
    def check(v):
        j = v.index(r); v = v[j:] + v[:j]; return valid(v, A, r)
    t = x + y
    if t:
        j = w.index(t)
        return any(check(w[:j] + pair + w[j+1:]) for pair in ((x, y), (y, x)))
    return any(check(w[:i] + (u,) + w[i:j] + (v,) + w[j:]) for i, j in combinations(range(len(w)), 2) for u, v in ((x, y), (y, x)))
assert sum(P) == sum(N) == 14 and max(P) + max(N) == 11 and P != N
original = list(walks(A, r))
assert set(original) == {(2, -5, 6, -2, -3, 1, 5, -4), (2, -4, 5, 1, -3, -2, 6, -5)}
results = {}
for x, y in combinations(sorted(A), 2):
    t = x + y; B = A - {x, y}
    if t in B: continue
    if t: B.add(t)
    best = Fraction(0)
    for root in sorted(B):
        W = list(walks(B, root))
        if not W: continue
        count = sum(lifts(w, x, y) for w in W)
        best = max(best, Fraction(count, len(W)))
    results[x, y] = best
assert len(results) == 17 and max(results.values()) == Fraction(1, 7)
assert sum(f > 0 for f in results.values()) == 3
print("Verified: no safe reduction; max lifting fraction = 1/7; original walks:", len(original))
