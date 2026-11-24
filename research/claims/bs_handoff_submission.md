# Erdős #475 — bounded-span research handoff

## Status and exact target

The full conjecture remains open in this work. The bounded-span conjecture (BS) is sufficient: every finite set of distinct nonzero integers B of sum zero, with P=max B and Q=-min B, admits a cyclic ordering whose n distinct cyclic vertices have span at most P+Q. This stronger integer assertion is unproved in general. It is not known here to be necessary for Graham.

For a zero-sum set A in F_p, take increasing least-positive representatives a_1,...,a_n with sum kp. Subtract p from the k largest. The resulting distinct nonzero integer lift has sum zero and diameter P+Q=p-(a_{n-k+1}-a_{n-k})<p. BS would give a simple modular cycle. The earlier nonzero-sum reduction completes the prime-field implication. This argument works for zero-sum sets in composite cyclic groups too.

## New theorem: two monotone paths can be separated

Two strictly decreasing paths on the integer line use prescribed step magnitudes, distinct within each path, in freely chosen orders. Suppose their upper endpoints are distinct and, for all permissible orders, neither lower endpoint can occur on the other path. There exist orders making the two vertex sets disjoint.

Proof: Minimize the number of shared vertices, then maximize the sum of their two position indices. At an interior intersection v, a swap of adjacent steps changes just that vertex to v'!=v, strictly between its original neighbors. Minimality forces v' onto the other path, and maximality forces v' to have an earlier index there. If u_1,u_2 are the predecessors of v on the two decreasing paths, the swap on path 1 implies u_2<=v'<u_1, hence u_2<u_1. Swapping on path 2 gives the reverse strict inequality. At an upper-endpoint collision, swap the internal occurrence; either the collision is removed or its new position on the path starting at v is later, contradicting the objective. Lower-endpoint collisions are excluded by hypothesis. This proves the result. If both paths have the same two endpoints, ignore those endpoints; the interior argument gives disjoint interiors. The proof also supplies an algorithm: make any lexicographically improving swap until there are no prohibited intersections.

## New theorem: BS for at most two elements of either sign

One positive element is trivial by following it with all negatives. Negation handles the analogous cases. Suppose positives are a<b, negative magnitudes form a distinct set C with sum a+b, and Q=max C. If a<=Q, the two monotone paths from a+b to 0 (one using a,b; the other using C) can be separated at all interior vertices by the preceding lemma. Traverse the first in reverse and then the second. Span a+b<=b+Q.

**Strict crossing lemma.** If distinct positive integers C satisfy max C<h and sum C>2h, there is X subset C with h<sum X<h+min X. Induct on h. Read C in decreasing order until its prefix sum first reaches or exceeds h. Strict overshoot gives X immediately, since removing the smallest term returns to a sum below h. In the equality case let x be the smallest term of the prefix. The prefix has at least two terms, so h>=2x. The unused terms are all smaller than x and their sum exceeds h>=2x. Apply induction with threshold x to the unused terms, obtaining Z with x<sum Z<x+min Z. Replace x by Z. The new subset has the required strict inequality, since all retained prefix terms exceed every term of Z.

Now suppose a>Q. Apply the strict crossing lemma with h=a, and put Y=C\\X, e=sum X-a, so 0<e<min X<=Q<a. If sum X!=b, use the cycle (a,-X,b,-Y), where each list of negative magnitudes is permuted. The two descending paths have endpoints a,-e and b-e,0. The first path's proper prefixes have positive vertices (every proper subset of X has sum<a), so it never visits 0. The second path stays nonnegative, so never visits -e. Their upper endpoints are distinct because sum X!=b. The separation lemma gives disjoint paths. The span is max(a+e,b)<=b+Q.

**Equal-peak exception.** If sum X=b, then sum Y=a. Let q=min C and Z be the member of {X,Y} containing q; call the other W. Set u=sum Z and v=sum W. Use the cycle (u,-(Z\\{q}),v,-q,-W). The first descending path goes u to q; the second free descending path goes v to 0, with a fixed bridge q -> q+v -> v. The second free path cannot visit q since every magnitude in W exceeds q, and its nonzero suffix sums all exceed q. The first path cannot visit 0. The upper endpoints u,v are distinct. The bridge peak q+v is above both paths: when u=a,v=b this is immediate; when u=b,v=a, q belongs to X and q>e=b-a, so q+a>b. In both cases the free paths can be separated by the lemma, and the fixed bridge adds no collisions. Their span is q+v<=b+Q. This proves BS for two positive steps, and by negation for two negative steps.

