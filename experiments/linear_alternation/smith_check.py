"""Integral Smith invariants of the packet lattice vs the full projected lattice, ranks 4..6 (unnormalised projection Pi=sum chi(g) g)."""
import sys
from math import gcd
import coverage_check as C
from artin import *
def snf_invariants(M):
    M=[r[:] for r in M if any(r)]; inv=[]
    if not M: return inv
    ncol=len(M[0])
    t=0
    while True:
        # find nonzero pivot of min abs value in submatrix rows>=t, cols>=t
        best=None
        for i in range(t,len(M)):
            for j in range(t,ncol):
                if M[i][j] and (best is None or abs(M[i][j])<abs(M[best[0]][best[1]])): best=(i,j)
        if best is None: break
        i,j=best; M[t],M[i]=M[i],M[t]
        for r in M: r[t],r[j]=r[j],r[t]
        while True:
            p=M[t][t]; done=True
            for i in range(t+1,len(M)):
                if M[i][t]:
                    q=M[i][t]//p; M[i]=[a-q*b for a,b in zip(M[i],M[t])]
                    if M[i][t]: M[t],M[i]=M[i],M[t]; done=False; break
            if not done: continue
            for j in range(t+1,ncol):
                if M[t][j]:
                    q=M[t][j]//p
                    for r in M: r[j]-=q*r[t]
                    if M[t][j]:
                        for r in M: r[t],r[j]=r[j],r[t]
                        done=False; break
            if done:
                # divisibility condition
                bad=[(i,j) for i in range(t+1,len(M)) for j in range(t+1,ncol) if M[i][j]%p]
                if bad:
                    i,j=bad[0]; M[t]=[a+b for a,b in zip(M[t],M[i])]; continue
                break
        inv.append(abs(M[t][t])); t+=1
        if t>=min(len(M),ncol): break
    return inv
def build(m):
    import random, itertools
    R=Ring(m)
    # reuse coverage_check internals by re-deriving with a hook
    return None
if __name__=="__main__":
    for m in range(4,int(sys.argv[1])+1):
        R,rows_pack,rows_full,keys=C.run_vectors(m)
        idx={k:i for i,k in enumerate(sorted(keys))}
        def mat(rows): return [[r.get(k,0) for k in sorted(keys)] for r in rows]
        ip=snf_invariants(mat(rows_pack)); ifull=snf_invariants(mat(rows_full))
        print(f"rank {m}: packet invariants {ip}  full invariants {ifull}")
        # index of packet lattice in full lattice when equal ranks
        if len(ip)==len(ifull):
            pi=1; fi=1
            for a in ip: pi*=a
            for a in ifull: fi*=a
            print(f"   relative index = {pi//fi if pi%fi==0 else pi/fi}")
