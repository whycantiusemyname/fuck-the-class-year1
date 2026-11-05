"""振动题图：定量约束曲线与无刻度定性波形分开；布局参数不充作周期。
Python/NumPy/Matplotlib；几何工具来自同目录体系的02章。
"""
from pathlib import Path
import importlib.util,numpy as np
from matplotlib.patches import Circle,Arc
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('base',H.parent/'02_动力学与守恒/generate.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.O=H
canvas,L,A,T,rect,ground,wall,ceiling,spring,save=[getattr(m,k) for k in ['canvas','L','A','T','rect','ground','wall','ceiling','spring','save']]
def curve(n,mode):
 if mode=='cm12':bounds=(-2.0,17,-13,14);t=np.linspace(-1.0,15,700);y=10*np.cos(np.pi*t/6+np.pi/3);ylabel='$x/\\mathrm{cm}$'
 elif mode=='period4':bounds=(-.7,5.8,-8,8.7);t=np.linspace(0,5.1,600);y=-6*np.sin(np.pi*t/2);ylabel='$x/\\mathrm{cm}$'
 elif mode in ['m24','cm24']:bounds=(-.65,3.7,-5.8,6.0);t=np.linspace(0,3.4,600);y=4*np.cos(5*np.pi*t/6-np.pi/3);ylabel='$x/\\mathrm{m}$' if mode=='m24' else '$x/\\mathrm{cm}$'
 else:bounds=(-.8,11.9,-1.5,1.6);t=np.linspace(0,11,700);y=np.cos(t+(-np.pi/3 if mode=='vpositive' else 2*np.pi/3));ylabel='$v/(\\mathrm{m/s})$'
 f,a=canvas((6.8,3.9),bounds);a.set_aspect('auto');x0,x1,y0,y1=bounds
 A(a,(x0+.1,0),(x1-.15,0));A(a,(0,y0+.15),(0,y1-.2));T(a,-.10,y1-.1,ylabel,ha='right');T(a,x1-.15,y0*.28,'$t/\\mathrm{s}$',ha='right');T(a,-.13,y0*.12,'$O$',ha='right');a.plot(t,y,color='black',lw=1.8)
 def lab(x,y,s):T(a,x,y,s,fontsize=17,ha='right' if x<0 else 'center')
 if mode=='cm12':
  for x in [1,4,7,10,13]:lab(x,-1.0,'$'+str(x)+'$')
  for y in [10,5,-10]:lab(-.35,y,'$'+str(y)+'$')
  L(a,(0,10),(10,10),ls=(0,(4,3)),lw=1.1);L(a,(0,-10),(4,-10),ls=(0,(4,3)),lw=1.1)
  assert np.allclose(10*np.cos(np.pi*np.array([0,1,4,7,10,13])/6+np.pi/3),[5,0,-10,0,10,0],atol=1e-10)
 elif mode=='period4':
  for x in [1,2,3,4]:lab(x,-.7,'$'+str(x)+'$')
  lab(-.28,6,'$6$');lab(-.28,-6,'$-6$');assert np.allclose(-6*np.sin(np.pi*np.array([0,1,2,3,4])/2),[0,-6,0,6,0],atol=1e-10)
 elif mode in ['m24','cm24']:
  lab(-.20,4,'$4$');lab(-.20,2,'$2$');lab(1,-.6,'$1$');L(a,(0,4),(.4,4),ls=(0,(4,3)),lw=1.1)
  assert np.isclose(4*np.cos(-np.pi/3),2) and np.isclose(4*np.cos(5*np.pi/6-np.pi/3),0,atol=1e-10)
 else:
  # Internal phase parameter carries no numeric time scale; no t ticks are emitted.
  lab(-.35,1 if mode=='vpositive' else -1,'$v_m$' if mode=='vpositive' else '$-v_m$')
  lab(-.37,.5 if mode=='vpositive' else -.5,'$v_m/2$' if mode=='vpositive' else '$-v_m/2$')
  phase=-np.pi/3 if mode=='vpositive' else 2*np.pi/3
  trough=np.pi-phase;peak=-phase
  if mode=='vpositive':L(a,(0,1),(peak,1),ls=(0,(4,3)),lw=1.1)
  else:
   L(a,(0,-1),(trough,-1),ls=(0,(4,3)),lw=1.1);L(a,(trough,0),(trough,-1),ls=(0,(4,3)),lw=1.1);L(a,(2*np.pi-phase,0),(2*np.pi-phase,1),ls=(0,(4,3)),lw=1.1)
 save(f,n)
def opposing():
 f,a=canvas((6.6,3.9),(-.8,7.3,-1.4,1.5));a.set_aspect('auto');A(a,(-.6,0),(7.1,0));A(a,(0,-1.2),(0,1.35));T(a,-.2,1.3,'$x$');T(a,7,-.2,'$t$');T(a,-.12,-.15,'$O$')
 t=np.linspace(0,6.7,600);a.plot(t,-np.cos(t),color='black',lw=1.9);a.plot(t,.5*np.cos(t),color='black',lw=1.7,ls=(0,(5,2)))
 L(a,(0,.5),(6.4,.5),ls=(0,(3,3)),lw=.9);L(a,(0,-1),(6.4,-1),ls=(0,(3,3)),lw=.9);T(a,-.25,.5,'$A/2$');T(a,-.25,-1,'$-A$');T(a,6.35,-.9,'$x_1$');T(a,6.4,.88,'$x_2$');save(f,7)
def spring_pulley():
 f,a=canvas((4.4,5.4),(-.5,4.5,-.5,5.4));ceiling(a,0,4,4.9);a.add_patch(Circle((2,3.8),.7,fill=False,lw=1.7));L(a,(2,4.9),(2,3.8));L(a,(1.3,3.8),(1.3,2.0));spring(a,(1.3,2),(1.3,.1),.18);ground(a,.5,2.1,.1);L(a,(2.7,3.8),(2.7,1.9));rect(a,2.35,1.4,.7,.5);T(a,3.4,1.65,'$m$');rect(a,2.35,.6,.7,.5);a.patches[-1].set_linestyle((0,(4,3)));save(f,5)
def vector(n,angle,option=None):
 f,a=canvas((4.6,4.4),(-1.65,1.8,-1.5,1.6));a.add_patch(Circle((0,0),1,fill=False,lw=1.7));A(a,(0,0),(1.6,0));T(a,1.65,-.13,'$x$');T(a,-.16,-.1,'$O$');rad=np.deg2rad(angle);p=np.array([np.cos(rad),np.sin(rad)]);A(a,(0,0),tuple(p));T(a,*(.66*p+[-.12,.04]),'$A$');L(a,(p[0],-.08),(p[0],.08),lw=1.2);T(a,p[0],-.27 if p[0]>0 else .24,'$A/2$' if p[0]>0 else '$-A/2$')
 th=np.linspace(rad-.18,rad+.18,30);a.plot(1.22*np.cos(th),1.22*np.sin(th),color='black',lw=1.2);A(a,(1.22*np.cos(th[-2]),1.22*np.sin(th[-2])),(1.22*np.cos(th[-1]),1.22*np.sin(th[-1])));T(a,1.37*np.cos(rad),1.37*np.sin(rad),'$\\omega$')
 if option:T(a,-1.45,.1,'('+option+')')
 save(f,n)
if __name__=='__main__':
 curve(1,'m24');curve(2,'period4');curve(3,'cm12');curve(6,'vpositive');curve(10,'cm24');curve(14,'vnegative');opposing();spring_pulley()
 for n,ang,opt in [(20,60,'A'),(21,-60,'B'),(22,120,'C'),(23,240,'D'),(32,60,None),(33,-60,None),(34,120,None),(35,240,None)]:vector(n,ang,opt)
 print('16 vibration figures; quantitative constraints checked; uncalibrated graphs contain no numeric period')
