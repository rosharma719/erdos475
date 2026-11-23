"""Frame + graceful core for the B-shape D={-1,0}∪[2,M-2]∪{M+1}.
Frame: path whose labels are M-1, M-2, ..., n+1 in DECREASING order (a,b removed), with the triple 0-a-(M+1) inserted
once (both directions allowed), then a connecting edge of length n into a core interval [s,s+n-1], which is covered
by any graceful path (labels 1..n-1) starting at the entry vertex."""
import sys, itertools
from functools import lru_cache
def graceful_from(n,k):
    """graceful path on [0,n-1] (labels 1..n-1) starting at k? brute force small n, else assume (Cattell)."""
    if n<=1: return k==0
    if n>9: return None
    for perm in itertools.permutations([x for x in range(n) if x!=k]):
        p=(k,)+perm
        if sorted(abs(p[i+1]-p[i]) for i in range(n-1))==list(range(1,n)): return True
    return False
def search(M,a,maxn=None):
    b=M+1-a; D=set([-1,0])|set(range(2,M-1))|{M+1}
    res=[]
    for n in range(1,(maxn or a)):
        if n+1>a: break
        labs=[l for l in range(M-1,n,-1) if l not in (a,b)]
        for s in range(2,M-1-n+1):
            core=set(range(s,s+n))
            if a in core or not core<=D: continue
            F=D-core
            # DFS
            def rec(v,i,vis,tri,path):
                if i==len(labs):
                    if not tri:
                        # insert triple at the end
                        if v==0 and a not in vis and (M+1) not in vis:
                            return rec(M+1,i,vis|{a,M+1},True,path+[a,M+1])
                        if v==M+1 and a not in vis and 0 not in vis:
                            return rec(0,i,vis|{a,0},True,path+[a,0])
                        return None
                    if vis!=F: return None
                    for c0 in (v+n,v-n):
                        if c0 in core:
                            g=graceful_from(n,c0-s)
                            if g or g is None: return path+[('core',c0,n)]
                    return None
                out=None
                if not tri:
                    if v==0 and a not in vis and (M+1) not in vis:
                        out=rec(M+1,i,vis|{a,M+1},True,path+[a,M+1])
                        if out: return out
                    if v==M+1 and a not in vis and 0 not in vis:
                        out=rec(0,i,vis|{a,0},True,path+[a,0])
                        if out: return out
                L=labs[i]
                for w in (v+L,v-L):
                    if w in F and w not in vis:
                        r=rec(w,i+1,vis|{w},tri,path+[w])
                        if r: return r
                return None
            for st in F:
                r=rec(st,0,{st},False,[st])
                if r: res.append((n,s,r)); return res
    return res
for M in range(int(sys.argv[1]),int(sys.argv[2])+1):
    row=[]
    for a in range(2,(M+1)//2+1):
        if 2*a==M+1: continue
        r=search(M,a)
        row.append(f"a{a}:{'n=%d,s=%d'%(r[0][0],r[0][1]) if r else '-'}")
    print("M",M," ".join(row),flush=True)
