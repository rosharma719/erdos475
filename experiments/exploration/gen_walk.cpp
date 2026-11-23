// Generalised symmetric walks: delta = any signed ordering of S\{M} whose prefix sums T_j (j=0..m-1) are distinct with max-min <= M-1.
// Walk (delta, M, -delta^rev, -M) is a valid cycle (vertices T u (M+T)).  For each target A (from stdin, p k a1..ak) search random generalised walks
// and label-matching contractions (kept vertices' consecutive differences == A, up to dilation).  Reports covered / not.
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <random>
#include <algorithm>
using namespace std;
int p,r,K; vector<char> inA; vector<int> V; int n; long long nodes; mt19937_64 rng(99);
bool dfs(int i,int cnt,unsigned long long lab,int first,int last){ if(++nodes>300000) return false;
  if(cnt==K){ int d=((first-last)%p+p)%p; return d && !(lab>>(d-1)&1) && inA[d]; }
  for(int j=i;j<n;j++){ int d=((V[j]-last)%p+p)%p; if(d==0||!inA[d]||(lab>>(d-1)&1)) continue; if(n-j-1<K-cnt-1) break; if(dfs(j+1,cnt+1,lab|(1ULL<<(d-1)),first,V[j])) return true; } return false; }
// random generalised delta for S (M=max): DFS over orders/signs with prefix window
bool gen_delta(vector<int>&rest,int M,vector<int>&delta,int tries){
  int m=rest.size(); for(int t=0;t<tries;t++){ vector<int> ord=rest; shuffle(ord.begin(),ord.end(),rng); vector<int> T(1,0); delta.clear(); int mn=0,mx=0; bool ok=true;
    for(int x:ord){ int sg=(rng()&1)?1:-1; int ns=T.back()+sg*x; bool bad=false; for(int q:T) if(q==ns) bad=true; int nmn=min(mn,ns),nmx=max(mx,ns); if(bad||nmx-nmn>M-1){ ns=T.back()-sg*x; bad=false; for(int q:T) if(q==ns) bad=true; nmn=min(mn,ns),nmx=max(mx,ns); if(bad||nmx-nmn>M-1){ok=false;break;} sg=-sg; }
      T.push_back(ns); delta.push_back(sg*x); mn=nmn; mx=nmx; }
    if(ok) return true; } return false; }
int main(int argc,char**argv){ p=atoi(argv[1]); r=(p-1)/2; int walks=atoi(argv[2]); int total=0,cov=0;
  while(true){ int kk; if(scanf("%d",&kk)!=1) break; vector<int> A(kk); for(int i=0;i<kk;i++) scanf("%d",&A[i]); K=kk; total++; bool found=false;
    for(int a=1;a<p&&!found;a++){ inA.assign(p,0); for(int x:A) inA[x*a%p]=1;
      for(int w=0; w<walks && !found; w++){ int m=(K+1)/2 + rng()%(unsigned)max(1,min(r-(K+1)/2+1,K/2+3)); vector<int> pool(r); for(int i=0;i<r;i++) pool[i]=i+1; shuffle(pool.begin(),pool.end(),rng); vector<int> S(pool.begin(),pool.begin()+m); sort(S.rbegin(),S.rend()); int M=S[0]; vector<int> rest(S.begin()+1,S.end()); vector<int> delta; if(!gen_delta(rest,M,delta,20)) continue;
        vector<int> wk=delta; wk.push_back(M); for(int i=(int)delta.size()-1;i>=0;i--) wk.push_back(-delta[i]); wk.push_back(-M); n=wk.size(); V.assign(n,0); int s=0; for(int i=0;i<n;i++){ V[i]=((s%p)+p)%p; s+=wk[i]; }
        if(n<K) continue; for(int f=0; f<=n-K && !found; f++){ nodes=0; if(dfs(f+1,1,0,V[f],V[f])) found=true; } } }
    cov+=found; if(!found){ printf("NOT FOUND:"); for(int x:A) printf(" %d",x); printf("\n"); fflush(stdout);} }
  printf("p=%d: targets %d, covered by generalised symmetric walks %d\n",p,total,cov); }
