"""Chapter 5 exact circuit redraws. Run: python generate.py. Dependencies: schemdraw, matplotlib, PyMuPDF, Pillow.
Coordinates express layout only. Source names and verified mappings are in ledger.json.
"""
from pathlib import Path
import sys,json,numpy as np
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent))
import common as M
from panels import combine
import matplotlib.pyplot as plt
import fitz
M.OUT=HERE;C=M.Circuit

def ports(c,top=4,bottom=0,width=7,ui='$u_i$',uo='$u_o$'):
 c.port((0,top),ui);c.port((0,bottom),'$-$');c.port((width,top),uo,'right');c.port((width,bottom),'$-$','right');c.wire((0,bottom),(width,bottom))
def meter(c,a,b,label):
 c.part('S',a,b);c.text((a[0]+b[0])/2,(a[1]+b[1])/2,label)
def saveplot(fig,key):
 for ext in ['svg','png']:fig.savefig(HERE/(key+'.'+ext),dpi=210,bbox_inches='tight',pad_inches=.18,facecolor='white')
 plt.close(fig)
 p=HERE/(key+'.svg');p.write_bytes(('\n'.join(x.rstrip() for x in p.read_text(encoding='utf-8').splitlines())+'\n').encode())
def wave(key,kind):
 fig,ax=plt.subplots(figsize=(6.4,3.5));ax.axis('off')
 if kind=='square':
  ax.plot([0,1.5,1.5,3,3,4.5],[12,12,-12,-12,12,12],color='black',lw=1.65)
  ax.annotate('',annotation_clip=False,xy=(4.8,0),xytext=(-.25,0),arrowprops={'arrowstyle':'->','color':'black'});ax.annotate('',annotation_clip=False,xy=(0,16),xytext=(0,-16),arrowprops={'arrowstyle':'->','color':'black'})
  for y in [12,0,-12]:ax.text(-.12,y,'$'+str(y)+'$',ha='right',va='center',fontsize=17)
  ax.text(-.18,16,r'$u_1/\mathrm{V}$',ha='right',fontsize=17);ax.text(4.8,-2,'$t$',fontsize=17)
 elif kind=='pulse':
  ax.plot([0,0,10,10,18],[0,3,3,0,0],color='black',lw=1.65)
  ax.annotate('',annotation_clip=False,xy=(20,0),xytext=(-1,0),arrowprops={'arrowstyle':'->','color':'black'});ax.annotate('',annotation_clip=False,xy=(0,4),xytext=(0,-.4),arrowprops={'arrowstyle':'->','color':'black'})
  ax.text(-.5,3,'$3$',ha='right',fontsize=17);ax.text(10,-.4,'$10$',ha='center',fontsize=17);ax.text(-.4,4,r'$u_i/\mathrm{V}$',ha='right',fontsize=17);ax.text(20,-.4,r'$t/\mathrm{ms}$',fontsize=17)
 elif kind=='triangle':
  ax.plot([0,1,2,3,4,5,6],[0,4,0,-4,0,4,0],color='black',lw=1.65)
  ax.annotate('',annotation_clip=False,xy=(6.5,0),xytext=(-.4,0),arrowprops={'arrowstyle':'->','color':'black'});ax.annotate('',annotation_clip=False,xy=(0,5),xytext=(0,-5),arrowprops={'arrowstyle':'->','color':'black'})
  ax.hlines([4,-4],0,3,linestyles='--',lw=1,color='black');ax.text(-.15,4,r'$4\,\mathrm{V}$',ha='right',fontsize=17);ax.text(-.15,-4,r'$-4\,\mathrm{V}$',ha='right',fontsize=17);ax.text(-.1,5,'$v_i$',ha='right',fontsize=17);ax.text(6.5,-.5,'$t$',fontsize=17)
 saveplot(fig,key)

