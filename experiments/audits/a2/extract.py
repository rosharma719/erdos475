import re,ast,sys
src=open(sys.argv[1]).read()
i=src.index('CERTIFICATES = {');j=src.index('def verify_geometry')
d=ast.literal_eval(src[i+len('CERTIFICATES = '):j].strip())
print(len(d))
import json;json.dump({k:v['path'] for k,v in d.items()},open('a2/certs.json','w'))
