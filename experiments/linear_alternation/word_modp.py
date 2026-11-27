import sympy
from word_patterns import patterns, interp, H
for m in range(2,6):
    for d in range(1,m+1):
        hs=list(range(0,m*(m+1)//2+3))
        SAB,SBA=patterns(m,d,hs); pa=interp(SAB); pb=interp(SBA)
        refl=[s for s in (1,-1) if sympy.expand(pb - s*pa.subs(H,-1-H))==0]
        eps=(-1)**(m-1); G=sympy.expand(pa+eps*pb)
        out=[]
        for p in sympy.primerange(m+2,40):
            def ok(poly,x):
                num,den=sympy.fraction(sympy.together(poly)); return sympy.Poly(num,H).eval(x)%p==0
            top=sum(1 for j in range(1,m+1) if ok(pa,p-j)); bot=sum(1 for j in range(0,m) if ok(pb,j))
            out.append(f"p{p}:{top}/{bot}")
        print(f"m={m} d={d}: S_BA(h) = s*S_AB(-1-h) with s={refl};  roots mod p in top/bottom m heights: "+" ".join(out))
