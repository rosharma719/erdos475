# Template: W = (+r, -delta^rev, -r, delta) i.e. half-walk with offset c=r rotated to start at +r.
# delta = signed ordering of S\{r}. Need: valid cycle, vertices in [-M+1, M].
# Test (a) delta in descending magnitude order with free signs; (b) any order (search).
import itertools, random
def check(W,M):
    v=[0]
    for x in W: v.append(v[-1]+x)
    if v[-1]!=0: return False
    vs=v[:-1]
    return len(set(vs))==len(vs) and min(vs)>=-M+1 and max(vs)<=M
def tmpl(S,r,delta):
    return [r]+[-x for x in reversed(delta)]+[-r]+delta
def desc_ok(S,r):
    M=max(S); rest=sorted(set(S)-{r},reverse=True)
    for eps in itertools.product((1,-1),repeat=len(rest)):
        d=[e*x for e,x in zip(eps,rest)]
        if check(tmpl(S,r,d),M): return d
    return None
def any_ok(S,r):
    M=max(S); rest=sorted(set(S)-{r})
    for perm in itertools.permutations(rest):
        for eps in itertools.product((1,-1),repeat=len(rest)):
            d=[e*x for e,x in zip(eps,perm)]
            if check(tmpl(S,r,d),M): return d
    return None
rng=random.Random(3); stats={'desc':0,'any':0,'none':0}; n=0; ex=[]
for t in range(400):
    S=sorted(rng.sample(range(1,16),rng.randint(3,6))); r=rng.choice(S)
    n+=1
    if desc_ok(S,r): stats['desc']+=1
    elif any_ok(S,r): stats['any']+=1
    else: stats['none']+=1; ex.append((S,r))
print(n,stats); print(ex[:12])
