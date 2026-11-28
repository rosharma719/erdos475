import random
from fractions import Fraction
from deformed_ext import *
def rand_even(m,pairs,seed):
    random.seed(seed); tot={}
    for _ in range(pairs):
        a=random.randint(1,m); b=random.randint(1,m); c=Fraction(random.randint(-4,4),random.randint(1,3))
        if c==0: continue
        tot=gw_add(tot,gw_scale(gw_mul(u(a,m),v(b,m)),c))
    return tot
ok=True; n=0; nonscalar=0
for m in (3,4):
    top=(1<<(2*m))-1
    for trial in range(8):
        k=random.randint(1,m-1)
        f=rand_even(m,4,100+trial); 
        for _ in range(k-1): f=gw_mul(f,rand_even(m,3,200+trial+_))
        g=rand_even(m,4,300+trial)
        for _ in range(m-k-1): g=gw_mul(g,rand_even(m,3,400+trial+_))
        a=gw_mul(f,g).get(top,{}); b=gw_mul(g,f).get(top,{})
        n+=1
        if a!=b: ok=False
        if any(key!=(0,0) for key in a): nonscalar+=1
print(f"top-coefficient cyclicity tau(fg) = tau(gf) for random even elements (m=3,4): {n} trials, all equal: {ok}; trials where the top coefficient was not a pure scalar: {nonscalar}")
