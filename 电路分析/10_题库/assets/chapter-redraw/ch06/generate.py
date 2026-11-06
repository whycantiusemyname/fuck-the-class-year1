"""Chapter 6 source-faithful vector circuit redraws; layout coordinates are not physical dimensions."""
from pathlib import Path
import sys,json,math
from types import SimpleNamespace
from schemdraw.util import Point
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent))
import common as M
from panels import combine
import fitz
M.OUT=HERE;E=M.E
class C(M.Circuit):
 def port(self,p,label=None,side='left'):
  if label=='$-$' and side=='right':
   super().port(p,None,side);self.text(p[0]+.18,p[1]+.3,label,ha='left')
  else:super().port(p,label,side)
def bjt(c,x,y,label='T',pnp=False,flip=False):
 elm=E.BjtPnp() if pnp else E.BjtNpn()
 if pnp != flip:elm.flip()  # Normalize both transistor families to collector-up unless flip=True.
 t=c.d.add(elm.at((x,y)).anchor('base'))
 if label:c.text(t.center.x+.5,t.center.y,'$'+label+'$',ha='left')
 return t
def cap(c,a,b,label=None,plus=None):
 c.part('C',a,b,'$'+label+'$' if label else None)
 if plus:
  # Place a + close to the designated terminal, clear of the label above the plates.
  x=(a[0]+b[0])/2;y=(a[1]+b[1])/2
  if abs(a[1]-b[1])<.01:c.text(x+(-.3 if plus=='a' else .3),y-.35,'$+$',size=14)
  else:c.text(x-.35,y+(.3 if plus=='a' else -.3),'$+$',size=14)
def output(c,a,x=14,caplabel='C_2',load=True):
 cap(c,a,(x,a[1]),caplabel,'a');c.port((x,a[1]),'$+$','right');c.port((x,0),'$-$','right')
 if load:c.part('R',(x,a[1]),(x,0),'$R_L$');c.dot((x,a[1]));c.dot((x,0))
 c.text(x+1.8,a[1]/2,'$u_o$',ha='left');return x
def supply(c,left=3,right=9,top=9,label='+U_{CC}'):
 c.wire((left,top),(right,top));c.supply((right,top),'$'+label+'$')
def emitter(c,t,label='R_E',bypass=False,split=False):
 p=(t.emitter.x,3.5);c.wire(t.emitter,p)
 if split:
  c.part('R',p,(p[0],2),'$R_E^{\prime}$',offset=-.5);p=(p[0],2)
 c.part('R',p,(p[0],0),'$'+label+'$',offset=-.5)
 if bypass:
  x=p[0]+2;c.wire(p,(x,p[1]));cap(c,(x,p[1]),(x,0),'C_E','a');c.dot(p);c.dot((x,0))
 return p
def input(c,t,xnode=3,source=False):
 cap(c,(0,t.base.y),(xnode,t.base.y),'C_1','b');c.wire((xnode,t.base.y),t.base)
 c.port((0,0),'$-$');c.text(-.7,t.base.y/2,'$u_i$',ha='right')
 if source:
  c.part('R',(0,t.base.y),(0,2),'$R_S$',offset=-.5);c.part('V',(0,0),(0,2),'$u_s$',offset=-.8)
 else:c.port((0,t.base.y),'$+$')
 return (xnode,t.base.y)

# Device terminals and given voltages only; no operating-state answer is drawn.
for letter,pnp,flip,values in [('a',False,False,['+6','+0.1','-0.2']),('b',True,False,['-18','-12.3','-12']),('c',False,True,['-5.6','-6.3','-3'])]:
 c=C('F033-'+letter,'E6-2',size=(5,4));t=bjt(c,3,3,'',pnp,flip);upper=t.emitter if flip else t.collector;lower=t.collector if flip else t.emitter
 c.wire(upper,(upper.x,5));c.supply((upper.x,5),'$'+values[0]+r'\,\mathrm{V}$');c.wire(lower,(lower.x,.5));c.port((lower.x,.5));c.text(lower.x,-.1,'$'+values[2]+r'\,\mathrm{V}$');c.wire((1,3),t.base);c.port((1,3),'$'+values[1]+r'\,\mathrm{V}$');c.save()
