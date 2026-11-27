import sys, time
src=open('tworoot_checks.py').read()
exec(src[:src.index("# (1) Schur expansion")])
from math import factorial
def parts_(m,d,r):
    J=tuple(c for c in range(1,m+1) if c!=d); A=tuple(c for c in range(1,m+2) if c not in (r,m+1+d-r)); return J,A
g=lambda v: reduce(gcd,[abs(x) for x in v]) if v else 0
for m in range(3,int(sys.argv[1])+1):
    full1=[];full2=[];proj1=[];proj2=[]
    for d in range(1,m+1):
        for r in range(d,(m+d)//2+1):
            J,A=parts_(m,d,r)
            a=kappa(J,A); b=kappa(A,J)
            full1.append(a); full2.append(b)
            if d==1 and r>=2: proj1.append(a); proj2.append(b)
    print(f"rank {m}: kappa(J_d,A): full gcd {g(full1)}, projected {g(proj1)};   kappa(A,J_d): full gcd {g(full2)}, projected {g(proj2)}",flush=True)
