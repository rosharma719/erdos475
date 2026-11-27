"""Marked-root algebra C_m = K[u,v,w_0..w_{m-1}] / (H_m, H_{m+1}, e_k(w) - (-1)^{k+1} v H_{k-2}, k=1..m), graded (u,w weight 1, v weight 2).
Checks (m=3,4): dim C_m = m(m+1)/2 * m!, socle degree N_m+2m-2, Ann(a_d)=(eta_d), Ann(eta_d)=(a_d), eta_d eta_e=0, eta_d^2=g eta_d,
sum eta_d = g, rho(I)=vC (I=(e_2..e_m)), dim C/(v) = m*m!, rank Phi vs (m!/2)(dim A + dim gA)."""
import itertools, sys, time, math
from modrank import rank_mod, P
def hlist(m):                       # H_j as polys in (u,v) over vars order [u,v,w..]: keep as dict {(a,b):c}
    h=[{(0,0):1},{(1,0):1}]
    for k in range(2,m+3):
        t={}
        for (a,b),c in h[k-1].items(): t[(a+1,b)]=t.get((a+1,b),0)+c
        for (a,b),c in h[k-2].items(): t[(a,b+1)]=t.get((a,b+1),0)-c
        h.append({k_:v for k_,v in t.items() if v})
    return h
