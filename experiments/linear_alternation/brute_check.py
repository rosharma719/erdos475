"""Independent brute-force check of c_{m,r}: H_{m,r}=sum_pi sgn(pi) X_{pi(r)} F_m(X_pi) = c_{m,r} * Delta_m,
evaluated exactly at x=(1..m) over all permutations. Usage: python3 brute_check.py M"""
import sys, itertools, math
from math import gcd
def run(m):
    x = list(range(1, m+1))
    delta = 1
    for i in range(m):
        for j in range(i+1, m): delta *= x[j]-x[i]
    H = [0]*m
    for perm in itertools.permutations(range(m)):
        # sign via inversion count
        inv = sum(1 for i in range(m) for j in range(i+1, m) if perm[i] > perm[j])
        sgn = -1 if inv & 1 else 1
        a = [x[k] for k in perm]
        pre = [0]
        for v in a: pre.append(pre[-1]+v)
        f = 1
        for i in range(m):
            for j in range(i+2, m+1):          # interval a[i..j-1], length>=2
                if i == 0 and j == m: continue
                f *= pre[j]-pre[i]
                if f == 0: break
            if f == 0: break
        if f == 0: continue
        for r in range(m): H[r] += sgn*a[r]*f
    assert all(h % delta == 0 for h in H), "non-integral"
    c = [h//delta for h in H]
    g = 0
    for v in c: g = gcd(g, abs(v))
    return c, g
if __name__ == "__main__":
    m = int(sys.argv[1]); c, g = run(m)
    print(f"m={m} {c} gcd={g}")
