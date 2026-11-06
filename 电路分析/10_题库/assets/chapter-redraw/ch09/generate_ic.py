"""Main-agent IC regulator transcriptions. No guessed pin numbers."""
from pathlib import Path
exec(Path(__file__).with_name('generate.py').read_text(encoding='utf8').split('# Explicit bridge')[0])

def regbase(key,name,pins=False,size=(15,11)):
 c=C(key,key,size=size);a,b,g=regulator(c,3,10,name,pins);c.wire((0,10),a);c.wire(b,(17,10));c.wire((0,0),(17,0));ports(c,0,17,10);return c,g

# E9-13 and E9-14: reverse-facing followers, upper plus/lower minus.
for suffix in ['a','b']:
 c,g=regbase('F089-'+suffix,'W7805' if suffix=='a' else 'W7812',pins=True)
 n,p,o=c.op(8,5,label='A',reverse=True,plus_top=True);c.wire(g,(g[0],5),o);c.wire(n,(11,n.y),(11,2),(g[0],2),(g[0],5));part(c,'R',(g[0],2),(g[0],0),'R_2',offset=-.5);c.dot((g[0],5));part(c,'R',(15,10),(15,p.y),'R_1');c.wire((15,p.y),p);c.dot((15,p.y));part(c,'R',(15,p.y),(15,0),'R_3' if suffix=='a' else 'R_L',offset=.6);c.ground((15,0))
 if suffix=='a':
  arrow(c,(16.5,2.8),(15.2,2.8));c.wire((16.5,2.8),(17.3,2.8),(17.3,1),(15,1));c.dot((15,1))
 else:arrow(c,(14.4,1),(15.5,3));arrow(c,(16.5,4),(16.5,2),'I_O',(17,3))
 c.save()
panels('F089',['F089-a','F089-b']);QA['F089']='E9-13(a)W7805、R3滑端短下端；(b)W7812、RL可调并标IO向下；两运放上正下负、输出接稳压器公共脚并回负端，R2从公共脚到地。1/2/3引脚照图。'

c,g=regbase('F090','W7815');n,p,o=c.op(8,5,label='A',reverse=True,plus_top=True);c.wire(g,(g[0],5),o);part(c,'R',(g[0],5),(g[0],0),r'R_3=1\,\mathrm{k}\Omega',offset=-.5);c.wire(n,(11,n.y),(11,7),(g[0],7));part(c,'R',(15,10),(15,p.y),r'R_1=2\,\mathrm{k}\Omega');c.wire((15,p.y),p);part(c,'R',(15,p.y),(15,0),r'R_2=1\,\mathrm{k}\Omega');arrow(c,(13.5,2.8),(14.8,2.8));c.wire((13.5,2.8),(13,2.8),(13,p.y),(15,p.y));dot(c,(13,p.y),(g[0],7),(15,p.y));save(c,'E9-14完整页恢复W7815；R1=2k、R2=1k、R3=1k，R2滑端回上端；运放上正下负跟随、输出接公共端，R3泄放地，未漏短接线。')

c,g=regbase('F091','W7808');n,p,o=leftop(c,8,5);c.wire(g,(g[0],5),o);c.wire(n,(12,n.y),(12,8),(g[0],8));c.dot((g[0],8));part(c,'R',(15,10),(15,7),'R_1');part(c,'R',(15,7),(15,3),'R_P');part(c,'R',(15,3),(15,0),'R_2');arrow(c,(13.5,5),(14.8,5));c.wire(p,(13.5,p.y),(13.5,5));save(c,'E9-15 W7808、R1/RP/R2串采样，RP滑端入正端，负端回公共脚/运放输出；无额外R3泄放，不套上一题结构。')

def offset_reg(key,name,numbered=False):
 c,g=regbase(key,name,pins=numbered,size=(16,12));n,p,o=leftop(c,8,5);c.wire(g,(g[0],5),o);part(c,'R',(13,10),(13,8),r'R_1=2.5\,\mathrm{k}\Omega' if key=='F088' else 'R_2');part(c,'R',(13,8),(13,6.8),r'R_2=2.5\,\mathrm{k}\Omega' if key=='F088' else 'R_1');c.wire((13,6.8),(g[0],6.8));c.wire(n,(12,n.y),(12,8),(13,8));c.dot((13,8))
 # The first resistor is output→sample; the second is sample→common.
 # The original short horizontal above is removed by using only the resistor nodes.
 part(c,'R',(17,10),(17,7),r'500\,\Omega' if key=='F088' else 'R_3');part(c,'R',(17,7),(17,3),r'1.5\,\mathrm{k}\Omega' if key=='F088' else 'R_4');part(c,'R',(17,3),(17,0),r'2.5\,\mathrm{k}\Omega' if key=='F088' else 'R_5');arrow(c,(15.5,5),(16.8,5));c.wire(p,(15.5,p.y),(15.5,5));
 # Physical supply leads are separate from signal inputs and the common pin.
 c.wire((1,10),(1,6),(8.9,6),(8.9,5.52));c.wire((8.9,4.48),(8.9,0));c.dot((1,10));c.ground((8.9,0))
 if key=='F088':c.text(19.7,8.5,'$R_3$',ha='left');c.text(19.7,1.5,'$R_4$',ha='left');c.text(-1.4,4,r'$30\,\mathrm{V}$')
 else:part(c,'R',(20,10),(20,0),'R_L');c.wire((17,10),(20,10));c.wire((17,0),(20,0));c.labels=[r for r in c.labels if not (abs(r[0]-19.7)<.01 and r[2]=='$U_O$')];c.text(22,5,'$U_O$')
 return c

