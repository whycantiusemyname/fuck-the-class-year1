"""Exact parametric geometry; run with Python, numpy and matplotlib."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':18,'svg.fonttype':'path','svg.hashsalt':'calculus-20261106'})
def canvas():
    f,a=plt.subplots(figsize=(6,5));a.set_aspect('equal');a.axis('off');return f,a
def curve(a,x,y,style='-',lw=1.5):a.plot(x,y,style,color='black',lw=lw)
def arrow(a,p,q):a.annotate('',xy=q,xytext=p,arrowprops=dict(arrowstyle='-|>',color='black',lw=1.5,mutation_scale=15))
def label(a,p,s,**kw):a.text(*p,s,ha='center',va='center',**kw)
def proj(x,y,z):return np.asarray(y)-.65*np.asarray(x),np.asarray(z)-.35*np.asarray(x)-.15*np.asarray(y)
def spacecurve(a,x,y,z,style='-',lw=1.5):curve(a,*proj(x,y,z),style,lw)
def axes(a,r):
    for p,s,offset in [((r,0,0),'$x$',(-.10,-.05)),((0,r,0),'$y$',(.10,0)),((0,0,r),'$z$',(-.12,.02))]:
        q=proj(*p);arrow(a,(0,0),q);label(a,(q[0]+offset[0],q[1]+offset[1]),s)
    label(a,(.13,.10),'$O$')
def save(f,n):
    f.savefig(OUT/(n+'.svg'),bbox_inches='tight',metadata={'Date':None});f.savefig(OUT/(n+'.png'),dpi=200,bbox_inches='tight');plt.close(f)
def hemisphere():
    f,a=canvas();t=np.linspace(0,2*np.pi,501)
    # Unit lower hemisphere, with an inward (upper-side) normal.
    for z in [-.35,-.7]:
        r=np.sqrt(1-z*z);spacecurve(a,r*np.cos(t),r*np.sin(t),z,'--',.55)
    v=np.linspace(0,np.pi/2,160)
    for phi in np.linspace(0,2*np.pi,6,endpoint=False):spacecurve(a,np.cos(v)*np.cos(phi),np.cos(v)*np.sin(phi),-np.sin(v),'--',.55)
    spacecurve(a,np.cos(t),np.sin(t),0,lw=1.8)
    axes(a,1.4)
    p=np.array([.65,-.45,-np.sqrt(1-.65**2-.45**2)]);q=.55*p
    arrow(a,proj(*p),proj(*q));xy=proj(*q);label(a,(xy[0]+.20,xy[1]-.05),r'$\hat{n}$')
    label(a,(-.15,-.86),'$S$');a.set_xlim(-1.5,1.6);a.set_ylim(-1.35,1.65);save(f,'lower-hemisphere')
def intersection():
    f,a=canvas();t=np.linspace(0,2*np.pi,801)
    spacecurve(a,2*np.cos(t),2*np.sin(t),0,lw=1.5)
    v=np.linspace(0,np.pi/2,180)
    for phi in np.linspace(0,2*np.pi,9,endpoint=False):spacecurve(a,2*np.cos(v)*np.cos(phi),2*np.cos(v)*np.sin(phi),2*np.sin(v),'--',.55)
    for z in [.55,1.1]:
        r=np.sqrt(4-z*z);spacecurve(a,r*np.cos(t),r*np.sin(t),z,'--',.55)
    for phi in [0,np.pi/2,np.pi,3*np.pi/2]:
        x=1+np.cos(phi);y=np.sin(phi);spacecurve(a,[x,x],[y,y],[0,np.sqrt(max(0,4-x*x-y*y))],'--',.75)
    spacecurve(a,1+np.cos(t),np.sin(t),0,'--',.9)
    x=1+np.cos(t);y=np.sin(t);z=2*np.sin(t/2)
    assert np.allclose(x*x+y*y+z*z,4) and np.allclose((x-1)**2+y*y,1)
    spacecurve(a,x,y,z,lw=2.1)
    # Increasing t is counterclockwise when viewed from +x towards -x.
    for k in [175,610]:arrow(a,proj(x[k],y[k],z[k]),proj(x[k+18],y[k+18],z[k+18]))
    axes(a,2.65);label(a,(-1.42,-.76),'$2$');label(a,(2.12,-.47),'$2$');label(a,(.16,2.13),'$2$');label(a,(-1.05,.68),r'$\Gamma$')
    a.set_xlim(-2.6,3);a.set_ylim(-1.4,3);save(f,'sphere-cylinder')
def path():
    f,a=canvas();arrow(a,(-1.3,0),(1.4,0));arrow(a,(0,-.2),(0,1.4));label(a,(1.38,-.12),'$x$');label(a,(-.12,1.38),'$y$');label(a,(-.10,-.13),'$O$')
    t=np.linspace(np.pi/2,np.pi,301);curve(a,np.cos(t),np.sin(t),lw=1.9);curve(a,[1,0],[0,1],lw=1.9)
    arrow(a,(.6,.4),(.42,.58));arrow(a,(np.cos(2.55),np.sin(2.55)),(np.cos(2.73),np.sin(2.73)))
    label(a,(1.03,-.15),'$A(1,0)$');label(a,(.34,1.07),'$B(0,1)$');label(a,(-1.05,-.15),'$C(-1,0)$')
    a.set_xlim(-1.5,1.6);a.set_ylim(-.35,1.6);save(f,'directed-path')
if __name__=='__main__':hemisphere();intersection();path()
