from itertools import combinations, permutations
def ps(o):
    s=0;out=[]
    for x in o: s+=x; out.append(s)
    return out
# Thm 1: X,Y distinct positive sets, sum X != sum Y  =>  orderings with disjoint nonempty partial sums
bad=0;tot=0
for nx in range(1,5):
  for X in combinations(range(1,10),nx):
    for ny in range(1,5):
      for Y in combinations(range(1,10),ny):
        if sum(X)==sum(Y): continue
        tot+=1
        PX=[set(ps(o)) for o in permutations(X)]; PY=[set(ps(o)) for o in permutations(Y)]
        if not any(not(a&b) for a in PX for b in PY):
            bad+=1
            if bad<=5: print("THM1 FAIL",X,Y)
print("Thm1 tested",tot,"failures",bad)
def valid(w,D):
    assert sum(w)==0; v=[0]
    for x in w[:-1]: v.append(v[-1]+x)
    return len(set(v))==len(v) and max(v)-min(v)<=D, max(v)-min(v)
print(valid((2,3,4,5,-13,29,-9,-8,-7,-6),42))
print(valid((8,-6,1,-4,7,-2,-3,-1),14))
# family k: check construction claim for k=4..20 using peak removal with a=P,b=Q
for k in (4,5,10,20):
    X0=list(range(2,k+2)); Y0=list(range(k+2,2*k+2)); a=sum(Y0)-1; b=sum(X0)-1
    X=X0+[a]; Y=Y0+[b]; T=sum(X); assert T==sum(Y)
    P,Q=max(X),max(Y); h=T-P-Q
    # Thm1 orderings for X\{P}, Y\{Q}: increasing orders, check disjointness directly
    Xp=sorted(set(X)-{P}); Yp=sorted(set(Y)-{Q})
    sx=set(ps(Xp)); sy=set(ps(Yp))
    w=Xp+[-Q,P]+[-y for y in reversed(Yp)]
    print(k,len(X)+len(Y),P+Q,h,valid(tuple(w),P+Q))
