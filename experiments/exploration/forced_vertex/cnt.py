from collections import Counter
from itertools import combinations
from math import factorial
def masks(m):
    while m:
        b = m & -m; yield b; m ^= b
def elements(m): return [b.bit_length()-1 for b in masks(m)]
def subsets(m):
    s = m
    while s:
        yield s; s = (s-1)&m
def audit(p):
    full = (1<<p)-1
    sets = [a for a in range(2,full+1,2) if a.bit_count()>=2 and sum(elements(a))%p==0]
    sets.sort(key=int.bit_count)
    C = {}; V = {}
    ns=ne=one=weighted=zero=0; eligible=local=global_=petal=combined=0
    for A in sets:
        n = A.bit_count(); r = elements(A)[0]
        G = Counter(); F = Counter(); N = [0,0,0]; vm = Counter()
        def tally(w,hist,seen,rep):
            if rep<0: vm[seen] += 1
            if n<3: return
            g=0
            for i,h in enumerate(hist):
                if rep>=0 and h!=rep: continue
                a,b = w[i-1],w[i]; s = (a+b)%p
                if s and not (A>>s&1):
                    key=tuple(sorted((a,b))); (G if rep<0 else F)[key]+=1; g+=1
            if rep>=0: N[g]+=1
        def dfs(rem,h,seen,rep,w,hist):
            for bit in masks(rem):
                a=bit.bit_length()-1; z=(h+a)%p; R=rem^bit
                if not R:
                    assert z==0; tally(w+[a],hist,seen,rep)
                elif not seen>>z&1: dfs(R,z,seen|(1<<z),rep,w+[a],hist+[z])
                elif rep<0: dfs(R,z,seen,z,w+[a],hist+[z])
        dfs(A^(1<<r),r,1|(1<<r),-1,[r],[0,r])
        C[A]=sum(vm.values()); V[A]=vm
        if n<3: continue
        parts=[(u,A^u) for u in subsets(A) if u!=A and (u>>r&1) and C.get(u,0) and C.get(A^u,0)]
        glue=0
        for u,v in parts:
            for x,cx in V[u].items():
                for y,cy in V[v].items():
                    for d in range(p):
                        yy=((y<<d)|(y>>(p-d)))&full
                        if (x&yy).bit_count()==1: glue+=cx*cy
        assert glue==sum(N)
        S=bad=0; has=win=pwin=False
        for a,b in combinations(elements(A),2):
            s=(a+b)%p
            if not s or A>>s&1: continue
            R=A^(1<<a)^(1<<b); B=R|(1<<s); count=C[B]
            assert 2*count==G[a,b]+F[a,b]
            H=sum(C[u]*C[v] for u,v in parts if bool(u>>a&1)!=bool(u>>b&1))
            assert F[a,b]%2==0 and F[a,b]//2<=H
            win |= count>H
            J=0
            for z in (a,b):
                for L in subsets(R):
                    c=C.get(L|(1<<z),0)
                    if not c: continue
                    for E in subsets(R^L):
                        D=R^L^E
                        if D: J+=c*C.get(E|(1<<z),0)*factorial(D.bit_count())
            pwin |= count>J; S+=count; bad+=F[a,b]; ne+=1; has=True
        assert bad==N[1]+2*N[2]
        if has:
            eligible+=1; local+=win; global_+=S>glue; petal+=pwin
            ok=win or pwin or S>glue; combined+=ok
            if not ok: assert A==sum(1<<(p-a) for a in elements(A))
        ns+=1; one+=glue; weighted+=bad; zero+=N[0]
    return (ns,ne,one,weighted,zero,eligible,local,global_,petal,combined)
expected={5:(1,0,4,0,4,0,0,0,0,0),7:(6,12,66,12,60,5,5,2,5,5),11:(88,460,34000,7660,27630,87,82,62,82,82),13:(309,2352,1134780,294144,886020,308,286,229,296,302)}
for p,target in expected.items():
    res=audit(p); assert res==target,(p,res); print(p,res,flush=True)
print("counting identities verified through p=13")
