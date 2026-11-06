"""Remaining source figures drawn by the main agent, including open problem terminals."""
from pathlib import Path
exec(Path(__file__).with_name('generate.py').read_text(encoding='utf8').split('# Explicit bridge')[0])

c=C('F081','E9-1',size=(19,18))
part(c,'L',(0,11),(0,5),'N_1',offset=-.8);c.wire((0,11),(-2,11),(-2,0));c.d.add(E.Fuse().at((-2,0)).to((-2,-2)));c.text(-3,-1,r'$\mathrm{FU}_1:\ 1\,\mathrm{A}$',ha='right');c.wire((-2,-2),(-2,-5));c.port((-2,-5));c.port((1,-5));c.text(-.5,-5.7,r'$\sim220\,\mathrm{V}$');c.wire((1,-5),(1,-1),(5,-1));c.wire((0,5),(0,-3),(8,-3),(8,-1))
part(c,'L',(4,17),(4,14),'N_2');part(c,'S',(8,17),(8,14));c.ax.plot([7.65,8.35],[15.15,15.85],color='black',lw=1.65);c.ax.plot([7.65,8.35],[15.85,15.15],color='black',lw=1.65);c.wire((4,17),(8,17));c.wire((4,14),(8,14))
part(c,'L',(4,11),(4,5),'N_3');part(c,'C',(6,11),(6,5));c.text(5.5,10,'$C_2$',ha='right');c.text(3,12.2,r'$C_2=0.047\,\mu\mathrm{F}$');c.wire((4,11),(10,11));c.wire((4,5),(6,5),(6,2),(5,2));
top=(10,11);bot=(10,5);left=(7,8);right=(13,8)
part(c,'D',right,top);part(c,'D',right,bot);part(c,'D',top,left);part(c,'D',bot,left);c.text(10,12,r'$2\mathrm{CZ}12\times4$');c.wire(left,(6.8,8),(6.8,6.8));c.ground((6.8,6.8));c.wire(right,(15,8));c.d.add(E.Fuse().at((15,8)).to((18,8)));c.text(16.5,9,r'$\mathrm{FU}_2:\ 3\,\mathrm{A}$');c.wire((18,8),(22,8));c.port((22,8),r'$-24\,\mathrm{V}$','right');part(c,'C',(20,8),(20,4),r'C_1=2000\,\mu\mathrm{F}');c.text(19.5,5.2,'$+$');c.ground((20,4));c.dot((20,8));c.wire(bot,(10,4),(8,4),(8,2));c.wire((10,11),(14,11),(14,-5));c.port((14,-5));c.wire((11,2),(12,2),(12,-5));c.port((12,-5));c.text(13,-5.7,r'$24\,\mathrm{V}$')
for y in [2,-1]:
 for x in [5,8,11]:c.port((x,y))
 c.wire((8,y),(10.4,y+.7))
c.ax.plot([9.1,9.1],[-.6,2.4],color='black',ls='--',lw=1);c.text(5,-2,'交流');c.text(10.8,-2,'直流');save(c,'完整E9-1：N2独立照明、N3/C2、四管桥输出右端−24V/C1正极地；双刀转换开关下方直流触点本来开口，保持开口；FU1=1A/FU2=3A及24V外接端/220V输入照录，不将交流输入误作输出档。')

c=C('F087','E9-9',size=(25,14));front(c);t1=passnpn(c,18,9,'T_1');t2=passnpn(c,17,6.7,'T_2');c.wire((11,10),(t1.collector.x,10),t1.collector);c.wire(t1.emitter,(t1.emitter.x,10),(30,10));c.wire(t2.collector,(14,t2.collector.y),(14,10));c.wire(t2.emitter,(18,t2.emitter.y),t1.base);dot(c,(14,10));n,p,o=leftop(c,17,4,unsigned=True);c.wire(o,(15,4),(15,6.7),t2.base)
part(c,'R',(13,10),(13,5),"R'");part(c,'Z',(13,0),(13,5),"D_Z'");part(c,'R',(12,1.5),(22,1.5),'R');c.wire((13,5),(12,5),(12,1.5));part(c,'Z',(22,0),(22,1.5),'D_Z');c.wire(p,(21,p.y),(21,1.5),(22,1.5));c.wire((13,5),(16,5),(16,6),(18.4,6),(18.4,4.8));c.wire((18.4,3.2),(18.4,0));c.ground((18.4,0))
part(c,'R',(26,10),(26,7),'R_1');part(c,'R',(26,7),(26,3),'R_2');part(c,'R',(26,3),(26,0),'R_3');arrow(c,(24.5,5),(25.8,5));c.wire(n,(23,n.y),(23,5),(24.5,5));cap(c,28,10,0,'C_2');part(c,'R',(30,10),(30,0),'R_L');c.wire((11,0),(30,0));c.text(31.2,5,'$U_O$');c.text(31,10,'$+$');c.text(31,0,'$-$');dot(c,(13,5),(22,1.5),(26,10),(26,0),(28,10),(28,0));c.text(-5,6,r'$\sim220\,\mathrm{V}$');c.text(-4,3,r'$50\,\mathrm{Hz}$');save(c,'E9-9原题要求标运放同/反相，故两输入端不预填±；复合NPN T1/T2、R′/DZ′电源、R/DZ参考、R1/R2/R3滑动采样和C1/C2均照题，供电脚与信号脚独立，未用参考解替题图。')

