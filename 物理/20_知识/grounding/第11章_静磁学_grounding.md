# 第11章 静磁学 grounding

## 来源与边界

- 主来源：`物理/00_原材料/大学物理学（下册）（第二版） (孙云卿，雷雨) (z-library.sk, 1lib.sk, z-lib.sk).pdf` 第11章，目录标示教材页 71-119；本轮重点读取第11章正文、思考题入口和学习指导题面。
- 辅助来源：`物理/10_题库/学习指导/学习指导_第11章_静磁学_题面整理.md`，只用于题型信号；`物理/10_题库/_标签库.md`，确认受控标签 `学习指导｜静磁学综合`；`物理/20_知识/README.md`，确认第11章对应教材与三件套路径。
- 不扩展到课外：不引入教材外磁标势、边界条件体系、麦克斯韦方程完整组、相对论电动力学推导细节或工程磁路理论。
- 教材缓存 `completion.json` 显示 status 为 complete，但本轮局部运行 `verify_completion.py` 未通过 schema/status 检查；因此最终范围说明以原 PDF 直接文本抽取和允许的辅助文件为准。

## 本章主线

稳恒电流和运动电荷产生磁场，磁场由磁感应强度 $\mathbf B$ 描述。计算磁场有两条入口：一般电流分布用毕奥-萨伐尔定律积分叠加；高对称稳恒电流分布用安培环路定理。磁场再作用于运动电荷和载流导线，微观表现为洛伦兹力，宏观表现为安培力和载流线圈力矩。加入磁介质后，磁化电流参与产生总磁场，引入 $\mathbf M$ 和 $\mathbf H$ 来区分磁化响应与传导电流贡献。

S10 对话优先让学生说清：源是什么、场点在哪里、方向如何定、是否具备对称性、求的是 $\mathbf B$ 还是 $\mathbf H$。

## 课程用语与记号

- 磁感应强度：$\mathbf B$，单位 T，描述磁场强弱和方向。
- 磁通量：$\Phi_m=\int_S \mathbf B\cdot \mathrm d\mathbf S$。
- 真空磁导率：$\mu_0=4\pi\times 10^{-7}\,\mathrm{T\cdot m/A}$。
- 电流元：$I\,\mathrm d\mathbf l$，方向沿电流方向。
- 洛伦兹力：$\mathbf f=q\mathbf v\times\mathbf B$；含电场时教材写 $\mathbf F=q\mathbf E+q\mathbf v\times\mathbf B$。
- 安培力：$\mathrm d\mathbf F=I\,\mathrm d\mathbf l\times\mathbf B$。
- 磁矩：$\mathbf p_m=NIS\,\mathbf e_n$；力矩 $\mathbf M=\mathbf p_m\times\mathbf B$。
- 磁化强度：$\mathbf M$；磁场强度：$\mathbf H=\mathbf B/\mu_0-\mathbf M$。
- 线性各向同性介质：$\mathbf M=\chi_m\mathbf H$，$\mathbf B=\mu_0\mu_r\mathbf H=\mu\mathbf H$。

## 公式 / 方法 / 条件

- 毕奥-萨伐尔定律：
  $$
  \mathrm d\mathbf B=\frac{\mu_0}{4\pi}\frac{I\,\mathrm d\mathbf l\times\mathbf e_r}{r^2}
  =\frac{\mu_0}{4\pi}\frac{I\,\mathrm d\mathbf l\times\mathbf r}{r^3}.
  $$
  条件：稳恒电流；需对电流分布积分；方向由叉乘给出。
- 典型结果：无限长直导线 $B=\mu_0 I/(2\pi a)$；圆电流圆心 $B=\mu_0 I/(2R)$；长直螺线管内部近似匀强，按教材轴线叠加或后续安培环路处理。
- 磁场高斯定理：
  $$
  \oint_S\mathbf B\cdot\mathrm d\mathbf S=0,\qquad \nabla\cdot\mathbf B=0.
  $$
  条件：磁感应线无头无尾；闭合曲面磁通量为零。
- 真空中安培环路定理：
  $$
  \oint_L\mathbf B\cdot\mathrm d\mathbf l=\mu_0\sum I_{\text{内}}.
  $$
  使用条件：稳恒闭合电流；对称性足够强时才可直接解 $B$。左侧 $\mathbf B$ 是所有电流合场，右侧只计环路所包围电流代数和。
