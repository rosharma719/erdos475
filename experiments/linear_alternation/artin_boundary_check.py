"""Reduce B_m = Q_m * prod_{j=1}^{m-1} y_j in the integral coinvariant ring (Artin normal form) and compare its coefficients on
M_i = (staircase monomial)/w_i with b_{m,i} = -sum_{j<i} c_{m,j}."""
import re, sys
from artin import *
C={}
for line in open('results_reported.txt'):
    m=int(re.match(r'm=(\d+)',line).group(1)); C[m]=[int(v) for v in re.search(r'\[(.*)\]',line).group(1).split(',') if v.strip()]
def interval_poly(n,m):                 # F over first m-1 variables: all intervals length>=2 except the full one among w_0..w_{m-2}
    P=const(n,1); mm=m-1
    for i in range(mm):
        for j in range(i+1,mm):
            if i==0 and j==mm-1: continue
            P=pmul(P,lin(n,range(i,j+1)))
    return P
for m in range(4,int(sys.argv[1])+1):
    R=Ring(m)
    B=interval_poly(m,m)
    for j in range(1,m): B=pmul(B,lin(m,range(0,j)))          # y_1..y_{m-1}
    nf=R.nf(B)
    stair=[k for k in range(m)]
    got={}
    for i in range(2,m+1):                                   # M_i: staircase exponent of variable i (1-indexed) reduced by 1
        e=stair[:]; e[i-1]-=1; got[i]=nf.get(tuple(e),0)
    extra=[k for k in nf if k not in {tuple(stair[:i-1]+[stair[i-1]-1]+stair[i:]) for i in range(2,m+1)}]
    c=C[m]; b={i:-sum(c[:i-1]) for i in range(2,m+1)}
    same=[got[i]==b[i] for i in range(2,m+1)]; neg=[got[i]==-b[i] for i in range(2,m+1)]
    print(f"m={m}: nf(B_m) has {len(nf)} terms (all Artin M_i: {not extra}); coefficients {[got[i] for i in range(2,m+1)]}; equal to b: {all(same)}, equal to -b: {all(neg)}",flush=True)
