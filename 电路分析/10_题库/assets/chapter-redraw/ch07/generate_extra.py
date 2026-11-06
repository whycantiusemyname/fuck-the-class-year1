"""Main-agent source-bound multi-stage and teaching figures."""
from pathlib import Path
exec((Path(__file__).with_name('generate.py')).read_text(encoding='utf8').split('# E7-1:')[0])

def instrumentation(key,bridge=False):
 c=C(key,key,size=(22 if bridge else 17,13));dx=7 if bridge else 0
 n1,p1,o1=op(c,4+dx,11,'A_1',plus_top=True);n2,p2,o2=op(c,4+dx,4,'A_2');n3,p3,o3=op(c,18+dx,7,'A_3',plus_top=bridge)
 if bridge:
  c.supply((1,14),r'$E=+5\,\mathrm{V}$');c.wire((1,14),(-1,14));c.wire((1,14),(3,14))
  for x,k in [(-1,'R'),(3,'R_t')]:
   part(c,'R',(x,14),(x,9),'R');part(c,'R',(x,9),(x,3),k,offset=-.5 if x<0 else .5);c.wire((x,3),(1,3));c.dot((x,9))
  c.ground((1,3));c.d.add(E.Arrow().at((2.45,5.5)).to((3.55,6.5)))
  c.wire((-1,9),(0,9),(0,12.5),(7,12.5),(7,p1.y),p1);c.wire((3,9),(6,9),(6,p2.y),p2)
  c.d.add(E.Arrow().at((5,4.8)).to((5,11.3)));c.text(4.6,8,'$u_i$')
 else:
  c.port((0,p1.y),'$u_{I1}$');c.wire((0,p1.y),p1);c.port((0,p2.y),'$u_{I2}$');c.wire((0,p2.y),p2)
 rail=10+dx;c.wire(o1,(rail,11));c.wire(o2,(rail,4));part(c,'R',(rail,11),(rail,9),'R' if bridge else 'R_1');part(c,'R',(rail,9),(rail,6),'R_W' if bridge else 'R_2');part(c,'R',(rail,6),(rail,4),'R' if bridge else 'R_1')
 c.wire(n1,(3+dx,n1.y),(3+dx,9),(rail,9));c.wire(n2,(3+dx,n2.y),(3+dx,6),(rail,6))
 for y in [11,9,6,4]:c.dot((rail,y))
 c.text(rail+.35,11.5,'$u_{o1}$',ha='left');c.text(rail+.35,3.4,'$u_{o2}$',ha='left')
 top=p3 if bridge else n3;bot=n3 if bridge else p3
 c.wire((rail,11),(rail+1,11));part(c,'R',(rail+1,11),(16+dx,11),'R_1' if bridge else 'R');c.wire((16+dx,11),(16+dx,top.y),top)
 c.wire((16+dx,top.y),(17+dx,top.y),(17+dx,14));part(c,'R',(17+dx,14),(25+dx,14),'R_2' if bridge else 'R_f');c.wire((25+dx,14),(25+dx,7),o3);c.dot((16+dx,top.y));c.dot((25+dx,7))
 c.wire((rail,4),(rail+1,4));part(c,'R',(rail+1,4),(16+dx,4),'R_1' if bridge else 'R');c.wire((16+dx,4),(16+dx,bot.y),bot);part(c,'R',(16+dx,4),(16+dx,0),'R_2' if bridge else 'R_f');c.ground((16+dx,0));c.dot((16+dx,4));output(c,o3,x=27+dx)
 if not bridge:
  c.text(rail-.4,9,'$A$',ha='right');c.text(rail-.4,6,'$B$',ha='right')
 return c

c=instrumentation('F097',bridge=True);done(c,'电桥上两臂R、下左R/下右Rt，E=+5V；两取样端对应A1/A2正端；前级R/RW/R；末级上正下负及R1/R2分配照原题，不套常见极性。')
c=instrumentation('F191');done(c,'两同相输入uI1/uI2，前级R1/R2/R1取样A/B，末级上负下正、R输入/Rf反馈与接地，未复制电桥题相反末级极性。')