# E5-1: two diode orientations and two source polarities, not an inferred operating model.
for reverse in [False,True]:
 suffix='b' if reverse else 'a';c=C('F024-'+suffix,'E5-1',size=(7,5))
 c.wire((0,0),(0,5));c.part('D',(0,5),(5,5),'$D_1$',reverse);c.part('V',(1.8,0),(1.8,3.6),r'$12\,\mathrm{V}$',reverse,offset=-.5);c.part('D',(1.8,3.6),(5,3.6),'$D_2$',reverse)
 c.wire((5,5),(5,3.6),(6.5,3.6));c.dot((5,3.6));c.part('R',(5,3.6),(5,1.8),'$R$');c.part('V',(5,0),(5,1.8),r'$6\,\mathrm{V}$',offset=-.5);c.wire((0,0),(6.5,0));c.dot((1.8,0));c.dot((5,0));c.port((6.5,3.6),'$+$','right');c.port((6.5,0),'$-$','right');c.text(7.0,1.8,'$U_o$',ha='left');c.save()
combine(HERE,'F024',['F024-a','F024-b'],['(a)','(b)'])
for suffix in ['a','b']:
 c=C('F025-'+suffix,'E5-2',size=(7,5));ports(c)
 if suffix=='a':
  c.part('R',(0,4),(4.5,4),'$R$');c.wire((4.5,4),(7,4));c.part('D',(4.5,4),(4.5,2),'$D$');c.part('V',(4.5,0),(4.5,2),'$U$',offset=-.5)
 else:
  c.part('D',(0,4),(4.5,4),'$D$');c.wire((4.5,4),(7,4));c.part('R',(4.5,4),(4.5,2),'$R$');c.part('V',(4.5,0),(4.5,2),'$U$',offset=-.5)
 c.dot((4.5,4));c.dot((4.5,0));c.save()
combine(HERE,'F025',['F025-a','F025-b'],['(a)','(b)'])
c=C('F026-a','E5-3',size=(7,5));c.port((0,5),'$u_1$');c.port((0,0),'$-$');c.port((8,0),'$-$','right');c.wire((0,0),(8,0));c.text(8.4,1.5,'$u_o$',ha='left');c.part('R',(0,5),(3,5),'$R$');c.part('D',(6,5),(3,5),'$D$');c.wire((6,5),(6,3),(8,3));c.port((8,3),'$+$','right');c.wire((3,5),(3,3));c.part('R',(3,3),(6,3),'$R$',offset=-.4);c.part('R',(6,3),(6,0),'$R$');c.dot((3,5));c.dot((6,3));c.dot((6,0));c.save()
wave('F026-b','square');combine(HERE,'F026',['F026-a','F026-b'],['(a)','(b)'])
c=C('F027','E5-4',size=(6,5));c.supply((5,6),r'$+12\,\mathrm{V}$');c.part('R',(5,6),(5,3.5),r'$R=3.9\,\mathrm{k}\Omega$');c.part('D',(5,3.5),(0,3.5),'$D_A$');c.wire((5,3.5),(5,1.3));c.part('D',(5,1.3),(0,1.3),'$D_B$');c.wire((5,3.5),(7,3.5));c.dot((5,3.5));c.port((0,3.5),'$A$');c.port((0,1.3),'$B$');c.port((7,3.5),'$F$','right');c.save()
c=C('F028','E5-5',size=(7,5))
for y,label in [(5,'A'),(3,'B')]:
 c.port((0,y),'$'+label+'$');c.part('R',(0,y),(3,y),r'$1\,\mathrm{k}\Omega$');c.part('D',(3,y),(6,y),'$D_'+label+'$')
c.wire((6,5),(6,3),(8,3));c.dot((6,3));c.part('R',(6,3),(6,0),r'$R=9\,\mathrm{k}\Omega$');c.ground((6,0));c.port((8,3),'$F$','right');c.save()

# Transformer windings: connection positions matter; winding shapes are qualitative.
def transformer(c,x=0,top=6,bottom=0,taps=None):
 c.part('L',(x,top),(x,bottom))
 ys=[top]+(taps or [])+[bottom]
 for a,b in zip(ys,ys[1:]):c.part('L',(x+1,a),(x+1,b))
 c.port((x-1,top));c.port((x-1,bottom));c.wire((x-1,top),(x,top));c.wire((x-1,bottom),(x,bottom));c.text(x-1,(top+bottom)/2,r'$\sim$')
 return x+1
