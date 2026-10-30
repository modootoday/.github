# README 빌드 구조 (모듈화)

## 왜 include 문법을 쓰지 않나
GitHub의 마크다운(GFM)에는 다른 파일을 불러오는 include 문법이 없습니다. 조직 프로필은 저장소에 커밋된 `profile/README.md` 하나를 그대로 보여 줄 뿐이라, 보여 주기 전에 무언가를 실행할 수도 없습니다.
Jekyll `{% include %}`, AsciiDoc `include::`, 서브모듈, iframe은 프로필 README에서 동작하지 않습니다. Actions 없이 할 수 있는 방법(손으로 복사하기, 외부 서버에서 만든 이미지 쓰기)은 마크다운 자체를 합쳐 주지 못합니다.
그래서 **소스를 나눠 관리하고, 빌드로 합친 결과 파일을 커밋하는 방식**을 씁니다. 이 방식이 일반적이고, 합치는 작업은 GitHub Actions가 자동으로 합니다.

## 저장소 구조 (modootoday/.github 기준)
```
modootoday/.github/            ← 저장소 이름이 ".github"
├── .github/workflows/         ← 워크플로는 저장소 안의 .github/workflows/ 에 둡니다 (이름이 겹쳐 보이지만 정상)
│   ├── build-readme.yml
│   └── update-activity.yml
├── profile/
│   ├── README.md              ← 생성 파일. 직접 수정하지 않습니다
│   └── assets/                ← SVG (아이콘은 assets/icons/)
├── src/
│   ├── README.tpl.md          ← 전체 순서 (include 줄 목록)
│   ├── partials/              ← header, intro, services, services-table, other-repos, flow,
│   │                             terminal, activity, maker, contact, packages, footer
│   ├── components/            ← picture(라이트/다크), section-heading, card-link, icon
│   └── data/site.json         ← asset_base, 서비스 10개, 연락처, 패키지 저장소, 나중에 추가할 칸
└── build/
    ├── build.mjs              ← 의존성 없는 Node 렌더러 (--check 지원)
    ├── lint.py                ← 표준 라이브러리만 쓰는 검사
    ├── gen_assets.py          ← SVG 생성 (로컬에서 실행, Pillow 필요)
    ├── source/                ← gen_assets.py 입력: 공식 마크 SVG, 프로필 사진
    └── gen_activity.py        ← 최근 활동 SVG (Actions에서 6시간마다)
```
제안서 폴더에만 있는 `tools/`(미리보기 렌더링·스크린샷)와 `preview-*`는 실제 저장소에 넣지 않습니다.

## 문법
- `{{> partials/이름}}`: 조각을 넣습니다 (`src/partials/이름.md`).
- `{{> components/picture name="hero" alt="..."}}`: 인자를 넘깁니다. `key=변수` 형태도 됩니다.
- `{{ asset_base }}`, `{{ width|100% }}`: 변수입니다. `|` 뒤는 기본값입니다.
- `{{#each services}} … {{ this.name }} … {{/each}}`: 반복합니다. `@index`도 쓸 수 있습니다.
- `{{#if this.repo}} … {{/if}}`: 값이 있을 때만 넣습니다.

빌드가 실패하는 경우: 없는 조각, 없는 변수, 닫히지 않은 블록, 어디서도 쓰지 않는 partial. 쓰지 않는 component는 경고만 합니다.

## 서비스 추가
`src/data/site.json`의 `services`에 항목 하나를 추가하면 카드 그리드와 텍스트 표에 함께 들어갑니다.
카드 SVG는 `build/gen_assets.py`의 `SERV`에 같은 slug를 추가한 뒤 실행해서 만듭니다.

## 섹션 추가
`src/partials/새섹션.md`를 만들고 `src/README.tpl.md`에 `{{> partials/새섹션}}` 한 줄을 넣습니다.

## 로컬 실행
```
python3 build/gen_assets.py      # SVG를 바꿨을 때만
node build/build.mjs             # profile/README.md 생성
node build/build.mjs --check     # 커밋된 결과와 다르면 실패
python3 build/lint.py            # 이모지, SVG 유효성, 외부 참조, 자산 존재, 빈 링크
```

## 접근성 · 대비 검사

- **대체 텍스트**: `build/gen_assets.py` 가 SVG 안에 보이는 글자를 빠짐없이 담은 설명을 `src/data/alts.json` 에 쓰고, 같은 문장을 각 SVG 의 `<title>`·`aria-label` 에 넣습니다. 활동 SVG 는 `gen_activity.py` 가 6시간마다 커밋 목록으로 갱신합니다. `components/picture` 에 `alt` 를 주지 않으면 이미지 이름으로 alts.json 에서 찾아 넣고, 없으면 빌드가 실패합니다. 장식용 구분선만 `alt=""` 로 명시합니다. SVG 의 글자를 바꿨다면 gen_assets.py 의 `ALT` 도 함께 고치세요.
- **lint 접근성 검사** (`build/lint.py`): alt 누락·비어 있음(장식 제외), SVG 의 보이는 글자가 alt 에 빠짐, `<title>`/`role="img"`/`aria-label` 누락, h1 이 정확히 1개가 아님, 제목 단계 건너뜀, 이름 없는 링크.
- **대비 검사** (`python3 build/contrast.py`, 의존성 없음): `profile/assets/*-{light,dark}.svg` 의 글자·아이콘 색을 실제 배경(카드, 그라데이션, 캔버스 #ffffff/#0d1117)과 비교해 WCAG 기준 미만이면 실패합니다. 본문 글자 4.5:1, 큰 글자(24px 이상, 또는 굵게 18.66px 이상) 3:1, 아이콘·의미 있는 선 3:1, 장식선 1.25:1. 애니메이션 투명도는 가장 진한 순간을 기준으로 합니다. `--all` 은 통과한 항목도 보여 줍니다. `--render` (Playwright + Chromium 필요, 로컬 전용) 는 SVG 를 실제로 렌더링해 여러 애니메이션 시점에서 글자 상자 아래 가장 불리한 배경 픽셀(그라데이션·광원·사진 포함)과 비교합니다. 정적 검사로 못 잡는 그라데이션 위 글자를 확인할 때 쓰세요. 두 워크플로 모두 lint 다음에 실행합니다.

## Actions 동작
- **build-readme.yml**
  - main에 push가 들어오고 `src/`, `profile/assets/`, `build/`가 바뀌면 빌드하고 lint를 돌린 뒤, `profile/README.md`만 커밋합니다(`[skip ci]`).
  - 작성자가 github-actions[bot]이거나 커밋 메시지에 `[skip ci]`가 있으면 건너뜁니다. GITHUB_TOKEN으로 한 push는 원래 다른 워크플로를 깨우지 않아서, 반복 실행은 두 겹으로 막혀 있습니다.
  - PR에서는 `--check`와 lint만 하고 커밋하지 않습니다. 기본 권한은 `contents: read`이고, 커밋하는 job만 `write`입니다.
- **update-activity.yml**: 6시간마다 공개 저장소 커밋으로 활동 SVG를 다시 만듭니다. 위 이유로 이 push가 build-readme를 깨우지 못하므로, 같은 job 안에서 빌드와 lint까지 이어서 실행합니다. 커밋 메시지에 섞인 이모지는 생성기가 지웁니다.
- 두 워크플로 모두 수동 실행(`workflow_dispatch`)이 됩니다.
