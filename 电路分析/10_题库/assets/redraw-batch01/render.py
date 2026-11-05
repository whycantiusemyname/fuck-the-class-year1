"""Deterministic SVG/PNG redraws; sources and certified conversion are read-only."""
from pathlib import Path
import json,shutil,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as E
from matplotlib.path import Path as GeometryPath
from PIL import Image,ImageDraw,ImageFont

COURSE=Path(__file__).resolve().parents[3]
ROOT=COURSE/'10_题库/assets/电子线路期末复习'
OUT=COURSE/'10_题库/assets/redraw-batch01'
OUT.mkdir(exist_ok=True)
plt.rcParams['svg.fonttype']='path'  # Outline glyphs for portable primes/subscripts; edit labels in this source.
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','axes.unicode_minus':False})
records=[]

class Circuit:
    def __init__(self,key,title,size=(10,6)):
        self.key,self.title=key,title
        self.fig,self.ax=plt.subplots(figsize=size)
        self.d=schemdraw.Drawing(canvas=self.ax,show=False,fontsize=17,lw=1.65,color='black')
        self.labels=[];self.components=[];self.wires=[];self.op_triangles=[]
    def wire(self,*pts):
        for a,b in zip(pts,pts[1:]):
            self.d.add(E.Line().at(a).to(b));self.wires.append((tuple(a),tuple(b)))
    def text(self,x,y,label,ha='center',va='center',size=17):self.labels.append((x,y,label,ha,va,size))
    def dot(self,p):self.d.add(E.Dot(radius=.045).at(p))
    def port(self,p,label=None,side='left'):
        self.d.add(E.Dot(open=True,radius=.065).at(p))
        if label:self.text(p[0]+(-.18 if side=='left' else .18),p[1],label,ha='right' if side=='left' else 'left')
    def ground(self,p):self.d.add(E.Ground().at(p))
    def part(self,kind,a,b,label=None,reverse=False,offset=.36):
        elm={'R':E.ResistorIEC,'C':E.Capacitor,'D':E.Diode,'Z':E.Zener,'V':E.SourceV,'S':E.Source,'B':E.BatteryCell}[kind]()
        if reverse:elm.reverse()
        self.d.add(elm.at(a).to(b))
        self.components.append({'kind':kind,'a':list(a),'b':list(b),'label':label,'reverse':reverse})
        if label:
            x=(a[0]+b[0])/2;y=(a[1]+b[1])/2
            if abs(a[0]-b[0])<.01:self.text(x+offset,y,label,ha='left' if offset>0 else 'right')
            else:self.text(x,y+offset,label,va='bottom' if offset>0 else 'top')
    def op(self,x,y,label='A',plus_top=False,reverse=False):
        op=E.Opamp().right().at((x,y))
        if plus_top:op.flip()
        if reverse:op.reverse()
        t=self.d.add(op)
        self.op_triangles.append([(t.in1.x,t.center.y+1.25),tuple(t.out),(t.in1.x,t.center.y-1.25)])
        self.text(t.center.x,t.center.y,'$'+label+'$',size=18)
        return t.in1,t.in2,t.out
    def bjt(self,p,label='T'):
        t=self.d.add(E.BjtNpn().at(p).anchor('base'))
        if label:self.text(t.center.x+.4,t.center.y,'$'+label+'$',ha='left')
        return t
    def supply(self,p,label):
        self.port(p);self.text(p[0],p[1]+.35,label,va='bottom')
    def save(self,note='',page=None):
        if self.key!='OP-symbol':
            for triangle in self.op_triangles:
                area=sum(triangle[i][0]*triangle[(i+1)%3][1]-triangle[(i+1)%3][0]*triangle[i][1] for i in range(3))
                if area<0:triangle=triangle[::-1]
                shape=GeometryPath(triangle)
                for a,b in self.wires:
                    pts=[(a[0]+(b[0]-a[0])*i/100,a[1]+(b[1]-a[1])*i/100) for i in range(1,100)]
                    assert not shape.contains_points(pts,radius=-.03).any(),(self.key,'导线穿过运放内部',a,b)
        self.d.draw(show=False)
        for x,y,s,ha,va,size in self.labels:self.ax.text(x,y,s,ha=ha,va=va,fontsize=size,color='black',fontfamily='Microsoft YaHei' if any(ord(ch)>127 for ch in s) else 'STIXGeneral')
        self.ax.set_aspect('equal');self.ax.axis('off')
        # Data limits include explicit labels; prevent edge clipping of annotations.
        xs=[v[0] for v in self.labels];ys=[v[1] for v in self.labels]
        if xs:
            lo,hi=self.ax.get_xlim();self.ax.set_xlim(min(lo,min(xs)-1.1),max(hi,max(xs)+1.1))
            lo,hi=self.ax.get_ylim();self.ax.set_ylim(min(lo,min(ys)-.6),max(hi,max(ys)+.6))
        for ext in ['svg','png']:
            self.fig.savefig(OUT/(self.key+'.'+ext),dpi=210,bbox_inches='tight',pad_inches=.18,facecolor='white')
        svg=OUT/(self.key+'.svg');svg.write_bytes(('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n').encode('utf-8'))
        plt.close(self.fig)
        records.append({'id':self.key,'title':self.title,'page':page,'note':note,'svg':self.key+'.svg','png':self.key+'.png','components':self.components,'wires':self.wires,'运放内部穿线检查':'通过' if self.key!='OP-symbol' else '电源引脚按符号规范接入'})

