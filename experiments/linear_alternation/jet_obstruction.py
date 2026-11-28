import sympy
t=sympy.symbols('t')
def E(i): return sum(t**j for j in range(i+1))
for s in (6,7,8,9):
    P=E(s)**2*(E(s-2)*E(s)-E(s-1)**2)
    closed=-t**(s-1)*(1-t**(s+1))**2/(1-t)**2
    ok=sympy.simplify(P-closed)==0
    def coef(expr,k): return sympy.series(expr,t,0,k+1).removeO().coeff(t,k)
    j1=-coef((1+t)**3*(1-t**(s+1))**2/(1-t),s+1)
    j2=-coef((1+t)**2*(1-t**(s+1))**2/(1-t),s)
    print(f"s={s}: P(E) closed form ok: {ok};  J_(n-1)(dg2) = {j1};  J_(n-2)(dg3) = {j2};  delta a = {-(j1)+ (j2)} (report: 6-4=2 via signs eps_2=+1? )")
