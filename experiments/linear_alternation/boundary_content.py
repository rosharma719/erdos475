import sys, itertools, math
sys.argv=[sys.argv[0]]
from content_lib import content
m=int(__import__('os').environ.get('M','10'))
g,vals=content(m)
print(f"m={m}: boundary-packet content = {g}; nonzero values {sum(1 for x in vals if x)}/{len(vals)}",flush=True)
