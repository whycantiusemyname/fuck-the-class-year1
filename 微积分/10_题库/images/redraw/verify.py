from pathlib import Path
import json,re,hashlib,xml.etree.ElementTree as ET
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
ASSET=Path(__file__).resolve().parent
rows=json.loads((ASSET/'mapping.json').read_text(encoding='utf-8'))
for r in rows:
    assert hashlib.sha256((ROOT/r['original']).read_bytes()).hexdigest()==r['original_sha256']
    svg=ROOT/r['svg'];assert ET.parse(svg).getroot().tag.endswith('svg')
    assert (ROOT/r['png']).is_file()
    assert (ROOT/r['document']).read_text(encoding='utf-8').count('images/redraw/'+svg.name)==1
t=np.linspace(0,2*np.pi,10001);x=1+np.cos(t);y=np.sin(t);z=2*np.sin(t/2)
assert np.max(np.abs(x*x+y*y+z*z-4))<1e-12
assert np.max(np.abs((x-1)**2+y*y-1))<1e-12
assert np.all(z>=0)
# In the observer's yz plane, signed area is positive for the requested CCW traversal.
assert np.trapezoid(y*np.gradient(z,t)-z*np.gradient(y,t),t)>0
refs=[]
for directory in ['10_题库','20_知识']:
    for p in (ROOT/directory).rglob('*.md'):
        refs += [(p,m) for m in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf-8'))]
assert len(refs)==4,len(refs)
assert sum('/redraw/' in m for p,m in refs)==3
print('PASS: 3 SVG geometries/references; 4 total image references including retained QR code')
