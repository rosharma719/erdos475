// Usage: fv_fixed_size P N [W w]  (p <= 256; optional: only first label a with a%W==w)
// FV at fixed prime p (any p <= 256) and size n, t=1 normalized. Bitsets of 4 x u64.
// Usage: fvw P N [W w]: only first label a with a%W==w.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef struct { uint64_t w[4]; } bs;
static inline int has(const bs*s,int v){return s->w[v>>6]>>(v&63)&1;}
static inline void setb(bs*s,int v){s->w[v>>6]|=1ULL<<(v&63);}
static inline void clrb(bs*s,int v){s->w[v>>6]&=~(1ULL<<(v&63));}
int p,n,lab[16],m; bs K,seen,MIN; int found;
static int eq(const bs*a,const bs*b){for(int i=0;i<4;i++) if(a->w[i]!=b->w[i]) return 0; return 1;}
void dfs(int used,int at){
  int full=(1<<m)-1;
  if(used==full){ for(int i=0;i<4;i++) K.w[i]&=seen.w[i]; found=1; return;}
  for(int i=0;i<m;i++) if(!(used>>i&1)){
    int v=(at+lab[i])%p;
    if(used==(full^(1<<i))){ if(v==0) dfs(used|1<<i,v); continue;}
    if(has(&seen,v)) continue;
    setb(&seen,v); dfs(used|1<<i,v); clrb(&seen,v);
    if(eq(&K,&MIN)) return;
  }
}
int cur[16]; long long sets=0,bad=0;
void rec(int start,int k,int sum){
  if(k==n-2){ int last=(p-(1+sum)%p)%p; if(last<=cur[k-1]||last<2) return;
    cur[k]=last; m=n-1; for(int i=0;i<m;i++) lab[i]=cur[i];
    sets++; for(int i=0;i<4;i++){K.w[i]=~0ULL;seen.w[i]=0;} found=0; setb(&seen,0); setb(&seen,1);
    dfs(0,1);
    if(!found){ printf("NO VALID ORDERING p=%d B={1",p); for(int i=0;i<m;i++)printf(",%d",lab[i]); puts("}"); fflush(stdout); bad++; return;}
    clrb(&K,0); clrb(&K,1); clrb(&K,(p+1)/2);
    for(int v=p;v<256;v++) clrb(&K,v);
    int any=0; for(int i=0;i<4;i++) if(K.w[i]) any=1;
    if(any){ bad++; printf("FV FAIL p=%d B={1",p); for(int i=0;i<m;i++)printf(",%d",lab[i]); printf("} forced:");
      for(int v=0;v<p;v++) if(has(&K,v)) printf(" %d",v); puts(""); fflush(stdout);}
    return; }
  for(int a=start;a<p;a++){ cur[k]=a; rec(a+1,k+1,(sum+a)%p); }
}
int main(int c,char**v){ p=atoi(v[1]); n=atoi(v[2]); int W=1,w=0; if(c>4){W=atoi(v[3]);w=atoi(v[4]);}
  for(int i=0;i<4;i++)MIN.w[i]=0; setb(&MIN,0); setb(&MIN,1);
  for(int a=2;a<p;a++) if(a%W==w){cur[0]=a; rec(a+1,1,a%p);}
  printf("p=%d n=%d sets=%lld failures=%lld\n",p,n,sets,bad); }
