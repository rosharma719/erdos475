"""Diagonal one-hole packet K(J_d,J_d), d=1..m: how many leading entries are needed so that no prime p>m+1 divides them all?
For every prime p in (m+1, PMAX] record the smallest d with K(J_d,J_d) != 0 mod p."""
import sys, time
src=open('tworoot_checks.py').read()
exec(src[:src.index("# (1) Schur expansion")])
def pf(n):
    s={};d=2
    while d*d<=n:
        while n%d==0: s[d]=s.get(d,0)+1; n//=d
        d+=1
    if n>1: s[n]=s.get(n,0)+1
    return s
def primes_upto(n):
    return [q for q in range(2,n+1) if all(q%r for r in range(2,int(q**0.5)+1))]
PMAX=2000
rows={}
for m in range(3,int(sys.argv[1])+1):
    t0=time.time()
    K=[kappa(tuple(c for c in range(1,m+1) if c!=d),tuple(c for c in range(1,m+1) if c!=d)) for d in range(1,m+1)]
    rows[m]=K
    out=[]
    for t in (1,2,3):
        g=reduce(gcd,[abs(x) for x in K[:t]])
        big=[q for q in pf(g) if q>m+1] if g else ['zero']
        out.append((t,g,big))
    # smallest witness index per admissible prime (up to PMAX)
    wit={}
    worst=0; worst_p=None
    for p in primes_upto(PMAX):
        if p<=m+1: continue
        d0=next((d for d,x in enumerate(K,1) if x%p!=0),None)
        wit[p]=d0
        if d0 is None: worst=999; worst_p=p; break
        if d0>worst: worst=d0; worst_p=p
    print(f"m={m}: first-t gcds (t, gcd, primes>m+1 dividing it): {out};  max over admissible primes p<={PMAX} of the smallest witness index d: {worst} (at p={worst_p})   ({time.time()-t0:.0f}s)",flush=True)
