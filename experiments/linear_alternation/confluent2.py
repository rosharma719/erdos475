import mpmath as mp
from confluent import Bspec
mp.mp.dps=400
for m in (6,7,8):
    zeta=mp.exp(2j*mp.pi/m); full=Bspec(m,[zeta**i for i in range(1,m)])
    print(f"m={m}: B_m coeffs = {[mp.nstr(mp.re(x),8) for x in full]}",flush=True)
    for n in range(m-1,1,-1):
        k=m-n; eta=mp.exp(2j*mp.pi/n); eps=mp.mpf('1e-40')
        t=[eta**i for i in range(1,n)]+[eps*(j+1)*mp.mpc(1,0.3*(j+1)) for j in range(k)]
        sp=Bspec(m,t)
        diff=[abs(a-b) for a,b in zip(full,sp)]
        top=max([d for d in range(len(diff)) if diff[d]>1e-20],default=-1)
        print(f"  n={n} ({k} zero edges): differs up to degree {top} (bound m-n={m-n});  B_(m;n) = {[mp.nstr(mp.re(x),8) for x in sp]}",flush=True)
