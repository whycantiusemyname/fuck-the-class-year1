"""Full chapter render: python finish_knowledge.py. Source figures remain read-only."""
from exams_and_knowledge import *

# Simulation screenshot: the 180k resistor is connected to the upper bias node,
# not directly to the gate. The 3M resistor connects that node to the gate.
c=C('F003','simulation 4',size=(14,9));t=fet(c,7,5,r'\mathrm{IRF1310}')
c.wire((-4,0),(15,0));c.ground((8,0));c.part('AC',(-4,0),(-4,5),'$u_i$',offset=-.8)
cap(c,(-4,5),(0,5),r'30\,\mu\mathrm{F}');c.wire((0,5),t.gate)
c.wire((4,10),(t.drain.x,10),t.drain);c.supply((t.drain.x,10),r'$12\,\mathrm{V}$')
c.part('R',(4,10),(1.5,10),r'$51\,\mathrm{k}\Omega$');c.wire((1.5,10),(1.5,8),(3,8))
c.part('R',(3,8),(3,5),r'$3\,\mathrm{M}\Omega$',offset=.5)
# Cross the input at x=1.5 with a bridge, preserving the non-junction.
c.wire((1.5,8),(1.5,5.18));c.ax.add_patch(__import__('matplotlib').patches.Arc((1.5,5),.36,.36,theta1=-90,theta2=90,lw=1.65));c.wire((1.5,4.82),(1.5,2.6));c.part('R',(1.5,2.6),(1.5,0),r'$180\,\mathrm{k}\Omega$',offset=-.5)
c.part('R',t.source,(t.source.x,0),r'$680\,\Omega$',offset=-.5);cap(c,t.source,(14,t.source.y),r'30\,\mu\mathrm{F}');c.part('R',(14,t.source.y),(14,0),r'$6.8\,\mathrm{k}\Omega$')
c.wire((t.drain.x,10),(11,10),(11,8));c.part('S',(11,8),(11,6));c.text(11,7,'$V$');c.text(12,7,r'$1.992\,\mathrm{V}$',ha='left');c.text(10.7,8.1,'$+$');c.text(10.7,5.9,'$-$');c.wire((11,6),(11,4.8),(10,4.8),(10,t.source.y),t.source);c.dot((10,t.source.y))
c.port((-4,5),'A','left');c.port((14,t.source.y),'B','right');c.text(7,-1,'A、B：原示波器通道；电压表读数照录原截图',size=15)
for q in [(3,5),(1.5,8),(t.drain.x,10),tuple(t.source),(14,0)]:c.dot(q)
c.save()

c=C('F184','cascade port model',size=(19,8));c.part('V',(0,0),(0,2),'$u_s$',offset=-.6);c.part('R',(0,2),(0,5),'$R_s$',offset=-.5)
for i,x in enumerate([3,10,18],1):
 suffix=str(i) if i<3 else 'n';prev='i' if i==1 else 'o1' if i==2 else 'o(n-1)'
 c.part('R',(x,5),(x,0),'$R_{i'+suffix+'}$',offset=.4)
 c.d.add(E.SourceControlledV().at((x+3,0)).to((x+3,2.4)).theta(90));c.text(x+3.6,1.2,'$A_{uo'+suffix+'}u_{'+prev+'}$',ha='left')
 c.part('R',(x+3,2.4),(x+3,5),'$R_{o'+suffix+'}$');c.ax.add_patch(Rectangle((x-1,-.7),5.2,6.7,fill=False,linestyle='--',lw=1.2,color='black'))
 c.wire((x,0),(x+3,0));c.ground((x+1.5,0));c.dot((x,0));c.dot((x+3,0))
c.wire((0,5),(3,5));c.wire((0,0),(3,0));c.wire((6,5),(10,5));c.wire((6,0),(10,0))
c.d.add(E.Line().at((13,5)).to((18,5)).linestyle(':'));c.d.add(E.Line().at((13,0)).to((18,0)).linestyle(':'));c.text(15.5,-1.2,'$u_{o(n-1)}$')
c.wire((21,5),(25,5));c.part('R',(25,5),(25,0),'$R_L$');c.wire((21,0),(25,0));c.d.add(E.Arrow().at((22,5.3)).to((24,5.3)));c.text(23,5.9,'$i_o$');c.d.add(E.Arrow().at((.6,5.3)).to((2,5.3)));c.text(1.3,5.9,'$i_i$')
for x,l in [(1.8,'u_i'),(8,'u_{o1}'),(24,'u_o')]:
 c.text(x,4.4,'$+$');c.text(x,2.5,'$'+l+'$');c.text(x,.6,'$-$')