c=offset_reg('F088','W7805',numbered=True);save(c,'E9-10恢复W7805完整电路；输出到采样R1=2.5k、采样到公共端R2=2.5k，负端取中点；正端取右侧1.5k电位器滑端，上500Ω/下2.5k；R3/R4为滑动分段，不反填计算结果。')
c=offset_reg('F092-a','W7812');c.save()
c,g=regbase('F092-b','W117');part(c,'R',(1,10),(1,4),'R_1',offset=-.5);c.wire((1,4),(g[0],4),g);part(c,'R',(13,10),(13,4),'R_2');c.wire((13,4),(1,4));part(c,'Z',(g[0],0),(g[0],4),'D_Z');dot(c,(1,10),(g[0],4));c.text(11,7,r'$U_{\mathrm{REF}}$');c.text(12,9,'$+$');c.text(12,5,'$-$');c.save()
c=C('F092-c','E9-16(c)',size=(16,12));a,b,g=regulator(c,3,10,'W117');c.wire((0,10),a);c.wire(b,(17,10));c.wire((0,-4),(14,-4));cap(c,1,10,0,'C_1');cap(c,1,0,-4,'C_2');part(c,'Z',(7,-4),(7,0),'D_Z');part(c,'R',(12,10),(12,4),'R_1');c.wire(g,(g[0],4),(12,4),(12,-2));part(c,'R',(11,0),(11,-4),'R_2',offset=-.5);arrow(c,(12,-2),(11.2,-2));c.wire((1,0),(17,0));c.ground((1,0));c.port((0,10),'$+$');c.port((0,-4),'$-$');c.text(-1.4,3,'$U_I$');c.port((17,10),'$+$','right');c.port((17,0),'$-$','right');c.text(18,5,'$U_O$');c.text(13.5,7,r'$U_{\mathrm{REF}}$');c.text(12.5,10,'$+$');c.text(12.5,4,'$-$');c.text(13,-.8,r"$R_2^{\prime}$");c.text(13,-3.2,r"$R_2^{\prime\prime}$");dot(c,(1,0),(7,0),(7,-4));c.save();panels('F092',['F092-a','F092-b','F092-c']);QA['F092']='E9-16三幅完整：a为W7812、R2输出/R1公共端、正端取R4滑端及RL；b为W117+DZ参考/R1输入供电/R2输出至ADJ；c地在两输入电容中点，输出负端同该地，DZ跨下半电源，R2滑端回ADJ、下端接输入负端，R2′/R2″保留。'

c=C('F093','E9-17',size=(16,11));a,b,g=regulator(c,3,10,'LM317');c.wire((0,10),a);c.wire(b,(18,10));c.wire((0,0),(18,0));ports(c,0,18,10);c.text(2.5,11,'IN');c.text(6.8,11,'OUT');c.text(4,8.7,'ADJ',ha='right');c.text(2.5,9.3,'$2$');c.text(6.5,9.3,'$3$');c.text(5.2,8.7,'$1$');cap(c,1.5,10,0,'C_1');c.wire(g,(g[0],4));part(c,'R',(g[0],4),(g[0],0),r'R_2=6.2\,\mathrm{k}\Omega',offset=-.5);c.wire((g[0],4),(11,4));part(c,'R',(11,10),(11,4),r'R_1=210\,\Omega',offset=-.5);cap(c,11,4,0,'C_2');part(c,'D',(14,4),(14,10),'D');c.wire((11,4),(14,4));cap(c,16,10,0,'C_3');arrow(c,(6,2),(4.7,2));c.wire((6,2),(6,4));dot(c,(g[0],4),(11,4),(11,10),(16,10),(16,0));save(c,'LM317引脚IN=2/OUT=3/ADJ=1按原图；R1=210Ω、R2标6.2kΩ可调且滑端回ADJ；C1输入/C2旁路/C3输出，保护D阳极ADJ、阴极OUT。题干另指定3kΩ计算时不改原图标值。')

(HERE/'ic-geometry.json').write_bytes((json.dumps(M.records,ensure_ascii=False,indent=2)+'\n').encode())
(HERE/'qa-ic.json').write_bytes((json.dumps(QA,ensure_ascii=False,indent=2)+'\n').encode())
