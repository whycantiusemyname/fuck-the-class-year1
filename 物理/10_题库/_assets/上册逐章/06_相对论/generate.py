"""相对论参考系定性示意；未给出的坐标间距与箭长不表示测量值。"""
from pathlib import Path
import importlib.util
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('base',H.parent/'02_动力学与守恒/generate.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.O=H
canvas,A,T,save=[getattr(m,k) for k in ['canvas','A','T','save']]
if __name__=='__main__':
 f,a=canvas((6,4),(-.6,6.7,-.7,4.8));A(a,(0,0),(0,4.2));A(a,(1.7,0),(1.7,4.2));A(a,(0,0),(6.2,0));T(a,-.3,4,'$S$');T(a,1.4,4,'$S\prime$');T(a,5,-.35,'$x$');T(a,6.15,-.35,'$x\prime$');A(a,(1.7,2.8),(3.8,2.8));T(a,3,3.2,'$u$');A(a,(3.4,1.6),(5.4,1.6));T(a,5.2,1.2,'$v\prime$');save(f,4)
