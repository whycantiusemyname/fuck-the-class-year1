"""Assemble vector panels without rasterization; normalize SVG IDs and whitespace."""
from pathlib import Path
import xml.etree.ElementTree as ET
ET.register_namespace('','http://www.w3.org/2000/svg');ET.register_namespace('xlink','http://www.w3.org/1999/xlink')
NS='{http://www.w3.org/2000/svg}'
def combine(out,key,parts,labels=None):
 roots=[ET.parse(out/(x+'.svg')).getroot() for x in parts]
 sizes=[list(map(float,r.attrib['viewBox'].split()))[2:] for r in roots]
 width=max(s[0] for s in sizes);height=sum(s[1]+24 for s in sizes)
 root=ET.Element(NS+'svg',{'width':f'{width}pt','height':f'{height}pt','viewBox':f'0 0 {width} {height}'})
 ET.SubElement(root,NS+'rect',{'width':'100%','height':'100%','fill':'white'});y=0
 for i,(r,(w,h)) in enumerate(zip(roots,sizes)):
  prefix='p'+str(i)+'_';raw=ET.tostring(r,encoding='unicode')
  for ident in sorted([e.attrib['id'] for e in r.iter() if 'id' in e.attrib],key=len,reverse=True):raw=raw.replace('id="'+ident+'"','id="'+prefix+ident+'"').replace('#'+ident+'"','#'+prefix+ident+'"').replace('#'+ident+')','#'+prefix+ident+')')
  g=ET.SubElement(root,NS+'g',{'transform':f'translate({(width-w)/2},{y})'})
  for child in list(ET.fromstring(raw)):g.append(child)
  if labels:
   t=ET.SubElement(root,NS+'text',{'x':str(width/2),'y':str(y+h+15),'font-size':'14','font-family':'STIXGeneral','text-anchor':'middle'});t.text=labels[i]
  y+=h+24
 p=out/(key+'.svg');ET.ElementTree(root).write(p,encoding='utf-8',xml_declaration=True)
 p.write_bytes(('\n'.join(x.rstrip() for x in p.read_text(encoding='utf-8').splitlines())+'\n').encode())
