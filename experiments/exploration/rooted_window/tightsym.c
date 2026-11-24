// Tight family (M,a,b=M+1-a): find valid cycle of +-S, S=[1,M]\{b}, starting +a, vertices in [-M+1, M].
// Lift: prepend +(M+1), -b  => tight-family cycle with vertices in (-M, M+1], range <= 2M (IRC).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int M,a,b,ne,el[128],lo,hi; char vis[512]; long long nodes,cap; int path[128];
int dfs(int pos,int cnt,unsigned char*used){
  if(++nodes>cap) return -1;
  if(cnt==ne) return pos==0;
  // heuristic: try steps that move toward the opposite side, large magnitudes first
  int order[128],k=0;
  for(int i=0;i<ne;i++) if(!used[i]) order[k++]=i;
  for(int t=0;t<k;t++){ int i=order[t]; int w=pos+el[i];
    if(cnt==ne-1){ if(w==0){path[cnt]=el[i];return 1;} continue;}
    if(w<lo||w>hi||vis[w+256]) continue;
    vis[w+256]=1; used[i]=1; path[cnt]=el[i];
    int r=dfs(w,cnt+1,used); vis[w+256]=0; used[i]=0; if(r) return r; }
  return 0;
}
int main(int argc,char**argv){
  int Mmax=atoi(argv[1]); cap=atoll(argv[2]);
  for(M=4;M<=Mmax;M++) for(a=2;a<=M/2;a++){ b=M+1-a;
    ne=0; el[ne++]=a;
    // order: alternate big positive/negative magnitudes (descending)
    for(int x=M;x>=1;x--){ if(x==b) continue; if(x!=a) el[ne++]=x; el[ne++]=-x; }
    lo=-M+1; hi=M; memset(vis,0,sizeof vis); vis[256]=1; vis[a+256]=1;
    unsigned char used[128]={0}; used[0]=1; path[0]=a; nodes=0;
    int r=dfs(a,1,used);
    printf("M=%d a=%d: %s nodes=%lld",M,a,r==1?"FOUND":r==0?"NONE":"UNDET",nodes);
    if(r==1){ printf("  walk:"); for(int i=0;i<ne;i++) printf(" %d",path[i]); }
    printf("\n"); fflush(stdout);
  }
}
