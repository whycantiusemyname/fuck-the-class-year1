"""Portable verification: python verify_batch.py in either source or share workspace."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET,importlib.util
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=json.loads((HERE/'mapping.json').read_text(encoding='utf-8'))
report=ROOT/'40_派生视图/大物上/图像重绘批01/validation.json'
record=json.loads(report.read_text(encoding='utf-8'))
spec=importlib.util.spec_from_file_location('batch_generate',HERE/'generate.py')
generator=importlib.util.module_from_spec(spec);spec.loader.exec_module(generator)
generator.scientific_checks()
assert len(rows)==8
for r in rows:
    assert sha(ROOT/r['path'])==r['sha256'],r['path']
    assert sha(ROOT/r['new_svg'])==record['assets'][r['new_svg']],r['new_svg']
    ET.parse(ROOT/r['new_svg']);Image.open(ROOT/r['new_png']).verify()
for doc,expected in record['prior_documents_normalized_sha256'].items():
    text=(ROOT/doc).read_text(encoding='utf-8')
    for r in rows:
        if r['document'].replace('\\','/')!=doc:continue
        old='物理/'+r['path'];new='物理/'+r['new_svg']
        assert text.count(new)==1,(doc,new)
        text=text.replace(new,old)
    assert hashlib.sha256(text.encode()).hexdigest()==expected,('non-image edit',doc)
print('PASS: 8 original hashes, 8 SVG hashes/XML, 8 PNGs, curve/geometry constraints; 3 documents contain only 8 reference replacements')
