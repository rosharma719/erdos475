from itertools import permutations, combinations, product
p = 11
A = {1, 2, 3, 4, 5, 8, 10}
def vertices(w):
    v = 0; seen = {0}
    for a in w[:-1]:
        v = (v + a) % p
        if v in seen: return None
        seen.add(v)
    if (v + w[-1]) % p: return None
    return seen
def cycles(B, t):
    for tail in permutations(sorted(B - {t})):
        w = (t,) + tail
        if vertices(w) is not None: yield w
def rotate(w, t):
    i = w.index(t); return w[i:] + w[:i]
def arcs(w, a, b):
    w = rotate(w, a); i = w.index(b); return w[1:i], w[i+1:]
def exchanges(w, old, new, root):
    U, V = arcs(w, *old); a, b = new
    for X, Y in ((U, V), (V, U)):
        for Xp, Yp in product(permutations(X), permutations(Y)):
            yield rotate((a,) + Xp + (b,) + Yp, root)
assert sum(A) % p == 0
B = (A - {5, 1}) | {6}; C = (A - {5, 4}) | {9}
W = list(cycles(B, 6)); assert len(W) == 44
blocked = [w for w in W if {1, 5} <= vertices(w)]; assert len(blocked) == 6
for w in blocked:
    U, V = arcs(w, 6, 4); assert U and V and {sum(U) % p, sum(V) % p} == {2, 10}
    for c in exchanges(w, (6, 4), (9, 1), 9): assert set(c) == C and vertices(c) is None
assert len(list(cycles(C, 9))) == 14
w = (9, 1, 2, 3, 10, 8); assert vertices(w) is not None and 5 not in vertices(w)
assert vertices((5, 4, 1, 2, 3, 10, 8)) is not None
splits = {(x, y) for x, y in combinations(sorted(A), 2) if (x + y) % p not in A | {0}}
assert splits == {(1, 5), (1, 8), (2, 4), (2, 5), (3, 4), (4, 5), (8, 10)}
source = {1, 8}; t = 9; w = (9, 4, 10, 5, 2, 3)
assert set(w) == (A - source) | {t} and source <= vertices(w)
tested = 0
for pair in splits:
    target = set(pair)
    if target == source: continue
    tt = sum(target) % p; common = source & target
    if common:
        z = next(iter(target - common)); y = next(iter(source - common)); old = (t, z); new = (tt, y)
    elif tt == t:
        old = tuple(sorted(target)); new = tuple(sorted(source))
    else: continue
    U, V = arcs(w, *old); assert U and V
    assert {sum(U) % p, sum(V) % p} == {-new[0] % p, -new[1] % p}
    for c in exchanges(w, old, new, tt): assert vertices(c) is None
    tested += 1
assert tested == 3
print("Both exchange counterexamples verified.")
