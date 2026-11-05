"""Recreate adopted PDF crops at native resolution. Originals must be available.
Uses mapping.json; never writes source PDFs or original image assets.
Dependencies: PyMuPDF (fitz), Pillow.
"""
from pathlib import Path
import json,io
import fitz
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def extract(record):
 pdf=fitz.open(ROOT/record['source_pdf']);page=pdf[record['pdf_page']-1]
 b=record['bbox_1000'];r=fitz.Rect(b[0]*page.rect.width/1000,b[1]*page.rect.height/1000,b[2]*page.rect.width/1000,b[3]*page.rect.height/1000)
 images=page.get_images(full=True)
 if record['extraction']=='native_scan_crop':
  assert len(images)==1
  raw=Image.open(io.BytesIO(pdf.extract_image(images[0][0])['image'])).convert('RGB');ir=page.get_image_rects(images[0][0])[0]
  box=tuple(round(v) for v in ((r.x0-ir.x0)/ir.width*raw.width,(r.y0-ir.y0)/ir.height*raw.height,(r.x1-ir.x0)/ir.width*raw.width,(r.y1-ir.y0)/ir.height*raw.height))
  image=raw.crop(box)
 else:image=Image.open(io.BytesIO(page.get_pixmap(matrix=fitz.Matrix(4,4),clip=r).tobytes('png'))).convert('RGB')
 dst=ROOT/record['new_path'];assert dst.parent==HERE
 image.save(dst);pdf.close()
if __name__=='__main__':
 records=json.loads((HERE/'mapping.json').read_text(encoding='utf-8'))
 for r in records:
  if r['method']=='native_extraction':extract(r)
 print('Adopted PDF crops recreated')
