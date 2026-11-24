// For every zero-sum B in Z_p^* (orbit reps under dilation), every t in B, every x not in {0,t,t/2}:
// exists a valid cycle (distinct partial sums, closes at 0) starting with t whose vertex set avoids x?
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int p,el[32],ne,X; char vis[64]; long long nodes;
int dfs(int pos,int cnt,unsigned used){
  if(cnt==ne) return pos==0;
  for(int i=0;i<ne;i++){ if(used>>i&1) continue; int w=(pos+el[i])%p;
    if(cnt==ne-1){ if(w==0) return 1; continue;}
    if(w==0||w==X||vis[w]) continue; vis[w]=1; int r=dfs(w,cnt+1,used|1u<<i); vis[w]=0; if(r) return 1;}
  return 0;}
int main(int argc,char**argv){ p=atoi(argv[1]); int kmin=atoi(argv[2]),kmax=atoi(argv[3]);
  long long tests=0,fails=0;
  for(unsigned m=1;m<(1u<<(p-1));m++){ int k=__builtin_popcount(m); if(k<kmin||k>kmax) continue;
    int s=0; for(int i=0;i<p-1;i++) if(m>>i&1) s+=i+1; if(s%p) continue;
    int rep=1; for(int l=2;l<p&&rep;l++){unsigned mm=0; for(int i=0;i<p-1;i++) if(m>>i&1) mm|=1u<<(((i+1)*l)%p-1); if(mm<m) rep=0;} if(!rep) continue;
    int B[32],nb=0; for(int i=0;i<p-1;i++) if(m>>i&1) B[nb++]=i+1;
    for(int ti=0;ti<nb;ti++){ int t=B[ti]; int half=(t*((p+1)/2))%p;
      ne=0; el[ne++]=t; for(int i=0;i<nb;i++) if(i!=ti) el[ne++]=B[i];
      for(X=1;X<p;X++){ if(X==t||X==half) continue;
        memset(vis,0,sizeof vis); vis[t]=1; if(X==t) continue;
        int ok = (ne==1)?0:dfs(t,1,1u); tests++;
        if(!ok){ fails++; if(fails<=10){ printf("FAIL p=%d B={",p); for(int i=0;i<nb;i++) printf("%d,",B[i]); printf("} t=%d x=%d\n",t,X);} } } } }
  printf("p=%d sizes %d..%d: tests=%lld failures=%lld\n",p,kmin,kmax,tests,fails);
}
