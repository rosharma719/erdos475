#!/usr/bin/env python3
"""Erdos #475: exact modular repair and rational-certificate audit.

This file verifies the explicit certificates in the accompanying chat and
implements a torsion-aware symbolic search for zero-sum sets of a FIXED size.
It does not prove the all-cardinalities conjecture. Python 3; SymPy required
for exact rational linear algebra. No floating-point rank tests.

Run: python erdos475_modular_repair_audit.py
Optional: --symbolic-size N (can grow exponentially).
"""
import argparse
from itertools import permutations, combinations
from math import lcm, gcd, factorial
from sympy import Matrix, factorint


def vertices(word, p):
    out = [0]
    for a in word[:-1]:
        out.append((out[-1] + a) % p)
    return out


def simple(word, p):
    return sum(word) % p == 0 and len(set(vertices(word, p))) == len(word)


def check_short_window_trap():
    p = 23
    w = [14,5,7,17,13,18,19,8,22,4,15,11,3,20,2,12,1,6,10]
    assert len(set(w)) == len(w) and sum(w) % p == 0
    assert set(w) != {(-a) % p for a in w}
    assert len(set(vertices(w,p))) == len(w)-1
    tested = 0
    for r in range(2,7):
        for i in range(len(w)):
            rot = w[i:]+w[:i]
            for block in permutations(rot[:r]):
                assert not simple(list(block)+rot[r:],p)
                tested += 1
    assert tested == len(w)*sum(factorial(r) for r in range(2,7))
    repaired = w[:6]+[22,8,4,15,3,11,19]+w[13:]
    assert sorted(repaired) == sorted(w) and simple(repaired,p)
    print('Short-window trap: p=23, n=19; permutations checked:',tested)
    print('Original vertices:', vertices(w,p))
    print('Repaired vertices:', vertices(repaired,p))


def check_rational_certificate():
    p=29
    mags=[1,2,3,4,5,8,13]
    labels=mags+[-x for x in mags]
    relations=[(x,-x) for x in mags]+[
        (1,2,-3),(1,3,-4),(1,4,-5),(2,3,-5),
        (3,5,-8),(5,8,-13),(13,8,5,3)]
    rows=Matrix([[int(a in S) for a in labels] for S in relations])
    assert len(set(x%p for x in labels))==len(labels)
    assert all(sum(S)%p==0 for S in relations)
    assert abs(rows.det())==p
    assert rows*Matrix(labels)==Matrix([sum(S) for S in relations])
    # Every coordinate is in the rational row span, but not zero mod p.
    e=Matrix([1]+[0]*(len(labels)-1))
    coeff=rows.T.inv()*e
    m=lcm(*(int(x.q) for x in coeff))
    assert m==p
    assert rows.T*(m*coeff)==m*e
    print('Rational-rank counterexample: p=29, n=14, det =',rows.det(), 'denominator =',m)


def integer_order(weights):
    """Simple cyclic order of distinct nonzero zero-sum integer weights.
    Two increasing paths, lexicographically minimize common interior sums.
    Returns indices of weights (the second path is traversed backwards).
    """
    n=len(weights)
    assert len(set(weights))==n and all(weights) and sum(weights)==0
    X=[i for i,x in enumerate(weights) if x>0]
    Y=[i for i,x in enumerate(weights) if x<0]
    def pref(path):
        s=0; out=[]
        for i in path:
            s+=abs(weights[i]);out.append(s)
        return out
    def cost():
        common=set(pref(X)[:-1])&set(pref(Y)[:-1])
        return len(common),sum(common),common
    while True:
        h,t,common=cost()
        if not h:return X+Y[::-1]
        improved=False
        for path in (X,Y):
            for j,v in enumerate(pref(path)[:-1]):
                if v not in common:continue
                path[j],path[j+1]=path[j+1],path[j]
                if cost()[:2]<(h,t):improved=True;break
                path[j],path[j+1]=path[j+1],path[j]
            if improved:break
        assert improved, 'Monotone separation proof would be contradicted'


def symbolic_prime_candidates(n):
    """Sound finite over-approximation to exceptional primes for this size.
    Branch over every proper cyclic interval of an integer witness ordering.
    Every branch increases rational rank; terminal denominators give primes.
    A returned prime is NOT a counterexample; it requires modular checking.
    """
    assert n>=2
    E=[tuple(int(i==j) for i in range(n)) for j in range(n)]
    forbidden=E+[tuple(a-b for a,b in zip(E[i],E[j])) for i,j in combinations(range(n),2)]
    visited=set(); candidates=set(); nodes=0
    def visit(rows):
        nonlocal nodes
        # Row order is irrelevant, but we keep the actual integer rows:
        # rational row-space equality alone would lose lattice denominators.
        key=tuple(sorted(rows))
        if key in visited:return
        visited.add(key);nodes+=1
        M=Matrix(rows)
        N=M.nullspace()
        terminal=[]
        for u in forbidden:
            if all(sum(a*b for a,b in zip(u,v))==0 for v in N):
                coeff=M.T.gauss_jordan_solve(Matrix(u))[0]
                terminal.append(lcm(*(int(x.q) for x in coeff)))
        if terminal:
            g=gcd(*terminal)
            candidates.update(int(p) for p in factorint(g) if p>n)
            return
        assert N
        t=0
        while True:
            v=sum((b*t**j for j,b in enumerate(N)),Matrix.zeros(n,1))
            if all(v) and len(set(v))==n:break
            t+=1
        den=lcm(*(int(x.q) for x in v))
        weights=[int(x*den) for x in v]
        order=integer_order(weights)
        assert len(order)==n
        # Use complements to avoid duplicate zero-sum constraints.
        children=set()
        for i in range(n):
            for r in range(2,n//2+1):
                S={order[(i+j)%n] for j in range(r)}
                row=tuple(int(k in S) for k in range(n))
                if r*2==n:row=min(row,tuple(1-x for x in row))
                assert sum(a*b for a,b in zip(row,weights))!=0
                children.add(row)
        for row in sorted(children):visit(rows+(row,))
    visit(((1,)*n,))
    return nodes,sorted(candidates)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--symbolic-size',type=int,default=None)
    args=ap.parse_args()
    check_rational_certificate()
    check_short_window_trap()
    for n in ([args.symbolic_size] if args.symbolic_size else range(2,6)):
        nodes,candidates=symbolic_prime_candidates(n)
        print(f'Symbolic n={n}: nodes={nodes}, candidate primes > n = {candidates}')

if __name__=='__main__':main()
