"""Source-bound redraw of the formally referenced chapter-3 simulation circuit."""
from pathlib import Path
import sys,json
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import common as M
from common import Circuit as C,E
M.OUT=HERE
c=C('F001','simulation 1',size=(10,7))
c.part('AC',(0,0),(0,6),offset=-.8)
c.text(-.25,3.55,'$+$');c.text(-.25,2.45,'$-$')
c.text(.9,4,'$V_1$',ha='left');c.text(.9,3.25,r'$2\,\mathrm{V_{rms}}$',ha='left');c.text(.9,2.5,r'$1000\,\mathrm{Hz}$',ha='left');c.text(.9,1.75,r'$0^\circ$',ha='left')
c.wire((0,6),(3,6));c.part('R',(3,6),(7,6),'$R_1$');c.text(5,5.35,r'$50\,\Omega$')
c.wire((7,6),(10,6));c.part('C',(10,6),(10,0));c.text(10.5,3.5,'$C_1$',ha='left');c.text(10.5,2.8,r'$1.023\,\mu\mathrm{F}$',ha='left');c.wire((10,0),(0,0));c.ground((5,0))
c.text(1.8,6.35,'$1$');c.text(8,6.35,'$2$');c.text(5.3,.35,'$0$')
for x,y,l in [(1.1,7.1,'A'),(2.5,7.1,'V')]:
 c.ax.add_patch(M.plt.matplotlib.patches.Circle((x,y),.3,fill=False,lw=1.3,color='black'));c.text(x,y,l,size=14);c.d.add(E.Arrow().at((x,y-.3)).to((x,6.02)))
c.text(3.3,7.1,r'$\mathrm{PR1}$',ha='left');c.save()
(HERE/'geometry.json').write_bytes((json.dumps(M.records,ensure_ascii=False,indent=2)+'\n').encode())
