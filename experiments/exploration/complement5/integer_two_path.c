// Integer two-path lemma IT(k): T = zero-sum set of k nonzero integers, M = max|t|.
// S = {±1..±M} \ T. Need simple paths P, Q in [0,M], both from 0 to the same vertex E>0,
// steps(P) ⊔ (−steps(Q)) = S  (Q read backwards gives labels −q).
// Encoding: label v in S -> bit index (v>0 ? v-1 : M + (-v) - 1).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
int M,k,T[16]; int inS[64]; // index by v+M
typedef struct{uint64_t key;} K; K *buf; long long nb,cap;
static inline int bit(int v){return v>0? v-1 : M+(-v)-1;}
void push(uint64_t key){ if(nb==cap){cap=cap?cap*2:1<<20; buf=realloc(buf,cap*sizeof(K));} buf[nb++].key=key; }
int cmpk(const void*a,const void*b){uint64_t x=((K*)a)->key,y=((K*)b)->key; return x<y?-1:x>y;}
int vis[64];
// enumerate paths from 0 using steps sign*S (sign=+1 for P, -1 for Q); record (E,mask of S-labels used)
int mode; uint64_t full; int found;
int has(uint64_t key){ long long lo=0,hi=nb-1; while(lo<=hi){long long m=(lo+hi)/2; if(buf[m].key==key) return 1; if(buf[m].key<key) lo=m+1; else hi=m-1;} return 0;}
void dfs(int at, uint64_t mask){
  if(at>0){ uint64_t key=((uint64_t)at<<48)|mask;
    if(mode==0) push(key); else { uint64_t need=full&~mask; if(has(((uint64_t)at<<48)|need)){found=1;return;} } }
  for(int v=-M; v<=M; v++){ if(!v||!inS[v+M]) continue; int b=bit(v); if(mask>>b&1) continue;
    int step = mode==0? v : -v; int w=at+step; if(w<0||w>M||vis[w]) continue;
    vis[w]=1; dfs(w,mask|(1ULL<<b)); vis[w]=0; if(found) return; }
}
int test(){
  for(int i=0;i<2*M+1;i++) inS[i]=1; inS[M]=0; for(int i=0;i<k;i++) inS[T[i]+M]=0;
  full=0; for(int v=-M;v<=M;v++) if(v&&inS[v+M]) full|=1ULL<<bit(v);
  nb=0; found=0; memset(vis,0,sizeof vis); vis[0]=1; mode=0; dfs(0,0);
  qsort(buf,nb,sizeof(K),cmpk);
  memset(vis,0,sizeof vis); vis[0]=1; mode=1; found=0; dfs(0,0);
  return found;
}
long long tot=0,bad=0;
int cur[16];
void rec(int idx,int start,int sum){
  if(idx==k-1){ int last=-sum; if(last<=cur[idx-1]||last==0||last<-M||last>M) return;
    // last must be > previous (sorted) ; require max |.| == M
    cur[idx]=last; int mx=0; for(int i=0;i<k;i++){int a=abs(cur[i]); if(a>mx) mx=a;} if(mx!=M) return;
    // distinct and no zero already ensured; T may contain ± pairs
    for(int i=0;i<k;i++) T[i]=cur[i];
    tot++; if(!test()){ bad++; printf("FAIL M=%d T=",M); for(int i=0;i<k;i++) printf("%d ",T[i]); puts(""); fflush(stdout);} return; }
  for(int a=start;a<=M;a++){ if(!a) continue; cur[idx]=a; rec(idx+1,a+1,sum+a); }
}
int main(int c,char**v){ k=atoi(v[1]); int M0=atoi(v[2]), M1=atoi(v[3]);
  for(M=M0;M<=M1;M++){ long long t0=tot,b0=bad; rec(0,-M,0); printf("k=%d M=%d sets=%lld fails=%lld\n",k,M,tot-t0,bad-b0); fflush(stdout);} }
