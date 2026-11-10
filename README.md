# 구파발경희한의원 홈페이지

정적 사이트입니다. 모든 페이지는 `build.py`가 생성하고, 생성된 HTML을 그대로 GitHub Pages로 배포합니다.

## 수정 방법
1. 전화번호·진료시간·주소·사업자번호·FAQ·페이지 문구는 **`build.py`** 에서 수정합니다.
   (맨 위 `CLINIC`, `HOURS`, `FAQS`, 네이버 예약 주소 `BOOKING` 과 각 `build_*` 함수)
2. 터미널에서 `python3 build.py` 실행 → HTML, sitemap.xml, robots.txt, llms.txt가 다시 만들어집니다.
3. `git add -A && git commit -m "내용" && git push`

진료시간을 바꾸면 `js/main.js`의 `SCHEDULE`(오늘 진료 중 표시)도 함께 맞춰 주세요.

## 로컬 확인
    python3 -m http.server 8000   # http://localhost:8000

## 검색(SEO·AEO·GEO) 구성
- 페이지별 title / description / canonical / Open Graph, sitemap.xml, robots.txt
- 구조화 데이터(JSON-LD): MedicalClinic(요일별 진료시간 포함), Physician, WebSite, BreadcrumbList, FAQPage
- 질문·답변 형식의 FAQ 페이지(faq.html)와 각 진료 페이지의 FAQ
- llms.txt: AI가 읽기 쉬운 사이트 요약. robots.txt에서 주요 AI 크롤러를 허용
- 내용(전화·진료시간 등)을 자바스크립트가 아닌 HTML에 직접 넣어 로봇이 읽을 수 있음

## 공개 후 할 일
- [ ] 네이버 서치어드바이저, 구글 서치콘솔에 https://gupabalhani.org 등록 후 sitemap.xml 제출
- [ ] 네이버 플레이스·카카오맵 등록 (지역 검색 노출에 중요)
- [x] 성장클리닉(RUF 방식) 설명 반영 완료
- [x] 온라인 예약: 네이버 예약으로 연결 완료 (`BOOKING`)
- [x] 개인정보처리방침 작성 완료 (실제 운영과 맞는지 확인, 위탁·CCTV 등이 생기면 갱신)
- [ ] AI 생성 이미지를 실제 사진으로 교체

## 칼럼 쓰는 법 (원장 칼럼)
글은 **마크다운 파일 하나**가 곧 페이지 하나입니다.

1. **초안 작성**: `columns/drafts/` 폴더에 `주제-영문-이름.md` 파일을 만듭니다. 이 폴더는 GitHub에 올라가지 않아 공개되지 않습니다.
2. **미리보기**: `python3 build.py --preview` 실행 → `python3 -m http.server 8000` → 브라우저에서 `http://localhost:8000/preview/column/` 를 엽니다. (공개·색인되지 않음)
3. **공개**: **원장 검수가 끝난 글만** 파일을 `columns/` 로 옮기고 맨 위 `status: draft` 를 `status: published` 로 바꿉니다. 공개된 글은 맨 위에 **날짜만** 표시되고(수정일은 표시하지 않음), 맨 아래 면책 문구 바로 위에 `작성·감수 최솔 원장` 이 표시됩니다. 글 데이터(구조화 데이터)에도 감수자가 들어갑니다. 그래서 **검수 전 글은 절대 공개하지 않습니다.**
4. **올리기**: `python3 build.py` → `git add -A && git commit -m "칼럼: 제목" && git push`
5. 공개되면 홈·`/column/`·사이트맵(`sitemap.xml`)·RSS(`feed.xml`)·`llms.txt` 가 자동으로 갱신됩니다. 공개 후 네이버 서치어드바이저 **요청 → RSS 제출**에 `https://gupabalhani.org/feed.xml` 을 한 번 등록하세요.
6. **네이버 블로그**: 빌드하면 `blog_out/글이름.txt` 에 블로그에 붙여 넣을 본문이 생깁니다. 끝에 원문 링크가 들어 있습니다. (이 폴더도 GitHub에 올라가지 않습니다.)

### 파일 맨 위 (머리말) 예시
```
---
title: 글 제목
date: 2026-11-08
category: growth        # accident, no, diet, growth, postpartum, yakchim, clinic 중 하나
description: 검색 결과에 보일 한두 문장 설명
seo_title: (선택) 검색 결과에 보일 제목. 지역 검색 의도가 있는 글에만 "구파발 …" 형태로 씁니다. 비우면 "글 제목 | 구파발경희한의원 건강칼럼"
summary: 글 맨 위 '핵심 요약' 2~3줄. **굵게** 사용 가능
related: growth.html    # 글 아래 '진료 안내' 버튼이 연결할 페이지
status: draft           # 공개할 때 published
---
```
`seo_title` 예: `구파발 교통사고 한의원, 후유증은 언제까지 치료할까 | 구파발경희한의원` (화면의 글 제목은 `title` 그대로 보입니다. 일반 의학 정보 글에는 쓰지 않는 것을 권합니다.)

