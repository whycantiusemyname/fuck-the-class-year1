"""动力学与守恒题图。无刻度图均为定性示意，箭长不表示力大小。
Python + NumPy + Matplotlib。运行 python generate.py。
采用源题的符号、方向、几何约束；无题设数值的角度仅为布局参数。
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Arc,Rectangle,Ellipse
O=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':18,
 'lines.linewidth':1.8,'svg.fonttype':'path','svg.hashsalt':'upper-ch02'})
def canvas(size=(6,3.8),bounds=(-.7,8.2,-.8,4.8)):
 f,a=plt.subplots(figsize=size);f.subplots_adjust(left=.04,right=.96,bottom=.06,top=.94)
 a.set(xlim=bounds[:2],ylim=bounds[2:]);a.axis('off');a.set_aspect('equal');return f,a
def L(a,p,q,**kw):a.plot([p[0],q[0]],[p[1],q[1]],color='black',**kw)
def A(a,p,q):a.annotate('',xy=q,xytext=p,arrowprops=dict(arrowstyle='-|>',color='black',lw=1.7,mutation_scale=15))
def T(a,x,y,s,**kw):a.text(x,y,s,ha=kw.pop('ha','center'),va=kw.pop('va','center'),**kw)
def rect(a,x,y,w,h,t=None):
 a.add_patch(Rectangle((x,y),w,h,fill=False,lw=1.8))
 if t:T(a,x+w/2,y+h/2,t)
def ground(a,x0,x1,y):
 L(a,(x0,y),(x1,y))
 for x in np.arange(x0+.1,x1,.25):L(a,(x-.15,y-.18),(x,y),lw=.9)
def wall(a,x,y0,y1):
 L(a,(x,y0),(x,y1))
 for y in np.arange(y0+.1,y1,.25):L(a,(x-.18,y-.12),(x,y),lw=.9)
def ceiling(a,x0,x1,y):
 L(a,(x0,y),(x1,y))
 for x in np.arange(x0+.1,x1,.25):L(a,(x,y),(x+.15,y+.18),lw=.9)
def spring(a,p,q,amp=.14,n=9):
 p=np.array(p,float);q=np.array(q,float);v=q-p;length=np.linalg.norm(v);u=v/length;normal=np.array([-u[1],u[0]])
 points=[p,p+.10*v]
 for i in range(2*n+1):points.append(p+(.15+.70*i/(2*n))*v+((-1)**i)*amp*normal)
 points.extend([p+.90*v,q]);points=np.array(points);a.plot(points[:,0],points[:,1],color='black',lw=1.6)
def dim(a,p,q,s,offset=(0,0)):
 a.annotate('',xy=q,xytext=p,arrowprops=dict(arrowstyle='<->',lw=1.2,color='black'))
 mid=(np.array(p)+q)/2+offset;T(a,*mid,s)
def save(f,n):
 p=O/(f'{n:03}.svg');f.savefig(p,metadata={'Date':None});p.write_text('\n'.join(x.rstrip() for x in p.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8',newline='\n');f.savefig(O/(f'{n:03}.png'),dpi=220);plt.close(f)
def two_blocks():
 f,a=canvas();ground(a,.2,7,0);rect(a,2.2,0,1.4,1.3,'$m_1$');rect(a,3.6,0,2.0,2.3,'$m_2$')
 for y in [.7,1.8]:A(a,(.6,y),(2.2 if y<1 else 3.6,y));T(a,.7,y+.36,'$\\vec F$')
 save(f,1)
def wall_block():
 f,a=canvas((4.4,4),(-.7,4,-.5,4));wall(a,.3,.0,3.7);rect(a,.3,1,1.6,1.7,'$A$');A(a,(3.6,1.85),(1.9,1.85));T(a,2.9,1.40,'$F$');save(f,2)
def pulley_accel():
 f,a=canvas((4.6,5.4),(-.5,4.5,-.8,5.1));ceiling(a,.1,4,4.7);a.add_patch(Circle((2,3.6),.72,fill=False,lw=1.8));L(a,(2,4.7),(2,3.6))
 L(a,(1.28,3.6),(1.28,.8));rect(a,.85,.1,.86,.7,'$m_1$');L(a,(2.72,3.6),(2.72,1.05));a.add_patch(Ellipse((2.72,1.05),.7,.28,fill=False,lw=1.6));T(a,2.05,1.05,'$m_2$');A(a,(3.7,1.8),(3.7,.3));T(a,4.1,1,'$\\vec a_2$');save(f,3)
def conical():
 f,a=canvas((5,4.8),(-.7,4.9,-.7,4.7));ceiling(a,.0,4.5,4.3);p=np.array([2.5,4.3]);q=np.array([.5,.7]);L(a,p,q);L(a,p,(2.5,.7),ls=(0,(4,3)),lw=1.1)
 a.add_patch(Ellipse((2.5,.7),4,.70,fill=False,lw=1.6));a.plot(*q,'ko',ms=5)
 T(a,.2,.75,'$m$');T(a,1.2,2.55,'$l$');a.add_patch(Arc(tuple(p),1.8,1.8,theta1=241,theta2=270,color='black',lw=1.3));T(a,2.12,3.2,'$\\theta$');save(f,6)
def springs_three():
 f,a=canvas((4,6),(-1.1,3,-.5,6));ceiling(a,.2,2.8,5.6);T(a,1.5,5.95,'$O$');spring(a,(1.5,5.6),(1.5,4.4));rect(a,1.12,3.9,.76,.5,'$m_1$');T(a,2.25,4.15,'$A$')
 spring(a,(1.5,3.9),(1.5,2.3));rect(a,1.12,1.8,.76,.5,'$m_2$');rect(a,1.12,1.3,.76,.5,'$m_3$');T(a,2.25,2.05,'$B$');T(a,2.25,1.55,'$C$');A(a,(-.4,5.6),(-.4,.4));T(a,-.65,.35,'$x$');save(f,7)
def moving_circle():
 f,a=canvas((5,4.8),(-1.8,1.8,-1.8,1.8));a.add_patch(Circle((0,0),1.25,fill=False,lw=1.6,ls=(0,(4,3))));p=np.array([-.82,.94]);L(a,(0,0),p);L(a,(0,0),(0,1.25),ls=(0,(4,3)),lw=1.1)
 a.add_patch(Circle(tuple(p),.11,color='white',ec='black',lw=1.5));A(a,p,tuple(p+np.array([-.65,-.57])));T(a,-1.54,.15,'$\\vec v$');T(a,-.8,1.2,'$m$');T(a,-.31,.45,'$R$');T(a,.20,-.15,'$O$');a.add_patch(Arc((0,0),1.1,1.1,theta1=90,theta2=131,color='black',lw=1.2));T(a,-.25,.78,'$\\theta$');save(f,8)
def ab_spring(n,style='base'):
 f,a=canvas();ground(a,.2,7.6,0);wall(a,.25,0,2.8) if style in ['base','tie'] else None
 if style=='force':leftlabel,rightlabel='$B$','$A$'
 elif style in ['mass','tie']:leftlabel,rightlabel='$m_1$','$m_2$'
 elif style=='mAB':leftlabel,rightlabel='$m_A$','$m_B$'
 else:leftlabel,rightlabel='$A$','$B$'
 rect(a,.4,0,1.2,1.35,leftlabel);rect(a,5.1,0,1.2,1.35,rightlabel);spring(a,(1.6,.65),(5.1,.65),.22)
 if style=='base':T(a,.95,1.70,'$m_1$');T(a,5.7,1.70,'$m_2$');T(a,3.35,1.5,'$k$')
 if style=='tie':L(a,(1.6,1.0),(2.3,1.55));L(a,(2.3,1.55),(4.4,1.55));L(a,(4.4,1.55),(5.1,1));T(a,1,1.8,'$A$');T(a,5.7,1.8,'$B$')
 if style=='force':A(a,(6.3,.65),(7.8,.65));T(a,7.4,1.15,'$\\vec F$');A(a,(.3,-.15),(7.8,-.15));T(a,7.8,-.5,'$x$')
 save(f,n)
def L_spring():
 f,a=canvas((5,5.3),(-1.0,4.5,-.8,4.8));p=(.5,3.8);spring(a,p,(3.4,3.8));spring(a,p,(.5,.5));a.add_patch(Circle((3.6,3.8),.18,fill=False,lw=1.5));a.add_patch(Circle((.5,.3),.18,fill=False,lw=1.5))
 T(a,.18,4,'$O$');T(a,3.95,3.9,'$A$');T(a,3.65,3.35,'$m$');T(a,.93,.3,'$B$');T(a,.3,-.05,'$m$');T(a,2.05,3.35,'$k$')
 dim(a,(.5,4.35),(3.6,4.35),'$l_0$',(0,.25));dim(a,(-.25,3.8),(-.25,.3),'$l$',(-.25,0));save(f,11)
def chain(n):
 f,a=canvas((5,4.5),(-.5,5.5,-.8,4.2));ground(a,0,4,2.6);wall(a,4,.2,2.6)
 # Rounded links follow a right angle. Link count is illustrative, not specified.
 for x in np.linspace(.7,3.8,8):a.add_patch(Ellipse((x,2.73),.42,.22,fill=False,lw=1.4))
 for y in np.linspace(.9,2.43,5):a.add_patch(Ellipse((4.12,y),.22,.42,fill=False,lw=1.4))
 dim(a,(.5,3.5),(4,3.5),'$l-a$',(0,.28));dim(a,(4.9,2.6),(4.9,.65),'$a$',(.3,0));save(f,n)
def half_tube():
 f,a=canvas((4.3,5),(-1.7,1,-1.8,1.8));
 for r in [1.12,1.25]:a.add_patch(Arc((0,0),2*r,2*r,theta1=90,theta2=270,lw=1.8,color='black'))
 rect(a,.1,1.08,.45,.18);A(a,(.1,1.40),(-.65,1.40));T(a,.4,1.6,'$m$');T(a,.35,.72,'$v_0$');save(f,13)
def bullet_ab():
 f,a=canvas();ground(a,0,7.6,0);rect(a,3,0,1.4,2.6,'$A$');rect(a,4.4,0,1.4,2.6,'$B$');A(a,(.4,1.4),(2.3,1.4));rect(a,.1,1.3,.35,.2);save(f,15)
def stack():
 f,a=canvas();ground(a,.2,7.2,0);rect(a,2,0,3.6,1.25,'$B$');rect(a,2.5,1.25,1.8,1.1,'$A$');A(a,(4.3,1.8),(6.7,1.8));T(a,5.5,2.35,'$\\vec F$');save(f,21)
def offset_circle(n):
 f,a=canvas((4.6,4.8),(-1.7,2.1,-.6,3.3));a.add_patch(Circle((0,1.2),1.2,fill=False,lw=1.8));A(a,(-1.45,0),(1.7,0));A(a,(0,-.3),(0,3));T(a,1.8,-.15,'$x$');T(a,-.18,3.05,'$y$');T(a,-.20,-.18,'$O$');A(a,(0,1.2),(.95,1.92));T(a,.63,1.85,'$R$');save(f,n)
def drop_spring(n):
 f,a=canvas((4.2,5),(-.5,3.7,-.5,5));ground(a,.1,3.2,0);spring(a,(1.6,0),(1.6,2.2),.25);L(a,(.8,2.2),(2.5,2.2));rect(a,1.1,3.6,1, .7,'$m$');L(a,(.8,3.6),(2.5,3.6));dim(a,(.5,3.6),(.5,2.2),'$h$',(-.3,0));save(f,n)
def ladder():
 f,a=canvas((4.7,5),(-.8,4.0,-.5,4.7));ground(a,0,3.7,0);wall(a,0,0,4.4);L(a,(.12,3.8),(2.8,.12));L(a,(.24,3.86),(2.92,.18));T(a,.43,4.08,'$A$');T(a,3.15,.23,'$B$');a.add_patch(Arc((.12,3.8),1.5,1.5,theta1=270,theta2=306,color='black',lw=1.2));T(a,.50,2.72,'$\\theta$');save(f,27)
def horizontal_spring():
 f,a=canvas();ground(a,.2,7.4,0);wall(a,.25,0,2.4);spring(a,(.25,1),(3.8,1),.3);rect(a,3.8,0,1.6,1.8,'$m$');T(a,2.0,2,'$k$');A(a,(5.4,1),(7.3,1));T(a,6.6,1.6,'$\\vec F$');A(a,(3.3,0),(7.6,0));T(a,7.8,-.2,'$x$');T(a,4.6,-.35,'$O$');save(f,33)
def pull_block(n):
 f,a=canvas();ground(a,.2,7.4,0);rect(a,2,0,2.4,1.8,'$A$');p=(4.4,1.8);A(a,p,(6.7,3.1));L(a,p,(6.6,1.8),lw=1.1);a.add_patch(Arc(p,1.8,1.8,theta1=0,theta2=29.5,color='black',lw=1.2));T(a,5.5,2.12,'$\\theta$');T(a,6.8,3.5,'$F$');save(f,n)
def outward(n):
 f,a=canvas();ground(a,0,7.7,0)
 for x,label in [(2,'$m_1$'),(5.3,'$m_2$')]:a.add_patch(Circle((x,.38),.38,fill=False,lw=1.8));T(a,x,1.15,label)
 spring(a,(2.38,.38),(4.92,.38),.23);A(a,(1.62,.38),(.1,.38));A(a,(5.68,.38),(7.4,.38));T(a,.55,1,'$\\vec F$');T(a,6.9,1,'$\\vec F$');save(f,n)
def collision_spring():
 f,a=canvas();ground(a,0,7.6,0);wall(a,.25,0,2.7);spring(a,(.25,.70),(3.1,.70),.3);a.add_patch(Circle((3.8,.7),.7,fill=False,lw=1.8));T(a,3.8,.7,'$M$');rect(a,6.3,.45,.6,.3);T(a,6.6,1.25,'$m$');A(a,(6.2,.65),(4.8,.65));T(a,5.6,1.2,'$\\vec v$');save(f,37)
def pushed_blocks():
 f,a=canvas();ground(a,.2,7.5,0);rect(a,2,0,1.8,1.6,'$A$');rect(a,3.8,0,2.6,2.1,'$B$');A(a,(.6,2.7),(2,1.65));L(a,(.6,1.65),(2,1.65),ls=(0,(4,3)),lw=1.1);T(a,.55,3.1,'$\\vec F$');T(a,.65,2.0,'$36.9^\\circ$');save(f,38)
def two_vertical():
 f,a=canvas((4,5.5),(-.5,3.6,-.5,5.6));ceiling(a,.2,3.2,5.1);spring(a,(1.7,5.1),(1.7,3.6));spring(a,(1.7,3.6),(1.7,1.5));rect(a,1.2,.7,1,.8,'$m$');T(a,.5,4.3,'$A$');T(a,.5,2.6,'$B$');T(a,2.8,4.3,'$k_A$');T(a,2.8,2.6,'$k_B$');save(f,39)
def force_time():
 f,a=canvas((6.2,4.4),(-4,24,-8,14));a.set_aspect('auto');A(a,(-2,0),(23,0));A(a,(0,-7),(0,13));T(a,-.4,13.3,'$F/(\\mathrm{N})$',ha='right');T(a,23,-1.5,'$t/(\\mathrm{s})$',ha='right');T(a,-.8,-1,'$O$');L(a,(0,10),(10,0));L(a,(10,0),(20,-5));L(a,(0,-5),(20,-5),ls=(0,(4,3)),lw=1.1);L(a,(20,0),(20,-5),ls=(0,(4,3)),lw=1.1)
 for x,y,t in [(-.8,10,'10'),(-.8,5,'5'),(-.8,-5,'-5'),(10,-1.3,'10'),(20,1.3,'20')]:T(a,x,y,'$'+t+'$',ha='right' if x<0 else 'center')
 assert np.interp(10,[0,10,20],[10,0,-5])==0;save(f,41)
def bullet_block():
 f,a=canvas();ground(a,0,7.5,0);rect(a,3.8,0,2,1.8);rect(a,.6,.8,.5,.22);A(a,(.6,1.65),(2.4,1.65));T(a,1.5,2.1,'$v$');save(f,44)
def atwood():
 f,a=canvas((4.4,5.2),(-.7,4.5,-.4,5.2));ceiling(a,0,4,4.8);a.add_patch(Circle((2,3.3),.8,fill=False,lw=1.8));L(a,(2,4.8),(2,3.3));L(a,(1.2,3.3),(1.2,.9));L(a,(2.8,3.3),(2.8,.9));rect(a,.8,.25,.8,.65,'$A$');rect(a,2.4,.25,.8,.65,'$B$');save(f,53)
def beam():
 f,a=canvas();rect(a,1.3,1.4,4.6,.22);A(a,(1.5,1.62),(1.5,3.8));T(a,1.2,4.15,'$T_1$');A(a,(5.7,1.62),(5.7,3.1));T(a,6.0,3.5,'$T_2$');A(a,(3.2,1.4),(3.2,.2));T(a,2.8,.55,"$N'$");A(a,(3.6,1.4),(3.6,-.2));T(a,4,-.35,'$m_2g$');save(f,71)
if __name__=='__main__':
 two_blocks();wall_block();pulley_accel();conical();springs_three();moving_circle();L_spring();half_tube();bullet_ab();stack();ladder();horizontal_spring();collision_spring();pushed_blocks();two_vertical();force_time();bullet_block();atwood();beam()
 for n in [10,80]:ab_spring(n,'base')
 ab_spring(23,'mAB');ab_spring(40,'tie');ab_spring(49,'force');ab_spring(57,'mass')
 for n in [12,28]:chain(n)
 for n in [24,30,55]:offset_circle(n)
 for n in [25,45]:drop_spring(n)
 for n in [35,50]:pull_block(n)
 for n in [36,51]:outward(n)
 print('36 scientific SVG/PNG figures rendered')