- 洛伦兹力：
  $$
  \mathbf f=q\mathbf v\times\mathbf B,\qquad f=|q|vB\sin\theta.
  $$
  条件：磁场力垂直速度，不做功；正负电荷方向相反。
- 匀强磁场中带电粒子：
  $$
  R=\frac{mv}{|q|B},\qquad T=\frac{2\pi m}{|q|B}
  $$
  适用于 $\mathbf v\perp\mathbf B$ 的圆周分量；一般斜入射可分解为平行匀速与垂直圆周。
- 安培力和力矩：
  $$
  \mathrm d\mathbf F=I\,\mathrm d\mathbf l\times\mathbf B,\qquad
  \mathbf M=\mathbf p_m\times\mathbf B.
  $$
  匀强磁场中闭合线圈合力为零但可有力矩；非匀强磁场中可同时平动和转动。
- 介质中安培环路定理：
  $$
  \oint_L\mathbf H\cdot\mathrm d\mathbf l=\sum I_{0\text{内}}.
  $$
  只计传导电流；再用 $\mathbf B=\mu\mathbf H$ 或 $\mathbf M=\chi_m\mathbf H$ 求目标量。
- 磁化电流：
  $$
  \mathbf J'=\mathbf M\times\mathbf e_n.
  $$
  用于介质表面磁化电流方向与大小判断。

## 题型信号与第一步

- 受控标签：`学习指导｜静磁学综合`。
- 载流导线、圆环、半圆片、螺旋线、旋转带电体：第一步选电流元或等效圆电流，判断方向叠加，通常入口为毕奥-萨伐尔。
- 无限长圆柱、挖空导体、同轴线、螺线环、无限大面电流：第一步判断对称性和包围电流分段，通常入口为安培环路定理。
- 半球面磁通量：第一步补成闭合曲面，用 $\oint\mathbf B\cdot\mathrm d\mathbf S=0$。
- 带电粒子进入磁场、电子出射点、反求 $\mathbf B$：第一步画 $\mathbf v,\mathbf B,\mathbf f$，判断电荷正负和圆周半径。
- 霍尔效应：第一步判断载流子符号、漂移方向、洛伦兹力方向和横向电场方向。
- 载流导线、圆电流、线圈受力/力矩/做功：第一步写 $I\,\mathrm d\mathbf l\times\mathbf B$ 或磁矩 $\mathbf p_m$。
- 磁介质、铁环、$\mu_r$、$\chi_m$、$\mathbf H$：第一步先用传导电流求 $\mathbf H$，再换算 $\mathbf B,\mathbf M$ 或磁化电流。

## 高频/考试提示

- 未运行新的 S2 考频统计；不得声称频率结论。
- 从学习指导题面看，入口覆盖较广：磁场计算、安培环路、磁通量、洛伦兹力轨迹、霍尔效应、安培力/力矩、磁介质与铁磁质计算均出现。
- 标签库仅给出总标签 `学习指导｜静磁学综合`，不要在正式题库标签外新造细标签。

## S10 主动 probe 种子

1. 这题是“电流产生磁场”，还是“磁场作用于电荷/电流”，还是“磁介质中的场”？
2. 如果你想用安培环路定理，哪条路径上 $B$ 的大小能被拿出积分号？为什么？
3. 你画出的 $\mathbf B$ 或 $\mathbf f$ 方向，用的是哪个右手定则？负电荷是否要反向？
4. 这个题求的是 $\mathbf B$ 还是 $\mathbf H$？有没有磁介质，右边应不应该只计传导电流？
5. 若把电流取零、半径取无穷或磁导率取 $\mu_r=1$，你的结果是否回到合理极限？

## 范围待确认

- 教师课堂是否要求掌握教材 11.8 铁磁质的磁滞回线与磁畴到计算题深度，未确认；本轮按教材基础概念和学习指导入口处理。
- 阅读材料“磁流体发电”只作为洛伦兹力应用理解，不写成必考主线。
- 教材 PDF 转换缓存的 completion 独立校验在本轮未通过脚本 gate；父线程若做 digest/verify，可进一步确认缓存状态。
