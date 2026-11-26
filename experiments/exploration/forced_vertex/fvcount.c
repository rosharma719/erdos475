// min over (B,t=1,x) of #FV orderings (start t, distinct vertices, avoid x); x ranges over all admissible (x!=0,1, 2x!=1)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int p,n,m,lab[16]; long long cnt[64];
void dfs(int used,int at,unsigned long long seen){
  if(used==(1<<m)-1){ for(int x=0;x<p;x++) if(!(seen>>x&1)) cnt[x]++; return;}
  int full=(1<<m)-1;
  for(int i=0;i<m;i++) if(!(used>>i&1)){
    int v=(at+lab[i])%p;
    if(used==(full^(1<<i))){ if(v==0) dfs(used|1<<i,v,seen); continue;}
    if(seen>>v&1) continue;
    dfs(used|1<<i,v,seen|(1ULL<<v));
  }
}
int cur[16]; long long best=-1; int bestB[16],bestx; long long nsets=0;
void rec(int start,int k,int sum){
  if(k==n-2){ int last=(p-(1+sum)%p)%p; if(last<=(k?cur[k-1]:1)||last<2) return; cur[k]=last; m=n-1;
    for(int i=0;i<m;i++) lab[i]=cur[i];
    // skip symmetric sets? keep all
    memset(cnt,0,sizeof cnt); nsets++;
    dfs(0,1,3ULL);
    for(int x=2;x<p;x++){ if((2*x)%p==1) continue; if(best<0||cnt[x]<best){best=cnt[x];bestx=x;for(int i=0;i<m;i++)bestB[i]=lab[i];}}
    return;}
  for(int a=start;a<p;a++){cur[k]=a;rec(a+1,k+1,(sum+a)%p);}
}
int main(int c,char**v){p=atoi(v[1]);n=atoi(v[2]);rec(2,0,0);
  printf("p=%d n=%d sets=%lld minFV=%lld at B={1",p,n,nsets,best);for(int i=0;i<n-1;i++)printf(",%d",bestB[i]);printf("} x=%d\n",bestx);}
