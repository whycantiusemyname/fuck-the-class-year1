"""Complete chapter-6 generation: python exams_and_knowledge.py.
Imports the chapter's source-checked textbook primitives, then adds exam and knowledge diagrams.
"""
from generate import *
from matplotlib.patches import Circle,Rectangle

def ccsource(c,a,b,label):
 c.d.add(E.SourceControlledI().at(a).to(b).theta(math.degrees(math.atan2(b[1]-a[1],b[0]-a[0]))))
 c.text((a[0]+b[0])/2+.65,6 if 'U_{GS}' in label else (a[1]+b[1])/2,label,ha='left')
def value(k):return '$'+k+'$'

# Generic MOS stages. Numeric values are included only where printed on the source figure.
mos_specs={
'F112':dict(v='V_S',r1='R_{G1}',r2='R_{G2}',rd='R_D',rsig='R_{sig}',ui='v_{sig}',c1='C_1',outputcap=None,rl=None),
'F151':dict(v='9\\,\\mathrm{V}',r1='350\\,\\mathrm{k}\\Omega',r2='100\\,\\mathrm{k}\\Omega',rd='2\\,\\mathrm{k}\\Omega',c1='5\\,\\mu\\mathrm{F}',outputcap='5\\,\\mu\\mathrm{F}',rl='2\\,\\mathrm{k}\\Omega'),
'F160':dict(v='V_S',r1='R_{G1}',r2='R_{G2}',rd='R_D',rsig='R_{sig}',ui='v_{sig}',c1='C_1',outputcap='C_2',rl=None),
'F165':dict(v='V_S',r1='R_1',r2='R_2',rd='R_3',c1='C_1',outputcap=None,rl=None),
'F168':dict(v='3\\,\\mathrm{V}',r1='10\\,\\mathrm{k}\\Omega',r2='10\\,\\mathrm{k}\\Omega',rd='5\\,\\mathrm{k}\\Omega',ui='u_s(t)',c1='C_1',outputcap='C_2',rl=None,source=True),
'F172':dict(v='V_S=10\\,\\mathrm{V}',r1='R_1',r2='R_2',rd='R_D=6\\,\\mathrm{k}\\Omega',rg='R_G',c1='C_1',outputcap='C_2',rl='R_L',source=True),
'F178':dict(v='V_S',r1='R_1',r2='R_2',rd='R_3',re='R_4',ce='C_2',c1='C_1',outputcap='C_3',rl='R_L'),
'F145':dict(v='12\\,\\mathrm{V}',r1='50\\,\\mathrm{k}\\Omega',r2='R',rd='0.5\\,\\mathrm{k}\\Omega',rg='1\\,\\mathrm{M}\\Omega',c1='C',outputcap=None,rl=None),
'F003':dict(v='12\\,\\mathrm{V}',r1='3\\,\\mathrm{M}\\Omega',r2='180\\,\\mathrm{k}\\Omega',rd=None,re='680\\,\\Omega',c1='30\\,\\mu\\mathrm{F}',outputcap='30\\,\\mu\\mathrm{F}',rl='6.8\\,\\mathrm{k}\\Omega',supplyr='51\\,\\mathrm{k}\\Omega',source=False,follower=True),
}
for key,spec in mos_specs.items():
 if key=='F003':continue
 c=C(key,'MOS amplifier',size=(12,8));t=fet(c,7,5,'' if key in ['F112','F160','F165','F168','F172','F178'] else ('IRF1310' if key=='F003' else 'T_1'));g,d,s=t.gate,t.drain,t.source;top=10;biasx=4.5 if spec.get('rg') else 3.5;c.wire((0,0),(16,0));c.ground((d.x,0))
 # Some source drawings use an unnumbered third MOS terminal; do not add body terminal text.
 by=3.5 if spec.get('rg') else 5;c.part('R',(biasx,top),(biasx,by),value(spec['r1']),offset=-.5);c.part('R',(biasx,by),(biasx,0),value(spec['r2']),offset=-.5);c.dot((biasx,by));c.dot((biasx,0))
 if spec.get('rg'):
  # Divider-to-gate resistor under the input wire; their crossing is not a junction.
  cap(c,(0,g.y),(2,g.y),spec['c1']);c.wire((2,g.y),g);c.wire((2.5,g.y),(2.5,3.5));c.part('R',(2.5,3.5),(biasx,3.5),value(spec['rg']),offset=-.45);c.dot((2.5,g.y))
 else:
  cap(c,(0,g.y),(biasx,g.y),spec['c1']);c.wire((biasx,g.y),g)
 if spec.get('source') or spec.get('rsig'):
  if spec.get('rsig'):
   c.part('R',(-4,g.y),(-1,g.y),value(spec['rsig']));c.wire((-1,g.y),(0,g.y));c.part('V',(-4,0),(-4,g.y),value(spec.get('ui','u_i')),offset=-.8);c.wire((-4,0),(0,0));c.ground((-4,0))
  else:c.part('V',(0,0),(0,g.y),value(spec.get('ui','u_i')),offset=-.8)
 else:
  c.port((0,g.y),'$+$');c.port((0,0),'$-$');c.text(-.6,2.5,value('u_i(t)' if key=='F165' else 'v_i' if key=='F178' else 'u_i'),ha='right')

 if key=='F003':c.part('R',(biasx,top),(d.x,top),value(spec['supplyr']))
 else:c.wire((biasx,top),(d.x,top))
 c.supply((d.x,top),value(spec['v']))
 if spec.get('rd'):c.part('R',(d.x,top),d,value(spec['rd']))
 else:c.wire((d.x,top),d)
 if spec.get('re'):
  c.wire(s,(s.x,2.8));c.part('R',(s.x,2.8),(s.x,0),value(spec['re']),offset=-.5)
  if spec.get('ce'):c.wire((s.x,2.8),(10,2.8));cap(c,(10,2.8),(10,0),spec['ce']);c.dot((s.x,2.8));c.dot((10,0))
 else:c.wire(s,(s.x,0))
 out=s if spec.get('follower') else d
 if spec.get('outputcap'):cap(c,out,(14,out.y),spec['outputcap'])
 else:c.wire(out,(14,out.y))
 c.port((14,out.y),'$+$','right');c.port((14,0),'$-$','right');c.text(17,out.y/2,'$u_o(t)$' if key in ['F165','F168'] else '$v_o$' if key in ['F112','F160','F178'] else '$u_o$',ha='left')
 if spec.get('rl'):c.part('R',(14,out.y),(14,0),value(spec['rl']));c.dot((14,out.y));c.dot((14,0))
 c.dot((d.x,0));c.dot(d)
 if key=='F165':
  for p,label in [(g,'g'),(d,'d'),(s,'s')]:c.text(p.x-.5,p.y+.2,'$'+label+'$',ha='right')
 if key=='F160':c.text(14.2,out.y+.5,'$2$');c.text(14.2,-.5,"$2'$ ");c.text(.2,-.5,"$1'$")
 if key=='F003':
  # Supply-series 51k branch and a voltmeter are part of the printed simulation schematic.
  c.text(d.x+1.3,7.7,'$V$',ha='left');c.part('AC',(0,0),(0,g.y),'$u_i$',offset=-.8)
 c.save()

