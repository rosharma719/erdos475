"""Independent audit of GPT's quantitative flexibility note (own code)."""
import itertools, sys, random, math
from collections import Counter

def verts(a, p):
    s = 0; V = [0]
    for x in a[:-1]: s = (s + x) % p; V.append(s)
    return V
def valid(a, p):
    if sum(a) % p: return False
    return len(set(verts(a, p))) == len(a)
def primes(a, b): return [q for q in range(a, b + 1) if q > 1 and all(q % d for d in range(2, int(q ** .5) + 1))]

def part1():   # counterexample B={±1,±2,±3}, z=1, a=(1,3,-2,-3,-1,2), r=4
    for p in primes(13, 103):
        a = [1, 3, -2, -3, -1, 2]; a = [x % p for x in a]
        assert valid(a, p) and set(a) == {1, 2, 3, p - 1, p - 2, p - 3}
        V = verts(a, p); assert V == [0, 1, 4, 2, p - 1, p - 2] and 4 in V
        # all non-root single swaps (positions i=2..k-1, steps i,i+1)
        ok_single = []
        for i in range(2, len(a)):
            b = a[:]; b[i - 1], b[i] = b[i], b[i - 1]; ok_single.append(valid(b, p))
        # all simultaneous nonempty sets of nonconsecutive swaps
        any_batch = False
        idx = list(range(2, len(a)))
        for r in range(1, 4):
            for I in itertools.combinations(idx, r):
                if any(abs(x - y) == 1 for x, y in itertools.combinations(I, 2)): continue
                b = a[:]
                for i in I: b[i - 1], b[i] = b[i], b[i - 1]
                if valid(b, p): any_batch = True
        assert not any(ok_single) and not any_batch, (p, ok_single)
    print("(1) counterexample verified for every prime 13<=p<=101: no valid single swap, no valid simultaneous batch")

def rooted_cycles(B, p, z):
    rest = [x for x in B if x != z]; out = []; k = len(B)
    def rec(seq, used, s, seen):
        if len(seq) == k: out.append(tuple(seq)); return
        last = len(seq) == k - 1
        for i, a in enumerate(rest):
            if used >> i & 1: continue
            t = (s + a) % p
            if last:
                if t == 0: out.append(tuple(seq) + (a,))
                continue
            if t in seen: continue
            seen.add(t); seq.append(a); rec(seq, used | 1 << i, t, seen); seq.pop(); seen.discard(t)
    rec([z], 0, z % p, {0, z % p}); return out

def zero_sum_counts(B, p):
    Bs = list(B); Z2 = sum(1 for x in Bs if (-x) % p in B and x < (-x) % p)
    Z3 = 0
    for r in range(3, len(Bs)):
        Z3 += sum(1 for S in itertools.combinations(Bs, r) if sum(S) % p == 0)
    return Z2, Z3

def part2(p, kmin, kmax):   # deterministic bound: #valid single swaps >= max(0, k-2-2*Z2-Z3)
    viol = tot = 0; worst = None
    for k in range(kmin, kmax + 1):
        for B in itertools.combinations(range(1, p), k):
            if sum(B) % p: continue
            Z2, Z3 = zero_sum_counts(B, p); bound = max(0, k - 2 - 2 * Z2 - Z3)
            for z in B:
                for a in rooted_cycles(B, p, z):
                    good = 0
                    for i in range(2, k):
                        b = list(a); b[i - 1], b[i] = b[i], b[i - 1]
                        good += len(set(verts(b, p))) == k
                    tot += 1
                    if good < bound:
                        viol += 1
                        if worst is None: worst = (B, z, a, good, bound, Z2, Z3)
    print(f"(2) deterministic bound p={p}, k={kmin}..{kmax}: cycles checked {tot}, violations {viol}", worst if worst else "")

def part3(p, k):  # probability bound over uniform valid rooted cycles (sets vary), first step z fixed
    z = 1; cnt = tot = 0
    def rec(seq, s, seen):
        nonlocal cnt, tot
        if len(seq) == k:
            if s == 0:
                tot += 1; a = seq
                if all(len(set(verts(a[:i - 1] + [a[i], a[i - 1]] + a[i + 1:], p))) == k for i in range(2, k)): cnt += 1
            return
        for x in range(1, p):
            if x in seq: continue
            t = (s + x) % p
            if len(seq) == k - 1:
                if t == 0: rec(seq + [x], t, seen)
                continue
            if t in seen: continue
            rec(seq + [x], t, seen | {t})
    rec([z], z % p, {0, z % p})
    bound = max(0, 1 - (k * k - 5 * k + 7) / (p - k * k)) if p > k * k else None
    print(f"(3) probability bound p={p}, k={k}: cycles {tot}, all-swaps-valid fraction {cnt/tot:.4f}; GPT bound (k^2-5k+7) {bound}; sharper (k^2-5k+6) {max(0, 1-(k*k-5*k+6)/(p-k*k)) if p>k*k else None}", flush=True)

def mV(V, d, p): return sum(1 for x in V if (x + d) % p in V)

def part4(p, kmin, kmax):  # unique-difference relocation
    viol = ex = tot = 0; cnt_viol_bound = 0
    for k in range(kmin, kmax + 1):
        for B in itertools.combinations(range(1, p), k):
            if sum(B) % p: continue
            for z in B:
                for a in rooted_cycles(B, p, z):
                    V = set(verts(a, p)); tot += 1
                    good_positions = 0
                    for i in range(2, k):   # step a_i is a[i-1] (1-indexed step i)
                        d = a[i - 1]
                        if mV(V, d, p) == 1:
                            b = list(a[:i - 1]) + list(a[i:]) + [a[i - 1]]
                            ex += 1
                            if not valid(b, p): viol += 1
                            else: good_positions += 1
                    E = sum(mV(V, d, p) * (mV(V, d, p) - 1) for d in range(1, p))
                    if good_positions < max(0, k - 2 - E // 2):
                        cnt_viol_bound += 1
    print(f"(4) unique-difference relocation p={p}: cycles {tot}, relocations with m_V=1 tested {ex}, invalid {viol}; cycles violating the counting bound k-2-floor(E/2): {cnt_viol_bound}", flush=True)

def part5():  # (6,-4,-10,-6,10,4): external residue 2 visited; no single-step relocation avoids it
    for p in primes(29, 101):
        a = [x % p for x in (6, -4, -10, -6, 10, 4)]
        assert valid(a, p) and 2 in verts(a, p) and 2 not in set(a) | {0}
        k = len(a); found = False
        for i in range(1, k):
            for j in range(0, k):
                if j == i: continue
                b = a[:i] + a[i + 1:]; b.insert(j, a[i])
                if b[0] != a[0]: continue
                if valid(b, p) and 2 not in verts(b, p): found = True
        assert not found, p
    print("(5) relocation counterexample (6,-4,-10,-6,10,4): no single-step relocation preserving the first step yields a valid cycle avoiding 2, for all 29<=p<=101")

if __name__ == "__main__":
    for part in sys.argv[1:]:
        if part == "1": part1()
        elif part == "2": part2(11, 4, 8); part2(13, 4, 8)
        elif part == "3": part3(17, 4); part3(19, 4); part3(23, 4)
        elif part == "4": part4(11, 4, 8); part4(13, 5, 8)
        elif part == "5": part5()
