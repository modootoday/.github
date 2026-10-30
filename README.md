# modootoday/.github

이 저장소는 [github.com/modootoday](https://github.com/modootoday) 조직 프로필의 소스입니다. 방문자가 보는 화면은 이 파일이 아니라 [`profile/README.md`](profile/README.md) 입니다.

완성된 모습은 [조직 프로필](https://github.com/modootoday)에서 바로 볼 수 있습니다.

## 구조

```text
.github/workflows/   빌드 검사와 최근 활동 갱신 워크플로
profile/             생성물. 직접 고치지 않습니다 (README.md, assets/)
src/                 소스. 템플릿, 조각(partials), 컴포넌트, 데이터(site.json)
build/               빌드, 검사, SVG 생성 스크립트
BUILD.md             템플릿 문법과 빌드 구조 설명
```

## 어떻게 고치나

1. 글이나 서비스 목록은 `src/data/site.json` 에서, 문단 구성은 `src/partials/` 에서 고칩니다.
2. 아래 명령으로 빌드하고 검사합니다.
3. `src/` 와 함께 다시 만들어진 `profile/README.md` 도 커밋합니다.
4. main 에 push 하면 `build-readme` 워크플로가 다시 빌드하고 검사합니다. 결과가 달라졌을 때만 `profile/README.md` 를 커밋합니다. PR 에서는 검사만 합니다.

`profile/` 안의 파일은 빌드 결과라서, 직접 고치면 다음 빌드에서 덮어써집니다.

## 명령

빌드 (Node 20, 의존성 없음):

```sh
node build/build.mjs
```

커밋된 결과가 소스와 같은지 확인:

```sh
node build/build.mjs --check
```

검사 (Python 표준 라이브러리만 사용):

```sh
python3 build/lint.py
python3 build/contrast.py
```

SVG 를 바꿀 때만 (Pillow 필요):

```sh
python3 build/gen_assets.py
```

## 최근 활동과 워크플로

최근 활동 카드는 조직 공개 저장소의 최근 커밋을 SVG 로 그린 것입니다. `update-activity` 워크플로가 6시간마다 `build/gen_activity.py` 를 실행해 SVG 와 대체 텍스트를 다시 만들고, 바뀐 부분이 있으면 커밋합니다.

`build-readme` 는 main 에 push 할 때와 PR 에서 돌아갑니다. 두 워크플로 모두 봇이 만든 커밋에는 `[skip ci]` 를 붙여 서로를 다시 부르지 않게 합니다.

## 디자인 규칙

- 이미지는 라이트와 다크 두 벌을 `<picture>` 로 넣습니다.
- 모든 이미지에 대체 텍스트를 붙입니다. 링크 글은 목적지를 알 수 있게 씁니다.
- 제목은 h1 하나, 단계는 건너뛰지 않습니다.
- 글자 대비는 `contrast.py` 기준을 통과해야 합니다.
- SVG 는 외부 리소스를 불러오지 않고, 한 장에 60KB 를 넘지 않습니다.
- 이모지는 쓰지 않고, 차분한 말투로 씁니다.

`lint.py` 가 이 규칙 대부분을 자동으로 확인합니다.

## 주의할 점

- GitHub 는 README 이미지를 캐시합니다. SVG 를 바꿔도 프로필에 바로 보이지 않을 수 있습니다.
- 워크플로가 커밋하려면 Actions 토큰에 쓰기 권한이 있어야 합니다. 조직이나 저장소 설정에서 막혀 있으면 push 단계가 403 으로 실패할 수 있습니다. 현재 설정은 아직 확인하지 않았습니다.

## 더 보기

템플릿 문법과 빌드 구조는 [BUILD.md](BUILD.md) 에 있습니다.

문의: support@modoo.today