c=C('F030','E5-8',size=(9,5));x=transformer(c);c.wire((x,6),(3,6));c.part('D',(3,6),(5.5,6),'$D$');meter(c,(5.5,6),(7,6),'$A$');c.wire((7,6),(10,6));c.wire((x,0),(10,0));c.wire((3,6),(3,4.5));meter(c,(3,4.5),(3,1.5),'$V_1$');c.wire((3,1.5),(3,0));c.part('R',(8,6),(8,0),'$R_L$');meter(c,(10,6),(10,0),'$V$')
for p in [(3,6),(3,0),(8,6),(8,0)]:c.dot(p)
c.save()
c=C('F031','E5-9',size=(9,6));transformer(c,taps=[3]);c.wire((1,6),(3,6));c.part('D',(3,6),(7,6),'$D_1$');c.wire((1,0),(3,0));c.part('D',(3,0),(7,0),'$D_2$');c.wire((7,0),(7,2.7));c.wire((7,3.3),(7,6),(9,6));c.ax.add_patch(M.plt.matplotlib.patches.Arc((7,3),.6,.6,theta1=-90,theta2=90,color='black',lw=1.65));c.part('R',(9,6),(9,3),'$R_L$');c.wire((1,3),(9,3));c.dot((1,3));c.dot((7,6));c.text(1.8,5.7,'$+$');c.text(1.8,4.5,'$u_2$');c.text(1.8,3.3,'$-$');c.text(1.8,2.7,'$+$');c.text(1.8,1.5,'$u_2$');c.text(1.8,.3,'$-$');c.text(11,5.5,'$+$');c.text(11,4.5,'$u_o$');c.text(11,3.3,'$-$');c.d.add(M.E.Arrow().at((9.5,6.7)).to((9.5,5.5)));c.text(10,6.5,'$i_o$',ha='left');c.save()
c=C('F032','E5-10',size=(10,8));transformer(c,top=9,bottom=0,taps=[5.5,2.7]);c.text(-1.1,4.5,r'$220\,\mathrm{V}$',ha='right');c.wire((1,9),(3,9));c.part('D',(6,9),(3,9),'$D_1$');c.wire((6,9),(10,9));c.wire((1,5.5),(3,5.5));c.part('D',(3,5.5),(6,5.5),'$D_2$');c.wire((6,5.5),(10,5.5));c.wire((1,0),(3,0));c.part('D',(3,0),(6,0),'$D_3$');c.wire((6,0),(6,5.5));c.dot((6,5.5));c.part('R',(9,9),(9,6.5),'$R_{L1}$');c.ground((9,6.5));c.part('R',(9,5.5),(9,2.7),'$R_{L2}$');c.ground((9,2.7));c.wire((1,2.7),(3,2.7));c.ground((3,2.7));c.dot((1,2.7))
for p in [(1.2,8.4),(1.2,4.9),(1.2,2.1),(-.2,6.7)]:c.dot(p)
for y,label in [(7.2,r'$90\,\mathrm{V}$'),(4.1,r'$10\,\mathrm{V}$'),(1.4,r'$10\,\mathrm{V}$')]:c.text(1.7,y,label,ha='left')
for y0,y1,label in [(9,6.5,'u_{o1}'),(5.5,2.7,'u_{o2}')]:c.port((10,y0),'$+$','right');c.port((10,y1),'$-$','right');c.ground((10,y1));c.text(10.5,(y0+y1)/2,'$'+label+'$',ha='left')
c.text(8.5,7.1,r'$10\,\mathrm{k}\Omega$',ha='right');c.text(8.5,3.9,r'$10\,\Omega$',ha='right');c.dot((9,9));c.dot((9,5.5));c.save()