# Source follower following a common-source stage, including gate-protection bias resistors.
for key in ['F108','F125']:
 c=C(key,'MOS cascade',size=(15,8));t1=fet(c,6,5,'T_1');t2=fet(c,13,5,'T_2');top=10;c.wire((0,0),(18,0));c.ground((t1.source.x,0));c.wire(t1.source,(t1.source.x,0));c.wire(t2.drain,(t2.drain.x,top));c.wire((3,top),(t2.drain.x,top));c.supply((t2.drain.x,top),'$V_{CC}$' if key=='F108' else '$12\,\mathrm{V}$')
 cap(c,(0,5),(2,5),'C_1');c.wire((2,5),t1.gate);c.part('R',(3,top),(3,6.5),r'$40\,\mathrm{k}\Omega$' if key=='F108' else r'$6\,\mathrm{k}\Omega$');c.part('R',(3,6.5),(3,0),r'$20\,\mathrm{k}\Omega$' if key=='F108' else r'$3\,\mathrm{k}\Omega$');c.wire((3,6.5),(4,6.5));c.part('R',(4,6.5),(4,5),r'$1\,\mathrm{M}\Omega$' if key=='F108' else r'$48\,\mathrm{k}\Omega$');c.dot((3,6.5));c.dot((4,5))
 c.part('R',(t1.drain.x,top),t1.drain,r'$5\,\mathrm{k}\Omega$' if key=='F108' else r'$1\,\mathrm{k}\Omega$')
 if key=='F108':
  cap(c,t1.drain,(10,t1.drain.y),'C_2');c.part('R',(10,top),(10,5),r'$20\,\mathrm{k}\Omega$')
 else:c.wire(t1.drain,(10,t1.drain.y))
 c.wire((10,t1.drain.y),(10,5),t2.gate);c.dot((10,5))
 if key=='F108':c.part('R',(10,5),(10,0),r'$40\,\mathrm{k}\Omega$')
 else:
  # The second gate is wired to the first drain in this source; remove the extra invented bias branch.
  pass
 c.wire(t2.source,(t2.source.x,3));c.part('R',(t2.source.x,3),(t2.source.x,0),r'$5\,\mathrm{k}\Omega$' if key=='F108' else r'$1\,\mathrm{k}\Omega$');cap(c,t2.source,(17,t2.source.y),'C_3' if key=='F108' else 'C_2');c.port((17,t2.source.y),'$+$','right');c.port((17,0),'$-$','right');c.port((0,5),'$+$');c.port((0,0),'$-$');c.text(19.5,t2.source.y/2,'$u_o$',ha='left');c.text(-.5,2.5,'$u_i$',ha='right')
 if key=='F125':c.part('R',(17,t2.source.y),(17,0),r'$1\,\mathrm{k}\Omega$')
 c.save()

