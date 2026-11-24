"""Self-contained constructions and checks for quotient-block lifting, Erdős #475.
The checks are examples, not an exhaustive verification of Graham's conjecture.
"""
from itertools import accumulate

def vertices(word):
    return [0, *accumulate(word)][:-1]

def check(word, original):
    assert sorted(word)==sorted(original) and sum(word)==0
    v=vertices(word)
    assert len(set(v))==len(v)
    span=max(v)-min(v)
    assert span<=max(original)-min(original)
    return span

def symmetric_core(k,g):
    x=[(-1)**j*(j+1)*g for j in range(k)]
    return x+[-a for a in reversed(x[:-1])]+[-x[-1]]

def bounded_walk(block,start,L,U,P,Q):
    pos=sorted(a for a in block if a>0)
    neg=sorted(a for a in block if a<0)
    z=start; word=[]
    assert L<=start<=U and L<=start+sum(block)<=U
    while pos or neg:
        if pos and neg: a=pos.pop() if z<=L+Q else neg.pop()
        elif pos: a=pos.pop()
        else: a=neg.pop()
        z+=a; word.append(a)
        assert L<=z<=U
    return word

def triples(k):
    N=2*k; g=12*N+1; C=k+1
    blocks={}
    for i in range(1,N+1):
        r=2*i-1; s=2*N+2*i; t=r+s
        d=g*(i if i<=k else -(i-k))
        blocks[d]=[C*g+r,C*g+s,-(2*C*g+t-d)]
    # Check quotient minimality and disjoint residue supports explicitly.
    used=set()
    for d,block in blocks.items():
        assert sum(block)==d and d%g==0
        R={sum(block[j] for j in range(3) if mask>>j&1)%g for mask in range(1,7)}
        assert 0 not in R and not (used&R)
        used|=R
    A=[a for block in blocks.values() for a in block]
    assert len(set(A))==len(A) and sum(A)==0
    P=max(A); Q=-min(A); D=P+Q
    core=symmetric_core(k,g); check(core,list(blocks))
    L=min(vertices(core)); U=L+D
    assert max(vertices(core))<=U
    out=[]; z=0
    for d in core:
        out.extend(bounded_walk(blocks[d],z,L,U,P,Q)); z+=d
    span=check(out,A)
    return len(A),D,span,sum(a for a in A if a>0),g*k*(k+1)//2

def old_obstruction(s):
    P=[a for j in range(2*s) for a in (4*j+1,-(4*j+3))]
    Q=[a for j in range(2*s) for a in (4*j+2,-(4*j+4))]
    rotated=Q[-1:]+Q[:-1]
    A=P+[-a for a in Q]
    word=P+[-a for a in reversed(rotated)]
    return check(word,A),word

if __name__=='__main__':
    for k in range(1,101): triples(k)
    for s in range(1,101): old_obstruction(s)
    print('100 unequal-sign triple-block family instances passed.')
    print('100 interleaved-band obstruction family instances passed.')
    for k in (1,5,10,25,100):
        n,D,W,T,t=triples(k)
        print(f'k={k}: n={n}, D={D}, W={W}, T/D={T/D:.3f}, core mass/D={t/D:.3f}')
    print('16-element obstruction:',old_obstruction(2))
