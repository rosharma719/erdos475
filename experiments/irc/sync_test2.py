import random,sys,itertools
from syncwalk import search, verts, comonotone
# how restrictive is co-monotonicity? fraction of cross-valid (X,K) pairs that are co-monotone, on a few instances
random.seed(5);tot=com=0
for _ in range(30):
    while True:
        P=sorted(random.sample(range(1,11),4));N=sorted(random.sample(range(1,11),4))
        if sum(P)==sum(N) and P!=N and set(P)&set(N): break
    c=max(set(P)&set(N));Pr=[x for x in P if x!=c];Nr=[x for x in N if x!=c]
    for mp in range(1<<3):
        P1=[Pr[i] for i in range(3) if mp>>i&1];P2=[Pr[i] for i in range(3) if not mp>>i&1]
        for mn in range(1<<3):
            N1=[Nr[i] for i in range(3) if mn>>i&1];N2=[Nr[i] for i in range(3) if not mn>>i&1]
            if sum(P1)-sum(N1)!=sum(N2)-sum(P2): continue
            for xs in itertools.permutations(P1+[-x for x in N1]):
                xv=verts(xs)
                if len(set(xv))<len(xv): continue
                for ks in itertools.permutations(N2+[-x for x in P2]):
                    kv=verts(ks)
                    if len(set(kv))<len(kv) or set(xv)&{v+c for v in kv}: continue
                    tot+=1;com+=comonotone(tuple(xv),tuple(kv))
print("cross-valid pairs",tot,"co-monotone",com)
# tight family check
for M in range(4,8):
    for a in range(1,(M+1)//2+1):
        if 2*a==M+1: continue
        P=list(range(1,M+1));N=sorted(set(range(1,M+2))-{a,M+1-a})
        r=search(P,N,True,2*M+2)
        print("tight",M,a,"found" if r else "NONE",flush=True)