Audit: exhaustive testing of every distinct negative-magnitude subset of [1,11] and every possible positive pair a<b totaling its sum yielded 32,232 cases (20,029 mass, 11,333 strict crossing, 870 bridge), no failures. A separate seeded 1,000-case random test had 527,465,8 cases respectively and no failures. Proof is independent of these tests. This is a theorem about the stronger bounded-span problem; the corresponding modular index-two families were already covered by previous work.

## General safe contraction criterion

For any legal opposite-sign contraction (x,-y)->c=x-y, where c is nonzero and absent from the other steps, let the smaller set have a simple integer cycle with vertices V, interval [L,H], and W=H-L. Write u for the origin of c, so both u,u+c are in V. The expansion candidates are u+x and u-y. The first is admissible exactly when u+x is unoccupied and u<=L+D-x; the second exactly when u-y is unoccupied and u>=H-D+y, where D>=W is the desired final span. Both expansions increase span by at most min(x,y), since u and u+c both lie in [L,H]. Their candidates differ by x+y. Thus W+min(x,y)<=D and W<x+y imply that at least one is unoccupied and admissible. For the extremal contraction (P,-Q)->P-Q, a sufficient condition is W<=max(P,Q). A cardinality-minimal BS counterexample must therefore resist all legal contractions meeting the criterion.

For the extremal pair, with W<D=P+Q, the safe origin zone is [H-P,L+Q]. If u lies there both candidates are admissible by span and at least one is unoccupied. Outside it only one option fits; that option can be occupied.

**Exact counterexample to universal expansion:** A=(-5,-3,-2,1,2,3,4), P=4,Q=5. Contract 4,-5 to -1, giving B={-3,-2,-1,1,2,3}. The bounded cycle (-1,2,3,1,-3,-2) has vertices (0,-1,1,4,5,2), span 6. Inserting 4 hits an occupied vertex; inserting -5 makes span 10>9. A different smaller cycle does expand successfully, yielding (-5,4,-3,-2,3,1,2), which satisfies BS. The obstruction refutes arbitrary-cycle extension only.

## Exact obstruction to monotone adjacent-swap compression

Let B={±1,±2,±3,±4}, D=8, and w=(-4,-3,-2,1,2,4,-1,3). Its cyclic vertices are (0,-4,-7,-9,-8,-6,-2,-3), span 9. At boundary i, the swapped vertex is f_i=v_i+w_i-w_{i-1} (indices cyclic). The alternatives are (-7,-3,-6,-6,-7,-4,-7,1). The first seven are occupied, and the last gives span 10. Hence not even a plateau of equal-span single adjacent swaps is available. This disproves the universal monotone-compression strategy. A temporary increase to 10 suffices, via the following cyclic words:

```
(-4,-3,-2,1,2,4,-1,3)  9
(-4,-3,-2,1,2,4,3,-1)  10
(-4,-3,-2,1,2,3,4,-1)  10
(-4,-3,-2,1,3,2,4,-1)  10
(-4,-3,-2,1,3,4,2,-1)  10
(-4,-3,-2,1,3,4,-1,2)  9
(-4,-3,1,-2,3,4,-1,2)  8
```

Each word differs from the previous one by a cyclic adjacent swap and is simple. A separate example shows that even simultaneous independent swaps need not strictly compress: w=(-4,-3,-2,-1,4,1,2,3), vertices (0,-4,-7,-9,-10,-6,-5,-3), alternatives (-7,-3,-6,-8,-5,-9,-4,-2). Moving boundary 0 forces boundaries 2,5,3; moving boundary 4 forces 6,1,7. Each forced set contains adjacent indices, so neither extreme can be moved by independent swaps while maintaining simplicity. This second example does have a non-increasing multi-step repair, unlike the first.

## Exact remaining obligation

