"""波动题图。几何图是定性示意；只有029按给定刻度绘制定量正弦曲线。"""
from pathlib import Path
import importlib.util,numpy as np
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('base',H.parent/'02_动力学与守恒/generate.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.O=H
canvas,L,A,T,save=[getattr(m,k) for k in ['canvas','L','A','T','save']]

def axis(n):
 f,a=canvas((6,2.6),(-.5,7,-.7,2));A(a,(-.3,0),(6.7,0));T(a,6.7,-.35,'$x$')
 for x,t in [(1,'B'),(3.4,'A')]:L(a,(x,0),(x,.23));T(a,x,-.42,'$'+t+'$')
 A(a,(5.6,1),(1.6,1));T(a,3.5,1.4,'$u$');save(f,n)

def sources(n):
 # Positions serve layout only. Ray lengths and included angle are not data.
 f,a=canvas((5.5,3.5),(-.6,6,-.6,3.5));p=(5,2.8)
 for q,label,r in [((.3,2.8),'S_1','r_1'),((.3,.2),'S_2','r_2')]:
  L(a,q,p);a.plot(*q,'ko',ms=5);T(a,q[0]-.1,q[1]+.35,'$'+label+'$')
  d=np.array(p)-q;A(a,tuple(np.array(q)+.40*d),tuple(np.array(q)+.60*d));mid=np.array(q)+.47*d;T(a,mid[0],mid[1]+.35,'$'+r+'$')
 a.plot(*p,'ko',ms=5);T(a,5.2,3.12,'$P$');save(f,n)

def vibration():
 f,a=canvas((6.6,3.9),(-.6,5.3,-2.65,2.8));a.set_aspect('auto');A(a,(-.4,0),(5.1,0));A(a,(0,-2.5),(0,2.55));T(a,-.06,2.7,'$y/\\mathrm{cm}$',ha='right');T(a,5.1,-.38,'$t/\\mathrm{s}$',ha='right');T(a,-.17,-.25,'$O$')
 t=np.linspace(0,4.7,600);a.plot(t,2*np.sin(np.pi*t/2),color='black',lw=1.8);L(a,(0,2),(1,2),ls=(0,(4,3)),lw=1.1);T(a,-.20,2,'$2$',ha='right')
 for x in [2,4]:T(a,x,.30,'$'+str(x)+'$')
 assert np.allclose(2*np.sin(np.pi*np.array([0,1,2,3,4])/2),[0,2,0,-2,0],atol=1e-10)
 save(f,29)

if __name__=='__main__':
 axis(12);axis(33);axis(48);sources(30);vibration()
