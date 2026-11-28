"""Schubert coefficients of the residual cycle polynomial F_m (intervals x_i+..+x_j, 1<=i<j<=m-1, (i,j)!=(1,m-1))
in the coinvariant ring, via a_sigma = top coefficient (coefficient of x^delta) of F_m * S_sigma."""
import sys, itertools, time
from functools import lru_cache
from itertools import combinations_with_replacement
from math import gcd
import sympy
m=int(sys.argv[1]); delta=tuple(range(m-1,-1,-1))
# coinvariant reduction with standard convention: basis x^a, a_j <= m-j (j=1..m); top monomial x^delta.
# Groebner basis h_k(x_1..x_k)?? use reversal of the earlier triangular basis: generators h_{m+1-j}(x_1..x_j), leading x_j^{m+1-j} (lex x_m > ... > x_1)
def hmonos(k,upto):   # exponent tuples of h_k(x_1..x_upto) (0-based vars < upto)
    out=[]
    for c in combinations_with_replacement(range(upto),k):
        e=[0]*m
        for v in c: e[v]+=1
        out.append(tuple(e))
    return out
HC={}
@lru_cache(maxsize=None)
def red(mono):
    for j in range(m-1,-1,-1):           # variable j (0-based), bound m-j
        b=m-j
        if mono[j]>=b:
            base=list(mono); base[j]-=b; res={}
            for t in range(0,b):          # x_j^b = -sum_{t<b} x_j^t h_{b-t}(x_1..x_{j-1})
                for e in HC.setdefault((b-t,j),hmonos(b-t,j)):
                    nm=[a+c for a,c in zip(base,e)]; nm[j]+=t
                    for kk,vv in red(tuple(nm)).items(): res[kk]=res.get(kk,0)-vv
            return {k:v for k,v in res.items() if v}
    return {mono:1}
def mul(P,Q):
    out={}
    for a,c in P.items():
        for b,d in Q.items():
            for kk,vv in red(tuple(x+y for x,y in zip(a,b))).items(): out[kk]=out.get(kk,0)+c*d*vv
    return {k:v for k,v in out.items() if v}
def linear(idxs):
    out={}
    for i in idxs:
        e=[0]*m; e[i]=1; out[tuple(e)]=1
    return out
def ddiff(P,i):   # divided difference in (x_i, x_{i+1}), 0-based i
    out={}
    for a,c in P.items():
        p,q=a[i],a[i+1]
        if p==q: continue
        lo,hi=(q,p) if p>q else (p,q); s=1 if p>q else -1
        for k in range(hi-lo):
            e=list(a); e[i]=hi-1-k; e[i+1]=lo+k
            out[tuple(e)]=out.get(tuple(e),0)+s*c
    return {k:v for k,v in out.items() if v}
def reduced_word(w):   # w as tuple (one-line, values 1..m); return word of simple transpositions s_i (0-based) with w = s_{i1}...s_{ik}
    w=list(w); word=[]
    while True:
        for i in range(m-1):
            if w[i]>w[i+1]:
                w[i],w[i+1]=w[i+1],w[i]; word.append(i); break
        else: break
    return word[::-1]   # w = s_word[0] ... applied appropriately
def schubert(u):
    # S_u = d_{u^{-1} w0} x^delta ; d_v = d_{i1}...d_{ik} for reduced word v = s_{i1}...s_{ik}
    w0=tuple(range(m,0,-1))
    uinv=[0]*m
    for pos,val in enumerate(u): uinv[val-1]=pos+1
    v=tuple(uinv[w0[k]-1] for k in range(m))   # (u^{-1} w0)(k) = u^{-1}(w0(k))
    word=reduced_word(v)
    P={delta:1}
    for i in reversed(word): P=ddiff(P,i)
    return P
def length(p): return sum(1 for i in range(m) for j in range(i+1,m) if p[i]>p[j])
t0=time.time()
F={tuple([0]*m):1}
for i in range(1,m):
    for j in range(i+1,m):
        if (i,j)==(1,m-1): continue
        F=mul(F,linear(list(range(i-1,j))))
# sanity: Schubert of identity = 1, top coefficient of x^delta =1
def coef(sigma):
    P=mul(F,schubert(sigma)); return P.get(delta,0)
if len(sys.argv)>2:
    sig=tuple(map(int,sys.argv[2].split(',')))
    print(f"m={m}: length {length(sig)}; a_sigma = {coef(sig)}  ({time.time()-t0:.0f}s)")
else:
    vals=[]
    for sig in itertools.permutations(range(1,m+1)):
        if length(sig)!=m: continue
        c=coef(sig)
        if c: vals.append((sig,c))
    adm=[c for _,c in vals if all(p<=m+1 for p in sympy.factorint(abs(c)))]
    print(f"m={m}: nonzero Schubert coeffs {len(vals)}; min |a| {min(abs(c) for _,c in vals)}; admissible-unit coeffs {len(adm)}  ({time.time()-t0:.0f}s)")
