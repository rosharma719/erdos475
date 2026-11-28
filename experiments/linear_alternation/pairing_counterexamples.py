import itertools, sys
from math import gcd
from functools import reduce
from sat_lib import group, orbit_sum, chiQ
from pairing_matrix_checks import lam_generic, esym
def Prow(m,q,d_list):
    out={}
    for d in d_list:
        row=[]
        for j in range(m):
            def f(w,j=j,d=d):
                y=[]; acc=0
                for k in range(m-1): acc+=w[k]; y.append(acc)
                e=esym(y,m-1)
                return q(w)*w[j]**d*e[m-d]
            row.append(lam_generic(m,f))
        out[d]=row
    return out
# ---- rank 5 degree-5 counterexample
def q5(w):
    return sum(w[i]*(w[(i+1)%5]**2*w[(i+2)%5]**2+w[(i-1)%5]**2*w[(i-2)%5]**2) for i in range(5))
P5=Prow(5,q5,[1,2,3,4,5])
print("rank-5 q: matrix rows d=1..5, columns j=1..5:")
for d in range(1,6): print("  d=%d"%d,P5[d])
print("  report: rows [0,0,0,0,0],[0,-7,0,7,0],[0,-2,4,-2,0],[0,5,0,-5,0],[0,0,0,0,0]")
# ---- rank 6: q = f * prod (w_i + w_{i+1}),  f from signed dihedral orbit sums (rotation, reversal act by -1)
m=6; els=group(m,lambda k,c:chiQ(m,k,c))
terms=[((3,0,0,0,0,0),5),((1,1,1,0,0,0),-26),((1,1,0,1,0,0),35)]
orb=[]
for a,c in terms:
    o=orbit_sum(a,els,m); orb.append((c,o))
def f6(w):
    t=0
    for c,o in orb:
        for b,s in o.items():
            v=s*c
            for e,x in zip(b,w): v*=x**e
            t+=v
    return t
def q6(w):
    v=f6(w)
    for i in range(6): v*=(w[i]+w[(i+1)%6])
    return v
P6=Prow(6,q6,[1,5])
print("rank-6 q: first row P_{6,1,.} =",P6[1],"  penultimate row P_{6,5,.} =",P6[5],"  (report: zeros and (0,-144,216,-216,144,0))")
