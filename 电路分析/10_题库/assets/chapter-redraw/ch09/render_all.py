"""Rebuild all 20 main-agent chapter 9 figures and their geometry ledger."""
from pathlib import Path
import subprocess,sys,json
HERE=Path(__file__).resolve().parent
for name in ['generate.py','generate_ic.py','generate_remaining.py']:subprocess.run([sys.executable,str(HERE/name)],check=True)
load=lambda name:json.loads((HERE/name).read_text(encoding='utf8'))
rows=load('geometry.json')+load('ic-geometry.json')+load('remaining-geometry.json')
(HERE/'geometry.json').write_bytes((json.dumps(rows,ensure_ascii=False,indent=2)+'\n').encode())
qa={}
for name in ['qa-partial.json','qa-ic.json','qa-remaining.json']:qa.update({k:v for k,v in load(name).items() if '-' not in k})
(HERE/'qa.json').write_bytes((json.dumps({'verified':qa,'pending':{}},ensure_ascii=False,indent=2)+'\n').encode())
assert len(qa)==20,len(qa)
print(len(qa),'figures rendered')
