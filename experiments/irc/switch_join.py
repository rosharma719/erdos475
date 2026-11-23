"""Label-preserving switches on a label-exact cover; can they always join cycles?"""
import sys, itertools, random
def build(M):
    V=sorted(set(range(-M+1,M+1))-{M-1}); f={}
    for s in V: f[s]=2*s+M if s<=0 else (2*s-M-3 if s%2==0 else 2*s-M+1)
    return V,f
def ncyc(f):
    seen=set();c=0
    for s in f:
        if s in seen: continue
        c+=1;x=s
        while x not in seen: seen.add(x);x=f[x]
    return c
def switches(V,f,k):
    A=[s for s in V if s<=0];B=[s for s in V if s>0]
    for side in (A,B):
        for S in itertools.combinations(side,k):
            old=[f[s] for s in S];lab=[f[s]-s for s in S];oset=sorted(old)
            for perm in itertools.permutations(range(k)):
                if all(perm[i]==i for i in range(k)): continue
                new=[S[i]+lab[perm[i]] for i in range(k)]
                if sorted(new)==oset: yield S,new
def join(M,ks=(2,3,4),maxsteps=60):
    V,f=build(M);f=dict(f);steps=0
    while ncyc(f)>1 and steps<maxsteps:
        c0=ncyc(f);done=False
        for k in ks:
            best=None
            for S,new in switches(V,f,k):
                g=dict(f)
                for s,t in zip(S,new): g[s]=t
                c=ncyc(g)
                if c<c0 and (best is None or c<best[0]): best=(c,g)
                if best and best[0]==1: break
            if best: f=best[1];done=True;break
        if not done: return ncyc(f),steps,"STUCK"
        steps+=1
    return ncyc(f),steps,"ok"
if __name__=="__main__":
    for M in [6,12,14,16,18,22,24,26,30]:
        V,f=build(M);print(M,"start cycles",ncyc(f),"->",join(M,ks=(2,3)),flush=True)
