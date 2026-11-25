// Coverage of zero-sum 5-hole sets H (A = F_p^x \ H) by 5-vertex contractions of cycles B_alpha,
// alpha a graceful permutation of [1..r] (distinct |differences| 1..r-1), B=(delta, r, -delta^rev, -r).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int p,r,n; int alpha[64],used[64],dused[64]; int lab[128];
unsigned char *covered; // index by canonical orbit key
int inv[256];
static long long keyof(int *h){ // canonical under dilation: min over lambda of sorted tuple encoded
  long long best=-1;
  for(int l=1;l<p;l++){ int t[5]; for(int i=0;i<5;i++) t[i]=(h[i]*l)%p;
    for(int i=1;i<5;i++){int x=t[i],j=i-1; while(j>=0&&t[j]>x){t[j+1]=t[j];j--;} t[j+1]=x;}
    long long k=0; for(int i=0;i<5;i++) k=k*p+t[i]; if(best<0||k<best) best=k;}
  return best;
}
int randgrace(int i){ // fill alpha[i..r-1]
  if(i==r) return 1;
  int cand[64],c=0; for(int v=1;v<=r;v++) if(!used[v]){int d=abs(v-alpha[i-1]); if(!dused[d]) cand[c++]=v;}
  for(int k=c-1;k>0;k--){int j=rand()%(k+1);int t=cand[k];cand[k]=cand[j];cand[j]=t;}
  for(int k=0;k<c;k++){int v=cand[k],d=abs(v-alpha[i-1]); used[v]=dused[d]=1; alpha[i]=v; if(randgrace(i+1)) return 1; used[v]=dused[d]=0;}
  return 0;
}
int main(int argc,char**argv){ p=atoi(argv[1]); int N=atoi(argv[2]); srand(atoi(argv[3])); r=(p-1)/2; n=2*r;
  long long K=1; for(int i=0;i<5;i++) K*=p; covered=calloc(K,1);
  // count orbits of zero-sum 5-sets: mark all as 2 (exists), covered=1
  unsigned char *exists=calloc(K,1); long long norb=0, norb_inv=0;
  int h[5];
  for(h[0]=1;h[0]<p;h[0]++)for(h[1]=h[0]+1;h[1]<p;h[1]++)for(h[2]=h[1]+1;h[2]<p;h[2]++)for(h[3]=h[2]+1;h[3]<p;h[3]++){
    int s=(p*4-(h[0]+h[1]+h[2]+h[3]))%p; if(s<=h[3]) continue; h[4]=s;
    long long k=keyof(h); if(!exists[k]){exists[k]=1+ 0; norb++;
      int pairfree=1; for(int i=0;i<5;i++)for(int j=i+1;j<5;j++) if((h[i]+h[j])%p==0) pairfree=0;
      if(pairfree){exists[k]=2;norb_inv++;} } }
  long long ncov=0,ncov_inv=0;
  for(int it=0;it<N;it++){
    memset(used,0,sizeof used); memset(dused,0,sizeof dused);
    alpha[0]=1+rand()%r; used[alpha[0]]=1; if(!randgrace(1)){it--;continue;}
    // labels
    int m=0; for(int i=0;i<r-1;i++) lab[m++]=(alpha[i+1]-alpha[i]+p)%p; lab[m++]=r;
    for(int i=r-2;i>=0;i--) lab[m++]=(p-(alpha[i+1]-alpha[i]+p)%p)%p; lab[m++]=p-r;
    // vertex j (0..n-1) sits between lab[j-1] and lab[j] (cyclic). delete 5 vertices.
    int d[5];
    for(d[0]=0;d[0]<n;d[0]++)for(d[1]=d[0]+1;d[1]<n;d[1]++)for(d[2]=d[1]+1;d[2]<n;d[2]++)for(d[3]=d[2]+1;d[3]<n;d[3]++)for(d[4]=d[3]+1;d[4]<n;d[4]++){
      // new labels: merge across deleted vertices
      static int cnt[256]; static int stamp[256]; static int st=0; st++;
      int del[128]={0}; for(int i=0;i<5;i++) del[d[i]]=1;
      // find a non-deleted start vertex
      int s0=-1; for(int j=0;j<n;j++) if(!del[j]){s0=j;break;}
      int okset=1; int acc=0; int nl=0;
      for(int k=0;k<n;k++){ int j=(s0+k)%n; acc=(acc+lab[j])%p; int nv=(j+1)%n; if(!del[nv]){ if(acc==0||(stamp[acc]==st)){okset=0;break;} stamp[acc]=st; nl++; acc=0;} }
      if(!okset) continue;
      int hh[5],c=0; for(int v=1;v<p;v++) if(stamp[v]!=st){ if(c<5) hh[c]=v; c++; }
      if(c!=5) continue;
      long long k=keyof(hh); if(covered[k]) continue; covered[k]=1; ncov++; if(exists[k]==2) ncov_inv++;
    }
  }
  printf("p=%d cycles=%d orbits=%lld covered=%lld | inverse-free orbits=%lld covered=%lld\n",p,N,norb,ncov,norb_inv,ncov_inv);
}
