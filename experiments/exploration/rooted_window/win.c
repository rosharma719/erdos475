// H(P,N): with p1=maxP >= q1=maxN, exists valid cycle starting with +p1, all vertices in (-q1, p1].
// Also records instances where H fails, and whether the "lift" applies (exists y in N, y < p1-p2).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int MAXE=12;
int V, el[64], ne, lo, hi; char vis[256]; long long nodes;
int dfs(int pos,int usedmask_dummy,int cnt,unsigned long long used){
  if(++nodes>20000000) return -1;
  if(cnt==ne) return pos==0;
  for(int i=0;i<ne;i++){ if(used>>i&1) continue;
    int w=pos+el[i];
    if(cnt==ne-1){ if(w==0) return 1; continue; }
    if(w<lo||w>hi||vis[w+128]) continue;
    vis[w+128]=1; int r=dfs(w,0,cnt+1,used|1ULL<<i); vis[w+128]=0;
    if(r) return r;
  }
  return 0;
}
int main(int argc,char**argv){
  V=atoi(argv[1]); if(argc>2) MAXE=atoi(argv[2]); long long tot=0,fail=0,und=0,liftable=0;
  for(int P=1;P<(1<<V);P++) for(int N=1;N<(1<<V);N++){
    int sp=0,sn=0,p1=0,p2=0,q1=0,cp=0,cn=0;
    for(int x=1;x<=V;x++){ if(P>>(x-1)&1){sp+=x;cp++; p2=p1; p1=x;} if(N>>(x-1)&1){sn+=x;cn++;q1=x;} }
    if(sp!=sn||p1<q1) continue;
    if(cp+cn>MAXE) continue;
    ne=0; el[ne++]=p1; for(int x=1;x<=V;x++){ if((P>>(x-1)&1)&&x!=p1) el[ne++]=x; if(N>>(x-1)&1) el[ne++]=-x; }
    lo=-q1+1; hi=p1; memset(vis,0,sizeof vis); vis[128]=1;
    // first step forced: +p1
    int pos=p1; vis[pos+128]=1; nodes=0;
    int r = (ne==1)?0: dfs(pos,0,1,1ULL);
    tot++;
    int lift=0; for(int y=1;y<=V;y++) if((N>>(y-1)&1) && y<p1-p2) lift=1;
    if(r==0){ fail++; if(fail<=25){ printf("FAIL P={"); for(int x=1;x<=V;x++) if(P>>(x-1)&1) printf("%d,",x); printf("} N={"); for(int x=1;x<=V;x++) if(N>>(x-1)&1) printf("%d,",x); printf("} lift=%d\n",lift);} }
    if(r<0) und++;
    if(lift) liftable++;
  }
  printf("V=%d instances=%lld H-fail=%lld undetermined=%lld liftable=%lld\n",V,tot,fail,und,liftable);
}