Prove BS for arbitrary sign counts, or find a different modular construction. A hypothetical minimal BS counterexample must have at least three positive and three negative steps, total positive mass exceeding P+Q, and resist every legal contraction whose reduced diameter meets the safe contraction criterion. These conditions do not yet yield a contradiction. Extremal path separation cannot simply be asserted for arbitrary many paths, and the monotone compression and arbitrary-cycle expansion strategies have concrete obstructions above. A successful compression argument must permit more powerful exchanges or temporary range increases and control their endpoint behavior. No full proof or counterexample to Graham was obtained here.

The unrestricted integer sequencing theorem is already in Kravitz, *Rearranging small sets for distinct partial sums*, https://arxiv.org/abs/2407.01835. Our new target is the additional span guarantee, not the existence of unrestricted integer orderings. Graham's all-primes question is recorded at https://www.erdosproblems.com/475.

## Consolidated source files

The following code blocks are the actual source files. Save each block under its indicated name if executing them. The historical scripts are retained unchanged; their search scope and claims should be interpreted according to their own code and the prior report, not as proofs of the general conjecture.

### erdos475_bounded_span_audit.py

```python
from itertools import combinations
from functools import lru_cache

def solve(A,W):
 n=len(A);F=(1<<n)-1
 @lru_cache(None)
 def f(m,s,v):
  if m==F:return ()
  for i,a in enumerate(A):
   if m>>i&1:continue
   t=s+a
   if not 0<=t<=W:continue
   if m|1<<i==F:
    if t==0:return (a,)
   elif not v>>t&1:
    w=f(m|1<<i,t,v|1<<t)
    if w is not None:return (a,)+w
  return None
 return f(0,0,1)
for M in range(1,12):
 A0=list(range(-M,0))+list(range(1,M+1));count=0
 for k in range(2,2*M+1):
  for A in combinations(A0,k):
   if sum(A) or max(map(abs,A))!=M:continue
   count+=1
   W=max(A)-min(A)
   if solve(A,W) is None:print('FAIL',M,A,W,flush=True);raise SystemExit
 print(M,count,flush=True)

```

### erdos475_core_search.cpp

