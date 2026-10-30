import re,os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','profile','assets'))
import os
_SRC=os.path.join(os.path.dirname(os.path.abspath(__file__)),'source')  # 공식 마크, 프로필 사진(Gravatar)
src=open(os.path.join(_SRC,'modootoday-mark.svg')).read()
HEX,WORD=[re.search(r'd="([^"]+)"',p).group(1) for p in re.findall(r'<path[^>]*/>',src)]
F="Pretendard,'Apple SD Gothic Neo','Noto Sans KR','Malgun Gothic',-apple-system,'Segoe UI',sans-serif"
M="ui-monospace,SFMono-Regular,Menlo,Consolas,'D2Coding',monospace"
T={'light':dict(bg='#F3F4F6',card='#FFFFFF',fg='#1A1A1F',mu='#5B616B',sub='#4A505A',ln='#DDE1E6',p='#d94925',p2='#b94022',grid='#1A1A1F'),
   'dark':dict(bg='#0D1117',card='#161B22',fg='#F0F3F6',mu='#AAB3BD',sub='#D5DBE2',ln='#3D444D',p='#F07450',p2='#d94925',grid='#FFFFFF')}
# 작은 글자용 브랜드색(pt)과 상태 초록(ok): 라이트 #d94925 는 흰 배경에서 4.26:1 이라 본문 크기 글자에는 한 단계 진한 색을 씁니다.
T['light'].update(ln2='#CDD3DA',pt='#b94022',ok='#1a7f37',num='#C9CED6',fw1='#a3381b',fw2='#c4441f')
T['dark'].update(ln2='#3D444D',pt='#F07450',ok='#3FB950',num='#59616B',fw1='#a3381b',fw2='#c4441f')
def _rgb(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]
def _lum(h): return sum(w*(v/12.92 if v<=.03928 else ((v+.055)/1.055)**2.4) for w,v in zip((.2126,.7152,.0722),_rgb(h)))
def _ratio(a,b):
  x,y=sorted((_lum(a),_lum(b)),reverse=True); return (x+.05)/(y+.05)
def lift(col,bg,target=4.6):
  # 다크 테마용: 같은 색조를 유지한 채 흰색 쪽으로 조금씩 섞어 목표 대비에 닿는 가장 어두운 색
  if _ratio(col,bg)>=target: return col
  r=_rgb(col)
  for i in range(1,101):
    t=i/100; h='#'+''.join(f'{round((v+(1-v)*t)*255):02x}' for v in r)
    if _ratio(h,bg)>=target: return h.upper()
  return '#FFFFFF'
RM="@media (prefers-reduced-motion: reduce){*{animation:none!important}}"
def svg(w,h,body,label,c,style=""):
  return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}"><title>{label}</title><style>text{{font-family:{F}}} .m{{font-family:{M}}} {style} {RM}</style>{body}</svg>'
def mark(x,y,s,c,draw=True,word=True,cls="mk"):
  d=f'<svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="48 48 416 416">'
  if draw:
    d+=f'<path d="M256 91 399 173v166l-143 83-143-83V173Z" fill="none" stroke="{c["p"]}" stroke-width="14" stroke-linejoin="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"><animate attributeName="stroke-dashoffset" values="100;0;0" keyTimes="0;.6;1" dur="2.4s" fill="freeze"/></path>'
    d+=f'<path d="{HEX}" fill="{c["p"]}" fill-rule="evenodd" opacity="0"><animate attributeName="opacity" values="0;0;1" keyTimes="0;.6;1" dur="2.4s" fill="freeze"/></path>'
  else: d+=f'<path class="{cls}" d="{HEX}" fill="{c["p"]}" fill-rule="evenodd"/>'
  if word: d+=f'<path d="{WORD}" fill="{c["p"]}" fill-rule="evenodd"/>'
  return d+'</svg>'

