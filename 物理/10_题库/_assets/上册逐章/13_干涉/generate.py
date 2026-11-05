"""薄膜/劈尖定性几何。厚度、夹角与箭长仅作布局，不引入题设外数值。"""
from pathlib import Path
import importlib.util
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('base',H.parent/'02_动力学与守恒/generate.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.O=H
canvas,L,A,T,save=[getattr(m,k) for k in ['canvas','L','A','T','save']]
m.plt.rcParams['font.size']=24

def slab(n,numeric=False,silicon=False):
 f,a=canvas((6.8,3.9),(-.7,7,-1.4,3.4));L(a,(0,0),(6,0));L(a,(0,1.2),(6,1.2));L(a,(0,0),(0,1.2));L(a,(6,0),(6,1.2))
 for x in ([1.5,4.2] if n in [31,37] else [1,3,5]):A(a,(x,3),(x,1.2))
 if not silicon:T(a,3 if n!=31 else 1.2,3.15,'$\\lambda$')
 T(a,.65,2,'$n_1=1.00$' if numeric else ('$n_1=1$' if silicon else '$n_1$'),ha='right' if not numeric else 'center')
 T(a,3,.65,'$n_2=1.30$' if numeric else '$n_2$');T(a,3,-.55,'$n_3=1.50$' if numeric else '$n_3$')
 a.annotate('',xy=(6.35,1.2),xytext=(6.35,0),arrowprops=dict(arrowstyle='<->',color='black',lw=1.2));T(a,6.7,.6,'$e$')
 if silicon:
  T(a,1,.6,r'$\mathrm{SiO_2}$');T(a,1,-.55,r'$\mathrm{Si}$');L(a,(0,0),(0,-1));L(a,(0,-1),(6,-1));L(a,(6,0),(6,-1))
 save(f,n)

def wedge(n,incident=False):
 f,a=canvas((6.6,3.6),(-.6,7,-1.15,3.1));L(a,(0,0),(6,0));L(a,(0,0),(6,1.5));L(a,(6,0),(6,1.5));T(a,4,2.0,'$n_1$');T(a,4,.5,'$n_2$');T(a,4,-.55,'$n_3$')
 if incident:
  for x in ([1.7,3.5] if n==33 else [1.2,3,4.8]):A(a,(x,2.8),(x,x*.25))
  T(a,2.2,2.75,'$\\lambda$')
 if n==11:T(a,-.13,-.25,'$O$')
 save(f,n)

if __name__=='__main__':
 slab(2,True);slab(21);slab(31);slab(37,silicon=True)
 wedge(9);wedge(11,True);wedge(33,True)