본문은 `## 소제목`, `### 작은 소제목`, `- 목록`, `1. 번호목록`, `> 안내 상자`, `**굵게**`, `[글자](주소)` 를 쓸 수 있습니다.
`## 자주 묻는 질문` 아래에 `### 질문?` 과 답변 문단을 쓰면 FAQ(구조화 데이터 포함)로, `## 참고 문헌` 아래 `- 항목` 은 참고 문헌 목록이 됩니다.

### 공개 전 체크리스트 (의료광고·정확성)
- 치료 경험담·후기·전후 사진, "최고·완치·즉시 효과", 다른 병원과의 비교 표현이 없는가
- 수치·기준은 학회 지침이나 논문에서 확인했고 **참고 문헌**에 출처를 달았는가
- 진단·치료를 대신하지 않는다는 안내와, 필요하면 병원 진료를 권하는 문장이 있는가
- 원장이 사실과 표현을 확인했는가 (공개된 글에는 항상 "감수 최솔 원장"이 표시됩니다)
- 권장 빈도: 주 2~3회, 한 편 1,200~2,000자. 양보다 정확성이 우선입니다.

### 네이버 블로그 복사용 페이지
`python3 blog_kit.py blog_out/글이름.txt` → 서식이 입혀진 `글이름-copy.html` 이 열리고, 이미지는 `~/Downloads/블로그이미지/글이름/` 에 복사됩니다. 초안 안의 `{{img:파일.png}}` 가 이미지 위치입니다. 이미지는 브라우저 제한 때문에 직접 업로드해야 합니다.

## 가격 정책
한약·제품 가격은 사이트에 표시하지 않고 "진찰 후 안내"로 둡니다. 비급여 진료비 고지 대상에 한약이 포함되면 별도의 비급여 진료비 안내 페이지가 필요할 수 있으니 확인하세요.

## 의료광고 유의
효능 단정, 완치·최고 같은 표현, 다른 의료기관과의 비교, 치료 전후 사진은 쓰지 않습니다.
문구를 고칠 때도 같은 기준을 지켜 주세요.

## 도메인
gupabalhani.org (GitHub Pages, CNAME 파일). DNS A 레코드 185.199.108–111.153.

## 오늘의 생활 날씨 (생활안내 페이지)
- 매일 한국 시간 아침 7시 무렵 GitHub Actions(`.github/workflows/weather.yml`)가 `scripts/update_weather.py`를 실행해 `data/weather.json`에 하루치(날씨, 기온, 강수확률, 미세먼지, 한 줄 멘트)를 추가하고 생활안내 페이지를 다시 만듭니다.
- 인증키는 저장소 **Settings → Secrets and variables → Actions** 의 `DATA_GO_KR_KEY` 에만 넣습니다. 코드·파일에는 절대 넣지 않습니다.
- 한 줄 멘트는 `data/weather_phrases.json` 의 확정된 문구에서만 고르며, 14일 안에 쓴 문구는 제외합니다. 문구를 바꿀 때는 이 파일을 고칩니다.
- 수동 실행: GitHub → Actions → "오늘의 생활 날씨 갱신" → Run workflow. 로컬 시험: `DATA_GO_KR_KEY=... python3 scripts/update_weather.py`

## 원장 칼럼과 네이버 블로그는 따로 운영합니다
- **원장 칼럼**: 홈페이지에 직접 올리는 글(`columns/*.md`). 대메뉴 '원장 칼럼'과 홈의 원장 칼럼 섹션에만 나옵니다. 분야가 2개 이상이면 목록에 분야 탭이 생깁니다.
- **네이버 블로그 글**: 기존 글은 가져오지 않고, 새로 쓴 글 중 원장님이 고른 글만 `data/blog_posts.json`에 추가합니다. 홈에는 최신 3편, 진료 페이지 하단에는 그 페이지로 지정한 글만 나옵니다. 목록이 비면 섹션이 숨겨집니다.
  - 추가: `python3 scripts/add_blog_post.py <블로그 글 주소> --pages accident,diet`
  - 삭제: `python3 scripts/add_blog_post.py --remove <블로그 글 주소>`
  - 페이지 키: accident, diet, growth, postpartum, yakchim, gongjindan, bopae, anshim, bujong, patch
- **빠른 연결(휴대폰 하단 바·데스크톱 오른쪽)**: `build.py`의 `QUICK_LINKS` 목록 하나로 관리합니다. 유튜브·인스타그램 주소가 생기면 이 목록에 추가하세요.