ICONS={
'compass':'<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
'rocket':'<path d="M12 15c4-3 6-7 6-11-4 0-8 2-11 6l5 5z"/><path d="M7 10l-3 1 2 3M14 17l-1 3-3-2"/><circle cx="14" cy="9" r="1.5"/>',
'pen':'<path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M14 6l3 3"/>',
'building':'<path d="M4 21V5l8-2v18M12 9l8 2v10M3 21h18M7 8h2M7 12h2M7 16h2M15 14h2M15 17h2"/>',
'tools':'<path d="M14 7a4 4 0 0 0 5 5l-8 8-3-3 8-8a4 4 0 0 1-2-2z"/><path d="M4 4l5 5"/>',
'chart':'<path d="M4 20V4M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
'user':'<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/>',
'mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
'brain':'<path d="M12 5a3 3 0 0 0-6 1 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 6 1zM12 5a3 3 0 0 1 6 1 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-6 1z"/>',
'film':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M7 5v14M17 5v14M3 9h4M3 15h4M17 9h4M17 15h4"/>',
'loop':'<path d="M20 12a8 8 0 0 1-14 5M4 12a8 8 0 0 1 14-5"/><path d="M18 3v4h-4M6 21v-4h4"/>',
'sprout':'<path d="M12 21v-9M12 12c0-4-3-6-7-6 0 4 3 6 7 6zM12 14c0-4 3-6 7-6 0 4-3 6-7 6z"/>',
'link':'<path d="M10 14a4 4 0 0 0 6 0l3-3a4 4 0 0 0-6-6l-1 1M14 10a4 4 0 0 0-6 0l-3 3a4 4 0 0 0 6 6l1-1"/>',
'handshake':'<path d="M3 11l4-4 5 2 5-2 4 4-8 8z"/><path d="M8 13l2 2M11 12l2 2"/>',
'github':'<path d="M9 19c-4 1-4-2-6-2M15 21v-3.5a3 3 0 0 0-1-2.5c3 0 6-1.5 6-6a4.5 4.5 0 0 0-1-3 4 4 0 0 0-.1-3S17.8 2.6 15 4.5a12 12 0 0 0-6 0C6.2 2.6 5.1 3 5.1 3a4 4 0 0 0-.1 3 4.5 4.5 0 0 0-1 3c0 4.5 3 6 6 6a3 3 0 0 0-1 2.5V21"/>',
'x':'<path d="M4 4h4.5L20 20h-4.5z"/><path d="M19.5 4l-6.6 7.4M4.5 20l6.6-7.4"/>',
'wave':'<path d="M7 11V6a1.5 1.5 0 0 1 3 0v4M10 10V4.5a1.5 1.5 0 0 1 3 0V10M13 10V5.5a1.5 1.5 0 0 1 3 0V12M16 9a1.5 1.5 0 0 1 3 0v4a8 8 0 0 1-8 8 6 6 0 0 1-5-3l-2-4a1.5 1.5 0 0 1 2.5-1.5L7 14"/>',
'pin':'<path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
'grid':'<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
'activity':'<path d="M3 12h4l3-7 4 14 3-7h4"/>',
'npm':'<rect x="3.5" y="3.5" width="17" height="17" rx="2"/><path d="M8 16.5V8h8v8.5M12 11v5.5"/>',
'crate':'<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
'gem':'<path d="M7 4h10l4 5-9 11L3 9z"/><path d="M3 9h18M9 4l3 16M15 4l-3 16"/>',
'news':'<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
}
def ico(n,x,y,s,col,anim=False):
  a='<animate attributeName="opacity" values="1;.45;1" dur="3s" repeatCount="indefinite"/>' if anim else ''
  return f'<svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="0 0 24 24"><g fill="none" stroke="{col}" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{ICONS[n]}{a}</g></svg>'
def arrow(x,y,col):  # drawn right arrow, baseline-aligned, 14px
  return f'<path d="M{x} {y-5}h11M{x+7} {y-9}l4 4-4 4" fill="none" stroke="{col}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
os.makedirs('icons',exist_ok=True)
for k,c in T.items():
  for n in ICONS:
    open(f'icons/{n}-{k}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><title>{n} 아이콘</title><style>@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}</style><g fill="none" stroke="{c["p"]}" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{ICONS[n]}</g></svg>')
def W(n,s): open(n,'w').write(s)

