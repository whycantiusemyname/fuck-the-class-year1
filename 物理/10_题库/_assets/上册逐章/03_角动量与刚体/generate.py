"""刚体题图生成源。依赖相邻02章的基础绘图工具，均随仓库交付。
除题给标注外均为定性示意；未给定半径比、杆长比、角度及箭头大小不作测量。
运行 python generate.py。
"""
from pathlib import Path
import importlib.util,numpy as np
from matplotlib.patches import Circle,Arc,Ellipse
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('mechanics_primitives',HERE.parent/'02_动力学与守恒/generate.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.O=HERE
canvas,L,A,T,rect,ground,wall,ceiling,dim,save=[getattr(m,n) for n in ['canvas','L','A','T','rect','ground','wall','ceiling','dim','save']]
def compare_pulleys():
 f,a=canvas((6.8,4.8),(-.5,8.8,-.5,5.4))
 for cx,t in [(2,'$A$'),(6,'$B$')]:
  ceiling(a,cx-1.3,cx+1.3,4.8);L(a,(cx,4.8),(cx,3.3));a.add_patch(Circle((cx,3.3),.72,fill=False,lw=1.8));T(a,cx-1.0,3.3,t);L(a,(cx-.72,3.3),(cx-.72,.8))
 rect(a,.83,.1,.9,.7,'$M$');A(a,(5.28,.8),(5.28,-.1));T(a,5.85,.20,'$F$');save(f,4)
def hole_table(n):
 f,a=canvas((6,4),(-.5,7.6,-1.3,4.0));L(a,(.1,1.5),(6.6,1.5));L(a,(.1,1.25),(6.6,1.25));L(a,(.5,1.25),(.5,-.3));L(a,(6.3,1.25),(6.3,-.3));rect(a,4.7,1.5,1.1,.65)
 L(a,(2.4,1.5),(4.7,1.82));A(a,(2.4,1.5),(2.4,-.65));T(a,2.1,1.9,'$O$');T(a,2.75,-.75,'$v$');dim(a,(2.4,2.9),(5.2,2.9),'$R$',(0,.3));L(a,(2.4,2.5),(2.4,3.2),lw=1.1);L(a,(5.2,2.5),(5.2,3.2),lw=1.1);save(f,n)
def rod_bullet(n):
 f,a=canvas((4.8,5.5),(-1,3.9,-.8,5.3));ceiling(a,1,3.7,4.8);a.add_patch(Circle((2.35,4.5),.18,fill=False,lw=1.6));T(a,2.86,4.55,'$O$');rect(a,2.17,.2,.35,4.1);a.add_patch(Circle((-.2,2.3),.18,fill=False,lw=1.6));A(a,(.0,2.3),(1.6,2.3));save(f,n)
def concentric_forces():
 f,a=canvas((4.8,5.4),(-2.0,1.7,-2.4,1.8));a.add_patch(Circle((0,0),1.25,fill=False,lw=1.8));a.add_patch(Circle((0,0),.72,fill=False,lw=1.8));T(a,-.22,.22,'$A$');T(a,.18,1.02,'$B$')
 A(a,(0,0),(.60,.40));A(a,(0,0),(.86,.91));T(a,.39,.17,'$r_A$');T(a,.60,.93,'$r_B$');A(a,(-1.25,0),(-1.25,-2.0));A(a,(-.72,0),(-.72,-2.0));T(a,-1.56,-2.15,'$f_B$');T(a,-.42,-2.15,'$f_A$');save(f,16)
def impact_rod():
 f,a=canvas((6.6,3.8),(-.5,7.5,-1.4,3.9));rect(a,.5,2.0,5.5,.22);a.plot(3.25,2.11,'ko',ms=4);T(a,3.25,1.6,'$O$');T(a,1.1,1.45,'$m,l$');rect(a,6,.25,.26,.55);A(a,(6.8,.25),(6.8,1.55));T(a,7.1,1,'$v$');save(f,21)
def sliding_balls():
 f,a=canvas((6.8,3.4),(-.5,7.8,-1.3,3.2));rect(a,.4,1.1,6.8,.18);cx=3.8
 L(a,(cx,-.4),(cx,2.8),ls=(0,(4,3)),lw=1.1);T(a,4.05,2.5,'$O$')
 for x in [2.65,4.95]:a.add_patch(Circle((x,1.19),.25,color='white',ec='black',lw=1.6));L(a,(x,.7),(x,-.1),lw=1.0)
 dim(a,(2.65,.30),(cx,.30),'$d$',(0,-.38));dim(a,(cx,.30),(4.95,.30),'$d$',(0,-.38));dim(a,(.4,-.8),(7.2,-.8),'$l$',(0,-.3));save(f,22)
def axle_mass():
 f,a=canvas((4.8,5.4),(-1.8,2.3,-2.3,1.8));a.add_patch(Circle((0,0),1.25,fill=False,lw=1.8));a.add_patch(Circle((0,0),.65,fill=False,lw=1.8));a.plot(0,0,'ko',ms=4);T(a,-.28,-.15,'$O$')
 L(a,(0,0),(.65,0));T(a,.32,.22,'$r$');L(a,(.65,0),(.65,-1.5));rect(a,.25,-2.1,.8,.6,'$m$')
 a.add_patch(Arc((0,0),1.75,1.75,theta1=-45,theta2=10,color='black',lw=1.3));A(a,(.80,-.35),(.64,-.61));save(f,26)
def two_bullets():
 f,a=canvas((6.8,4.3),(-3.4,3.4,-1.8,1.8));a.add_patch(Circle((0,0),1.25,fill=False,lw=1.8));T(a,-.45,-.35,'$O$');a.plot(-.24,-.12,'ko',ms=3);T(a,.3,-.6,'$M$');L(a,(-2.4,.65),(2.4,.65),ls=(0,(4,3)),lw=1.1)
 for x in [-2.9,2.9]:T(a,x,1.12,'$m$')
 A(a,(-3.0,.65),(-1.8,.65));A(a,(3,.65),(1.8,.65));save(f,31)
def rod_opposite_balls():
 f,a=canvas((6,4),(-.4,7.3,-1.8,3.5));rect(a,.3,1,6,.2);a.plot(3.3,1.1,'ko',ms=4);T(a,3.3,1.55,'$O$');T(a,3.3,.65,'$m$')
 for x,y,v in [(.3,-.8,'$v$'),(6.3,2.35,'$v$')]:
  a.add_patch(Circle((x,y),.28,fill=False,lw=1.6))
  if x<1:A(a,(x,y+.28),(x,y+1.18));T(a,x+.4,y+.95,v)
  else:A(a,(x,y-.28),(x,y-1.1));T(a,x+.4,y-.85,v)
  T(a,x-.43,y,'$m$')
 save(f,36)
def one_body():
 f,a=canvas((3.5,4.8),(-1.4,1.4,-1.9,2.1));rect(a,-.4,-.3,.8,.6);a.plot(0,0,'ko',ms=4);A(a,(0,0),(0,1.65));A(a,(0,0),(0,-1.55));T(a,.45,1.72,"$T'$");T(a,.45,-1.65,'$mg$');save(f,41)
def atwood_masses():
 f,a=canvas((4.6,5.4),(-.7,4.4,-.5,5.2));ceiling(a,0,4,4.8);a.add_patch(Circle((2,3.3),.8,fill=False,lw=1.8));L(a,(2,4.8),(2,3.3));a.plot(2,3.3,'ko',ms=4);T(a,2.35,3.15,'$O$');L(a,(1.2,3.3),(1.2,.5));L(a,(2.8,3.3),(2.8,1.3));rect(a,.7,-.1,1,.6,'$m_1$');rect(a,2.3,.7,1,.6,'$m_2$');a.add_patch(Arc((2,3.3),2.3,2.3,theta1=135,theta2=190,color='black',lw=1.2));A(a,(.87,3.15),(.91,2.9));save(f,42)
def compound_pulley():
 f,a=canvas((4.6,5.4),(-1.9,2.0,-2.4,1.7));a.add_patch(Circle((0,0),1.25,fill=False,lw=1.8));a.add_patch(Circle((0,0),.65,fill=False,lw=1.8));a.plot(0,0,'ko',ms=4);T(a,.22,-.15,'$O$');L(a,(-1.25,0),(-1.25,-1.6));L(a,(.65,0),(.65,-1.6));rect(a,-1.65,-2.2,.8,.6,'$2m$');rect(a,.25,-2.2,.8,.6,'$m$');save(f,43)
if __name__=='__main__':
 compare_pulleys();concentric_forces();impact_rod();sliding_balls();axle_mass();two_bullets();rod_opposite_balls();one_body();atwood_masses();compound_pulley()
 for n in [7,17]:hole_table(n)
 for n in [14,19,23,33]:rod_bullet(n)
 print('16 SVG/PNG redrawn; unprovided scales remain qualitative')
