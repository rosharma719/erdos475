import sys
sys.argv=[sys.argv[0],'2','4']
exec(open('halfwalk.py').read().split("for spread in")[0])
for M in range(6,13):
    for a in (2,3,(M+1)//2 - (1 if M%2 else 0)):
        if a<2 or 2*a==M+1: continue
        D=find(M,a,M+2)
        print(M,a,flush=True,end=" ");print("spread M+2:",D if D else None, [D[i+1]-D[i] for i in range(len(D)-1)] if D else "")
