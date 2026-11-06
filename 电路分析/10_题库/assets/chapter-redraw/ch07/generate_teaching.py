"""Teaching schematics, reconstructed by the main agent from current references."""
from pathlib import Path
exec((Path(__file__).with_name('generate.py')).read_text(encoding='utf8').split('# E7-1:')[0])
from matplotlib.patches import Rectangle

c=C('F006','OP symbol',size=(10,7));n,p,o=op(c,4,4);c.port((0,n.y),'$u_n$');c.wire((0,n.y),n);c.port((0,p.y),'$u_p$');c.wire((0,p.y),p);c.wire(o,(10,4));c.port((10,4),'$u_o$','right');edge=1.25*(1-1/2.165);c.wire((5,4+edge),(5,7));c.supply((5,7),'$+V_{CC}$');c.wire((5,4-edge),(5,1));c.port((5,1));c.text(5,.4,'$-V_{CC}$');done(c,'同一符号上负下正，un/up/uo和±VCC照原矢量图；电源脚与三角形边界相接，字形统一STIX。')
c=C('F007','OP transfer',size=(10,7));c.d.add(E.Arrow().at((-5,0)).to((5.2,0)));c.d.add(E.Arrow().at((0,-3.6)).to((0,3.8)));c.ax.plot([-4.5,-1.5,1.5,4.5],[-3,-3,3,3],color='black',lw=1.65);c.text(5,-.4,'$u_p-u_n$',ha='right');c.text(-.25,3.65,'$u_o$',ha='right');c.text(-.25,3,'$+U_{om}$',ha='right');c.text(-.25,-3,'$-U_{om}$',ha='right');done(c,'开环定性传输保留正斜率线性段和±Uom饱和，不增加数值刻度；输入差明确up-un。')

c=C('F188','运放五部分',size=(15,8))
def block(x,y,w,h,label):c.ax.add_patch(Rectangle((x,y),w,h,fill=False,lw=1.65,color='black'));c.text(x+w/2,y+h/2,label,size=18)
def arrow(a,b):c.ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','lw':1.65,'color':'black'},annotation_clip=False)
block(1,4,2,3,'输入级');block(6,4,2,3,'中间级');block(11,4,2,3,'输出级');block(1,0,4,1.5,'偏置电路');block(9,0,4,1.5,'保护电路')
arrow((-3,6),(1,6));arrow((-3,5),(1,5));c.text(-3.2,6,'同相输入端 +',ha='right');c.text(-3.2,5,'反相输入端 −',ha='right');arrow((3,5.5),(6,5.5));arrow((8,5.5),(11,5.5));arrow((13,5.5),(16,5.5));c.text(16.2,5.5,'输出端',ha='left');arrow((5,.75),(9,.75));arrow((2,1.5),(2,4));arrow((4,1.5),(4,3));arrow((4,3),(7,3));arrow((7,3),(7,4));arrow((11,1.5),(12,4))
arrow((2,-2),(2,0));arrow((4,-2),(4,0));c.text(2,-2.4,'$-U_S$');c.text(4,-2.4,'$+U_S$');c.text(3,-3.2,'直流电源');c.ax.add_patch(Rectangle((.1,-.5),13.7,8.3,fill=False,lw=1.25,ls='--',color='black'));c.ax.set_xlim(-8,19);c.ax.set_ylim(-4,9);done(c,'保留输入/中间/输出/偏置/保护五部分；同相/反相输入和双电源±US、偏置与保护连向，改为黑白线型且不依赖底色。')

