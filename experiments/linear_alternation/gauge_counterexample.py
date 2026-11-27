import itertools
from math import comb
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def pmul(P,Q):
    out={}
    for (x1,t1),c1 in P.items():
        pass
    return out
# F_A(t1,t2) for r=2:  [x^A] Alt_x det((x_i - t_i x_{i+1})^{a_j}), rows: (x1 - t1 x2), (x2 - t2 x1)
def FA2(A):
    a1,a2=A; poly={}
    for perm in itertools.permutations(range(2)):            # Alt over x-variables
        sx=sgn(perm)
        for tau in itertools.permutations(range(2)):
            st=sgn(tau); b=[A[tau[0]],A[tau[1]]]
            # row1: (x_{p0} - t1 x_{p1})^{b0}, row2: (x_{p1} - t2 x_{p0})^{b1}
            for k in range(b[0]+1):
                for l in range(b[1]+1):
                    ex=[0,0]
                    ex[perm[0]]+=b[0]-k; ex[perm[1]]+=k; ex[perm[1]]+=b[1]-l; ex[perm[0]]+=l
                    if tuple(ex)!=tuple(A): continue
                    co=comb(b[0],k)*(-1)**k*comb(b[1],l)*(-1)**l
                    key=(k,l); poly[key]=poly.get(key,0)+sx*st*co
    return {k:v for k,v in poly.items() if v}
A=(4,5); p=7
P=FA2(A)
f1={}
for (k,l),c in P.items():                    # t1=1, t2=t
    f1[l]=f1.get(l,0)+c
f1={k:v%p for k,v in f1.items() if v%p}
print("f_1(t)=F_A(1,t) mod 7:",sorted(f1.items()),"  report: t+3t^2+6t^3+3t^4+t^5")
rec={}
for k,c in f1.items():
    rec[k]=(rec.get(k,0)+c)%p
    rec[6-k]=(rec.get(6-k,0)-c)%p
print("f_1(t) - t^6 f_1(1/t) mod 7:",{k:v for k,v in rec.items() if v},"  (report: identically 0)")
found=[]
for z2 in range(1,p):
    # f_z(t) = F_A(z1/z2, t z2/z1) with z1=1: t1 = 1/z2, t2 = t*z2
    inv=pow(z2,-1,p); f={}
    for (k,l),c in P.items():
        f[l]=(f.get(l,0)+c*pow(inv,k,p)*pow(z2,l,p))%p
    g={}
    for k,c in f.items():
        g[k]=(g.get(k,0)+c)%p; g[6-k]=(g.get(6-k,0)-c)%p
    g={k:v for k,v in g.items() if v}
    found.append((z2,sorted(g.items())))
for z2,g in found: print(f"  gauge z=(1,{z2}): G_z(t) = f_z(t) - t^6 f_z(1/t) mod 7 = {g}")
print("report: G_z(t) = 5 + 3t + 4t^5 + 2t^6 (for its chosen gauge; sign convention of the projection may differ)")
