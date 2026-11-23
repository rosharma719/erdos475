// Which zero-sum sets A (up to dilation) arise as the step-label set of a vertex-deletion (contraction) of the symmetric walk W_S, S any subset of [1..r]?
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <unordered_set>
#include <algorithm>
using namespace std; typedef unsigned int U;
int p,r;
vector<int> walk(const vector<int>&S){ // S sorted descending
  int m=S.size(); vector<int> d; for(int i=1;i<m;i++) d.push_back((i%2==1?1:-1)*S[i]);
  vector<int> w=d; w.push_back(S[0]); for(int i=(int)d.size()-1;i>=0;i--) w.push_back(-d[i]); w.push_back(-S[0]); return w; }
int main(int argc,char**argv){ p=atoi(argv[1]); r=(p-1)/2; int mmax=argc>2?atoi(argv[2]):r;
  unordered_set<U> got; got.reserve(1<<24);
  for(int mask=1; mask<(1<<r); mask++){ int m=__builtin_popcount(mask); if(m>mmax) continue; vector<int> S; for(int i=r;i>=1;i--) if(mask>>(i-1)&1) S.push_back(i);
    vector<int> w=walk(S); int n=w.size(); vector<int> V(n); int s=0; for(int i=0;i<n;i++){ V[i]=((s%p)+p)%p; s+=w[i]; }
    for(unsigned long long sub=7; sub<(1ULL<<n); sub++){ int cnt=__builtin_popcountll(sub); if(cnt<4) continue; // keep >=4 vertices
      int first=-1, prev=-1; U lab=0; bool ok=true;
      for(int i=0;i<n && ok;i++) if(sub>>i&1){ if(prev>=0){ int d=((V[i]-prev)%p+p)%p; if(d==0||(lab>>(d-1)&1)){ok=false;break;} lab|=1u<<(d-1);} else first=V[i]; prev=V[i]; }
      if(!ok) continue; int d=((first-prev)%p+p)%p; if(d==0||(lab>>(d-1)&1)) continue; lab|=1u<<(d-1); got.insert(lab); } }
  // coverage of zero-sum orbits
  long long orb[40]={0}, cov[40]={0}; 
  for(U A=1; A<(1u<<(p-1)); A++){ int k=__builtin_popcount(A); if(k<4||k>p-6) continue; int sum=0; for(int i=0;i<p-1;i++) if(A>>i&1) sum+=i+1; if(sum%p) continue;
    // canonical: A must be minimal among dilates
    bool canon=true; bool covered=false;
    for(int a=1;a<p;a++){ U B=0; for(int i=0;i<p-1;i++) if(A>>i&1) B|=1u<<(((i+1)*a%p)-1); if(a>1&&B<A) {canon=false;break;} if(got.count(B)) covered=true; }
    if(!canon) continue; orb[k]++; if(covered) cov[k]++; }
  printf("p=%d: distinct label sets from symmetric-walk contractions: %zu\n",p,got.size());
  long long to=0,tc=0; for(int k=4;k<=p-6;k++) if(orb[k]){ printf("  |A|=%2d: zero-sum orbits %6lld, covered %6lld (%.1f%%)\n",k,orb[k],cov[k],100.0*cov[k]/orb[k]); to+=orb[k]; tc+=cov[k]; }
  printf("  total orbits %lld covered %lld (%.1f%%)\n",to,tc,100.0*tc/to); }
