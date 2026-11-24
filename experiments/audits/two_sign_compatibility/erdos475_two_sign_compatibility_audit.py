#!/usr/bin/env python3
"""Consolidated research verifier: two-sign compatible constructions and exact
finite search for the two induction targets. Requires only Python 3 for the
constructive audit. --exhaustive also requires a C++17 compiler (g++).
Usage: python erdos475_two_sign_compatibility_audit.py
       python erdos475_two_sign_compatibility_audit.py --exhaustive --limit 15
The finite tests are evidence, not a uniform proof of the unrestricted targets.
"""
from itertools import combinations

def verts(w):
 s=0; v=[0]
 for x in w[:-1]:s+=x;v.append(s)
 return v

def span(w):
 v=verts(w);return max(v)-min(v)

def check(w,A,D):
 assert sorted(w)==sorted(A) and sum(w)==0
 assert len(set(verts(w)))==len(w) and span(w)<=D,(w,A,D,span(w))

def avoid(C,F):
 C=list(C);T=sum(C);F={f for f in F if 0<f<T}
 assert len(F)<=len(C)-1 or not C and not F
 if not F:return C
 c=max(C);C.remove(c)
 if c in F:
  w=avoid(C,{f for f in F if f<c}|{f-c for f in F if f>c});return [w[0],c]+w[1:]
 if min(F)<c:return [c]+avoid(C,{f-c for f in F if f>c})
 f0=min(F);w=[c]+avoid(C,{f-c for f in F if f>f0});s=0
 for i,x in enumerate(w):
  s+=x
  if s==f0:w[0],w[i+1]=w[i+1],w[0];break
 return w

def path(start,C):
 v=[start]
 for x in C:v.append(v[-1]-x)
 return v

def separate(a,C,b,E):
 C=list(C);E=list(E)
 def score(C,E):
  x=path(a,C);y=path(b,E);z=set(x)&set(y)
  return len(z),-sum(x.index(t)+y.index(t) for t in z)
 while True:
  f=score(C,E)
  if f[0]==0:return C,E
  found=False
  for W in (C,E):
   for i in range(len(W)-1):
    W[i],W[i+1]=W[i+1],W[i]
    if score(C,E)<f:found=True;break
    W[i],W[i+1]=W[i+1],W[i]
   if found:break
  assert found,(a,C,b,E)

def crossing(Y,a):
 Y=sorted(Y,reverse=True);assert max(Y)<a and sum(Y)>2*a
 s=0
 for j,x in enumerate(Y):
  s+=x
  if s>a:return Y[:j+1]
  if s==a:return Y[:j]+crossing(Y[j+1:],x)
 raise AssertionError

def high(a,b,Y):
 X=crossing(Y,a);e=sum(X)-a;R=sorted(set(Y)-set(X))
 assert 0<e<min(X)
 if sum(X)!=b:
  X,R=separate(a,X,b-e,R)
  w=[a]+[-x for x in X]+[b]+[-y for y in R]
  # contraction index: pair starting at j
  j=len(X)+1 if R[0]!=b-a else len(X)
  # insertion around second descending path: cut before first negative after b, after last
  return w,j,('up',len(X)+2,len(w))
 # equal peak: X sums b, R sums a
 candidates=[q for q in R if q<min(X) and q!=e]
 if candidates: q=candidates[0];Z=R;W=X;u,v=a,b
 else:q=min(X);Z=X;W=R;u,v=b,a
 F,G=separate(u,[z for z in Z if z!=q],v,W)
 w=[u]+[-x for x in F]+[v,-q]+[-x for x in G]
 j=len(F)+1 if v==b else 0
 # shift first descending path down: after u through before v
 return w,j,('down',1,1+len(F))

def targetA(X,Y):
 X=sorted(X);Y=sorted(Y);b=X[-1];Q=Y[-1];D=b+Q
 assert b!=Q
 if len(X)==1:w=[b]+[-y for y in Y];j=0
 else:
  a,b=X
  if Q>b:
   if Q-b not in Y:w=[a,b,-Q]+[-y for y in Y if y!=Q];j=1
   elif Q-a not in Y:w=[b,a,-Q]+[-y for y in Y if y!=Q];j=1
   else:
    y=next(y for y in Y if y!=Q and y!=b-a)
    w=[a,b,-y,-Q]+[-z for z in Y if z not in (y,Q)];j=1
  elif a<=Q:
   yy=[y for y in Y if y not in (Q,b-a)]
   if yy:
    y=yy[0];R=[z for z in Y if z!=y]
    # descending from T-y to 0, avoid vertex a -> ascending prefix avoid b-y
    w=[a,b,-y]+[-z for z in avoid(R,{b-y})] if len(R)>=2 else [a,b,-y]+[-z for z in R]
   else:w=[a,b,-Q,-(b-a)]
   j=1
  else:w,j,_=high(a,b,Y)
 check(w,X+[-y for y in Y],D)
 x,y=w[j:j+2];c=x+y;assert x*y<0 and (b in (x,y) or -Q in (x,y)) and c and c not in w,(X,Y,w,j)
 w2=w[:j]+[c]+w[j+2:];check(w2,[z for z in w if z not in (x,y)]+[c],max(w2)-min(w2))
 return w,w2