# F051: MOS common-source -> BJT common-emitter, every printed value retained.
c=C('F051','E6-32',size=(20,9));t1=fet(c,6,5,'');t2=bjt(c,17,5,'T');top=10;c.wire((0,0),(23,0));c.ground((6,0));c.wire((3,top),(t2.collector.x,top));c.supply((t2.collector.x,top),r'$+24\,\mathrm{V}$')
cap(c,(0,5),(2,5),'C_1','b');c.wire((2,5),t1.gate);c.wire((2.5,5),(2.5,3.5));c.part('R',(2.5,3.5),(4,3.5),r'$R_G$'+'\n'+r'$1\,\mathrm{M}\Omega$',offset=-.5);c.part('R',(4,top),(4,3.5),r'$R_{G1}$'+'\n'+r'$200\,\mathrm{k}\Omega$',offset=-.5);c.part('R',(4,3.5),(4,0),r'$R_{G2}$'+'\n'+r'$60\,\mathrm{k}\Omega$',offset=-.5);c.dot((4,3.5))
c.part('R',(t1.drain.x,top),t1.drain,r'$R_D$'+'\n'+r'$10\,\mathrm{k}\Omega$');c.wire(t1.source,(t1.source.x,2.5));c.part('R',(t1.source.x,2.5),(t1.source.x,0),r'$R_S$'+'\n'+r'$10\,\mathrm{k}\Omega$',offset=-.5);c.wire((t1.source.x,2.5),(9,2.5));cap(c,(9,2.5),(9,0),'C_S','a')
cap(c,t1.drain,(14,t1.drain.y),'C_2','a');c.wire((14,t1.drain.y),(14,5),t2.base);c.part('R',(14,top),(14,5),r'$R_{B1}$'+'\n'+r'$33\,\mathrm{k}\Omega$',offset=-.5);c.part('R',(14,5),(14,0),r'$R_{B2}$'+'\n'+r'$8.2\,\mathrm{k}\Omega$',offset=-.5);c.dot((14,5));c.part('R',(t2.collector.x,top),t2.collector,r'$R_C$'+'\n'+r'$10\,\mathrm{k}\Omega$');c.wire(t2.emitter,(t2.emitter.x,3.2));c.part('R',(t2.emitter.x,3.2),(t2.emitter.x,1.8),r'$R_E^{\prime}$'+'\n'+r'$0.39\,\mathrm{k}\Omega$',offset=-.5);c.part('R',(t2.emitter.x,1.8),(t2.emitter.x,0),r'$R_E$'+'\n'+r'$3\,\mathrm{k}\Omega$',offset=-.5);c.wire((t2.emitter.x,1.8),(20,1.8));cap(c,(20,1.8),(20,0),'C_E','a');cap(c,t2.collector,(22,t2.collector.y),'C_3','a');c.part('R',(22,t2.collector.y),(22,0),r'$R_L$'+'\n'+r'$10\,\mathrm{k}\Omega$');c.port((0,5),'$+$');c.port((0,0),'$-$');c.text(-.5,2.5,'$u_i$',ha='right');c.text(24.5,t2.collector.y/2,'$u_o$',ha='left');c.save()

