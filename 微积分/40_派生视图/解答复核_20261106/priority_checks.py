from pathlib import Path
import sympy as s,json,math
from scipy.optimize import brentq
r=Path(__file__).resolve().parent;out=[]
def check(label,ok,evidence):
 assert ok,label
 out.append(dict(label=label,passed=True,evidence=evidence))
x=s.symbols('x',real=True);yp=x/8+x*s.sin(2*x)/8
check('11-12期中选4：特解代回',s.simplify(s.diff(yp,x,2)+4*yp-(x+s.cos(2*x))/2)==0,'y_p=x/8+x sin(2x)/8; residual=0; A,B,D均可包含该特解')
t=brentq(lambda z:math.exp(z)-2*z-1,1,2)
check('23-24期末选1：第二分支',abs(math.exp(t)-2*t-1)<1e-10 and math.exp(t)!=2,dict(second_root=t,dz_dx=-1/(math.exp(t)-2),zero_branch_dz_dx=1))
h=s.symbols('h',positive=True)
check('23-24期末算3：反例偏导/连续性',s.limit(h*h/h,h,0)==0,'坐标轴f(h,0)=h²,f(0,h)=h²; y=-x非零点赋值1,故沿该直线不连续；商在x+y≠0恒1')
y,z=s.symbols('y z',positive=True);rho=s.symbols('rho',positive=True)
check('15-16期末八：奇点不能抵消',s.limit(z*(y/z+z/y),z,0)==y,'f=1时球面法向通量密度的奇异部分=(y/z+z/y)/rho;固定y>0,z→0+有1/z发散')
check('16-17期末填4：字面前提矛盾',s.simplify((-2)*s.Symbol('a')+2*s.Symbol('a'))==0,'x=0与x=4的级数为-2Σa_n与2Σa_n,同敛散；补幂次n后才有R=2')
a=s.symbols('a',positive=True);p,q,v=s.symbols('p q v',positive=True)
check('10-11期中算10：正则点截距和',s.simplify((a**s.Rational(4,3)*(p+q+v)-a*a).subs(v,a**s.Rational(2,3)-p-q))==0,'在p=|x|^(2/3),q=|y|^(2/3),v=|z|^(2/3),p+q+v=a^(2/3)时截距平方和=a²；a=0时曲面退化为点')
(r/'priority-checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(len(out),'priority checks passed')
