import sys
from fractions import Fraction
src=open('tworoot_checks.py').read()
exec(src[:src.index("# (1) Schur expansion")])
def pf(n):
    n=abs(n); s={};d=2
    if n==0: return {0:1}
    while d*d<=n:
        while n%d==0: s[d]=s.get(d,0)+1; n//=d
        d+=1
    if n>1: s[n]=s.get(n,0)+1
    return s
def newton_degree(vals):
    d=vals[:]; deg=-1; k=0
    diffs=[d]
    while any(x!=0 for x in d) and len(d)>1:
        d=[d[i+1]-d[i] for i in range(len(d)-1)]; diffs.append(d)
    # degree = last nonzero level index
    for lvl,row in enumerate(diffs):
        if any(x!=0 for x in row): deg=lvl
    return deg
print("shifted diagonal coefficient D(r,c) = kappa(I_{r,c}, I_{r,c}), I_{r,c} = {c..c+r-1}")
for r in range(2,6):
    vals=[kappa(tuple(range(c,c+r)),tuple(range(c,c+r))) for c in range(1,16 if r<5 else 13)]
    deg=newton_degree(vals)
    print(f"r={r}: values c=1..: {vals}")
    print(f"      finite-difference degree in c: {deg} (data points {len(vals)}); zeros at c = {[c for c,v in zip(range(1,99),vals) if v==0]}")
    print(f"      factorisation of D(r,c), c=2..8: {[ (c,pf(v)) for c,v in zip(range(1,99),vals) if 2<=c<=8]}")
