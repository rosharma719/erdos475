"""Fraction of (random) valid complementary cycles that admit four-block fusion, A=F_p^x, per atom class."""
import random,sys
from itertools import combinations
sys.argv=['x']; 
exec(open('audit_sfcx.py').read().split('# (2)')[0].replace('print(','(lambda *a,**k:None)('))
def minimal(B): return sum(B)%p==0 and all(sum(T)%p for r in range(1,len(B)) for T in combinations(B,r))
exec(open('audit_sfcx.py').read().split('def rand_cycle')[1].join(['def rand_cycle','']) if False else '')
from audit_sfcx import rand_cycle  # noqa
