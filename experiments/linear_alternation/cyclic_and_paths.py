import itertools, sys, subprocess
# (A) rotation character, using the standard-convention reduction from schubert_coeffs
import importlib.util
def run_char(n):
    sys.argv=['x',str(n)]
    src=open('schubert_coeffs.py').read().split("# sanity")[0]
    g={}; exec(src,g)
    F=g['F']; red=g['red']; m=n
    # rotation x_i -> x_{i+1} (0-based i -> i+1 mod m) acting on exponents: new exponent at i+1 = old at i
    rot={}
    for a,c in F.items():
        b=tuple(a[(k-1)%m] for k in range(m))
        for kk,vv in red(b).items(): rot[kk]=rot.get(kk,0)+c*vv
    rot={k:v for k,v in rot.items() if v}
    s=(-1)**(n-1)
    ok=all(rot.get(k,0)==s*F.get(k,0) for k in set(rot)|set(F))
    print(f"n={n}: tau F_n = (-1)^(n-1) F_n in C_n: {ok}")
for n in (4,5,6,7): run_char(n)
# (B) Monk paths at m=5 for L1 L2 E3 from 13425 to 25314
m=5
def length(p): return sum(1 for i in range(len(p)) for j in range(i+1,len(p)) if p[i]>p[j])
def monk(w,lam):
    out=[]
    for a in range(m):
        for b in range(a+1,m):
            u=list(w); u[a],u[b]=u[b],u[a]; u=tuple(u)
            if length(u)==length(w)+1 and lam[a]!=lam[b]: out.append((u,lam[a]-lam[b]))
    return out
def lin(prefix,last):  # E_prefix (+ x_m if last)
    return [1 if (k<prefix or (last and k==m-1)) else 0 for k in range(m)]
factors={'L1':lin(1,True),'L2':lin(2,True),'E3':lin(3,False)}
start=(1,3,4,2,5); end=(2,5,3,1,4)
for order in itertools.permutations(['L1','L2','E3']):
    paths=[([start],1)]
    for f in order:
        new=[]
        for p,wt in paths:
            for u,c in monk(p[-1],factors[f]): new.append((p+[u],wt*c))
        paths=new
    hits=[(p,wt) for p,wt in paths if p[-1]==end]
    print("order",order,": paths to",end,":",[(''.join(map(str,q)) for q in p) and ('->'.join(''.join(map(str,q)) for q in p),wt) for p,wt in hits],"total",sum(w for _,w in hits))