combine(HERE,'F033',['F033-a','F033-b','F033-c'],['(a)','(b)','(c)'])
# E6-3 deliberately includes incorrect bias circuits; preserve them instead of fixing the question.
for letter in ['a','b','c','d']:
 c=C('F034-'+letter,'E6-3',size=(7,5));t=bjt(c,5,4,'T',pnp=letter=='c');input(c,t);supply(c,3,t.collector.x,7,'+12\,\mathrm{V}')
 if letter=='a':c.wire((3,7),(3,4))
 else:c.part('R',(3,7),(3,4),'$R_B$')
 if letter=='d':c.wire((t.collector.x,7),t.collector)
 else:c.part('R',(t.collector.x,7),t.collector,'$R_C$')
 c.wire(t.emitter,(t.emitter.x,0));cap(c,t.collector,(9,t.collector.y),'C_2','a');c.port((9,t.collector.y));c.port((9,0));c.wire((0,0),(9,0));c.ground((t.emitter.x,0));c.dot((3,4));c.dot((t.emitter.x,0));c.save()
combine(HERE,'F034',['F034-'+l for l in ['a','b','c','d']],['(a)','(b)','(c)','(d)'])

for key in ['F035','F036','F037','F038','F042','F043','F044','F183']:
 c=C(key,'BJT amplifier',size=(11,7));t=bjt(c,6,5);co,em,ba=t.collector,t.emitter,t.base
 top=9;division=key in ['F036','F037'];follower=key=='F038';collectorfb=key in ['F043','F044'];source=key in ['F036','F038','F044','F183']
 node=input(c,t,source=source)
 c.wire((0,0),(15,0));c.ground((co.x,0));c.dot((co.x,0))
 if follower:
  supply(c,3,co.x,top);c.wire((co.x,top),co)
 else:
  supply(c,co.x if collectorfb else 3,co.x,top);c.part('R',(co.x,top),co,'$R_c$' if key=='F183' else '$R_C$')
 if collectorfb:
  if key=='F043':
   c.wire(node,(3,co.y));c.part('R',(3,co.y),co,'$R_B$');c.dot(co)
  else:
   c.wire(node,(3,co.y));c.part('R',(3,co.y),(4.7,co.y),'$R_{B1}$');c.part('R',(4.7,co.y),co,'$R_{B2}$');c.wire((4.7,co.y),(4.7,5.2));c.wire((4.7,4.8),(4.7,3));c.wire((4.7,1),(4.7,0));c.ax.add_patch(M.plt.matplotlib.patches.Arc((4.7,5),.4,.4,theta1=-90,theta2=90,color='black',lw=1.65));cap(c,(4.7,3),(4.7,1),'C_3','a');c.dot((4.7,co.y));c.dot(co)
 else:
  c.part('R',(3,top),node,'$R_{B1}$' if division else ('$R_b$' if key=='F183' else '$R_B$'),offset=-.55)
  if division:c.part('R',node,(3,0),'$R_{B2}$',offset=-.55);c.dot((3,0))
 c.dot(node)
 if key in ['F035','F043','F044','F183']:c.wire(em,(em.x,0))
 else:emitter(c,t,bypass=key in ['F036','F037'],split=key=='F037')
 if key=='F042':
  cap(c,co,(12,co.y),plus='a');cap(c,em,(12,em.y),plus='a');c.port((12,co.y),'$1$','right');c.port((12,em.y),'$2$','right');c.port((12,0),'$-$','right');c.text(13,4.5,'$u_{o1}$',ha='left');c.text(13,1.5,'$u_{o2}$',ha='left')
 else:output(c,em if follower else co,x=13,load=key not in ['F043','F044'])
 if key=='F183':
  c.text(1.5,4,'$U_{BEQ}$');c.text(9.8,4.5,'$U_{CEQ}$');c.text(1.15,5.35,'$-$',size=14);c.text(10.2,6.1,'$-$',size=14);c.labels=[(x,y,'$v_i$' if z=='$u_i$' else z,ha,va,sz) for x,y,z,ha,va,sz in c.labels]
 c.save()