SERV=[("modoo","모두의오늘","modoo.today","창작자","브랜드 콘텐츠를 운영하는 통합 AI OS","Write · Card · Motion · Voice · Market","#b94022","시작하기"),
 ("biz","모두의오늘 비즈","biz.modoo.today","사업자 · 대행사","브랜드의 오늘을, 근거가 남는 운영 결과로.","제작 · 검토 · 승인 · 발행 · 고객사별 데이터 분리","#b94022","시작하기"),
 ("ink","Minago Ink","ink.minago.blog","창작자","내 글 1~3편으로 말투를 배우는 AI 대필 작가","Written like you, minutes ago.","#c41265","시작하기"),
 ("kinekino","kinekino","github.com/modootoday/kinekino","창작자","창작자를 위한 AI 영상 플레이어 · 클립 작업대","자막 · 구간 감지 · 클립 · 로컬 모델 · pre-alpha","#5B616B","저장소 보기"),
 ("datalab","데이터랩툴즈 헬퍼","datalab.tools","창작자 · 마케터","보던 화면을 분석 도구로 바꾸는 브라우저 헬퍼","위젯 143개 · AIO 사이드패널 · MCP 브리지","#2463eb","설치하기"),
 ("codex","SOLA Codex","codex.datalab.tools","데이터 · 분석","콘텐츠 품질 점수를 계산하는 방식을 공개한 문서","가이드북 · 분류 체계 · 용어집","#2463eb","읽어보기"),
 ("skills","모두의오늘 스킬","skills.modoo.today","AI 사용자","87개 분야 508개 스킬 중 필요한 것만 읽는 MCP 커넥터","Claude · ChatGPT · Codex","#b94022","연결하기"),
 ("envs","envs","envs.build","개발자 도구","프로젝트의 모든 .env를 암호화된 카탈로그 하나로","$ npx @modootoday/envs init","#803119","시작하기"),
 ("specfold","specfold","specfold.build","개발자 도구","설계·계획 문서를 코드와 함께 움직이게","$ spec check","#5B616B","시작하기"),
 ("pmcp","pmcp","pmcp.build","개발자 도구","AI CLI 밑의 오픈소스 레이어: 스킬 · 공유 설정 · 메일박스","pmcp.toml","#204635","시작하기"),
 ("humanymous","humanymous","humanymous.net","개발자 도구","봇과 사람 요청을 구분하는 리버스 프록시 Gate","Apache-2.0 · 문서","#5B616B","문서 보기"),
 ("meari","Meari","github.com/modootoday/meari","개발자 도구","React·Tailwind 디자인 계약을 쓰는 Rust UI 프레임워크","Rust · Native/Web 빌더 · Apache-2.0 · 개발 중","#5B616B","저장소 보기")]

