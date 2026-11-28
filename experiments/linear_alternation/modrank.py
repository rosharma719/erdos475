P=1000003
def rank_mod(rows):
    rows=[dict(r) for r in rows if r]; piv={}; rk=0
    for r in rows:
        r={k:v%P for k,v in r.items() if v%P}
        while r:
            k=min(r)
            if k in piv:
                pr=piv[k]; f=r[k]
                for kk,vv in pr.items(): r[kk]=(r.get(kk,0)-f*vv)%P
                r={a:b for a,b in r.items() if b}
            else:
                inv=pow(r[k],P-2,P); r={a:b*inv%P for a,b in r.items()}; piv[k]=r; rk+=1; break
    return rk
