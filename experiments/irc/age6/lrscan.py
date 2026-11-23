"""LR(M,a,k): Hamiltonian path on [0,M-1]\\{k+1,k+a} from k, labels [1,M-1]\\{a,M+1-a}.
(= X-bridge core D=[-k,M-1-k]\\{1,a} shifted by k.) Print good k per (a,M)."""
import sys
from shape_sat import hpath
def lr(M,a,k,timeout=20):
    V=set(range(M))-{k+1,k+a}
    if k not in V or len(V)!=M-2: return None
    return hpath(V,set(range(1,M))-{a,M+1-a},k,timeout=timeout)
if __name__=="__main__":
    for spec in sys.argv[1:]:
        a,M=map(int,spec.split(':'))
        good=[k for k in range(0,M-a) if isinstance(lr(M,a,k),list)]
        print(a,M,'good k:',good,flush=True)
