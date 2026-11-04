"""Verify exported file hashes, local Markdown/wiki dependencies and credential patterns."""
from pathlib import Path
import re,json,hashlib,urllib.parse,sys

root=Path(__file__).resolve().parents[1]
files=[p for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts]
index={}
for p in files:
    index.setdefault(p.name,[]).append(p)
    index.setdefault(p.stem,[]).append(p)
errors=[]; count=0
for row in json.loads((root/'export-manifest.json').read_text(encoding='utf-8')):
    p=root/row['path']
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']: errors.append(('hash',row['path']))

def exists(raw,doc,wiki=False):
    raw=urllib.parse.unquote(raw.replace('\\|','|').split('|')[0]).strip('<>')
    if re.match(r'^(https?:|mailto:|data:|#)',raw): return True
    raw=raw.split('#')[0].replace('\\','/')
    if not raw: return True
    for base in [doc.parent,root,root/doc.relative_to(root).parts[0]]:
        p=base/raw
        if p.exists() or (wiki and not p.suffix and p.with_suffix('.md').exists()): return True
    return wiki and bool(index.get(Path(raw).name))

secret=re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,}|Bearer\s+[A-Za-z0-9._-]{20,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----)')
for p in files:
    if p.suffix not in ['.md','.json','.txt','.html']: continue
    text=p.read_text(encoding='utf-8-sig',errors='replace')
    if secret.search(text): errors.append(('credential',str(p.relative_to(root))))
    if p.suffix!='.md': continue
    for m in re.finditer(r'!?\[\[([^\]\n]+)\]\]',text):
        count+=1
        if not exists(m[1],p,True): errors.append(('wiki',str(p.relative_to(root)),m[1]))
    for m in re.finditer(r'!?\[[^\]\n]*\]\(',text):
        start=m.end(); end=start; depth=1
        while end<len(text) and depth:
            if text[end]=='(' and text[end-1]!='\\': depth+=1
            if text[end]==')' and text[end-1]!='\\': depth-=1
            end+=1
        if depth: continue
        raw=text[start:end-1]; count+=1
        if not exists(raw,p): errors.append(('markdown',str(p.relative_to(root)),raw))
print(json.dumps({'files':len(files),'links_checked':count,'errors':errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