for suffix in ['a','b']:
    c=Circuit('B19-'+suffix,'共射电路等效变换 ('+suffix+')',size=(10,6));t=c.bjt((5,3),'');em,co,ba=t.emitter,t.collector,t.base
    c.part('R',(0,3),(2,3),r'$R_s=600\,\Omega$');c.part('C',(2,3),(4,3),None);c.wire((4,3),ba);c.part('S',(0,.3),(0,3),'$u_s$',offset=-.9)
    c.text(-.7,2.35,'$+$');c.text(-.7,.85,'$-$')
    c.part('R',(4,6),(4,3),r'$910\,\mathrm{k}\Omega$',offset=-.4);c.wire((4,3),ba);c.dot((4,3));c.supply((4,6),r'$18\,\mathrm{V}$')
    c.part('R',(co.x,6),co,r'$3\,\mathrm{k}\Omega$' if suffix=='a' else "$R'$")
    c.supply((co.x,6),r'$18\,\mathrm{V}$' if suffix=='a' else "$+U'_{CC}$")
    c.wire(em,(em.x,.3),(0,.3));c.ground((em.x,.3));c.wire(co,(9,co.y));c.dot(co);c.port((9,co.y),r'$+\quad u_o$','right');c.port((9,.3),'$-$','right');c.wire((em.x,.3),(9,.3))
    c.dot((em.x,.3))
    if suffix=='a':
        c.wire((4,6),(co.x,6));c.dot((4,6));c.dot((co.x,6))
        c.part('R',(8,co.y),(8,.3),r'$3\,\mathrm{k}\Omega$');c.dot((8,co.y));c.dot((8,.3))
    c.save('',5)


