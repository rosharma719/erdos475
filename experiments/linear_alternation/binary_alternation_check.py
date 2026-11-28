"""Independent check of the 'binary alternation' reduction (report 2026-11-27).
P_{n,d}(a,b) = Alt_z(Q_n)/Delta(z) with e_k(z) = (-1)^k h_k(a,b); Q_n = product of nonadjacent chords of the
n-cycle of partial sums; a at edge 0, b at edge d, z = other n-2 edges. Evaluated at a=1, b=zeta^j,
z = mu_n minus {1, zeta^j} (valid since e_k(mu_n)=0 for 1<=k<=n-1), then P(1,T) (degree n-3) fitted by least squares
over j=1..n-1 and rounded. Overall sign of each P is not fixed (rotation sign ambiguity). Usage: python3 binary_alternation_check.py N"""
import itertools, sys, numpy as np
from math import gcd
def sgn_perms(r):
    perms=np.array(list(itertools.permutations(range(r))),dtype=np.int8)
    # parity via inversion count
    inv=np.zeros(len(perms),dtype=np.int64)
    for i in range(r):
        for j in range(i+1,r): inv+= perms[:,i]>perms[:,j]
    return perms, 1-2*(inv&1)
def run(n):
    r=n-2; perms,sg=sgn_perms(r); zeta=np.exp(2j*np.pi/n)
    pairs=[(k,l) for k in range(n) for l in range(k+2,n) if not (k==0 and l==n-1)]
    out={}
    for d in range(1,n//2+1):
        vals=[]
        for j in range(1,n):
            a,b=1.0+0j,zeta**j
            Z=np.array([zeta**m for m in range(n) if m not in (0,j)])
            Zp=Z[perms]                        # (N, r)
            # edges: position 0 -> a, position d -> b, remaining in order
            X=np.zeros((len(perms),n),dtype=complex); X[:,0]=a; X[:,d]=b
            others=[p for p in range(n) if p not in (0,d)]
            X[:,others]=Zp
            Y=np.concatenate([np.zeros((len(perms),1)),np.cumsum(X,axis=1)[:,:-1]],axis=1)
            Qv=np.ones(len(perms),dtype=complex)
            for k,l in pairs: Qv*=Y[:,l]-Y[:,k]
            delta=1
            for u in range(r):
                for v in range(u+1,r): delta*=Z[v]-Z[u]
            vals.append((sg*Qv).sum()/delta)
        V=np.array([[zeta**(j*k) for k in range(n-2)] for j in range(1,n)])
        q,res,_,_=np.linalg.lstsq(V,np.array(vals),rcond=None)
        qi=np.rint(q.real).astype(object); err=max(abs(q-np.rint(q.real)))
        out[d]=([int(v) for v in qi],err)
    return out
if __name__=="__main__":
    for n in range(4,int(sys.argv[1])+1):
        res=run(n); g=0
        for d,(q,err) in res.items():
            for v in q: g=gcd(g,abs(v))
            print(f"n={n} d={d} err={err:.1e} P(1,T) coeffs={q}")
        print(f"n={n} binary content beta={g}")
