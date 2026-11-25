// Usage: fv_fixed_size P N [W w]  (optional: only first-label a with a%W==w, for parallel runs)
// FV at fixed prime p and size n, normalized t=1: for each zero-sum B (|B|=n, 1 in B, 0 notin B),
// compute K = intersection of vertex sets over all valid orderings starting with 1;
// FV fails iff K contains x not in {0,1,(p+1)/2}. Vertex sets as 128-bit masks (p<128).
#include <stdio.h>
#include <stdlib.h>
typedef unsigned __int128 u128;
int p,n,lab[16],m; u128 K; int found;
void dfs(int used,int at,u128 seen){
  if(used==(1<<m)-1){ K&=seen; found=1; return;}
  for(int i=0;i<m;i++) if(!(used>>i&1)){
    int v=(at+lab[i])%p;
    if(used==(((1<<m)-1)^(1<<i))){ if(v!=0) continue; dfs(used|1<<i,v,seen); continue;}
    if(seen>>v&1) continue;
    u128 ns=seen|((u128)1<<v);
    if((ns&K)==K && 0){} 
    dfs(used|1<<i,v,ns);
    if(K==(((u128)1)|((u128)1<<1))) return; // K already minimal {0,1}
  }
}
int cur[16]; long long sets=0,bad=0;
void rec(int start,int k,int sum){
  if(k==n-2){ int last=(p-(1+sum)%p)%p; if(last<=cur[k-1]||last<2) return;
    cur[k]=last; m=n-1; for(int i=0;i<m;i++) lab[i]=cur[i];
    sets++; K=~(u128)0; found=0;
    dfs(0,1,((u128)1)|((u128)1<<1));
    if(!found){ printf("NO VALID ORDERING p=%d B={1",p); for(int i=0;i<m;i++)printf(",%d",lab[i]); puts("}"); bad++; return;}
    u128 Kx=K & ~(((u128)1)|((u128)1<<1)|((u128)1<<((p+1)/2)));
    if(Kx){ bad++; printf("FV FAIL p=%d B={1",p); for(int i=0;i<m;i++)printf(",%d",lab[i]); printf("} forced:");
      for(int v=0;v<p;v++) if(Kx>>v&1) printf(" %d",v); puts(""); }
    return; }
  for(int a=start;a<p;a++){ cur[k]=a; rec(a+1,k+1,(sum+a)%p); }
}
int W=1,w=0;
int main(int c,char**v){ p=atoi(v[1]); n=atoi(v[2]); if(c>4){W=atoi(v[3]);w=atoi(v[4]);}
  for(int a=2;a<p;a++) if(a%W==w){cur[0]=a; rec(a+1,1,a%p);}
  printf("p=%d n=%d sets=%lld failures=%lld\n",p,n,sets,bad); }
