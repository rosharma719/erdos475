"""Test the induction-ready STRONG fusion statement for small p:
For every zero-sum A (|A| in [5, maxn]) that is not itself a minimal atom, there exist a minimal atom B ⊂ A
(|B|>=2) with Z=A\\B zero-sum, such that for EVERY valid cycle z of Z, some rotation/reversal of z and some
order (b1..bm) of B make (b1, z1, b2..bm, z2..zn) valid.  Report counterexamples."""
import sys
from itertools import combinations, permutations
def valid(w,p):
    s=0;seen={0}
    for i,x in enumerate(w):
        s=(s+x)%p
        if i<len(w)-1:
            if s in seen: return False
            seen.add(s)
    return s==0
def minimal(B,p): return sum(B)%p==0 and all(sum(T)%p for r in range(1,len(B)) for T in combinations(B,r))
def cycles(Z,p):
    Z=list(Z); f=Z[0]; out=[]
    for rest in permutations(Z[1:]):
        w=(f,)+rest
        if valid(w,p): out.append(w)
    return out
def variants(z):
    n=len(z); r=z[::-1]
    return [z[i:]+z[:i] for i in range(n)]+[r[i:]+r[:i] for i in range(n)]
def fuses(B,z,p):
    for v in variants(z):
        for pb in permutations(B):
            if valid((pb[0],v[0])+pb[1:]+v[1:],p): return True
    return False
p=int(sys.argv[1]); maxn=int(sys.argv[2])
fails=[];tested=0
for n in range(4,maxn+1):
    for A in combinations(range(1,p),n):
        if sum(A)%p or minimal(A,p): continue
        tested+=1; okA=False; weak=False
        for r in range(2,n-1):
            for B in combinations(A,r):
                if not minimal(B,p): continue
                Z=tuple(x for x in A if x not in B)
                cz=cycles(Z,p)
                if not cz: continue
                if any(fuses(B,z,p) for z in cz): weak=True
                if all(fuses(B,z,p) for z in cz): okA=True;break
            if okA: break
        if not okA: fails.append((A,'weak-ok' if weak else 'WEAK-FAILS'))
print('p',p,'tested',tested,'strong-fusion failures',len(fails),fails[:8])
