"""Connectivity of the valid-cycle space of dense zero-sum sets under local moves.
Question (LSA1): are valid cycles of A connected by moves that stay valid, and how far is any cycle
from one where a given pair (a1,a2) is adjacent?  Moves: adjacent swap, segment reversal, single relocation."""
import sys, itertools, collections

def valid_cycles(A, p):
    A = sorted(A); k = len(A); m = A[0]; out = []
    def rec(seq, used, s, seen):
        if len(seq) == k:
            out.append(tuple(seq)); return
        for i, a in enumerate(A):
            if used >> i & 1 or (not seq and a != m): continue
            t = (s + a) % p
            if t in seen and not (len(seq) == k - 1 and t == 0): continue
            if t in seen: continue
            seen.add(t); seq.append(a)
            rec(seq, used | 1 << i, t, seen)
            seq.pop(); seen.discard(t)
    rec([], 0, 0, set())
    return out

def canon(c):
    i = c.index(min(c)); return c[i:] + c[:i]

def neighbors(c):
    k = len(c)
    for i in range(k):
        for j in range(i + 2, k + 1):                       # reversal of c[i:j]
            yield c[:i] + c[i:j][::-1] + c[j:]
        x = c[i]; r = c[:i] + c[i + 1:]
        for j in range(k):                                  # relocation
            if j != i: yield r[:j] + (x,) + r[j:]

def analyse(p, A):
    cyc = set(canon(c) for c in valid_cycles(A, p))
    idx = {c: n for n, c in enumerate(cyc)}; cl = list(cyc)
    par = list(range(len(cl)))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for c in cl:
        for d in neighbors(c):
            d = canon(d)
            if d in idx: par[f(idx[c])] = f(idx[d])
    comps = collections.Counter(f(i) for i in range(len(cl)))
    print(f"p={p} |A|={len(A)} valid cycles={len(cl)} components={len(comps)} largest={max(comps.values())}")
    # adjacency coverage per admissible merge pair, and per component
    Aset = set(A); bad_pairs = 0; pairs = 0
    for a1, a2 in itertools.combinations(A, 2):
        z = (a1 + a2) % p
        if z == 0 or z in Aset: continue
        pairs += 1
        adj_comps = set()
        for i, c in enumerate(cl):
            k = len(c)
            if any({c[t], c[(t + 1) % k]} == {a1, a2} for t in range(k)): adj_comps.add(f(i))
        if not adj_comps: bad_pairs += 1
        elif len(comps) > 1 and len(adj_comps) < len(comps):
            print(f"  pair ({a1},{a2}): adjacency realised in {len(adj_comps)}/{len(comps)} components")
    print(f"  admissible pairs={pairs}, pairs never adjacent in any valid cycle={bad_pairs}")

if __name__ == "__main__":
    for p in map(int, sys.argv[1:]):
        analyse(p, [x for x in range(2, p - 1)])           # Z_p^* \ {±1}
