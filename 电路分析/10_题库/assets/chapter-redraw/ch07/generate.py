"""Main-agent redraws, checked against the actual question figures. Run generate.py."""
from pathlib import Path
import sys,json,math
from PIL import Image,ImageDraw,ImageFont
from matplotlib.font_manager import findfont
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent))
import common as M
from panels import combine
import fitz
M.OUT=HERE;C=M.Circuit;E=M.E
QA={}
def part(c,k,a,b,label=None,**kw):c.part(k,a,b,'$'+label+'$' if label else None,**kw)
def op(c,x,y,name='A',plus_top=False):return c.op(x,y,label=name,plus_top=plus_top)
def output(c,o,x=12,label='u_o',negative=True):
 c.wire(o,(x,o.y));c.port((x,o.y),'$+$','right')
 if negative:c.port((x,0),'$-$','right');c.ground((x,0));c.text(x+1.5,o.y/2,'$'+label+'$')
 else:c.text(x+.6,o.y,'$'+label+'$',ha='left')
def feedback(c,n,o,label='R_F',y=8,xleft=None,xright=10,kind='R'):
 left=n.x-1 if xleft is None else xleft
 c.wire(n,(left,n.y),(left,y));part(c,kind,(left,y),(xright,y),label);c.wire((xright,y),(xright,o.y),o);c.dot((left,n.y));c.dot((xright,o.y));return left,xright
def grounded(c,p,label=None,x=None):
 if x is not None:c.wire(p,(x,p.y));p=(x,p.y)
 if label:part(c,'R',p,(p[0],0),label,offset=-.5)
 else:c.wire(p,(p[0],0))
 c.ground((p[0],0))