# Bridge rectifier: transformer connects AC top/bottom; load joins right/left DC nodes.
c=C('F029','E5-6 / E5-7',size=(11,7));transformer(c,top=6,bottom=0);top=(5,6);right=(7,3);bottom=(5,0);left=(3,3)
c.wire((1,6),top);c.wire((1,0),bottom)
for a,b,label in [(top,right,'D_1'),(bottom,right,'D_2'),(left,bottom,'D_3'),(left,top,'D_4')]:c.part('D',a,b,'$'+label+'$',offset=.6)
c.wire(right,(9.5,3),(9.5,6.5),(11,6.5));c.part('R',(11,6.5),(11,-1),'$R_L$');c.wire(left,(2,3),(2,.3));c.wire((2,-.3),(2,-1),(11,-1));c.ax.add_patch(M.plt.matplotlib.patches.Arc((2,0),.6,.6,theta1=-90,theta2=90,color='black',lw=1.65))
for p in [top,right,bottom,left]:c.dot(p)
c.text(1.5,3,'$u_2$',ha='left');c.text(.5,5.4,'$Tr$');c.text(4.7,6.4,'$a$');c.text(4.7,-.4,'$b$');c.text(13,6,'$+$');c.text(13,3,'$u_o$');c.text(13,-.5,'$-$');c.d.add(M.E.Arrow().at((10,6.5)).to((11,6.5)));c.text(10.3,7,'$i_o$');c.text(-3,4.1,'$u_1$',ha='right');c.ax.plot([-3,-2.8,-2.6,-2.4,-2.2,-2,-1.8,-1.6,-1.4],[3,3.35,3.5,3.35,3,2.65,2.5,2.65,3],color='black',lw=1.3);c.ax.annotate('',annotation_clip=False,xy=(-1.2,3),xytext=(-3.2,3),arrowprops={'arrowstyle':'->','color':'black','lw':1});c.save()

# Simulation bridge gate: diodes point away from +VL and towards -VL.
c=C('F002','仿真作业2',size=(8,8));t=(4,5);l=(2,3);r=(6,3);b=(4,1)
for a,z,label in [(t,l,'D_1'),(t,r,'D_2'),(l,b,'D_3'),(r,b,'D_4')]:c.part('D',a,z,'$'+label+'$',offset=.5)
c.part('R',(4,8),t,r'$R_1=2.2\,\mathrm{k}\Omega$');c.supply((4,8),r'$+V_L\ (+5\,\mathrm{V})$');c.part('R',b,(4,-2),r'$R_2=2.2\,\mathrm{k}\Omega$');c.port((4,-2));c.text(4,-2.5,r'$-V_L\ (-5\,\mathrm{V})$')
c.part('AC',(0,0),(0,3),'$u_i$',offset=-.7);c.wire((0,3),l);c.ground((0,0));c.wire(r,(8,3));c.port((8,3),'$u_o$','right');c.part('R',(7,3),(7,0),r'$R_3=1\,\mathrm{M}\Omega$');c.ground((7,0))
for p in [t,l,r,b,(7,3)]:c.dot(p)
c.save()

def diode_bias(key,leftpol=True,volt=5,rightvolt=10,reverse=False,diode='D',res='R'):
 c=C(key,'diode bias',size=(7,5));c.part('V',(1,0),(1,4),'$'+str(volt)+r'\,\mathrm{V}$',not leftpol,offset=-.7);c.part('D',(1,4),(5,4),'$'+diode+'$',reverse);c.part('R',(5,4),(5,2),'$'+res+'$');c.part('V',(5,0),(5,2),'$'+str(rightvolt)+r'\,\mathrm{V}$',True,offset=-.6);c.wire((1,0),(7,0));c.wire((5,4),(7,4));c.port((7,4),'$+$','right');c.port((7,0),'$-$','right');c.text(7.5,2,'$u_o$',ha='left');c.text(1,4.5,'$c$');c.text(5,4.5,'$b$');c.text(5,-.4,'$a$');c.dot((5,4));c.dot((5,0));c.save()
