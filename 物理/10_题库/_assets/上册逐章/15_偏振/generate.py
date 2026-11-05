"""E、P1和P2方向与角标定性示意。内部布局角不代表给定数值。"""
from pathlib import Path
import importlib.util,numpy as np
from matplotlib.patches import Arc
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('base',H.parent/'02_动力学与守恒/generate.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.O=H
canvas,A,T,save=[getattr(m,k) for k in ['canvas','A','T','save']]
m.plt.rcParams['font.size']=24
if __name__=='__main__':
 f,a=canvas((6.3,4),(-.3,6.5,-.5,4.4));A(a,(0,0),(6,0));A(a,(0,0),(5.5,1.7));A(a,(0,0),(3.8,3.7));T(a,6.15,-.08,'$P_2$');T(a,5.8,1.8,'$P_1$');T(a,4,3.9,'$\\vec E$')
 e=np.degrees(np.arctan2(3.7,3.8));p=np.degrees(np.arctan2(1.7,5.5));a.add_patch(Arc((0,0),2.3,2.3,theta1=0,theta2=e,lw=1.3));T(a,1.23,.65,'$A$');a.add_patch(Arc((0,0),3.9,3.9,theta1=0,theta2=p,lw=1.3));T(a,2.13,.23,'$\\alpha$');save(f,4)