# Two-stage RC-coupled and direct-coupled amplifiers.
for key in ['F039','F040','F041','F045']:
 c=C(key,'two-stage amplifier',size=(15,8));t1=bjt(c,5,5,'T_1');t2=bjt(c,12,5,'T_2');top=10
 input(c,t1,source=key=='F039');c.wire((0,0),(18,0));c.ground((12.55,0));supply(c,3,t2.collector.x,top)
 c.part('R',(3,top),(3,5),'$R_B$' if key=='F041' else '$R_{B1}$');c.dot((3,5))
 if key!='F041':c.part('R',(3,5),(3,0),'$R_{B2}$');c.dot((3,0))
 if key=='F041':c.wire((t1.collector.x,top),t1.collector)
 else:c.part('R',(t1.collector.x,top),t1.collector,'$R_{C2}$' if key=='F040' else '$R_{C1}$')
 # First emitter network.
 e1=(t1.emitter.x,2.5);c.wire(t1.emitter,e1);c.part('R',e1,(e1[0],0),'$R_{E1}$',offset=-.5)
 if key in ['F039','F040']:
  c.wire(e1,(7.5,2.5));cap(c,(7.5,2.5),(7.5,0),'C_{E1}','a');c.dot(e1);c.dot((7.5,0))
 if key=='F045':
  # Direct coupling first collector -> second base. Feedback from second collector to first emitter.
  c.wire(t1.collector,(8,t1.collector.y),(8,5),t2.base);c.dot(t1.collector)
  c.wire(e1,(9,2.5),(9,4.8));c.ax.add_patch(M.plt.matplotlib.patches.Arc((9,5),.4,.4,theta1=-90,theta2=90,color='black',lw=1.65));c.wire((9,5.2),(9,7));c.part('R',(9,7),(t2.collector.x,7),'$R_F$');c.wire((t2.collector.x,7),t2.collector);c.dot(t2.collector);c.dot(e1)
 else:
  coupling=t1.emitter if key=='F041' else t1.collector;cap(c,coupling,(10,coupling.y),'C_2','a');c.wire((10,coupling.y),(10,5),t2.base);c.dot((10,5));c.part('R',(10,top),(10,5),'$R_{B1}$' if key=='F041' else '$R_{B3}$')
  if key in ['F039','F041']:c.part('R',(10,5),(10,0),'$R_{B2}$' if key=='F041' else '$R_{B4}$');c.dot((10,0))
 if key=='F040':c.wire((t2.collector.x,top),t2.collector)
 else:c.part('R',(t2.collector.x,top),t2.collector,'$R_{C2}$')
 e2=(t2.emitter.x,3);c.wire(t2.emitter,e2)
 if key=='F041':
  c.part('R',e2,(e2[0],1.5),'$R_{E21}$',offset=-.5);e2=(e2[0],1.5);c.part('R',e2,(e2[0],0),'$R_{E22}$',offset=-.5)
 else:c.part('R',e2,(e2[0],0),'$R_{E2}$',offset=-.5)
 if key in ['F039','F041','F045']:
  c.wire(e2,(14.5,e2[1]));cap(c,(14.5,e2[1]),(14.5,0),'C_{E2}','a');c.dot(e2);c.dot((14.5,0))
 output(c,t2.emitter if key=='F040' else t2.collector,x=17,caplabel='C_2' if key=='F045' else 'C_3',load=key!='F041');c.dot((t1.emitter.x,0));c.dot((t2.emitter.x,0));c.save()

