"""H_k: Hamiltonian path on {-k-1..-1} ∪ {2..k+1}, start k+1, labels 2..2k+1 each once.
Search: inward zigzag prefix k+1,-k,k,-(k-1),... of length Lz, then DFS tail."""
import sys,time
def tail_search(k,Lz,tl=10):
    V=set(range(-k-1,0))|set(range(2,k+2))
    z=[k+1];hi=k;lo=-k
    # zigzag: k+1,-k,k,-(k-1),k-1,...
    seq=[k+1]; p=k; n=-k
    while len(seq)<Lz:
        seq.append(n); n+=1
        if len(seq)<Lz: seq.append(p); p-=1
    labs=[abs(seq[i+1]-seq[i]) for i in range(len(seq)-1)]
    if len(set(labs))<len(labs) or not set(seq)<=V: return None
    used=set(labs); rest=V-set(seq); need=set(range(2,2*k+2))-used
    path=list(seq); t0=time.time()
    def rec():
        if time.time()-t0>tl: raise TimeoutError
        if len(path)==len(V): return list(path)
        x=path[-1]
        for L in sorted(need-used,reverse=True):
            for y in (x+L,x-L):
                if y in rest and y not in path:
                    path.append(y);used.add(L)
                    r=rec()
                    if r: return r
                    path.pop();used.discard(L)
        return None
    try: return rec()
    except TimeoutError: return 'TO'
for k in range(int(sys.argv[1]),int(sys.argv[2])+1):
    best=None
    for Lz in range(2*k+1,1,-1):
        r=tail_search(k,Lz,tl=5)
        if r and r!='TO': best=(Lz,r);break
    if best:
        Lz,r=best; tail=r[Lz:]
        print(k,"zigzag len",Lz,"tail",[(v if v>-k-1 else "-(k+1)") for v in tail],flush=True)
    else: print(k,None,flush=True)
