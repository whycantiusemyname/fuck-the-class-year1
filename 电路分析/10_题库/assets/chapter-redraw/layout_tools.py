"""Measure rendered label clearance; explicit reviewed adjustments live per chapter.

Bounding-box warnings are review candidates, not proof of an electrical error.
This module never changes wires, components, or label content automatically.
"""
import json, os
from pathlib import Path
from matplotlib.transforms import Bbox

def prepare(c, directory):
    p=Path(directory)/'layout-fixes.json'
    rules=json.loads(p.read_text(encoding='utf8')).get(c.key,[]) if p.exists() else []
    for rule in rules:
        hits=[i for i,v in enumerate(c.labels) if v[2]==rule['text'] and abs(v[0]-rule['from'][0])<1e-5 and abs(v[1]-rule['from'][1])<1e-5]
        assert len(hits)==1,(c.key,rule,hits)
        i=hits[0]; x,y,s,ha,va,size=c.labels[i]
        c.labels[i]=(rule['to'][0],rule['to'][1],s,rule.get('ha',ha),rule.get('va',va),rule.get('size',size))

def measure(c, directory):
    c.fig.canvas.draw()
    renderer=c.fig.canvas.get_renderer()
    texts=[t for t in c.ax.texts if t.get_visible() and t.get_text().strip()]
    boxes=[t.get_window_extent(renderer) for t in texts]
    paths=[]
    for artist in [*c.ax.lines,*c.ax.patches]:
        if artist.get_visible():
            paths.append(artist.get_path().transformed(artist.get_transform()))
    warnings=[]
    for i,(t,b) in enumerate(zip(texts,boxes)):
        # Leave a small safety margin without counting the font's empty fringe.
        inner=Bbox.from_extents(b.x0+1.5,b.y0+2,b.x1-1.5,b.y1-2)
        if any(p.intersects_bbox(inner,filled=False) for p in paths):
            warnings.append({'type':'text/stroke','text':t.get_text(),'at':list(t.get_position())})
        for j in range(i):
            other=boxes[j]
            overlap=Bbox.intersection(inner,other)
            if overlap is not None and overlap.width>1 and overlap.height>2:
                warnings.append({'type':'text/text','text':t.get_text(),'other':texts[j].get_text(),'at':list(t.get_position())})
    result={'id':c.key,'warnings':warnings,'label_count':len(texts)}
    dest=os.environ.get('FTC_LAYOUT_AUDIT_DIR')
    if dest:
        p=Path(dest)/Path(directory).name;p.mkdir(parents=True,exist_ok=True)
        (p/(c.key+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return result