```cpp
// Exhaustive canonical-core search with independent, non-root switches.
// Input: p and five unpaired residues. Maximal symmetric completion only.
// Output: first witness, or failure for the specified switch budget.
#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <vector>
#include <set>
using namespace std;
int p;
int mod(long long x){int r=x%p;return r<0?r+p:r;}
struct Opt {vector<int>D,E;int d,e;};
int main(int argc,char**argv){
 int cap=argc>1?stoi(argv[1]):1;
 vector<int>U(5);if(!(cin>>p))return 0;for(int&u:U)cin>>u;sort(U.begin(),U.end());
 vector<int>A(p,1);A[0]=0;for(int u:U)A[p-u]=0;
 vector<Opt>opts;
 for(int i=0;i<5;i++)for(int j=i+1;j<5;j++){
  vector<int>X{U[i],U[j]},Y;for(int k=0;k<5;k++)if(k!=i&&k!=j)Y.push_back(U[k]);int c=mod(U[i]+U[j]);
  if(!A[c])opts.push_back({X,Y,c,p-c});
  else for(int x:X)for(int y:Y){vector<int>D{X[0]==x?X[1]:X[0],p-c},E{c};for(int z:Y)if(z!=y)E.push_back(z);opts.push_back({D,E,p-x,p-y});}
 }
 vector<int>V,ix(p),where(p),alt,step;
 long long candidates=0;
 for(auto opt:opts){
  auto [D,E,d,e]=opt;sort(D.begin(),D.end());sort(E.begin(),E.end());vector<int>B=A;for(int a:D)B[a]=0;for(int a:E)B[a]=0;B[d]=B[e]=1;for(int a=1;a<p;a++)assert(B[a]==B[p-a]);
  vector<int>missing;for(int a=1;a<=p/2;a++)if(!B[a])missing.push_back(a);
  for(int l=1;l<=p/2;l++){
   vector<int>omit;for(int a:missing){int t=mod(1LL*l*a);omit.push_back(min(t,p-t));}sort(omit.begin(),omit.end());
   step.clear();int parity=0;size_t mi=0;for(int a=1;a<=p/2;a++){if(mi<omit.size()&&a==omit[mi]){mi++;continue;}step.push_back(parity++%2?p-a:a);}int k=step.size();for(int i=k-2;i>=0;i--)step.push_back(p-step[i]);step.push_back(p-step[k-1]);int n=step.size();
   V.resize(n);alt.resize(n);fill(ix.begin(),ix.end(),-1);int s=0;for(int i=0;i<n;i++){assert(ix[s]<0);ix[s]=i;V[i]=s;where[step[i]]=i;s=mod(s+step[i]);}assert(s==0);for(int i=0;i<n;i++)alt[i]=mod(V[i]+step[i]-step[(i+n-1)%n]);
   for(int sg:{1,-1}){
    int dd=mod(1LL*d*l*sg),ee=mod(1LL*e*l*sg),u=V[where[dd]],v=V[where[ee]];
    do{do{
      candidates++;array<int,3>K{mod(u+1LL*D[0]*l*sg),mod(v+1LL*E[0]*l*sg),mod(v+1LL*(E[0]+E[1])*l*sg)};
      if(K[0]==K[1]||K[0]==K[2]||K[1]==K[2])continue;
      vector<int>need,used;bool good=true;for(int h:K)if(ix[h]>=0)need.push_back(ix[h]);
      for(size_t j=0;j<need.size()&&good;j++){
       int i=need[j],a=step[(i+n-1)%n],b=step[i],h=alt[i];
       if((cap>=0&&int(need.size())>cap)||i==0||a==dd||a==ee||b==dd||b==ee||find(K.begin(),K.end(),h)!=K.end()||find(used.begin(),used.end(),h)!=used.end()){good=false;break;}
       for(int t:need)if((i+1)%n==t||(t+1)%n==i){good=false;break;}if(!good)break;
       used.push_back(h);int t=ix[h];if(t>=0&&find(need.begin(),need.end(),t)==need.end())need.push_back(t);
      }
      if(good){
       // Independent direct validation in scaled coordinates.
       vector<int>w=step;for(int i:need)swap(w[i-1],w[i]);vector<int>out;for(int a:w){if(a==dd)for(int z:D)out.push_back(mod(1LL*z*l*sg));else if(a==ee)for(int z:E)out.push_back(mod(1LL*z*l*sg));else out.push_back(a);}
       vector<int>seen(p),labels(p);s=0;for(int a:out){assert(!labels[a]++);s=mod(s+a);assert(!seen[s]++);}assert(s==0);for(int a=1;a<p;a++)assert(A[a]==labels[mod(1LL*a*l*sg)]);
       cout<<"PASS "<<p<<" l="<<l<<" sign="<<sg<<" d="<<d<<" e="<<e<<" D=";for(int a:D)cout<<a<<",";cout<<" E=";for(int a:E)cout<<a<<",";cout<<" switches=";for(int i:need)cout<<i<<",";cout<<" candidates="<<candidates<<"\n";return 0;
      }
    }while(next_permutation(E.begin(),E.end()));}while(next_permutation(D.begin(),D.end()));
   }
  }
 }
 cout<<"FAIL "<<p<<" cap="<<cap<<" candidates="<<candidates<<"\n";
}

```

### erdos475_flexible_core.py