c.text(12,-2.3,'后级放大器的输入电阻是前级放大器的负载，前级放大器的输出电路是后级放大器的信号源。',size=15);c.save()

c=C('F185','differential half circuit',size=(13,8));q1=bjt(c,4,5,'');q2=c.d.add(E.BjtNpn().reverse().at((12,5)).anchor('base'));mid=8;top=9;em=2
for q,idx,x,sgn in [(q1,'1',0,''),(q2,'2',16,'-')]:
 c.part('R',(x,5),q.base,'$R_{b'+idx+'}$');c.part('V',(x,0),(x,5),'$'+sgn+r'\frac{u_{id}}{2}$',offset=-1 if x==0 else .5);c.ground((x,0));c.port((x,5),'a' if idx=='1' else 'b','left' if x==0 else 'right');c.part('R',(q.collector.x,top),q.collector,'$R_{C'+idx+'}$',offset=-.5 if idx=='1' else .4);c.wire(q.emitter,(q.emitter.x,em));c.wire((q.collector.x,top),(mid,top));c.part('R',q.collector,(mid,q.collector.y),r'$\frac{R_L}{2}$');c.dot(q.collector)
c.wire((q1.emitter.x,em),(q2.emitter.x,em));c.ground((mid,top));c.ground((mid,q1.collector.y));c.ground((mid,em));c.ax.plot([mid,mid],[.5,10],ls=':',color='black',lw=1.5)
c.text(6.1,4.5,r'$+\quad\frac{v_{od}}{2}\quad-$');c.text(10,4.5,r'$-\quad-\frac{v_{od}}{2}\quad+$');c.save()

for otl in [False,True]:
 key='F186-'+('OTL' if otl else 'OCL');c=C(key,key,size=(10,8));q1=bjt(c,5,7,'T_1');q2=bjt(c,5,3,'T_2',pnp=True,flip=True);top=10;bottom=0
 c.wire(q1.collector,(q1.collector.x,top),(2,top));c.part('R',(2,top),(2,7),'$R_1$',offset=-.5);c.wire((2,7),q1.base);c.part('D',(2,7),(2,5),'$D_1$',offset=-.5);c.part('D',(2,5),(2,3),'$D_2$',offset=-.5);c.wire((2,3),q2.base);c.part('R',(2,3),(2,bottom),'$R_2$',offset=-.5);c.wire((2,bottom),(q2.collector.x,bottom),q2.collector)
 c.wire(q1.emitter,(q1.emitter.x,5),q2.emitter);c.supply((q1.collector.x,top),'$+V_{CC}$');c.wire((0,5),(2,5));c.port((0,5),'$+$');c.port((0,1),'$-$');c.ground((0,1));c.text(-.5,3,'$v_i$',ha='right')
 if otl:cap(c,(q1.emitter.x,5),(10,5),'C');c.ground((q2.collector.x,0));c.wire((q2.collector.x,0),(10,0))
 else:c.wire((q1.emitter.x,5),(10,5));c.port((q2.collector.x,0),'$-V_{CC}$','right');c.ground((10,0))
 c.part('R',(10,5),(10,0),'$R_L$');c.text(12,2.5,'$v_o$');c.text(11,4.7,'$+$');c.text(11,.3,'$-$')
 for p in [(2,7),(2,5),(2,3),(q1.emitter.x,5)]:c.dot(p)
 c.text(5,-1.7,'OTL：单电源' if otl else 'OCL：双电源',size=17);c.text(5,-3,r'$P_{OM}=\frac{(V_{CC}/2)^2}{2R_L}=\frac{V_{CC}^2}{8R_L}$' if otl else r'$P_{OM}=\frac{V_{CC}^2}{2R_L}$',size=22);c.save()
combine(HERE,'F186',['F186-OCL','F186-OTL'])
import recover_C3
render_all();print('full chapter 6 rendered')