# Transistor voltage checks: source polarity/direction is preserved without adding state answers.
c=C('F132','device terminal voltages',size=(5,5));c.ax.add_patch(Circle((3,3),1.2,fill=False,lw=1.65,color='black'));c.wire((3,4.2),(3,5.5));c.wire((3,1.8),(3,.3));c.wire((.3,3),(1.8,3));c.text(3,6,r'$12\,\mathrm{V}$');c.text(3,-.2,r'$0\,\mathrm{V}$');c.text(.2,3,r'$11.3\,\mathrm{V}$',ha='right');c.save()
for i,(pnp,vs) in enumerate([(False,['8','3.7','3']),(True,['12','2','3']),(False,['3.3','3.7','3'])]):
 c=C('F136-'+str(i),'transistor voltages',size=(5,4));t=bjt(c,3,3,'',pnp=pnp);c.wire(t.collector,(t.collector.x,5.5));c.supply((t.collector.x,5.5),'$'+vs[0]+r'\,\mathrm{V}$');c.wire(t.emitter,(t.emitter.x,.5));c.port((t.emitter.x,.5));c.text(t.emitter.x,-.1,'$'+vs[2]+r'\,\mathrm{V}$');c.wire((1,3),t.base);c.port((1,3),'$'+vs[1]+r'\,\mathrm{V}$');c.save()
combine(HERE,'F136',['F136-0','F136-1','F136-2'])
c=C('F137','separate bias CE',size=(10,6));t=bjt(c,6,5,'');c.wire(t.emitter,(t.emitter.x,0));c.ground((t.emitter.x,0));c.wire((0,0),(14,0));cap(c,(0,5),(3,5),'C_1','b');c.wire((3,5),t.base);c.part('R',(3,5),(3,2),'$R_b$',offset=-.5);c.part('B',(3,0),(3,2),'$V_{BB}$',True,offset=-.6);c.wire(t.collector,(9,t.collector.y));c.part('R',(9,t.collector.y),(9,2),'$R_c$');c.part('B',(9,0),(9,2),'$V_{CC}$',True);cap(c,t.collector,(12,t.collector.y),'C_2','a');c.port((0,5),'$+$');c.port((0,0),'$-$');c.port((12,t.collector.y),'$+$','right');c.port((12,0),'$-$','right');c.text(13,3,'$v_o$',ha='left');c.text(-.5,2.5,'$v_i$',ha='right');c.dot((3,5));c.dot(t.collector)
for p,label in [(t.base,'b'),(t.collector,'c'),(t.emitter,'e')]:c.text(p.x-.2,p.y+.3,'$'+label+'$',ha='right')
c.save()

