"""Independent-switch repair for five unpaired elements. Finite search only.
Requires erdos475_asymmetry_audit.py, standard library only.
"""
from itertools import combinations, permutations
from random import Random
from erdos475_asymmetry_audit import sym, valid, maximal_completion

def search(A,p,U,maxswitch=None):
    for X in combinations(sorted(U),2):
        X=set(X);Y=U-X;c=sum(X)%p
        if c not in A:opts=[(X,Y,c,-c%p)]
        else:opts=[((X-{x})|{-c%p},(Y-{y})|{c},-x%p,-y%p) for x in sorted(X) for y in sorted(Y)]
        for D,E,d,e in opts:
            B=A-(D|E)|{d,e}; assert B=={-x%p for x in B}
            for l in range(1,p//2+1):
                w0=sym(B,p,l)
                for sg in (1,-1):
                    w=tuple(sg*x%p for x in w0)
                    V=[];s=0;u=v=None
                    for a in w:
                        V.append(s)
                        if a==d:u=s
                        if a==e:v=s
                        s=(s+a)%p
                    pos={v:i for i,v in enumerate(V)}
                    n=len(w);alt=[(V[i]+w[i]-w[i-1])%p for i in range(n)]
                    movable=[i!=0 and w[i-1] not in (d,e) and w[i] not in (d,e) for i in range(n)]
                    for dd in permutations(sorted(D)):
                        h=(u+dd[0])%p
                        for ee in permutations(sorted(E)):
                            j=(v+ee[0])%p;k=(j+ee[1])%p;K={h,j,k}
                            if len(K)!=3:continue
                            need={pos[x] for x in K if x in pos};todo=list(need);used=set();good=True
                            while todo:
                                i=todo.pop()
                                if (maxswitch is not None and len(need)>maxswitch) or not movable[i] or (i-1)%n in need or (i+1)%n in need or alt[i] in K or alt[i] in used:
                                    good=False;break
                                used.add(alt[i]);t=pos.get(alt[i])
                                if t is not None and t not in need:need.add(t);todo.append(t)
                            if not good:continue
                            out=list(w)
                            for i in need:out[i-1],out[i]=out[i],out[i-1]
                            z=tuple(a for b in out for a in (dd if b==d else ee if b==e else (b,)))
                            assert len(z)==len(A)==len(set(z)) and set(z)==A and sum(z)%p==0 and valid(z,p)
                            return (l,sg,dd,ee,d,e,tuple(sorted(need)),z)
    return None

def cases(p,count,seed):
    rng=Random(seed);seen=set()
    while len(seen)<count:
        U=set(rng.sample(range(1,p),4));U.add(-sum(U)%p)
        if len(U)!=5 or 0 in U or any(-a%p in U for a in U) or any((a+b)%p in U for a,b in combinations(U,2)):continue
        key=tuple(sorted(U))
        if key in seen:continue
        seen.add(key);yield U

if __name__=='__main__':
    import argparse,time
    a=argparse.ArgumentParser();a.add_argument('--count',type=int,default=20);a.add_argument('--primes',type=int,nargs='+',default=[211,503,1009]);args=a.parse_args()
    for p,U in [(211,{31,87,133,179,203}),(503,{112,168,388,406,435})]:
        ans=search(maximal_completion(p,U),p,U,1);print('known',p,ans[:-1] if ans else None,flush=True)
    for p in args.primes:
        t=time.monotonic();hist={};fail=[]
        for U in cases(p,args.count,475+p):
            ans=search(maximal_completion(p,U),p,U,1)
            if ans is None:
                fail.append(tuple(sorted(U))); print('ONE SWITCH FAILURE',p,fail[-1],flush=True)
            else:hist[len(ans[-2])]=hist.get(len(ans[-2]),0)+1
        print(p,'counts',hist,'failures',fail,'seconds',round(time.monotonic()-t,2),flush=True)
