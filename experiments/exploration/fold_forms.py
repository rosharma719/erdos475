"""FOLD solutions in the Q-picture: Q_0..Q_m, Q_m=-Q_0, classes |Q_j| distinct nonzero (j<m), step classes = W.
Test restricted forms:  d = number of same-sign ("difference-type") edges.  Odd #opposite-sign edges required.
Form SUM: d<=1 (all edges opposite-sign except possibly one).   Form MONO: additionally labels |Q_j| unimodal?  (just report d_min)."""
import itertools, sys, random

def solve(W, p, r, dmax, rng, cap=300000):
    m = len(W); Ws = set(W); n = [0]
    def rec(Q, used_cls, usedW, flips, diffs):
        n[0] += 1
        if n[0] > cap: return None
        j = len(Q) - 1                      # have Q_0..Q_j
        if j == m:
            return True if (Q[m] == (-Q[0]) % p) else False
        if j == m - 1:                      # last step goes to -Q_0
            tgt = (-Q[0]) % p
            c = min((tgt - Q[j]) % p, (Q[j] - tgt) % p)
            if c in Ws and c not in usedW:
                same = (Q[j] <= r) == (tgt <= r) if False else None
                # sign relation: eps_j vs eps_m=-eps_0 ; compute #diff edges so far via signs of Q
                Q.append(tgt); usedW.add(c)
                ok = check(Q)
                if ok: return True
                Q.pop(); usedW.discard(c)
            return False
        cand = list(range(1, p)); rng.shuffle(cand)
        for q in cand:
            c = min(q % p, (-q) % p)
            if c in used_cls: continue
            st = min((q - Q[-1]) % p, (Q[-1] - q) % p)
            if st not in Ws or st in usedW: continue
            Q.append(q); used_cls.add(c); usedW.add(st)
            res = rec(Q, used_cls, usedW, 0, 0)
            if res: return True
            Q.pop(); used_cls.discard(c); usedW.discard(st)
            if res is None: return None
        return False
    def sign(q): return 1 if q <= r else -1
    def check(Q):
        # edge j between Q_{j-1},Q_j: same-sign iff sign equal (signs relative to representative in [1..r] for Q_j, j<m; Q_m has sign -sign(Q_0))
        d = 0
        for j in range(1, m + 1):
            a, b = Q[j - 1], Q[j]
            same = sign(a) == sign(b)
            d += same
        return (d <= dmax if dmax >= 0 else d == m - 1) and (m - d) % 2 == 1
    used_cls = {min(q, p - q) for q in ()}
    for q0 in range(1, p):
        if q0 > r: continue
        res = rec([q0], {min(q0, p - q0)}, set(), 0, 0)
        if res: return True
        if res is None: return None
    return False

def run(p, dmax):
    r = (p - 1) // 2; rng = random.Random(5); tot = bad = und = 0
    for m in range(2, r + 1):
        for W in itertools.combinations(range(1, r + 1), m):
            tot += 1
            res = solve(W, p, r, dmax, rng)
            if res is None: und += 1
            elif res is False:
                bad += 1
                if bad <= 5: print("   no form-d<=%d solution:" % dmax, p, W, flush=True)
    print(f"p={p}, d<={dmax}: symmetric sets {tot}, no solution of this form {bad}, undetermined {und}", flush=True)

if __name__ == "__main__":
    p = int(sys.argv[1]); dmax = int(sys.argv[2]); run(p, dmax)
