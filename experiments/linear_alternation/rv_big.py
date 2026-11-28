import sys, time
from rv_contents import *
for m in range(int(sys.argv[1]),int(sys.argv[2])+1):
    t0=time.time()
    q1=[qq(m,1,r) for r in range(1,(m+1)//2+1)]
    print(f"rank {m}: projected packet q_(m,1,r), r=1..: {q1}",flush=True)
    print(f"     gcd of r>=2 coordinates = {reduce(gcd,[abs(x) for x in q1[1:]])}; gcd of last two = {gcd(abs(q1[-1]),abs(q1[-2]))}; vector mod 19 = {[x%19 for x in q1]}; mod 7 = {[x%7 for x in q1]}",flush=True)
    R,V=RV(m); cr,dr=content_of(R); cv,dv=content_of(V)
    print(f"     content(R_m)={cr}, content(V_m)={cv}   ({time.time()-t0:.0f}s)",flush=True)