class Alg:
    def __init__(s,m):
        s.m=m; s.n=m+2; s.wt=[1,2]+[1]*m
        H=hlist(m); s.H=H
        gens=[s.fromuv(H[m]),s.fromuv(H[m+1])]
        for k in range(1,m+1):
            ek=s.elem(k)
            rhs={}
            if k>=2:
                for (a,b),c in H[k-2].items(): rhs=s.add(rhs,{s.mono(u=a,v=b+1):c*(-1)**(k+1)})
            gens.append(s.add(ek,rhs,-1))
        s.gens=gens; s.cache={}
    def mono(s,u=0,v=0,w=None):
        e=[0]*s.n; e[0]=u; e[1]=v
        if w:
            for i,x in w.items(): e[2+i]=x
        return tuple(e)
    def fromuv(s,p): return {s.mono(u=a,v=b):c for (a,b),c in p.items()}
    def add(s,P_,Q_,sg=1):
        o=dict(P_)
        for k,v in Q_.items(): o[k]=o.get(k,0)+sg*v
        return {k:v%P for k,v in o.items() if v%P}
    def mul(s,P_,Q_):
        o={}
        for a,c in P_.items():
            for b,d in Q_.items():
                k=tuple(x+y for x,y in zip(a,b)); o[k]=(o.get(k,0)+c*d)%P
        return {k:v for k,v in o.items() if v}
    def var(s,i): e=[0]*s.n; e[i]=1; return {tuple(e):1}
    def const(s,c): return {(0,)*s.n:c%P}
    def elem(s,k):
        t={}
        for S in itertools.combinations(range(s.m),k):
            e=[0]*s.n
            for i in S: e[2+i]=1
            t[tuple(e)]=1
        return t
    def wdeg(s,e): return sum(a*b for a,b in zip(e,s.wt))
    def monos(s,d):
        if d in s.cache: return s.cache[d]
        out=[]
        def rec(i,left,cur):
            if i==s.n:
                if left==0: out.append(tuple(cur))
                return
            for a in range(left//s.wt[i]+1):
                cur.append(a); rec(i+1,left-a*s.wt[i],cur); cur.pop()
        rec(0,d,[]); s.cache[d]=out; return out
    def ideal_rows(s,d,extra=()):
        rows=[]
        for g in list(s.gens)+list(extra):
            wg=s.wdeg(next(iter(g)))
            if wg>d: continue
            for mo in s.monos(d-wg): rows.append(s.mul(g,{mo:1}))
        return rows
    def hom(s,f): return s.wdeg(next(iter(f)))
def run(m,tmax):
    A=Alg(m); N=m*(m-1)//2; soc=N+2*m-2
    t0=time.time(); dims=[]; Irank={}
    for d in range(0,soc+3):
        r=rank_mod(A.ideal_rows(d)); Irank[d]=r; dims.append(len(A.monos(d))-r)
    total=sum(dims); print(f"m={m}: graded dims {dims}; dim C = {total} (expected {m*(m+1)//2*math.factorial(m)}); socle degree {max(i for i,x in enumerate(dims) if x)} (expected {soc})",flush=True)
    w=[A.var(2+i) for i in range(m)]; u=A.var(0)
    a=[A.add(w[d],u,-1) for d in range(m)]
    eta=[]
    for d in range(m):
        t=A.const(1)
        for i in range(m):
            if i!=d: t=A.mul(t,A.add(u,w[i],-1))
        eta.append(t)
    Hm=A.H
    g={}
    for j in range(m):
        uj={A.mono(u=m-1-j):1}
        g=A.add(g,A.mul(A.fromuv(Hm[j]),uj))
    def inI(f):
        d=A.hom(f)
        if d not in Irank: Irank[d]=rank_mod(A.ideal_rows(d))
        return rank_mod(A.ideal_rows(d)+[f])==Irank[d]
    def ann_dims(mult,K):
        ok=True; wm=A.hom(mult); wk=A.hom(K)
        for d in range(0,soc+2):
            V=A.monos(d)
            Id1=A.ideal_rows(d+wm); r1=rank_mod(Id1)
            mV=[A.mul(mult,{x:1}) for x in V]
            ann=len(V)-(rank_mod(Id1+mV)-r1)-Irank[d]  # Irank filled for d<=soc+2
            Kd=[A.mul(K,{x:1}) for x in A.monos(d-wk)] if d>=wk else []
            ks=rank_mod(A.ideal_rows(d)+Kd)-Irank[d]
            inc=all(inI(A.mul(mult,k)) for k in ([A.mul(K,{x:1}) for x in A.monos(d-wk)] if d>=wk else []))
            if ann!=ks or not inc: ok=False
        return ok
    print(f"  eta_d a_d=0: {all(inI(A.mul(eta[d],a[d])) for d in range(m))};  eta_d eta_e=0 (d!=e): {all(inI(A.mul(eta[d],eta[e])) for d in range(m) for e in range(m) if d!=e)};  "
          f"eta_d^2=g eta_d: {all(inI(A.add(A.mul(eta[d],eta[d]),A.mul(g,eta[d]),-1)) for d in range(m))};  sum eta_d = g: {inI(A.add(A.const(0) if False else {k:v for k,v in sum_polys(A,eta).items()},g,-1))}",flush=True)
    print(f"  Ann(a_0)=(eta_0): {ann_dims(a[0],eta[0])};  Ann(eta_0)=(a_0): {ann_dims(eta[0],a[0])}   [{time.time()-t0:.0f}s]",flush=True)
    # rho(I)=vC and dim C/(v)
    v=A.var(1); ok=True; vdim=0
    for d in range(0,soc+2):
        base=A.ideal_rows(d); rb=Irank[d]
        vV=[A.mul(v,{x:1}) for x in A.monos(d-2)] if d>=2 else []
        eV=[]
        for k in range(2,m+1):
            ek=A.elem(k)
            if d>=k: eV+= [A.mul(ek,{x:1}) for x in A.monos(d-k)]
        rv=rank_mod(base+vV); re=rank_mod(base+eV); rj=rank_mod(base+vV+eV)
        if not (rv==re==rj): ok=False
        vdim+=rv-rb
    print(f"  (e_2..e_m)C = vC: {ok};  dim C/(v) = {total-vdim} (expected m*m! = {m*math.factorial(m)})   [{time.time()-t0:.0f}s]",flush=True)
    return A
def sum_polys(A,ps):
    o={}
    for p in ps: o=A.add(o,p)
    return o
if __name__=="__main__":
    for m in range(3,int(sys.argv[1])+1): run(m,0)
