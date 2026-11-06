"""Main-agent chapter 9 redraws from actual referenced figures and full PDF pages."""
from pathlib import Path
import sys,json,math
from collections import namedtuple
P=namedtuple('Point','x y')
from PIL import Image,ImageDraw,ImageFont
from matplotlib.font_manager import findfont
from matplotlib.patches import Rectangle,Polygon,Arc
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent))
import common as M
from panels import combine
M.OUT=HERE;C=M.Circuit;E=M.E;QA={}
def part(c,k,a,b,label=None,**kw):
 if k!='L':return c.part(k,a,b,'$'+label+'$' if label else None,**kw)
 c.d.add(E.Inductor().scalex(2).scaley(1.5).at(a).to(b));c.components.append(dict(kind='L',a=list(a),b=list(b),label=label))
 if label:c.text((a[0]+b[0])/2+kw.get('offset',.5),(a[1]+b[1])/2,'$'+label+'$',ha='left')
def save(c,note):c.save(note=note);QA[c.key]=note
def dot(c,*ps):
 for p in ps:c.dot(p)
def arrow(c,a,b,label=None,where=None):
 c.d.add(E.Arrow().at(a).to(b))
 if label:c.text(*(where or ((a[0]+b[0])/2,(a[1]+b[1])/2+.5)),'$'+label+'$',size=15)
def ports(c,x0,x1,top,bottom=0,ui='U_I',uo='U_O'):
 for x in [x0,x1]:c.port((x,top),'$+$','left' if x==x0 else 'right');c.port((x,bottom),'$-$','left' if x==x0 else 'right')
 c.text(x0-1.2,(top+bottom)/2,'$'+ui+'$');c.text(x1+2.7,(top+bottom)/2,'$'+uo+'$')