def targetB(X,Y,M):
 if len(Y)==1 and len(X)>1:
  w,z=targetB(Y,X,M);return [-x for x in w],[-x for x in z]
 X=sorted(X);Y=sorted(Y);b=X[-1];Q=Y[-1];D=b+Q
 assert max(b,Q)<M
 if len(X)==1:
  w=[b]+[-y for y in Y];ins=('up',0,1)
 else:
  a,b=X
  if Q<a:w,_,ins=high(a,b,Y)
  elif Q>a and Q!=b:
   e=Q-a;R=[y for y in Y if y!=Q];v=b-e
   # descending from v, avoid a -> prefix avoid v-a
   R=avoid(R,{v-a}) if len(R)>=2 else R
   w=[a,-Q,b]+[-y for y in R];ins=('up',3,len(w))
  elif Q==b:
   R=[y for y in Y if y!=b]
   if len(R)==1:
    # B symmetric; handled separately, retained for completeness
    assert R[0]==a
    w=[a,-b,-a,b]
    z=[a,-b,-a,M,b,-M] if M!=a+b else [a,b,-a,-M,-b,M]
    if M==a+b:w=[a,b,-a,-b]
    check(w,X+[-y for y in Y],D);check(z,X+[-y for y in Y]+[M,-M],2*M);return w,z
   q=min(R);w=[a]+[-y for y in R if y!=q]+[b,-q,-b];ins=('down',1,len(R))
  else: # Q=a<b
   R=[y for y in Y if y!=a];h=a+b-M
   if len(R)>=3:
    # descending from b avoid a and h -> prefix heights b-a,b-h
    R=avoid(R,{b-a,b-h})
   else:
    assert len(R)==2
    if b-R[0]==h:R=R[::-1]
   w=[a,b,-a]+[-y for y in R];ins=('up',3,len(w))
   if h<=0:
    # W<=M, find one-edge translate
    for i in range(len(w)):
     z=w[:i]+[M,w[i],-M]+w[i+1:]
     if len(set(verts(z)))==len(z) and span(z)<=2*M:break
    else:raise AssertionError((w,M))
    check(w,X+[-y for y in Y],D);check(z,X+[-y for y in Y]+[M,-M],2*M);return w,z
 check(w,X+[-y for y in Y],D)
 dr,i,j=ins;d=M if dr=='up' else -M
 assert i<j,(w,ins)
 z=w[:i]+[d]+w[i:j]+[-d]+w[j:];check(z,X+[-y for y in Y]+[M,-M],2*M)
 return w,z

def subsets_sum(M,T):
 def go(n,T,p):
  if T==0:yield p;return
  for i in range(n,min(T,M)+1):yield from go(i+1,T-i,p+[i])
 yield from go(1,T,[])

def main(maxm=20):
 na=nb=0
 for b in range(2,maxm+1):
  for X in [[b]]+[[a,b] for a in range(1,b)]:
   for Y in subsets_sum(maxm,sum(X)):
    if b!=max(Y):targetA(X,Y);na+=1
    for M in range(max(b,max(Y))+1,maxm+1):targetB(X,Y,M);nb+=1
 print('compatible two-sign cases',na,nb)