def done(c,note):c.save(note=note);QA[c.key]=note
def panels(key,ids,labels):
 combine(HERE,key,ids,labels)
 images=[Image.open(HERE/(x+'.png')).convert('RGB') for x in ids];w=max(i.width for i in images);canvas=Image.new('RGB',(w,sum(i.height+70 for i in images)),'white');d=ImageDraw.Draw(canvas);font=ImageFont.truetype(findfont('STIXGeneral'),40);y=0
 for im,label in zip(images,labels):
  canvas.paste(im,((w-im.width)//2,y));d.text((w/2,y+im.height+5),label,anchor='mt',font=font,fill='black');y+=im.height+70
 canvas.save(HERE/(key+'.png'))
def limiter(c,x,top=4,bottom=0,label=r'\pm U_Z'):
 mid=(top+bottom)/2;part(c,'Z',(x,top),(x,mid));part(c,'Z',(x,mid),(x,bottom),reverse=True);c.ground((x,bottom));c.text(x+.7,mid,'$'+label+'$',ha='left');c.dot((x,top))

# E7-1: neither circuit is simplified or solved; preserve the two input resistor roles.
for suffix in ['a','b']:
 c=C('F052-'+suffix,'E7-1',size=(10,7));n,p,o=op(c,5,4)
 if suffix=='a':
  c.port((0,n.y),'$u_1$');part(c,'R',(0,n.y),(4,n.y),'R_1');c.wire((4,n.y),n);grounded(c,p,'R_2')
 else:
  c.port((0,p.y),'$u_1$');part(c,'R',(0,p.y),p,'R_2');c.wire(n,(4,n.y));part(c,'R',(0,n.y),(4,n.y),'R_1');c.ground((0,n.y))
 feedback(c,n,o,'R_F',y=7,xleft=4,xright=10);output(c,o);done(c,'R1/R2/RF roles, upper inverting and lower noninverting inputs, grounded bias branch and feedback connections checked against source.')
panels('F052',['F052-a','F052-b'],['(a)','(b)']);QA['F052']='两幅分别为反相与同相放大；保留R1/R2输入和接地角色、RF反馈、u1/uo及正负输入方向。'

# E7-2: inverting first stage and noninverting second stage.
c=C('F053','E7-2',size=(16,8));n1,p1,o1=op(c,4,4,'A_1');n2,p2,o2=op(c,13,4,'A_2')
c.port((0,n1.y),'$u_1$');part(c,'R',(0,n1.y),(3,n1.y),'R_1');c.wire((3,n1.y),n1);grounded(c,p1,'R_2');feedback(c,n1,o1,'R_{F1}',y=8,xleft=3,xright=8)
part(c,'R',(8,p2.y),(12,p2.y),'R_3');c.wire(o1,(8,o1.y),(8,p2.y));c.wire((12,p2.y),p2);c.dot((12,p2.y));grounded(c,(12,p2.y),'R_4')
c.wire(n2,(11,n2.y));part(c,'R',(11,n2.y),(11,8),'R_{F2}',offset=-.5);c.wire((11,8),(18,8),(18,o2.y),o2);c.dot((18,o2.y));output(c,o2,x=20)
done(c,'A1反相输入R1、RF1反馈、正端R2接地；A1输出经R3到A2正端并由R4接地；A2负端仅经RF2回输出，保留原题无下分压电阻的结构。')

# E7-3: the three input resistors share only the inverting summing node.
c=C('F054','E7-3',size=(11,9));n,p,o=op(c,5,3)
for index,y in [(11,7),(12,5.4),(13,n.y)]:
 c.port((0,y),'$u_{'+str(index)+'}$');part(c,'R',(0,y),(3,y),'R_{'+str(index)+'}');c.wire((3,y),(3,n.y));c.dot((3,y))
c.wire((3,n.y),n);feedback(c,n,o,'R_F',y=9,xleft=3,xright=10);grounded(c,p,'R_2');output(c,o,x=12)
done(c,'u11/u12/u13分别经R11/R12/R13共接反相汇流节点；RF从该节点反馈输出；正端R2接地，未合并任何元件。')

# E7-4: the load measures the current from the noninverting node to ground.
c=C('F055','E7-4',size=(11,8));n,p,o=op(c,5,4)
c.port((0,n.y),'$u_{11}$');part(c,'R',(0,n.y),(4,n.y),'R_1');c.wire((4,n.y),n);feedback(c,n,o,'R_2',y=8,xleft=4,xright=10)
c.port((0,p.y),'$u_{12}$');part(c,'R',(0,p.y),(3,p.y),'R_3');c.wire((3,p.y),p);c.dot((3,p.y))
part(c,'R',(3,p.y),(3,0),'R_L',offset=-.5);c.ground((3,0));c.wire((3,p.y),(4,p.y),(4,-1));part(c,'R',(4,-1),(10,-1),'R_4');c.wire((10,-1),(10,4));c.dot((10,4))
c.d.add(E.Arrow().at((.9,2)).to((.9,.8)));c.text(.25,1.4,'$I_L$');output(c,o,x=12)
done(c,'R1/R2接反相输入与输出；R3接u12到正端，正端另经R4接输出并经RL接地；IL向下，反馈下行线独立绕开RL本体。')

# E7-5: two T networks. The alpha branch crosses the output without a junction.
c=C('F056','E7-5',size=(13,9));n,p,o=op(c,5,4)
for point,label in [(n,'u_{11}'),(p,'u_{12}')]:
 c.port((0,point.y),'$'+label+'$');part(c,'R',(0,point.y),(4,point.y),'R_1');c.wire((4,point.y),point);c.dot((4,point.y))
c.wire((4,n.y),(4,8));part(c,'R',(4,8),(9,8),'R_2');part(c,'R',(9,8),(12,8),'R_2');c.wire((12,8),(12,o.y),o);c.dot((12,o.y));c.dot((9,8));c.text(9.3,8.4,'$a$',size=15)
part(c,'R',(9,8),(9,5.5),r'\alpha R_2',offset=-.5);c.wire((9,5.5),(9,4.2));c.ax.add_patch(M.plt.matplotlib.patches.Arc((9,4),.4,.4,theta1=-90,theta2=90,lw=1.65,color='black'));c.wire((9,3.8),(9,1))
c.wire((4,p.y),(4,1));part(c,'R',(4,1),(9,1),'R_2');part(c,'R',(9,1),(12,1),'R_2');c.ground((12,1));c.dot((9,1));c.text(9.3,.6,'$b$',size=15);output(c,o,x=14)
done(c,'两输入各经R1到对应端；上、下各有两只R2构成T支路，a-b间为αR2；a到输出经R2，b右侧R2接地；α支路跨输出线不连接。')

# E7-6: potentiometer load with its wiper returned to the output.
c=C('F057','E7-6',size=(11,7));n,p,o=op(c,5,4)
c.port((0,n.y),'$u_1$');part(c,'R',(0,n.y),(4,n.y),'R_1');c.wire((4,n.y),n);grounded(c,p,'R_2');feedback(c,n,o,'R_F',y=7,xleft=4,xright=10)
part(c,'R',(10,4),(10,0),'R_P');c.ground((10,0));c.wire((10,4),(8.5,4),(8.5,2));c.d.add(E.Arrow().at((8.5,2)).to((9.75,2)));c.dot((10,4));output(c,o)
done(c,'反相R1/RF与正端R2接地；RP负载接地，滑臂返回输出端，未将负载误作输入电阻。')

# E7-7: three voltage followers feed the weighted average node.
c=C('F058','E7-7',size=(18,12))
for i,y in enumerate([12,7,2],1):
 n,p,o=op(c,3,y,'A_'+str(i));c.port((0,p.y),'$u_'+str(i)+'$');c.wire((0,p.y),p);c.wire(n,(2,n.y),(2,y+2),(7,y+2),(7,y),o);c.dot((7,y));part(c,'R',(7,y),(11,y),'3R');c.dot((11,y))
c.wire((11,2),(11,12));part(c,'R',(11,2),(11,0),'30R');c.ground((11,0));c.text(11.7,7.5,'$u_A$')
n,p,o=op(c,16,7,'A_4');c.wire((11,7),(13,7),(13,p.y),p);c.wire(n,(15,n.y),(15,11));part(c,'R',(15,11),(22,11),'30R');c.wire((22,11),(22,7),o);c.dot((22,7));part(c,'R',(15,9),(12,9),'R');c.ground((12,9));c.dot((15,9));output(c,o,x=24)
done(c,'A1/A2/A3均为电压跟随；三路输出各经3R汇于uA，uA经30R接地后送A4正端；A4负端经R到地、30R回输出，所有输出端实际连线。')

# E7-8: inverting summer followed by a second mixed-input stage.
c=C('F059','E7-8',size=(17,10));n1,p1,o1=op(c,4,8,'A_1');n2,p2,o2=op(c,15,8,'A_2')
for y,u,r in [(10.5,'u_1','R_1'),(n1.y,'u_2','R_2')]:
 c.port((0,y),'$'+u+'$');part(c,'R',(0,y),(2.5,y),r);c.wire((2.5,y),(2.5,n1.y));c.dot((2.5,y))
c.wire((2.5,n1.y),n1);feedback(c,n1,o1,'R_3',y=12,xleft=2.5,xright=8);part(c,'R',p1,(p1.x,4),'R',offset=-.5);c.ground((p1.x,4));c.text(8.5,8.5,'$u_{o1}$')
c.wire((8,8),(10,8));part(c,'R',(10,8),(13,8),'R_4');c.wire((13,8),(13,n2.y),n2);feedback(c,n2,o2,'R_5',y=12,xleft=14,xright=20)
for y,u,r in [(5.4,'u_3','R_6'),(3.4,'u_4','R_7')]:
 c.port((9,y),'$'+u+'$');part(c,'R',(9,y),(13,y),r);c.wire((13,y),(13,p2.y));c.dot((13,y))
c.wire((13,p2.y),p2);output(c,o2,x=22)
done(c,'第一级u1/R1与u2/R2反相汇流、R3反馈、正端R接地；uo1经R4入第二级负端，R5反馈；u3/R6和u4/R7共接第二级正端，未添加接地电阻。')

# E7-9: T-shaped feedback has its centre resistor R4 connected to ground.
c=C('F060','E7-9',size=(12,8));n,p,o=op(c,5,4)
c.port((0,n.y),'$u_1$');part(c,'R',(0,n.y),(4,n.y),'R_1');c.wire((4,n.y),n);c.wire((4,n.y),(4,8));c.dot((4,n.y));part(c,'R',(4,8),(8,8),'R_2');part(c,'R',(8,8),(12,8),'R_3');c.wire((12,8),(12,4),o);part(c,'R',(8,8),(8,5.7),'R_4');c.ground((8,5.7));c.dot((8,8));c.dot((12,4));grounded(c,p,'R');output(c,o,x=14)
done(c,'输入R1、反相反馈R2/R3串联，其中点经R4接地；正端经R到地，R4未误接正端或输出。')

# E7-10: all source millivolt values and resistor values remain given data.
c=C('F061','E7-10',size=(20,14));n1,p1,o1=op(c,4,12,'A_1');n2,p2,o2=op(c,4,4,'A_2',plus_top=True);n3,p3,o3=op(c,16,8,'A_3')
for y,val,ohms in [(14.5,'5','6'),(n1.y,'-5','4')]:
 c.port((0,y),'$'+val+r'\,\mathrm{mV}$');part(c,'R',(0,y),(2,y),ohms+r'\,\mathrm{k}\Omega');c.wire((2,y),(2,n1.y));c.dot((2,y))
c.wire((2,n1.y),n1);feedback(c,n1,o1,r'24\,\mathrm{k}\Omega',y=16,xleft=2,xright=8);part(c,'R',p1,(p1.x,9),r'2.2\,\mathrm{k}\Omega',offset=-.5);c.ground((p1.x,9))
c.port((0,p2.y),r'$-6\,\mathrm{mV}$');part(c,'R',(0,p2.y),(3,p2.y),r'6\,\mathrm{k}\Omega');c.wire((3,p2.y),p2);c.dot((3,p2.y))
c.wire((3,p2.y),(3,n2.y+.2));c.ax.add_patch(M.plt.matplotlib.patches.Arc((3,n2.y),.4,.4,theta1=-90,theta2=90,lw=1.65,color='black'));c.wire((3,n2.y-.2),(3,2.7));part(c,'R',(3,2.7),(3,0),r'6\,\mathrm{k}\Omega',offset=.5);c.ground((3,0))
c.port((0,1),r'$6\,\mathrm{mV}$');part(c,'R',(0,1),(2.5,1),r'6\,\mathrm{k}\Omega');c.wire((2.5,1),(2.5,n2.y),n2);c.dot((2.5,n2.y));c.wire((2.5,n2.y),(2.5,-1),(10,-1),(10,1.8),(8,1.8));c.dot((8,1.8))
c.wire(o2,(8,4));part(c,'R',(8,4),(8,1.8),r'4\,\mathrm{k}\Omega',offset=.5);part(c,'R',(8,1.8),(8,0),r'6\,\mathrm{k}\Omega',offset=.5);c.ground((8,0));c.dot((8,4))
part(c,'R',(8,12),(13,12),r'12\,\mathrm{k}\Omega');c.wire((13,12),(13,n3.y),n3);feedback(c,n3,o3,r'6\,\mathrm{k}\Omega',y=14,xleft=15,xright=23)
part(c,'R',(8,4),(13,4),r'12\,\mathrm{k}\Omega');c.wire((13,4),(13,p3.y),p3);part(c,'R',(13,4),(13,0),r'6\,\mathrm{k}\Omega');c.ground((13,0));c.dot((13,4));output(c,o3,x=25)
done(c,'A1输入5mV/6k和−5mV/4k、反馈24k、正端2.2k接地；A2正端−6mV经6k及6k接地，负端+6mV经6k并接4k/6k反馈分压；末级两路12k、负反馈6k及正端6k接地，所有给定数值照录。')

# E7-11: a differential output, with neither output terminal grounded.
c=C('F062','E7-11',size=(12,11));n1,p1,o1=op(c,4,9,'A_1',plus_top=True);n2,p2,o2=op(c,4,3,'A_2')
c.port((0,p1.y),'$u_1$');c.wire((0,p1.y),p1);c.port((0,p2.y),'$u_2$');c.wire((0,p2.y),p2)
c.wire(o1,(10,9));part(c,'R',(10,9),(10,7),'R_1');part(c,'R',(10,7),(10,5),'R_2');part(c,'R',(10,5),(10,3),'R_3');c.wire((10,3),o2)
c.wire(n1,(3,n1.y),(3,7),(10,7));c.wire(n2,(3,n2.y),(3,5),(10,5));c.dot((10,7));c.dot((10,5));c.dot((10,9));c.dot((10,3))
c.wire((10,9),(13,9));c.wire((10,3),(13,3));c.port((13,9),'$+$','right');c.port((13,3),'$-$','right');c.text(14.5,6,'$u_o$')
done(c,'A1正端接u1、A2正端接u2；R1/R2/R3串接两个输出，两个反相端分别取R1/R2与R2/R3节点；uo跨两个输出，绝不把负输出接地。')

# E7-12: retain the cR1/bR1/dR1 labels and variable middle resistor.
c=C('F063','E7-12',size=(19,11));n1,p1,o1=op(c,4,10,'A_1',plus_top=True);n2,p2,o2=op(c,4,3,'A_2');n3,p3,o3=op(c,18,6,'A_3')
c.port((0,p1.y),'$u_1$');c.wire((0,p1.y),p1);c.port((0,p2.y),'$u_2$');c.wire((0,p2.y),p2)
c.wire(o1,(10,10));c.wire(o2,(10,3));part(c,'R',(10,10),(10,8),'cR_1');part(c,'R',(10,8),(10,5),'bR_1',offset=.7);part(c,'R',(10,5),(10,3),'dR_1');c.d.add(E.Arrow().at((9.5,6)).to((10.5,7)))
c.wire(n1,(3,n1.y),(3,8),(10,8));c.wire(n2,(3,n2.y),(3,5),(10,5));c.dot((10,8));c.dot((10,5));c.dot((10,10));c.dot((10,3))
c.wire((10,10),(12,10));part(c,'R',(12,10),(16,10),'R_2');c.wire((16,10),(16,n3.y),n3);feedback(c,n3,o3,'aR_2',y=13,xleft=17,xright=25)
c.wire((10,3),(12,3));part(c,'R',(12,3),(16,3),'R_3');c.wire((16,3),(16,p3.y),p3);part(c,'R',(16,3),(16,0),'aR_3');c.ground((16,0));c.dot((16,3));output(c,o3,x=27)
done(c,'前级R1分段标号确为cR1、bR1、dR1，中段可调；两反相端分别取分段节点；末级上路R2/aR2、下路R3/aR3接地，保留原题参数字母。')

# E7-13: differential integrator, including the shunt capacitor on the positive input.
c=C('F064','E7-13',size=(11,8));n,p,o=op(c,5,4)
c.port((0,n.y),'$u_{11}$');part(c,'R',(0,n.y),(4,n.y),'R');c.wire((4,n.y),n);feedback(c,n,o,'C',y=8,xleft=4,xright=10,kind='C')
c.port((0,p.y),'$u_{12}$');part(c,'R',(0,p.y),(3,p.y),'R');c.wire((3,p.y),p);part(c,'C',(3,p.y),(3,0),'C');c.dot((3,p.y));c.wire((0,0),(12,0));c.ground((3,0));output(c,o)
done(c,'u11经R入反相端、C反馈；u12经R入同相端、C到公共下轨；两输入负参考端与输出负端同轨，未对调正负输入。')

# E7-14: circuit and the given qualitative rectangular input, without adding an answer waveform.
c=C('F065-a','E7-14(a)',size=(10,7));n,p,o=op(c,5,4);c.port((0,n.y),'$u_1$');part(c,'C',(0,n.y),(4,n.y),'C');c.wire((4,n.y),n);feedback(c,n,o,'R',y=7,xleft=4,xright=10);grounded(c,p,'R');output(c,o);c.save()
c=C('F065-b','E7-14(b)',size=(10,4));c.d.add(E.Arrow().at((0,-.35)).to((0,3)));c.d.add(E.Arrow().at((-.5,0)).to((9.5,0)));c.ax.plot([0,1,1,4,4,7,7,9],[0,0,2,2,0,0,2,2],color='black',lw=1.65);c.text(-.3,-.3,'$0$');c.text(-.35,2.8,'$u_1$');c.text(9.35,-.3,'$t$')
for a,b,label in [(1,4,'T_1'),(4,7,'T_2')]:
 c.ax.annotate('',xy=(b,1.05),xytext=(a,1.05),arrowprops={'arrowstyle':'<->','lw':1.15},annotation_clip=False);c.text((a+b)/2,.65,'$'+label+'$')
c.save();panels('F065',['F065-a','F065-b'],['(a)','(b)']);QA['F065']='电路为输入C、反馈R、正端R接地；输入矩形波仅标T1/T2及0、u1、t，无虚构幅值/周期，也不添加输出答案波形。'

# E7-15: differentiating stage followed by an integrating stage.
c=C('F066','E7-15',size=(16,8));n1,p1,o1=op(c,4,5,'A_1');n2,p2,o2=op(c,13,5,'A_2')
c.port((0,n1.y),'$u_1$');part(c,'C',(0,n1.y),(3,n1.y),'C');c.wire((3,n1.y),n1);feedback(c,n1,o1,'R_1',y=8,xleft=3,xright=8);grounded(c,p1,'R_2')
c.wire((8,5),(10,5));part(c,'R',(10,5),(12,5),'R_1');c.wire((12,5),(12,n2.y),n2);feedback(c,n2,o2,'C',y=9,xleft=12,xright=18,kind='C');grounded(c,p2,'R_2');output(c,o2,x=20)
done(c,'第一级输入C、反馈R1，第二级输入R1、反馈C；两级正端均R2接地，级间没有额外旁路或短接。')

# E7-16: differential first stage followed by series RF-C feedback.
c=C('F067','E7-16',size=(17,9));n1,p1,o1=op(c,4,5,'A_1');n2,p2,o2=op(c,14,5,'A_2')
for a,u in [(n1,'u_{11}'),(p1,'u_{12}')]:c.port((0,a.y),'$'+u+'$');part(c,'R',(0,a.y),(3,a.y),'R_1');c.wire((3,a.y),a)
feedback(c,n1,o1,'R_2',y=9,xleft=3,xright=8);grounded(c,(3,p1.y),'R_2');c.dot((3,p1.y));part(c,'R',(8,5),(12,5),'R_3');c.wire((12,5),(12,n2.y),n2)
c.wire(n2,(13,n2.y),(13,9));part(c,'R',(13,9),(17,9),'R_F');part(c,'C',(17,9),(20,9),'C');c.wire((20,9),(20,5),o2);c.dot((20,5));grounded(c,p2,'R_4');c.wire((0,0),(22,0));output(c,o2,x=22)
done(c,'差分级两输入R1、负反馈R2和正端R2接地；后级R3输入，RF与C串联反馈，正端R4到公共下轨；未将串联反馈误画并联。')

# E7-17: two inverting inputs plus an independently driven noninverting input.
c=C('F068','E7-17',size=(18,11));n1,p1,o1=op(c,5,6,'A_1');n2,p2,o2=op(c,16,6,'A_2')
for y,u in [(10,'u_{11}'),(n1.y,'u_{12}')]:c.port((0,y),'$'+u+'$');part(c,'R',(0,y),(3,y),'R_1');c.wire((3,y),(3,n1.y));c.dot((3,y))
c.wire((3,n1.y),n1);feedback(c,n1,o1,'R_2',y=12,xleft=3,xright=10);c.port((0,p1.y),'$u_{13}$');part(c,'R',(0,p1.y),p1,'R_3')
part(c,'R',(10,6),(14,6),'R_4');c.wire((14,6),(14,n2.y),n2);feedback(c,n2,o2,'C',y=10,xleft=15,xright=22,kind='C');grounded(c,p2,'R_5');c.wire((0,0),(24,0));output(c,o2,x=24)
done(c,'u11/u12各经R1共接第一负端，R2反馈；u13经R3接正端且无额外接地电阻；R4接第二负端、C反馈、正端R5接公共下轨。')

# E7-18: the transfer curve is given source data, not a newly solved answer.
c=C('F069-a','E7-18(a)',size=(12,8));n,p,o=op(c,5,4);c.port((0,n.y),'$u_1$');part(c,'R',(0,n.y),(4,n.y),'R_1');c.wire((4,n.y),n);feedback(c,n,o,'R_2',y=8,xleft=4,xright=9);grounded(c,p,'R_3');part(c,'R',(9,4),(12,4),'R_4');limiter(c,12);c.wire((12,4),(14,4));c.port((14,4),'$+$','right');c.port((14,0),'$-$','right');c.ground((14,0));c.text(15.5,2,'$u_o$');c.save()
c=C('F069-b','E7-18(b)',size=(9,6));c.d.add(E.Arrow().at((-4.5,0)).to((4.8,0)));c.d.add(E.Arrow().at((0,-3.6)).to((0,3.8)));c.ax.plot([-4,-2,2,4],[-3,-3,3,3],color='black',lw=1.65)
for x,y,lab in [(2,3,'4'),(-2,-3,'-4')]:
 c.ax.plot([x,x],[0,y],color='black',ls='--',lw=1);c.ax.plot([0,x],[y,y],color='black',ls='--',lw=1);c.text(x,-.35,'$'+lab+'$');c.text(-.45,y,'$+12$' if y>0 else '$-12$',ha='right')
c.text(-.3,-.3,'$0$');c.text(4.65,-.4,r'$u_1/\mathrm{V}$');c.text(.25,3.6,r'$u_o/\mathrm{V}$',ha='left');c.save();panels('F069',['F069-a','F069-b'],['(a)','(b)']);QA['F069']='电路R1/R2/R3/R4与输出双向稳压限幅照录；原给定传输图保留±12V饱和及±4V输入拐点，未据曲线反填图中未知电阻值。'

# E7-19: two limiter stages and the given sinusoidal input.
c=C('F070-a','E7-19(a)',size=(19,9));n1,p1,o1=op(c,5,6,'A_1');n2,p2,o2=op(c,15,6,'A_2')
c.port((0,n1.y),'$u_i$');part(c,'R',(0,n1.y),(4,n1.y),'R_1');c.wire((4,n1.y),n1);grounded(c,p1,'R_2');c.wire((4,n1.y),(4,10));part(c,'Z',(4,10),(7,10));part(c,'Z',(7,10),(10,10),reverse=True);c.text(7,10.7,'$U_{Z1}$');c.wire((10,10),(10,6),o1);c.dot((4,n1.y));c.dot((10,6));c.text(10.5,6.5,'$u_{o1}$')
c.wire((10,6),(13,6),(13,n2.y),n2);c.wire(p2,(14,p2.y),(14,3));part(c,'R',(14,3),(14,0),'R_3',offset=-.5);c.ground((14,0));part(c,'R',(14,3),(22,3),'R_4');c.wire((22,3),(22,6));c.dot((14,3));part(c,'R',o2,(22,6),'R_5');c.wire((22,6),(24,6));limiter(c,24,top=6,label='U_{Z2}');c.wire((0,0),(26,0));c.wire((24,6),(26,6));c.port((26,6),'$+$','right');c.port((26,0),'$-$','right');c.text(27.4,3,'$u_{o2}$');c.save()
c=C('F070-b','E7-19(b)',size=(10,4));c.d.add(E.Arrow().at((-.3,0)).to((8.7,0)));c.d.add(E.Arrow().at((0,-2.7)).to((0,2.7)));xs=[i/100 for i in range(801)];c.ax.plot(xs,[2*math.sin(math.pi*x/2) for x in xs],color='black',lw=1.65)
for y,lab in [(2,'3'),(-2,'-3')]:c.ax.plot([0,8],[y,y],ls='--',color='black',lw=1);c.text(-.35,y,'$'+lab+'$',ha='right')
c.text(8.5,-.4,r'$t/\mathrm{s}$');c.text(.2,2.6,r'$u_i/\mathrm{V}$',ha='left');c.text(-.3,-.3,'$0$');c.save();panels('F070',['F070-a','F070-b'],['(a)','(b)']);QA['F070']='第一运放R1输入/R2正端接地/UZ1双向稳压反馈；uo1接第二负端，正端R3/R4构成正反馈，R5后UZ2限幅；只重绘原给定±3V正弦输入，不添周期值与输出答案。'

# E7-20: comparator alarm output, with a base-emitter protection diode.
c=C('F071','E7-20',size=(13,10));n,p,o=op(c,5,4);c.port((0,n.y),'$U_R$');part(c,'R',(0,n.y),n,'R_1');c.port((0,p.y),'$u_1$');part(c,'R',(0,p.y),p,'R_2')
t=c.d.add(E.BjtNpn().at((12,4)).anchor('base'));c.text(t.center.x+.5,4,'$T$',ha='left');part(c,'R',o,t.base,'R_3');c.wire(t.emitter,(t.emitter.x,0));c.wire((0,0),(15,0));c.ground((t.emitter.x,0));part(c,'D',(11.3,0),(11.3,4),'D');c.dot((11.3,4));c.dot((11.3,0))
c.wire(t.collector,(t.collector.x,6));part(c,'S',(t.collector.x,6),(t.collector.x,9));c.ax.plot([t.collector.x-.35,t.collector.x+.35],[7.15,7.85],color='black',lw=1.65);c.ax.plot([t.collector.x-.35,t.collector.x+.35],[7.85,7.15],color='black',lw=1.65);c.wire((t.collector.x,9),(t.collector.x,10));c.supply((t.collector.x,10),'$+U_{CC}$');c.text(t.collector.x+1,7.5,'报警指示灯',ha='left')
done(c,'UR经R1入负端、u1经R2入正端；输出经R3驱动NPN基极，发射极接地、集电极串灯到+UCC；D阴极接基极、阳极接地，方向照录。')

(HERE/'geometry.json').write_bytes((json.dumps(M.records,ensure_ascii=False,indent=2)+'\n').encode())
(HERE/'qa-partial.json').write_bytes((json.dumps(QA,ensure_ascii=False,indent=2)+'\n').encode())
