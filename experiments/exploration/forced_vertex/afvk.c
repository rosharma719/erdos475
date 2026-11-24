// AFV_k: family of k disjoint admissible pairs (distinct sums, sums notin B∪{0,x,y}); need t-rooted valid cycle avoiding x with all pairs adjacent.
// mode: k fixed (all families of size k) ; k=0 => all maximal families
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int p,n,B[32],X,K,pa[16],pb[16]; char vis[64]; int partner[64];
int dfs(int pos,int cnt,unsigned used,int last,unsigned ok){
  if(cnt==n) return pos==0 && ok==(1u<<K)-1;
  for(int i=0;i<n;i++){ if(used>>i&1) continue; int a=B[i]; int w=(pos+a)%p;
    unsigned nok=ok; if(last>=0) for(int q=0;q<K;q++) if((last==pa[q]&&a==pb[q])||(last==pb[q]&&a==pa[q])) nok|=1u<<q;
    if(cnt==n-1){ if(w==0 && nok==(1u<<K)-1) return 1; continue; }
    if(w==0||w==X||vis[w]) continue;
    // prune: if last is in a pair whose partner is still unused and a is not partner, that pair can never become adjacent? (it can, if partner placed before? no: adjacency is consecutive) -> pair must be adjacent somewhere; skip prune for safety
    vis[w]=1; int r=dfs(w,cnt+1,used|1u<<i,a,nok); vis[w]=0; if(r) return 1; }
  return 0;}
int np,pr[256][2]; long long tests,fails;
void fam(int start,int k,int need,unsigned usedel,int *sums,int mode){
  // mode 1: exact size need; mode 0: maximal
  if(mode==1 && k==need){ K=k; memset(vis,0,sizeof vis); vis[1]=1; tests++; if(!dfs(1,1,1u,1,0)){fails++; if(fails<=5){printf("FAIL p=%d B={",p);for(int q=0;q<n;q++)printf("%d,",B[q]);printf("} x=%d pairs",X);for(int q=0;q<K;q++)printf(" (%d,%d)",pa[q],pb[q]);printf("\n");}} return; }
  int extended=0;
  for(int a=start;a<np;a++){ int u=pr[a][0],v=pr[a][1],s=(u+v)%p; if((usedel>>u&1)||(usedel>>v&1)) continue;
    int dup=0; for(int q=0;q<k;q++) if(sums[q]==s) dup=1; if(dup) continue;
    pa[k]=u;pb[k]=v;sums[k]=s; extended=1; fam(a+1,k+1,need,usedel|1u<<u|1u<<v,sums,mode);
    if(mode==1 && tests>4000000) return; }
  if(mode==0 && !extended && k>0){ // maximal (w.r.t. later pairs only; approximate maximality)
    K=k; memset(vis,0,sizeof vis); vis[1]=1; tests++; if(!dfs(1,1,1u,1,0)){fails++; if(fails<=5){printf("MAXFAIL p=%d B={",p);for(int q=0;q<n;q++)printf("%d,",B[q]);printf("} x=%d pairs",X);for(int q=0;q<K;q++)printf(" (%d,%d)",pa[q],pb[q]);printf("\n");}} }
}
int main(int argc,char**argv){ p=atoi(argv[1]); int kmin=atoi(argv[2]); int need=atoi(argv[3]); int mode=need>0;
  for(unsigned m=0;m<(1u<<(p-2));m++){ unsigned M=(m<<1)|1; int k=__builtin_popcount(M); if(k<kmin||k>p-3) continue;
    int s=0; n=0; for(int i=0;i<p-1;i++) if(M>>i&1){B[n++]=i+1;s+=i+1;} if(s%p) continue;
    int inB[64]={0}; for(int i=0;i<n;i++) inB[B[i]]=1;
    for(X=2;X<p;X++){ int Y=(1-X+p)%p; if(Y<=X||inB[X]||inB[Y]) continue;
      np=0; for(int i=1;i<n;i++) for(int j=i+1;j<n;j++){int sm=(B[i]+B[j])%p; if(!sm||inB[sm]||sm==X||sm==Y) continue; pr[np][0]=B[i];pr[np][1]=B[j];np++;}
      int sums[16]; fam(0,0,need,0,sums,mode); } }
  printf("p=%d |B|>=%d %s%d: tests=%lld failures=%lld\n",p,kmin,mode?"k=":"maximal(",need,tests,fails);}
