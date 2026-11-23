# Does deleting the new labels from a zigzag at M+d leave a zigzag at M?  (a=1 tight family)
from audit_skew import allzig
def isz(st):
    v=0;seen=set()
    for d in st:
        if (v<=0)!=(d>0) or v in seen: return False
        seen.add(v);v+=d
    return v==0
def fam(M): return list(range(1,M+1)), list(range(2,M))+[M+1]
for M,d in ((5,1),(6,1),(7,1),(8,1),(5,2),(6,2),(7,2)):
    P,N=fam(M);P2,N2=fam(M+d)
    newp=set(P2)-set(P);newn=set(N2)-set(N);gonen=set(N)-set(N2)
    if gonen: 
        # label M+1 in N is replaced; treat by also deleting it and requiring merge? skip
        pass
    Z2=allzig(P2,N2);ok=0
    small=set(tuple(s) for s,_ in allzig(P,N))
    for st,_ in Z2:
        r=[x for x in st if not ((x>0 and x in newp) or (x<0 and -x in newn))]
        # if N lost a label (M+1 -> not in N2), cannot restrict directly
        if tuple(r) in small: ok+=1
    print(f"M={M}->{M+d}: zigzags at M+d {len(Z2)}, restricting to a zigzag at M: {ok}; new+ {sorted(newp)} new- {sorted(newn)} lost- {sorted(gonen)}",flush=True)