# Four-transistor differential input with diode-connected mirror bias.
c=C('F094','differential mirror bias',size=(12,9));q1=bjt(c,4,7,'Q_1');q2elm=E.BjtNpn().reverse();q2=c.d.add(q2elm.at((11,7)).anchor('base'));c.text(q2.center.x-.4,7,'$Q_2$',ha='right');q3=c.d.add(E.BjtNpn().reverse().at((6,2.5)).anchor('base'));q4=bjt(c,8,2.5,'Q_4');c.text(q3.center.x-.4,2.5,'$Q_3$',ha='right');top=10;bottom=-1;c.wire((q1.collector.x,top),(q2.collector.x,top));c.supply((q4.collector.x,top),'$+V_{CC}$')
for q in [q1,q2]:c.part('R',(q.collector.x,top),q.collector,'$R_C$');c.wire(q.emitter,(q.emitter.x,5.7))
c.wire((q1.emitter.x,5.7),(q2.emitter.x,5.7));c.wire((7.5,5.7),(7.5,4.2),(q3.collector.x,4.2),q3.collector);c.dot((7.5,5.7));c.wire(q3.base,q4.base);c.wire(q4.collector,(7,q4.collector.y),(7,2.5));c.dot(q4.collector);c.dot((7,2.5));c.part('R',(q4.collector.x,5),q4.collector,'$R$');c.d.add(E.Ground().up().at((q4.collector.x,5)));c.part('R',q3.emitter,(q3.emitter.x,bottom),'$R_1$');c.part('R',q4.emitter,(q4.emitter.x,bottom),'$R_2$');c.wire((q3.emitter.x,bottom),(q4.emitter.x,bottom));c.port((q4.emitter.x,bottom));c.text(q4.emitter.x,bottom-.6,'$-V_{EE}$',va='top');c.wire((2,7),q1.base);c.port((2,7),'$v_1$');c.wire(q2.base,(13,7));c.port((13,7),'$v_2$','right');c.wire(q1.collector,(q1.collector.x+.6,q1.collector.y));c.port((q1.collector.x+.6,q1.collector.y));c.wire(q2.collector,(q2.collector.x-.6,q2.collector.y));c.port((q2.collector.x-.6,q2.collector.y));c.text(7.5,8.2,'$+\quad v_o\quad-$');c.save()

