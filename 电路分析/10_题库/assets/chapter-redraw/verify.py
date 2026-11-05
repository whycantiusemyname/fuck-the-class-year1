"""Portable per-chapter verifier; python verify.py ch05."""
from pathlib import Path
import sys,json,hashlib,re,os,xml.etree.ElementTree as ET
from PIL import Image
A=Path(__file__).resolve().parent;R=A.parents[2];O=A/sys.argv[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
data=json.loads((O/'ledger.json').read_text(encoding='utf-8'));n=0
for row in data['figures']:
 assert sha(R/row['original'])==row['sha256'],row['id']
 if row['status']!='verified':continue
 p=O/(row['id']+'.svg');assert sha(p)==row['svg_sha256'];root=ET.parse(p).getroot()
 ids=[e.attrib['id'] for e in root.iter() if 'id' in e.attrib];assert len(ids)==len(set(ids))
 for e in root.iter():
  assert not e.tag.endswith('image'),('raster embedded',p)
  for attr,v in e.attrib.items():
   if attr.endswith('href') and v.startswith('#'):assert v[1:] in ids
 Image.open(O/(row['id']+'.png')).verify()
 for ref in row['references']:
  text=(R/ref['document']).read_text(encoding='utf-8-sig');assert row['new_target'] in text or os.path.relpath(O/(row['id']+'.svg'),(R/ref['document']).parent).replace('\\','/') in text
 n+=1
for doc,expected in data['document_invariants'].items():
 t=(R/doc).read_text(encoding='utf-8-sig')
 for row in data['figures']:
  if row['status']=='verified':
   for replacement in row.get('replacements',[]):
    if replacement['document']==doc:t=t.replace(replacement['new'],replacement['old'])
 assert hashlib.sha256(t.encode()).hexdigest()==expected,('non-image document change',doc)
print(f'PASS {sys.argv[1]}: {n} SVG/PNG pairs; original hashes; IDs; exact document reverse replacement')
