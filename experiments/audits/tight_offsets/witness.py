import sys
sys.setrecursionlimit(10000)
def find(D,M,a):
    b=M+1-a; Ds=set(D); used={0,a,M+1}
    def dfs(path,lens):
        if len(used)==M: return path if not lens else None
        for end in (0,1):
            v=path[0] if end==0 else path[-1]
            for l in sorted(lens):
                for w in (v+l,v-l):
                    if w in Ds and w not in used:
                        used.add(w); lens.discard(l)
                        r=dfs([w]+path if end==0 else path+[w],lens)
                        if r: return r
                        used.discard(w); lens.add(l)
        return None
    return dfs([0,a,M+1],set(range(2,M+1))-{a,b})
def check(path,M,a):
    b=M+1-a
    # delta = steps along path starting at its first vertex; translate so first vertex is 0
    steps=[path[i+1]-path[i] for i in range(len(path)-1)]
    W=steps+[1]+[-s for s in reversed(steps)]+[-1]
    # contract the two consecutive negative steps of sizes a,b (in either half) into -(M+1)
    for i in range(len(W)-1):
        if W[i]<0 and W[i+1]<0 and {-W[i],-W[i+1]}=={a,b}:
            W=W[:i]+[W[i]+W[i+1]]+W[i+2:]; break
    P=sorted(x for x in W if x>0); N=sorted(-x for x in W if x<0)
    assert P==list(range(1,M+1)), P
    assert N==sorted(set(range(1,M+2))-{a,b}), N
    ps=[0]
    for x in W: ps.append(ps[-1]+x)
    assert ps[-1]==0
    verts=ps[:-1]; assert len(set(verts))==len(verts)
    rng=max(verts)-min(verts); assert rng<=2*M+2, rng
    p=2*M+3; assert len({v%p for v in verts})==len(verts)
    return W,rng
for M,a,t,k in [(10,3,-2,1),(14,3,-4,2),(14,5,-4,2)]:
    D=[t+2*i for i in range(k+1)]+[t+2*k+3+2*j for j in range(M-k-1)]
    path=find(D,M,a); W,r=check(path,M,a)
    print(f"M={M} a={a} D={D}\n  path={path}\n  W={W}\n  range={r}  valid mod p={2*M+3}: yes")
