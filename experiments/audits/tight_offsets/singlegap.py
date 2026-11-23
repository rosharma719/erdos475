import sys
sys.setrecursionlimit(10000)
def search(D,M,a):
    b=M+1-a; Ds=set(D); need=set(range(2,M+1))-{a,b}
    # path must contain consecutive 0,a,M+1 (lengths a,b). Build path as: left part ... 0, a, M+1 ... right part.
    # DFS extending both ends.
    used={0,a,M+1}
    def dfs(L,R,lens):
        if len(used)==M: return [L,R] if not lens else None
        for end in (0,1):
            v = L if end==0 else R
            for l in list(lens):
                for w in (v+l,v-l):
                    if w in Ds and w not in used:
                        used.add(w); lens.discard(l)
                        r=dfs(w if end==0 else L, w if end==1 else R, lens)
                        if r is not None: return r
                        used.discard(w); lens.add(l)
            # to avoid duplicate work, only extend the left end once it is fixed? keep both: small M
        return None
    return dfs(0,M+1,set(need)) is not None
def forms(M,a):
    out=[]
    for t in range(-2*M,1):
        for k in range(0,M):
            low=[t+2*i for i in range(k+1)]
            high=[t+2*k+3+2*j for j in range(M-k-1)]
            D=low+high
            if {0,a,M+1}<=set(D) and max(D)-min(D)<=2*M+1:
                out.append((t,k,D))
    return out
for M in range(6,15,2):
    for a in range(3,M//2,2):  # odd a < M/2, a>=3 (a=1 excluded, c=1 in S)
        res=[]
        for t,k,D in forms(M,a):
            if search(D,M,a): res.append((t,k))
        print("M",M,"a",a,"single-gap forms with a c=1 half-walk:",res)
