import itertools, random, math
from fractions import Fraction
from math import comb
def sgn(p):
    s=1
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: s=-s
    return s
def vand(pts):
    d=Fraction(1)
    for a in range(len(pts)):
        for b in range(a+1,len(pts)): d*=pts[b]-pts[a]
    return d
def Phi(t,x):
    k=len(x); tot=Fraction(0)
    for p in itertools.permutations(range(k)):
        s=0; pts=[Fraction(0)]
        for i in p: s+=x[i]; pts.append(s)
        pts.append(Fraction(t)); tot+=sgn(p)*vand(pts)
    return tot
random.seed(3)
def L(t,x):
    k=len(x); S=sum(x); den=vand([Fraction(v) for v in x])
    for v in x: den*=v
    den*=S*t*(t-S)
    return Phi(t,x)/den
for k in (3,4,5):
    ok_int=True; ok_hom=True; ok_sym=True; ok_ref=True
    for _ in range(4):
        x=[Fraction(v) for v in random.sample(range(1,13),k)]; t=Fraction(random.randint(13,30))
        if sum(x)==t or sum(x)==0: continue
        l1=L(t,x)
        if l1.denominator!=1: ok_int=False
        for lam in (2,3):
            if L(lam*t,[lam*v for v in x])!=lam**(k-2)*l1: ok_hom=False
        xs=x[:]; random.shuffle(xs)
        if L(t,xs)!=l1: ok_sym=False
        S=sum(x)
        sign=(-1)**(comb(k+1,2)+1)
        if Phi(S-t,x)!=sign*Phi(t,x): ok_ref=False
    print(f"k={k} (m=k+1={k+1}): L_k integer-valued: {ok_int}; homogeneous of degree k-2: {ok_hom}; symmetric in edges: {ok_sym}; Phi_k(S-t)=(-1)^(C(m,2)+1) Phi_k(t): {ok_ref}")
# collision recurrence: d/dh Phi_k(t;h,x)|_{h=0} = (-1)^{k-1} Alt_x [ Delta(y_0..y_{k-1},t) sum_i (t-y_i) f'(y_i) ]
def lagrange_deriv_at0(vals):                      # vals[j] = P(j), j=0..n ; derivative at 0
    n=len(vals)-1; tot=Fraction(0)
    for j in range(n+1):
        # derivative of Lagrange basis l_j at 0
        denom=Fraction(1)
        for m_ in range(n+1):
            if m_!=j: denom*=(j-m_)
        if j==0:
            dl=sum(Fraction(1,0-m_) for m_ in range(1,n+1))
        else:
            num=Fraction(1)
            for m_ in range(n+1):
                if m_!=j and m_!=0: num*=(0-m_)
            dl=num/denom
        tot+=vals[j]*dl
    return tot
for k in (3,4):
    x=[Fraction(v) for v in random.sample(range(1,10),k-1)]; t=Fraction(random.randint(11,20))
    deg=comb(k+2,2)+1
    vals=[Phi(t,[Fraction(h)]+x) for h in range(deg+1)]
    lhs=lagrange_deriv_at0(vals)
    # check exactness of the interpolation degree
    chk=Phi(t,[Fraction(deg+1)]+x)
    # RHS
    rhs=Fraction(0)
    for p in itertools.permutations(range(k-1)):
        y=[Fraction(0)]
        for i in p: y.append(y[-1]+x[i])
        f=lambda z:math.prod([z-yy for yy in y])
        def fp(yi): 
            r=Fraction(1)
            for yy in y:
                if yy!=yi: r*=(yi-yy)
            return r
        w=sum((t-yi)*fp(yi) for yi in y)
        rhs+=sgn(p)*vand(y+[t])*w
    rhs*=(-1)**(k-1)
    print(f"k={k}: d/dh Phi_k|_(h=0) = {lhs};  RHS formula = {rhs};  equal: {lhs==rhs}   (negated: {lhs==-rhs})")
