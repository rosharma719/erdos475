// FV over Z: all zero-sum sets of distinct nonzero integers in [-K,K], size n; every t in B; every x not in {0,t}, 2x!=t.
// Compute forced vertices K = intersection over valid t-rooted orderings (distinct partial sums s0..s_{n-1}); report failures.
#include <stdio.h>
#include <stdlib.h>
#define OFF 200
int K,n,el[20],lab[20],m; static unsigned char seen[400]; static int inter[400],nval; int found;
int vs[20];
void dfs(int used,int at,int depth){
  int full=(1<<m)-1;
  if(used==full){ found=1; // vertices vs[0..depth-1]
    static int mark[400]; static int stamp=0; stamp++;
    for(int i=0;i<depth;i++) mark[vs[i]+OFF]=stamp;
    for(int v=0;v<400;v++) if(inter[v] && mark[v]!=stamp) inter[v]=0;
    return;}
  for(int i=0;i<m;i++) if(!(used>>i&1)){
    int v=at+lab[i];
    if(used==(full^(1<<i))){ if(v==0) dfs(used|1<<i,v,depth); continue;}
    if(seen[v+OFF]) continue;
    seen[v+OFF]=1; vs[depth]=v; dfs(used|1<<i,v,depth+1); seen[v+OFF]=0;
  }
}
long long sets=0,fails=0;
void test(){
  for(int ti=0;ti<n;ti++){ int t=el[ti]; m=0; for(int i=0;i<n;i++) if(i!=ti) lab[m++]=el[i];
    for(int v=0;v<400;v++) inter[v]=1; found=0;
    seen[OFF]=1; seen[t+OFF]=1; vs[0]=0; vs[1]=t;
    dfs(0,t,2);
    seen[OFF]=0; seen[t+OFF]=0;
    if(!found){ printf("NO ORDERING B="); for(int i=0;i<n;i++)printf("%d ",el[i]); printf("t=%d\n",t); fails++; continue;}
    for(int v=0;v<400;v++) if(inter[v]){ int x=v-OFF; if(x==0||x==t||2*x==t) continue;
      printf("FAIL B="); for(int i=0;i<n;i++)printf("%d ",el[i]); printf(" t=%d x=%d\n",t,x); fails++; }
  }
}
void rec(int start,int k,int sum){
  if(k==n){ if(sum==0){sets++;test();} return;}
  for(int a=start;a<=K;a++){ if(a==0) continue; el[k]=a; rec(a+1,k+1,sum+a);}
}
int main(int c,char**v){K=atoi(v[1]);n=atoi(v[2]);rec(-K,0,0);printf("K=%d n=%d sets=%lld failures=%lld\n",K,n,sets,fails);}