c=C('F101-a','F101(a)',size=(10,7));n,p,o=op(c,5,4);c.port((0,n.y),'$u_i$');part(c,'R',(0,n.y),(4,n.y),r'R=100\,\mathrm{k}\Omega');c.wire((4,n.y),n);feedback(c,n,o,r'C=10\,\mu\mathrm{F}',y=8,xleft=4,xright=10,kind='C');grounded(c,p);output(c,o);c.save()
c=C('F101-b','F101(b)',size=(11,9))
for y,name,vals in [(5,'u_i',[-1,1]),(0,'u_o',[-2,-1,1,2])]:
 c.d.add(E.Arrow().at((0,y-2.4)).to((0,y+2.5)));c.d.add(E.Arrow().at((-.4,y)).to((8.4,y)));c.text(.15,y+2.4,'$'+name+r'/\mathrm{V}$',ha='left');c.text(8.2,y-.35,r'$t/\mathrm{s}$');c.text(-.3,y-.3,'$0$')
 for v in vals:c.text(-.3,y+v,'$'+('+' if v>0 else '')+str(v)+'$',ha='right')
c.ax.plot([0,1,1,3,3,5,5,7,7,8],[6,6,4,4,6,6,4,4,6,6],color='black',lw=1.65)
for x in [1,3,5,7]:c.ax.plot([x,x],[-2.25,6.4],ls='--',lw=1,color='black');c.text(x,4.65,'$'+str(x)+'$')
c.save();panels('F101',['F101-a','F101-b'],['(a)','(b)']);QA['F101']='100kΩ输入/10μF反馈积分器，正端地；输入给定±1V，1/3/5/7s跳变；输出坐标保留±1/±2V而不添加答案曲线。'

c=C('F156','F156',size=(23,9));n1,p1,o1=op(c,4,5,'A_1',plus_top=True);n2,p2,o2=op(c,13,5,'A_2',plus_top=True);n3,p3,o3=op(c,22,5,'A_3',plus_top=True)
part(c,'V',(0,0),(0,p1.y),'v_i');c.ground((0,0));part(c,'R',(0,p1.y),p1,r'1\,\mathrm{k}\Omega');part(c,'R',(0,n1.y),(3,n1.y),r'1\,\mathrm{k}\Omega');c.ground((0,n1.y));c.wire((3,n1.y),n1,(3,n1.y),(3,1.7));part(c,'R',(3,1.7),(9,1.7),r'10\,\mathrm{k}\Omega');c.wire((9,1.7),(9,5),o1);c.dot((3,n1.y));c.dot((9,5));c.text(9.1,5.5,'$v_{o1}$')
part(c,'R',(9,5),(12,5),r'1\,\mathrm{k}\Omega');c.wire((12,5),(12,p2.y),p2);c.wire(n2,(12,n2.y),(12,1.7),(18,1.7),(18,5),o2);c.dot((18,5));c.text(18.1,5.5,'$v_{o2}$')
part(c,'R',(18,5),(21,5),r'1\,\mathrm{k}\Omega');c.wire((21,5),(21,p3.y),p3);grounded(c,n3);output(c,o3,x=27,label='v_{o3}')
for x in [5,14,23]:
 edge=1.25*(1-1/2.165);c.wire((x,5+edge),(x,7));c.wire((x,5-edge),(x,3));c.text(x+.2,7,r'$12\,\mathrm{V}$',ha='left');c.text(x+.2,3,r'$-12\,\mathrm{V}$',ha='left')
done(c,'三级分别同相1k/10k放大、跟随、负端接地比较器；三级均±12V供电，输入间1kΩ均保留，未添加第三反馈。')

c=C('F167','F167',size=(18,10));n1,p1,o1=op(c,6,6,'A_1');n2,p2,o2=op(c,16,6,'A_2',plus_top=True)
c.port((0,n1.y),'$u_i$');part(c,'R',(0,n1.y),(5,n1.y),'R_2');c.wire((5,n1.y),n1);feedback(c,n1,o1,'R_2',y=10,xleft=5,xright=11)
c.wire((0,n1.y),(0,p1.y));part(c,'C',(0,p1.y),(4,p1.y),'C_1');c.wire((4,p1.y),p1);part(c,'R',(4,p1.y),(4,0),'R_1');c.ground((4,0));c.dot((0,n1.y));c.dot((4,p1.y))
c.wire((11,6),(14,6),(14,p2.y),p2);c.text(11.5,6.5,'$u_{o1}$');c.wire(n2,(15,n2.y),(15,2));part(c,'R',(10,2),(15,2),'R_3');c.ground((10,2));part(c,'R',(15,2),(22,2),'R_4');c.wire((22,2),(22,6),o2);c.dot((15,2));c.dot((22,6));output(c,o2,x=24);done(c,'第一级输入分两路：R2到负端、C1到正端；R2负反馈、R1正端地；第二级上正下负，R3地/R4反馈。')