diode_bias('F133',False,diode='VD');diode_bias('F134',True,diode='VD')
c=C('F131','diode bias',size=(5,5));c.part('D',(1,4),(1,2),'$D$');c.part('B',(1,0),(1,2),r'$2\,\mathrm{V}$',True,offset=-.4);c.part('R',(4,4),(4,2),'$R$');c.part('B',(4,0),(4,2),r'$2\,\mathrm{V}$',False,offset=.4);c.wire((1,4),(6,4));c.wire((1,0),(6,0));c.port((6,4),'$+$','right');c.port((6,0),'$-$','right');c.text(6.4,2,'$u_o$',ha='left');c.dot((4,4));c.dot((4,0));c.save()
c=C('F140','charging',size=(7,4));c.part('V',(0,0),(0,3),'$u_i$',offset=-.8);c.part('R',(0,3),(3,3),'$R$');c.part('D',(3,3),(6,3),'$D$');c.part('C',(6,3),(6,0),r'$0.1\,\mu\mathrm{F}$');c.wire((6,0),(0,0));c.save();wave('F141','pulse')
c=C('F144','box load',size=(6,4));c.part('V',(0,0),(0,3),'$u_s$',offset=-.8);c.part('R',(0,3),(5,3),r'$1\,\mathrm{k}\Omega$');c.part('R',(5,3),(5,0),None);c.text(6,2.7,'$+$');c.text(6,1.5,'$u$');c.text(6,.3,'$-$');c.text(5,1.5,'$A$');c.wire((5,0),(0,0));c.d.add(M.E.Arrow().at((5.5,3.3)).to((5.5,2.4)));c.text(6,3,'$i$');c.save()
c=C('F155-a','limiter',size=(6,4));ports(c,3,0,6,ui='$v_i$',uo='$v_o$');c.part('R',(0,3),(2.5,3),'$R_1$');c.wire((2.5,3),(6,3));c.part('R',(3,3),(3,0),'$R_2$');c.part('Z',(5,0),(5,3),None);c.dot((3,3));c.dot((5,3));c.dot((3,0));c.dot((5,0));c.save();wave('F155-b','triangle');combine(HERE,'F155',['F155-a','F155-b'],['(a)','(b)'])
for key,res,voltage in [('F158',r'$1\,\mathrm{k}\Omega$',r'$2.6\,\mathrm{V}$'),('F176',r'$R_2=960\,\Omega$',r'$3\,\mathrm{V}$')]:
 c=C(key,'diode small signal',size=(8,5));c.port((0,4),'$+$');c.port((0,0),'$-$');c.text(-.5,2,'$v_i$' if key=='F158' else '$u_i$',ha='right');c.part('C',(0,4),(3,4),'$C$')
 if key=='F176':c.part('R',(3,4),(6,4),r'$R_1=10\,\Omega$');x=6
 else:x=3
 c.wire((x,4),(9,4));c.part('R',(x,4),(x,2),res);c.part('V',(x,0),(x,2),voltage,offset=-.65);c.part('D',(9,4),(9,0),'$D$');c.wire((0,0),(9,0));c.dot((x,4));c.dot((x,0))
 if key=='F176':c.d.add(M.E.Arrow().at((9.5,4)).to((9.5,3)));c.text(10,3.6,'$i_D$',ha='left')
 c.save()
c=C('F164','diode bridge divider',size=(6,6))
for x,v in [(1,'6'),(6,'5')]:
 c.supply((x,6),'$+'+v+r'\,\mathrm{V}$');c.part('R',(x,6),(x,3),r'$10\,\mathrm{k}\Omega$',offset=-.4 if x==1 else .4);c.part('R',(x,3),(x,0),r'$10\,\mathrm{k}\Omega$',offset=-.4 if x==1 else .4);c.ground((x,0));c.dot((x,3))
