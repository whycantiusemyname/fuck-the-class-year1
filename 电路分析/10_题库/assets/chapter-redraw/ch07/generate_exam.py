"""Personally transcribed exam figures; no generated bitmap circuitry."""
from pathlib import Path
exec((Path(__file__).with_name('generate.py')).read_text(encoding='utf8').split('# E7-1:')[0])

def inv(key,ri,rf,bias,ci=None,cf=None,ind=None,load=None,ui='u_i',uo='u_o',supply=False):
 c=C(key,key,size=(11,9));n,p,o=op(c,5,4)
 c.port((0,n.y),'$'+ui+'$')
 if ci:
  part(c,'C',(0,n.y),(2,n.y),ci);part(c,'R',(2,n.y),(4,n.y),ri)
 else:part(c,'R',(0,n.y),(4,n.y),ri)
 c.wire((4,n.y),n);c.dot((4,n.y));c.wire((4,n.y),(4,8))
 part(c,'R',(4,8),(10,8),rf);c.wire((10,8),(10,4),o);c.dot((10,4))
 for y,kind,lab in [(10,'C',cf),(12,'L',ind)]:
  if lab:c.wire((4,8),(4,y));part(c,kind,(4,y),(10,y),lab);c.wire((10,y),(10,8));c.dot((4,8));c.dot((10,8))
 grounded(c,p,bias);output(c,o,x=13,label=uo)
 if load:part(c,'R',(11,4),(11,0),load);c.ground((11,0));c.dot((11,4))
 if supply:
  edge=1.25*(1-1/2.165)
  c.wire((6,4+edge),(6,6));c.port((6,6),'$+u_s$','right');c.wire((6,4-edge),(6,2));c.port((6,2),'$-u_s$','right')
 return c

c=inv('F104',r'R=800\,\Omega',r'R_f=8\,\mathrm{k}\Omega',r'R_p=8\,\mathrm{k}\Omega',ci=r'C=2\,\mu\mathrm{F}')
done(c,'原图输入C=2μF串R=800Ω；Rf=8kΩ负反馈、Rp=8kΩ正端接地；所有单位照录。')
for key,load in [('F115',None),('F116','R_L')]:
 c=inv(key,'R_1','R_2','R_3',load=load,ui='v_{in}',uo='v_o');done(c,'R1输入、R2反馈、R3正端接地；'+('RL由输出到地。' if load else '原(a)图无负载，不擅加RL。'))

# An integrator and its GIVEN input/output waveforms are distinct source figures.
c=C('F117','F117',size=(11,8));n,p,o=op(c,5,4);c.port((0,n.y),'$v_i$');part(c,'R',(0,n.y),(4,n.y),'R');c.wire((4,n.y),n);feedback(c,n,o,'C',y=8,xleft=4,xright=10,kind='C');grounded(c,p,'R');output(c,o,label='v_o');done(c,'积分器：输入R、反馈C、同相R接地，v_i/v_o照原图。')
c=C('F118','F118',size=(11,9))
for base,name,amp in [(5,'v_i','1'),(0,'v_o','0.5')]:
 c.d.add(E.Arrow().at((0,base-1.7)).to((0,base+1.8)));c.d.add(E.Arrow().at((-.4,base)).to((9.4,base)));c.text(.1,base+1.75,'$'+name+'$',ha='left');c.text(9.3,base-.35,r'$t/(\mu\mathrm{s})$');c.text(-.25,base-.25,'$0$')
 for y,sgn in [(base+1.2,''),(base-1.2,'-')]:c.text(-.3,y,'$'+sgn+amp+r'\,\mathrm{V}$',ha='right')
c.ax.plot([0,2,2,4,4,6,6,8,8,9],[6.2,6.2,3.8,3.8,6.2,6.2,3.8,3.8,6.2,6.2],color='black',lw=1.65)
c.ax.plot([0,2,4,6,8],[1.2,-1.2,1.2,-1.2,1.2],color='black',lw=1.65)
for x in [2,4,6,8]:c.ax.plot([x,x],[-1.5,6.4],ls='--',lw=1,color='black')
c.text(1.75,4.6,'$0.1$');c.text(3.75,4.6,'$0.2$');done(c,'原题给定上下两波形：输入±1V、输出±0.5V，0.1/0.2μs及反相斜率照录；这是题干条件图，不是代画解答。')

def filter2(key,high=False,res='R',cap=r'0.1\,\mu\mathrm{F}'):
 c=C(key,key,size=(13,10));n,p,o=op(c,8,5)
 c.wire(n,(7,n.y));part(c,'R',(3,n.y),(7,n.y),'R_1');c.ground((3,n.y));feedback(c,n,o,'R_f' if high else 'R_2',y=9,xleft=7,xright=13)
 c.port((0,p.y),'$u_i$')
 series,shunt=('C','R') if high else ('R','C')
 part(c,series,(0,p.y),(3,p.y),cap if high else res);part(c,series,(3,p.y),(6,p.y),cap if high else res);c.wire((6,p.y),p)
 part(c,shunt,(6,p.y),(6,0),res if high else cap);c.ground((6,0));c.dot((6,p.y))
 if high:part(c,'R',(3,p.y),(3,0),res);c.ground((3,0))
 else:part(c,'C',(3,p.y),(3,1),cap);c.wire((3,1),(13,1),(13,5));c.dot((13,5))
 c.dot((3,p.y));output(c,o,x=15);return c
