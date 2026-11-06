"""Chapter 8: main-agent transcriptions from uncropped textbook and exam sources."""
from pathlib import Path
import sys,json,math
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent))
import common as M
from panels import combine
from PIL import Image,ImageDraw,ImageFont
from matplotlib.font_manager import findfont
from matplotlib.patches import Polygon
M.OUT=HERE;C=M.Circuit;E=M.E;QA={}
def part(c,k,a,b,label=None,**kw):
 if k!='L':return c.part(k,a,b,'$'+label+'$' if label else None,**kw)
 c.d.add(E.Inductor().scalex(2).scaley(1.5).at(a).to(b));c.components.append(dict(kind='L',a=list(a),b=list(b),label='$'+label+'$' if label else None,reverse=False))
 if label:
  offset=kw.get('offset',.5);x=(a[0]+b[0])/2;y=(a[1]+b[1])/2
  c.text(x+offset,y,'$'+label+'$',ha='left' if offset>0 else 'right')

def op(c,x,y,label='A',plus_top=False):return c.op(x,y,label=label,plus_top=plus_top)
def save(c,note):c.save(note=note);QA[c.key]=note
def ground(c,p,label=None,bottom=0,offset=-.5):
 if label:part(c,'R',p,(p[0],bottom),label,offset=offset)
 else:c.wire(p,(p[0],bottom))
 c.ground((p[0],bottom))
def feedback(c,n,o,label,y=11,left=None,right=None,kind='R'):
 left=n.x-1 if left is None else left;right=o.x+2 if right is None else right;c.wire(n,(left,n.y),(left,y));part(c,kind,(left,y),(right,y),label);c.wire((right,y),(right,o.y),o);c.dot((left,n.y));c.dot((right,o.y))
def output(c,o,x,label='u_o'):c.wire(o,(x,o.y));c.port((x,o.y),'$'+label+'$','right')
def clamp(c,x,top=6,bottom=2,label=r'\pm U_Z'):
 mid=(top+bottom)/2;part(c,'Z',(x,top),(x,mid));part(c,'Z',(x,mid),(x,bottom),reverse=True);c.ground((x,bottom));c.text(x+.7,mid,'$'+label+'$',ha='left');c.dot((x,top))
