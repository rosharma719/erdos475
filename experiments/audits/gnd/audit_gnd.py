"""Audit of uniform one-hole G_{n,d} (d>=4, n>=d+1): start n-1, n-1 distinct vertices in [1,n], labels [1,n-1]\\{d}.
Claude's citation-free bases (pure zigzags), plus GPT's bases B/C checked with an independent graceful-start search."""
def zig(lo,hi,start_low=True):
    out=[];l,h=lo,hi
    while l<=h:
        if start_low: out.append(l);l+=1;start_low=False
        else: out.append(h);h-=1;start_low=True
    return out
def base(n,d):
    if n==d+1: return zig(1,d,False)                       # d,1,d-1,2,...
    if n==d+2: return [d+1,d+2]+zig(1,d,True)[:-1]         # labels 1,d+1, then d-1..2
    if n==d+3:
        Z=zig(2,d,True); Z=Z[:-2]+Z[-1:]                    # zigzag d-2..3, then 1 (label 2 skipped)
        return [d+2,1,d+3,d+1]+Z                            # labels d+1,d+2,2,d-1
def G(n,d):
    if n<=d+3: return base(n,d)
    return [n-1,1,n]+[n-1-x for x in G(n-3,d)]
def ok(n,d,p):
    L=sorted(abs(y-x) for x,y in zip(p,p[1:]))
    return p[0]==n-1 and len(p)==n-1==len(set(p)) and all(1<=v<=n for v in p) and L==[q for q in range(1,n) if q!=d]
import sys; sys.setrecursionlimit(100000)
bad=[(n,d) for d in range(4,151) for n in range(d+1,d+200) if not ok(n,d,G(n,d))]
print("Claude zigzag bases: failures d=4..150, n<=d+199:",bad[:10],len(bad))
# GPT base B (d>=6): (d+1,3,d+2,1)+graceful perm of [4,d] from d-2 ; base C: (d+2,1,d+3)+graceful perm of [2,d] from 4
def grace(lo,hi,s):
    r=hi-lo+1; path=[s]; used=set(); on={s}
    def rec():
        if len(path)==r: return True
        x=path[-1]
        for l in range(r-1,0,-1):
            if l in used: continue
            for y in (x+l,x-l):
                if lo<=y<=hi and y not in on:
                    path.append(y);used.add(l);on.add(y)
                    if rec(): return True
                    path.pop();used.discard(l);on.discard(y)
        return False
    return path if rec() else None
gb=[];gc=[]
for d in range(6,23):
    p=grace(4,d,d-2); gb.append(p is not None and ok(d+2,d,[d+1,3,d+2,1]+p))
    p=grace(2,d,4); gc.append(p is not None and ok(d+3,d,[d+2,1,d+3]+p))
print("GPT base B d=6..22:",all(gb),"base C:",all(gc))
