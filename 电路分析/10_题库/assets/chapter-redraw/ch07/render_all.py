"""Rebuild the main agent's accepted chapter candidates without touching documents."""
from pathlib import Path
import json,subprocess,sys
HERE=Path(__file__).resolve().parent
for name in ['generate.py','generate_exam.py','generate_extra.py','generate_teaching.py']:
 subprocess.run([sys.executable,str(HERE/name)],check=True)
load=lambda p:json.loads(p.read_text(encoding='utf8'))
rows=load(HERE/'geometry.json')
for name in ['exam-geometry.json','extra-geometry.json','teaching-geometry.json']:rows+=load(HERE/name)
(HERE/'geometry.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
verified={}
for name in ['qa-partial.json','qa-exam.json','qa-extra.json','qa-teaching.json']:
 verified.update({k:v for k,v in load(HERE/name).items() if '-' not in k})
pending={
 'F005':'保留仿真原截图：XBP1测量端、彩色交叉布线及U1供电脚的连接尚未从原生仿真文件独立确认。需要原生电路/网表再裁决，暂不发布猜测的电路图。',
 'F009':'A7的二极管方向/符号仍有来源歧义；保留原手绘图，等待更清楚的原题或教师裁决。',
 'F139':'已回查扫描件物理第63页；六小图中(4)左侧电源的数值在原扫描中也截缺，只剩V，不能根据答案反填−2V。整幅保留原图，需未截缺原卷。'
}
(HERE/'qa.json').write_text(json.dumps({'verified':verified,'pending':pending},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(len(verified),'main-agent redraws;',len(pending),'sources pending')