# Three common-emitter stages with emitter-current feedback; upper rail is AC ground in the source.
c=C('F095','three-stage feedback',size=(16,8));ts=[bjt(c,x,5,'VT_'+str(i+1)) for i,x in enumerate([4,9,14])];c.wire((0,0),(19,0));c.wire((ts[0].collector.x,9),(ts[2].collector.x,9));c.ground((ts[2].collector.x,9))
for i,t in enumerate(ts):c.part('R',(t.collector.x,9),t.collector,'$R_{C'+str(i+1)+'}$')
for a,b in zip(ts,ts[1:]):c.wire(a.collector,(a.collector.x+1.5,a.collector.y),(a.collector.x+1.5,5),b.base)
c.wire((0,5),ts[0].base);c.port((0,5),'$+$');c.port((0,0),'$-$');c.part('R',(2,5),(2,0),'$R_{B1}$');c.dot((2,5));c.wire(ts[1].emitter,(ts[1].emitter.x,0));c.wire(ts[0].emitter,(ts[0].emitter.x,2.5));c.part('R',(ts[0].emitter.x,2.5),(ts[0].emitter.x,0),'$R_{E1}$');c.wire(ts[2].emitter,(ts[2].emitter.x,2.5));c.part('R',(ts[2].emitter.x,2.5),(ts[2].emitter.x,0),'$R_{E3}$');c.part('R',(ts[0].emitter.x,2.5),(7,2.5),'$R_{F2}$');c.wire((7,2.5),(ts[1].emitter.x-.2,2.5));c.ax.add_patch(M.plt.matplotlib.patches.Arc((ts[1].emitter.x,2.5),.4,.4,theta1=0,theta2=180,color='black',lw=1.65));c.wire((ts[1].emitter.x+.2,2.5),(ts[2].emitter.x,2.5));c.wire(ts[2].collector,(18,ts[2].collector.y));c.part('R',(18,ts[2].collector.y),(18,0),'$R_L$');c.port((18,ts[2].collector.y),'$+$','right');c.port((18,0),'$-$','right');c.text(19,2.7,'$u_o$',ha='left');c.text(-.7,2.5,'$u_i$',ha='right');c.d.add(E.Arrow().at((.5,5.5)).to((2,5.5)));c.text(1,6,'$i_i$');c.d.add(E.Arrow().at((17,6.4)).to((15,6.4)));c.text(16,7,'$i_{c3}$');c.text(.7,-.8,'$R_{if}$');c.d.add(E.Arrow().at((.7,.3)).to((.7,3.5)));c.text(17,-.8,'$R_{of}$');c.d.add(E.Arrow().at((17,.3)).to((17,3.5)));c.save()

# Controlled-source small-signal networks.
c=C('F107','controlled current source',size=(10,5));c.part('V',(0,0),(0,4),'$u_s$',offset=-.8);c.part('R',(0,4),(3,4),r'$0.2\,\mathrm{k}\Omega$');c.part('R',(3,4),(6,4),r'$1.8\,\mathrm{k}\Omega$');c.part('R',(3,4),(3,0),r'$200\,\mathrm{k}\Omega$',offset=-.5);c.wire((6,4),(10,4));ccsource(c,(7,0),(7,4),'$65i_b$');c.part('R',(10,4),(10,0),r'$2\,\mathrm{k}\Omega$');c.wire((0,0),(10,0));c.ground((7,0));c.dot((3,4));c.dot((7,4));c.text(12.5,2,'$u_o$');c.d.add(E.Arrow().at((3.4,5.2)).to((4.6,5.2)));c.text(4,5.7,'$i_b$');c.save()
for key in ['F123','F149','F150']:
 c=C(key,'controlled source network',size=(13,6));c.wire((0,0),(15,0));c.ground((7,0))
 if key=='F123':
  c.part('V',(0,0),(0,2),r'$12\,\mathrm{V}$',offset=-.7);c.part('R',(0,2),(0,5),r'$3\,\mathrm{k}\Omega$',offset=-.5);c.wire((0,5),(3,5));c.part('R',(3,5),(3,0),r'$1\,\mathrm{k}\Omega$');c.text(5,4.8,'$+$');c.text(5,2.5,'$U_{GS}$');c.text(5,.5,'$-$');c.part('V',(7,0),(7,2),r'$2\,\mathrm{V}$',offset=-.7);ccsource(c,(7,5),(7,2),r'$\frac{4}{7}(U_{GS}-2)$');c.part('V',(10,0),(10,2),r'$12\,\mathrm{V}$');c.part('R',(10,5),(10,2),r'$2\,\mathrm{k}\Omega$');rload=r'$2\,\mathrm{k}\Omega$';clabel=r'5\,\mu\mathrm{F}'
 elif key=='F149':
  c.part('V',(0,0),(0,2),r'$9\,\mathrm{V}$',offset=-.7);c.part('R',(0,2),(0,5),r'$414\,\mathrm{k}\Omega$',offset=-.5);c.wire((0,5),(3,5));c.part('R',(3,5),(3,2),r'$1\,\mathrm{k}\Omega$',offset=-.6);c.part('V',(3,0),(3,2),r'$0.7\,\mathrm{V}$');ccsource(c,(7,5),(7,0),'$50I$');c.part('V',(10,0),(10,2),r'$9\,\mathrm{V}$');c.part('R',(10,5),(10,2),r'$5\,\mathrm{k}\Omega$');rload=r'$5\,\mathrm{k}\Omega$';clabel=r'5\,\mu\mathrm{F}';c.d.add(E.Arrow().at((4.2,4.4)).to((4.2,3.5)));c.text(4.6,4.1,'$I$')
 else:
  c.part('V',(0,0),(0,3),'$u_i$',offset=-.7);c.part('R',(0,3),(0,5),r'$0.5\,\mathrm{k}\Omega$',offset=-.5);c.wire((0,5),(3,5));cap(c,(3,5),(3,0),r'50\,\mathrm{pF}');c.text(4.8,2.5,'$u$');c.text(4.8,4.5,'$+$');c.text(4.8,.5,'$-$');ccsource(c,(7,5),(7,0),'$4u$');c.part('R',(10,5),(10,0),r'$1\,\mathrm{k}\Omega$');rload=r'$1\,\mathrm{k}\Omega$';clabel=r'5\,\mu\mathrm{F}'
 c.wire((7,5),(10,5));cap(c,(10,5),(14,5),clabel);c.part('R',(14,5),(14,0),rload);c.port((14,5),'$+$','right');c.port((14,0),'$-$','right');c.text(17,2.5,'$u_o$',ha='left');c.dot((10,5));c.dot((7,5));c.save()

