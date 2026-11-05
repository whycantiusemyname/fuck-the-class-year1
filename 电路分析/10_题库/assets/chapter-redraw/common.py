"""Deterministic SVG/PNG redraws; sources and certified conversion are read-only."""
from pathlib import Path
import json,shutil,hashlib
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as E
from matplotlib.path import Path as GeometryPath
from PIL import Image,ImageDraw,ImageFont

COURSE=Path(__file__).resolve().parents[3]
ROOT=COURSE/'10_题库/assets/电子线路期末复习'
OUT=Path(__file__).resolve().parent
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
        elm={'R':E.ResistorIEC,'C':E.Capacitor,'D':E.Diode,'Z':E.Zener,'V':E.SourceV,'S':E.Source,'B':E.BatteryCell,'L':E.Inductor,'AC':E.SourceSin}[kind]()
        if reverse:elm.reverse()
        if kind in ['V','S','AC']:elm.theta(math.degrees(math.atan2(b[1]-a[1],b[0]-a[0])))
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
