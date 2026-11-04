# 第10章 静电学 grounding

## 来源与边界

- 主来源：`物理/00_原材料/大学物理学（下册）（第二版） (孙云卿，雷雨) (z-library.sk, 1lib.sk, z-lib.sk).pdf` 第10章。
- 教材目录边界：10.1 电场；10.2 电场的描述；10.3 高斯定理；10.4 静电场环路定理；10.5 静电场中的导体；10.6 电介质；10.7 电容和电容器；10.8 静电场的能量；阅读材料“热电体、压电体、铁电体和驻极体”。
- 辅助来源：`10_题库/学习指导/学习指导_第10章_静电学_题面整理.md`、`10_题库/_标签库.md`、`20_知识/README.md`。
- 题库只用于题型命名和 S10 入口信号，不把学习指导解析当教材主线。
- 本 grounding 只供 AI tutor 控制边界，不替代 `第10章_静电学_主干讲解.md`。

## 本章主线

静止电荷产生静电场，静电场用场强 $\boldsymbol E$ 描述力的性质，用电势 $U$ 描述能的性质。主线按：

> 库仑定律与电力叠加
> → 电场强度与场强叠加
> → 电通量与高斯定理
> → 环路定理、电势、电势梯度
> → 导体静电平衡与感应电荷
> → 电介质极化、电位移 D
> → 电容器与静电场能量

S10 中优先让学生先判断对象、边界与入口，再调用公式。

## 课程用语与记号

- 静电荷、静电场、源电荷、检验电荷、场点。
- 电场强度 $\boldsymbol E$，电场力 $\boldsymbol F=q_0\boldsymbol E$。
- 电通量 $\Phi_e$，闭合曲面外法线 $d\boldsymbol S$，高斯面。
- 电势 $U$，电势差，电势零点，等势面，电势梯度。
- 电荷线密度 $\lambda$、面密度 $\sigma$、体密度 $\rho$。
- 导体静电平衡、静电感应、静电屏蔽、接地。
- 电介质、极化、极化强度 $\boldsymbol P$、束缚电荷、自由电荷、电位移 $\boldsymbol D$、相对介电常量 $\varepsilon_r$。
- 电容 $C$、电容器电压 $V$、静电场能量 $W_e$、能量密度 $w_e$。

## 公式 / 方法 / 条件

- 库仑定律：
  $$
  \boldsymbol F=\frac{1}{4\pi\varepsilon_0}\frac{q_1q_2}{r^2}\boldsymbol e_r
  $$
  条件：真空中两个静止点电荷；方向沿连线。
- 场强定义：
  $$
  \boldsymbol E=\boldsymbol F/q_0
  $$
  条件：检验电荷足够小，不扰动源电荷分布。
- 点电荷场强：
  $$
  \boldsymbol E=\frac{1}{4\pi\varepsilon_0}\frac{q}{r^2}\boldsymbol e_r
  $$
  正电荷沿矢径向外，负电荷方向相反。
- 连续分布场强：
  $$
  d\boldsymbol E=\frac{1}{4\pi\varepsilon_0}\frac{dq}{r^2}\boldsymbol e_r,\quad
  dq=\lambda dl,\ \sigma dS,\ \rho dV
  $$
  方法：选电荷元，分解矢量分量，利用对称性。
- 电通量：
  $$
  \Phi_e=\int_S \boldsymbol E\cdot d\boldsymbol S,\qquad
  \Phi_e=\oint_S \boldsymbol E\cdot d\boldsymbol S
  $$
  闭合面用外法线；通量可正可负。
- 真空中高斯定理：
  $$
  \oint_S \boldsymbol E\cdot d\boldsymbol S=\frac{q_{\text{内}}}{\varepsilon_0}
  $$
  注意：$\boldsymbol E$ 是所有电荷产生的合场强；通量只由面内净电荷决定。直接求 $E$ 需要球/柱/面对称。
- 静电场环路定理：
  $$
  \oint \boldsymbol E\cdot d\boldsymbol l=0
  $$
  含义：静电场保守，电场力做功与路径无关。
- 电势差：
  $$
  U_a-U_b=\int_a^b \boldsymbol E\cdot d\boldsymbol l,\qquad
  A_{a\to b}=q_0(U_a-U_b)
  $$
  零点可选；有限电荷分布常取无穷远，数学无限延伸模型需在有限处选零点。
- 点电荷电势与电势叠加：
  $$
  U=\frac{1}{4\pi\varepsilon_0}\frac{q}{r},\qquad
  U=\sum_i \frac{1}{4\pi\varepsilon_0}\frac{q_i}{r_i},\qquad
  U=\int \frac{1}{4\pi\varepsilon_0}\frac{dq}{r}
  $$
