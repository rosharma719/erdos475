"""Exact audit of singular projection and one-defect repair certificates.
Python 3, standard library only. No external data or claimed open-problem proof.
Run: python erdos475_singular_projection_audit.py
"""
from itertools import combinations
from random import Random


def kernel(A,p):
    """Kernel of the span of ALL binary zero-sum incidence rows, over F_p."""
    n=len(A); rows={}; sums=[0]*(1<<n)
    for mask in range(1,1<<n):
        j=(mask&-mask).bit_length()-1
        sums[mask]=(sums[mask^(1<<j)]+A[j])%p
        if sums[mask]: continue
        v=[(mask>>i)&1 for i in range(n)]
        for i,r in sorted(rows.items()):
            if v[i]:
                c=v[i]; v=[(x-c*y)%p for x,y in zip(v,r)]
        j=next((j for j,x in enumerate(v) if x),None)
        if j is not None:
            c=pow(v[j],-1,p); rows[j]=[x*c%p for x in v]
            if len(rows)==n-1: break # actual A is a nonzero kernel vector
    out=[]
    for i in range(n):
        if i in rows: continue
        x=[0]*n; x[i]=1
        for j,r in sorted(rows.items(),reverse=True):
            x[j]=-sum(a*b for a,b in zip(x,r))%p
        out.append(x)
    return out


def singular_lines(B,p):
    assert len(B)==2
    # In a two-dimensional space, each zero-coordinate hyperplane is a line.
    # Enumerate all projective lines once, and keep the singular ones.
    for x in [B[1]]+[[(a+t*b)%p for a,b in zip(*B)] for t in range(p)]:
        if 0 in x: yield x


def certificate(x,p,allow_defect=False):
    """Exact multiset DFS. A returned one-defect word has a common step
    value on both sides of its unique collision interval."""
    a=tuple(sorted(i for i in x if i))
    if len(a)<2:return None
    assert sum(a)%p==0
    def dfs(rem,s,vs,w,defect):
        if not rem:
            if s:return None
            if defect is None:return w,None
            i,j=defect
            if set(w[i:j]) & set(w[:i]+w[j:]):return w,defect
            return None
        for i,t in enumerate(rem):
            if i and t==rem[i-1]:continue
            u=(s+t)%p; nd=defect
            if len(rem)>1 and u in vs:
                if not allow_defect or defect is not None:continue
                nd=(vs.index(u),len(vs))
            z=dfs(rem[:i]+rem[i+1:],u,vs+(u,),w+(t,),nd)
            if z:return z
        return None
    return dfs(a,0,(0,),(),None)


def check_kernel(A,B,p):
    for mask in range(1,1<<len(A)):
        idx=[i for i in range(len(A)) if mask>>i&1]
        if sum(A[i] for i in idx)%p==0:
            assert all(sum(b[i] for i in idx)%p==0 for b in B)


def simple(word,p):
    s=0; seen=set()
    for a in word:
        s=(s+a)%p
        if s in seen:return False
        seen.add(s)
    return s==0


def main():
    p=13; A=[1,2,3,4,8,9,12]; B=kernel(A,p); check_kernel(A,B,p)
    assert len(B)==2
    xs=list(singular_lines(B,p))
    assert len(xs)==4
    assert all(certificate(x,p) is None for x in xs)
    assert all(certificate(x,p,True) is not None for x in xs)
    x=[0,0,12,12,1,1,0]; assert x in B
    # Order of the projected nonzero multiset: 1,1,-1,-1.
    # Insert zero-projection pieces [1] and [2,12] at distinct unique heights.
    bad=[1,8,9,2,12,3,4]; good=[1,9,8,2,12,3,4]
    assert sorted(bad)==sorted(good)==A
    assert not simple(bad,p) and simple(good,p)
    print('p=13 simple-projection obstruction and repair:',B,good)
    p=17; A=[2,3,4,5,6,7,11,13]; B=kernel(A,p);check_kernel(A,B,p)
    assert len(B)==2
    xs=list(singular_lines(B,p))
    assert all(len([a for a in x if a])!=len(set(a for a in x if a)) for x in xs)
    assert any(certificate(x,p) is not None for x in xs)
    print('p=17 distinct-projection obstruction, repaired by multiset projection')
    p=13;A=[1,2,3,4,5,6,7,11];B=kernel(A,p);check_kernel(A,B,p)
    assert len(B)==1 and all(B[0]); print('rank-one obstruction:',B)
    rng=Random(477);cnt=0;no_simple=0;fail=0;seen=set();unique_no_simple=0
    for _ in range(20000):
        p=rng.choice([11,13,17,19,23,29,31,37,43,53,61,79,101,127,211])
        n=rng.randrange(4,min(11,p-1)+1)
        A=rng.sample(range(1,p),n-1);b=-sum(A)%p
        if b==0 or b in A:continue
        A.append(b);A.sort();B=kernel(A,p)
        if len(B)!=2 or set(A)=={(-a)%p for a in A}:continue
        cnt+=1; key=(p,tuple(A)); first=key not in seen; seen.add(key)
        xs=list(singular_lines(B,p))
        if any(certificate(x,p) is not None for x in xs):continue
        no_simple+=1; unique_no_simple+=first
        if not any(certificate(x,p,True) is not None for x in xs):
            fail+=1; print('FAIL',p,A,B)
    print('rank-two nonsymmetric sample draws:',cnt,'distinct sets:',len(seen),
          'without simple projection:',no_simple,'distinct such sets:',unique_no_simple,
          'without one-defect certificate:',fail)

if __name__=='__main__':main()