c=filter2('F110');done(c,'低通：两串联R；第一只0.1μF从两R中点接输出，第二只从正输入接地；负端R1接地/R2反馈，未把第一电容误接地。')
c=filter2('F153',res=r'1.6\,\mathrm{k}\Omega',cap='C');done(c,'低通两R均1.6kΩ，两C分别跨接中点到输出/正端到地；R1接地R2负反馈。')
c=filter2('F128',high=True);done(c,'高通两只0.1μF串联；两节点各自R接地，确无输出到第一个中点的反馈支路；R1接地、Rf负反馈。')

def two_caps(key,cross,series,source=False):
 c=C(key,key,size=(12,10));n,p,o=op(c,7,4)
 if source:part(c,'V',(0,0),(0,n.y),'v_i');c.ground((0,0))
 else:c.port((0,n.y),'$u_i$')
 part(c,'R',(0,n.y),(3,n.y),'R_1');c.text(3,n.y-.55,'$v_1$') if source else None
 part(c,'C',(3,n.y),(6,n.y),series);c.wire((6,n.y),n);c.dot((3,n.y));c.dot((6,n.y))
 c.wire((3,n.y),(3,10));part(c,'C',(3,10),(12,10),cross);c.wire((12,10),(12,4),o)
 c.wire((6,n.y),(6,8));part(c,'R',(6,8),(12,8),'R_2');c.dot((12,8));c.dot((12,4));grounded(c,p);output(c,o,x=14,label='v_o' if source else 'u_o')
 if source:c.text(6,n.y-.55,'$v_2$')
 return c
c=two_caps('F120','C_1','C_2',source=True);done(c,'R1后节点v1经C2到负端v2；C1从v1跨到输出，R2从v2反馈输出；正端接地；不能交换C1/C2标号。')
c=two_caps('F171','C_2','C_1');done(c,'R1后节点经C1到负端，C2从R1/C1节点跨到输出；R2负反馈、正端地，与另一年份题的电容编号相反。')
c=inv('F147',r'R=1\,\mathrm{k}\Omega',r'R_f=10\,\mathrm{k}\Omega',r'1\,\mathrm{k}\Omega',cf=r'0.2\,\mu\mathrm{F}');done(c,'1kΩ输入、10kΩ与0.2μF并联反馈、正端1kΩ地；不是串联RC反馈。')
c=inv('F169',r'10\,\mathrm{k}\Omega',r'100\,\mathrm{k}\Omega',r'10\,\mathrm{k}\Omega',cf='C',ui='u_i(t)',uo='u_o(t)',supply=True);done(c,'10kΩ输入/正端接地、100kΩ与C并联反馈，保留±us供电引脚和时间变量。')
c=inv('F174',r'1\,\mathrm{k}\Omega',r'10\,\mathrm{k}\Omega',None,cf=r'0.1\,\mu\mathrm{F}',ind=r'1\,\mathrm{mH}');done(c,'输入1kΩ；反馈10kΩ、0.1μF、1mH三支路并联，正端直接地；三个反馈元件均保留。')

c=C('F162','F162',size=(11,8));n,p,o=op(c,6,5,plus_top=True);part(c,'V',(0,0),(0,p.y),'v_i');c.ground((0,0));part(c,'C',(0,p.y),(4,p.y),'C');c.wire((4,p.y),p);part(c,'R',(4,p.y),(4,0),'R');c.ground((4,0));c.dot((4,p.y));c.wire(n,(5,n.y));part(c,'R',(5,2.8),(5,0),'R_1',offset=.5);c.ground((5,0));c.wire((5,n.y),(5,2.8));part(c,'R',(5,2.8),(11,2.8),'R_2');c.wire((11,2.8),(11,5),o);c.dot((5,n.y));c.dot((5,2.8));c.dot((11,5));output(c,o,x=13,label='v_o');done(c,'C串接同相输入、R并地；R1从负端到地、R2回输出；源电压正上负下，不能误画反相高通。')

c=C('F177','F177',size=(11,8));n,p,o=op(c,5,4);c.wire(n,(4,n.y));part(c,'R',(0,n.y),(4,n.y),'R_1');c.ground((0,n.y));feedback(c,n,o,'R_f',y=8,xleft=4,xright=10);c.port((0,p.y),'$v_i$');part(c,'R',(0,p.y),p,'R_3');output(c,o,label='v_o');done(c,'同相放大：R1负端接地、Rf反馈、vi经R3到正端；按原图R3而非擅改R2。')

c=C('F182','F182',size=(12,9));n,p,o=op(c,5,6,plus_top=True);part(c,'AC',(0,0),(0,p.y),'v_i');c.ground((0,0));c.wire((0,p.y),p);c.wire(o,(10,6));part(c,'R',(10,6),(10,3),'R_1');part(c,'R',(10,3),(10,0),'R_2');c.ground((10,0));c.wire(n,(4,n.y),(4,3),(10,3));c.dot((10,3));c.dot((10,6));part(c,'R',(13,6),(13,0),'R_L');c.wire((10,6),(15,6));c.wire((0,0),(15,0));c.dot((13,6));c.dot((13,0));c.port((15,6),'$+$','right');c.port((15,0),'$-$','right');c.text(16.5,3,'$v_o$');done(c,'vi交流源接同相；负端取R1/R2中点；RL跨输出和公共地，不与R1/R2串联；输出极性保留。')

(HERE/'exam-geometry.json').write_text(json.dumps(M.records,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(HERE/'qa-exam.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
