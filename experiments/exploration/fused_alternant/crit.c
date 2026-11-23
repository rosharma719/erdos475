// For zero-sum A in Z_p^*, merge pair (a1,a2) with z=a1+a2 not in A∪{0}:
// S = sum over orderings pi of B=A\{a1,a2} of sgn(pi) * prod_{0<=i<j<=n}(u_j-u_i) * prod_{j=1}^{n-1}(u_j+a2)  mod p
// Report how often S==0 (criterion fails) and whether a valid ordering exists anyway.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int p,n,B[64],used[64],u[64],a2; long long S; long long cnt;
long long md(long long x){x%=p; if(x<0)x+=p; return x;}
void dfs(int d,int sg,long long w){
  if(d==n){ S=md(S+sg*w); cnt++; return;}
  // sign: choosing B[i] at position d: sign changes by (-1)^{#unused indices less than i}
  int less=0;
  for(int i=0;i<n;i++){ if(used[i]) continue;
    int nu=md(u[d]+B[i]);
    long long f=1; int ok=1;
    for(int j=0;j<=d;j++){ long long df=md(nu-u[j]); if(!df){ok=0;break;} f=f*df%p; }
    if(ok && d+1<n){ long long g=md(nu+a2); if(!g) ok=0; else f=f*g%p; }
    if(ok){ used[i]=1; u[d+1]=nu; dfs(d+1,(less&1)?-sg:sg,w*f%p); used[i]=0; }
    less++;
  }
}
int main(int argc,char**argv){
  p=atoi(argv[1]); int kmin=atoi(argv[2]), kmax=atoi(argv[3]);
  long long tot=0,fail=0,failvalid=0,nofp=0;
  for(long long mask=1;mask<(1LL<<(p-1));mask++){
    int k=__builtin_popcountll(mask); if(k<kmin||k>kmax) continue;
    int A[64],m=0,s=0,inA[64]={0};
    for(int i=0;i<p-1;i++) if(mask>>i&1){A[m++]=i+1; s+=i+1; inA[i+1]=1;}
    if(s%p) continue;
    // scaling orbit rep: require mask minimal under multiplication
    int rep=1;
    for(int l=2;l<p&&rep;l++){ long long mm=0; for(int i=0;i<m;i++) mm|=1LL<<((A[i]*l)%p-1); if(mm<mask) rep=0; }
    if(!rep) continue;
    for(int x=0;x<m;x++) for(int y=0;y<m;y++){ if(x==y) continue;
      int z=(A[x]+A[y])%p; if(z==0||inA[z]) continue;
      n=0; for(int i=0;i<m;i++) if(i!=x&&i!=y) B[n++]=A[i];
      a2=A[y]; memset(used,0,sizeof used); u[0]=0; S=0; cnt=0;
      dfs(0,1,1);
      tot++;
      if(S==0){ fail++; if(cnt>0) failvalid++; }
      if(cnt==0) nofp++;
    }
  }
  printf("p=%d k=%d..%d pairs=%lld criterionZero=%lld (of which FP still true=%lld) FPfalse=%lld rate=%.4f 1/p=%.4f\n",p,kmin,kmax,tot,fail,failvalid,nofp,(double)fail/tot,1.0/p);
}
