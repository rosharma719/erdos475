#!/usr/bin/env python3
"""Exact finite audit of compatible extreme contraction and maximum-pair insertion.
Run: python erdos475_extreme_compatibility_audit.py --max-magnitude 11
The search is finite evidence, not a proof of either universal conjecture.
"""
import argparse
from itertools import combinations


def vertices(word):
    s = 0
    out = [0]
    for a in word[:-1]:
        s += a
        out.append(s)
    return out


def span(word):
    v = vertices(word)
    return max(v) - min(v)


def valid(word, D):
    if not word:
        return True
    v = vertices(word)
    return sum(word) == 0 and len(v) == len(set(v)) and max(v)-min(v) <= D


def compatible(A):
    P, Q = max(A), -min(A)
    D, N, S = P+Q, len(A), set(A)
    equal = P == Q
    candidates = {}
    if equal:
        B = S-{P,-P}
        if not B:
            return True
        d = max(B)-min(B)
    else:
        for a in A:
            for b in A:
                if a*b < 0 and (a in (P,-Q) or b in (P,-Q)) and a+b not in S|{0}:
                    B = (S-{a,b})|{a+b}
                    candidates[a,b] = max(B)-min(B)
        if not candidates:
            return False
    # Every cycle can be rotated so that P is its first step.
    w, v = [P], {0,P}
    def dfs(s, rem, lo, hi):
        if not rem:
            if equal:
                return valid([a for a in w if abs(a)!=P],d)
            for i in range(N):
                a,b = w[i],w[(i+1)%N]
                if (a,b) in candidates:
                    z = w[i:]+w[:i]
                    if valid([a+b]+z[2:],candidates[a,b]):
                        return True
            return False
        for a in rem:
            t = s+a
            if (len(rem)>1 and t in v) or max(hi,t)-min(lo,t)>D:
                continue
            w.append(a)
            v.add(t)
            if dfs(t,rem-{a},min(lo,t),max(hi,t)):
                return True
            w.pop()
            if t!=0:
                v.remove(t)
        return False
    return dfs(P,S-{P},0,P)


def check_certificates():
    core = (1,-3,-2,-1,2,3)
    assert valid(core,6)
    tail = core[1:]
    print('Fixed-core nonadjacent splitting obstruction:')
    for a,b in [(5,-4),(-4,5)]:
        for j in range(len(tail)+1):
            w = (a,)+tail[:j]+(b,)+tail[j:]
            assert not valid(w,9)
            print('  first=',a,'gap=',j,'simple=',valid(w,100),'span=',span(w))
    w = (1,-3,-1,2,3,-2)
    assert valid(w,6) and valid((5,-4)+w[1:],9)
    A = {-5,-4,-3,1,5,6}
    cores = set()
    for a in A:
        for b in A:
            if a*b<0 and (a in (6,-5) or b in (6,-5)) and a+b not in A|{0}:
                cores.add(tuple(sorted((A-{a,b})|{a+b})))
    assert cores == {(-5,-4,1,3,5),(-5,-3,1,2,5)}
    assert all(max(B)==-min(B) and set(B)!={-a for a in B} for B in cores)
    print('Unequal-extreme induction escape obstruction:',sorted(cores))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--max-magnitude',type=int,default=11)
    args=ap.parse_args()
    check_certificates()
    totals=[0,0]
    for M in range(2,args.max_magnitude+1):
        V=list(range(-M,0))+list(range(1,M+1))
        counts=[0,0]
        for n in range(3,len(V)+1):
            for A in combinations(V,n):
                # Normalize the larger absolute extremum to be positive.
                # Equal-extreme sets are not identified with their negations.
                if sum(A) or max(A)!=M or A==tuple(-x for x in A[::-1]):
                    continue
                eq=int(max(A)==-min(A))
                if not compatible(A):
                    raise AssertionError(('counterexample to reduction',A,eq))
                counts[eq]+=1
        totals=[a+b for a,b in zip(totals,counts)]
        print(M,counts,flush=True)
    print('Totals:',totals,'total',sum(totals))

if __name__=='__main__':
    main()