# F046's two different feedback paths are kept as separate panels.
for letter in ['a','b']:
 c=C('F046-'+letter,'E6-22',size=(15,8));t1=bjt(c,5,5,'T_1');t2=bjt(c,12,5,'T_2');c.wire((0,0),(18,0));c.ground((t2.emitter.x,0));supply(c,3,t2.collector.x,10)
 input(c,t1);c.part('R',(t1.collector.x,10),t1.collector,'$R_{C1}$');c.part('R',(t2.collector.x,10),t2.collector,'$R_{C2}$')
 if letter=='a':
  c.part('R',(3,10),(3,5),'$R_{B1}$');c.part('R',(10,10),(10,5),'$R_{B2}$');cap(c,t1.collector,(10,t1.collector.y),'C_2','a');c.wire((10,t1.collector.y),(10,5),t2.base)
  c.wire(t1.emitter,(t1.emitter.x,2.8));c.part('R',(t1.emitter.x,2.8),(t1.emitter.x,0),'$R_{E1}$');c.wire((t1.emitter.x,2.8),(7.5,2.8));cap(c,(7.5,2.8),(7.5,0),'C_{E1}','a');c.wire(t2.emitter,(t2.emitter.x,2.8));c.part('R',(t2.emitter.x,2.8),(t2.emitter.x,0),'$R_{E2}$')
  # AC-coupled feedback from stage-2 emitter to stage-1 base, routed below ground with non-junction crossings.
  c.wire((3,5),(3,.2));c.ax.add_patch(M.plt.matplotlib.patches.Arc((3,0),.4,.4,theta1=-90,theta2=90,color='black',lw=1.65));c.wire((3,-.2),(3,-1));c.part('R',(3,-1),(7,-1),'$R_F$',offset=-.4);cap(c,(7,-1),(10,-1),'C_F','b');c.wire((10,-1),(10,-.2));c.ax.add_patch(M.plt.matplotlib.patches.Arc((10,0),.4,.4,theta1=-90,theta2=90,color='black',lw=1.65));c.wire((10,.2),(10,2.8),(t2.emitter.x,2.8));c.dot((3,5));c.dot((t2.emitter.x,2.8));c.dot((10,5));c.dot((t1.emitter.x,2.8));c.dot((7.5,0))
 else:
  c.wire(t1.collector,(8,t1.collector.y),(8,5),t2.base)
  c.wire(t1.emitter,(t1.emitter.x,2.5));c.part('R',(t1.emitter.x,2.5),(t1.emitter.x,0),'$R_{E1}$');c.wire((t1.emitter.x,2.5),(9,2.5),(9,4.8));c.ax.add_patch(M.plt.matplotlib.patches.Arc((9,5),.4,.4,theta1=-90,theta2=90,color='black',lw=1.65));c.wire((9,5.2),(9,7));c.part('R',(9,7),(t2.collector.x,7),'$R_{F1}$');c.wire((t2.collector.x,7),t2.collector)
  c.wire(t2.emitter,(t2.emitter.x,3.5));c.part('R',(t2.emitter.x,3.5),(t2.emitter.x,2.5),'$R_{E2}$');c.part('R',(t2.emitter.x,2.5),(t2.emitter.x,1.3),'$R_1$');c.part('R',(t2.emitter.x,1.3),(t2.emitter.x,0),'$R_2$');c.wire((t2.emitter.x,2.5),(15,2.5));cap(c,(15,2.5),(15,0),'C_{E2}','a')
  c.wire((3,5),(3,.2));c.ax.add_patch(M.plt.matplotlib.patches.Arc((3,0),.4,.4,theta1=-90,theta2=90,color='black',lw=1.65));c.wire((3,-.2),(3,-1));c.part('R',(3,-1),(11.5,-1),'$R_{F2}$');c.wire((11.5,-1),(11.5,-.2));c.ax.add_patch(M.plt.matplotlib.patches.Arc((11.5,0),.4,.4,theta1=-90,theta2=90,color='black',lw=1.65));c.wire((11.5,.2),(11.5,1.3),(t2.emitter.x,1.3));c.dot((3,5));c.dot((t2.emitter.x,1.3));c.dot((t2.emitter.x,2.5));c.dot(t2.collector)
 output(c,t2.collector,x=17,caplabel='C_3' if letter=='a' else 'C_2');c.save()
combine(HERE,'F046',['F046-a','F046-b'],['(a)','(b)'])

# Complementary push-pull stages: NPN upper device, PNP lower device.
for key in ['F047','F048']:
 c=C(key,'complementary output',size=(10,8));t1=bjt(c,6,6,'T_1');t2=bjt(c,6,2,'T_2',pnp=True,flip=True)
 c.wire(t1.emitter,(t1.emitter.x,4),t2.emitter);c.dot((t1.emitter.x,4));c.wire(t1.collector,(t1.collector.x,9));c.supply((t1.collector.x,9),'$+U_{CC}$');c.wire((3,9),(t1.collector.x,9));c.part('R',(3,9),(3,6),'$R_{B1}$',offset=-.5);c.wire((3,6),t1.base);c.part('D',(3,6),(3,4),'$D_1$',offset=-.5);c.part('D',(3,4),(3,2),'$D_2$',offset=-.5);c.wire((3,2),t2.base);c.dot((3,6));c.dot((3,2))
 if key=='F047':
  c.wire(t2.collector,(t2.collector.x,-1));c.supply((t2.collector.x,-1),'$-U_{CC}$');c.part('R',(3,2),(3,-1),'$R_{B2}$',offset=-.5);c.wire((3,-1),(t2.collector.x,-1));c.wire((0,6),(3,6));c.port((0,6),'$+$');c.port((0,0),'$-$');c.ground((0,0));c.wire((t1.emitter.x,4),(10,4));c.part('R',(10,4),(10,0),'$R_L$');c.ground((10,0));c.text(12,3.5,'$+$');c.text(12,2,'$u_o$');c.text(12,.3,'$-$')
 else:
  c.wire(t2.collector,(t2.collector.x,0));c.part('R',(3,2),(3,0),'$R_{B2}$',offset=-.5);c.wire((0,0),(11,0));c.ground((t2.collector.x,0));cap(c,(0,6),(3,6),'C_1','b');c.port((0,6),'$+$');c.port((0,0),'$-$');cap(c,(t1.emitter.x,4),(10,4),'C_2','a');c.part('R',(10,4),(10,0),'$R_L$');c.text(12,3.5,'$+$');c.text(12,2,'$u_o$');c.text(12,.3,'$-$');c.dot((10,0));c.text(8.4,3.15,'$U_C$');c.text(9.2,3.65,'$-$',size=14)
 # Variable upper bias resistance, with the wiper joined to the upper terminal as in the source.
 c.wire((3,9),(4.3,9),(4.3,7.5));c.d.add(E.Arrow().at((4.3,7.5)).to((3.25,7.5)))
 c.text(-.8,3,'$u_i$');c.save()

