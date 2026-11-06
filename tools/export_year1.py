from pathlib import Path
import os,re,json,shutil,hashlib,urllib.parse,sys
from collections import defaultdict,deque

SRC=Path('D:/FuckTheClass')
OUT=Path('D:/FuckTheClass-publish/fuck-the-class-year1')
SRC=SRC.resolve(); OUT=OUT.resolve()
sys.path.insert(0,str(OUT/'tools'))
from publish_policy import excluded, preferred, publication_text, clean_existing, references
COURSES=['微积分','电路分析','物理']
allfiles=[]
for c in COURSES:
    for root,ds,fs in os.walk(SRC/c):
        ds[:]=[d for d in ds if d not in ['node_modules','.git','__pycache__','lo-profile','lo-profile-single']]
        allfiles.extend(Path(root)/f for f in fs)
byname=defaultdict(list)
for p in allfiles: byname[p.name.lower()].append(p)

def resolve(raw,doc):
    raw=urllib.parse.unquote(raw.strip().replace('\\|','|').split('|')[0]).replace('\\','/')
    if re.match(r'^(https?:|data:|mailto:|plugin:)',raw): return None
    raw=raw.split('#')[0].strip().strip('<>')
    if not raw: return None
    candidates=[doc.parent/raw,SRC/raw,SRC/doc.relative_to(SRC).parts[0]/raw]
    if re.match(r'^[A-Za-z]:/',raw): candidates.insert(0,Path(raw))
    for p in candidates:
        for q in [p,p.with_suffix('.md') if not p.suffix else p]:
            if q.is_file(): return preferred(q.resolve())
    for name in [Path(raw).name,Path(raw).name+'.md']:
        found=byname.get(name.lower(),[])
        same=[p for p in found if p.relative_to(SRC).parts[0]==doc.relative_to(SRC).parts[0]]
        if len(same)==1: return preferred(same[0])
        if len(same)>1 and re.fullmatch(r'[0-9a-f]{64}\.[a-z]+',name):
            if len({hashlib.sha256(p.read_bytes()).hexdigest() for p in same})==1: return preferred(same[0])
    return None

def refs(text):
    for start,end,raw,kind,label in references(text):
        yield ('source' if kind=='code' else 'link' if kind in ['image','reference','tex','css'] else kind,raw)

selected=set(); reasons={}; queue=deque(); missing=[]; edges=[]; blocked=[]
def add(p,reason):
    p=preferred(p.resolve())
    if not p.is_relative_to(SRC): return
    if excluded(p.relative_to(SRC)): return
    rel=p.relative_to(SRC)
    if '30_我的数据' in rel.parts or p.name=='学生状态快照.md':
        blocked.append({'from':reason,'target':str(rel)}); return
    if p not in selected:
        selected.add(p); reasons[str(rel)]=reason
        if p.suffix.lower() in ['.md','.json','.html','.css','.tex','.txt']: queue.append(p)

for p in allfiles:
    rel=p.relative_to(SRC); parts=rel.parts; c=parts[0]
    if c!='物理':
        if len(parts)>1 and parts[1] in ['00_原材料','10_题库','20_知识','40_派生视图'] and not any(x in parts for x in ['temp','node_modules']): add(p,'course content')
        if len(parts)>2 and parts[1:3]==('10_工作区','章节梳理'): add(p,'legacy chapter document')
    else:
        chapter=re.search(r'第(\d+)章',p.name)
        if len(parts)>1 and parts[1]=='20_知识' and chapter and int(chapter[1])<=9: add(p,'physics upper chapters')
        if len(parts)>2 and parts[1:3]==('40_派生视图','大物上'): add(p,'physics upper views')
        if p.suffix=='.md' and len(parts)>2 and parts[1]=='10_题库':
            if parts[2]=='学习指导' and chapter and int(chapter[1])<=9: add(p,'upper exercises')
            if parts[2]=='清华题库' and chapter and int(chapter[1])<=5: add(p,'upper question bank')
            if parts[2]=='习题册' and '下册' not in p.name: add(p,'upper workbook')
            if parts[2]=='历年真题' and '大学物理II' not in parts: add(p,'upper exams')
        if len(parts)==2 and (p.suffix=='.md' or p.suffix=='.pdf'): add(p,'upper original/index')
        if '大学物理习题册（上）' in parts and p.suffix=='.md': add(p,'upper original workbook')
        if len(parts)>1 and parts[1]=='00_原材料' and ('十三五' in p.name or '十一五' in p.name or '清华' in p.name): add(p,'upper source textbook')
        if p.name=='_标签库.md': add(p,'tag vocabulary')

while queue:
    p=queue.popleft()
    try: text=p.read_text(encoding='utf-8-sig')
    except (UnicodeError,OSError): continue
    for kind,raw in refs(text):
        target=resolve(raw,p)
        if target and target.is_relative_to(SRC) and excluded(target.relative_to(SRC)):
            blocked.append({'from':str(p.relative_to(SRC)),'target':str(target.relative_to(SRC))}); continue
        if target:
            edges.append((p,target,kind,raw)); add(target,str(p.relative_to(SRC)))
        elif kind!='source' and not re.match(r'^(https?:|data:|mailto:|#)',raw) and not (SRC/raw.split('|')[0]).is_dir():
            missing.append({'document':str(p.relative_to(SRC)),'kind':kind,'reference':raw})

OUT.mkdir(parents=True,exist_ok=True)
# Prune older exports too; filtering new copies alone leaves stale tracked files.
clean_existing(OUT)
manifest=[]
repairs=[]
for p in sorted(selected):
    rel=p.relative_to(SRC); dest=OUT/rel; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,dest)
    if p.suffix.lower() in ['.md','.html','.tex','.css','.json']:
        body=p.read_text(encoding='utf-8-sig')
        body=publication_text(body,p,SRC)
        dest.write_text(body,encoding='utf-8',newline='\r\n' if b'\r\n' in p.read_bytes() else '\n')
    manifest.append({'path':rel.as_posix(),'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
loss=[{'document':str(p.relative_to(SRC)),'target':str(q.relative_to(SRC))} for p,q,k,r in edges if q.is_relative_to(SRC) and not (OUT/q.relative_to(SRC)).is_file()]
report={'files':len(manifest),'MiB':round(sum(x['bytes'] for x in manifest)/2**20,2),'retained_cache_files':sum('/90_缓存/' in x['path'] for x in manifest),'preexisting_unresolved_links':missing,'excluded_private_dependencies':blocked,'export_missing_dependencies':loss,'large_files':[x for x in manifest if x['bytes']>95*2**20]}
report['repaired_links']=repairs
for tool in sorted((OUT/'tools').glob('*.py')):
    manifest.append({'path':tool.relative_to(OUT).as_posix(),'bytes':tool.stat().st_size,'sha256':hashlib.sha256(tool.read_bytes()).hexdigest()})
(OUT/'export-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8',newline='')
(OUT.parent/'export-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT.parent/'export-reasons.json').write_text(json.dumps(reasons,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v if not isinstance(v,list) else len(v) for k,v in report.items()},ensure_ascii=False))
