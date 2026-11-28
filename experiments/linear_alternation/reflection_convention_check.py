"""What is the true dihedral character of Q_m, and which reflection convention makes the rank-6 witness Q-equivariant?
Action: (g.f)(w) = f(w') with w'_i = w_{g(i)}  (matches orbit sums: monomial exponent b[g(i)] = a[i])."""
import random
from coverage_check import Qval, perm_sign
from witness_data import WITNESS
def act_vec(w,g): return [w[g[i]] for i in range(len(w))]
def rand_zero_sum(m):
    while True:
        w=[random.randint(-9,9) or 1 for _ in range(m-1)]; w.append(-sum(w))
        if all(w): return w
def q_char(m,trials=30):
    out={}
    rots=[[(i+r)%m for i in range(m)] for r in range(m)]
    refs=[[(c-i)%m for i in range(m)] for c in range(m)]
    for name,gs in (("rot",rots),("ref",refs)):
        for c,g in enumerate(gs):
            vals=set()
            for _ in range(trials):
                w=rand_zero_sum(m); a,b=Qval(w),Qval(act_vec(w,g))
                if a: vals.add(b//a if b%a==0 else None)
            out[(name,c)]=vals
    return out
random.seed(1)
print("== true character of Q_m under rotations i->i+r and reflections i->c-i ==")
for m in (4,5,6,7,8):
    ch=q_char(m)
    rot=[sorted(ch[("rot",r)])[0] for r in range(m)]; ref=[sorted(ch[("ref",c)])[0] for c in range(m)]
    assert all(len(ch[k])==1 for k in ch)
    print(f"m={m}: rotations r=0..{m-1}: {rot}   reflections c=0..{m-1}: {ref}")
# --- witness: build q under two conventions and test equivariance with the *true* character of Q_6
m=6
chi_rot=lambda r:(-1)**r
def build(conv):
    els=[]
    for r in range(m):
        els.append(([(i+r)%m for i in range(m)],(-1)**r))
        if conv==0: els.append(([(r-i)%m for i in range(m)],(-1)**(r+1)))     # i -> r-i with sign (-1)^(r+1)
        else:       els.append(([(r-1-i)%m for i in range(m)],(-1)**(r+1)))   # i -> r-1-i with sign (-1)^(r+1)
    terms=[]; 
    for a,c in WITNESS:
        d={}
        for g,s in els:
            b=[0]*m
            for i in range(m): b[g[i]]=a[i]
            d.setdefault(tuple(b),set()).add(s)
        if any(len(v)>1 for v in d.values()): continue
        terms.append((c,{b:list(v)[0] for b,v in d.items()}))
    def q(w):
        t=0
        for c,tt in terms:
            for b,s in tt.items():
                v=s*c
                for e,x in zip(b,w): v*=x**e
                t+=v
        return t
    return q
ch6=q_char(6)
for conv in (0,1):
    q=build(conv); bad=[]
    for kind,gs in (("rot",[[(i+r)%m for i in range(m)] for r in range(m)]),("ref",[[(c-i)%m for i in range(m)] for c in range(m)])):
        for c,g in enumerate(gs):
            chi=sorted(ch6[(kind,c)])[0]
            ok=True
            for _ in range(20):
                w=[random.randint(-9,9) for _ in range(m)]   # equivariance of a polynomial holds for arbitrary points
                if q(act_vec(w,g))!=chi*q(w): ok=False;break
            if not ok: bad.append((kind,c))
    print(f"witness built with convention {conv} ({'i->r-i' if conv==0 else 'i->r-1-i'}): equivariant under true chi_Q for all 12 elements?", "YES" if not bad else f"NO, fails for {bad}")
