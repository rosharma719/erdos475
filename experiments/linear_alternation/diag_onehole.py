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
for m in range(3,int(sys.argv[1])+1):
    t0=time.time()
    K=[kappa(tuple(c for c in range(1,m+1) if c!=d),tuple(c for c in range(1,m+1) if c!=d)) for d in range(1,m+1)]
    g=reduce(gcd,[abs(x) for x in K])
    print(f"m={m}: K(J_d,J_d), d=1..m = {K if m<=8 else [len(str(abs(x))) for x in K]}  gcd over d = {g} = {pf(g) if g else 0}   primes>m+1 dividing gcd: {[q for q in pf(g) if q>m+1] if g else 'n/a'}  ({time.time()-t0:.0f}s)",flush=True)