```python
"""Independent-switch repair for five unpaired elements. Finite search only.
Requires erdos475_asymmetry_audit.py, standard library only.
"""
from itertools import combinations, permutations
from random import Random
from erdos475_asymmetry_audit import sym, valid, maximal_completion

def search(A,p,U,maxswitch=None):
    for X in combinations(sorted(U),2):
        X=set(X);Y=U-X;c=sum(X)%p
        if c not in A:opts=[(X,Y,c,-c%p)]
        else:opts=[((X-{x})|{-c%p},(Y-{y})|{c},-x%p,-y%p) for x in sorted(X) for y in sorted(Y)]
        for D,E,d,e in opts:
            B=A-(D|E)|{d,e}; assert B=={-x%p for x in B}
            for l in range(1,p//2+1):
                w0=sym(B,p,l)
                for sg in (1,-1):
                    w=tuple(sg*x%p for x in w0)
                    V=[];s=0;u=v=None
                    for a in w:
                        V.append(s)
                        if a==d:u=s
                        if a==e:v=s
                        s=(s+a)%p
                    pos={v:i for i,v in enumerate(V)}
                    n=len(w);alt=[(V[i]+w[i]-w[i-1])%p for i in range(n)]
                    movable=[i!=0 and w[i-1] not in (d,e) and w[i] not in (d,e) for i in range(n)]
                    for dd in permutations(sorted(D)):
                        h=(u+dd[0])%p
                        for ee in permutations(sorted(E)):
                            j=(v+ee[0])%p;k=(j+ee[1])%p;K={h,j,k}
                            if len(K)!=3:continue
                            need={pos[x] for x in K if x in pos};todo=list(need);used=set();good=True
                            while todo:
                                i=todo.pop()
                                if (maxswitch is not None and len(need)>maxswitch) or not movable[i] or (i-1)%n in need or (i+1)%n in need or alt[i] in K or alt[i] in used:
                                    good=False;break
                                used.add(alt[i]);t=pos.get(alt[i])
                                if t is not None and t not in need:need.add(t);todo.append(t)
                            if not good:continue
                            out=list(w)
                            for i in need:out[i-1],out[i]=out[i],out[i-1]
                            z=tuple(a for b in out for a in (dd if b==d else ee if b==e else (b,)))
                            assert len(z)==len(A)==len(set(z)) and set(z)==A and sum(z)%p==0 and valid(z,p)
                            return (l,sg,dd,ee,d,e,tuple(sorted(need)),z)
    return None

def cases(p,count,seed):
    rng=Random(seed);seen=set()
    while len(seen)<count:
        U=set(rng.sample(range(1,p),4));U.add(-sum(U)%p)
        if len(U)!=5 or 0 in U or any(-a%p in U for a in U) or any((a+b)%p in U for a,b in combinations(U,2)):continue
        key=tuple(sorted(U))
        if key in seen:continue
        seen.add(key);yield U

if __name__=='__main__':
    import argparse,time
    a=argparse.ArgumentParser();a.add_argument('--count',type=int,default=20);a.add_argument('--primes',type=int,nargs='+',default=[211,503,1009]);args=a.parse_args()
    for p,U in [(211,{31,87,133,179,203}),(503,{112,168,388,406,435})]:
        ans=search(maximal_completion(p,U),p,U,1);print('known',p,ans[:-1] if ans else None,flush=True)
    for p in args.primes:
        t=time.monotonic();hist={};fail=[]
        for U in cases(p,args.count,475+p):
            ans=search(maximal_completion(p,U),p,U,1)
            if ans is None:
                fail.append(tuple(sorted(U))); print('ONE SWITCH FAILURE',p,fail[-1],flush=True)
            else:hist[len(ans[-2])]=hist.get(len(ans[-2]),0)+1
        print(p,'counts',hist,'failures',fail,'seconds',round(time.monotonic()-t,2),flush=True)

```

### erdos475_asymmetry_audit.py