# Op-amp current-feedback networks, preserving the particular source input polarities.
for key in ['F109','F126','F142']:
 c=C(key,'two-opamp feedback',size=(16,8));plus1=key!='F109';n1,p1,o1=c.op(4,6,plus_top=plus1,label='A_1');n2,p2,o2=c.op(10,6,plus_top=key!='F109',label='A_2');k='5' if key=='F126' else '10';inp=p1 if plus1 else n1;other=n1 if plus1 else p1;c.part('R',(0,inp.y),inp,'$'+k+r'\,\mathrm{k}\Omega$');c.port((0,inp.y),'$u_i$');c.wire(other,(3,other.y),(3,3));c.part('R',(3,3),(3,0),'$'+k+r'\,\mathrm{k}\Omega$');c.ground((3,0));mid=p2 if key!='F109' else n2;c.part('R',o1,mid,'$'+k+r'\,\mathrm{k}\Omega$');other2=n2 if key!='F109' else p2
 if key=='F109':
  c.wire(other2,(9,other2.y),(9,3));c.part('R',(9,3),(9,0),r'$10\,\mathrm{k}\Omega$');c.ground((9,0))
 else:
  c.wire(other2,(9,other2.y),(9,8.5));c.part('R',(9,8.5),(14,8.5),r'$10\,\mathrm{k}\Omega$');c.wire((14,8.5),(14,6),o2);c.dot((14,6))
  if key=='F126':c.part('R',(9,other2.y),(9,0),r'$10\,\mathrm{k}\Omega$');c.ground((9,0))
 c.wire(o2,(14,6));c.part('R',(14,6),(17,6),'$R_L$');c.part('R',(17,6),(17,0),r'$5\,\mathrm{k}\Omega$' if key=='F126' else r'$1\,\mathrm{k}\Omega$' if key=='F142' else r'$10\,\mathrm{k}\Omega$');c.ground((17,0));c.d.add(E.Arrow().at((16,6.5)).to((17.5,6.5)));c.text(16.7,7,'$i_o$')
 if key=='F142':
  c.wire((17,6),(18,6),(18,-1))
  if key=='F142':c.part('R',(18,-1),(1.5,-1),'$R_f$')
  else:c.wire((18,-1),(1.5,-1))
  c.wire((1.5,-1),(1.5,3),(3,3));c.dot((17,6));c.dot((3,3))
 c.save()