- 场强与电势：
  $$
  \boldsymbol E=-\nabla U
  $$
  只由电势空间变化决定，不由单点电势数值决定。
- 导体静电平衡：
  $$
  \boldsymbol E_{\text{导体内}}=0
  $$
  表面外紧邻场强垂直表面；导体是等势体；实心导体净电荷在表面；空腔无电荷时腔内 $E=0$；腔内有电荷 $q$ 时内表面感应总电荷 $-q$。
- 导体表面附近：
  $$
  E=\sigma/\varepsilon_0
  $$
  条件：静电平衡导体表面外紧邻处。
- 电介质：
  $$
  \boldsymbol D=\varepsilon_0\boldsymbol E+\boldsymbol P,\qquad
  \oint_S \boldsymbol D\cdot d\boldsymbol S=q_{\text{自由,内}}
  $$
  在线性、各向同性、均匀介质且外场不太强时：
  $$
  \boldsymbol D=\varepsilon\boldsymbol E=\varepsilon_0\varepsilon_r\boldsymbol E
  $$
- 电容器：
  $$
  C=Q/V,\qquad C_{\text{平行板}}=\varepsilon_0\varepsilon_r S/d
  $$
  串联：$\frac1C=\frac1{C_1}+\frac1{C_2}+\cdots$。并联：$C=C_1+C_2+\cdots$。
- 电场能量：
  $$
  W_e=\frac{Q^2}{2C}=\frac12CV^2=\frac12QV,\qquad
  w_e=\frac12\varepsilon E^2=\frac12\boldsymbol E\cdot\boldsymbol D
  $$
  电容器变化题先判断固定 $Q$ 还是固定 $V$。

## 题型信号与第一步

- 受控题型名：`学习指导｜静电学综合`。
- 电偶极子、点电荷系：画方向，做矢量叠加；可追问电矩方向与远场近似条件。
- 带电直线、半圆环、圆环、圆盘、球体：选 $dq$，写 $d\boldsymbol E$ 或 $dU$，用对称性消分量。
- 无限长直线、无限大平面、均匀球体/球面、同轴圆柱：优先检查高斯面是否能让 $E$ 提出积分号。
- 立方体高斯面、非均匀场：常是通量/净电荷理解题，不一定要求场强分布。
- 电势、路径、做功、动能变化：先写电势差和零势点；路径通常不是核心。
- 导体球壳、空腔、接地金属板、平行导体板：先写导体内 $E=0$、等势、表面电荷守恒或接地条件。
- 电介质、$\varepsilon_r$、束缚电荷、$\boldsymbol D$：先区分自由电荷和束缚电荷。
- 电容器插介质、拉开极板、串并联：先判断电源连接状态，确定 $Q$ 固定还是 $V$ 固定。
- 电场能量、外力做功：用 $W_e$ 变化或场能密度积分。

## 高频/考试提示

- 未运行 S2 考频，本轮不作频率结论。
- 题库题面显示第10章覆盖面较宽：场强叠加、高斯定理、电势、导体与感应电荷、电介质、电容器、电场能量均出现。
- S10 不应把阅读材料“热电体、压电体、铁电体和驻极体”当作默认应试主线；除非用户明确问教材阅读材料。

## S10 主动 probe 种子

1. 这题要求的是 $\boldsymbol E$、$U$、通量、感应电荷、$C$ 还是 $W_e$？
2. 如果你想用高斯定理，哪个对称性让 $E$ 能从积分号里拿出来？
3. 这个电势题的零势点在哪里？如果改零势点，电势差会不会变？
4. 导体题里，哪一块区域必须满足 $E=0$？哪一块只是等势？
5. 介质题中哪些是自由电荷，哪些是束缚电荷？
6. 电容器题里电源是否断开？固定 $Q$ 还是固定 $V$？
7. 你的答案在 $r\to\infty$、$\varepsilon_r\to1$、$d$ 增大时是否符合直觉？

## 范围待确认

- 教师课堂是否删去 10.5 后半的稳恒电流/欧姆定律/电动势内容：教材第10章含此内容，但用户提示的重点偏静电主线，本轮未作为主干重点展开。
- 教师是否要求阅读材料“热电体、压电体、铁电体和驻极体”：本轮仅标为了解性拓展。
- 是否需要把“电象法/唯一性定理”作为应试主线：教材导体例题出现，但用户给出的重点未点名，本轮只在导体边界题中保留入口，不展开为必会方法。
