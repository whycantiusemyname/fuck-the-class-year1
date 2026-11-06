"""C3 recovered from the uncropped original photo. The blank resistor stays blank."""
from pathlib import Path
import sys,json
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent))
import common as M
from common import Circuit as C,E
M.OUT=HERE
first_record=len(M.records)
c=C('F017','C3 original-photo recovery',size=(16,10))
n1,p1,o1=c.op(4,7,label='A_1')
c.part('R',(0,n1.y),(3,n1.y),'$R$');c.ground((0,n1.y));c.wire((3,n1.y),n1);c.wire((3,n1.y),(3,10))
c.part('R',(3,10),(10,10))
c.wire((10,10),(10,7),o1);c.dot((3,n1.y));c.dot((10,7))
c.part('R',(10,7),(15,7),'$R_0$');c.wire((15,7),(18,7));c.part('R',(18,7),(18,3.5),'$R_L$');c.ground((18,3.5))
c.d.add(E.Arrow().at((15.4,7.6)).to((17.3,7.6)));c.text(16.35,8.15,r'$i_o^{\prime}$')
c.port((0,p1.y),'$u_i$');c.part('R',(0,p1.y),(3,p1.y),'$R$');c.wire((3,p1.y),p1);c.dot((3,p1.y))
c.wire((3,p1.y),(3,4));c.part('R',(3,4),(3,1.5),'$R$')
n2,p2,o2=c.op(7.4,1.5,label='A_2',reverse=True)
c.wire((3,1.5),o2);c.text(3,.8,'$u_{o2}$');c.dot((3,1.5))
c.wire(n2,(11,n2.y),(11,3.5),(7,3.5),(7,1.5),o2);c.dot((7,1.5))
c.wire((15,7),(16.5,7),(16.5,p2.y),p2);c.dot((15,7));c.dot((18,7))
c.text(n1.x-.5,n1.y+.4,'$N_1$',size=14);c.text(p1.x-.5,p1.y+.4,'$P_1$',size=14)
c.text(n2.x+.4,n2.y+.3,'$N_2$',size=14);c.text(p2.x+.4,p2.y-.4,'$P_2$',size=14)
c.save(note='Uncropped photo 16139e9cc73fa00690f9250ca6bcd131.jpg; top feedback resistor deliberately unlabelled; question condition remains pending.')
(HERE/'C3-geometry.json').write_bytes((json.dumps(M.records[first_record:],ensure_ascii=False,indent=2)+'\n').encode())
