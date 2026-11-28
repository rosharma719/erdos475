import sys, time
sys.argv=[sys.argv[0]]+sys.argv[1:]
src=open('tworoot_checks.py').read()
exec(src[:src.index("# (1) Schur expansion")])
def qq(m,d,r):
    J=tuple(c for c in range(1,m+1) if c!=d); A=tuple(c for c in range(1,m+2) if c not in (r,m+1+d-r))
    return kappa(J,A)
M=int(sys.argv[1]) if len(sys.argv)>1 else 9
for m in range(3,M+1):
    t0=time.time()
    allq=[qq(m,d,r) for d in range(1,m+1) for r in range(d,(m+d)//2+1)]
    proj=[qq(m,1,r) for r in range(2,(m+1)//2+1)]
    g=lambda v: reduce(gcd,[abs(x) for x in v]) if v else 0
    print(f"rank {m}: packet size {len(allq)}, full two-root packet gcd = {g(allq)}, projected Witt gcd = {g(proj)} ({len(proj)} coordinates)   ({time.time()-t0:.0f}s)",flush=True)
