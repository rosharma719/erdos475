"""Independent audit of GPT's reflected-core + four-step bridge constructions (a=2..5). Own implementation from the
stated formulas; seeds copied from the note."""
def incr(p): return [y-x for x,y in zip(p,p[1:])]
G4={7:[6,1,7,4,2,3],8:[7,1,8,3,6,4,5],9:[8,1,9,3,6,7,2,4]}
G5={6:[5,1,4,2,3],7:[6,2,3,1,7,4],8:[7,1,8,4,2,5,6],9:[8,1,9,3,7,4,6,5],10:[9,1,10,3,7,6,8,2,5]}
def G(n,d):
    seeds=G4 if d==4 else G5; cut=10 if d==4 else 11
    if n<cut: return list(seeds[n])
    return [n-1,1,n]+[n-1-x for x in G(n-3,d)]
D3={6:[5,-2,-1],7:[6,-4,2,-1],8:[7,-5,2,1,-4]}
D4={8:[6,-7,3,2,-1],9:[7,-8,5,-3,2,-1],10:[8,-9,6,-3,1,-2,5]}
D5={10:[4,-1,2,-7,9,-8,3],11:[6,-8,10,-9,4,2,-3,-1]}
def delta(M,a):
    if a==2:
        q=sorted(set(range(1,M-1))-{2},reverse=True); return [x if i%2==0 else -x for i,x in enumerate(q)]
    if a==3:
        if M<9: return list(D3[M])
        return [M-1,-(M-3),M-5]+[-x for x in delta(M-3,3)]
    if a==4:
        if M<=10: return list(D4[M])
        return [M-2,-(M-1),M-4]+incr(G(M-4,4))
    if a==5:
        if M<=11: return list(D5[M])
        return [M-5,-(M-3),M-1,-(M-2),M-6]+incr(G(M-6,5))
def W(M,a):
    b=M+1-a; d=delta(M,a)
    return d+[M]+[-x for x in d[::-1]]+[b,-M,-(M+1),a]
def ok(M,a):
    b=M+1-a; w=W(M,a)
    if sorted(x for x in w if x>0)!=list(range(1,M+1)): return False
    if sorted(-x for x in w if x<0)!=sorted(set(range(1,M+2))-{a,b}): return False
    v=0;S=[0]
    for x in w[:-1]: v+=x;S.append(v)
    if len(set(S))!=len(S) or v+w[-1]!=0 or max(S)-min(S)>2*M+2: return False
    p=2*M+3
    return len({s%p for s in S})==len(S)
bad={}
for a,lo in ((2,4),(3,6),(4,8),(5,10)):
    bad[a]=[M for M in range(lo,1201) if 2*a<M+1 and not ok(M,a)]
print("failures by a (M up to 1200):",{a:v[:5] for a,v in bad.items()}, "counts",{a:len(v) for a,v in bad.items()})
print("large M:",[(a,M,ok(M,a)) for a in (2,3,4,5) for M in (3001,5000)])