CONTACTS=[("mail","mail","문의","support@modoo.today"),("github","github","GitHub","@modootoday · @myso-kr"),("x","x","X","x.com/datalab_tools"),("blog","pen","블로그","준비 중"),("news","news","뉴스레터","준비 중"),("npm","npm","npm 패키지","~modootoday"),("crates","crate","crates.io 크레이트","myso-kr"),("rubygems","gem","RubyGems 젬","modootoday")]
import base64,io
from PIL import Image
_b=io.BytesIO();Image.open(os.path.join(_SRC,'gravatar.png')).convert('RGB').resize((192,192),Image.LANCZOS).save(_b,'JPEG',quality=80);AV=base64.b64encode(_b.getvalue()).decode()
for k,c in T.items():
  # HERO
  b=f'''<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['card']}"/><stop offset="1" stop-color="{c['bg']}"/></linearGradient>
<radialGradient id="a1"><stop offset="0" stop-color="{c['p']}" stop-opacity=".45"/><stop offset="1" stop-color="{c['p']}" stop-opacity="0"/></radialGradient>
<radialGradient id="a2"><stop offset="0" stop-color="#f2a07e" stop-opacity=".40"/><stop offset="1" stop-color="#f2a07e" stop-opacity="0"/></radialGradient>
<radialGradient id="a3"><stop offset="0" stop-color="#2463eb" stop-opacity=".18"/><stop offset="1" stop-color="#2463eb" stop-opacity="0"/></radialGradient>
<pattern id="gr" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{c['grid']}" stroke-opacity=".06"/></pattern>
<clipPath id="cl"><rect width="1200" height="360" rx="24"/></clipPath>
<linearGradient id="ul" x1="0" x2="1"><stop offset="0" stop-color="{c['p']}"/><stop offset="1" stop-color="#f2a07e"/></linearGradient></defs>
<g clip-path="url(#cl)"><rect width="1200" height="360" fill="url(#bg)"/>
<circle class="au1" cx="980" cy="80" r="260" fill="url(#a1)"/><circle class="au2" cx="760" cy="320" r="220" fill="url(#a2)"/><circle class="au3" cx="1140" cy="300" r="200" fill="url(#a3)"/>
<rect width="1200" height="360" fill="url(#gr)"/>
<g opacity=".9"><circle cx="0" cy="0" r="4" fill="{c['p']}"><animateMotion dur="9s" repeatCount="indefinite" path="M960 180a150 150 0 1 0 .1 0"/></circle>
<circle r="3" fill="{lift('#2463eb',c['card'],3.8)}"><animateMotion dur="13s" repeatCount="indefinite" path="M960 180a200 120 0 1 1 -.1 0"/></circle>
<circle r="2.5" fill="{c['mu']}"><animateMotion dur="7s" repeatCount="indefinite" path="M960 180a110 110 0 1 0 .1 0"/></circle></g>
<ellipse cx="960" cy="180" rx="150" ry="150" fill="none" stroke="{c['ln2']}" stroke-dasharray="2 8"/><ellipse cx="960" cy="180" rx="200" ry="120" fill="none" stroke="{c['ln2']}" stroke-dasharray="2 8"/>
{mark(870,90,180,c,draw=True,word=True)}
<text x="72" y="88" font-size="15" font-weight="600" fill="{c['pt']}" letter-spacing="2">MODOOTODAY · 1인 기업</text>
<text x="72" y="160" font-size="62" font-weight="800" fill="{c['fg']}">모두의오늘</text>
<rect x="72" y="178" height="6" rx="3" fill="url(#ul)" width="0"><animate attributeName="width" values="0;300" dur="1.6s" begin=".4s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1"/></rect>
<g font-size="24" fill="{c['sub']}">
<text x="72" y="232" opacity="1">브랜드 콘텐츠를 운영하는 통합 AI OS<animate attributeName="opacity" values="1;1;0;0;0;1" keyTimes="0;.318;.333;.985;.985;1" dur="12s" repeatCount="indefinite"/></text>
<text x="72" y="232" opacity="0">콘텐츠 기획·제작·발행과 성과를 한 흐름에서<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;.333;.348;.652;.667;1" dur="12s" repeatCount="indefinite"/></text>
<text x="72" y="232" opacity="0">창작자 서비스부터 개발자 CLI까지, 직접 만듭니다<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.667;.682;.985;1" dur="12s" repeatCount="indefinite"/></text></g>
<g font-size="15" fill="{c['fg']}">
<rect x="72" y="258" width="176" height="44" rx="22" fill="{c['card']}" stroke="{c['ln2']}"/><text x="160" y="285" text-anchor="middle">브랜드 브레인</text>
<rect x="264" y="258" width="176" height="44" rx="22" fill="{c['card']}" stroke="{c['ln2']}"/><text x="352" y="285" text-anchor="middle">통합 스튜디오</text>
<rect x="456" y="258" width="176" height="44" rx="22" fill="{c['card']}" stroke="{c['ln2']}"/><text x="544" y="285" text-anchor="middle">운영 흐름</text></g>
</g><rect x=".5" y=".5" width="1199" height="359" rx="24" fill="none" stroke="{c['ln2']}"/>'''
  st="@keyframes dr{0%,100%{transform:translate(0,0)}50%{transform:translate(-40px,25px)}} .au1{animation:dr 14s ease-in-out infinite} .au2{animation:dr 18s ease-in-out infinite reverse} .au3{animation:dr 22s ease-in-out infinite}"
  W(f'hero-{k}.svg',svg(1200,360,b,"모두의오늘 · 브랜드 콘텐츠를 운영하는 통합 AI OS",c,st))
  # SECTION HEADERS
  for i,(slug,title,sub,ico_) in enumerate([("services","서비스","누구를 위한 도구인지 한눈에","grid"),("flow","이렇게 이어집니다","브랜드 브레인 · 스튜디오 · 발행 · 성과","loop"),("activity","최근 활동","공개 저장소의 최근 커밋","activity"),("maker","만드는 사람","대표 · 개발자 최원","user"),("contact","연락","문의와 링크","mail")],1):
    b=f'''<text x="0" y="58" font-size="44" font-weight="800" fill="{c['num']}">0{i}</text>
<text x="76" y="44" font-size="28" font-weight="800" fill="{c['fg']}">{title}</text><text x="76" y="72" font-size="16" fill="{c['mu']}">{sub}</text>
<rect x="0" y="86" width="120" height="5" rx="2.5" fill="{c['p']}"><animate attributeName="x" values="0;1080;0" dur="10s" repeatCount="indefinite" calcMode="spline" keySplines=".5 0 .5 1;.5 0 .5 1"/></rect>
{ico(ico_,1164,22,36,c['p'],True)}'''
    W(f'sec-{slug}-{k}.svg',svg(1200,96,b,f"{i:02d} {title}",c))
  # DIVIDERS
  b=f'''<path d="M0 20H1200" stroke="{c['ln']}" stroke-width="2"/><path d="M0 20H1200" stroke="{c['p']}" stroke-width="2" stroke-dasharray="6 14"><animate attributeName="stroke-dashoffset" values="0;-200" dur="4s" repeatCount="indefinite"/></path>'''
  W(f'divider-flow-{k}.svg',svg(1200,40,b,"",c))
  b=f'''<path id="tr" d="M0 30H420l20-18h160l20 18H1140" fill="none" stroke="{c['ln']}" stroke-width="2"/>
<circle r="4" fill="{c['p']}"><animateMotion dur="5s" repeatCount="indefinite" path="M0 30H420l20-18h160l20 18H1140"/></circle>
<circle cx="440" cy="12" r="3" fill="{c['ln']}"/><circle cx="600" cy="12" r="3" fill="{c['ln']}"/>{mark(1144,6,48,c,draw=False,word=False,cls="pu")}'''
  W(f'divider-circuit-{k}.svg',svg(1200,60,b,"",c,"@keyframes pu{50%{opacity:.4}} .pu{animation:pu 2.4s ease-in-out infinite}"))
  b=f'''<path d="M0 25 H500 l12-18 14 36 14-36 14 36 12-18 H1200" fill="none" stroke="{c['ln']}" stroke-width="2"/><path d="M0 25 H500 l12-18 14 36 14-36 14 36 12-18 H1200" fill="none" stroke="{c['p']}" stroke-width="2.5" pathLength="100" stroke-dasharray="14 86"><animate attributeName="stroke-dashoffset" values="100;0" dur="3s" repeatCount="indefinite"/></path>'''
  W(f'divider-pulse-{k}.svg',svg(1200,50,b,"",c))
  # STATUS  (canvas 1200x112: 18px transparent margin top/bottom, pill 76px tall, 48px side padding)
  b=f'''<rect x=".5" y="18.5" width="1199" height="75" rx="37.5" fill="{c['card']}" stroke="{c['ln']}"/>
<circle cx="56" cy="56" r="6" fill="{c['ok']}"/><circle cx="56" cy="56" r="6" fill="none" stroke="{c['ok']}" stroke-width="2"><animate attributeName="r" values="6;16" dur="1.8s" repeatCount="indefinite"/><animate attributeName="opacity" values=".9;0" dur="1.8s" repeatCount="indefinite"/></circle>
<text x="84" y="62" font-size="17" font-weight="700" fill="{c['fg']}">모든 프로젝트는 계속 발전 중</text>
<path d="M340 44V68" stroke="{c['ln']}" stroke-width="1.5"/>
<text x="364" y="62" font-size="15" fill="{c['mu']}">서비스·도구 12개 · 공개 저장소 다수 · 1인 기업이 직접 만들고 운영합니다</text>
<text x="1152" y="62" text-anchor="end" font-size="15" fill="{c['pt']}" font-weight="600">support@modoo.today</text>'''
  W(f'status-{k}.svg',svg(1200,112,b,"모든 프로젝트는 계속 발전 중",c))
  # CARDS
  for slug,name,dom,aud,one,meta,col,cta in SERV:
    if k=='dark': col=lift(col,c['card'])
    cli=meta.startswith("$") or meta.endswith(".toml")
    typed=f'''<rect x="28" y="140" width="300" height="34" rx="8" fill="{'#0D1117' if k=='light' else '#010409'}"/><clipPath id="tc"><rect x="40" y="140" height="34" width="0"><animate attributeName="width" values="280;280;0;280;280" keyTimes="0;.5;.55;.85;1" dur="6s" repeatCount="indefinite"/></rect></clipPath>
<text class="m" x="40" y="162" font-size="14" fill="#E6EDF3" clip-path="url(#tc)">{meta}</text>''' if cli else f'<text x="28" y="162" font-size="14" fill="{c["mu"]}">{meta}</text>'
    spark=f'<polyline points="380,166 400,158 420,162 440,148 460,152 480,140 500,144 520,132" fill="none" stroke="{col}" stroke-width="2.5" stroke-linecap="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"><animate attributeName="stroke-dashoffset" values="100;0;0" keyTimes="0;.5;1" dur="5s" repeatCount="indefinite"/></polyline>' if slug in("datalab","codex","biz") else ""
    b=f'''<defs><linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="{col}" stop-opacity="0"/><stop offset=".5" stop-color="{col}" stop-opacity=".9"/><stop offset="1" stop-color="{col}" stop-opacity="0"/><animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="4s" repeatCount="indefinite"/></linearGradient></defs>
<g><rect x="1" y="1" width="578" height="206" rx="18" fill="{c['card']}" stroke="{c['ln']}"/>
<rect x="1" y="1" width="578" height="206" rx="18" fill="none" stroke="url(#sh)" stroke-width="2"/>
<rect x="28" y="28" width="10" height="10" rx="3" fill="{col}"/><text x="46" y="38" font-size="13" font-weight="600" fill="{c['mu']}">{aud}</text>
<circle cx="548" cy="34" r="5" fill="{c['ok']}"><animate attributeName="opacity" values="1;.25;1" dur="2.2s" repeatCount="indefinite"/></circle>
<text x="28" y="78" font-size="26" font-weight="800" fill="{c['fg']}">{name}</text>
<text x="28" y="110" font-size="16" fill="{c['fg']}" opacity=".85">{one}</text>
{typed}{spark}
<text x="530" y="190" text-anchor="end" font-size="14" font-weight="700" fill="{col}">{cta}</text>{arrow(538,190,col)}
<text x="28" y="190" class="m" font-size="12" fill="{c['mu']}">{dom}</text></g>'''
    W(f'card-{slug}-{k}.svg',svg(580,210,b,f"{name} – {one}",c,"@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-2px)}} .fl{animation:fl 6s ease-in-out infinite}"))
  # FLOW DIAGRAM
  nodes=[("브랜드 브레인","브랜드 정보를 축적",150),("통합 스튜디오","글과 영상을 기획·제작",450),("발행","채널에 내보내기",750),("성과","다음 콘텐츠에 반영",1050)]
  b=f'<rect x=".5" y=".5" width="1199" height="279" rx="20" fill="{c["card"]}" stroke="{c["ln"]}"/>'
  for i in range(3):
    x1=nodes[i][2]+100;x2=nodes[i+1][2]-100
    b+=f'<path d="M{x1} 120H{x2}" stroke="{c["ln"]}" stroke-width="2"/><path d="M{x1} 120H{x2}" stroke="{c["p"]}" stroke-width="2" stroke-dasharray="4 10"><animate attributeName="stroke-dashoffset" values="0;-28" dur="1s" repeatCount="indefinite"/></path><path d="M{x2-8} 114l8 6-8 6" fill="none" stroke="{c["p"]}" stroke-width="2"/>'
  loop="M1050 165 C1050 250 150 250 150 165"
  b+=f'<path d="{loop}" fill="none" stroke="{c["ln"]}" stroke-width="2" stroke-dasharray="3 7"/><circle r="5" fill="{c["p"]}"><animateMotion dur="5s" repeatCount="indefinite" path="{loop}"/></circle><text x="600" y="262" text-anchor="middle" font-size="14" fill="{c["mu"]}">발행 성과를 다음 콘텐츠에 반영하는 운영 흐름</text>'
  for j,(t,s,x) in enumerate(nodes):
    b+=f'<rect x="{x-100}" y="75" width="200" height="90" rx="16" fill="{c["bg"]}" stroke="{c["p"] if j==0 else c["ln"]}" stroke-width="{2 if j==0 else 1}"><animate attributeName="stroke" values="{c["ln"]};{c["p"]};{c["ln"]}" dur="4s" begin="{j}s" repeatCount="indefinite"/></rect><text x="{x}" y="113" text-anchor="middle" font-size="19" font-weight="800" fill="{c["fg"]}">{t}</text><text x="{x}" y="140" text-anchor="middle" font-size="14" fill="{c["mu"]}">{s}</text>'
  b+=f'<text x="40" y="44" font-size="14" font-weight="700" fill="{c["pt"]}" letter-spacing="1">모두의오늘 · 운영 흐름</text>'
  W(f'flow-{k}.svg',svg(1200,280,b,"브랜드 브레인, 통합 스튜디오, 발행, 성과 반영",c))
  # TERMINAL
  lines=[("$ npx @modootoday/envs init","#E6EDF3"),("# 프로젝트의 .env 값을 암호화된 카탈로그로","#7D8590"),("$ spec check","#E6EDF3"),("# 프로젝트 문서를 규칙에 맞춰 검사합니다","#7D8590")]
  b=f'<rect width="1200" height="250" rx="16" fill="#0D1117" stroke="{c["ln"]}"/><circle cx="28" cy="26" r="6" fill="#ff5f57"/><circle cx="48" cy="26" r="6" fill="#febc2e"/><circle cx="68" cy="26" r="6" fill="#28c840"/><text x="600" y="31" text-anchor="middle" font-size="13" fill="#7D8590">modootoday — 개발자 도구</text>'
  for i,(t,col) in enumerate(lines):
    y=88+i*42;st=i*1.6
    b+=f'<clipPath id="l{i}"><rect x="36" y="{y-24}" height="34" width="0"><animate attributeName="width" values="900;0;0;900;900" keyTimes="0;.02;{.02+st/10:.2f};{.02+(st+1.4)/10:.2f};1" dur="10s" repeatCount="indefinite"/></rect></clipPath><text class="m" x="40" y="{y}" font-size="19" fill="{col}" clip-path="url(#l{i})">{t}</text>'
  b+='<rect x="40" y="236" width="0" height="0"/><rect class="cu" x="40" y="224" width="11" height="4" fill="#EE6A45"/>'
  W(f'terminal-{k}.svg',svg(1200,250,b,"터미널: npx @modootoday/envs init, spec check",c,"@keyframes bl{50%{opacity:0}} .cu{animation:bl 1s step-end infinite}"))
  # MAKER
  b=f'''<rect x=".5" y=".5" width="1199" height="219" rx="20" fill="{c['card']}" stroke="{c['ln']}"/>
<circle cx="120" cy="110" r="62" fill="{c['bg']}" stroke="{c['p']}" stroke-width="3" stroke-dasharray="6 6"><animateTransform attributeName="transform" type="rotate" values="0 120 110;360 120 110" dur="30s" repeatCount="indefinite"/></circle>
<clipPath id="av"><circle cx="120" cy="110" r="54"/></clipPath><image href="data:image/jpeg;base64,{AV}" x="66" y="56" width="108" height="108" clip-path="url(#av)"/>
<text x="220" y="82" font-size="30" font-weight="800" fill="{c['fg']}">최원</text><text x="300" y="82" font-size="17" fill="{c['mu']}">모두의오늘 대표 · 개발자 · @myso-kr</text>
<text x="220" y="118" font-size="17" fill="{c['fg']}">기획부터 개발, 출시와 운영까지 혼자 맡는 1인 기업입니다.</text>
<text x="220" y="146" font-size="17" fill="{c['fg']}">창작자 서비스, 사업자용 플랫폼, 개발자 CLI를 함께 만듭니다.</text>
<g font-size="14" fill="{c['mu']}"><rect x="220" y="164" width="104" height="30" rx="15" fill="{c['bg']}"/><text x="272" y="184" text-anchor="middle">TypeScript</text>
<rect x="332" y="164" width="70" height="30" rx="15" fill="{c['bg']}"/><text x="367" y="184" text-anchor="middle">Rust</text>
<rect x="410" y="164" width="60" height="30" rx="15" fill="{c['bg']}"/><text x="440" y="184" text-anchor="middle">Go</text></g>'''
  W(f'maker-{k}.svg',svg(1200,220,b,"최원 · 모두의오늘 대표 · 개발자",c))
  for slug,n,lab,val in CONTACTS:
    b=f'''<rect x="1" y="1" width="378" height="86" rx="16" fill="{c['card']}" stroke="{c['ln']}"/><rect x="22" y="22" width="44" height="44" rx="12" fill="{c['bg']}"/>{ico(n,32,32,24,c['p'],slug=="mail")}
<text x="84" y="40" font-size="13" font-weight="600" fill="{c['mu']}">{lab}</text><text x="84" y="64" font-size="17" font-weight="700" fill="{c['fg']}">{val}</text>{arrow(346,52,c['mu'])}'''
    W(f'contact-{slug}-{k}.svg',svg(380,88,b,f"{lab} {val}",c))
  # FOOTER
  b=f'''<defs><linearGradient id="fw" x1="0" x2="1"><stop offset="0" stop-color="{c['fw1']}"/><stop offset="1" stop-color="{c['fw2']}"/></linearGradient></defs>
<path fill="url(#fw)" opacity=".35"><animate attributeName="d" dur="10s" repeatCount="indefinite" values="M0 110 Q300 60 600 110 T1200 110 V200 H0Z;M0 110 Q300 160 600 110 T1200 110 V200 H0Z;M0 110 Q300 60 600 110 T1200 110 V200 H0Z"/></path>
<path fill="url(#fw)"><animate attributeName="d" dur="7s" repeatCount="indefinite" values="M0 130 Q300 170 600 130 T1200 130 V200 H0Z;M0 130 Q300 90 600 130 T1200 130 V200 H0Z;M0 130 Q300 170 600 130 T1200 130 V200 H0Z"/></path>
{mark(566,20,68,c,draw=False,word=True,cls="pu")}
<text x="600" y="182" text-anchor="middle" font-size="16" font-weight="700" fill="#FFFFFF" data-bg="{c['fw1']},{c['fw2']}">support@modoo.today · © 모두의오늘</text>'''
  W(f'footer-{k}.svg',svg(1200,200,b,"모두의오늘 · support@modoo.today",c,"@keyframes pu{50%{opacity:.55}} .pu{animation:pu 3s ease-in-out infinite}"))

