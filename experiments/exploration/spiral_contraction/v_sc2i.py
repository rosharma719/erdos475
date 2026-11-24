from collections import Counter
from math import comb
def centered(x, p):
    m = (p - 1) // 2
    return (x + m) % p - m
def F(A, p, s):
    total = sum(centered(s*a, p) for a in A)
    assert total % p == 0
    return total // p
def verify_counterexample(removed, added):
    p = 59; m = 29
    Q = {x*x % p for x in range(1, p)}
    assert removed <= Q and not added & Q
    A = (Q - removed) | added
    assert len(A) == 29 and sum(A) % p == 0
    values = {s: F(A, p, s) for s in range(1, p)}
    assert min(map(abs, values.values())) == 1
    for s, f in values.items():
        if abs(f) > 1: continue
        B = {s*a % p for a in A}
        assert abs(f) == 1 and (-f*m) % p in B
    print("SC2-I counterexample verified:", sorted(removed), "->", sorted(added))
verify_counterexample({15, 21, 26}, {2, 8, 52})
verify_counterexample({22, 36, 49}, {2, 13, 33})
p = 181
H = {pow(2, 4*j, p) for j in range(45)}
assert len(H) == 45 and sum(H) % p == 0 and not H & {(-x) % p for x in H}
assert [F(H, p, s) for s in (1, 2, 4, 8)] == [3, 4, -3, -4]
assert min(abs(F(H, p, s)) for s in range(1, p)) == 3
available = [x for x in range(1, 91) if x not in H and p-x not in H]
assert len(available) == 45
R = set(available[:23]); R |= {p-x for x in R}
A = H | R
assert len(A) == 91 and sum(A) % p == 0
assert all(F(A, p, s) == F(H, p, s) for s in range(1, p))
assert all({s*a % p for a in A} != A for s in range(2, p))
print("Padded exception family:", comb(45, 23))
# class number check
def h(D):  # class number of discriminant -D via reduced forms
    c=0;a=1
    while 3*a*a<=D:
        for b in range(-a+1,a+1):
            if (b*b+D)%(4*a)==0:
                cc=(b*b+D)//(4*a)
                if cc>=a and not (b<0 and (a==cc)):
                    from math import gcd
                    if gcd(gcd(a,abs(b)),cc)==1: c+=1
        a+=1
    return c
for p in [11,19,43,59,67,83,107,131,139,163,179,211,227,251,7,23,31,47,71,79,103,127]:
    Q={x*x%p for x in range(1,p)}
    I=min(abs(F(Q,p,s)) for s in range(1,p)) if sum(Q)%p==0 else None
    exp=h(p) if p%8==3 else 0
    print(p, p%8, "I(Q)=",I," predicted",exp, "OK" if I==exp else "MISMATCH")
