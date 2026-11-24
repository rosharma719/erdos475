import sys
from shape_sat import hpath
from xcore import walk,ok
lo,hi=int(sys.argv[1]),int(sys.argv[2])
for M in range(lo,hi+1):
    row=[]
    for a in range(6,(M+1)//2+1):
        if 2*a>=M+1: continue
        b=M+1-a; V={0,M+2}|set(range(3,M)); V.discard(a)
        r=hpath(V,set(range(1,M))-{a,b},0,timeout=30)
        row.append(f"{a}:{'Y' if isinstance(r,list) and ok(M,a,walk(M,a,r)) else r}")
    print(M," ".join(row),flush=True)
