#include <algorithm>
#include <cstdio>
using namespace std;
int p,x,a[20],b[20],L[20],R[20],m;long long tests,bad;bool printed;
bool place(unsigned left,int at,unsigned seen){
 if(!left)return at==0;
 for(unsigned s=left;s;s&=s-1){
  int i=__builtin_ctz(s),v=(at+L[i])%p,w=v;
  if(R[i]){if(seen>>v&1)continue;w=(v+R[i])%p;}
  if(w==x||((seen>>w&1)&&!(w==0&&left==(1u<<i))))continue;
  unsigned vis=seen|(1u<<v)|(1u<<w);
  if(place(left^(1u<<i),w,vis))return true;
 }return false;
}
void gen(unsigned rem,unsigned forbid,int k){
 if(!rem){
  ++tests;if(place((1u<<k)-1,1,3u|(1u<<x)))return;
  for(int j=0;j<k;j++)if(R[j])swap(L[j],R[j]);
  bool ok=place((1u<<k)-1,1,3u|(1u<<x));
  for(int j=0;j<k;j++)if(R[j])swap(L[j],R[j]);
  if(ok)return;
  ++bad;if(!printed){printf("p=%d x=%d blocks",p,x);for(int i=0;i<k;i++)printf(" (%d,%d)",L[i],R[i]);puts("");printed=true;}
  return;
 }
 int u=__builtin_ctz(rem); rem^=1u<<u;
 L[k]=u;R[k]=0;gen(rem,forbid,k+1);
 for(unsigned z=rem;z;z&=z-1){int v=__builtin_ctz(z),s=(u+v)%p;if(forbid>>s&1)continue;
 for(int r=0;r<2;r++){L[k]=r?v:u;R[k]=r?u:v;gen(rem^(1u<<v),forbid|(1u<<s),k+1);}
 }
}
int main(){for(int q:{2,3,5,7,11,13,17,19}){p=q;bad=tests=0;printed=false;
 for(unsigned B=2;B<(1u<<p);B+=4){int sum=0;for(unsigned z=B;z;z&=z-1)sum+=__builtin_ctz(z);
 if(sum%p)continue;
 for(x=2;x<p;x++){int y=(1-x+p)%p;if(y==x||((B>>x|B>>y)&1))continue;
 gen(B^2,B|1u|(1u<<x)|(1u<<y),0);}
 }printf("%d %lld %lld\n",p,tests,bad);fflush(stdout);}}