def b20():
    c=Circuit('B20','分压偏置共射放大电路',size=(12,7));t=c.bjt((5,3.7),'');co,em,ba=t.collector,t.emitter,t.base;top=6.7;bottom=.4
    c.wire((3,top),(em.x,top));c.supply((em.x,top),'$+V_{CC}$');c.part('R',(em.x,top),co,'$R_C$');c.wire(ba,(3,ba.y));c.dot((3,ba.y))
    c.part('R',(3,top),(3,ba.y),'$R_{b2}$',offset=-.4);c.part('R',(3,ba.y),(3,bottom),'$R_{b1}$',offset=-.4)
    c.part('C',(.5,ba.y),(3,ba.y),'$C_1$');c.port((.5,ba.y),r'$+\quad u_i$');c.wire(em,(em.x,2.3));c.dot((em.x,2.3))
    c.part('R',(em.x,2.3),(em.x,bottom),'$R_e$',offset=-.4);c.wire((em.x,2.3),(8,2.3));c.part('C',(8,2.3),(8,bottom),'$C_e$')
    c.wire(co,(8,co.y));c.dot(co);c.part('C',(8,co.y),(10.5,co.y),'$C_2$');c.part('R',(10.5,co.y),(10.5,bottom),'$R_L$')
    c.wire((.5,bottom),(11.5,bottom));c.wire((10.5,co.y),(11.5,co.y));c.dot((10.5,co.y))
    for x in [3,em.x,8,10.5]:c.dot((x,bottom))
    c.port((.5,bottom),'$-$');c.port((11.5,co.y),r'$+\quad u_o$','right');c.port((11.5,bottom),'$-$','right');c.ground((em.x,bottom));c.save('',6)
b20()


def b21(key='B21',page=6):
    c=Circuit(key,'共源放大电路');t=c.d.add(E.NMos().at((5,3)).anchor('gate'));g,dr,sr=t.gate,t.drain,t.source
    c.text(dr.x+.45,3.15,'$T$',ha='left')
    c.part('R',dr,(dr.x,6),r'$R_d=3\,\mathrm{k}\Omega$');c.supply((dr.x,6),r'$+V_{DD}=12\,\mathrm{V}$');c.wire(dr,(8,dr.y));c.dot(dr);c.port((8,dr.y),r'$+\quad u_o$','right')
    c.wire(sr,(sr.x,.3),(1,.3));c.wire((sr.x,.3),(8,.3));c.ground((sr.x,.3));c.port((8,.3),'$-$','right')
    c.part('R',(1,g.y),g,r'$R_g=2\,\mathrm{M}\Omega$');c.part('S',(1,1.6),(1,g.y),'$u_i$',offset=-.9);c.part('B',(1,.3),(1,1.6),r'$V_{GG}=6\,\mathrm{V}$',True,offset=-.4)
    c.text(.3,2.75,'$+$');c.text(.3,1.8,'$-$');c.dot((sr.x,.3))
    c.save('',page)
b21()


c=Circuit('C2','反相积分电路');n,p,o=c.op(4,3)
c.part('R',(0,n.y),n,'$R$');c.port((0,n.y),'$u_i$');c.wire(n,(3,n.y),(3,5));c.part('C',(3,5),(8,5),'$C$');c.wire((8,5),(8,3),o);c.wire((8,3),(9,3));c.port((9,3),'$u_o$','right');c.dot((8,3));c.dot(n)
c.part('R',(1,p.y),p,None);c.ground((1,p.y));c.dot((3,n.y));c.save('',13)


c=Circuit('C5','双运放差分输出',size=(11,8));n1,p1,o1=c.op(3,6,plus_top=True,label='A_1');n2,p2,o2=c.op(3,1,label='A_2')
c.part('R',(0,p1.y),p1,'$R$');c.port((0,p1.y),'$U_1$');c.part('R',(0,p2.y),p2,'$R$');c.port((0,p2.y),'$U_2$')
c.wire(o1,(8,6));c.wire(o2,(8,1));c.part('R',(8,6),(8,4.3),'$R$');c.part('R',(8,4.3),(8,2.7),'$R$');c.part('R',(8,2.7),(8,1),'$R$')
c.wire(n1,(2,n1.y),(2,4.3),(8,4.3));c.wire(n2,(1.3,n2.y),(1.3,2.7),(8,2.7));c.dot((8,4.3));c.dot((8,2.7));c.wire((8,6),(10,6));c.wire((8,1),(10,1));c.dot((8,6));c.dot((8,1));c.port((10,6),'$+$','right');c.port((10,1),'$-$','right');c.text(10.3,3.5,'$u_o$',ha='left');c.save('',10)

