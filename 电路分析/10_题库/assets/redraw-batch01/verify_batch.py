"""Verify portable assets, original hashes, and question anchors in either workspace."""
from pathlib import Path
import hashlib,json,re,xml.etree.ElementTree as ET
from PIL import Image
O=Path(__file__).resolve().parent;R=O.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=json.loads((O/'ledger.json').read_text(encoding='utf-8'))
assert ledger['verified_count']==10 and len(ledger['records'])==10
assert sha(R/ledger['source_pdf'])==ledger['source_pdf_sha256']
q=(R/'10_题库/电子线路期末复习_题面整理.md').read_text(encoding='utf-8')
headings=re.findall(r'(?m)^### (.+)$',q)
for row in ledger['records']:
 k=row['id'];assert sha(R/row['original'])==row['original_sha256'],k
 assert row['question'] in headings and headings.count(row['question'])==1,k
 assert q.count(f'(assets/redraw-batch01/{k}.svg)')==1,k
 for field in ['svg','png']:
  p=O/row[field];assert sha(p)==row[field+'_sha256'],str(p)
  if field=='png':Image.open(p).verify()
  else:
   root=ET.parse(p).getroot();ids=[e.attrib['id'] for e in root.iter() if 'id' in e.attrib]
   assert len(ids)==len(set(ids)),('duplicate SVG IDs',k)
   for e in root.iter():
    for attr,value in e.attrib.items():
     if attr.endswith('href') and value.startswith('#'):assert value[1:] in ids,(k,value)
   assert not any(e.tag.endswith('image') for e in root.iter()),('raster SVG',k)
 for source in row['editable_sources']:assert (O/source).is_file()
for k in ['A4','A7','C3']:
 block=q.split('### 电子复习-'+k+'\n',1)[1].split('\n### ',1)[0]
 assert f'![原扫描题图：保留待确认](assets/电子线路期末复习/{k}.png)' in block
 assert not re.search(r'!\[.*\]\(assets/电子线路期末复习/redrawn/',block)
print('PASS: 10 vector plates + PNG, editable sources, original/source hashes, SVG IDs, 10 anchors/references; 3 uncertain originals retained')
