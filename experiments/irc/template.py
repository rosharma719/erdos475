"""Template: path = L + [M+1, a, 0, M-3, -1, M-2, 2] + Z, Z = inward zigzag continuing from 2 on low [3..] / high [..M-4],
taking k more vertices (skipping a). L = searched path on the remaining vertices ending at x with |x-(M+1)| unused label.
Report the smallest |L| for which a solution exists, for growing M (fixed a)."""
import sys, time
def zig_tail(M,a,k):
    lo=[v for v in range(3,M) if v!=a]; hi=[v for v in range(M-4,1,-1) if v!=a]
    seq=[];i=j=0
    # after 2 comes M-4 (high), then 3 (low), ...
    turn_hi=True
    while len(seq)<k:
        if turn_hi: v=hi[j];j+=1
        else: v=lo[i];i+=1
        if v in seq: break
        seq.append(v);turn_hi=not turn_hi
    return seq
def solve(M,a,tl=20):
    b=M+1-a; U=set([-1,0])|set(range(2,M-1))|{M+1}
    head=[M+1,a,0,M-3,-1,M-2,2]
    t0=time.time()
    for k in range(M,-1,-1):   # longest zigzag tail first => smallest L
        Z=zig_tail(M,a,k)
        if len(Z)<k: continue
        right=head+Z
        if len(set(right))<len(right) or not set(right)<=U: continue
        labs=[abs(right[i+1]-right[i]) for i in range(len(right)-1)]
        if len(set(labs))<len(labs): continue
        rest=U-set(right); remL=set(range(1,M))-set(labs)
        # search L: path on rest, last vertex x adjacent to M+1
        n=len(rest)
        if n==0:
            continue
        rest_l=sorted(rest)
        def rec(path,vis,used):
            if time.time()-t0>tl: raise TimeoutError
            if len(path)==n:
                L=abs(M+1-path[-1])
                return list(path) if (L in remL and L not in used and len(used)+1==len(remL)) else None
            x=path[-1]
            for y in rest_l:
                if y in vis: continue
                L=abs(y-x)
                if L in remL and L not in used:
                    path.append(y);vis.add(y);used.add(L)
                    r=rec(path,vis,used)
                    if r: return r
                    path.pop();vis.discard(y);used.discard(L)
            return None
        try:
            for st in rest_l:
                r=rec([st],{st},set())
                if r: return k,r+right
        except TimeoutError: return 'TO'
    return None
a=int(sys.argv[1])
for M in map(int,sys.argv[2].split(',')):
    r=solve(M,a)
    if r in (None,'TO'): print(M,r,flush=True);continue
    k,p=r; Lsz=len(p)-7-k
    print(M,"tail k",k,"|L|",Lsz,"L:",[ (v if v<M/2 else f"M{v-M:+d}") for v in p[:Lsz]],flush=True)
