import sys,time
from halfwalk_sat import solve,lift
def fits(M,c): return any((M+j)%c==0 for j in range(4))
lo,hi=int(sys.argv[1]),int(sys.argv[2])
for M in range(lo,hi+1):
    row=[]
    for a in range(2,(M+1)//2+1):
        if 2*a>=M+1: continue
        b=M+1-a; got=None
        tries=[]
        if fits(M,a): tries.append((a,'junction'))
        tries+= [(M,'internal'),(1,'internal'),(2,'internal'),(3,'internal')]
        if fits(M,b): tries.append((b,'junction'))
        for c,mode in tries:
            if not fits(M,c): continue
            r,p=solve(M,a,c,mode,timeout=60)
            if r=='FOUND' and lift(M,a,c,mode,p)[0]: got=f"{mode[0]}{c}";break
        row.append(f"a{a}:{got}")
    print("M",M," ".join(row),flush=True)
