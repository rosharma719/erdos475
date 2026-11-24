"""How symmetric are lifted pairs? For random zero-sum A in Z_p^* of density alpha, best over dilations lambda and
lifts T: core C=P∩N, remainder sizes |P0|+|N0|. Dense sets should be near-symmetric."""
import random,sys
def lift(A,p):
    r=sorted(x%p for x in A)
    best=None
    for T in range(len(r)+1):
        P=r[:len(r)-T]; N=[p-x for x in r[len(r)-T:]]
        if sum(P)==sum(N): best=(P,N);break
    return best
p=int(sys.argv[1]);random.seed(1)
for alpha in (0.2,0.35,0.5,0.65,0.8,0.9):
    k=int(alpha*(p-1));tot=0;rows=[]
    for _ in range(20):
        while True:
            A=random.sample(range(1,p),k-1);s=(-sum(A))%p
            if s and s not in A: A.append(s);break
        best=None
        for lam in range(1,p):
            L=lift([lam*x for x in A],p)
            if not L: continue
            P,N=L;C=set(P)&set(N);rem=len(P)+len(N)-2*len(C)
            if best is None or rem<best: best=rem
        rows.append(best)
    print(f"p={p} alpha={alpha} k={k}: min over dilations of remainder |P0|+|N0| (avg) = {sum(rows)/len(rows):.1f}  vs k={k}",flush=True)
