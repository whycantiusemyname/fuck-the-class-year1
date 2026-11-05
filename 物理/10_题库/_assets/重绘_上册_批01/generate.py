"""Reproducible black/white physics figures. Python 3 + numpy + matplotlib.
Run in this directory: python generate.py
All coordinates for schematic layouts are drawing coordinates, not measurements.
Scientific constraints and provenance are recorded in mapping.json.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Arc

OUT=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix',
    'font.size':19,'lines.linewidth':1.8,'svg.fonttype':'path',
    'savefig.facecolor':'white','axes.unicode_minus':False})

def canvas(xlim,ylim,size=(6.4,3.6)):
    fig,ax=plt.subplots(figsize=size)
    fig.subplots_adjust(left=.035,right=.965,bottom=.09,top=.95)
    ax.set(xlim=xlim,ylim=ylim);ax.axis('off')
    return fig,ax

def line(ax,x,y,**kw):
    ax.plot(x,y,color='black',**kw)

def arrow(ax,start,end,dashed=False):
    ax.annotate('',xy=end,xytext=start,arrowprops=dict(arrowstyle='-|>',color='black',
        lw=1.65,mutation_scale=16,linestyle=(0,(4,3)) if dashed else '-'),zorder=4)

def text(ax,x,y,s,**kw):
    ax.text(x,y,s,ha=kw.pop('ha','center'),va=kw.pop('va','center'),**kw)

def axes(ax,x0,x1,y0,y1,xlabel,ylabel,origin=True,xlabel_y=None):
    arrow(ax,(x0,0),(x1,0));arrow(ax,(0,y0),(0,y1))
    text(ax,x1,y0*.25 if xlabel_y is None else xlabel_y,xlabel,ha='right')
    text(ax,-.026*(x1-x0),y1,ylabel,ha='right',va='top')
    if origin:text(ax,-.018*(x1-x0),-.08*(y1-y0),'$O$',ha='right')

def save(fig,name):
    fig.savefig(OUT/(name+'.svg'))
    svg=OUT/(name+'.svg')
    svg.write_text('\n'.join(s.rstrip() for s in svg.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8',newline='\n')
    fig.savefig(OUT/(name+'.png'),dpi=220)
    plt.close(fig)

def cone(name,friction_up):
    # theta=60 degrees in the question: wall is 30 degrees from vertical.
    # Arrow lengths are qualitative; a_n is acceleration, distinguished by dashes.
    fig,ax=canvas((-1.35,1.45),(-1.55,1.5),(4.5,4.6));ax.set_aspect('equal')
    line(ax,[0,0],[0,1.4],ls=(0,(4,3)),lw=1.2)
    # Only the side opposite the friction arrow needs a wall reference line.
    sign=1 if friction_up else -1
    line(ax,[0,.70*sign],[0,-1.212*sign],ls=(0,(4,3)),lw=1.2)
    arrow(ax,(0,0),(1.05*np.cos(np.pi/6),1.05*np.sin(np.pi/6)))
    text(ax,1.03,.61,'$N$')
    f=np.array([-.5,np.sqrt(3)/2])*(1 if friction_up else -1)
    arrow(ax,(0,0),tuple(1.18*f));text(ax,1.30*f[0],1.30*f[1],'$f$')
    arrow(ax,(0,0),(0,-1.21));text(ax,0,-1.39,'$mg$')
    arrow(ax,(0,0),(1.13,0),dashed=True);text(ax,1.27,.03,'$a_n$')
    ax.plot(0,0,'ko',ms=5);text(ax,-.14,-.13,'$m$')
    if friction_up:
        ax.add_patch(Arc((0,0),1.10,1.10,theta1=90,theta2=120,color='black',lw=1.1))
        text(ax,-.21,.78,'$\\theta/2$')
    save(fig,name)

def pulley():
    fig,ax=canvas((-2.0,1.8),(-1.8,1.4),(5.2,4.4));ax.set_aspect('equal')
    ax.add_patch(Circle((0,0),.8,fill=False,lw=1.8,color='black'))
    # A tangent at the upper left of a circle. Its angle is schematic, not given.
    phi=np.deg2rad(125);p=.8*np.array([np.cos(phi),np.sin(phi)])
    tangent=np.array([-np.sin(phi),np.cos(phi)])
    arrow(ax,tuple(p),tuple(p+1.45*tangent))
    text(ax,-1.63,.04,"$T'_1$")
    arrow(ax,(.8,0),(.8,-1.45));text(ax,1.03,-1.47,'$T_2$')
    # Radius is symbolic R, with no numerical value or scale.
    q=.8*np.array([np.cos(np.pi/9),np.sin(np.pi/9)])
    line(ax,[0,q[0]],[0,q[1]],lw=1.5);ax.plot(0,0,'ko',ms=4)
    text(ax,.26,-.16,'$R$')
    save(fig,'03-pulley-4-7')

def vibration():
    # x/A=cos(pi*t/6+2*pi/3). x(0)/A=-1/2, initial velocity negative;
    # first upward equilibrium crossing is t=5 s. No numerical A is invented.
    fig,ax=canvas((-1.7,11.75),(-1.40,1.55))
    axes(ax,-1.45,11.45,-1.25,1.4,'$t/\\mathrm{s}$','$x$')
    t=np.linspace(0,11,700);line(ax,t,np.cos(np.pi*t/6+2*np.pi/3))
    line(ax,[0,8],[1,1],ls=(0,(4,3)),lw=1.1)
    text(ax,-.27,1,'$A$',ha='right');text(ax,-.30,-.5,'$-A/2$',ha='right')
    text(ax,5,-.23,'$5$');line(ax,[-.14,0],[-.5,-.5],lw=1.2)
    save(fig,'04-vibration-4-7')

def qualitative_wave(name,spatial):
    # Unit-free layout parameter s. These are qualitative, uncalibrated diagrams;
    # no physical amplitude, wavelength, period, or numeric phase is asserted.
    fig,ax=canvas((-.16,1.22),(-1.48,1.58))
    axes(ax,-.13,1.18,-1.31,1.4,'$x$' if spatial else '$t$','$y$',origin=not spatial)
    s=np.linspace(0,1,601);line(ax,s,-np.sin(2*np.pi*s))
    if spatial:
        for pos,label,dy in [(.25,'M',-.29),(.5,'N',-.28),(.75,'P',.29),(1,'Q',-.28)]:
            y=-np.sin(2*np.pi*pos);ax.plot(pos,y,'ko',ms=5.2);text(ax,pos,y+dy,'$'+label+'$')
        arrow(ax,(.19,1.13),(.40,1.13));text(ax,.29,1.39,'$v$')
    save(fig,name)

def wave_513():
    # t=3 s snapshot: y=-0.02*cos(pi*x/10), x in metres, y in metres.
    fig,ax=canvas((-5.2,31.8),(-.031,.036))
    axes(ax,-4.8,31,-.027,.033,'$x$','$y/\\mathrm{m}$',origin=False)
    x=np.linspace(-3.4,29.5,700);line(ax,x,-.02*np.cos(np.pi*x/10))
    for v in (5,10,15,20):
        dx=.45 if v==5 else (-.6 if v==15 else 0)
        text(ax,v+dx,-.0055,f'${v}$',fontsize=17)
    text(ax,-.5,-.023,'$-0.02$',ha='right')
    arrow(ax,(16,.023),(21,.023));text(ax,18.5,.029,'$u$')
    save(fig,'07-wave-5-13')

def wave_56():
    # Snapshot t=1/3 s, y in cm, x in cm. A=10 cm, y(0)=-5 cm,
    # positive spatial slope at x=0; distance between adjacent zeroes=20 cm.
    # Thus y=10*sin(pi*x/20-pi/6). Keep the point name A distinct from amplitude.
    fig,ax=canvas((-11.2,47.0),(-15.9,17.5))
    axes(ax,-10.6,45.5,-14,16,'$x/\\mathrm{cm}$','$y/\\mathrm{cm}$',xlabel_y=-12.5)
    x=np.linspace(0,43.33,800);line(ax,x,10*np.sin(np.pi*x/20-np.pi/6))
    line(ax,[0,40/3],[10,10],ls=(0,(4,3)),lw=1.1)
    text(ax,-1.0,10,'$10$',ha='right');text(ax,-1.0,-5,'$-5$',ha='right')
    left=10/3;right=70/3
    text(ax,right+.7,2.4,'$A$')
    for v in (left,right):line(ax,[v,v],[-.8,-4.8],lw=1.1)
    ax.annotate('',xy=(right,-3.4),xytext=(left,-3.4),arrowprops=dict(arrowstyle='<->',lw=1.3,color='black'))
    text(ax,(left+right)/2,-6.1,'$20$')
    save(fig,'08-wave-5-6')

def scientific_checks():
    assert np.isclose(np.cos(2*np.pi/3),-.5)
    assert -np.sin(2*np.pi/3)<0
    assert np.isclose(np.cos(np.pi*5/6+2*np.pi/3),0)
    assert -np.sin(np.pi*5/6+2*np.pi/3)>0
    assert np.allclose(-.02*np.cos(np.pi*np.array([0,5,10,15,20])/10),[-.02,0,.02,0,-.02])
    f=lambda x:10*np.sin(np.pi*x/20-np.pi/6)
    assert np.isclose(f(0),-5) and np.isclose(f(40/3),10)
    assert np.allclose([f(10/3),f(70/3)],[0,0]) and np.isclose(70/3-10/3,20)
    # Cone: N normal to wall; friction along wall, either up or down.
    assert np.isclose(np.dot([np.cos(np.pi/6),np.sin(np.pi/6)],[-.5,np.sqrt(3)/2]),0)

if __name__=='__main__':
    scientific_checks()
    cone('01-cone-2-3-b',True);cone('02-cone-2-3-c',False);pulley();vibration()
    qualitative_wave('05-wave-5-10-a',True);qualitative_wave('06-wave-5-10-b',False)
    wave_513();wave_56()
    print('8 SVG + 8 PNG rendered; scientific constraint checks passed')
