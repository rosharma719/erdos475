"""Obstacle avoidance: zero-sum R (size r) in Z_p^*, forbidden F (size f, 0 not in F).
Is there an ordering of R whose nonzero partial sums are distinct and avoid F? Random F vs interval-cluster F."""
import random,sys,time
def solvable(R,F,p,tl=5):
    n=len(R);t0=time.time()
    def rec(mask,s,seen):
        if time.time()-t0>tl: raise TimeoutError
        if mask==(1<<n)-1: return True
        for j in range(n):
            if mask>>j&1: continue
            t=(s+R[j])%p; last=(mask|1<<j)==(1<<n)-1
            if last:
                if t==0: return True
                continue
            if t==0 or t in F or t in seen: continue
            seen.add(t)
            if rec(mask|1<<j,t,seen): return True
            seen.discard(t)
        return False
    try: return rec(0,0,set())
    except TimeoutError: return None
p=int(sys.argv[1]);kind=sys.argv[2];random.seed(5)
for r in (6,10,14):
    for frac in (0.3,0.5,0.6,0.7,0.8):
        f=int(frac*(p-1))-r
        if f<0: continue
        ok=0;tot=0;to=0
        for _ in range(15):
            while True:
                R=random.sample(range(1,p),r-1);s=(-sum(R))%p
                if s and s not in R: R.append(s);break
            if kind=='random': F=set(random.sample(range(1,p),f))
            else:
                # two clusters: [1,f/2] and [L, L+f/2) with random L (mod p), like D and b1+D
                h=f//2; L=random.randrange(p); F=set(range(1,h+1))|{(L+i)%p for i in range(f-h)}; F.discard(0)
            res=solvable(R,F,p); tot+=1
            if res is None: to+=1
            elif res: ok+=1
        print(f"p={p} {kind} r={r} (r+f)/(p-1)={frac}: solvable {ok}/{tot} (timeouts {to})",flush=True)