def ground(c,p):c.ground(p)
def cap(c,x,top,bottom,label):part(c,'C',(x,top),(x,bottom),label);c.text(x-.35,(top+bottom)/2+.5,'$+$')
def panels(key,ids):
 labels=['('+chr(97+i)+')' for i in range(len(ids))];combine(HERE,key,ids,labels);ims=[Image.open(HERE/(k+'.png')).convert('RGB') for k in ids];w=max(im.width for im in ims);out=Image.new('RGB',(w,sum(im.height+70 for im in ims)),'white');d=ImageDraw.Draw(out);f=ImageFont.truetype(findfont('STIXGeneral'),40);y=0
 for im,label in zip(ims,labels):out.paste(im,((w-im.width)//2,y));d.text((w/2,y+im.height+5),label,anchor='mt',font=f,fill='black');y+=im.height+70
 out.save(HERE/(key+'.png'))
def trans(c,x=0,top=8,bottom=2):
 part(c,'L',(x,top),(x,bottom));part(c,'L',(x+2,top),(x+2,bottom));c.wire((x-2,top),(x,top));c.wire((x-2,bottom),(x,bottom));c.port((x-2,top),'$+$');c.port((x-2,bottom),'$-$');c.text(x-3,(top+bottom)/2,'$u_1$');c.text(x+1,top+.7,r'$\mathrm{Tr}$');c.text(x+3,(top+bottom)/2,'$u_2$');return (x+2,top),(x+2,bottom)
def bridge_symbol(c,x,y):
 # Standard rectifier package: top/bottom AC, left DC-, right DC+.
 c.ax.add_patch(Polygon([(x,y+2),(x+2,y),(x,y-2),(x-2,y)],fill=False,lw=1.65,color='black'));part(c,'D',(x-1,y),(x+1,y));return (x,y+2),(x,y-2),(x-2,y),(x+2,y)
def front(c):
 a,b=trans(c);at,ab,neg,pos=bridge_symbol(c,6,5);c.wire(a,(6,8),at);c.wire(b,ab);c.wire(neg,(4,0),(11,0));c.wire(pos,(10,5),(10,10),(11,10));cap(c,11,10,0,'C_1');c.text(12,6,'$U_1$');return (11,10)
def leftop(c,x,y,label='A',unsigned=False):
 if not unsigned:return c.op(x,y,label=label,reverse=True)
 c.ax.add_patch(Polygon([(x+2.165,y+1.25),(x,y),(x+2.165,y-1.25)],fill=False,lw=1.65,color='black'));c.text(x+1.1,y,'$'+label+'$');c.op_triangles.append([(x+2.165,y+1.25),(x,y),(x+2.165,y-1.25)]);return P(x=x+2.165,y=y+.625),P(x=x+2.165,y=y-.625),P(x=x,y=y)
def passnpn(c,x,y,label='T'):
 # Rotate the emitter follower so collector is left, emitter right, base below.
 t=c.d.add(E.BjtNpn().theta(90).at((x,y)).anchor('base'));c.text(x,y+1,'$'+label+'$');return t
def regulator(c,x,y,name,pins=False):
 c.ax.add_patch(Rectangle((x,y-.7),3,1.4,fill=False,lw=1.65,color='black'));c.text(x+1.5,y,name,size=18)
 if pins:c.text(x-.3,y+.5,'$1$');c.text(x+3.3,y+.5,'$3$');c.text(x+1.8,y-1,'$2$')
 return (x,y),(x+3,y),(x+1.5,y-.7)

# Explicit bridge, preserving original diode numbering.
c=C('F082','E9-2',size=(15,10));a,b=trans(c);c.wire(a,(4,8),(4,5),(7,5));c.wire(b,(4,2),(4,3.5),(10,3.5));
for x,up,lo in [(7,'D_1','D_3'),(10,'D_2','D_4')]:
 part(c,'D',(x,5 if x==7 else 3.5),(x,10),up);part(c,'D',(x,0),(x,5 if x==7 else 3.5),lo);c.dot((x,5 if x==7 else 3.5))
c.wire((7,10),(17,10));c.wire((7,0),(17,0));cap(c,13,10,0,'C');part(c,'R',(17,10),(17,0),'R_L');dot(c,(13,10),(13,0));arrow(c,(14.4,10.7),(16,10.7),'i_o');c.text(18,10,'$+$');c.text(18,0,'$-$');c.text(18.5,5,'$u_o$');save(c,'E9-2完整图：D1/D3左桥臂、D2/D4右桥臂均上阴极；次级分别接两中点，交叉处无接点；C正极上、RL并输出，io向右。')

c=C('F083','E9-5',size=(17,10));front(c);c.labels=[(x,y,'$C$' if t=='$C_1$' else t,h,v,z) for x,y,t,h,v,z in c.labels];part(c,'R',(11,10),(16,10),'R');part(c,'Z',(17,0),(17,10),'D_Z');part(c,'R',(21,10),(21,0),'R_L');c.wire((16,10),(21,10));c.wire((11,0),(21,0));arrow(c,(18.5,10.7),(20.2,10.7),'I_O');c.text(23,5,'$u_o$');dot(c,(17,10),(17,0));save(c,'E9-5整流包、C滤波后R串联，DZ阴极上与RL并联；保留变压器u1/u2、U1及IO，未把题干数值或答案回填图中。')
c=C('F084','E9-6',size=(11,8));c.port((0,7),'$+$');c.port((0,0),'$-$');cap(c,2,7,0,r'U_1=27\,\mathrm{V}');c.wire((0,7),(2,7));c.wire((0,0),(11,0));part(c,'R',(2,7),(7,7),r'R=0.6\,\mathrm{k}\Omega');c.wire((7,7),(11,7));part(c,'Z',(7,0),(7,7),'D_Z');part(c,'R',(11,7),(11,0),r'R_L=1\,\mathrm{k}\Omega');c.text(8.9,2.5,r'$9\,\mathrm{V}$');arrow(c,(8.1,6.6),(8.1,4.7),'I_Z',(8.6,5.9));arrow(c,(3,8),(4.5,8),'I');arrow(c,(8.8,8),(10.4,8),'I_O');dot(c,(7,7),(7,0));save(c,'27V输入、0.6kΩ串R、9V DZ反偏、1kΩRL并接，原图I/IO向右、IZ向下；输入符号按原双线源保留为电容状源标识。')

def series_reg(key,teaching=False,two=False):
 c=C(key,key,size=(23 if not teaching else 17,13));shift=0 if not teaching else -10
 if not teaching:front(c)
 else:c.port((1,10),'$+$');c.port((1,0),'$-$');c.text(-.5,5,'$U_I$');c.wire((1,10),(11+shift,10));c.wire((1,0),(11+shift,0))
 t=passnpn(c,15+shift,9);c.wire((11+shift,10),(t.collector.x,10),t.collector);c.wire(t.emitter,(t.emitter.x,10),(27+shift,10));c.wire((11+shift,0),(27+shift,0));dot(c,(11+shift,10));n,p,o=leftop(c,15+shift,6)
 c.wire(o,(14+shift,6),(14+shift,8),(t.base.x,8),t.base);refx=3 if teaching else 20
 if teaching:c.wire((1,10),(3,10));part(c,'R',(3,10),(3,4),'R',offset=-.5);c.wire((3,4),(20+shift,4));c.dot((3,10))
 else:part(c,'R',(20,10),(20,8),'R');c.wire((20,8),(20,4))
 part(c,'Z',(20+shift,0),(20+shift,4),'D_Z');c.wire(p,(18+shift,p.y),(18+shift,4),(20+shift,4));
 part(c,'R',(24+shift,10),(24+shift,7),'R_1');part(c,'R',(24+shift,7),(24+shift,3),'R_2',offset=.65);part(c,'R',(24+shift,3),(24+shift,0),'R_3');arrow(c,(23+shift,5),(23.8+shift,5));c.wire(n,(22+shift,n.y),(22+shift,5),(23+shift,5));part(c,'R',(27+shift,10),(27+shift,0),'R_L');dot(c,(20+shift,10),(20+shift,4),(20+shift,0),(24+shift,10),(24+shift,0));c.text(28+shift,10,'$+$');c.text(28+shift,0,'$-$');c.text(29+shift,5,'$U_O$')
 if not teaching:
  arrow(c,(17+shift,10.8),(18.5+shift,10.8),'I_E');arrow(c,(25+shift,10.8),(26.5+shift,10.8),'I_O');arrow(c,(19.4+shift,9),(19.4+shift,7.5),'I_R',(18.8+shift,8.3));arrow(c,(24.8+shift,9),(24.8+shift,7.5),'I_{R1}',(25.7+shift,8.3));c.text(22+shift,2.8,'$U_Z$');c.text(21+shift,3.7,'$+$');c.text(21+shift,.8,'$-$')
 else:
  c.text(15.5+shift,8.1,'$B$');c.text(n.x+.4,n.y+.4,'$N$',size=14);c.text(p.x+.4,p.y-.4,'$P$',size=14);c.text(25.7+shift,6.6,r"$R_2^{\prime\prime}$");c.text(25.7+shift,4.1,r"$R_2^{\prime}$")
 return c
c=series_reg('F085');save(c,'E9-7集成比较稳压：NPN串联T，输出经R到DZ基准，运放正端基准/负端电位器R2滑端；R1/R2/R3全分压、RL及IE/IR/IR1/IO原方向照录。')
c=series_reg('F198',teaching=True);save(c,'串联比较稳压知识图T基极B由运放驱动，正端P接DZ基准、负端N取R2滑端；R2上下段R2″/R2′及输入/输出极性保留，R从输入供基准。')

# Discrete comparator regulator: T2 is an NPN with base facing right.
c=C('F086','E9-8',size=(23,13));front(c);t1=passnpn(c,17,9,'T_1');c.wire((11,10),(t1.collector.x,10),t1.collector);c.wire(t1.emitter,(t1.emitter.x,10),(28,10));c.wire((11,0),(28,0));t2=c.d.add(E.BjtNpn().reverse().theta(0).at((21,5)).anchor('base'));c.text(t2.center.x-.5,5,'$T_2$',ha='right');c.wire(t1.base,(17,7),(t2.collector.x,7),t2.collector);part(c,'R',(15,10),(15,7),'R_1',offset=-.5);c.wire((15,7),(17,7));part(c,'R',(13,10),(13,2.5),'R_2',offset=-.5);c.wire(t2.emitter,(t2.emitter.x,2.5),(13,2.5));part(c,'Z',(t2.emitter.x,0),(t2.emitter.x,2.5),'D_Z');dot(c,(17,7),(t2.emitter.x,2.5));part(c,'R',(24,10),(24,7),'R_3');part(c,'R',(24,7),(24,3),'R_P');part(c,'R',(24,3),(24,0),'R_4');arrow(c,(23,5),(23.8,5));c.wire(t2.base,(23,5));cap(c,26,10,0,'C_2');part(c,'R',(28,10),(28,0),'R_L');c.text(25,2,'$U_F$');c.text(29,5,'$U_O$');dot(c,(15,10),(13,10),(24,10),(26,10),(26,0));save(c,'E9-8 NPN T1调整/T2比较，T2基极取RP滑端、发射极接DZ基准；R1由输入到T1基极/T2集电极，R2由输入供DZ；R3/RP/R4输出采样、C1/C2滤波完整。')

# Buck and boost retain the physical transistor and freewheel diode directions.
c=C('F199','降压开关',size=(14,9));t=passnpn(c,4,7);c.wire((0,8),(t.collector.x,8),t.collector);c.wire(t.emitter,(t.emitter.x,8),(7,8));part(c,'L',(7,8),(12,8));c.text(9.5,8.7,'$L$');c.wire((12,8),(16,8));c.wire((0,0),(16,0));part(c,'D',(7,0),(7,8),'D',offset=-.5);cap(c,12,8,0,'C');part(c,'R',(16,8),(16,0),'R_L');c.wire(t.base,(4,4));c.port((4,4),'$u_B$','right');c.text(7,8.6,'$e$');dot(c,(7,8),(7,0),(12,8),(12,0));ports(c,0,16,8);save(c,'Buck原理：NPN集电极接输入、发射极开关节点e，L串输出；续流D阳极地/阴极e；C与RL并联输出，基极uB开口控制，黑白分区不依赖原底色。')
c=C('F200','升压开关',size=(14,9));c.wire((0,8),(2,8));part(c,'L',(2,8),(7,8));c.text(4.5,8.7,'$L$');part(c,'D',(7,8),(12,8),'D');c.wire((12,8),(16,8));c.wire((0,0),(16,0));t=c.d.add(E.BjtNpn().reverse().theta(0).at((9,4)).anchor('base'));c.text(t.center.x-1,4,'$T$');c.wire(t.collector,(t.collector.x,8),(7,8));c.wire(t.emitter,(t.emitter.x,0));c.wire(t.base,(11,4));c.port((11,4));c.text(10.5,3,'$u_B$');cap(c,12,8,0,'C');part(c,'R',(16,8),(16,0),'R_L');ports(c,0,16,8);dot(c,(7,8),(12,8),(12,0),(t.emitter.x,0));save(c,'Boost原理：输入串L到开关节点，D阳极节点/阴极输出；NPN集电极节点、发射极地、基极uB，C/RL并输出；不画成Buck续流方向。')

# Actual four-diode rectangle from the exam, with its original labels and polarity.
def exam_bridge(key,limit,load):
 c=C(key,key,size=(16,10))
 for x,upper,lower,reverse in [(1,'D_1','D_2',False),(5,'D_4','D_3',True)]:
  part(c,'D',(x,10),(x,5),upper,reverse=reverse);part(c,'D',(x,5),(x,0),lower,reverse=not reverse);c.dot((x,5))
 c.wire((-1,10),(5,10));c.wire((-1,0),(5,0));c.port((-1,10),'$+$');c.port((-1,0),'$-$');c.text(-2,5,'$u_i$')
 c.wire((1,5),(3,5),(3,12),(9,12));c.wire((5,5),(7,5),(7,0),(18,0));cap(c,9,12,0,'C');part(c,'R',(9,12),(14,12),limit);c.wire((14,12),(18,12));part(c,'Z',(14,0),(14,12),'D_Z');part(c,'R',(18,12),(18,0),load);dot(c,(9,12),(9,0),(14,12),(14,0));c.text(19,12,'$+$');c.text(19,0,'$-$');c.text(21.5,6,'$u_o$');return c
c=exam_bridge('F130',r'60\,\Omega',r'120\,\Omega');save(c,'原卷桥式矩形接法：D1朝下/D2朝上、D4朝上/D3朝下；交流加上下母线、直流从两中点取出；C滤波、60Ω串联、DZ阴极输出/120Ω负载，数值与方向全保留。')
c=exam_bridge('F154',r'0.4\,\mathrm{k}\Omega',r'2\,\mathrm{k}\Omega');save(c,'同矩形整流拓扑独立对源核验，后级0.4kΩ及2kΩ，不能复用上一题60Ω/120Ω数值；C正上、DZ阴极上，交叉无连接。')

c=C('F197','桥式整流',size=(16,11));a,b=trans(c);c.wire(a,(7,8),(9,10));c.wire(b,(7,2),(9,0));top=(9,10);bot=(9,0);left=(6,5);right=(12,5)
part(c,'D',top,right,'D_1');part(c,'D',bot,right,'D_2');part(c,'D',left,bot,'D_3');part(c,'D',left,top,'D_4');c.wire(left,(4,5),(4,-2),(17,-2));c.wire(right,(17,5));part(c,'R',(17,5),(17,-2),'R_L');c.port((17,5),'$+$','right');c.port((17,-2),'$-$','right');c.text(18.5,1.5,'$u_o$');c.text(8,10.7,'$A$');c.text(8,-.7,'$B$');dot(c,top,bot,left,right);c.text(-4.5,5,r'$\sim220\,\mathrm{V}$');c.text(-4.5,3,r'$50\,\mathrm{Hz}$');save(c,'桥式整流知识图：A/B为次级交流端，D1/D2阴极汇右正输出，D3/D4阳极汇左负输出；RL跨直流两端，未把B误接负输出。')

(HERE/'geometry.json').write_bytes((json.dumps(M.records,ensure_ascii=False,indent=2)+'\n').encode())
(HERE/'qa-partial.json').write_bytes((json.dumps(QA,ensure_ascii=False,indent=2)+'\n').encode())