def panels(key,ids):
 labels=['('+chr(97+i)+')' for i in range(len(ids))];combine(HERE,key,ids,labels)
 ims=[Image.open(HERE/(k+'.png')).convert('RGB') for k in ids];w=max(im.width for im in ims);out=Image.new('RGB',(w,sum(im.height+70 for im in ims)),'white');d=ImageDraw.Draw(out);font=ImageFont.truetype(findfont('STIXGeneral'),40);y=0
 for im,label in zip(ims,labels):out.paste(im,((w-im.width)//2,y));d.text((w/2,y+im.height+5),label,anchor='mt',font=font,fill='black');y+=im.height+70
 out.save(HERE/(key+'.png'))

# Common-base LC circuits: the emitter coupling capacitor returns to the tank tap.
for suffix in ['a','b']:
 c=C('F072-'+suffix,'E8-1',size=(13,10));t=c.bjt((4,6));c.wire(t.base,(2,6));part(c,'R',(2,6),(2,11),'R_{B1}',offset=-.5);part(c,'R',(2,6),(2,0),'R_{B2}',offset=-.5);part(c,'C',(0,6),(2,6),'C_B');c.wire((0,6),(0,0),(14,0));c.ground((t.emitter.x,0));c.dot((2,6))
 c.wire(t.collector,(t.collector.x,8));part(c,'R',(t.collector.x,8),(t.collector.x,11),'R_C',offset=-.5);c.wire((2,11),(t.collector.x,11),(8,11));c.supply((8,11),'$+U_{CC}$');part(c,'C',(t.collector.x,8),(10,8),'C_C');c.dot((t.collector.x,8));part(c,'R',t.emitter,(t.emitter.x,0),'R_E',offset=-.5);part(c,'C',t.emitter,(10,t.emitter.y),'C_E');c.dot(t.emitter)
 if suffix=='a':
  part(c,'L',(10,8),(10,t.emitter.y),'L_1',offset=.5);part(c,'L',(10,t.emitter.y),(10,2),'L_2',offset=.5);part(c,'C',(14,8),(14,2),'C');c.wire((10,8),(14,8));c.wire((10,2),(14,2));c.wire((10,2),(10,0));c.dot((10,t.emitter.y))
 else:
  part(c,'C',(10,8),(10,t.emitter.y),'C_1',offset=-.5);part(c,'C',(10,t.emitter.y),(10,2),'C_2',offset=-.5);part(c,'L',(14,8),(14,2),'L');c.wire((10,8),(14,8));c.wire((10,2),(14,2));c.wire((10,2),(10,0));c.dot((10,t.emitter.y))
 c.save()
panels('F072',['F072-a','F072-b']);QA['F072']='两幅共基LC：CB接基极交流地，CC从集电极到谐振上端，CE从发射极到L1/L2或C1/C2中点；RE/RB1/RB2/RC及公共地保留，不把抽头短接地。'

def transformer(key,third=False):
 c=C(key,key,size=(14,12));t=c.bjt((4,6));c.wire(t.base,(2,6));part(c,'R',(2,6),(2,12),'R_{B1}',offset=-.5);part(c,'R',(2,6),(2,0),'R_{B2}',offset=-.5);c.wire((2,12),(7,12));c.supply((7,12),'$+U_{CC}$');c.dot((2,6));part(c,'C',(-1,6),(2,6),'C_1');c.wire((-1,6),(-1,14),(11,14),(11,12));c.text(11.6,11.6,'$1$');part(c,'L',(11,12),(11,8));c.text(11.6,8.4,'$2$');c.wire((11,8),(13,8));c.ground((13,8))
 part(c,'L',(7,12),(7,7),'L',offset=-.5);c.wire(t.collector,(7,t.collector.y),(7,7));c.wire(t.emitter,(t.emitter.x,4));part(c,'R',(t.emitter.x,4),(t.emitter.x,0),'R_E',offset=-.5);c.wire((t.emitter.x,4),(8,4));part(c,'C',(8,4),(8,0),'C_E');c.wire((2,0),(8,0));c.ground((t.emitter.x,0));c.dot((t.emitter.x,4))
 if third:
  part(c,'C',(15,12),(15,8),'C');c.wire((11,12),(15,12));c.wire((11,8),(15,8));c.dot((6.55,10.45))
 else:
  part(c,'C',(9,12),(9,7),'C',offset=-.5);c.wire((7,12),(9,12));c.wire((7,7),(9,7));c.dot((6.55,8.55));part(c,'L',(11,6),(11,2));part(c,'R',(15,6),(15,2),'R_L');c.wire((11,6),(15,6));c.wire((11,2),(15,2))
 return c
c=transformer('F073');save(c,'E8-2原题初级同名点在下端；上次级1/2端尚未标同名端，不补作答黑点；独立负载绕组与RL保留，反馈1端经C1接基极、2端地。')
c=transformer('F074',third=True);save(c,'E8-3初级同名点在电源上端；次级1端经C1回基极、2端地，次级与C并联；不把参考解新加的次级黑点写进题图，不在图中改写有争议的C单位。')

def wien(key,thermal=False,teaching=False):
 c=C(key,key,size=(13,11));n,p,o=op(c,6,6);c.wire(n,(5,n.y));part(c,'R',(1,n.y),(5,n.y),'R_F' if thermal else 'R_1');c.ground((1,n.y));feedback(c,n,o,'R_1' if thermal else ('R_f' if teaching else 'R_F'),y=11,left=5,right=12)
 if thermal:c.d.add(E.Line().at((8,10.4)).to((9,11.6)));c.text(8.6,10.2,r'$\theta$')
 c.wire(p,(4,p.y),(4,3));part(c,'C',(4,3),(8,3),'C');part(c,'R',(8,3),(12,3),'R');c.wire((12,3),(12,6));c.dot((12,6));c.dot((4,3));part(c,'C',(2,3),(2,0),'C',offset=-.5);part(c,'R',(5,3),(5,0),'R');c.wire((2,3),(5,3));c.wire((2,0),(5,0));c.ground((3.5,0));c.wire((2,0),(3.5,0));output(c,o,14,label=r'\dot U_o' if teaching else 'u_o');return c
c=wien('F075');save(c,'从完整物理279页恢复RF负反馈：R1接地、RF回输出；输出到正端为C/R串联，正端到地为R∥C。旧裁图缺顶部不可沿用。')
c=wien('F077',thermal=True);save(c,'完整物理281页确认RF为接地支路、R1为带θ标记热敏反馈电阻；文氏桥仍为串联CR和并联RC，未对调RF/R1。')
c=wien('F193',teaching=True);c.text(3.4,3.8,r'$\dot U_p$',ha='right');save(c,'文氏桥知识图RF负反馈/R1地，输出经串联C/R回正端，正端并联R/C到地；保留相量Up，移除背景截图。')

# The connection exercise stays OPEN: do not draw its answer connections.
c=C('F076','E8-5',size=(19,12));c.port((0,11),'$a$');part(c,'R',(0,11),(0,8),'R',offset=-.5);part(c,'C',(0,8),(0,5.5),'C',offset=-.5);c.dot((0,5.5));c.text(.5,5.5,'$b$');c.wire((0,5.5),(-2,5.5));part(c,'C',(-2,5.5),(-2,2),'C',offset=-.5);part(c,'R',(2,5.5),(2,2),'R');c.wire((0,5.5),(2,5.5));c.wire((-2,2),(2,2),(0,2),(0,0));c.port((0,0),'$c$')
t1=c.d.add(E.BjtNpn().theta(0).at((9,6)).anchor('base'));c.text(t1.center.x+.5,6,'$T_1$');t2=c.d.add(E.BjtNpn().reverse().theta(0).at((17,6)).anchor('base'));c.text(t2.center.x-.6,6,'$T_2$',ha='right');c.wire(t1.collector,(t1.collector.x,8));c.wire(t2.collector,(t2.collector.x,8));part(c,'R',(t1.collector.x,8),(t1.collector.x,12),'R_{C1}',offset=-.5);part(c,'R',(t2.collector.x,8),(t2.collector.x,12),'R_{C2}');c.wire((t1.collector.x,12),(t2.collector.x,12));c.supply((13,12),'$+U_{CC}$');c.wire((t1.collector.x,12),(13,12));c.wire(t1.emitter,(13,t1.emitter.y),t2.emitter);part(c,'R',(13,t1.emitter.y),(13,1),'R_E');c.port((13,1));c.wire(t1.base,(8,6));part(c,'R',(8,6),(8,2),'R_{B1}',offset=-.5);c.ground((8,2));c.wire(t2.base,(18,6));part(c,'R',(18,6),(18,2),'R_{B2}');c.ground((18,2));save(c,'RC网络a/b/c与差分级保持原题未接状态：上串RC、下并RC；两NPN共发射极/RE到开口电源端，RC1/RC2接+UCC，RB1/RB2各地；不代填连接答案。')

# E8-7 asks students to assign signs, so both op-amp inputs stay unmarked.
def unknown_op(c,x,y,label):
 c.ax.add_patch(Polygon([(x,y+1.25),(x+2.165,y),(x,y-1.25)],fill=False,lw=1.65,color='black'));c.text(x+.9,y,'$'+label+'$');c.op_triangles.append([(x,y+1.25),(x+2.165,y),(x,y-1.25)]);return (x,y+.625),(x,y-.625),(x+2.165,y)
c=C('F078','E8-7',size=(17,11));a,b,o1=unknown_op(c,6,6,'A_1');a2,b2,o2=unknown_op(c,15,6,'A_2');c.wire(a,(3,a[1]),(3,3));part(c,'C',(1,3),(1,0),'C',offset=-.5);part(c,'R',(4,3),(4,0),'R');c.wire((1,3),(4,3));c.wire((1,0),(4,0));c.ground((2.5,0));c.wire((1,0),(2.5,0));c.wire((3,a[1]),(3,11));part(c,'R',(3,11),(11,11),'R');part(c,'C',(11,11),(20,11),'C');c.wire((20,11),(20,6),o2);c.dot((3,a[1]));c.dot((20,6));c.wire(b,(5,b[1]),(5,3),(10,3),(10,6),o1);c.dot((10,6));c.wire((10,6),(13,6),(13,a2[1]),a2);c.wire(b2,(14,b2[1]),(14,2));part(c,'R',(14,2),(14,0),'R_1',offset=-.5);c.ground((14,0));part(c,'R',(14,2),(20,2),'R_2');c.wire((20,2),(20,6));c.dot((14,2))
c.wire(o2,(22,6));c.port((22,6),'$u_o$','right');save(c,'完整原题E8-7两运放均未标±，重绘保持空白；A1下输入回自身输出、上输入接并联RC节点；A2下输入R1地/R2输出，上输入接A1输出，顶部R/C串联回路齐全。')

def triangle_generator(key,knowledge=False,saw=None):
 c=C(key,key,size=(23 if saw else 20,13));n1,p1,o1=op(c,5,7,'A_1');n2,p2,o2=op(c,18 if saw else 15,7,'A_2');c.wire(n1,(4,n1.y));part(c,'R',(0,n1.y),(4,n1.y),r'5\,\mathrm{k}\Omega' if saw=='F111' else r'6\,\mathrm{k}\Omega') if saw else c.wire((0,n1.y),(4,n1.y));c.ground((0,n1.y))
 series=(r'1\,\mathrm{k}\Omega' if saw else ('R_4' if knowledge else 'R_3'));part(c,'R',o1,(10,7),('R_4=' if saw=='F129' else '')+series);c.dot((10,7));clamp(c,10,top=7,bottom=3,label='D_Z' if saw else r'\pm U_Z');c.wire(p1,(4,p1.y),(4,3));c.wire((4,3),(-2,3),(-2,11));part(c,'R',(-2,11),(10,11),('R_2=' if saw=='F129' else '')+(r'11\,\mathrm{k}\Omega' if saw=='F111' else r'15\,\mathrm{k}\Omega') if saw else 'R_2');c.wire((10,11),(10,7));c.dot((4,3))
 # Keep the feedback resistor on the lower rail, below all ground branches.
 c.wire((4,3),(4,-1));part(c,'R',(4,-1),(24 if saw else 21,-1),('R_1=' if saw=='F129' else '')+r'10\,\mathrm{k}\Omega' if saw else 'R_1');c.wire((24 if saw else 21,-1),(24 if saw else 21,7),o2);c.dot((24 if saw else 21,7))
 if saw:
  part(c,'R',(10,7),(13,7),('R_3=' if saw=='F129' else '')+(r'0.5\,\mathrm{k}\Omega' if saw=='F111' else r'1\,\mathrm{k}\Omega'));c.wire((13,7),(13,10));part(c,'D',(13,10),(16,10),'D_1');c.wire((13,7),(13,4));part(c,'D',(16,4),(13,4),'D_2',offset=-.5);part(c,'R',(16,10),(16,4),r'10\,\mathrm{k}\Omega',offset=-.5);c.d.add(E.Arrow().at((17,7)).to((16.2,7)));c.wire((17,7),(17.5,7),(17.5,n2.y),n2);c.dot((13,7));feedback(c,n2,o2,r'C=0.1\,\mu\mathrm{F}' if saw=='F129' else r'0.1\,\mu\mathrm{F}',y=13,left=17.5,right=24,kind='C');ground(c,p2,('R_5=' if saw=='F129' else '')+(r'5\,\mathrm{k}\Omega' if saw=='F111' else r'6\,\mathrm{k}\Omega'))
 else:
  part(c,'R',(10,7),(13,7),'R_3' if knowledge else 'R');c.wire((13,7),(13,n2.y),n2);feedback(c,n2,o2,'C',y=12,left=13,right=21,kind='C');ground(c,p2,'R_5' if knowledge else 'R');c.text(10.8,7.5,'$u_{o1}$') if knowledge else None
 output(c,o2,26 if saw else 23);return c
c=triangle_generator('F079');save(c,'E8-8：比较器负端地/正端R1接最终输出、R2接钳位节点，输出经R3限流；钳位节点再经R入A2负端、C反馈、正端R地；外反馈回最终三角波输出。')
c=triangle_generator('F195',knowledge=True);save(c,'方波/三角波互反馈：A1负端地、R4到钳位方波uo1，经R3入A2积分，C反馈/正端R5地；R2局部正反馈、R1最终输出反馈，原开口节点语义保留为同网导线。')
c=triangle_generator('F111',saw='F111');save(c,'锯齿波题：5k负端地、1k限流、0.5k串联；D1朝右/D2朝左分别接10k电位器两端，滑端送积分器；11k正反馈、10k外反馈、5k正端地、0.1μF均照录。')
c=triangle_generator('F129',saw='F129');save(c,'另一年份：6k负端地、R4=1k/R3=1k、R2=15k/R1=10k/R5=6k、C=0.1μF；D1/D2接电位器两端且方向相反，滑端接A2负端；不混入上一年份0.5k/11k。')

c=C('F080','E8-9',size=(19,11));n1,p1,o1=op(c,5,6,'A_1');n2,p2,o2=op(c,14,6,'A_2',plus_top=True);part(c,'R',(0,n1.y),(4,n1.y),'R')
# Only the resistor's left terminal returns to the final output.
c.wire((4,n1.y),n1);feedback(c,n1,o1,'C',y=9,left=4,right=9,kind='C');ground(c,p1,'R');part(c,'R',(9,6),(12,6),'R_1');c.wire((12,6),(12,p2.y),p2);c.text(9.5,6.5,'$u_{o1}$');c.wire((12,p2.y),(12,9));part(c,'R',(12,9),(22,9),'R_2');c.wire((22,9),(22,6));part(c,'R',o2,(22,6),'R_3');ground(c,n2,'R_B');clamp(c,22,top=6,bottom=1);c.wire((0,n1.y),(0,12),(22,12),(22,6));c.dot((12,p2.y));c.dot((22,6));c.wire((22,6),(24,6));c.port((24,6),'$u_o$','right');save(c,'E8-9第一级负端R输入/C反馈、正端R地；第二级上正下负，uo1经R1、钳位后uo经R2同接正端，负端RB地，R3输出限流；最终uo回第一级R输入，保留原振荡闭环。')

c=C('F194','矩形波发生器',size=(13,11));n,p,o=op(c,6,6);c.wire(n,(3,n.y),(3,10));part(c,'R',(3,10),(13,10),'R_3');c.wire((13,10),(13,6));part(c,'C',(3,n.y),(3,0),'C',offset=-.5);c.ground((3,0));c.dot((3,n.y));c.text(2.5,n.y+.5,r'$u_N\ (u_C)$',ha='right');c.text(5.4,n.y+.4,'$N$',size=14)
c.wire(p,(5,p.y),(5,3));part(c,'R',(5,3),(5,0),'R_1',offset=-.5);c.ground((5,0));part(c,'R',(5,3),(13,3),'R_2');c.wire((13,3),(13,6));c.dot((5,3));c.text(5.5,p.y-.4,'$P$',size=14);part(c,'R',o,(13,6),'R_4');clamp(c,13,top=3,bottom=-1,label=r'D_Z:\ \pm U_Z');c.wire((13,6),(15,6));c.port((15,6),'$u_o$','right');c.dot((13,6));save(c,'矩形波源R3从限幅输出回负端电容C节点；正端R1地/R2正反馈、输出R4串接双向DZ；所有连接使用黑线/节点，不依赖原红色高亮或鼠标标记。')
c=C('F196','积分器转换波形',size=(11,8));n,p,o=op(c,5,4);c.port((0,n.y),'$u_I$');part(c,'R',(0,n.y),(4,n.y),'R');c.wire((4,n.y),n);feedback(c,n,o,'C',y=8,left=4,right=10,kind='C');ground(c,p,"R'");output(c,o,12,label='u_O');c.d.add(E.Arrow().at((.8,n.y-.6)).to((2,n.y-.6)));c.text(1.4,n.y-1,'$i_R$');c.d.add(E.Arrow().at((6,7.3)).to((8,7.3)));c.text(7,6.8,'$i_C$');save(c,'方波转三角波积分器：R输入、C反馈、正端R′地；iR向右、iC反馈线向右，保留源变量撇号与箭头方向。')

(HERE/'geometry.json').write_bytes((json.dumps(M.records,ensure_ascii=False,indent=2)+'\n').encode())
(HERE/'qa.json').write_bytes((json.dumps({'verified':QA,'pending':{}},ensure_ascii=False,indent=2)+'\n').encode())
