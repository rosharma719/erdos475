// Coverage of zero-sum sets by contractions of symmetric walks, SAMPLED for larger p. got = bitset over label masks (2^(p-1) bits).
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <random>
#include <algorithm>
using namespace std; typedef unsigned long long U64;
int p,r;
vector<int> walk(const vector<int>&S){ int m=S.size(); vector<int> d; for(int i=1;i<m;i++) d.push_back((i%2==1?1:-1)*S[i]);
  vector<int> w=d; w.push_back(S[0]); for(int i=(int)d.size()-1;i>=0;i--) w.push_back(-d[i]); w.push_back(-S[0]); return w; }
int main(int argc,char**argv){ p=atoi(argv[1]); r=(p-1)/2; int mmax=atoi(argv[2]); int nsamp=atoi(argv[3]);
  vector<U64> got(((1ULL<<(p-1))+63)/64,0);
  long long patterns=0;
  for(unsigned mask=1; mask<(1u<<r); mask++){ int m=__builtin_popcount(mask); if(m>mmax) continue; vector<int> S; for(int i=r;i>=1;i--) if(mask>>(i-1)&1) S.push_back(i);
    vector<int> w=walk(S); int n=w.size(); vector<int> V(n); int s=0; for(int i=0;i<n;i++){ V[i]=((s%p)+p)%p; s+=w[i]; }
    for(unsigned long long sub=15; sub<(1ULL<<n); sub++){ int cnt=__builtin_popcountll(sub); if(cnt<5) continue; patterns++;
      int first=-1, prev=-1; unsigned lab=0; bool ok=true;
      for(int i=0;i<n;i++) if(sub>>i&1){ if(prev>=0){ int d=((V[i]-prev)%p+p)%p; if(d==0||(lab>>(d-1)&1)){ok=false;break;} lab|=1u<<(d-1);} else first=V[i]; prev=V[i]; }
      if(!ok) continue; int d=((first-prev)%p+p)%p; if(d==0||(lab>>(d-1)&1)) continue; lab|=1u<<(d-1); got[lab>>6]|=1ULL<<(lab&63); } }
  mt19937_64 rng(5); printf("p=%d, |S|<=%d (patterns %lld). Sampled coverage of zero-sum sets by size:\n",p,mmax,patterns);
  for(int k=6;k<=p-8;k+=1){ int tested=0,cov=0; int tries=0;
    while(tested<nsamp && tries<nsamp*400){ tries++; vector<int> A; vector<int> pool(p-1); for(int i=0;i<p-1;i++) pool[i]=i+1; shuffle(pool.begin(),pool.end(),rng); A.assign(pool.begin(),pool.begin()+k); int sum=0; for(int x:A) sum+=x; if(sum%p) continue; tested++;
      bool c=false; for(int a=1;a<p&&!c;a++){ unsigned B=0; for(int x:A) B|=1u<<(((long long)x*a%p)-1); if(got[B>>6]>>(B&63)&1) c=true; } cov+=c; }
    if(tested) printf("  |A|=%2d: sampled %4d zero-sum sets, covered %4d (%.1f%%)\n",k,tested,cov,100.0*cov/tested); fflush(stdout); } }