c=C('F098','composite opamp feedback',size=(14,8));n,p,o=c.op(5,6,plus_top=True,label='A_1');c.part('R',(0,p.y),p,'$R_s$');c.part('V',(0,0),(0,p.y),'$u_i$',offset=-.8);c.ground((0,0));c.wire(n,(4,n.y),(4,4));c.part('R',(2,4),(4,4),r'$R_1=2\,\mathrm{k}\Omega$');c.ground((2,4));c.part('R',(4,4),(4,1.8),r'$R_2=4\,\mathrm{k}\Omega$',offset=-.5);c.wire(o,(12,6));c.part('R',(12,6),(12,3.2),r'$R_3=10\,\mathrm{k}\Omega$');c.part('R',(12,3.2),(12,0),r'$R_4=5\,\mathrm{k}\Omega$');c.ground((12,0));n2,p2,o2=c.op(8,1.8,label='A_2',plus_top=True,reverse=True);c.wire(o2,(4,1.8));c.wire(p2,(11,p2.y),(11,3.2),(12,3.2));c.wire(n2,(11,n2.y),(11,.4),(6,.4),(6,1.8),o2);c.port((12,6),'$u_o$','right');c.dot((12,3.2));c.dot((4,4));c.save()

c=C('F152','opamp MOS output stage',size=(12,8));n,p,o=c.op(4,5,plus_top=True);t=fet(c,9,5,'T');c.part('R',(0,p.y),p,r'$0.4\,\mathrm{k}\Omega$');c.port((0,p.y),'$u_i$');c.wire(n,(3,n.y),(3,2));c.part('R',(3,2),(3,0),r'$0.8\,\mathrm{k}\Omega$');c.ground((3,0));c.wire(o,t.gate);c.part('R',(t.drain.x,9),t.drain,'$R_L$');c.supply((t.drain.x,9),r'$5\,\mathrm{V}$');c.wire(t.source,(t.source.x,2.5));c.part('R',(t.source.x,2.5),(t.source.x,0),r'$0.4\,\mathrm{k}\Omega$');c.port((t.source.x,0),r'$-5\,\mathrm{V}$','right');c.d.add(E.Arrow().at((t.drain.x+.5,7)).to((t.drain.x+.5,6)));c.text(t.drain.x+1,6.5,'$i_o$');c.d.add(E.Line().at((5.3,5.6)).to((5.3,9)));c.d.add(E.Line().at((5.3,4.4)).to((5.3,0)));c.wire((5.3,9),(t.drain.x,9));c.wire((5.3,0),(t.source.x,0));c.dot((t.drain.x,9));c.dot((t.source.x,0));c.save()

# Knowledge figure: voltage-series feedback with the load connected at the output node.
c=C('F187','non-inverting feedback',size=(11,7));n,p,o=c.op(4,5,plus_top=True);c.port((0,p.y),'$u_I$');c.wire((0,p.y),p);c.wire(n,(3,n.y),(3,2));c.part('R',(3,2),(3,0),'$R_1$',offset=-.5);c.ground((3,0));c.part('R',(3,2),(10,2),'$R_2$');c.wire((10,2),(10,5),o);c.wire((10,5),(13,5));c.part('R',(12,5),(12,0),'$R_L$');c.ground((12,0));c.port((13,5),'$u_o$','right');c.dot((3,2));c.dot((10,5));c.dot((12,5));c.text(2.6,3.3,'$u_D$',ha='right');c.text(3.8,1,'$u_F$');c.text(3.8,1.7,'$+$');c.text(3.8,.3,'$-$');c.text(2.6,4.8,'$+$');c.text(2.6,2.9,'$-$');c.save()

# Remaining knowledge diagrams are generated by finish_knowledge.py.
