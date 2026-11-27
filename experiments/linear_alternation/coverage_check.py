"""Reproduce the 'coverage' table: dim Pi(A0 R^2 + B0 R^3) [even m] / Pi(uA0 R^1 + uB0 R^2) [odd m]
vs dim Pi(R^m); Pi = projection onto the dihedral character pairing nontrivially with Q_m.  Rank over F_P (P=1000003)."""
import itertools, random, sys, math
from artin import *
from modrank import rank_mod
def Qval(u):
    m=len(u); y=[0]
    for i in range(m-1): y.append(y[-1]+u[i])
    num=1
    for i in range(m):
        for j in range(i+1,m): num*=y[j]-y[i]
    den=1
    for v in u: den*=v
    return num//den
def perm_sign(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def monos(n,d):
    def rec(k,left):
        if k==1: yield (left,); return
        for a in range(left+1):
            for r in rec(k-1,left-a): yield (a,)+r
    return list(rec(n,d))
def run_vectors(m):
    R=Ring(m); random.seed(m)
    rot=[(i+1)%m for i in range(m)]; rev=[m-1-i for i in range(m)]
    def chi_Q(pi):
        for _ in range(50):
            w=[random.randint(-9,9) or 1 for _ in range(m-1)]; w.append(-sum(w))
            if w[-1]==0: continue
            w2=[0]*m
            for i in range(m): w2[pi[i]]=w[i]
            a,b=Qval(w),Qval(w2)
            if a and b: return 1 if a==b else (-1 if a==-b else None)
    cq_rot,cq_rev=chi_Q(rot),chi_Q(rev)
    s_rot,s_rev=perm_sign(rot),perm_sign(rev)
    c_rot,c_rev=s_rot*cq_rot,s_rev*cq_rev            # test-space character
    # group elements with characters
    els=[]
    for r in range(m):
        # rotation^r
        p=[(i+r)%m for i in range(m)]; ch=c_rot**r
        els.append((p,ch))
        p2=[p[rev[i]] for i in range(m)]; els.append((p2,ch*c_rev))
    def act(p,mon):
        b=[0]*m
        for i in range(m): b[p[i]]=mon[i]
        return tuple(b)
    def Pi(poly):
        out={}
        for p,ch in els:
            out=padd(out,{act(p,mon):c for mon,c in poly.items()},ch)
        return R.nf(out)
    w=[var(m,i) for i in range(m)]
    y=lambda j: lin(m,range(j))
    A0=const(m,1); P1=const(m,1)
    for j in range(2,m):
        A0=pmul(A0,y(j)); P1=pmul(P1,lin(m,range(1,j)))     # y_j - w_0 = w_1+..+w_{j-1}
    diff=padd(P1,A0,-1); B0={}
    for mon,c in diff.items():
        assert mon[0]>=1; B0[(mon[0]-1,)+mon[1:]]=c
    u=w[0]
    if m%2==0: gens=[(A0,2),(B0,3)]
    else: gens=[(pmul(u,A0),1),(pmul(u,B0),2)]
    rows=[]
    for G,d in gens:
        for g in monos(m,d): rows.append(Pi(pmul(G,{g:1})))
    full_rows=[Pi({a:1}) for a in monos(m,m) if all(a[i]<=i for i in range(m))]
    keys=set()
    for r in rows+full_rows: keys|=set(r)
    return R,rows,full_rows,keys
def run(m):
    R,rows,full_rows,keys=run_vectors(m)
    return None,None,rank_mod(rows),rank_mod(full_rows)
if __name__=="__main__":
    for m in range(4,int(sys.argv[1])+1):
        a,b,p,f=run(m); print(f"rank {m}: chi_Q(rot)={a} chi_Q(rev)={b}  packet dim {p} / full projected test space {f}",flush=True)