# MOS/JFET textbook circuits use the source symbols, not an inferred replacement transistor family.
def fet(c,x,y,label='T',jfet=False):
 if jfet:
  t=SimpleNamespace(gate=Point((x,y)),drain=Point((x+.75,y+.8)),source=Point((x+.75,y-.8)))
  c.wire((x+.75,y-.4),(x+.75,y+.4));c.wire((x+.75,y+.4),t.drain);c.wire((x+.75,y-.4),t.source);c.wire(t.gate,(x+.3,y));c.d.add(E.Arrow().at((x+.3,y)).to((x+.75,y)))
  c.components.append({'kind':'JFET','gate_arrow':'towards_channel','gate':list(t.gate),'drain':list(t.drain),'source':list(t.source)})
 else:t=c.d.add(E.NMos().at((x,y)).anchor('gate'))
 if label and not jfet:c.text(t.drain.x+.5,y,'$'+label+'$',ha='left')
 return t
for key in ['F049','F050']:
 c=C(key,'FET amplifier',size=(10,7));t=fet(c,6,5,jfet=key=='F049');g,d,s=t.gate,t.drain,t.source;c.wire((0,0),(14,0));c.ground((d.x,0))
 if key=='F049':
  cap(c,(0,g.y),(3,g.y),'C_1','a');c.wire((3,g.y),g);c.part('R',(3,g.y),(3,0),'$R_1$',offset=-.6);c.dot((3,g.y));c.part('R',d,(d.x,9),r'$R_2=6.8\,\mathrm{k}\Omega$');c.supply((d.x,9),r'$+10\,\mathrm{V}$');c.wire(s,(s.x,3));c.part('R',(s.x,3),(s.x,0),'$R_3$',offset=-.6);c.wire((s.x,3),(9,3));cap(c,(9,3),(9,0),'C_3','a');output(c,d,x=12)
  c.text(12.5,.8,r'$10\,\mathrm{k}\Omega$',ha='left');c.text(2.4,1.5,r'$5\,\mathrm{M}\Omega$',ha='right');c.text(s.x-.5,.8,r'$2\,\mathrm{k}\Omega$',ha='right')
 else:
  cap(c,(0,g.y),(2,g.y),'C_1','b');c.wire((2,g.y),g);c.wire((2.5,g.y),(2.5,g.y-1.5));c.part('R',(2.5,g.y-1.5),(4.7,g.y-1.5),'$R_G$',offset=-.4);c.part('R',(4.7,9),(4.7,g.y-1.5),'$R_{G1}$',offset=-.5);c.part('R',(4.7,g.y-1.5),(4.7,0),'$R_{G2}$',offset=-.5);c.wire((4.7,9),(d.x,9),d);c.supply((d.x,9),'$+U_{CC}$');c.wire(s,(s.x,2));c.part('R',(s.x,2),(s.x,0),'$R_S$');output(c,s,x=12,load=False);c.dot((4.7,g.y-1.5));c.dot((2.5,g.y))
 c.port((0,g.y),'$+$');c.port((0,0),'$-$');c.text(-.5,g.y/2,'$u_i$' if key=='F049' else '$\dot U_i$',ha='right');c.labels=[(x,y,'$\dot U_o$' if key=='F050' and z=='$u_o$' else z,ha,va,sz) for x,y,z,ha,va,sz in c.labels];c.save()

# Final rendering. Extra exam and knowledge figures are appended below before this block.
def render_all():
 for p in HERE.glob('F*.svg'):
  if '-' in p.stem:continue
  # Standalone PNGs come directly from Matplotlib, which preserves dashed lines.
  # Only composed panels need SVG rasterization.
  if p.stem in ['F033','F034','F046','F136','F186']:
   d=fitz.open(p);pdf=fitz.open('pdf',d.convert_to_pdf());pdf[0].get_pixmap(matrix=fitz.Matrix(2,2)).save(p.with_suffix('.png'))
 (HERE/'geometry.json').write_bytes((json.dumps(M.records,ensure_ascii=False,indent=2)+'\n').encode())
if __name__=='__main__':render_all();print('chapter 6 draft circuits rendered')
