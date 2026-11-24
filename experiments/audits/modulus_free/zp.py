# Thm 3/4: B with a simple cycle (vertex set V, span W). a > max|b|. Insert (a,b,-a) or (-a,b,a) around one step.
# Need final cycle simple with span <= 2a (= diam of B u {+-a}).
from itertools import combinations
def cycles(B,cap=4000):
    B=list(B); n=len(B); out=[]
    def dfs(path,used,vis,s):
        if len(out)>=cap: return
        if len(path)==n:
            if s==0: out.append(tuple(path))
            return
        for i in range(n):
            if used>>i&1: continue
            t=s+B[i]
            if len(path)==n-1:
                if t==0: dfs(path+[B[i]],used|1<<i,vis,t)
                continue
            if t in vis: continue
            dfs(path+[B[i]],used|1<<i,vis|{t},t)
    dfs([B[0]],1,{0,B[0]},B[0])   # rotation: fix first element
    return out
def verts(w):
    v=[0]
    for x in w[:-1]: v.append(v[-1]+x)
    return v
def ok(w,D):
    v=verts(w); return sum(w)==0 and len(set(v))==len(v) and max(v)-min(v)<=D
def insert_ok(c,a):
    n=len(c)
    for i in range(n):
        for sg in (1,-1):
            w=list(c[:i])+[sg*a,c[i],-sg*a]+list(c[i+1:])
            if ok(w,2*a): return True
    return False
stats={'t3':[0,0],'t4':[0,0]}; bad=[]
vals=list(range(-6,0))+list(range(1,7))
for k in range(2,7):
    for B in combinations(vals,k):
        if sum(B): continue
        mb=max(abs(x) for x in B)
        for c in cycles(B,300):
            V=verts(c); W=max(V)-min(V)
            for a in range(mb+1, mb+8):
                if W<=a+1:
                    stats['t3'][1]+=1; r=insert_ok(c,a); stats['t3'][0]+=r
                    if not r and len(bad)<5: bad.append(('t3',c,a))
                else:
                    s=W-a
                    if 0<=s<a and len(B)>4*s+2:
                        stats['t4'][1]+=1; r=insert_ok(c,a); stats['t4'][0]+=r
                        if not r and len(bad)<5: bad.append(('t4',c,a))
print(stats, bad)
