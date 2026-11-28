import itertools
from modrank import rank_mod
P=1000003
def Hpoly(j):                       # H_j(u,v) as dict {(a,b):c} meaning u^a v^b
    h=[{(0,0):1},{(1,0):1}]
    for k in range(2,j+1):
        t={}
        for (a,b),c in h[k-1].items(): t[(a+1,b)]=t.get((a+1,b),0)+c
        for (a,b),c in h[k-2].items(): t[(a,b+1)]=t.get((a,b+1),0)-c
        h.append({k_:v for k_,v in t.items() if v})
    return h[j]
def wdeg(a,b): return a+2*b
def mono_basis(d): return [(d-2*b,b) for b in range(d//2+1)]
def shift(poly,a0,b0): return {(a+a0,b+b0):c for (a,b),c in poly.items()}
def span_rows(gens,d):              # all mono*gen in degree d
    rows=[]
    for g in gens:
        gd=wdeg(*next(iter(g)))
        if gd>d: continue
        for (a,b) in mono_basis(d-gd): rows.append(shift(g,a,b))
    return rows
