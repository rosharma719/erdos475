// Find a representation of a given zero-sum A (or a dilate) as a contraction of a symmetric walk; print S, kept vertices, labels per block.
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <random>
using namespace std;
int p,r; vector<int> A; vector<char> inA; 
vector<int> walk(const vector<int>&S){ int m=S.size(); vector<int> d; for(int i=1;i<m;i++) d.push_back((i%2==1?1:-1)*S[i]);
  vector<int> w=d; w.push_back(S[0]); for(int i=(int)d.size()-1;i>=0;i--) w.push_back(-d[i]); w.push_back(-S[0]); return w; }
int n; vector<int> V; vector<int> chosen; long long nodes;
bool dfs(int i,int cnt,unsigned lab,int first,int last){ // choose next kept index > last
  if(++nodes>20000000) return false;
  if(cnt==(int)A.size()){ int d=((first-last)%p+p)%p; return d && !(lab>>(d-1)&1) && inA[d]; }
  for(int j=i;j<n;j++){ int d=((V[j]-last)%p+p)%p; if(d==0||!inA[d]||(lab>>(d-1)&1)) continue; // label must lie in A and be new
    // remaining vertices must suffice
    if(n-j-1 < (int)A.size()-cnt-1) break;
    chosen.push_back(j); if(dfs(j+1,cnt+1,lab|(1u<<(d-1)),first,V[j])) return true; chosen.pop_back(); }
  return false; }
int main(int argc,char**argv){ p=atoi(argv[1]); r=(p-1)/2; int k=argc-2; A.clear(); for(int i=0;i<k;i++) A.push_back(atoi(argv[2+i]));
  for(int a=1;a<p;a++){ inA.assign(p,0); vector<int> B; for(int x:A){ int y=x*a%p; inA[y]=1; B.push_back(y);} 
    for(int m=(k+1)/2; m<=r; m++){ // try all S of size m (descending)
      vector<int> idx(m); for(int i=0;i<m;i++) idx[i]=i+1; 
      while(true){ vector<int> S(idx.rbegin(),idx.rend()); vector<int> w=walk(S); n=w.size(); V.assign(n,0); int s=0; for(int i=0;i<n;i++){ V[i]=((s%p)+p)%p; s+=w[i]; }
        if(n>=k){ for(int f=0; f<=n-k; f++){ chosen.clear(); chosen.push_back(f); nodes=0; if(dfs(f+1,1,0,V[f],V[f])){ 
              printf("dilation %d: A'=",a); for(int x:B) printf("%d ",x); printf("\n S="); for(int x:S) printf("%d ",x); printf("\n steps="); for(int x:w) printf("%d ",x); printf("\n kept idx="); for(int c:chosen) printf("%d ",c); printf("\n"); return 0; } } }
        int i=m-1; while(i>=0 && idx[i]==r-(m-1-i)) i--; if(i<0) break; idx[i]++; for(int j=i+1;j<m;j++) idx[j]=idx[j-1]+1; } } }
  printf("no representation found\n"); }
