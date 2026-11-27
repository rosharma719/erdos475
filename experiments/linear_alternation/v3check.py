import sympy, random
from fractions import Fraction
from seed_rigidity import F2_from_recurrence, V, f
random.seed(5)
for m in (4,5,6,7):
    seed=[Fraction(random.randint(-9,9)) for _ in range(m)]
    F2=F2_from_recurrence(m,seed); rat=set()
    for a in range(1,m+1):
        for b in range(a+1,m+1):
            h=tuple(x for x in range(1,m+1) if x not in (a,b))
            val=sympy.Rational(F2.get((h,h),0)); pred=V(a,b).subs({f[j]:sympy.Rational(seed[j]) for j in range(m)})
            rat.add(val/pred if pred else ('0' if val==0 else 'X'))
    print(m,rat)
