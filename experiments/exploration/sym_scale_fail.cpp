// Scalable test: is a random zero-sum A (size k) a contraction of a symmetric walk W_S with S ⊆ classes(λA) for some dilation λ?
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <random>
using namespace std;
int p,K; vector<char> inA; vector<int> V; int n; long long nodes;
vector<int> walk(const vector<int>&S){ int m=S.size(); vector<int> d; for(int i=1;i<m;i++) d.push_back((i%2==1?1:-1)*S[i]);
  vector<int> w=d; w.push_back(S[0]); for(int i=(int)d.size()-1;i>=0;i--) w.push_back(-d[i]); w.push_back(-S[0]); return w; }
bool dfs(int i,int cnt,unsigned long long lab,int first,int last){ if(++nodes>200000) return false;
  if(cnt==K){ int d=((first-last)%p+p)%p; return d && !(lab>>(d-1)&1) && inA[d]; }
  for(int j=i;j<n;j++){ int d=((V[j]-last)%p+p)%p; if(d==0||!inA[d]||(lab>>(d-1)&1)) continue; if(n-j-1<K-cnt-1) break; if(dfs(j+1,cnt+1,lab|(1ULL<<(d-1)),first,V[j])) return true; } return false; }
int main(int argc,char**argv){ p=atoi(argv[1]); K=atoi(argv[2]); int ns=atoi(argv[3]); unsigned seed=atoi(argv[4]); mt19937_64 rng(seed); int cov=0,tested=0;
  while(tested<ns){ vector<int> pool(p-1); for(int i=0;i<p-1;i++) pool[i]=i+1; shuffle(pool.begin(),pool.end(),rng); vector<int> A(pool.begin(),pool.begin()+K); int sum=0; for(int x:A) sum+=x; if(sum%p) continue; tested++;
    bool found=false; 
    for(int a=1;a<p&&!found;a++){ inA.assign(p,0); vector<int> cls; for(int x:A){ int y=x*a%p; inA[y]=1; int c=min(y,p-y); cls.push_back(c);} sort(cls.begin(),cls.end()); cls.erase(unique(cls.begin(),cls.end()),cls.end()); int c=cls.size();
      for(unsigned mask=1; mask<(1u<<c) && !found; mask++){ int m=__builtin_popcount(mask); if(m<(K+1)/2) continue; vector<int> S; for(int i=c-1;i>=0;i--) if(mask>>i&1) S.push_back(cls[i]);
        vector<int> w=walk(S); n=w.size(); if(n<K) continue; V.assign(n,0); int s=0; for(int i=0;i<n;i++){ V[i]=((s%p)+p)%p; s+=w[i]; }
        for(int f=0; f<=n-K && !found; f++){ nodes=0; if(dfs(f+1,1,0,V[f],V[f])) found=true; } } }
    cov+=found; if(!found){ printf("FAIL:"); for(int x:A) printf(" %d",x); printf("\n"); } }
  printf("p=%d k=%d: sampled %d zero-sum sets, representable with S ⊆ classes(λA): %d (%.1f%%)\n",p,K,tested,cov,100.0*cov/tested); }
