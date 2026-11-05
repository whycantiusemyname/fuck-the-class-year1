"""Assemble B19 panels and render the actual SVGs for visual review.
Run render.py first. Requires Pillow and PyMuPDF in addition to render.py's dependencies.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import fitz,xml.etree.ElementTree as ET

O=Path(__file__).resolve().parent
KEYS=['B19','B20','B21','C2','C5','C9','C12','C13','C14','C15']
ET.register_namespace('','http://www.w3.org/2000/svg')
ET.register_namespace('xlink','http://www.w3.org/1999/xlink')
ns='{http://www.w3.org/2000/svg}'
roots=[ET.parse(O/f'B19-{x}.svg').getroot() for x in ['a','b']]
dims=[list(map(float,r.attrib['viewBox'].split())) for r in roots]
w=max(x[2] for x in dims);h=max(x[3] for x in dims)
root=ET.Element(ns+'svg',{'width':f'{w}pt','height':f'{(h+28)*2}pt','viewBox':f'0 0 {w} {(h+28)*2}','version':'1.1'})
ET.SubElement(root,ns+'rect',{'width':'100%','height':'100%','fill':'white'})
for i,r in enumerate(roots):
 # Matplotlib IDs repeat across standalone figures; namespace all fragment references.
 oldids=[e.attrib['id'] for e in r.iter() if 'id' in e.attrib]
 raw=ET.tostring(r,encoding='unicode')
 for name in sorted(oldids,key=len,reverse=True):
  raw=raw.replace('id="'+name+'"','id="panel'+str(i)+'_'+name+'"').replace('#'+name+'"','#panel'+str(i)+'_'+name+'"').replace('#'+name+')','#panel'+str(i)+'_'+name+')')
 sub=ET.fromstring(raw)
 group=ET.SubElement(root,ns+'g',{'transform':f'translate(0,{i*(h+28)})'})
 for child in list(sub):group.append(child)
 text=ET.SubElement(root,ns+'text',{'x':str(w/2),'y':str(i*(h+28)+h+17),'text-anchor':'middle','font-family':'STIXGeneral','font-size':'14'});text.text='(a)' if i==0 else '(b)'
ET.ElementTree(root).write(O/'B19.svg',encoding='utf-8',xml_declaration=True)
svg=O/'B19.svg';svg.write_bytes(('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n').encode('utf-8'))
# Use MuPDF to independently render SVG instead of relying solely on the plot backend.
for key in KEYS:
 svg=fitz.open(O/f'{key}.svg');pdf=fitz.open('pdf',svg.convert_to_pdf());p=pdf[0]
 p.get_pixmap(matrix=fitz.Matrix(2,2)).save(O/f'{key}-svg-render.png')
 if key=='B19':p.get_pixmap(matrix=fitz.Matrix(3,3)).save(O/'B19.png')
 im=Image.open(O/f'{key}-svg-render.png').convert('RGB');im.resize((640,round(im.height*640/im.width)),Image.Resampling.LANCZOS).save(O/f'{key}-small.png')
 im.convert('L').resize((320,round(im.height*320/im.width)),Image.Resampling.LANCZOS).save(O/f'{key}-320px.png')
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
for i in range(0,10,2):
 sheet=Image.new('RGB',(1440,1080),'#efefef');draw=ImageDraw.Draw(sheet)
 for j,k in enumerate(KEYS[i:i+2]):
  y=j*540;draw.text((20,y+10),k+'：原生扫描提取 → SVG实际渲染',fill='#111111',font=font)
  for col,name in enumerate([k+'-source-native.png',k+'-svg-render.png']):
   im=Image.open(O/name).convert('RGB');im.thumbnail((690,475),Image.Resampling.LANCZOS);sheet.paste(im,(col*720+(720-im.width)//2,y+55+(475-im.height)//2))
 sheet.save(O/f'comparison-{i//2+1:02}.png')
sheet=Image.new('RGB',(1280,5*465),'white');draw=ImageDraw.Draw(sheet)
for i,k in enumerate(KEYS):
 x=(i%2)*640;y=(i//2)*465;draw.text((x+10,y+5),k,fill='black',font=font)
 im=Image.open(O/f'{k}-small.png');im.thumbnail((640,430),Image.Resampling.LANCZOS);sheet.paste(im,(x+(640-im.width)//2,y+30))
sheet.save(O/'small-reading.png')
sheet=Image.new('RGB',(960,1840),'white');draw=ImageDraw.Draw(sheet)
for i,k in enumerate(KEYS[1:]+['B19']):
 x=(i%3)*320;y=(i//3)*420
 draw.text((x+10,y+5),k,fill='black',font=font)
 im=Image.open(O/f'{k}-320px.png');sheet.paste(im,(x,y+30))
sheet.save(O/'reading-320px.png')
print('10 plates assembled; actual SVG and 640px views rendered')
