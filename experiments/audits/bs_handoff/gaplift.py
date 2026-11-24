# Top-gap lift: p1>q1, p1-p2>q2, t=p1-q1 not in P.  For any root r in P\{p1}:
# a G-walk of (P'=P\{p1}u{t}, N'=N\{q1}) rooted at r lifts to a G-walk of (P,N) rooted at r
# by replacing the step +t (from vertex v) with (+p1,-q1) if v<=0, else (-q1,+p1).
import random,sys
sys.setrecursionlimit(10000)
def gwalk(P,N,r,cap=200000):
    lo=-max(N)+1; hi=max(P); el=[x for x in P if x!=r]+[-x for x in N]
    vis={0,r}; cnt=[0]
    def dfs(pos,rem,path):
        cnt[0]+=1
        if cnt[0]>cap: return None
        if not rem: return path if pos==0 else None
        for i,x in enumerate(rem):
            w=pos+x
            if len(rem)==1:
                if w==0: return path+[x]
                continue
            if lo<=w<=hi and w not in vis:
                vis.add(w); res=dfs(w,rem[:i]+rem[i+1:],path+[x]); vis.discard(w)
                if res: return res
        return None
    return dfs(r,el,[r])
def check(P,N,W,r):
    assert W[0]==r and sorted(x for x in W if x>0)==sorted(P) and sorted(-x for x in W if x<0)==sorted(N)
    v=[0]
    for x in W: v.append(v[-1]+x)
    assert v[-1]==0; vs=v[:-1]; assert len(set(vs))==len(vs)
    assert all(-max(N)<x<=max(P) for x in vs)
rng=random.Random(7); done=0
while done<3000:
    P=set(rng.sample(range(1,25),rng.randint(2,7)))
    p=sorted(P,reverse=True); p1,p2=p[0],p[1]
    k=rng.randint(2,7); N=set(rng.sample(range(1,p1),min(k,p1-1)))
    d=sum(P)-sum(N)
    # adjust to balance: add/remove one element
    if d>0 and d not in N and d<p1: N.add(d)
    if sum(P)!=sum(N) or len(N)<2: continue
    q=sorted(N,reverse=True); q1,q2=q[0],q[1]
    t=p1-q1
    if not(p1>q1 and p1-p2>q2 and t not in P): continue
    P2=(P-{p1})|{t}; N2=N-{q1}
    for r in P-{p1}:
        w=gwalk(P2,N2,r)
        if w is None: continue
        v=[0]
        for x in w: v.append(v[-1]+x)
        i=w.index(t); vv=v[i]
        W=w[:i]+([p1,-q1] if vv<=0 else [-q1,p1])+w[i+1:]
        check(P,N,W,r); done+=1
print("lifted and verified",done,"walks")