c=C('F189-a','T反馈原电路',size=(12,10));n,p,o=op(c,5,4);c.port((0,n.y),'$u_I$');part(c,'R',(0,n.y),(4,n.y),'R_1');c.wire((4,n.y),n);c.wire((4,n.y),(4,9));part(c,'R',(4,9),(8,9),'R_2');part(c,'R',(8,9),(12,9),'R_4');c.wire((12,9),(12,4),o);part(c,'R',(8,9),(8,6.8),'R_3',offset=-.5);c.ground((8,6.8));grounded(c,p,'R_5');output(c,o,x=14,label='u_O');c.dot((4,n.y));c.dot((8,9));c.dot((12,4));c.text(3.5,n.y-.4,'$N$');c.text(8,9.5,'$M$');c.text(4.5,p.y-.35,'$P$')
for a,b,x,y,label in [((.8,5.5),(2.4,5.5),1.6,6,'i_1'),((4.8,8.2),(6.2,8.2),5.5,7.7,'i_2'),((8.6,10.2),(10.2,10.2),9.4,10.7,'i_4'),((8.8,8.4),(8.8,7),9.4,7,'i_3')]:c.d.add(E.Arrow().at(a).to(b));c.text(x,y,'$'+label+'$',size=14)
c.save()
c=C('F189-b','T反馈等效网络',size=(12,10));c.port((0,4),'$u_I$');part(c,'R',(0,4),(4,4),'R_1');c.dot((4,4));c.wire((4,4),(4,9));part(c,'R',(4,9),(8,9),'R_2');part(c,'R',(8,9),(12,9),'R_4');c.wire((12,9),(12,4),(14,4));c.port((14,4),'$u_O$','right');part(c,'R',(8,9),(8,6.8),'R_3',offset=-.5);c.ground((8,6.8));c.dot((8,9));c.port((4,2));part(c,'R',(4,2),(4,0),'R_5');c.ground((4,0));c.text(4.5,4,'$N$');c.text(4.5,2,'$P$');c.text(8,9.5,'$M$');c.ax.annotate('',xy=(4,3.8),xytext=(4,2.2),arrowprops={'arrowstyle':'<->','lw':1.2,'linestyle':'--'});c.text(7,3,'$u_P=u_N$');c.text(7,1.5,'虚断、虚短',size=17);c.save();panels('F189',['F189-a','F189-b'],['(a)','(b)']);QA['F189']='原电路及右侧虚短/虚断等效均重绘：R1输入、R2/R4反馈串接，中点M经R3地，正端P经R5地；等效P/N之间只画虚线关系，不画物理短线。'

c=C('F190','函数变换与微分',size=(13,13));n1,p1,o1=op(c,4,3,'A_1',plus_top=True);n2,p2,o2=c.op(4,11,label='A_2',reverse=True)
c.port((0,p1.y),'$u_I$');part(c,'R',(0,p1.y),(3,p1.y),'R_1');c.wire((3,p1.y),p1);c.dot((3,p1.y));part(c,'R',(3,p1.y),(3,7),'R_2',offset=.5);c.port((3,7),'$u_{O2}$');grounded(c,n1,'R_4');c.wire(o1,(12,3));c.port((12,3),'$u_O$','right')
c.wire(n2,(8,n2.y));part(c,'R',(8,n2.y),(12,n2.y),'R_3');c.port((12,n2.y),'$u_O$','right');c.wire(n2,(7,n2.y),(7,15));part(c,'C',(o2.x,15),(7,15),'C',offset=-.4);c.wire((o2.x,15),(o2.x,11),o2);c.dot((7,n2.y));c.dot(o2);c.text(3.9,11,'$u_{O2}$',ha='right');c.wire(p2,(8,p2.y));part(c,'R',(8,p2.y),(8,8),'R_5');c.ground((8,8))
for a,b,x,y,lab in [((1,4.5),(2.2,4.5),1.6,4.95,'i_{R1}'),((2.2,4.8),(2.2,6),1.4,6.1,'i_{R2}'),((11,12.5),(9,12.5),10,13,'i_{R3}'),((6.8,15.6),(5.2,15.6),6,16.1,'i_C')]:c.d.add(E.Arrow().at(a).to(b));c.text(x,y,'$'+lab+'$',size=14)
for x,y1,y2 in [(3,7.4,10.6),(12,3.4,n2.y-.4)]:c.ax.annotate('',xy=(x,y2),xytext=(x,y1),arrowprops={'arrowstyle':'<->','linestyle':'--','lw':1.15})
c.text(3.5,p1.y-.4,'$P_1$',size=14);c.text(3.5,n1.y+.3,'$N_1$',size=14);c.text(7,n2.y-.4,'$N_2$',size=14);c.text(7,p2.y+.3,'$P_2$',size=14);done(c,'照图分置A2朝左、A1朝右；A2负端R3输入/C反馈/正端R5地，A1正端R1输入/R2到标为uO2的开口端、负端R4地；虚线是电压对应箭头，未补为实导线。')

(HERE/'teaching-geometry.json').write_text(json.dumps(M.records,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(HERE/'qa-teaching.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