# ---- 대체 텍스트: SVG 안에 보이는 글자를 빠짐없이 담습니다 (README alt, SVG <title>/aria-label 공통) ----
import json,html as _h
DEST={"mail":"메일 보내기","github":"GitHub 조직 페이지","x":"X 프로필","blog":"블로그","news":"뉴스레터","npm":"npmjs.com 프로필","crates":"crates.io 프로필","rubygems":"rubygems.org 프로필"}
ALT={
 "hero":"모두의오늘 (MODOOTODAY · 1인 기업). 브랜드 콘텐츠를 운영하는 통합 AI OS. 콘텐츠 기획·제작·발행과 성과를 한 흐름에서. 창작자 서비스부터 개발자 CLI까지, 직접 만듭니다. 핵심 기능: 브랜드 브레인, 통합 스튜디오, 운영 흐름. 누르면 modoo.today로 이동",
 "status":"모든 프로젝트는 계속 발전 중. 서비스·도구 12개 · 공개 저장소 다수 · 1인 기업이 직접 만들고 운영합니다. 문의 support@modoo.today",
 "flow":"모두의오늘 · 운영 흐름 다이어그램. 1단계 브랜드 브레인: 브랜드 정보를 축적. 2단계 통합 스튜디오: 글과 영상을 기획·제작. 3단계 발행: 채널에 내보내기. 4단계 성과: 다음 콘텐츠에 반영. 발행 성과를 다음 콘텐츠에 반영하는 운영 흐름으로 다시 1단계에 이어집니다",
 "terminal":"터미널 사용 예 (modootoday — 개발자 도구). $ npx @modootoday/envs init — # 프로젝트의 .env 값을 암호화된 카탈로그로. $ spec check — # 프로젝트 문서를 규칙에 맞춰 검사합니다",
 "maker":"만드는 사람 최원. 모두의오늘 대표 · 개발자 · @myso-kr. 기획부터 개발, 출시와 운영까지 혼자 맡는 1인 기업입니다. 창작자 서비스, 사업자용 플랫폼, 개발자 CLI를 함께 만듭니다. 기술 스택: TypeScript, Rust, Go. 누르면 GitHub @myso-kr 프로필로 이동",
 "footer":"모두의오늘 마크. support@modoo.today · © 모두의오늘",
}
for i,(slug,title,sub) in enumerate([("services","서비스","누구를 위한 도구인지 한눈에"),("flow","이렇게 이어집니다","브랜드 브레인 · 스튜디오 · 발행 · 성과"),("activity","최근 활동","공개 저장소의 최근 커밋"),("maker","만드는 사람","대표 · 개발자 최원"),("contact","연락","문의와 링크")],1):
  ALT[f"sec-{slug}"]=f"0{i} {title} – {sub}"
