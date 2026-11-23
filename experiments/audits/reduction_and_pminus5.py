"""Independent audit (own code) of: (A) one-element balancing lemma + transfer, (B) zero-sum 4-complement construction (Walecki 2+2+3)."""
import itertools, sys
from collections import Counter

def vp(seq, p):
    s = 0; seen = set()
    for x in seq:
        s = (s + x) % p
        if s in seen: return False
        seen.add(s)
    return True

# ---------- (A) ----------
def audit_A(p, kmax_valid=None):
    miss = 0; n = 0; transfer_checked = 0
    for k in range(2, p - 2):
        for A in itertools.combinations(range(1, p), k):
            s = sum(A) % p
            if s == 0: continue
            Aset = set(A); n += 1
            cand = [(x, (x - s) % p) for x in A if (x - s) % p and (x - s) % p not in Aset]
            if not cand: miss += 1
    return n, miss

def valid_cycle_zero_sum(A, p):
    A = list(A); k = len(A)
    def rec(seq, used, s, seen):
        if len(seq) == k: return list(seq)
        for i, a in enumerate(A):
            if used >> i & 1: continue
            t = (s + a) % p
            last = (len(seq) == k - 1)
            if last:
                if t == 0: return list(seq) + [a]
                continue
            if t in seen: continue
            seen.add(t); seq.append(a)
            r = rec(seq, used | 1 << i, t, seen)
            if r: return r
            seq.pop(); seen.discard(t)
        return None
    return rec([], 0, 0, {0})

def transfer_check(p):
    bad = n = 0
    for k in range(2, p - 2):
        for A in itertools.combinations(range(1, p), k):
            s = sum(A) % p
            if s == 0: continue
            x, y = next((x, (x - s) % p) for x in A if (x - s) % p and (x - s) % p not in set(A))
            A2 = (set(A) - {x}) | {y}
            cyc = valid_cycle_zero_sum(A2, p)
            i = cyc.index(y); cyc = cyc[i:] + cyc[:i]
            order = [x] + cyc[1:]
            n += 1
            if sorted(order) != sorted(A) or not vp(order, p): bad += 1
    return n, bad

# ---------- (B) ----------
def walecki(r):
    a, lo, hi, tl = [], 1, r, True
    while lo <= hi:
        if tl: a.append(lo); lo += 1
        else: a.append(hi); hi -= 1
        tl = not tl
    return a

def construct4(p, C):
    r = (p - 1) // 2; n = p - 1
    al = walecki(r); d = [al[i + 1] - al[i] for i in range(r - 1)]
    B = [x % p for x in d + [r] + [-x for x in reversed(d)] + [-r]]
    q0 = r - 2                                        # 0-indexed start of Q=(δ_{r-1}, r, -δ_{r-1})
    Qidx = {q0, q0 + 1, q0 + 2}
    L = sorted(C)
    for i in range(1, 4):
        X = {L[0], L[i]}; Y = set(C) - X
        for plus, minus in ((X, Y), (Y, X)):
            s = sum(plus) % p
            if s == 0: continue
            lam = pow(s, -1, p)
            P = {lam * x % p for x in plus}; M = {lam * x % p for x in minus}
            ips = [j for j in range(n) if {B[j], B[(j + 1) % n]} == P and not ({j, (j + 1) % n} & Qidx)]
            ims = [j for j in range(n) if {B[j], B[(j + 1) % n]} == M and not ({j, (j + 1) % n} & Qidx)]
            for a in ips:
                for c in ims:
                    if {a, (a + 1) % n} & {c, (c + 1) % n}: continue
                    out = []; j = q0; seen = 0
                    while seen < n:
                        if j == a: out.append(1); j = (j + 2) % n; seen += 2
                        elif j == c: out.append(p - 1); j = (j + 2) % n; seen += 2
                        elif j == q0: out.append(r); j = (j + 3) % n; seen += 3
                        else: out.append(B[j]); j = (j + 1) % n; seen += 1
                    inv = pow(lam, -1, p)
                    res = [inv * x % p for x in out]
                    if len(res) == p - 5 and sorted(res) == sorted(set(range(1, p)) - set(C)) and vp(res, p):
                        return res
    return None

def is_R(x, y, j, p): return y % p == (-j * x) % p or x % p == (-j * y) % p

def selection_ok(C, p):
    L = sorted(C)
    for i in range(1, 4):
        X = [L[0], L[i]]; Y = [z for z in L if z not in X]
        sx = sum(X) % p
        if sx == 0: continue
        if is_R(*X, 2, p) or is_R(*Y, 2, p): continue
        if is_R(*X, 3, p) and is_R(*Y, 3, p): continue
        return True
    return False

def primes(a, b): return [q for q in range(a, b + 1) if all(q % d for d in range(2, int(q ** .5) + 1))]

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "A":
        for p in (5, 7, 11, 13, 17, 19, 23):
            n, miss = audit_A(p); print(f"A: lemma p={p}: nonzero-sum sets 2<=k<=p-3: {n}, with NO balancing replacement: {miss}", flush=True)
        for p in (7, 11, 13):
            n, bad = transfer_check(p); print(f"A: transfer p={p}: {n} nonzero-sum sets, orderings built {n-bad}, invalid {bad}", flush=True)
    else:
        for p in primes(11, int(sys.argv[2])):
            tot = fail = selfail = 0
            for C in itertools.combinations(range(1, p), 4):
                if sum(C) % p: continue
                tot += 1
                if construct4(p, C) is None: fail += 1
                if not selection_ok(C, p): selfail += 1
            print(f"B: p={p}: zero-sum 4-complements {tot}, construction failures {fail}, selection-lemma conditions unsatisfiable {selfail}", flush=True)
