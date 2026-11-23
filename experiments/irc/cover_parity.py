# enumerate ALL label-exact zigzag-sign cycle covers for tight pair; record cycle-count parity by holes
import sys, collections
def covers(M,a):
    b=M+1-a; P=list(range(1,M+1)); N=sorted(set(range(1,M+2))-{a,b})
    out=collections.Counter(); cyc1=collections.Counter()
    for u in range(1,M+1):          # negative hole -u
        for v in range(1,M+1):      # positive hole v
            V=[x for x in range(-M,M+1) if x not in (-u,v)]
            Vs=set(V); neg=[x for x in V if x<=0]; pos=[x for x in V if x>0]
            srcs=neg+pos; f={}
            def rec(i,usedP,usedN,tg):
                if i==len(srcs):
                    seen=set();c=0
                    for s in V:
                        if s in seen: continue
                        c+=1;x=s
                        while x not in seen: seen.add(x);x=f[x]
                    out[(u,v,c%2)]+=1
                    if c==1: cyc1[(u,v)]+=1
                    return
                s=srcs[i]
                if s<=0:
                    for p in P:
                        if p in usedP: continue
                        t=s+p
                        if t in Vs and t not in tg:
                            f[s]=t;usedP.add(p);tg.add(t);rec(i+1,usedP,usedN,tg);usedP.discard(p);tg.discard(t)
                else:
                    for n in N:
                        if n in usedN: continue
                        t=s-n
                        if t in Vs and t not in tg:
                            f[s]=t;usedN.add(n);tg.add(t);rec(i+1,usedP,usedN,tg);usedN.discard(n);tg.discard(t)
            rec(0,set(),set(),set())
    return out,cyc1
M=int(sys.argv[1]);a=int(sys.argv[2])
out,c1=covers(M,a)
holes=sorted(set((u,v) for u,v,_ in out))
for h in holes:
    e=out.get((h[0],h[1],0),0);o=out.get((h[0],h[1],1),0)
    print("holes",h,"covers even-count",e,"odd-count",o,"hamiltonian",c1.get(h,0))
