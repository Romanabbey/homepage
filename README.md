# 구파발경희한의원 홈페이지

정적 사이트입니다. 모든 페이지는 `build.py`가 생성하고, 생성된 HTML을 그대로 GitHub Pages로 배포합니다.

## 수정 방법
1. 전화번호·진료시간·주소·사업자번호·FAQ·페이지 문구는 **`build.py`** 에서 수정합니다.
   (맨 위 `CLINIC`, `HOURS`, `FAQS` 와 각 `build_*` 함수)
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
- [ ] 확인 필요한 문구 점검: 부종환 엔오, 엔오 리커버리 패치, 성장클리닉 설명은 상세 정보 없이 일반 문구로 작성됨
- [ ] 예약 폼 연결(현재는 접수되지 않고 전화 안내만 표시)
- [ ] 개인정보처리방침 실제 문안으로 교체
- [ ] AI 생성 이미지를 실제 사진으로 교체

## 의료광고 유의
효능 단정, 완치·최고 같은 표현, 다른 의료기관과의 비교, 치료 전후 사진은 쓰지 않습니다.
문구를 고칠 때도 같은 기준을 지켜 주세요.

## 도메인
gupabalhani.org (GitHub Pages, CNAME 파일). DNS A 레코드 185.199.108–111.153.
