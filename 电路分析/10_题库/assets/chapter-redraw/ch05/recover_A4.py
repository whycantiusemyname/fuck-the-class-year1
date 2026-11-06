"""Redraw A4 with the source's genuinely blank left supply value left blank."""
from pathlib import Path
import sys,json
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent))
import common as M
from common import Circuit as C
M.OUT=HERE;start=len(M.records)
c=C('F008','A4 unlabelled supply',size=(9,7))
c.part('B',(0,0),(0,4),reverse=True);c.wire((0,4),(0,7),(2,7));c.part('D',(2,7),(7,7),'$D_1$',reverse=True)
c.wire((2,0),(2,5));c.part('D',(2,5),(7,5),'$D_2$',reverse=True);c.wire((7,7),(7,5));c.dot((7,5))
c.part('R',(7,5),(7,2),r'$1\,\mathrm{k}\Omega$');c.part('B',(7,0),(7,2),r'$3\,\mathrm{V}$',reverse=True,offset=.7)
c.wire((0,0),(9,0));c.wire((7,7),(9,7));c.port((9,7),'$+$','right');c.port((9,0),'$-$','right');c.text(10,3.5,'$u_o$')
c.save(note='Left supply polarity is visible; no voltage value is printed on the original A4. No value has been inferred from similar courseware examples.')
(HERE/'A4-geometry.json').write_bytes((json.dumps(M.records[start:],ensure_ascii=False,indent=2)+'\n').encode())