c=C('F175','F175',size=(19,11));n1,p1,o1=op(c,4,7,'A_1',plus_top=True);n2,p2,o2=op(c,14,7,'A_2');c.port((0,p1.y),'$u_i$');c.wire((0,p1.y),p1);c.wire(n1,(3,n1.y),(3,2));part(c,'R',(3,2),(3,0),r'1\,\mathrm{k}\Omega',offset=-.5);c.ground((3,0));c.dot((3,2))
part(c,'R',o1,(12,7),r'1\,\mathrm{k}\Omega');c.wire((12,7),(12,n2.y),n2);feedback(c,n2,o2,r'11\,\mathrm{k}\Omega',y=11,xleft=12,xright=20);grounded(c,p2)
part(c,'R',(20,7),(20,2),r'20\,\mathrm{k}\Omega');part(c,'R',(20,2),(20,-1),r'10\,\mathrm{k}\Omega');c.ground((20,-1));part(c,'R',(3,2),(20,2),r'9\,\mathrm{k}\Omega');c.dot((20,2));output(c,o2,x=23);done(c,'A1上正下负；输出经1kΩ到A2负端，A2正端直接地/11kΩ反馈；输出20k/10k中点经9k接A1负端，再1k地，五处不同数值不混用。')

# C1: insulated gate and left-pointing channel arrow follow the uncropped photo.
c=C('F015','C1',size=(12,9));n,p,o=op(c,4,6,plus_top=True);c.port((0,p.y),'$u_I$');c.wire((0,p.y),p)
c.wire(o,(10,6));c.wire((10,5.4),(10,6.6));c.wire((10.3,6.7),(11,6.7),(11,9));c.supply((11,9),'$V_{CC}$');c.wire((10.3,5.3),(11,5.3),(11,3));
for a,b in [(6.45,6.8),(5.8,6.15),(5.15,5.5)]:c.wire((10.3,a),(10.3,b))
c.d.add(E.Arrow().at((11,6)).to((10.35,6)));c.wire((11,6),(11,5.3));c.dot((11,5.3));c.wire(n,(3,n.y),(3,3));part(c,'R',(3,3),(3,0),'R_1',offset=-.5);c.ground((3,0));part(c,'R',(3,3),(11,3),'R_2');part(c,'R',(11,3),(11,0),'R_3');c.ground((11,0));c.wire((11,3),(14,3));c.port((14,3),'$u_o$','right');c.dot((3,3));c.dot((11,3));done(c,'未裁切照片确认是绝缘栅MOS器件：运放正端uI、负端R1地/R2回源极输出、R3负载；VCC接上端，沟道箭头朝左，未画成NPN三极管。')

c=C('F192','F192',size=(12,10));n,p,o=op(c,5,6);c.port((0,n.y),'$u_I$');c.wire((0,n.y),n);c.text(4.3,n.y+.4,'$N$',size=14);c.port((0,p.y),r'$U_{\mathrm{REF}}$');part(c,'R',(0,p.y),(4,p.y),'R_1');c.wire((4,p.y),p);c.dot((4,p.y));c.text(4.3,p.y+.4,'$P$',size=14)
part(c,'R',o,(12,6),'R');c.wire((4,p.y),(4,3));part(c,'R',(4,3),(12,3),'R_2');c.wire((12,3),(12,6));c.dot((12,3));limiter(c,12,top=3,bottom=-1,label=r'D_Z:\ \pm U_Z');c.wire((12,6),(14,6));c.port((14,6),'$u_o$','right');c.dot((12,6));done(c,'uI直入负端N；UREF经R1入正端P，R2从限幅后输出正反馈；R串于运放输出，双向DZ限幅到地，保留参考电压与节点标识。')

(HERE/'extra-geometry.json').write_text(json.dumps(M.records,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(HERE/'qa-extra.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