```python
"""Erdos #475: five-unpaired-element contraction audit.
Standard library only. Default verifies two template failures and a successful
symmetric-core expansion. --exhaustive also checks every symmetric completion
of each multiplicative orbit of weakly sum-free five-element zero-sum remainders
for p=23,29,31. This is not a proof or counterexample to Graham's conjecture.
"""
from itertools import combinations,product

def valid(w,p):
 s=0; v=set()
 for a in w:
  s=(s+a)%p
  if s in v:return False
  v.add(s)
 return True

def four(A,p):
 U=sorted(a for a in A if -a%p not in A)
 assert len(U)==4
 M=p//2
 for b in U[1:]:
  l=pow((U[0]+b)%p,-1,p); il=pow(l,-1,p)
  B={a*l%p for a in A};
  # descending scan, choose path for each unpaired
  def rec(i,P,Q,e,f):
   if i==0:
    if not P or not Q:return
    P=P[::-1]; Q=Q[::-1]
    for X,Y,sgn in [(P,Q,1),(Q,P,-1)]:
     w=X+[-a for a in Y[-2::-1]]+[-Y[-1]]
     yield tuple(a*il*sgn%p for a in w)
    return
   a=i in B; b=p-i in B
   if a and b:
    if e==f:yield from rec(i-1,P+[e*i],Q+[f*i],-e,-f)
   elif a or b:
    x=i if a else -i
    if x==e*i:yield from rec(i-1,P+[x],Q,-e,f)
    if -x==f*i:yield from rec(i-1,P,Q+[-x],e,-f)
   else:yield from rec(i-1,P,Q,e,f)
  yield from rec(M,[],[],1,1)

def solve(A,p,U):
 for a,b in combinations(sorted(U),2):
  c=(a+b)%p
  if c not in A:
   opts=[(a,b,c)]
  else:opts=[(a,-c%p,-b%p),(b,-c%p,-a%p)]
  for x,y,z in opts:
   B=(A-{x,y})|{z}
   assert len(B)==len(A)-1 and z not in A
   for w in four(B,p):
    assert valid(w,p),(w,B,p)
    j=w.index(z)
    for u,v in [(x,y),(y,x)]:
     w2=w[:j]+(u,v)+w[j+1:]
     if valid(w2,p):return w2
 return None

def reps(p):
 seen=set()
 for U in combinations(range(1,p),5):
  if sum(U)%p or any(-x%p in U for x in U) or any((x+y)%p in U for x,y in combinations(U,2)):continue
  U=frozenset(U)
  if U in seen:continue
  seen.update(frozenset(x*l%p for x in U) for l in range(1,p))
  yield U

from itertools import permutations

def sym(B,p,l):
 il=pow(l,-1,p)
 mags=sorted(min(a*l%p,-a*l%p) for a in B if a<(-a%p))
 X=[a if i%2==0 else -a for i,a in enumerate(mags)]
 return tuple(a*il%p for a in X+[-a for a in X[-2::-1]]+[-X[-1]])

def double(A,p,U):
 for pair in combinations(sorted(U),2):
  X=set(pair);Y=U-X;c=sum(X)%p
  if c not in A:
   opts=[(X,Y,c,-c%p)]
  else:
   opts=[((X-{x})|{-c%p},(Y-{y})|{c},-x%p,-y%p) for x in X for y in Y]
  for D,E,d,e in opts:
   B=A-(D|E)|{d,e}
   assert B=={-x%p for x in B} and len(B)==len(A)-3
   for l in range(1,p//2+1):
    w=sym(B,p,l); assert valid(w,p)
    # use both global orientations of x_i signs? B symmetric, negation gives alternative order, not same original expansion. try both signs (reverse not needed)
    for w in [w,tuple(-x%p for x in w)]:
     s=0;V=set();u=v=None
     for a in w:
      V.add(s)
      if a==d:u=s
      if a==e:v=s
      s=(s+a)%p
     for dd in permutations(D):
      s=u;H=set()
      for a in dd[:-1]:s=(s+a)%p;H.add(s)
      if H&V or len(H)!=len(dd)-1:continue
      for ee in permutations(E):
       s=v;J=set()
       for a in ee[:-1]:s=(s+a)%p;J.add(s)
       if J&(V|H) or len(J)!=len(ee)-1:continue
       w2=tuple(a for b in w for a in (dd if b==d else ee if b==e else (b,)))
       assert valid(w2,p) and set(w2)==A
       return (pair,d,e,l,dd,ee,w2)
 return None


def maximal_completion(p,U):
    assert len(U)==5 and sum(U)%p==0
    assert all(-a%p not in U for a in U)
    assert all((a+b)%p not in U for a,b in combinations(U,2))
    return set(range(1,p))-{-a%p for a in U}

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exhaustive',action='store_true')
    args=parser.parse_args()
    p=211; U={31,87,133,179,203}; A=maximal_completion(p,U)
    assert solve(A,p,U) is None
    ans=double(A,p,U)
    assert ans is not None and valid(ans[-1],p) and set(ans[-1])==A
    print('p=211: one-contraction template fails; two-block template succeeds:',ans[:-1])
    p=503; U={112,168,388,406,435}; A=maximal_completion(p,U)
    assert solve(A,p,U) is None
    assert double(A,p,U) is None
    print('p=503: both stated canonical templates fail.')
    if args.exhaustive:
        for p in (23,29,31):
            count=0
            for U in reps(p):
                av=[a for a in range(1,p//2+1) if a not in U and p-a not in U]
                for mask in range(1<<len(av)):
                    A=set(U)|{v for i,a in enumerate(av) if mask>>i&1 for v in (a,p-a)}
                    w=solve(A,p,U)
                    assert w is not None and valid(w,p) and set(w)==A and len(w)==len(A)
                    count+=1
            print(f'p={p}: {count} completions checked; no failures')

```

### erdos475_span_two_sign_audit.py

