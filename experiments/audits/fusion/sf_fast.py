"""Faster exhaustive Strong Fusion test using the edge-insertion form:
cycle z of Z with vertex set V (bitmask); replace edge u->u' by (b1, w, b2..bm): new points u+b1, u'+σ_j (j<m).
SF(A): exists atom B ⊂ A (Z=A\\B zero-sum) such that EVERY valid cycle of Z admits some edge + B-order.
Reversal is covered automatically? No — we also try the reversed cycle (edges reversed: u'->u with step -w),
which is equivalent to trying the negated configuration; included by iterating both directions."""
import sys,itertools
from itertools import combinations, permutations
def minimal(B,p): return sum(B)%p==0 and all(sum(T)%p for r in range(1,len(B)) for T in combinations(B,r))
def valid_cycles(Z,p):
    Z=list(Z); f=Z[0]; rest=Z[1:]; n=len(Z)
    # DFS over orders starting with f, tracking partial sums
    out=[]; path=[f]; seen={0,f%p}; s=[f%p]
    def rec(avail):
        if not avail:
            if s[-1]==0: pass
            return
        if len(avail)==1:
            x=avail[0]
            if (s[-1]+x)%p==0: out.append(tuple(path)+(x,))
            return
        for i,x in enumerate(avail):
            t=(s[-1]+x)%p
            if t in seen: continue
            seen.add(t); s.append(t); path.append(x)
            rec(avail[:i]+avail[i+1:])
            path.pop(); s.pop(); seen.discard(t)
    rec(rest); return out
def border_orders(B):
    return [(o, [sum(o[:j]) for j in range(1,len(o))]) for o in permutations(B)]
def fuses1(z,BO,p):
    n=len(z); verts=[0]
    for x in z[:-1]: verts.append((verts[-1]+x)%p)
    V=set(verts)
    for i in range(n):
        u0=verts[i]; u1=verts[(i+1)%n]
        for o,sig in BO:
            pts=[(u0+o[0])%p]+[(u1+s)%p for s in sig]
            if len(set(pts))==len(pts) and not (set(pts)&V): return True
    return False
def fuses(z,BO,p): return fuses1(z,BO,p) or fuses1(z[::-1],BO,p)
if __name__=="__main__":
    p=int(sys.argv[1]); lo=int(sys.argv[2]); hi=int(sys.argv[3])
    fails=[];tested=0
    for n in range(lo,hi+1):
        for A in combinations(range(1,p),n):
            if sum(A)%p or minimal(A,p): continue
            tested+=1; ok=False
            cands=sorted([B for r in range(2,n-1) for B in combinations(A,r) if minimal(B,p)],key=len)
            for B in cands:
                Z=tuple(x for x in A if x not in B)
                if sum(Z)%p: continue
                BO=border_orders(B); good=True
                for z in valid_cycles(Z,p):
                    if not fuses(z,BO,p): good=False;break
                if good: ok=True;break
            if not ok: fails.append(A); print('FAIL',p,A,flush=True)
        print('p',p,'n',n,'tested so far',tested,'fails',len(fails),flush=True)
