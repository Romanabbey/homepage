# 구파발경희한의원 홈페이지

빌드 없이 동작하는 정적 사이트입니다. 폴더 전체를 업로드하면 배포됩니다.

## 로컬 확인
    python3 -m http.server 8000   # http://localhost:8000

## 공개 전 체크리스트
- [ ] js/config.js: 전화번호, 사업자번호, 진료시간, SNS 링크
- [ ] about.html: 원장 약력·사진, 내부 사진
- [ ] hours-location.html: 교통·주차 안내
- [ ] privacy.html: 실제 개인정보처리방침
- [ ] notice.html: 예시 글 교체
- [ ] 각 페이지에서 "[수정 필요]" 검색 후 모두 처리
- [ ] 예약 폼 연결(네이버 예약 또는 Formspree 등)

## 배포 방법 (무료)
### Netlify (가장 쉬움)
1. https://app.netlify.com/drop 접속
2. 이 폴더(gupabal-kyunghee)를 화면에 끌어다 놓기
3. 발급된 주소 확인 → Domain settings에서 구매한 도메인 연결

### GitHub Pages
1. GitHub 저장소 생성 후 이 폴더 내용을 올리기
2. Settings → Pages → Branch: main / root 선택

## 도메인
.kr/.com 도메인은 가비아·후이즈 등에서 구매 후 호스팅 서비스의 DNS 안내에 따라 연결합니다.
도메인: gupabalhani.org (canonical, og:url, sitemap.xml, robots.txt 설정 완료).

## 네이버/구글 검색 등록
- 네이버 서치어드바이저, 구글 서치콘솔에 사이트 등록
- 네이버 플레이스·카카오맵에 한의원 등록(지역 검색 노출에 중요)

## 도메인 연결 (gupabalhani.org)
- Netlify: Domain management → Add domain → gupabalhani.org. 안내되는 DNS 레코드(A/CNAME 또는 네임서버)를 구매처 DNS 설정에 입력
- 반영까지 수 분~48시간, HTTPS 인증서는 자동 발급
- 연결 후 서치어드바이저/서치콘솔에 https://gupabalhani.org/sitemap.xml 제출
