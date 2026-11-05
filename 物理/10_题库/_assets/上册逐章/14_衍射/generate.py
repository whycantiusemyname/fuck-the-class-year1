"""单缝、透镜和屏的定性位置图；仅保留符号a、f，不赋予数值比例。"""
from pathlib import Path
import importlib.util
from matplotlib.patches import Ellipse,Rectangle
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('base',H.parent/'02_动力学与守恒/generate.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.O=H
canvas,L,A,T,save=[getattr(m,k) for k in ['canvas','L','A','T','save']]
m.plt.rcParams['font.size']=23
if __name__=='__main__':
 f,a=canvas((6.3,5.7),(-1,8,-4.1,3.7))
 for y in [-1.5,0,1.5]:A(a,(-.8,y),(.6,y))
 T(a,-.2,2.2,'$\\lambda$')
 for y in [.55,-2.5]:a.add_patch(Rectangle((1,y),.28,1.95,fill=False,hatch='///',lw=1.5))
 a.annotate('',xy=(.85,.55),xytext=(.85,-.55),arrowprops=dict(arrowstyle='<->',lw=1.2));T(a,1.4,0,'$a$')
 a.add_patch(Ellipse((3.5,0),.45,4.3,fill=False,lw=1.7));T(a,3.5,2.7,'$L$');L(a,(2.8,0),(7.3,0));L(a,(7.3,-1.9),(7.3,2.7));T(a,7.3,3.1,'$C$')
 a.annotate('',xy=(3.5,-2.25),xytext=(7.3,-2.25),arrowprops=dict(arrowstyle='<->',lw=1.2));T(a,5.4,-2.2,'$f$',bbox=dict(facecolor='white',edgecolor='none',pad=2))
 A(a,(1,-3.65),(1,-2.8));A(a,(1,-3.65),(4.8,-3.65));T(a,.65,-3.85,'$O$');T(a,.7,-2.9,'$y$');T(a,5,-3.65,'$x$');save(f,2)
