"""Independent check of GPT's SF counterexample at p=19: A=F_19^x.
(1) B={1,18}, given Z cycle: valid? all four-block words fail? all order-preserving insertions of {1,18} fail?
(2) For EVERY atom B of F_19^x (up to scaling), randomized search for an obstructing valid Z-cycle."""
import random,itertools
from itertools import combinations, permutations
p=19
def valid(w):
    s=0;seen={0}
    for i,x in enumerate(w):
        s=(s+x)%p
        if i<len(w)-1:
            if s in seen: return False
            seen.add(s)
    return s==0
def fuse_ok(B,z):
    n=len(z)
    for zz in (z,z[::-1]):
        for r in range(n):
            v=zz[r:]+zz[:r]
            for o in permutations(B):
                if valid((o[0],v[0])+o[1:]+v[1:]): return True
    return False
Z=(11,4,9,8,10,3,13,16,14,2,15,12,6,7,5,17)
print("Z elems ok:",sorted(Z)==sorted(set(range(1,19))-{1,18}),"Z valid:",valid(Z),"four-block fusion possible:",fuse_ok((1,18),Z))
# all order-preserving insertions of 1 and 18 into rotations/reversals
cnt=0;anyok=False
for zz in (Z,Z[::-1]):
    for r in range(16):
        v=list(zz[r:]+zz[:r])
        for i,j in combinations(range(18),2):
            for a,b in ((1,18),(18,1)):
                w=[];it=iter(v)
                for k in range(18): w.append(a if k==i else b if k==j else next(it))
                cnt+=1; anyok|=valid(w)
print("order-preserving shuffles:",cnt,"any valid:",anyok)
# (2) atoms up to scaling, random obstructing-cycle search
def minimal(B): return sum(B)%p==0 and all(sum(T)%p for r in range(1,len(B)) for T in combinations(B,r))
atoms=[B for r in range(2,8) for B in combinations(range(1,p),r) if minimal(B)]
reps={}
for B in atoms:
    key=min(tuple(sorted(x*c%p for x in B)) for c in range(1,p))
    reps.setdefault(key,B)
print("atoms",len(atoms),"scaling classes",len(reps),"sizes",sorted(len(k) for k in reps))
def rand_cycle(Zs,tries=200):
    Zs=list(Zs)
    for _ in range(tries):
        random.shuffle(Zs); path=[];s=0;seen={0};avail=Zs[:]
        ok=True
        while len(avail)>1:
            random.shuffle(avail)
            for i,x in enumerate(avail):
                t=(s+x)%p
                if t not in seen: path.append(x);seen.add(t);s=t;avail.pop(i);break
            else: ok=False;break
        if ok and (s+avail[0])%p==0: return tuple(path+avail)
    return None
random.seed(1); found=0; res={}
for key,B in reps.items():
    Zs=[x for x in range(1,p) if x not in B]; hit=None
    for _ in range(3000):
        z=rand_cycle(Zs)
        if z and not fuse_ok(B,z): hit=z;break
    res[key]=hit; found+= hit is not None
print("classes with an obstructing cycle found by random search:",found,"/",len(reps))
print("classes not yet obstructed:",[k for k in res if res[k] is None])
