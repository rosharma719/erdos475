"""rank of Phi: C_m -> (+)_d C_m/(a_d) and dim v*im(Phi) versus the report's formulas (m!/2)(dim A + dim gA), (m!/2)(dim vA + dim vgA)."""
import sys, math
from modrank import P
from marked_root_checks import Alg, hlist
import marked_root_checks as M
def echelon(rows):
    piv={}
    for r in rows:
        r={k:v%P for k,v in r.items() if v%P}
        while r:
            k=min(r)
            if k in piv:
                f=r[k]
                for kk,vv in piv[k].items(): r[kk]=(r.get(kk,0)-f*vv)%P
                r={a:b for a,b in r.items() if b}
            else:
                inv=pow(r[k],P-2,P); piv[k]={a:b*inv%P for a,b in r.items()}; break
    return piv
def reduce(vec,piv):
    r=dict(vec)
    for k in sorted(list(r)):
        pass
    changed=True
    while True:
        ks=[k for k in r if k in piv]
        if not ks: return r
        k=min(ks); f=r[k]
        for kk,vv in piv[k].items(): r[kk]=(r.get(kk,0)-f*vv)%P
        r={a:b for a,b in r.items() if b}
def rank_dicts(rows):
    return len(echelon(rows))
def A_dims(m):
    H=hlist(m)
    from split_edge_checks_lib import wdeg,mono_basis,shift,span_rows
    Hm,Hm1=H[m],H[m+1]; g={}
    for j in range(m):
        for (a,b),c in H[j].items(): g[(a+m-1-j,b)]=g.get((a+m-1-j,b),0)+c
    def mulp(p,q):
        o={}
        for (a,b),c in p.items():
            for (a2,b2),c2 in q.items(): o[(a+a2,b+b2)]=o.get((a+a2,b+b2),0)+c*c2
        return {k:v for k,v in o.items() if v}
    def dimspace(mult):
        tot=0; wm=wdeg(*next(iter(mult)))
        for d in range(0,2*m+4):
            I=span_rows([Hm,Hm1],d)
            if d<wm: continue
            rows=[mulp(mult,{mb:1}) for mb in mono_basis(d-wm)]
            tot+=rank_dicts(I+rows)-rank_dicts(I)
        return tot
    one={(0,0):1}; v={(0,1):1}
    return dimspace(one),dimspace(g),dimspace(v),dimspace(mulp(v,g))
def run(m):
    A=Alg(m); N=m*(m-1)//2; soc=N+2*m-2
    w=[A.var(2+i) for i in range(m)]; u=A.var(0); v=A.var(1)
    a=[A.add(w[d],u,-1) for d in range(m)]
    kerdim=0; imv=0; dimC=0; dimvC=0
    for d in range(0,soc+1):
        V=A.monos(d); I=A.ideal_rows(d); rI=rank_dicts(I); dimC+=len(V)-rI
        echs=[]
        for e in range(m):
            rows=I+([A.mul(a[e],{x:1}) for x in A.monos(d-1)] if d>=1 else [])
            echs.append(echelon(rows))
        def image(vec):
            out={}
            for e,piv in enumerate(echs):
                for k,val in reduce(vec,piv).items(): out[(e,k)]=val
            return out
        imgs=[image({x:1}) for x in V]
        rk=rank_dicts(imgs); kerdim+=len(V)-rk-rI
        # image of v*C
        if d>=2:
            vimgs=[image(A.mul(v,{x:1})) for x in A.monos(d-2)]
            imv+=rank_dicts(vimgs)
    imPhi=dimC-kerdim
    dA,dgA,dvA,dvgA=A_dims(m); f=math.factorial(m)//2
    print(f"m={m}: dim C={dimC}, rank Phi={imPhi}; formula (m!/2)(dim A + dim gA) = {f}*({dA}+{dgA}) = {f*(dA+dgA)}")
    print(f"     dim v*im(Phi) = {imv}; formula (m!/2)(dim vA + dim vgA) = {f}*({dvA}+{dvgA}) = {f*(dvA+dvgA)}")
    print(f"     'separate layers' count (m!/2) dim vA = {f*dvA}; extra (m!/2) dim vgA = {f*dvgA}")
if __name__=="__main__": run(int(sys.argv[1]))