c.part('D',(6,3),(1,3),None);c.text(3.5,2.2,'$-\quad v\quad+$');c.d.add(M.E.Arrow().at((4.7,4)).to((2.5,4)));c.text(3.5,4.4,'$I$');c.save()
c=C('F170','diode small signal network',size=(9,5));c.part('V',(0,0),(0,4),'$u_s$',offset=-.7);c.part('R',(0,4),(3,4),'$R_1$');c.part('R',(3,4),(6,4),'$R_3$');c.part('R',(3,4),(3,0),'$R_2$');c.part('D',(6,4),(6,0),'$D$');c.wire((6,4),(9,4));c.part('R',(9,4),(9,0),'$R_4$');c.wire((0,0),(9,0));c.text(7.6,3.4,'$+$');c.text(7.6,2,'$u_D$');c.text(7.6,.5,'$-$');c.d.add(M.E.Arrow().at((5.5,3.6)).to((5.5,2.7)));c.text(5.2,3.4,'$i_D$',ha='right')
for p in [(3,4),(6,4),(3,0),(6,0)]:c.dot(p)
c.save()
c=C('F173','switched diode RC',size=(10,5));c.part('V',(1,0),(1,3),r'$6\,\mathrm{V}$',offset=-.6);c.part('V',(3,0),(3,3),r'$8\,\mathrm{V}$');c.port((1,3));c.port((3,3));c.text(.6,3.3,'$1$');c.text(3.3,3.3,'$2$');c.port((2,4.6));c.wire((1,3),(2,4.6));c.text(1.6,5.2,r'$S\quad t=0\,\mathrm{s}$');c.part('D',(2,4.6),(5,4.6),None);c.part('R',(5,4.6),(8,4.6),r'$2\,\Omega$');c.wire((8,4.6),(11,4.6));c.part('R',(8,4.6),(8,0),r'$2\,\Omega$');c.part('C',(10,4.6),(10,0),r'$0.1\,\mathrm{F}$');c.wire((1,0),(11,0));c.port((11,4.6),'$+$','right');c.port((11,0),'$-$','right');c.text(11.5,2.3,'$u_o(t)$',ha='left')
for p in [(3,0),(8,0),(10,0),(8,4.6),(10,4.6)]:c.dot(p)
c.save()
# Correct the prior A9 drawing against the source; model voltage remains in the question.
c=C('F010','A9 circuit',size=(8,4));ports(c,3,0,8);c.part('R',(0,3),(3,3),'$R$');c.part('D',(3,3),(6,3),None);c.wire((6,3),(8,3));c.part('R',(6,3),(6,0),'$R_0$');c.dot((6,3));c.dot((6,0));c.save()
fig,axs=plt.subplots(2,1,figsize=(7,5.5),sharex=True)
for ax in axs:
 ax.set_xlim(0,6.7);ax.set_ylim(-4.5,4.5);ax.spines[['top','right']].set_visible(False);ax.spines['left'].set_position('zero');ax.spines['bottom'].set_position('zero');ax.set_xticks(range(7));ax.set_yticks([-3,-2,-1,0,1,2,3]);ax.set_xlabel(r'$t/\mathrm{s}$',loc='right',fontsize=17);ax.tick_params(labelbottom=True,labelsize=14)
axs[0].plot([0,1,2,3,4,5,6,6.5],[0,3,0,-3,0,3,0,-1.5],color='black',lw=1.65);axs[0].set_ylabel(r'$u_i/\mathrm{V}$',fontsize=17);axs[1].set_yticks(range(-4,5));axs[1].set_ylabel(r'$u_o/\mathrm{V}$',fontsize=17)
for ax in axs:
 ax.set_xlabel('');ax.text(1.02,.52,r'$t/\mathrm{s}$',transform=ax.transAxes,ha='left',va='bottom',fontsize=17)
saveplot(fig,'F011')
# Actual SVG rendering also serves PNG export for assembled figures.
for key in ['F002','F010','F011','F024','F025','F026','F027','F028','F029','F030','F031','F032','F131','F133','F134','F140','F141','F144','F155','F158','F164','F170','F173','F176']:
 d=fitz.open(HERE/(key+'.svg'));pdf=fitz.open('pdf',d.convert_to_pdf());pdf[0].get_pixmap(matrix=fitz.Matrix(2,2)).save(HERE/(key+'.png'))
(HERE/'geometry.json').write_bytes((json.dumps(M.records,ensure_ascii=False,indent=2)+'\n').encode())
# Compose the two native renders: MuPDF's SVG conversion loses dash patterns.
from PIL import Image,ImageDraw,ImageFont
imgs=[Image.open(HERE/(k+'.png')).convert('RGB') for k in ['F155-a','F155-b']]
w=max(im.width for im in imgs);out=Image.new('RGB',(w,sum(im.height+70 for im in imgs)),'white');draw=ImageDraw.Draw(out);y=0
for im,label in zip(imgs,['(a)','(b)']):
 out.paste(im,((w-im.width)//2,y));draw.text((w/2,y+im.height+5),label,anchor='mt',font=ImageFont.truetype('C:/Windows/Fonts/times.ttf',40),fill='black');y+=im.height+70
out.save(HERE/'F155.png')
print('24 exact vector figures rendered; F008 source uncertainty intentionally retained')
