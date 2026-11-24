import sys
from bridge_sat import solve,verify
lo,hi=int(sys.argv[1]),int(sys.argv[2])
for M in range(lo,hi+1):
    row=[]
    for a in range(6,(M+1)//2+1):
        if 2*a>=M+1: continue
        b=M+1-a; got=None
        for name,br in (("G",(b,-M,-(M+1),a)),("X",(a,-M,b,-(M+1))),("Y",(a,-M,-(M+1),b)),("Z",(b,-M,a,-(M+1)))):
            r=solve(M,a,br,timeout=40)
            if isinstance(r,list) and verify(M,a,r,br): got=name;break
            if r=='TO': got=(got or '')+'?'
        row.append(f"a{a}:{got}")
    print("M",M," ".join(row),flush=True)
