// AFV2: two disjoint admissible inner pairs (u1,v1),(u2,v2) in B\{t}, sums s1!=s2, each notin B∪{0,x,y};
// need t-rooted valid cycle avoiding x with both pairs adjacent.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int p,n,B[32],X,P[2][2]; char vis[64];
int adj(int a,int b,int k){return (a==P[k][0]&&b==P[k][1])||(a==P[k][1]&&b==P[k][0]);}
int dfs(int pos,int cnt,unsigned used,int last,int ok){
  if(cnt==n) return pos==0 && ok==3;
  for(int i=0;i<n;i++){ if(used>>i&1) continue; int a=B[i]; int w=(pos+a)%p;
    int nok=ok; if(last>=0){ if(adj(last,a,0)) nok|=1; if(adj(last,a,1)) nok|=2; }
    if(cnt==n-1){ if(w==0 && nok==3) return 1; continue; }
    if(w==0||w==X||vis[w]) continue; vis[w]=1; int r=dfs(w,cnt+1,used|1u<<i,a,nok); vis[w]=0; if(r) return 1; }
  return 0;}
int main(int argc,char**argv){ p=atoi(argv[1]); int kmin=atoi(argv[2]); long long tests=0,fails=0;
  for(unsigned m=0;m<(1u<<(p-2));m++){ unsigned M=(m<<1)|1; int k=__builtin_popcount(M); if(k<kmin||k>p-3) continue;
    int s=0; n=0; for(int i=0;i<p-1;i++) if(M>>i&1){B[n++]=i+1;s+=i+1;} if(s%p) continue;
    int inB[64]={0}; for(int i=0;i<n;i++) inB[B[i]]=1;
    for(X=2;X<p;X++){ int Y=(1-X+p)%p; if(Y<=X||inB[X]||inB[Y]) continue;
      int pr[256][2],np=0;
      for(int i=1;i<n;i++) for(int j=i+1;j<n;j++){int sm=(B[i]+B[j])%p; if(!sm||inB[sm]||sm==X||sm==Y) continue; pr[np][0]=B[i];pr[np][1]=B[j];np++;}
      for(int a=0;a<np;a++) for(int b=a+1;b<np;b++){
        if(pr[a][0]==pr[b][0]||pr[a][0]==pr[b][1]||pr[a][1]==pr[b][0]||pr[a][1]==pr[b][1]) continue;
        if((pr[a][0]+pr[a][1])%p==(pr[b][0]+pr[b][1])%p) continue;
        P[0][0]=pr[a][0];P[0][1]=pr[a][1];P[1][0]=pr[b][0];P[1][1]=pr[b][1];
        memset(vis,0,sizeof vis); vis[1]=1; tests++;
        if(!dfs(1,1,1u,1,0)){ fails++; if(fails<=6){printf("AFV2 FAIL p=%d B={",p); for(int q=0;q<n;q++) printf("%d,",B[q]); printf("} x=%d pairs (%d,%d),(%d,%d)\n",X,P[0][0],P[0][1],P[1][0],P[1][1]);} } } } }
  printf("p=%d |B|>=%d AFV2 tests=%lld failures=%lld\n",p,kmin,tests,fails);}
