def zigzag(n,skip):
    # inward zigzag on [0,n] starting at 0: lows ascending (skipping 'skip'), highs descending; alternate low,high
    lows=[x for x in range(0,n+1) if x not in skip]; highs=list(range(n,-1,-1))
    path=[];used=set();li=hi=0
    turn=0
    while True:
        if turn==0:
            while li<len(lows) and lows[li] in used: li+=1
            if li==len(lows): break
            v=lows[li]
        else:
            while hi<len(highs) and (highs[hi] in used or highs[hi] in skip): hi+=1
            if hi==len(highs): break
            v=highs[hi]
        if v in used: break
        path.append(v);used.add(v);turn^=1
    return path
def try_h(M,a):
    n=M-1;b=M+1-a;sols=[]
    for h in range(1,n+1):
        if h==a: continue
        z=zigzag(n,{a,h})
        P=[a]+z
        if len(set(P))!=len(P) or set(P)!=set(range(n+1))-{h}: continue
        L=[abs(P[i+1]-P[i]) for i in range(len(P)-1)]
        if sorted(L)==sorted(set(range(1,n+1))-{b}): sols.append(h)
    return sols
bad=[]
for M in range(5,41):
    for a in range(2,(M+1)//2+(0 if (M+1)%2 else 0)):
        if 2*a>=M+1: continue
        s=try_h(M,a)
        if not s: bad.append((M,a))
        elif M<=16: print(M,a,s)
print("no h found for:",bad[:40],len(bad))
