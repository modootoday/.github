# modootoday/.github

모두의오늘(modootoday) GitHub 조직의 프로필 저장소입니다. 방문자가 https://github.com/modootoday 에서 보는 화면은 이 파일이 아니라 `profile/README.md` 입니다.

- `profile/README.md`, `profile/assets/` 는 생성물입니다. 직접 고치지 말고 `src/` 와 `build/` 를 고친 뒤 빌드하세요.
- 빌드: `python3 build/gen_assets.py` (SVG를 바꿀 때만, Pillow 필요) → `node build/build.mjs` → `python3 build/lint.py` → `python3 build/contrast.py`
- 최근 활동 SVG 는 Actions(`update-activity.yml`)가 6시간마다 공개 커밋으로 갱신합니다.

자세한 구조와 문법은 [BUILD.md](BUILD.md) 를 보세요. 문의: support@modoo.today
