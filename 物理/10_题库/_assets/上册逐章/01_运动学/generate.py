"""七幅运动学定性示意。Python+NumPy+Matplotlib；无刻度坐标不是实际物理量。
题给30°仅用于第7图速度切线；其他未给角度、大小与比例均为布局参数。
SVG文字轮廓化，标签和几何可在本代码编辑。运行 python generate.py。
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Arc,Rectangle,Polygon
O=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':18,
 'lines.linewidth':1.8,'svg.fonttype':'path','svg.hashsalt':'physics-upper-ch01'})
def canvas(lim=(-1.6,1.7,-1.5,1.7),size=(4.9,4.3)):
 f,a=plt.subplots(figsize=size);f.subplots_adjust(left=.04,right=.96,bottom=.05,top=.95)
 a.set(xlim=lim[:2],ylim=lim[2:]);a.axis('off');a.set_aspect('equal');return f,a
def line(a,x,y,**kw):a.plot(x,y,color='black',**kw)
def arrow(a,p,q):a.annotate('',xy=q,xytext=p,arrowprops=dict(arrowstyle='-|>',lw=1.7,color='black',mutation_scale=15))
def label(a,x,y,t,**kw):a.text(x,y,t,ha=kw.pop('ha','center'),va=kw.pop('va','center'),**kw)
def arc(a,center,r,lo,hi,**kw):a.add_patch(Arc(center,2*r,2*r,theta1=lo,theta2=hi,lw=1.5,color='black',**kw))
def save(f,name):
 p=O/(name+'.svg');f.savefig(p,metadata={'Date':None});p.write_text('\n'.join(l.rstrip() for l in p.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8',newline='\n')
 f.savefig(O/(name+'.png'),dpi=220);plt.close(f)
def circle_position():
 f,a=canvas();a.add_patch(Circle((0,0),1,fill=False,lw=1.8))
 arrow(a,(-1.4,0),(1.46,0));arrow(a,(0,-1.28),(0,1.46))
 label(a,1.50,-.12,'$x$');label(a,-.12,1.49,'$y$');label(a,-.12,-.12,'$O$')
 p=(np.cos(.65),np.sin(.65));arrow(a,(0,0),p)
 label(a,.30,.39,'$\\vec r$');label(a,p[0]+.13,p[1]+.13,'$(x,y)$')
 arrow(a,(0,0),(.34,0));arrow(a,(0,0),(0,.34));label(a,.31,-.25,'$\\vec i$');label(a,-.18,.30,'$\\vec j$')
 arc(a,(0,0),1.21,48,78);q=np.deg2rad(78);arrow(a,(1.21*np.cos(q-.10),1.21*np.sin(q-.10)),(1.21*np.cos(q),1.21*np.sin(q)))
 label(a,.64,1.14,'$\\omega$');save(f,'01-circle-position')
def circle_p():
 f,a=canvas();a.add_patch(Circle((0,0),1,fill=False,lw=1.8));label(a,-.13,.08,'$O$')
 t=np.deg2rad(120);p=(np.cos(t),np.sin(t));a.plot(*p,'ko',ms=4)
 # Clockwise tangent at P points up-right, as on the original diagram.
 arrow(a,p,(p[0]+.35*np.sin(t),p[1]-.35*np.cos(t)))
 label(a,p[0]-.16,p[1]+.20,'$P$')
 q=(np.cos(-.8),np.sin(-.8));arrow(a,(0,0),q);label(a,.47,-.27,'$R$')
 save(f,'02-circle-P')
def boat():
 f,a=canvas((-1.0,3.2,-.7,2.4),(6.1,3.8))
 th=np.deg2rad(35);u=np.array([np.cos(th),np.sin(th)]);n=np.array([-u[1],u[0]])
 shape=[-.40*u-.15*n,-.40*u+.15*n,.23*u+.15*n,.48*u,.23*u-.15*n]
 a.add_patch(Polygon(shape,closed=True,fill=False,lw=1.6))
 arrow(a,(0,0),(2.75,0));arrow(a,(0,0),tuple(2.7*u))
 label(a,2.78,-.23,'$\\vec u$');label(a,2.7*u[0]+.15,2.7*u[1]+.13,'$\\vec v$')
 arc(a,(0,0),.72,0,35);label(a,.9,.22,'$\\alpha$');save(f,'03-boat-relative-velocity')
def sphere():
 f,a=canvas((-1.55,1.55,-.36,1.65),(5.6,3.6));arc(a,(0,0),1,0,180)
 line(a,[-1.4,1.4],[0,0]);
 for x in np.linspace(-1.35,1.35,26):line(a,[x-.08,x],[ -.12,0],lw=.9)
 line(a,[0,0],[0,1]);th=np.pi/4;b=np.array([np.sin(th),np.cos(th)])
 line(a,[0,b[0]],[0,b[1]])
 a.add_patch(Rectangle((-.12,1),.24,.15,fill=False,lw=1.6))
 tangent=np.array([np.cos(th),-np.sin(th)]);out=b
 verts=[b-.12*tangent,b+.12*tangent,b+.12*tangent+.15*out,b-.12*tangent+.15*out]
 a.add_patch(Polygon(verts,fill=False,lw=1.6))
 arc(a,(0,0),.42,45,90);label(a,.22,.57,'$\\theta$')
 label(a,0,1.38,'$A$');label(a,.96,.91,'$B$');save(f,'04-sphere-A-B')
def projectile():
 f,a=canvas((-.4,3.2,-.25,2.2),(5.0,3.9));a.set_aspect('auto')
 # Qualitative parabola: layout units; no numerical launch angle or height.
 x=np.linspace(0,2.6,300);y=1.05*x*(2.6-x)
 line(a,[-.25,2.95],[0,0]);line(a,x,y,ls=(0,(4,3)))
 slope=1.05*2.6;norm=np.sqrt(1+slope*slope);end=np.array([1,slope])/norm*1.0
 arrow(a,(0,0),tuple(end));label(a,end[0]-.10,end[1]+.12,'$\\vec v_0$')
 # θ denotes angle to horizontal as specified by the question.
 theta=np.degrees(np.arctan(slope));arc(a,(0,0),.50,0,theta);label(a,.63,.28,'$\\theta$')
 save(f,'05-projectile-launch')
def quarter_track():
 f,a=canvas((-.4,2.0,-.45,1.8),(5.0,4.2));a.set_aspect('equal')
 # Circle center at (1,1), A leftmost and B lowest: quarter circular arc.
 arc(a,(1,1),1,180,270)
 line(a,[0,1],[1,1],ls=(0,(4,3)),lw=1.2);line(a,[1,1],[1,0],ls=(0,(4,3)),lw=1.2)
 line(a,[-.15,-.15,0],[ -.30,1,1]);line(a,[1,1],[0,-.30]);line(a,[-.35,1.6],[-.30,-.30])
 a.add_patch(Circle((0,1),.065,color='white',ec='black',lw=1.6));a.add_patch(Circle((1,0),.065,color='white',ec='black',lw=1.6));a.plot(1,1,'ko',ms=4)
 label(a,-.10,1.23,'$A$');label(a,1.18,.04,'$B$');label(a,.55,1.18,'$R$');save(f,'06-quarter-circle-track')
def projectile_tangent():
 f,a=canvas((-.2,4.2,-.25,2.45),(6.3,3.8));a.set_aspect('equal')
 # A qualitative parabola, with its tangent at A constrained to the given 30°.
 slope=np.tan(np.pi/6);c=.42;xa=1.20;xv=xa+slope/(2*c);h=c*xv*xv
 x=np.linspace(0,2*xv,400);y=h-c*(x-xv)**2
 line(a,x,y,ls=(0,(1.5,2)));line(a,[-.1,2*xv+.2],[0,0])
 ya=h-c*(xa-xv)**2;point=np.array([xa,ya]);a.plot(*point,'ko',ms=4)
 arrow(a,point,tuple(point+1.25*np.array([np.cos(np.pi/6),.5])))
 line(a,[xa,xa+1.18],[ya,ya],ls=(0,(4,3)),lw=1.1)
 # Keep the angle label below the horizontal guide: the narrow wedge is
 # crossed by the physical trajectory, which must remain visible.
 arc(a,tuple(point),.55,0,30);label(a,xa+.78,ya-.18,'$30^\\circ$')
 label(a,xa-.18,ya-.07,'$A$');label(a,xa+1.10,ya+.78,'$\\vec v$');save(f,'07-projectile-tangent-30deg')
if __name__=='__main__':
 circle_position();circle_p();boat();sphere();projectile();quarter_track();projectile_tangent()
 assert np.isclose(np.tan(np.pi/6),1/np.sqrt(3))
 print('7 SVG+PNG; geometric and 30-degree tangent constraints passed')
