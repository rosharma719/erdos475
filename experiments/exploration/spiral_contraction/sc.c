// Independent spiral-contraction coverage at prime p.
// Half-walk W=(delta,+M,-delta^rev,-M), delta signed ordering of S\{M}, D distinct, span(D)<=M-1, M+span<=p-1.
// Mode 2: contractions with blocks of length 1 or 2 (cyclic matchings). Mode G: arbitrary blocks (kept-vertex subsets), small s only.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int p,h,mode; unsigned char *mark; int W[64],L; long long walks=0;
int mod(int x){x%=p;return x<0?x+p:x;}
void contract2(){ // enumerate cyclic matchings of steps 0..L-1 (pairs (i,i+1) incl (L-1,0))
  // iterate over subsets of disjoint adjacent pairs via recursion
  int n=L; int used[64];
  // linear DP enumeration: first decide whether pair (L-1,0) used
  for(int wrap=0;wrap<2;wrap++){
    // recursive
    int stack_i[64],stack_m[64]; // simple recursion via function below
    (void)stack_i;(void)stack_m;
    memset(used,0,sizeof used);
    if(wrap){used[L-1]=used[0]=1;}
    // recursive lambda substitute
    void rec(int i,unsigned mask,int ok){
      if(!ok) return;
      if(i>=n){ // add wrap block
        unsigned m=mask; int ok2=1;
        if(wrap){int s=mod(W[L-1]+W[0]); if(!s||(m>>(s-1)&1)) ok2=0; else m|=1u<<(s-1);}
        if(ok2) mark[m]=1; return;}
      if(used[i]){rec(i+1,mask,1);return;}
      // single
      {int s=mod(W[i]); if(!(mask>>(s-1)&1)) rec(i+1,mask|1u<<(s-1),1);}
      // pair (i,i+1)
      if(i+1<n && !used[i+1]){int s=mod(W[i]+W[i+1]); if(s && !(mask>>(s-1)&1)) rec(i+2,mask|1u<<(s-1),1);}
    }
    rec(0,0,1);
  }
}
void contractG(){ // all kept-vertex subsets containing vertex 0 (rotation-invariant enough since we mark all rotations' label sets equal)
  int n=L;
  for(unsigned keep=1;keep<(1u<<n);keep+=2){ // vertex 0 always kept
    unsigned m=0;int s=0,ok=1,first=1;
    for(int i=0;i<n&&ok;i++){ s=mod(s+W[i]); int nextkept=(i+1==n)?1:((keep>>(i+1))&1);
      if(nextkept){ if(!s||(m>>(s-1)&1)) ok=0; else m|=1u<<(s-1); s=0;} }
    if(ok) mark[m]=1;
  }
}
int Sset[32],ns,M,del[32],D[32],usedS[32];
void dfs(int k,int lo,int hi){
  if(k==ns-1){ // build walk
    L=0; for(int i=0;i<k;i++) W[L++]=del[i]; W[L++]=M; for(int i=k-1;i>=0;i--) W[L++]=-del[i]; W[L++]=-M;
    walks++; if(mode==2) contract2(); else contractG(); return;}
  for(int j=0;j<ns-1;j++){ if(usedS[j]) continue;
    for(int sg=1;sg>=-1;sg-=2){ int v=D[k]+sg*Sset[j]; int nlo=v<lo?v:lo,nhi=v>hi?v:hi;
      if(nhi-nlo>M-1||M+nhi-nlo>p-1) continue;
      int dup=0; for(int t=0;t<=k;t++) if(D[t]==v){dup=1;break;} if(dup) continue;
      usedS[j]=1; del[k]=sg*Sset[j]; D[k+1]=v; dfs(k+1,nlo,nhi); usedS[j]=0; } }
}
int main(int argc,char**argv){
  p=atoi(argv[1]); mode=atoi(argv[2]); int smax=argc>3?atoi(argv[3]):99; h=(p-1)/2;
  mark=calloc(1u<<(p-1),1);
  for(unsigned S=1;S<(1u<<h);S++){
    ns=0; for(int i=1;i<=h;i++) if(S>>(i-1)&1) Sset[ns++]=i;
    if(ns>smax) continue;
    M=Sset[ns-1]; D[0]=0; memset(usedS,0,sizeof usedS); dfs(0,0,0);
  }
  // count zero-sum orbits covered
  unsigned N=1u<<(p-1); char *isrep=calloc(N,1); long long tot=0,cov=0; long long bysize_t[64]={0},bysize_c[64]={0};
  for(unsigned m=1;m<N;m++){ int s=0; for(int i=0;i<p-1;i++) if(m>>i&1) s+=i+1; if(s%p) continue;
    unsigned best=m; int covered=0;
    for(int l=1;l<p;l++){ unsigned mm=0; for(int i=0;i<p-1;i++) if(m>>i&1) mm|=1u<<(((i+1)*l)%p-1); if(mm<best) best=mm; if(mark[mm]) covered=1; }
    if(best!=m) continue; int k=__builtin_popcount(m); tot++; bysize_t[k]++; if(covered){cov++;bysize_c[k]++;}
  }
  printf("p=%d mode=%s walks=%lld orbits=%lld covered=%lld\n",p,mode==2?"blocks<=2":"general",walks,tot,cov);
  for(int k=0;k<64;k++) if(bysize_t[k]) printf("  |A|=%d %lld/%lld\n",k,bysize_c[k],bysize_t[k]);
}