c=C('F004','仿真作业5',size=(23,15));n,p,o=c.op(11,7,label='U_1',plus_top=True);t=c.bjt((17,7),'Q_3');c.text(18.2,6,r'$2\mathrm{N}2712$',ha='left');c.text(12,9,r'$\mathrm{OPAMP\_5T\_VIRTUAL}$');c.wire(o,t.base);c.wire((0,11),(t.collector.x,11),t.collector);c.wire(t.emitter,(t.emitter.x,4),(23,4));c.dot((t.emitter.x,4));part(c,'R',(t.emitter.x,4),(t.emitter.x,0),r'R_5=200\,\Omega',offset=-.5);cap(c,21,4,0,r'C_1=47\,\mu\mathrm{F}');c.wire((0,0),(24,0));c.ground((0,0));c.ground((t.emitter.x,0));part(c,'S',(0,0),(0,11));c.ax.plot([-.3,-.3,-.1,-.1,.1,.1,.3],[5.3,5.7,5.7,5.3,5.3,5.7,5.7],color='black',lw=1.1);c.text(-1,4,r'$V_1$',ha='right');c.text(-1,3,r'$\mathrm{BIPOLAR\_VOLTAGE}$',ha='right')
c.wire((3,11),(3,p.y));part(c,'R',(3,p.y),(8,p.y),r'R_6=1\,\mathrm{k}\Omega');c.wire((8,p.y),p);part(c,'Z',(8,0),(8,p.y),r'D_1:\ 02\mathrm{BZ}2.2',offset=-.6);dot(c,(3,11),(8,p.y),(8,0));c.wire(n,(10,n.y),(10,3));part(c,'R',(10,3),(t.emitter.x,3),r'R_1=500\,\Omega');c.wire((t.emitter.x,3),(t.emitter.x,4));part(c,'R',(10,3),(10,0),r'R_2=1\,\mathrm{k}\Omega',offset=-.5);c.ground((10,0));c.dot((10,3))
edge=1.25*(1-1/2.165);c.wire((12,7+edge),(12,11));c.wire((12,7-edge),(12,1));c.ground((12,1));c.dot((12,11))
# Voltage meter across the reference and scope channels across input/output.
c.ax.add_patch(Rectangle((5,13),4,1.5,fill=False,lw=1.65));c.text(7,13.75,r'$\mathrm{XMM1}$');c.text(6,12.6,'$+$');c.text(8,12.6,'$-$');c.wire((6,13),(6,10),(8,10),(8,p.y));c.wire((8,13),(9.5,13),(9.5,1),(8,1),(8,0))
c.ax.add_patch(Rectangle((18,13),7,1.5,fill=False,lw=1.65));c.text(21.5,13.75,r'$\mathrm{XSC1}$');c.text(19.5,12.6,'$A$');c.text(23,12.6,'$B$');c.wire((19.5,13),(19.5,11),(t.collector.x,11));c.dot((19.5,11));c.wire((23,13),(24,13),(24,4),(23,4));c.wire((20,13),(20,0));c.wire((25,13),(26,13),(26,0),(24,0));c.dot((20,0));save(c,'仿真原图按节点核对：V1供Q3集电极和U1正电源，U1负电源地；R6=1k/D1=02BZ2.2参考，U1正端参考/负端500Ω+1k分压，Q3=2N2712、R5=200Ω、C1=47μF；XMM1跨参考、XSC1 A测输入/B测输出且回路地，保留原型名称与探测连接，不生成答案波形。')

(HERE/'remaining-geometry.json').write_bytes((json.dumps(M.records,ensure_ascii=False,indent=2)+'\n').encode())
(HERE/'qa-remaining.json').write_bytes((json.dumps(QA,ensure_ascii=False,indent=2)+'\n').encode())
