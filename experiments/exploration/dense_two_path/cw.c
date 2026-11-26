// Closed-walk search for the two-path lemma. Labels S = I_M \ T. Walk from 0 in [0,M] using each label once.
// Phase 1 (P): vertices distinct. Switch at y>0. Phase 2 (Q reversed): vertices distinct among phase-2 vertices
// (y counted), 0 only as the final vertex. Node cap -> inconclusive.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
int M,k,T[64],lab[128],nl; long long nodes,cap; uint64_t vP,vQ; int usedl[128];
int order[128];
int dfs(int at,int phase,int left){
  if(++nodes>cap) return -1;
  if(left==0) return at==0 && phase==2;
  if(phase==1 && at>0){ // option: switch here
    uint64_t sv=vQ; vQ|=1ULL<<at; int r=dfs(at,2,left); vQ=sv; if(r) return r; }
  for(int ii=0;ii<nl;ii++){ int i=order[ii]; if(usedl[i]) continue; int w=at+lab[i]; if(w<0||w>M) continue;
    if(phase==1){ if(w==0||(vP>>w&1)) continue; usedl[i]=1; vP|=1ULL<<w; int r=dfs(w,1,left-1); vP&=~(1ULL<<w); usedl[i]=0; if(r) return r; }
    else { if(w==0){ if(left!=1) continue; } else if(vQ>>w&1) continue;
      usedl[i]=1; if(w) vQ|=1ULL<<w; int r=dfs(w,2,left-1); if(w) vQ&=~(1ULL<<w); usedl[i]=0; if(r) return r; } }
  return 0;
}
int cmp(const void*a,const void*b){return abs(lab[*(int*)b])-abs(lab[*(int*)a]);}
int test(){ int inT[256]={0}; for(int i=0;i<k;i++) inT[T[i]+128]=1; nl=0;
  for(int v=-M;v<=M;v++) if(v&&!inT[v+128]) lab[nl++]=v;
  for(int i=0;i<nl;i++) order[i]=i; qsort(order,nl,sizeof(int),cmp);
  // randomize ties lightly
  memset(usedl,0,sizeof usedl); vP=1; vQ=0; nodes=0; return dfs(0,1,nl); }
int main(int c,char**v){ k=atoi(v[1]); M=atoi(v[2]); int N=atoi(v[3]); srand(atoi(v[4])); cap=atoll(v[5]);
  long long ok=0,fl=0,inc=0;
  for(int it=0;it<N;){ int used[256]={0},s=0;
    for(int i=0;i<k-1;i++){int a; do{a=rand()%(2*M+1)-M;}while(a==0||used[a+128]); used[a+128]=1; T[i]=a; s+=a;}
    int last=-s; if(!last||abs(last)>M||used[last+128]) continue; T[k-1]=last;
    int mx=0; for(int i=0;i<k;i++) if(abs(T[i])>mx) mx=abs(T[i]); if(mx!=M) continue;
    it++; int r=test(); if(r==1) ok++; else { if(r==0) fl++; else inc++;
      printf("%s M=%d k=%d T=",r==0?"FAIL":"INCONCL",M,k); for(int i=0;i<k;i++) printf("%d ",T[i]); puts(""); fflush(stdout);} }
  printf("k=%d M=%d samples=%d ok=%lld fail=%lld inconclusive=%lld\n",k,M,N,ok,fl,inc);
}
