"""(1) v*g = u^{m+1} - H_{m+1} (polynomial identity), g = sum_j H_j u^{m-1-j};  (2) rank 7: g, matrix of multiplication by g
A_7^3 -> A_7^9 in bases (u^3,uv)->(u^3v^3,uv^4): determinant and Smith form."""
from fractions import Fraction
from split_edge_checks_lib import Hpoly
def mulp(p,q):
    o={}
    for (a,b),c in p.items():
        for (a2,b2),c2 in q.items(): o[(a+a2,b+b2)]=o.get((a+a2,b+b2),0)+c*c2
    return {k:v for k,v in o.items() if v}
def addp(p,q,s=1):
    o=dict(p)
    for k,v in q.items(): o[k]=o.get(k,0)+s*v
    return {k:v for k,v in o.items() if v}
def gpoly(m):
    g={}
    for j in range(m): g=addp(g,mulp(Hpoly(j),{(m-1-j,0):1}))
    return g
for m in range(2,13):
    lhs=mulp({(0,1):1},gpoly(m)); rhs=addp({(m+1,0):1},Hpoly(m+1),-1)
    assert lhs==rhs, m
print("v*g = u^(m+1) - H_(m+1) verified symbolically for m = 2..12")
g7=gpoly(7); print("g_7 =",sorted(g7.items(),reverse=True))
# multiplication by g_7 : degree-3 part of A_7 -> degree-9 part
m=7; Hm,Hm1=Hpoly(7),Hpoly(8)
mon9=[(9-2*b,b) for b in range(5)]                      # u^9, u^7v, u^5v^2, u^3v^3, uv^4
rel=[]                                                   # relations in degree 9: mono*H_7 (deg 2: u^2, v), mono*H_8 (deg 1: u)
for (a,b) in [(2,0),(0,1)]: rel.append(mulp({(a,b):1},Hm))
rel.append(mulp({(1,0):1},Hm1))
idx={mm:i for i,mm in enumerate(mon9)}
rows=[[Fraction(r.get(mm,0)) for mm in mon9] for r in rel]
# eliminate columns 0,1,2 (u^9,u^7v,u^5v^2) to express them in terms of columns 3,4
for col in range(3):
    piv=next(i for i in range(col,3) if rows[i][col]!=0)
    rows[col],rows[piv]=rows[piv],rows[col]
    rows[col]=[x/rows[col][col] for x in rows[col]]
    for i in range(3):
        if i!=col and rows[i][col]!=0:
            f=rows[i][col]; rows[i]=[x-f*y for x,y in zip(rows[i],rows[col])]
def reduce9(p):
    vec=[Fraction(p.get(mm,0)) for mm in mon9]
    for col in range(3):
        f=vec[col]
        if f: vec=[x-f*y for x,y in zip(vec,rows[col])]
    return vec[3:]
G=[reduce9(mulp(g7,{(3,0):1})),reduce9(mulp(g7,{(1,1):1}))]
print("matrix of multiplication by g_7 (rows: images of u^3, uv; columns: u^3v^3, uv^4):",[[str(x) for x in r] for r in G])
det=G[0][0]*G[1][1]-G[0][1]*G[1][0]
print("det =",det)
from math import gcd
ents=[int(x) for r in G for x in r]
d1=0
for x in ents: d1=gcd(d1,abs(x))
print("Smith normal form diag(",d1,",",abs(int(det))//d1,")")
