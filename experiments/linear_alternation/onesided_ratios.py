import itertools
from fractions import Fraction
from onesided import X, Y, L, prop
for m in (4,5):
    top=tuple(range(1,m+1))
    for k in range(1,m+1):
        r3=set(); r3b=set(); r4=set()
        for A in itertools.combinations(top,k):
            for B in itertools.combinations(top,k):
                if sum(A)!=sum(B): continue
                f={(A,B):Fraction(1)}
                r3.add(prop(L(L(f)),X(Y(f,m),m))); r3b.add(prop(Y(X(f,m),m),X(Y(f,m),m))); r4.add(prop(L(X(f,m)),Y(L(f),m)))
        print(f"m={m} k={k}: L^2/(XY) {r3}  YX/XY {r3b}  LX/(YL) {r4}")
