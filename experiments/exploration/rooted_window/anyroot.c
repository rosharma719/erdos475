// G(P,N,r): valid cycle starting with +r, vertices in (-maxN, maxP]. Test all r in P, all instances (no maxP>=maxN restriction).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int el[64],ne,lo,hi; char vis[512];
int dfs(int pos,int cnt,unsigned long long used){
  if(cnt==ne) return pos==0;
  for(int i=0;i<ne;i++){ if(used>>i&1) continue; int w=pos+el[i];
    if(cnt==ne-1){ if(w==0) return 1; continue;}
    if(w<lo||w>hi||vis[w+256]) continue; vis[w+256]=1; int r=dfs(w,cnt+1,used|1ULL<<i); vis[w+256]=0; if(r) return 1; }
  return 0;
}
int main(int argc,char**argv){
  int V=atoi(argv[1]),MAXE=atoi(argv[2]); long long tot=0,inst=0,bad=0,badmax=0; int shown=0;
  for(int P=1;P<(1<<V);P++) for(int N=1;N<(1<<V);N++){
    int sp=0,sn=0,p1=0,q1=0,c=0;
    for(int x=1;x<=V;x++){ if(P>>(x-1)&1){sp+=x;c++;p1=x;} if(N>>(x-1)&1){sn+=x;c++;q1=x;} }
    if(sp!=sn||c>MAXE) continue; inst++;
    for(int r=1;r<=V;r++){ if(!(P>>(r-1)&1)) continue;
      ne=0; el[ne++]=r; for(int x=1;x<=V;x++){ if((P>>(x-1)&1)&&x!=r) el[ne++]=x; if(N>>(x-1)&1) el[ne++]=-x; }
      lo=-q1+1; hi=p1; memset(vis,0,sizeof vis); vis[256]=1;
      int ok; if(r>hi){ok=0;} else if(ne==1) ok=0; else { vis[r+256]=1; ok=dfs(r,1,1ULL);} 
      tot++; if(!ok){ bad++; if(r==p1) badmax++; if(shown<100000){shown++; printf("fail r=%d P={",r); for(int x=1;x<=V;x++) if(P>>(x-1)&1) printf("%d,",x); printf("} N={"); for(int x=1;x<=V;x++) if(N>>(x-1)&1) printf("%d,",x); printf("}\n");} }
    }
  }
  printf("V=%d instances=%lld roots=%lld fail=%lld fail_at_max=%lld\n",V,inst,tot,bad,badmax);
}
