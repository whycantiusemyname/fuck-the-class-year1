# 电路分析逐章矢量题图

精确电路使用 Schemdraw 与程序化几何图形绘制；数学文字使用 Matplotlib MathText 的 LaTeX 语法子集和 STIX 字体。没有使用生成式图片工具。SVG 字形转路径，便于跨设备显示上下标；数值、连接与文字的可编辑源在 Python 脚本中。

统一黑白、IEC 矩形电阻、1.65 pt 主线。节点以实心点表示，跨线桥表示不连接。电源、器件、极性和箭头以来源为准，不按常见电路猜补条件。

安装依赖后，在对应目录运行生成脚本：

```powershell
python -m pip install -r requirements.txt
python ch03/generate.py
python ch05/generate.py
python ch06/finish_knowledge.py
python ch07/render_all.py
python ch08/generate.py
python ch09/render_all.py
```

生成会写入该章目录中的 SVG、PNG 和几何记录；原始图片不参与覆盖。重新生成的 SVG 可能包含不同的内部标识和时间戳，重新发布时须复核并更新台账中的输出哈希。第7、8、9章当前采用稿均由主代理重新绘制与核验；被退回的早期草稿保存在工作区缓存中，未用于正式文档或分享仓库。

每章 `ledger.json` 保存原图 SHA-256、引用题目、新图映射和核验结论；`validation.json` 记录校验范围。前后对照与灰度缩图用于检查排版，复杂多子图在窄屏需要放大阅读。

```powershell
python verify.py ch06
```

上述命令核验当前原图/输出哈希、SVG内部引用、PNG可读性及文档图片引用。`--adoption-snapshot` 是采用当时的严格文字快照检查；后续章节换图或其他任务经授权修改答案/状态后，旧快照不代表当前文档应恢复到旧版本。

原题、原答案截图均保留。重绘稿不是原参考答案；原件条件缺失、裁边或方向无法裁决时保留原图，并在台账中列为待确认。
