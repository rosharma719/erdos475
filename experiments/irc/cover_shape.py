import sys, collections
def covers(M,a):
    b=M+1-a; P=list(range(1,M+1)); N=sorted(set(range(1,M+2))-{a,b})
    for u in range(1,M+1):
        for v in range(1,M+1):
            V=[x for x in range(-M,M+1) if x not in (-u,v)]; Vs=set(V)
            srcs=[x for x in V if x<=0]+[x for x in V if x>0]; f={}
            res=[]
            def rec(i,uP,uN,tg):
                if i==len(srcs): res.append(dict(f));return
                s=srcs[i]
                for lab in (P if s<=0 else N):
                    if lab in (uP if s<=0 else uN): continue
                    t=s+lab if s<=0 else s-lab
                    if t in Vs and t not in tg:
                        f[s]=t;(uP if s<=0 else uN).add(lab);tg.add(t)
                        rec(i+1,uP,uN,tg)
                        (uP if s<=0 else uN).discard(lab);tg.discard(t)
            rec(0,set(),set(),set())
            for g in res: yield (u,v),V,g
M=int(sys.argv[1]);a=int(sys.argv[2])
dist=collections.Counter();n=0
for h,V,g in covers(M,a):
    n+=1
    # c(x)=f(x)-2x ; count deviations from the doubling constants (M on x<=0, -(M+1) on x>0)
    dev=[x for x in V if g[x]-2*x != (M if x<=0 else -(M+1))]
    pieces=len(set((x<=0,g[x]-2*x) for x in V))
    dist[(len(dev),pieces)]+=1
print(M,a,"covers",n)
for k in sorted(dist): print("  #sources deviating from doubling, #distinct (side,c) pieces:",k,dist[k])