c=Circuit('C9','反相求和比较器与稳压限幅',size=(12,7));n,p,o=c.op(5,3)
c.part('R',(0,n.y),n,'$R_2$');c.port((0,n.y),'$U_I$');c.wire(n,(4,n.y),(4,5.5));c.part('R',(0,5.5),(4,5.5),'$R_1$');c.port((0,5.5),'$U_{REF}$');c.dot(n);c.wire(p,(4,p.y));c.ground((4,p.y))
c.part('R',o,(10,3),None);c.wire((10,3),(11.5,3));c.port((11.5,3),'$u_o$','right');c.dot((10,3));c.part('Z',(10,1.7),(10,3),'$D_{z1}$');c.part('Z',(10,1.7),(10,.4),'$D_{z2}$');c.ground((10,.4))
c.dot((4,n.y));c.save('',10)

c=Circuit('C12','同相输入 RC 低通与输出反馈');n,p,o=c.op(4,3,plus_top=True)
c.part('R',(0,p.y),(2.5,p.y),'$R_1$');c.wire((2.5,p.y),p);c.port((0,p.y),'$u_i$');c.part('C',(2.5,p.y),(2.5,1),'$C_1$',offset=-.4);c.ground((2.5,1));c.dot((2.5,p.y))
c.wire(n,(3.4,n.y),(3.4,.1));c.part('R',(3.4,.1),(8,.1),'$R_f$',offset=-.35);c.wire((8,.1),(8,3),o);c.wire((8,3),(9,3));c.dot((8,3));c.port((9,3),'$u_o$','right');c.save('',9)

c=Circuit('C13','运放与 BJT 复合反馈电路',size=(11,6));n,p,o=c.op(4,3.5,plus_top=True)
t=c.bjt((o.x+1,3.5),'Q_1');c.wire(o,t.base);c.wire(t.collector,(t.collector.x,6));c.supply((t.collector.x,6),'$V_{CC}$');c.wire(t.emitter,(t.emitter.x,2));c.part('R',(t.emitter.x,2),(t.emitter.x,0),'$R_3$');c.ground((t.emitter.x,0));c.dot((t.emitter.x,2));c.wire((t.emitter.x,2),(10,2));c.port((10,2),'$u_o$','right')
c.wire(n,(3,n.y),(3,2));c.part('R',(3,2),(t.emitter.x,2),'$R_2$');c.part('R',(3,2),(3,0),'$R_1$',offset=-.4);c.ground((3,0));c.dot((3,2));c.wire((1,p.y),p);c.port((1,p.y),'$u_i$');c.save('',9)

c=Circuit('C14','反相有源高通滤波电路');n,p,o=c.op(5,3)
c.port((0,n.y),'$u_i$');c.part('R',(0,n.y),(2.5,n.y),'$R$');c.part('C',(2.5,n.y),n,'$C$');c.dot(n);c.wire(n,(4,n.y),(4,5.3));c.dot((4,n.y));c.part('R',(4,5.3),(9,5.3),'$R_F$');c.wire((9,5.3),(9,3),o);c.dot((9,3));c.wire((9,3),(10,3));c.port((10,3),'$u_o$','right');c.part('R',(2,p.y),p,'$R_2$');c.ground((2,p.y));c.save('',9)

c=Circuit('C15','同相有源高通滤波电路');n,p,o=c.op(5,3)
c.part('C',(0,p.y),(3,p.y),'$C$');c.port((0,p.y),'$u_i$');c.wire((3,p.y),p);c.dot((3,p.y));c.part('R',(3,p.y),(3,.3),'$R$',offset=-.4);c.ground((3,.3))
c.part('R',(1,n.y),n,'$R_1$');c.ground((1,n.y));c.wire(n,(4,n.y),(4,5.3));c.dot((4,n.y));c.part('R',(4,5.3),(9,5.3),'$R_f$');c.wire((9,5.3),(9,3),o);c.dot(n);c.dot((9,3));c.wire((9,3),(10,3));c.port((10,3),'$u_o$','right');c.save('',9)


(OUT/'geometry.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
