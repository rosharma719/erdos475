import random,sys,time
from splice_test import lift, core_walk
def splice_sol(core,R,p,tl=20):
    n=len(core);t0=time.time()
    for rot in range(n):
        cw=core[rot:]+core[:rot]; seen={0}; seq=[]
        def rec(i,mask,s):
            if time.time()-t0>tl: raise TimeoutError
            if i==n and mask==(1<<len(R))-1: return True
            opts=([('c',cw[i])] if i<n else [])+[(j,R[j]) for j in range(len(R)) if not mask>>j&1]
            for o,x in opts:
                t=(s+x)%p; ni=i+(o=='c'); nm=mask|(0 if o=='c' else 1<<o)
                if ni==n and nm==(1<<len(R))-1:
                    if t==0: seq.append((o,x)); return True
                    continue
                if t in seen: continue
                seen.add(t); seq.append((o,x))
                if rec(ni,nm,t): return True
                seen.discard(t); seq.pop()
            return False
        try:
            if rec(0,0,0): return rot,cw,seq
        except TimeoutError: return None
    return None
p=int(sys.argv[1]);alpha=float(sys.argv[2]);random.seed(int(sys.argv[3]))
k=int(alpha*(p-1))
for trial in range(int(sys.argv[4])):
    while True:
        A=random.sample(range(1,p),k-1);s=(-sum(A))%p
        if s and s not in A: A.append(s);break
    best=None
    for lam in range(1,p):
        P,N=lift([lam*x for x in A],p);C=set(P)&set(N)
        rem=[x for x in P if x not in C]+[-x for x in N if x not in C]
        if C and (best is None or len(rem)<len(best[1])): best=(C,rem)
    C,R=best;core=core_walk(C)
    r=splice_sol(core,R,p)
    if not r: print("no/TO");continue
    rot,cw,seq=r
    # profile: for each remainder step, the index of core steps done before it, and running remainder sum
    ci=0;run=0;prof=[]
    for o,x in seq:
        if o=='c': ci+=1
        else: run+=x; prof.append((ci,x,run))
    n=len(core); half=n//2
    print(f"|C|={len(C)} core steps={n} rot={rot} b1={max(C)} | remainder (pos_in_core, step, running sum):",prof)
