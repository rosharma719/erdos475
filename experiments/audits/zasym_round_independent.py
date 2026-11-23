"""Independent audit of GPT's Asymmetric-Zigzag round: slack theorem, tight classification, staircase family, mechanism counterexamples, two-ruler equivalence."""
import itertools, collections
def zig_valid(steps, P, N):
    if sorted(x for x in steps if x > 0) != sorted(P) or sorted(-x for x in steps if x < 0) != sorted(N): return False
    s = 0; seen = {0}
    for i, d in enumerate(steps):
        if (d > 0) != (i == 0 or s < 0): return False
        s += d
        if i < len(steps) - 1:
            if s in seen or s == 0: return False
            seen.add(s)
    return s == 0
# (1) slack theorem + tight classification over all balanced pairs P != N inside [1..V]
V = 12; subsets = [frozenset(c) for k in range(1, V + 1) for c in itertools.combinations(range(1, V + 1), k)]
by = collections.defaultdict(list)
for s in subsets: by[sum(s)].append(s)
cnt = viol = tight = tight_bad = 0
for g in by.values():
    for P in g:
        for N in g:
            if P == N: continue
            cnt += 1; m, n, M, D = len(P), len(N), max(P), max(N)
            if not (m <= D - 1 and n <= M - 1): viol += 1
            if D - m == 1 and M - n == 1:
                tight += 1
                ok = False
                for (A, B) in ((P, N), (N, P)):
                    a_max, b_max = max(A), max(B)
                    if A == frozenset(range(1, a_max + 1)) and b_max == a_max + 1:
                        miss = sorted(set(range(1, b_max + 1)) - set(B)) if False else sorted(set(range(1, b_max)) - set(B))
                        if len(miss) == 2 and sum(miss) == a_max + 1 and (b_max in B): ok = True
                if not ok: tight_bad += 1
print(f"(1) balanced asymmetric pairs in [1..{V}]: {cnt}; slack-theorem violations {viol}; pairs with exactly one hole per side {tight}; not of the claimed form {tight_bad}")
# (2) staircase family
bad = 0
for h in range(2, 130):
    for q in range(1, h // 2 + 1):
        if h < 2 * q: continue
        P = {q} | set(range(h - q + 1, h + 1)); N = set(range(h - q + 2, h + 2))
        assert sum(P) == sum(N) and P != N, (h, q)
        steps = []
        for j in range(1, q + 1): steps += [h - j + 1, -(h - j + 2)]
        steps += [q]
        if not zig_valid(steps, P, N): bad += 1
print(f"(2) staircase family: all (h,q) with 1<=q<=h/2, h<=129: invalid {bad}")
# (3) mechanism counterexamples
P, N = (1, 2, 3, 4), (2, 3, 5)
def merge_ok(sig, tau):
    i = j = X = Y = 0; steps = []; seen = {0}; k = len(sig) + len(tau)
    while len(steps) < k:
        if steps and X == Y: return None
        if X <= Y:
            if i >= len(sig): return None
            d = sig[i]; i += 1; X += d
        else:
            if j >= len(tau): return None
            d = -tau[j]; j += 1; Y += tau[j - 1]
        steps.append(d); s = X - Y
        if len(steps) < k:
            if s in seen: return None
            seen.add(s)
    return steps if X == Y else None
def relocs(seq):
    out = {tuple(seq)}
    for i in range(len(seq)):
        for j in range(len(seq)):
            v = list(seq); x = v.pop(i); v.insert(j, x); out.add(tuple(v))
    return out
sig0, tau0 = (4, 3, 2, 1), (5, 3, 2)
ok_one = [(s, tau0) for s in relocs(sig0) if merge_ok(s, tau0)] + [(sig0, t) for t in relocs(tau0) if merge_ok(sig0, t)]
print(f"(3a) P={{1,2,3,4}}, N={{2,3,5}}: single-ruler one-relocation attempts that work: {len(ok_one)} (claim 0); two-ruler relocation (4,2,1,3),(3,5,2): {merge_ok((4,2,1,3),(3,5,2))}")
w = (8, -9, 7, -1, -2, -6, 5, -7, 3, 6, -3, -8, 1, 2, 4)
print("(3b) P=[1,8], N=[1,9]\\{4,5} witness valid:", zig_valid(w, range(1, 9), [1, 2, 3, 6, 7, 8, 9]))
# (4) two-ruler equivalence on all balanced pairs in [1..7]: brute-force over orderings of steps (zigzag) vs over (sigma,tau) merges
def zig_exists_bruteforce(P, N):
    for sig in itertools.permutations(sorted(P)):
        for tau in itertools.permutations(sorted(N)):
            if merge_ok(sig, tau): return True
    return False
def zig_exists_direct(P, N):
    P, N = sorted(P), sorted(N)
    def rec(pm, nm, s, seen, steps):
        if len(steps) == len(P) + len(N): return s == 0
        pos = not steps or s < 0
        for i, v in enumerate(P if pos else N):
            if (pm if pos else nm) >> i & 1: continue
            d = v if pos else -v; t = s + d; last = len(steps) + 1 == len(P) + len(N)
            if last:
                if t == 0: return True
                continue
            if t == 0 or t in seen: continue
            if rec(pm | (1 << i) if pos else pm, nm if pos else nm | (1 << i), t, seen | {t}, steps + [d]): return True
        return False
    return rec(0, 0, 0, frozenset([0]), [])
V = 7; subsets = [frozenset(c) for k in range(1, V + 1) for c in itertools.combinations(range(1, V + 1), k)]
by = collections.defaultdict(list)
for s in subsets: by[sum(s)].append(s)
cnt = mism = 0
for g in by.values():
    for P in g:
        for N in g:
            if len(P) + len(N) > 11: continue
            cnt += 1
            a = zig_exists_bruteforce(P, N); b = zig_exists_direct(P, N)
            if a != b: mism += 1
print(f"(4) two-ruler merge existence vs direct zigzag existence on {cnt} balanced pairs in [1..7]: mismatches {mism}")
