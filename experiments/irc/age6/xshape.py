import sys; sys.path.insert(0,'..'); sys.path.insert(0,'.')
from bridge_sat import solve,verify
for a,M in [(14,29),(14,30),(14,31),(15,31),(16,34),(18,38),(20,42),(20,43)]:
    b=M+1-a; br=(a,-M,b,-(M+1)); r=solve(M,a,br,timeout=60)
    if isinstance(r,list):
        D=sorted(r); print(a,M,'Dmin',D[0],'Dmax',D[-1],'missing in [min,max]:',sorted(set(range(D[0],D[-1]+1))-set(D)),flush=True)
    else: print(a,M,r)