CPP = r'''
#include <bits/stdc++.h>
using namespace std;using U=uint64_t;using I=uint32_t;
int M,P,Q,D,db,n,a[32],v[32];long long nodes;int base=30;
bool insertable(){int W=*max_element(v,v+n);for(int i=0;i<n;i++){U s=0;int mx=0,mn=100;for(int j=0;j<n-1;j++){int w=v[(i+j)%n];s|=1ull<<w;mx=max(mx,w);mn=min(mn,w);if(j==0)continue;U t=0;int mt=100;for(int k=j;k<=n;k++){int z=v[(i+k)%n];t|=1ull<<z;mt=min(mt,z);}if(!(s<<M &t)&&mx-mt<=M)return true;} // last arc length n-1 edges handled below
 U all=0;for(int j=0;j<n;j++)all|=1ull<<v[j];int u=v[i],w=v[(i+n-1)%n];U t=(1ull<<u)|(1ull<<w);if(!(all<<M&t)&&W-min(u,w)<=M)return true;
 }return false;}
bool dfsB(I r,int s,U used,int pos){++nodes;if(!r)return s==0&&insertable();I z=r;while(z){int i=__builtin_ctz(z);z&=z-1;int t=s+a[i];if(t<0||t>db)continue;I rr=r^(1u<<i);if(!rr){if(t==0&&insertable())return true;}else if(!(used>>t&1)){v[pos]=t;if(dfsB(rr,t,used|(1ull<<t),pos+1))return true;}}return false;}
int ca,cb;
bool dfsA(I r,int s,int lo,int hi,U used){++nodes;bool pa=!(used>>(ca+base)&1)&&max(hi,ca)-min(lo,ca)<=D;bool pb=!(used>>(cb+base)&1)&&max(hi,cb)-min(lo,cb)<=D;if(!pa&&!pb)return false;if(!r)return s==0;I z=r;while(z){int i=__builtin_ctz(z);z&=z-1;int t=s+a[i];if(max(hi,t)-min(lo,t)>db)continue;I rr=r^(1u<<i);if(!rr){if(t==0)return true;}else if(!(used>>(t+base)&1)&&dfsA(rr,t,min(lo,t),max(hi,t),used|(1ull<<(t+base))))return true;}return false;}
bool solve(int x,int y){vector<int>A;for(int i=1;i<=M;i++){if(x>>(i-1)&1)A.push_back(i);if(y>>(i-1)&1)A.push_back(-i);}P=32-__builtin_clz((unsigned)x);Q=32-__builtin_clz((unsigned)y);D=P+Q;
 if(P==Q){vector<int>B;for(int z:A)if(abs(z)!=P)B.push_back(z);if(B.empty())return true;n=B.size();db=*max_element(B.begin(),B.end())-*min_element(B.begin(),B.end());sort(B.begin(),B.end(),greater<int>());copy(B.begin(),B.end(),a);v[0]=0;return dfsB((1u<<n)-1,0,1,1);}
 vector<pair<int,int>> cand;for(int i:A)if(i>0)for(int j:A)if(j<0&&(i==P||j==-Q)&&i+j&&find(A.begin(),A.end(),i+j)==A.end())cand.push_back({i,j});sort(cand.begin(),cand.end(),[](auto a,auto b){return a.first-a.second>b.first-b.second;});
 for(auto [i,j]:cand){vector<int>B;for(int z:A)if(z!=i&&z!=j)B.push_back(z);B.push_back(i+j);db=*max_element(B.begin(),B.end())-*min_element(B.begin(),B.end());B.pop_back();sort(B.begin(),B.end(),greater<int>());n=B.size();copy(B.begin(),B.end(),a);int c=i+j;ca=i;cb=j;if(dfsA((1u<<n)-1,c,min(0,c),max(0,c),(1ull<<base)|(1ull<<(c+base))))return true;}
 return false;}
int main(int argc,char**argv){M=atoi(argv[1]);int maxm=1<<M;vector<vector<int>> masks(M*(M+1)/2+1);for(int m=1;m<maxm;m++){int s=0;for(int j=0;j<M;j++)if(m>>j&1)s+=j+1;masks[s].push_back(m);}long long cnt[2]={0,0};for(auto &L:masks)for(int x:L)for(int y:L){if(!(x>>(M-1)&1)||x==y)continue;nodes=0;if(!solve(x,y)){cerr<<"FAIL "<<M<<" "<<x<<" "<<y<<" nodes "<<nodes<<endl;for(int i=1;i<=M;i++){if(x>>(i-1)&1)cerr<<i<<",";if(y>>(i-1)&1)cerr<<-i<<",";}cerr<<endl;return 1;}++cnt[y>>(M-1)&1];}cout<<M<<" "<<cnt[0]<<" "<<cnt[1]<<endl;}

'''

def obstruction():
 v=[0,1,6,9,11,8,2];M=7;n=len(v);w=[v[(i+1)%n]-v[i] for i in range(n)]
 check(w,w,11)
 assert sum(x+M in v for x in v)==2
 assert min(v)+M not in v and max(v)-M not in v
 from collections import Counter
 ct=Counter()
 for i in range(n):
  for j in range(1,n):
   r=v[i:]+v[:i];s={a+M for a in r[:j+1]};t=set(r[j:]+r[:1]);z=s|t
   ct['collision' if s&t else max(z)-min(z)]+=1
 assert all(k=='collision' or k>2*M for k in ct)
 print('Fixed-order q=2 obstruction:',dict(ct))

if __name__=='__main__':
 import argparse,subprocess,tempfile
 from pathlib import Path
 ap=argparse.ArgumentParser();ap.add_argument('--exhaustive',action='store_true');ap.add_argument('--limit',type=int,default=15);ap.add_argument('--constructive-limit',type=int,default=20);args=ap.parse_args()
 obstruction();main(args.constructive_limit)
 if args.exhaustive:
  if not 2<=args.limit<=15:ap.error('compiled audit supports limits 2 through 15')
  with tempfile.TemporaryDirectory() as d:
   src=Path(d)/'audit.cpp';exe=Path(d)/'audit';src.write_text(CPP)
   subprocess.run(['g++','-O3','-std=c++17',str(src),'-o',str(exe)],check=True)
   for m in range(2,args.limit+1):subprocess.run([str(exe),str(m)],check=True)
