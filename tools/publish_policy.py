"""Publication policy shared by the exporter and one-time cleanup.

Course scripts and process artifacts stay in the source workspace. Only the
publication tooling itself lives under the share repository's root tools/.
"""
from pathlib import Path
import re
from functools import lru_cache


@lru_cache(maxsize=4)
def file_index(root):
    index = {}
    for p in root.rglob("*"):
        if p.is_file() and ".git" not in p.relative_to(root).parts:
            index.setdefault(p.name, []).append(p)
    return index


def excluded(path):
    """Return the exclusion category, or None for course reading material."""
    p = Path(path)
    parts = p.parts
    name = p.name.lower()
    if parts and parts[0] == 'tools' and name in {'publish_policy.py', 'export_year1.py'}:
        return None
    if p.suffix.lower() in {'.py', '.pyc', '.js', '.sh', '.ps1', '.bat'}:
        return 'process_scripts'
    if p.suffix.lower() in {'.png', '.jpg', '.jpeg', '.pdf'} and re.search(
            r'comparison|svg[-_]render|(?:^|[-_])render(?:ed)?(?:[-_.]|$)|对照|联系表|contact[-_]sheet', name):
        return 'render_comparisons'
    if any(x.lower() in {'reports', 'validation-logs', '__pycache__', 'node_modules', '.git'} for x in parts):
        return 'audit_artifacts'
    if any(re.search(r'图像可读性复核|image-readability|visual[-_]review', x, re.I) for x in parts):
        return 'audit_artifacts'
    if name == 'export-audit.json' or p.suffix.lower() == '.log':
        return 'audit_artifacts'
    if p.suffix.lower() == '.json' and re.search(
            r'verif|validat|audit|review|layout|geometry|ledger|^qa\.|completion|核验|审计|复核|全册覆盖', name):
        return 'audit_artifacts'
    if p.suffix.lower() == '.md' and re.search(r'验收报告|核验报告|排版复核|格式审计报告|重绘核对记录', name):
        return 'audit_artifacts'
    return None


def preferred(path):
    """A same-stem SVG is the published representation of a PNG/PDF."""
    p = Path(path)
    svg = p.with_suffix('.svg')
    return svg if p.suffix.lower() in {'.png', '.pdf'} and svg.is_file() else p


def references(text):
    """Yield (start, end, destination, kind, label) without losing URL suffixes."""
    for m in re.finditer(r'(!?)\[\[([^\]\n]+)\]\]', text):
        yield m.start(), m.end(), m[2], 'wiki', m[2].split('|')[-1]
    for m in re.finditer(r'(!?)\[([^\]\n]*)\]\(', text):
        end = m.end(); depth = 1
        while end < len(text) and depth:
            if text[end] == '(' and text[end-1] != '\\': depth += 1
            if text[end] == ')' and text[end-1] != '\\': depth -= 1
            end += 1
        if not depth:
            yield m.start(), end, text[m.end():end-1], 'image' if m[1] else 'link', m[2]
    for pattern, kind in [
        (r'(?:src|href)=["\']([^"\']+)["\']', 'html'),
        (r'\\(?:includegraphics|input|include)(?:\[[^\]]*\])?\{([^}]+)\}', 'tex'),
        (r'(?m)^\s*\[[^\]\n]+\]:\s*(<[^>]+>|\S+)', 'reference'),
        (r'url\(["\']?([^\)"\']+)["\']?\)', 'css'),
        (r'`([^`\n]+\.(?:md|pdf|png|svg|json|py|log|html))`', 'code'),
    ]:
        for m in re.finditer(pattern, text, re.I):
            yield m.start(1), m.end(1), m[1], kind, m[1]


def resolve_reference(raw, doc, root, wiki=False):
    import urllib.parse
    raw = urllib.parse.unquote(raw.replace('\\|', '|').split('|')[0]).strip().strip('<>')
    if re.match(r'^(?:[a-z]+://|data:|mailto:|plugin:|#)', raw, re.I): return None
    raw = raw.split('#')[0].split('?')[0].replace('\\', '/')
    if not raw: return None
    # Absolute source paths in prose/front matter can also identify a dependency.
    if raw.lower().startswith('d:/fucktheclass/'):
        raw = raw[len('d:/fucktheclass/'):]
    bases = [doc.parent, root, root/doc.relative_to(root).parts[0]]
    for base in bases:
        candidate = (base/raw).resolve()
        if not candidate.is_relative_to(root.resolve()): continue
        if candidate.exists(): return candidate
        if wiki and not candidate.suffix and candidate.with_suffix('.md').is_file():
            return candidate.with_suffix('.md')
    if wiki:
        matches = file_index(root).get(Path(raw).name, [])
        if not matches and not Path(raw).suffix:
            matches = file_index(root).get(Path(raw).name+'.md', [])
        if len(matches) == 1: return matches[0]
    return None


def publication_text(text, doc, root):
    """Redirect duplicate assets and omit links to private process artifacts."""
    import os
    import urllib.parse
    changes = []
    for start, end, raw, kind, label in references(text):
        target = resolve_reference(raw, doc, root, kind == 'wiki')
        if target is None: continue
        category = excluded(target.relative_to(root))
        if category:
            if kind in {'image', 'wiki', 'link'}:
                replacement = '' if kind == 'image' else label + '（过程产物未发布）'
            else:
                replacement = '' if kind in {'html', 'tex', 'css', 'reference'} else '过程产物未发布'
        else:
            new = preferred(target)
            # Repair source-absolute and root/course-relative Markdown paths as well.
            local_raw = urllib.parse.unquote(raw.split('#')[0]).strip('<>')
            if new == target and (kind not in {'link', 'image', 'html', 'tex', 'reference', 'css'} or (doc.parent/local_raw).exists()):
                continue
            replacement = Path(os.path.relpath(new, doc.parent)).as_posix()
            suffix = ('#'+raw.split('#', 1)[1]) if '#' in raw else ''
            replacement += suffix
            if kind == 'wiki':
                alias = '|'+raw.split('|', 1)[1] if '|' in raw else ''
                replacement = '[['+replacement+alias+']]'
                if text[start:start+1] == '!': replacement = '!'+replacement
            elif kind in {'link', 'image'}:
                replacement = ('!' if kind == 'image' else '')+'['+label+']('+replacement+')'
        changes.append((start, end, replacement))
    for start, end, value in sorted(changes, reverse=True):
        text = text[:start]+value+text[end:]
    return text


def clean_existing(root):
    """Clean only files under the explicitly selected share Git repository."""
    from collections import Counter
    root = root.resolve()
    if not (root/'.git').exists():
        raise ValueError('Cleanup requires an existing share Git repository')
    files = [p for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts]
    removals = {}
    for p in files:
        category = excluded(p.relative_to(root))
        if not category and preferred(p) != p: category = 'svg_duplicates'
        if category: removals[p] = category
    changed = 0
    for p in files:
        if p in removals or p.suffix.lower() not in {'.md', '.html', '.tex', '.css', '.json', '.txt'}: continue
        if p.name == 'export-manifest.json': continue
        original = p.read_text(encoding='utf-8-sig')
        body = publication_text(original, p, root)
        if body != original:
            p.write_text(body, encoding='utf-8', newline='\r\n' if b'\r\n' in p.read_bytes() else '\n'); changed += 1
    for p in removals:
        if not p.resolve().is_relative_to(root): raise ValueError('Path escaped share repository')
        p.unlink()
    file_index.cache_clear()
    return {'deleted': dict(Counter(removals.values())), 'documents_updated': changed}
