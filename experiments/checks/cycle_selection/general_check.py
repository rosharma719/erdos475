"""Check interval endpoints and the boundary contraction on varying radii."""
from offset_verify import build,check
from itertools import pairwise

def test():
    count=0
    for n in range(7,102,2):
        x,y=(3*n+1)//2,(3*n+5)//2
        U={x,y,-n,-n-1,-n-2}
        L=y
        for groups in ([[x,-n],[y,-n-1],[-n-2]],
                       [[x,-n],[y],[-n-1,-n-2]]):
            S=[];E=L
            for g in groups:
                E+=1+max(sum(t for t in g if t>0),-sum(t for t in g if t<0))
                S.append(E)
            for low in ([],[1],list(range(1,n))):
                P=[m if (len(low)-i)%2 else -m for i,m in enumerate(low)]
                A=U|set(low)|{-a for a in low}
                for after in ([],[S[-1]+1]):
                    outer=S+after
                    w=build(L,A,P,P,list(U),outer,groups+[[] for _ in after])
                    N=2*outer[-1]+1
                    labels=A|set(outer)|{-a for a in outer}
                    check(w,N,labels)
                    # Any first-bin boundary pair with sum strictly in its gap.
                    j=next(i for i,(a,b) in enumerate(pairwise(w+w[:1]))
                           if S[0] in (abs(a),abs(b)) and L<abs(a+b)<S[0])
                    w=w[j:]+w[:j];a,b=w[:2]
                    assert a%N not in check([a+b]+w[2:],N,(labels-{a,b})|{a+b})
                    count+=1
    print(count,'variable-radius checks passed.')

if __name__=='__main__':test()
