"""Ordinary simultaneous saturation by degree: missing directions = rank(T,L) - rank(T) over chi_Q-equivariant polynomials of degree k."""
import sys, time
from sat_lib import *
m=int(sys.argv[1]); k0=int(sys.argv[2]); k1=int(sys.argv[3])
els=group(m,lambda k,c:chiQ(m,k,c)); Rm=Ring(m); Rm1=Ring(m+1)
for k in range(k0,k1+1):
    t0=time.time(); seen=set(); rowsT=[]; rowsL=[]
    for a in monos(m,k):
        if a in seen: continue
        O=orbit_sum(a,els,m)
        for g,_ in els:
            b=[0]*m
            for i in range(m): b[g[i]]=a[i]
            seen.add(tuple(b))
        if not O: continue
        Lv=Rm.nf(O); Tv=Rm1.nf(transfer(m,O))
        rowsT.append({('T',kk):v for kk,v in Tv.items()}); rowsL.append({('L',kk):v for kk,v in Lv.items()})
    rT=rank_mod(rowsT); rJ=rank_mod([{**t,**l} for t,l in zip(rowsT,rowsL)])
    print(f"rank {m}, degree {k} (D_m={m*(m-1)//2-m}): rank T={rT}, joint={rJ}, missing={rJ-rT}  ({time.time()-t0:.0f}s)",flush=True)
