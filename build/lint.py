#!/usr/bin/env python3
"""README/asset lint (stdlib only).  python3 build/lint.py"""
import re, sys, glob, os, json
import xml.etree.ElementTree as ET
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.chdir(ROOT)
BASE = json.load(open('src/data/site.json'))['asset_base'].rstrip('/') + '/'
EMOJI = re.compile('[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\U0001D400-\U0001D7FF\u2190-\u21FF\u2B00-\u2BFF]')
errs = []
def err(m): errs.append(m)
texts = ['profile/README.md'] + glob.glob('src/**/*.md', recursive=True) + ['src/data/site.json']
svgs = sorted(glob.glob('profile/assets/**/*.svg', recursive=True))
for f in texts + svgs:
    for n, line in enumerate(open(f, encoding='utf-8'), 1):
        for ch in EMOJI.findall(line): err(f'{f}:{n}: emoji/symbol U+{ord(ch):04X}')
for f in svgs:
    s = open(f, encoding='utf-8').read()
    try: ET.fromstring(s)
    except ET.ParseError as e: err(f'{f}: invalid XML ({e})')
    if re.search(r'<(foreignObject|script)\b', s): err(f'{f}: foreignObject/script not allowed')
    if re.search(r'(?:href|src)="(?!data:|#)[^"]+"|url\((?!#)', s): err(f'{f}: external reference')
    if os.path.getsize(f) > 60_000: err(f'{f}: larger than 60KB')
readme = open('profile/README.md', encoding='utf-8').read()
live = re.sub(r'<!--.*?-->', '', readme, flags=re.S)  # commented-out slots are not checked
for url in set(re.findall(re.escape(BASE) + r'[^"\s)]+', live)):
    if not os.path.exists('profile/assets/' + url[len(BASE):]): err(f'missing asset {url}')
for href in re.findall(r'(?:href|src|srcset)="([^"]*)"', live) + re.findall(r'\]\(([^)]*)\)', live):
    if not href.strip() or href.strip() in ('#', 'https://...'): err(f'empty link "{href}"')
# ---- 접근성 ----
import html as H
DECOR = {'divider-flow', 'divider-circuit', 'divider-pulse'}
for f in svgs:   # 모든 SVG 에 <title>; 의미 있는 SVG 는 role="img" + aria-label, 장식은 aria-hidden
    s = open(f, encoding='utf-8').read(); head = re.search(r'<svg\b[^>]*>', s).group(0)
    name = re.sub(r'-(light|dark)\.svg$', '', os.path.basename(f))
    if '/icons/' in f or name in DECOR:
        if 'aria-hidden="true"' not in head: err(f'{f}: decorative svg needs aria-hidden="true"')
        if name in DECOR: continue
    elif not ('role="img"' in head and re.search(r'aria-label="[^"]+"', head)): err(f'{f}: missing role="img"/aria-label')
    if not re.search(r'<title>[^<]+</title>', s): err(f'{f}: missing or empty <title>')
def norm(t): return re.sub(r'\s+', ' ', H.unescape(t).replace('…', '')).strip()
for m in re.finditer(r'<img\b[^>]*>', live):
    tag = m.group(0); src = re.search(r'src="([^"]*)"', tag).group(1); am = re.search(r'alt="([^"]*)"', tag)
    name = re.sub(r'-(light|dark)\.svg$', '', src.rsplit('/', 1)[-1]) if src.startswith(BASE) else src
    if am is None: err(f'img without alt: {src}'); continue
    alt = norm(am.group(1))
    if not alt and name not in DECOR and '/icons/' not in src: err(f'empty alt on non-decorative image {name}')
    path = 'profile/assets/' + src[len(BASE):] if src.startswith(BASE) else None
    if alt and path and os.path.exists(path):   # SVG 에 보이는 글자는 모두 alt 에 있어야 합니다
        for t in re.findall(r'<text\b[^>]*>(.*?)</text>', open(path, encoding='utf-8').read(), flags=re.S):
            t = norm(re.sub(r'<[^>]+>', '', t))
            if t and t not in alt: err(f'alt of {name} lacks visible text "{t}"')
lv = [int(m.group(1) or len(m.group(2))) for m in re.finditer(r'<h([1-6])\b|^(#{1,6}) ', re.sub(r'(?ms)^```.*?^```', '', live), flags=re.M)]
if lv.count(1) != 1: err(f'expected exactly one h1, found {lv.count(1)}')
for a, b in zip(lv, lv[1:]):
    if b > a + 1: err(f'heading level skipped: h{a} then h{b}')
for t in re.findall(r'<a\b[^>]*>(.*?)</a>', live, flags=re.S):   # 링크 이름이 비지 않도록
    if not norm(re.sub(r'<[^>]+>', '', t)) and 'alt="' not in t: err('link without text or alt')
    if norm(re.sub(r'<[^>]+>', '', t)).lower() in ('here', '여기', 'link', '링크', 'repo'): err(f'non-descriptive link text "{t}"')
if not readme.startswith('<!-- GENERATED FILE'): err('profile/README.md lacks GENERATED header')
for e in errs: print('lint error:', e)
print(f'lint {"FAILED" if errs else "ok"}: {len(svgs)} svgs, {len(texts)} text files, {len(errs)} errors')
sys.exit(1 if errs else 0)
