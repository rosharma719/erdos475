import sys
sys.setrecursionlimit(10000)
def final_walk(M,a,delta):
    b=M+1-a
    W=[M+1,-b]+delta[1:]+[M]+[-x for x in reversed(delta)]+[-M]
    return W
def check(M,a,W,R):
    b=M+1-a
    P=sorted(x for x in W if x>0); N=sorted(-x for x in W if x<0)
    assert P==sorted(set(range(1,M+2))-{a,b}) and N==list(range(1,M+1)),(P,N)
    v=[0]
    for x in W: v.append(v[-1]+x)
    assert v[-1]==0; vs=v[:-1]; assert len(set(vs))==len(vs)
    assert max(vs)-min(vs)<=R
    return max(vs)-min(vs)
def search(M,a,R,nodecap=2_000_000):
    b=M+1-a; L=set(range(1,M))-{b}
    # vertices: 0, M+1, D_1.., D+M. window: all within span R.
    cnt=[0]
    def ok_add(x,occ):
        return x not in occ and (x+M) not in occ
    def dfs(D,occ,lens,lo,hi):
        cnt[0]+=1
        if cnt[0]>nodecap: return None
        if not lens: return list(D)
        v=D[-1]
        for l in sorted(lens,reverse=True):
            for w in (v+l,v-l):
                if w in occ or w+M in occ: continue
                nlo=min(lo,w); nhi=max(hi,w+M)
                if nhi-nlo>R: continue
                occ.add(w); occ.add(w+M); lens.discard(l); D.append(w)
                r=dfs(D,occ,lens,nlo,nhi)
                if r: return r
                D.pop(); lens.add(l); occ.discard(w); occ.discard(w+M)
        return None
    occ={0,M+1,M,a,a+M}
    if a+M==M+1 or a in (0,M,M+1): return None
    r=dfs([0,a],occ,L-{a},0,a+M)
    if r is None: return None
    steps=[r[i+1]-r[i] for i in range(len(r)-1)]
    return steps
R=int(sys.argv[2]) if len(sys.argv)>2 else None
for M in range(5,int(sys.argv[1])+1):
    row=[]
    for a in range(2,(M+1)//2+1):
        if 2*a==M+1: continue
        s=search(M,a,R if R is not None else 2*M+2)
        if s: check(M,a,final_walk(M,a,s),R if R is not None else 2*M+2)
        row.append((a,'ok' if s else '--'))
    print(M,row,flush=True)