for slug,name,dom,aud,one,meta,col,cta in SERV:
  ALT[f"card-{slug}"]=f"{name} (대상: {aud}) – {one}. {meta}. {cta}: {dom}"
for slug,n,lab,val in CONTACTS:
  ALT[f"contact-{slug}"]=f"{lab}: {val} ({DEST[slug]})"
for n in ("divider-flow","divider-circuit","divider-pulse"): ALT[n]=""   # 장식: README 에서 alt=""
for name,a in ALT.items():
  for k in T:
    f=f'{name}-{k}.svg'
    if not os.path.exists(f) or not a: continue
    t=open(f).read(); e=_h.escape(a,quote=True)
    t=re.sub(r'aria-label="[^"]*"',f'aria-label="{e}"',t,count=1); t=re.sub(r'<title>.*?</title>',f'<title>{e}</title>',t,count=1,flags=re.S)
    open(f,'w').write(t)
# 장식용 SVG 는 스크린리더에서 숨김
for n in ("divider-flow","divider-circuit","divider-pulse"):
  for k in T:
    f=f'{n}-{k}.svg'; t=open(f).read().replace('role="img" aria-label=""','aria-hidden="true"'); open(f,'w').write(t)
AP=os.path.join('..','..','src','data','alts.json')
old=json.load(open(AP)) if os.path.exists(AP) else {}
old.update(ALT); json.dump(dict(sorted(old.items())),open(AP,'w'),ensure_ascii=False,indent=2)
print(len(os.listdir('.')))