```python
from itertools import combinations, permutations
from random import Random

def vertices(xs,start):
    out=[start]
    for x in xs: out.append(out[-1]-x)
    return out

def score(xs,x0,ys,y0,ignore=frozenset()):
    v=vertices(xs,x0);w=vertices(ys,y0)
    common=(set(v)&set(w))-ignore
    return len(common),-sum(v.index(z)+w.index(z) for z in common)

def separate(xs,x0,ys,y0,ignore=frozenset()):
    xs=list(xs);ys=list(ys)
    while True:
        old=score(xs,x0,ys,y0,ignore)
        if old[0]==0:return xs,ys
        changed=False
        for side in (xs,ys):
            for i in range(len(side)-1):
                side[i],side[i+1]=side[i+1],side[i]
                if score(xs,x0,ys,y0,ignore)<old:
                    changed=True;break
                side[i],side[i+1]=side[i+1],side[i]
            if changed:break
        if not changed:raise AssertionError(('separation failed',xs,x0,ys,y0,ignore,old))

def strict_cross(vals,h):
    assert max(vals)<h and sum(vals)>2*h
    vals=sorted(vals,reverse=True);s=0
    for i,x in enumerate(vals):
        s+=x
        if s>h:
            out=vals[:i+1];assert h<sum(out)<h+min(out)
            return out
        if s==h:
            out=vals[:i]+strict_cross(vals[i+1:],x)
            assert h<sum(out)<h+min(out)
            return out
    raise AssertionError('unreachable')

def solve_two(a,b,qs):
    assert 0<a<b and len(qs)==len(set(qs)) and min(qs)>0 and sum(qs)==a+b
    Q=max(qs)
    if a<=Q:
        X,Y=separate([a,b],a+b,qs,a+b,{0,a+b})
        return tuple(X[::-1]+[-x for x in Y]),'mass'
    X=strict_cross(qs,a);Y=sorted(set(qs)-set(X));e=sum(X)-a
    if sum(X)!=b:
        X,Y=separate(X,a,Y,b-e)
        return tuple([a]+[-x for x in X]+[b]+[-y for y in Y]),'strict'
    q=min(qs)
    Z,W=(X,Y) if q in X else (Y,X)
    u,v=sum(Z),sum(W)
    Z=list(set(Z)-{q})
    Z,W=separate(Z,u,W,v)
    return tuple([u]+[-z for z in Z]+[v,-q]+[-w for w in W]),'bridge'

def verify(w,A,D):
    assert sorted(w)==sorted(A) and sum(w)==0
    V=[0]
    for a in w[:-1]:V.append(V[-1]+a)
    assert len(set(V))==len(V) and max(V)-min(V)<=D,(w,V,D)
    return V

def exhaustive(M):
    count={'mass':0,'strict':0,'bridge':0}
    for k in range(2,M+1):
        for qs in combinations(range(1,M+1),k):
            T=sum(qs)
            for a in range(1,(T+1)//2):
                b=T-a
                w,case=solve_two(a,b,qs)
                verify(w,[a,b]+[-x for x in qs],b+max(qs));count[case]+=1
    return count

def check_examples():
    B=(-1,2,3,1,-3,-2)
    V=verify(B, B, 6)
    assert 4 in V and max(max(V),-5)-min(min(V),-5)==10
    A=(-5,4,-3,-2,3,1,2);verify(A,A,9)
    w=(-4,-3,-2,1,2,4,-1,3);V=verify(w,w,9)
    opts=[]
    for i,x in enumerate(V):
        y=x+w[i]-w[i-1]; W=V.copy();W[i]=y
        opts.append(None if len(set(W))<len(W) else max(W)-min(W))
    assert opts==[None]*7+[10]
    return V,opts

if __name__=='__main__':
    print('exhaustive M=11:',exhaustive(11))
    rng=Random(475);counts={'mass':0,'strict':0,'bridge':0}
    for _ in range(1000):
        M=rng.randint(12,100);qs=rng.sample(range(1,M+1),rng.randint(2,min(15,M)))
        T=sum(qs);a=rng.randint(1,(T-1)//2);b=T-a
        w,case=solve_two(a,b,qs);verify(w,[a,b]+[-x for x in qs],b+max(qs));counts[case]+=1
    print('random:',counts)
    print('obstructions:',check_examples())

```
