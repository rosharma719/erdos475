import sys; sys.path.insert(0,"experiments/irc")
from zigzag_sat import decide, check_steps
out=open("research/data/zasym_witnesses.md","w")
out.write("# SAT witnesses: tight family P=[1,M], N=[1,M+1]\\{a,M+1-a}; steps listed (one valid zigzag each)\n")
for M in range(3,15):
    for a in range(1,(M+1)//2+1):
        b=M+1-a
        if a>=b: continue
        P=list(range(1,M+1));N=sorted(set(range(1,M+2))-{a,b})
        r,st,_=decide(P,N); assert r=="FOUND" and check_steps(st,P,N)
        v=0;V=[0]
        for d in st[:-1]: v+=d;V.append(v)
        hn=-next(iter(set(range(-M,1))-set(V)));hp=next(iter(set(range(1,M+1))-set(V)))
        out.write(f"M={M} a={a} b={b} holes(u,v)=({hn},{hp}) steps={st}\n");out.flush()
