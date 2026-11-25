"""Own audit of GPT near-balanced round: Theorem 1 (local-swap repair) on exhaustive small instances,
Theorem 2 (Phi-extremal exchange bound) exhaustively, Theorem 3 (short-relation greedy) randomized, trap + examples."""
from itertools import combinations, permutations
import random
def valid(w,p):
    s=0;seen={0}
    for i,x in enumerate(w):
        s=(s+x)%p
        if i<len(w)-1:
            if s in seen: return False
            seen.add(s)
    return s==0
def zsizes(A,p): return {r for r in range(1,len(A)) for T in combinations(A,r) if sum(T)%p==0}
def nb(A,p):
    n=len(A); return sum(A)%p==0 and zsizes(A,p)<= {n//2,(n+1)//2}
def winbad(Q,p,m): n=len(Q); return sum(sum(Q[(i+j)%n] for j in range(m))%p==0 for i in range(n))
def repair(Q,p):
    Q=list(Q);n=len(Q);m=n//2;steps=0
    while winbad(Q,p,m):
        s=next(i for i in range(n) if sum(Q[(i+j)%n] for j in range(m))%p==0)
        bnd=[((s+m-1)%n,(s+m)%n)]+([((s-1)%n,s)] if n%2 else [])
        b0=winbad(Q,p,m);done=False
        for i,j in bnd:
            R=Q[:];R[i],R[j]=R[j],R[i]
            if winbad(R,p,m)<b0: Q=R;done=True;break
        assert done; steps+=1
    return Q
# Theorem 1 exhaustive over p<=17 near-balanced sets (all of them, random start orders)
cnt=0
for p in (11,13,17):
    for n in range(4,9):
        for A in combinations(range(1,p),n):
            if nb(A,p):
                for _ in range(5):
                    q=random.sample(A,n); r=repair(q,p); assert valid(r,p); cnt+=1
print("Thm1 repairs verified:",cnt)
# Theorem 2: Phi-extremal partition bound, exhaustive small sets
def atoms_of(A,p): return [T for r in range(1,len(A)+1) for T in combinations(A,r) if sum(T)%p==0 and all(sum(U)%p for k in range(1,r) for U in combinations(T,k))]
def best_partition(A,p):
    At=atoms_of(A,p); best=None
    def rec(rest,parts):
        nonlocal best
        if not rest:
            key=(len(parts),sum(len(x)**2 for x in parts))
            if best is None or key>best[0]: best=(key,list(parts))
            return
        f=min(rest)
        for T in At:
            if f in T and set(T)<=rest: parts.append(T); rec(rest-set(T),parts); parts.pop()
    rec(set(A),[]); return best[1]
viol=0;pairs=0
for p in (11,13):
    for n in range(6,10):
        for A in combinations(range(1,p),n):
            if sum(A)%p: continue
            P=best_partition(A,p)
            for B,C in combinations(P,2):
                u,v=sorted((len(B),len(C))); pairs+=1
                if any(not(u<=r<=v) for r in zsizes(B+C,p)): viol+=1
print("Thm2 atom pairs checked:",pairs,"violations:",viol)
# Theorem 3 greedy word check, random
def thm3(B,C,p):
    B=list(B);pool=list(C);d={};n=len(C);m=len(B)
    def take(slot,forb):
        x=next(x for x in pool if x%p not in {f%p for f in forb}); d[slot]=x; pool.remove(x)
    take(1,(-B[0],-B[1],-B[0]-B[1],-B[1]-B[2])); take(2,(-B[-1],-B[-2]-B[-1])); take(3,(-B[-1]-d[2],))
    take(n,(-B[0],-B[0]-d[1])); take(n-1,(-B[0]-d[n],))
    for j in range(1,n+1):
        if j not in d: d[j]=pool.pop()
    oc=[d[i] for i in range(1,n+1)]; W=[B[0],oc[0]]+B[1:]+oc[1:]; N=len(W)
    for i in range(N):
        for r in (2,3):
            T=[W[(i+j)%N] for j in range(r)]
            if any(x in B for x in T) and any(x in oc for x in T): assert sum(T)%p
    return True
k=0
for _ in range(3000):
    p=random.choice([13,17,19,23,29,41,101]); m=random.randint(3,6); n=random.randint(6,min(12,p-1-m))
    V=random.sample(range(1,p),m+n); thm3(V[:m],V[m:],p); k+=1
print("Thm3 layouts:",k)
# trap and examples
Q=[4,1,6,10,9,5,7,2];p=11
def nbad(Q,p):
    n=len(Q); return sum(1 for r in range(2,n//2+1) for i in range(n//2 if 2*r==n else n) if sum(Q[(i+j)%n] for j in range(r))%p==0)
print("trap bad:",nbad(Q,p),"min over single swaps:",min(nbad([Q[j] if t==i else Q[i] if t==j else Q[t] for t in range(8)],p) for i,j in combinations(range(8),2)),"repaired valid:",valid([1,9,6,10,4,5,7,2],11))
print("ex19 nb:",nb((2,3,4,5,7,8,9),19),"ex47 valid:",valid((10,22,27,8,35,21,24,41),47), sum((10,22,27,8,35,21,24,41))%47)
