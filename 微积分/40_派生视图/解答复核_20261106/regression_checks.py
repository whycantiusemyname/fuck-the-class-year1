import json,math
from pathlib import Path
import sympy as s
from scipy.integrate import quad,dblquad
out=Path(__file__).resolve().parent
results=[]
def check(label,value,expected,tol=1e-8):
    value=float(value);expected=float(expected)
    assert abs(value-expected)<=tol*max(1,abs(expected)),(label,value,expected)
    results.append(dict(label=label,value=value,expected=expected))
pi=math.pi
check('18-19期中算6：原正方形上二维数值积分',
 dblquad(lambda y,x:1/(1+x*x+y*y)**2,0,1,lambda x:0,lambda x:1)[0],math.atan(1/math.sqrt(2))/math.sqrt(2))
check('20-21期中算6：取整径向变量独立积分',
 quad(lambda t:t*math.floor(1+t)/4,0,math.sqrt(2),points=[1])[0],3/8)
check('23-24期末算6：下半球上侧直接参数通量',
 dblquad(lambda ph,th: (-(2*(math.sin(ph)*math.cos(th))**2)+3*(math.sin(ph)*math.sin(th))**2
 +(1+math.cos(ph))**2*math.cos(ph))*math.sin(ph),
 0,2*pi,lambda th:0,lambda th:pi/2)[0],7*pi/2)
def line(t):
    x,y,z=1+math.cos(t),math.sin(t),2*math.sin(t/2)
    return (z*z-y*y)*(-math.sin(t))+(x*x-z*z)*math.cos(t)+(y*y-x*x)*math.cos(t/2)
check('23-24期末算7：原曲线参数直接数值积分',quad(line,0,2*pi)[0],4*pi)
check('19-20期末算4：原上半圆弧直接积分',
 quad(lambda t: math.exp(math.sin(t))*(-math.sin(t))+
 (1+math.cos(t))*(math.sin(t)+math.exp(math.sin(t)))*math.cos(t),pi,0)[0],4/3)
check('14-15期中算8：抛物面质量',6*pi*quad(lambda r:r*math.sqrt(1+4*r*r),0,math.sqrt(2))[0],13*pi)
check('13-14期中填1：固定y的对数极限',
 s.limit(s.Symbol('x')**2/(s.Symbol('x')+2)*s.log(1+1/(2*s.Symbol('x'))),s.Symbol('x'),s.oo),s.Rational(1,2))
x,y,z,u,v,w=s.symbols('x y z u v w',real=True)
f=u**3+2*u*u*v+3*u*v*v+v**3+u*v
f1,f2=s.diff(f,u),s.diff(f,v)
f11,f12,f22=s.diff(f,u,2),s.diff(f,u,v),s.diff(f,v,2)
def chain(label,U,V,formula,kind='xy',outer=1):
    env={u:U,v:V}
    actual=s.diff(outer*f.subs(env,simultaneous=True),x,y) if kind=='xy' else s.diff(f.subs(env,simultaneous=True),x,2)
    predicted=formula.subs(env,simultaneous=True)
    assert s.simplify(actual-predicted)==0,label
    results.append(dict(label=label,symbolic='zero residual for nonseparable cubic probe'))
g=1+x*x;gp=s.diff(g,x)
chain('10-11期中算4：系数项乘积求导',x+2*y,y*g,2*f11+(g+2*y*gp)*f12+y*g*gp*f22+gp*f2)
chain('11-12期中算5',x*y,x*x,f1+x*y*f11+2*x*x*f12)
chain('11-12期末选2',x*y,x*x-y*y,f1+x*y*f11+2*(x*x-y*y)*f12-4*x*y*f22)
chain('13-14/15-16期中复合函数',x+y,x*s.exp(y),f11+(x+1)*s.exp(y)*f12+x*s.exp(2*y)*f22+s.exp(y)*f2)
chain('16-17期中算1',x+y,x*y,f11+(x+y)*f12+x*y*f22+f2)
chain('18-19期中算4',x*y,(x*x-y*y)/2,y*y*f11+2*x*y*f12+x*x*f22+f2,kind='xx')
chain('19-20期末填2',x,x*y,x*f12+f2+x*y*f22)
chain('22-23期中算3',x-y,x*y,-f11+(x-y)*f12+x*y*f22+f2)
chain('23-24期中算4',x*y,x*x+y*y,2*x*f1+2*y*f2+x*x*y*f11+2*(x**3+x*y*y)*f12+4*x*x*y*f22,outer=x)
chain('24-25期末算3',2*x-y,y*s.sin(x),-2*f11+(2*s.sin(x)-y*s.cos(x))*f12+y*s.sin(x)*s.cos(x)*f22+s.cos(x)*f2)
r,t=s.symbols('r t',positive=True)
cases=[
 ('15-16期中第8题',s.integrate(t*(t-1),(t,1,3))/s.integrate(t-1,(t,1,3)),s.Rational(7,3)),
 ('15-16期末第5题',s.integrate(t**3*s.exp(-t*t)/3,(t,0,1)),(1-2/s.E)/6),
 ('15-16期末第6题',2*s.pi*s.integrate(t*t,(t,0,8)),1024*s.pi/3),
 ('16-17期中第6题',s.pi/2*s.integrate((1-r*r)*r,(r,0,1)),s.pi/8),
 ('16-17期中第7题',s.integrate(t*t*(3-3*t/2),(t,0,2)),2),
 ('16-17期末第5题',12*s.integrate(t*t*(1-t),(t,0,1)),1),
 ('16-17期末第6题：半球多项式通量',3*s.integrate(r**4,(r,0,1))*s.integrate(s.sin(t)**3,(t,0,s.pi/2))*2*s.pi,4*s.pi/5),
 ('缺卷头P54算5：两类矩独立合成',6*s.pi/5+s.pi/4,29*s.pi/20),
 ('23-24期末质心',s.Rational(1,5)/s.Rational(1,2),s.Rational(2,5)),
]
for label,actual,expected in cases:check(label,actual,expected)
# Check the convergent power series against their rational/logarithmic originals away from their centers.
for q in [-0.4,0.3,0.7]:
    value=-sum((1/2**(n+1)+(-1)**n/3**(n+1))*q**n for n in range(80))/5
    check('22-23期末泰勒：数值回代 t='+str(q),value,1/((q-2)*(q+3)))
# New source-comparison regressions.
C1,C2=s.symbols('C1 C2')
U=r**4/16+C1*s.log(r)+C2
check('12-13期中算8：径向通解代回',s.simplify(s.diff(U,r,2)+s.diff(U,r)/r-r*r),0)
yp=-x*(1+6*z)/(2*y*(1+3*z));zp=x/(1+3*z)
check('20-21期末算11：第一式导数残差',s.simplify(zp-2*x-2*y*yp),0)
check('20-21期末算11：第二式导数残差',s.simplify(2*x+4*y*yp+6*z*zp),0)
check('22-23期末算8：展开中心常数项',-s.Rational(1,5)*(s.Rational(1,2)+s.Rational(1,3)),-s.Rational(1,6))
(out/'mathematical-checks.json').write_text(json.dumps({'checks':len(results),'results':results},ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS',len(results),'independent symbolic/numerical checks')
