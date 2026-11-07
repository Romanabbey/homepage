#!/usr/bin/env python3
"""구파발경희한의원 사이트 생성기.
사용법: python3 build.py   (이 폴더에 HTML, sitemap.xml, robots.txt, llms.txt 생성)
정보(전화/시간/주소)는 아래 CLINIC 한 곳에서만 수정하세요."""
import json, html, datetime, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://gupabalhani.org"
TODAY = datetime.date.today().isoformat()

CLINIC = dict(
    name="구파발경희한의원",
    doctor="최솔",
    address="서울 은평구 진관4로 47, 은평뉴타운 상림마을 708동 상가 115호",
    street="진관4로 47, 은평뉴타운 상림마을 708동 상가 115호",
    phone="02-355-4517",
    phone_intl="+82-2-355-4517",
    biz="218-90-15783",
    naver="https://map.naver.com/p/entry/place/13116400",   # 네이버지도: 구파발경희한의원 장소
    kakao="https://place.map.kakao.com/1052835355",          # 카카오맵: 구파발경희한의원 장소
)
TEL = "tel:" + CLINIC["phone"].replace("-", "")
BOOKING = "https://booking.naver.com/booking/13/bizes/1548936"  # 네이버 예약
EXT = 'target="_blank" rel="noopener"'

# (표시용 요일, 시간, 비고)
HOURS = [
    ("월 · 화 · 수 · 금", "09:30 – 20:00", "점심시간 12:30 – 14:00"),
    ("목", "14:00 – 20:00", "오후 진료"),
    ("토", "09:30 – 13:00", "점심시간 없음"),
    ("일 · 공휴일", "휴진", ""),
]

DISCLAIMER = "치료 효과와 경과는 개인에 따라 다를 수 있습니다. 이 페이지는 일반적인 안내이며, 실제 치료는 진찰 후 개인별로 안내드립니다."

NAV = [
    ("처방", "#", [
        ("보폐고 엔오", "bopae.html"),
        ("안심환 엔오", "anshim.html"),
        ("부종환 엔오", "bujong.html"),
        ("활력 · 해울 공진단", "gongjindan.html"),
    ]),
    ("진료", "#", [
        ("저칼로리 다이어트", "diet.html"),
        ("성장클리닉", "growth.html"),
        ("교통사고 후유증", "accident.html"),
        ("N약침 · 초음파 가이드 약침", "yakchim.html"),
        ("엔오 리커버리 패치", "patch.html"),
    ]),
    ("원장소개", "about.html", []),
    ("진료안내", "hours-location.html", [
        ("진료시간 · 오시는 길", "hours-location.html"),
        ("예약 · 문의", "reservation.html"),
        ("자주 묻는 질문", "faq.html"),
    ]),
]

ICON_PATHS = {
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/>',
    "cal": '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "pin": '<path d="M12 21s7-6.2 7-11.5A7 7 0 005 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "ext": '<path d="M7 17L17 7M9 7h8v8"/>',
}


def ico(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON_PATHS[name]}</svg>'


EMBLEMS = {
    "bopae": '<path d="M8 22h30a8 8 0 10-8-8"/><path d="M8 33h40a8 8 0 11-8 8"/><path d="M8 44h20"/>',
    "anshim": '<path d="M42 8a24 24 0 1014 32 19 19 0 01-14-32z"/><circle cx="50" cy="16" r="1.5"/><circle cx="56" cy="26" r="1"/>',
    "bujong": '<path d="M32 6C23 19 14 28 14 39a18 18 0 0036 0C50 28 41 19 32 6z"/><path d="M24 41a8 8 0 008 8"/>',
    "gong": '<circle cx="32" cy="32" r="19"/><circle cx="32" cy="32" r="8"/><path d="M32 4v6M32 54v6M4 32h6M54 32h6"/>',
    "patch": '<rect x="10" y="10" width="44" height="44" rx="16"/><path d="M23 32h18M32 23v18"/>',
}


def emblem(key, cls="emb"):
    return f'<svg class="{cls}" viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{EMBLEMS[key]}</svg>'

# ------------------------------------------------------------------ FAQ
F = {
    "hours": ("진료시간은 어떻게 되나요?",
              "월·화·수·금요일은 09:30~20:00(점심시간 12:30~14:00), 목요일은 14:00~20:00, 토요일은 09:30~13:00(점심시간 없음)입니다. 일요일과 공휴일은 휴진입니다. 휴진 일정이 바뀔 수 있어 방문 전 전화(02-355-4517)로 확인하시면 가장 정확합니다."),
    "where": ("위치와 가는 방법, 주차는 어떻게 되나요?",
              "서울 은평구 진관4로 47, 은평뉴타운 상림마을 708동 상가 115호(708동 상가 1층)에 있으며 지하철 3호선 구파발역 인근입니다. 네이버지도·카카오맵에서 '구파발경희한의원'을 검색하시면 길 안내를 받으실 수 있습니다. 708동 지하주차장에 무료로 주차하실 수 있습니다."),
    "booking": ("예약 없이 방문해도 되나요?",
                "방문은 가능하지만 초음파 가이드 약침이나 초음파 성장 검사는 확인과 준비에 시간이 더 걸려 사전 예약을 권해 드립니다. 네이버 예약 또는 전화 02-355-4517로 문의해 주세요."),
    "diet": ("저칼로리 다이어트는 어떻게 진행되나요?",
             "상담과 진찰로 현재 상태를 확인한 뒤, 저칼로리 식단과 함께 개인별로 구성한 맞춤 한약을 원내에서 직접 달여 드립니다. 진행 중에는 경과를 확인하며 식단과 처방을 조정하고, 이후 유지 관리까지 상담합니다. 건강 상태에 따라 적합하지 않을 수 있어 사전 진찰이 필요합니다."),
    "inhouse": ("'원내에서 직접 달이는 개별 맞춤 한약'은 무슨 뜻인가요?",
                "진찰을 마친 뒤 환자분의 체질과 상태에 맞춰 약재를 구성하고, 한의원 안에서 직접 달여 조제한다는 뜻입니다. 구성과 복용 기간은 진찰 결과에 따라 달라집니다."),
    "nyak": ("N약침(엔오약침)은 무엇인가요?",
             "한약재에서 추출·정제한 약액을 치료 부위에 주입하는 약침 가운데, 산화질소(NO) 관련 성분을 함유한 약침입니다."),
    "nyak_diff": ("N약침은 다른 약침과 무엇이 다른가요?",
                  "N약침은 혈관 확장과 림프 순환에 관여하는 산화질소(NO)를 함유했다는 점이 가장 큰 특징입니다. 어떤 약침이 적합한지는 진찰을 통해 현재 상태에 맞춰 선택합니다."),
    "us": ("초음파 가이드 약침은 일반 약침과 무엇이 다른가요?",
           "초음파 영상으로 치료 부위와 주변 구조물을 실시간으로 확인하면서 시술하는 방식입니다. 위치를 영상으로 확인하며 진행한다는 점이 다르며, 확인 과정에 시간이 조금 더 걸릴 수 있습니다."),
    "yak_pain": ("약침 시술은 많이 아픈가요?",
                 "초음파 검사는 젤을 바르고 프로브를 대는 비침습 검사로 통증이 없습니다. 약침 시술은 통증을 줄이기 위해 인슐린 주사기 수준의 매우 얇은 주사기를 사용하며, 염증이 있는 부위는 뻐근한 느낌이 들 수 있지만 보통 수분 안에 가라앉습니다. 통증에 예민하시면 미리 말씀해 주세요."),
    "yak_freq": ("약침은 얼마나 자주 받아야 하나요?",
                 "증상의 종류와 정도에 따라 다르지만 보통 주 3회 이상을 권해 드립니다. 급성 통증은 초기에 매일 치료하기도 하며, 호전 속도에 맞춰 상담 후 간격을 조절합니다."),
    "growth_us": ("초음파 성장 검사에도 방사선을 쓰나요?",
                  "초음파 검사는 방사선을 사용하지 않습니다. RUF 방식의 성장 검사는 요골, 척골, 대퇴골의 연골과 골화 비율을 분석해 아이의 현재 성장 상태와 예상키를 확인합니다. 예상키는 검사 시점의 상태를 바탕으로 한 추정치이며 성장 결과를 보장하는 것은 아닙니다."),
    "puberty": ("성조숙증은 몇 살부터 의심하나요?",
                "일반적으로 여아는 만 8세 미만에 유방이 발달하기 시작하거나, 남아는 만 9세 미만에 고환이 커지기 시작하면(고환 용적 4mL 이상) 성조숙증을 의심합니다. 대한소아내분비학회 2022 진료지침 등에서 제시하는 일반적인 기준이며, 정확한 진단은 진찰과 뼈 나이·성호르몬 검사 등으로 이루어집니다. 걱정되시면 상담을 받아 보세요."),
    "accident": ("교통사고 후유증 치료는 어떻게 받나요?",
                 "침, 부항, 물리치료, 추나요법, 약침, 맞춤 한약 중 상태에 맞는 치료를 조합해 진행합니다. 자동차보험 접수 방법은 전화로 문의해 주세요. 의식 소실, 극심한 통증, 팔다리 마비 같은 증상이 있으면 먼저 응급실을 방문하셔야 합니다."),
    "zero": ("당뇨가 있는데 보폐고 엔오를 복용해도 되나요?",
             "꿀이 들어가지 않은 제로 버전도 있습니다. 진찰 시 당뇨 여부와 복용 중인 약을 알려 주시면 상태에 맞게 안내해 드립니다."),
    "gong_choose": ("활력공진단과 해울공진단 중 무엇을 선택하나요?",
                    "기본은 활력공진단입니다. 스트레스가 심하고 신경이 예민한 편이라면 활력공진단 대신 해울공진단을 대안으로 고려합니다. 최종 선택은 진찰 후 체질과 상태를 보고 정합니다."),
    "gong_make": ("활력공진단은 어떻게 만드나요?",
                  "녹용, 산수유, 당귀, 구기자, 황기, 향부자, 육계, 백출, 건강, 녹차, 감국, 박하 12가지 약재와 엔오(NO)를 초미세분말로 갈아 꿀로 반죽한 뒤, 5일간 숙성하고 금박을 입혀 완성합니다."),
    "price": ("처방과 제품의 소비자가격은 얼마인가요?",
              "소비자가격 기준으로 보폐고 엔오는 1박스(45포) 170,000원·2박스(90포) 300,000원, 안심환 엔오는 1박스(30포) 99,000원·3박스(90포) 270,000원, 부종환 엔오는 10일 체험분(30포) 60,000원·1개월분(90포) 150,000원, 활력공진단·해울공진단은 1환 15,000원·30환 450,000원, 사향 프리미엄 공진단은 1환(6g) 70,000원, 엔오 리커버리 패치는 1팩(16장) 15,900원입니다. 가격은 변동될 수 있어 방문 전 확인을 권해 드립니다."),
}
FAQS = list(F.values())  # faq.html 전체 목록 (페이지마다 필요한 것만 골라 씁니다)


# ------------------------------------------------------------------ helpers
def esc(s):
    return html.escape(s, quote=True)


def hours_rows():
    return "".join(
        f"<tr><th scope='row'>{d}</th><td>{t}</td><td class='muted'>{n}</td></tr>" for d, t, n in HOURS
    )


def clinic_schema():
    spec = []

    def add(days, o, c):
        spec.append({"@type": "OpeningHoursSpecification", "dayOfWeek": days, "opens": o, "closes": c})

    add(["Monday", "Tuesday", "Wednesday", "Friday"], "09:30", "12:30")
    add(["Monday", "Tuesday", "Wednesday", "Friday"], "14:00", "20:00")
    add(["Thursday"], "14:00", "20:00")
    add(["Saturday"], "09:30", "13:00")
    services = ["저칼로리 다이어트 맞춤 한약", "맞춤 한약", "활력공진단", "해울공진단", "사향 프리미엄 공진단", "N약침(엔오약침)",
                "초음파 가이드 약침", "초음파 성장 검사", "성장 클리닉", "침", "부항", "추나요법", "교통사고 후유증 진료"]
    return {
        "@type": ["MedicalClinic", "LocalBusiness"],
        "@id": DOMAIN + "/#clinic",
        "name": CLINIC["name"],
        "alternateName": "구파발 한의원",
        "url": DOMAIN + "/",
        "image": DOMAIN + "/assets/img/n-og.jpg",
        "telephone": CLINIC["phone_intl"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": CLINIC["street"],
            "addressLocality": "은평구",
            "addressRegion": "서울특별시",
            "addressCountry": "KR",
        },
        "hasMap": [CLINIC["naver"], CLINIC["kakao"]],
        "amenityFeature": {"@type": "LocationFeatureSpecification", "name": "무료 주차 (708동 지하주차장)", "value": True},
        "areaServed": ["서울특별시 은평구", "구파발", "진관동"],
        "openingHoursSpecification": spec,
        "availableService": [{"@type": "MedicalTherapy", "name": s} for s in services],
        "founder": {"@id": DOMAIN + "/#doctor"},
        "medicalSpecialty": "TraditionalChineseMedicine",
        "potentialAction": {"@type": "ReserveAction", "name": "네이버 예약",
                            "target": {"@type": "EntryPoint", "urlTemplate": BOOKING, "actionPlatform": ["http://schema.org/DesktopWebPlatform", "http://schema.org/MobileWebPlatform"]},
                            "result": {"@type": "Reservation", "name": "구파발경희한의원 진료 예약"}},
    }


def doctor_schema():
    return {
        "@type": "Physician",
        "@id": DOMAIN + "/#doctor",
        "name": CLINIC["doctor"],
        "jobTitle": "대표원장 (한의사)",
        "worksFor": {"@id": DOMAIN + "/#clinic"},
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "경희대학교 한의과대학"},
        "image": DOMAIN + "/assets/img/doctor.jpg",
        "url": DOMAIN + "/about.html",
    }


def website_schema():
    return {"@type": "WebSite", "@id": DOMAIN + "/#website", "name": CLINIC["name"], "url": DOMAIN + "/",
            "inLanguage": "ko-KR", "publisher": {"@id": DOMAIN + "/#clinic"}}


def breadcrumb(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + "/" + (u if u else "")}
        for i, (n, u) in enumerate(items)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def header_html(current):
    items = []
    for label, href, subs in NAV:
        is_active = current and (href == current or any(u == current for _, u in subs))
        active = " class='active'" if is_active else ""
        if subs:
            sub = "".join(f"<a href='{u}'>{esc(n)}</a>" for n, u in subs)
            top = f"<a href='{href}'{active}>{esc(label)}</a>" if href != "#" else f"<span class='navbtn'{active} tabindex='0'>{esc(label)}</span>"
            items.append(f"<li class='has-sub'>{top}<div class='sub'>{sub}</div></li>")
        else:
            items.append(f"<li><a href='{href}'{active}>{esc(label)}</a></li>")
    nav = "".join(items)
    return f"""<a class="skip" href="#main">본문 바로가기</a>
<header class="site-header">
  <div class="container nav-wrap">
    <a class="brand" href="index.html" aria-label="{CLINIC['name']} 홈">
      <svg viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="#16211c"/><path d="M12 28c0-9 6-15 17-16 0 10-6 16-15 16" fill="none" stroke="#f6f6f3" stroke-width="2" stroke-linejoin="round"/><path d="M11 29l10-10" stroke="#9fd3b8" stroke-width="2" stroke-linecap="round"/></svg>
      <span><b>{CLINIC['name']}</b><small>은평뉴타운 평생주치의</small></span>
    </a>
    <nav aria-label="주 메뉴" id="mainnav">
      <ul class="gnb">{nav}</ul>
      <div class="nav-cta-m">
        <a class="btn btn-ink" href="{BOOKING}" {EXT}>네이버 예약 {ico('ext')}</a>
        <a class="btn btn-line" href="{TEL}">{ico('phone')} {CLINIC['phone']}</a>
      </div>
    </nav>
    <div class="nav-right">
      <a class="tel" href="{TEL}">{ico('phone')}<span>{CLINIC['phone']}</span></a>
      <a class="btn btn-ink" href="{BOOKING}" {EXT}>네이버 예약</a>
    </div>
    <button class="burger" id="burger" aria-label="메뉴 열기" aria-expanded="false" aria-controls="mainnav"><span></span><span></span></button>
  </div>
</header>"""


def footer_html():
    groups = [
        ("처방", [("보폐고 엔오", "bopae.html"), ("안심환 엔오", "anshim.html"), ("부종환 엔오", "bujong.html"), ("활력·해울 공진단", "gongjindan.html")]),
        ("진료", [("저칼로리 다이어트", "diet.html"), ("성장클리닉", "growth.html"), ("교통사고 후유증", "accident.html"), ("N약침 · 초음파 가이드 약침", "yakchim.html"), ("엔오 리커버리 패치", "patch.html")]),
        ("안내", [("원장소개", "about.html"), ("진료시간 · 오시는 길", "hours-location.html"), ("예약 · 문의", "reservation.html"), ("자주 묻는 질문", "faq.html"), ("개인정보처리방침", "privacy.html")]),
    ]
    cols = "".join(f"<div><h4>{g}</h4>" + "".join(f"<a href='{u}'>{esc(n)}</a>" for n, u in ls) + "</div>" for g, ls in groups)
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="foot-grid">
      <div class="foot-id">
        <p class="foot-brand">{CLINIC['name']}</p>
        <address>
          대표원장 {CLINIC['doctor']} · 사업자등록번호 {CLINIC['biz']}<br>
          {CLINIC['address']}<br>
          TEL <a href="{TEL}">{CLINIC['phone']}</a>
        </address>
        <p class="foot-hours">월·화·수·금 09:30–20:00 (점심 12:30–14:00)<br>목 14:00–20:00 · 토 09:30–13:00 · 일·공휴일 휴진</p>
      </div>
      <nav class="foot-links" aria-label="푸터 메뉴">{cols}</nav>
    </div>
    <p class="foot-note">본 사이트의 내용은 일반적인 건강 정보이며 개인별 진단·치료를 대신하지 않습니다. {DISCLAIMER.split('. ')[0]}. 일부 이미지는 AI로 생성한 예시 이미지이며 실제 한의원 모습과 다를 수 있습니다.</p>
    <p class="foot-note">© {datetime.date.today().year} {CLINIC['name']}. All rights reserved.</p>
  </div>
</footer>
<div class="fab" aria-label="빠른 메뉴">
  <a class="fab-call" href="{TEL}">{ico('phone')} 전화 상담</a>
  <a class="fab-rsv" href="{BOOKING}" {EXT}>{ico('cal')} 네이버 예약</a>
</div>
<button class="to-top" id="toTop" aria-label="맨 위로">{ico('arrow')}</button>
<script src="js/main.js" defer></script>"""


def page(slug, title, desc, body, current=None, schema=None, crumbs=None, og="n-og.jpg", home=False, theme=None, extra_head=""):
    graph = [website_schema(), clinic_schema(), doctor_schema()] if home else [clinic_schema(), doctor_schema()]
    if crumbs:
        graph.append(breadcrumb(crumbs))
    if schema:
        graph += schema
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    url = DOMAIN + "/" + ("" if slug == "index.html" else slug)
    out = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#1d4a3a">
<meta property="og:type" content="website">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="{CLINIC['name']}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/assets/img/{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="css/site.css">
<script type="application/ld+json">{ld}</script>
{extra_head}</head>
<body{(" class='theme-" + theme + "'") if theme else ""}>
{header_html(current)}
<main id="main">
{body}
</main>
{footer_html()}
</body>
</html>
"""
    if slug == "404.html":  # 어떤 경로에서 열려도 깨지지 않도록 절대경로 사용
        out = re.sub(r'(href|src)=(["\'])(?!https?:|tel:|mailto:|#|/)', lambda mm: f"{mm.group(1)}={mm.group(2)}/", out)
    with open(os.path.join(ROOT, slug), "w", encoding="utf-8") as f:
        f.write(out)


def crumb_html(name):
    return f"<nav class='crumb' aria-label='현재 위치'><a href='index.html'>홈</a> <span>›</span> {esc(name)}</nav>"


def hero_sub(name, h1, lead, img, extra=""):
    return f"""<section class="phero">
  <div class="container phero-grid">
    <div>
      {crumb_html(name)}
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <div class="btn-row">
        <a class="btn btn-ink" href="{BOOKING}" {EXT}>네이버 예약 {ico('ext')}</a>
        <a class="btn btn-line" href="{TEL}">{ico('phone')} {CLINIC['phone']}</a>
      </div>
      {extra}
    </div>
    <figure class="phero-img"><img src="assets/img/{img}" alt="" width="1600" height="1244"></figure>
  </div>
</section>"""


def cta_band():
    return f"""<section class="cta-band">
  <div class="container cta-inner">
    <div><h2>궁금한 점은 편하게 문의해 주세요</h2><p>진찰 후 상태에 맞는 방법을 설명드립니다.</p></div>
    <div class="btn-row"><a class="btn btn-light" href="{TEL}">{ico('phone')} {CLINIC['phone']}</a><a class="btn btn-ghost" href="{BOOKING}" {EXT}>네이버 예약</a></div>
  </div>
</section>"""


def faq_block(items, title="자주 묻는 질문"):
    d = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in items)
    return f"""<section class="sec"><div class="container narrow">
  <div class="sec-head"><span class="tag">FAQ</span><h2>{title}</h2></div>
  <div class="faq">{d}</div>
</div></section>"""


def steps(items):
    li = "".join(f"<li><span class='n'>{i+1}</span><div><h3>{esc(t)}</h3><p>{esc(p)}</p></div></li>" for i, (t, p) in enumerate(items))
    return f"<ol class='steps'>{li}</ol>"


def checks(items):
    return "<ul class='checks'>" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def notice(text, title="안내 · 주의사항"):
    return f"<aside class='notice'><b>{title}</b><p>{text}</p></aside>"


def disclaimer():
    return f"<p class='disc'>※ {DISCLAIMER}</p>"


# ------------------------------------------------------------------ pages
def build_home():
    prods = "".join(f"""<a class="lineup t-{k} reveal" href="{pr['slug']}">
  <span class="lu-emb">{emblem(k)}</span>
  <span class="lu-tag">{pr['tag']}</span>
  <h3>{pr['name']}</h3>
  <p>{pr['tagline']}</p>
  <span class="lu-price">소비자가격 {pr['from_txt']}~</span>
  <img src="assets/img/{pr['img']}" alt="" loading="lazy" width="1400" height="1090">
  <span class="lu-go">{ico('arrow')}</span>
</a>""" for k, pr in PRODUCTS.items())
    gong = f"""<a class="lineup t-gong reveal" href="gongjindan.html">
  <span class="lu-emb">{emblem('gong')}</span>
  <span class="lu-tag">공진단</span>
  <h3>활력 · 해울 공진단</h3>
  <p>기운을 뿌리부터 채우는 활력공진단. 예민한 분께는 해울공진단.</p>
  <span class="lu-price">소비자가격 1환 15,000원~</span>
  <img src="assets/img/p-gong.jpg" alt="" loading="lazy" width="1400" height="1090">
  <span class="lu-go">{ico('arrow')}</span>
</a>"""
    services = [
        ("01", "저칼로리 다이어트", "저칼로리 식단과 원내에서 직접 달이는 개별 맞춤 한약", "diet.html", "n-diet.jpg"),
        ("02", "성장클리닉 · 초음파 성장 검사", "요골·척골·대퇴골 연골을 분석하는 초음파 검사, 나이·성별 맞춤 상담", "growth.html", "n-growth2.jpg"),
        ("03", "교통사고 후유증", "침 · 부항 · 물리치료 · 추나 · 약침 · 맞춤 한약", "accident.html", "n-accident.jpg"),
        ("04", "N약침 · 초음파 가이드 약침", "영상으로 위치를 확인하며 진행하는 약침 시술", "yakchim.html", "n-ultrasound.jpg"),
        ("05", "엔오 리커버리 패치", "내원하지 않는 날에도 간편하게 쓰는 패치(공산품)", "patch.html", "p-patch.jpg"),
    ]
    rows = "".join(f"""<a class="srow reveal" href="{h}"><span class="sr-n">{n}</span><span class="sr-t"><b>{esc(ti)}</b><small>{esc(d)}</small></span><img src="assets/img/{im}" alt="" loading="lazy" width="1600" height="1244"><span class="sr-go">{ico('arrow')}</span></a>""" for n, ti, d, h, im in services)
    body = f"""
<section class="hero">
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="kicker"><span class="status" id="openNow">진료시간 확인</span><span class="sep"></span>구파발역 인근 · 은평구 진관4로</p>
      <h1>진찰은 <b>꼼꼼하게</b>.<br>한약은 <b>원내에서 직접</b>.</h1>
      <p class="lead">저칼로리 다이어트, 초음파 가이드 약침, 성장클리닉, 교통사고 후유증 진료를 대표원장 {CLINIC['doctor']}이 직접 살핍니다.</p>
      <div class="btn-row">
        <a class="btn btn-ink btn-lg" href="{BOOKING}" {EXT}>네이버 예약 {ico('ext')}</a>
        <a class="btn btn-line btn-lg" href="{TEL}">{ico('phone')} {CLINIC['phone']}</a>
      </div>
    </div>
    <figure class="hero-img">
      <img src="assets/img/n-hero.jpg" alt="구파발경희한의원 접수 공간 예시 이미지" width="1600" height="914" fetchpriority="high">
      <figcaption class="hero-card">
        <span>{ico('clock')} 진료시간</span>
        <b>월·화·수·금 09:30–20:00</b>
        <small>목 14:00–20:00 · 토 09:30–13:00</small>
      </figcaption>
    </figure>
  </div>
</section>

<section class="facts"><div class="container facts-grid">
  <a href="hours-location.html#map">{ico('pin')}<span><b>오시는 길</b><small>은평구 진관4로 47, 상림마을 708동 상가 115호 · 무료 주차</small></span></a>
  <a href="{TEL}">{ico('phone')}<span><b>전화 상담</b><small>{CLINIC['phone']}</small></span></a>
  <a href="{BOOKING}" {EXT}>{ico('cal')}<span><b>네이버 예약</b><small>초음파 검사·시술은 사전 예약 권장</small></span></a>
</div></section>

<section class="sec" id="products">
  <div class="container">
    <div class="sec-head left"><span class="tag">PRESCRIPTIONS</span><h2>처방</h2><p>각각의 처방은 구성과 복용 방법, 가격이 다릅니다. 진찰 후 상태에 맞는 것을 안내해 드립니다.</p></div>
    <div class="lineups">{prods}{gong}</div>
    {disclaimer()}
  </div>
</section>

<section class="sec sec-tint" id="services">
  <div class="container">
    <div class="sec-head left"><span class="tag">CARE</span><h2>진료</h2></div>
    <div class="srows">{rows}</div>
  </div>
</section>

<section class="sec">
  <div class="container">
    <div class="sec-head left"><span class="tag">PRINCIPLES</span><h2>진료 원칙</h2></div>
    <div class="trio">
      <div class="reveal"><span class="num">01</span><h3>충분히 듣고, 직접 진찰합니다</h3><p>증상뿐 아니라 생활 습관과 걱정까지 듣고, 대표원장이 직접 진찰합니다.</p></div>
      <div class="reveal"><span class="num">02</span><h3>개인별로 구성해 원내에서 달입니다</h3><p>진찰 결과에 맞춰 약재를 구성하고, 한의원 안에서 직접 달여 조제합니다.</p></div>
      <div class="reveal"><span class="num">03</span><h3>영상으로 확인하고 설명드립니다</h3><p>초음파로 부위를 확인하고, 치료 방향과 기간, 관리법을 알기 쉽게 설명드립니다.</p></div>
    </div>
  </div>
</section>

<section class="sec sec-tint">
  <div class="container doc-grid">
    <figure class="doc-photo reveal"><img src="assets/img/doctor.jpg" alt="구파발경희한의원 대표원장 최솔" width="1024" height="1024" loading="lazy"></figure>
    <div class="reveal">
      <span class="tag">DOCTOR</span>
      <h2>대표원장 {CLINIC['doctor']}</h2>
      <p>경희대학교 한의과대학을 졸업하고 횡성군보건소 한방진료과장, 경희대학교 침구경락센터 협력 한의사, 한국한의학연구원 임상연구협력 한의사로 근무했습니다. 초음파 유도하 약침 정규과정을 수료했습니다.</p>
      <ul class="plain"><li>국민건강보험공단 장기요양등급판정위원</li><li>제중학회 학술부회장</li><li>한방비만학회 · 대한스포츠한의학회 회원</li></ul>
      <p><a class="btn btn-line" href="about.html">약력 전체 보기 {ico('arrow')}</a></p>
    </div>
  </div>
</section>

{faq_block([F["hours"], F["where"], F["booking"]])}
<div class="container narrow more-faq"><a class="btn btn-line" href="faq.html">질문 더 보기 {ico('arrow')}</a></div>

<section class="sec sec-tint" id="visit">
  <div class="container">
    <div class="sec-head left"><span class="tag">VISIT</span><h2>진료시간 · 오시는 길</h2></div>
    <div class="info-grid">
      <div class="panel"><h3>진료시간</h3>
        <table class="hours"><tbody>{hours_rows()}</tbody></table></div>
      <div class="panel"><h3>오시는 길</h3>
        <p class="addr">{CLINIC['address']}</p>
        <p class="muted">지하철 3호선 구파발역 인근 · 708동 지하주차장 무료 주차</p>
        <div class="btn-row"><a class="btn btn-naver" href="{CLINIC['naver']}" target="_blank" rel="noopener">네이버지도</a><a class="btn btn-kakao" href="{CLINIC['kakao']}" target="_blank" rel="noopener">카카오맵</a></div>
        <p class="muted">전화 <a href="{TEL}">{CLINIC['phone']}</a></p></div>
    </div>
  </div>
</section>
{cta_band()}
"""
    page("index.html",
         "구파발 한의원 | 구파발경희한의원 – 보폐고·안심환·부종환 엔오, 공진단, 초음파 가이드 약침",
         "서울 은평구 구파발역 인근 구파발경희한의원. 보폐고 엔오·안심환 엔오·부종환 엔오·활력해울공진단 처방, 저칼로리 다이어트, 초음파 가이드 약침, 성장클리닉, 교통사고 후유증 진료. 대표원장 최솔.",
         body, current="index.html", home=True)


def build_diet():
    body = hero_sub("저칼로리 다이어트", "저칼로리 다이어트,<br>개별 맞춤 한약으로 진행합니다",
                    "저칼로리 식단과 함께, 진찰 후 개인별로 구성한 한약을 구파발경희한의원에서 직접 달여 드립니다.", "n-diet.jpg") + f"""
<section class="sec"><div class="container narrow prose">
  <h2>어떤 프로그램인가요?</h2>
  <p>저칼로리 다이어트는 섭취 열량을 줄이는 식단을 기본으로 합니다. 열량을 줄이는 동안 허기와 기운 저하가 부담될 수 있어, 진찰 후 <b>개인별로 약재를 구성한 맞춤 한약</b>을 함께 처방합니다. 한약은 <b>한의원 안에서 직접 달여</b> 조제합니다.</p>
  <h2>진행 순서</h2>
  {steps([
    ("상담 · 진찰", "현재 체중과 체성분, 평소 식습관, 복용 중인 약, 과거 병력을 확인합니다."),
    ("처방 구성", "체질과 상태를 바탕으로 한약 구성을 정하고, 저칼로리 식단 방법을 안내합니다."),
    ("원내 탕전", "구성한 한약을 원내에서 직접 달여 조제합니다."),
    ("경과 확인", "진행 중 컨디션과 체중 변화를 확인하며 식단과 처방을 조정합니다."),
    ("유지 관리", "목표 도달 이후에도 식습관을 유지할 수 있도록 상담합니다."),
  ])}
  <h2>이런 분께 상담을 권합니다</h2>
  {checks(["체중 관리 목표가 있고 식단 조절을 병행할 수 있는 분", "식단을 줄이면 허기와 기운 저하가 걱정되는 분", "이전 체중 관리 후 유지 방법을 고민하시는 분"])}
  {notice("저칼로리 식단은 모든 분께 적합하지 않을 수 있어 사전 진찰이 필요합니다. 임신·수유 중이거나 지병이 있으면 진찰 시 알려 주세요. 감량 폭과 기간은 개인별로 다르며 특정 결과를 약속드리지 않습니다.")}
  {disclaimer()}
</div></section>
{faq_block([F["diet"], F["inhouse"]], "다이어트 관련 질문")}
{cta_band()}"""
    page("diet.html", "저칼로리 다이어트 한약 | 구파발경희한의원 (은평구)",
         "구파발경희한의원의 저칼로리 다이어트. 저칼로리 식단과 원내에서 직접 달이는 개별 맞춤 한약으로 진행합니다. 진료 전 상담 필수.",
         body, current="diet.html", crumbs=[("홈", ""), ("저칼로리 다이어트", "diet.html")],
         schema=[faq_schema([F["diet"], F["inhouse"]])], og="n-diet.jpg")


PRODUCTS = {
    "bopae": dict(
        slug="bopae.html", name="보폐고 엔오", theme="bopae", img="p-bopae.jpg", tag="호흡기 · 목",
        tagline="숨 쉬는 일상을 위한 처방",
        lead="호흡기와 목의 불편감을 관리하기 위한 한약 처방입니다. 영양제처럼 꾸준히 복용하는 방식으로 상담합니다.",
        extra="엔오(NO)는 처방의 작용을 보조하는 역할로 구성했습니다.",
        facts=["1박스 45포", "하루 3회 기준 15일분", "꿀 없는 제로 버전도 있음"],
        herbs=["길경", "대청엽", "우방자", "금은화", "연교", "죽엽", "포공영", "박하", "오미자", "사삼", "맥문동", "유근피", "산약", "감초", "건강"],
        herbnote="길경 등은 가래와 염증 관리, 오미자·사삼·맥문동은 기침 관리, 유근피·산약은 소화 부담을 줄이는 데, 감초·건강은 처방의 조화를 위해 구성했습니다.",
        targets=["만성적인 코막힘, 후비루, 축농증 등 코 불편", "기침과 가래가 오래 가는 경우", "목이 칼칼하거나 쉰 목소리, 인후 불편이 잦은 경우", "말을 많이 하는 직업(교사, 강사, 가수 등)으로 목 관리가 필요한 경우", "흡연으로 목이 답답하고 가래가 끼는 느낌이 있는 경우"],
        how=["1포씩, 하루 3회를 기본으로 합니다(1박스 45포 = 15일분).", "증상이 있을 때는 하루 3회, 증상이 심할 때는 하루 3~5회, 증상이 없는 관리 목적이라면 하루 1회로 조절합니다.", "코 증상처럼 오래된 불편은 한 달 이상 꾸준히 복용하며 경과를 살피는 경우가 많습니다."],
        cautions="위염·식도염이 있어 공복에 속쓰림이 나타나면 식후 복용을 상담하세요. 박하(멘톨)에 알레르기가 있으면 복용을 중단하고 알려 주세요. 당뇨 등으로 당 섭취를 조절 중이시면 진찰 시 꼭 알려 주세요. 소아는 연령과 상태에 따라 용량이 달라 진찰 후 안내합니다.",
        variant=("보폐고 엔오 제로", "꿀이 들어가지 않은 제로 버전도 있습니다. 당뇨 등으로 당 섭취가 걱정되시면 진찰 시 알려 주세요."),
        desc="호흡기와 목의 불편감을 관리하기 위한 한약 처방",
        packs=[("1박스 (45포 · 하루 3회 기준 15일분)", 170000), ("2박스 (90포 · 한 달분)", 300000)],
        from_txt="1박스 170,000원"),
    "anshim": dict(
        slug="anshim.html", name="안심환 엔오", theme="anshim", img="p-anshim.jpg", tag="긴장 · 스트레스 · 수면",
        tagline="예민한 하루를 위한 처방",
        lead="신경과민, 불안, 긴장, 스트레스와 관련된 불편감을 관리하기 위한 한약 환제입니다. 오래 사용해 온 탕약 처방을 스틱 포장 환제로 만들어, 쓴 탕약을 꾸준히 먹기 어려운 분도 휴대하며 복용하기 편합니다.",
        extra="특정 진단명에만 한정하지 않고, 예민함과 긴장이 증상에 함께 작용하는지를 폭넓게 살핍니다. 한약 처방이 중심이고 엔오(NO)는 보조 역할입니다.",
        facts=["1포 7g", "1박스 30포", "하루 3회 기준 10일분"],
        herbs=["복령", "시호", "황련", "야교등", "백자인", "합환피", "용골", "모려", "산조인", "원지", "석창포", "용안육", "향부자", "조구등", "유근피", "산약", "건강", "후박"],
        herbnote="",
        targets=["작은 자극에도 예민해지고 긴장이 잘 풀리지 않는 경우", "생각이 많고 스트레스 상황을 계속 떠올리는 경우", "두근거림, 얕아지는 호흡 느낌, 몸의 과도한 긴장이 함께 있는 경우", "스트레스에 따라 통증이 심해지고 근육이 굳거나, 신경성 소화 불편·이 악물기·눈 떨림이 있는 경우", "불안과 긴장 때문에 잠들기 어렵거나 숙면이 어려운 경우"],
        how=["1포는 7g이며, 1회 1포 하루 3회를 기본으로 합니다(1박스 30포 = 10일분).", "처음에는 1박스(10일분)로 복용감과 변화를 살펴봅니다.", "복용 직후의 강한 느낌보다, 예전보다 덜 신경 쓰이고 덜 예민해지는지를 살피며 3개월 정도의 관점으로 경과를 봅니다.", "예민함이 줄어든 뒤에는 하루 1회 유지 관리로 이어가기도 합니다."],
        cautions="복용 초기에 대소변 횟수가 달라지거나 나른할 수 있습니다. 졸림이나 소화 불편이 있으면 1포를 반씩 나누어 드시거나 횟수를 조절할 수 있으니 상담해 주세요. 고카페인 식품(커피, 녹차, 홍차, 콜라, 초콜릿, 에너지 음료)은 신경을 예민하게 할 수 있어 줄이시길 권합니다. 복용 중인 약이 있으면 알려 주세요.",
        desc="신경과민·불안·긴장·스트레스와 관련된 불편감을 관리하기 위한 한약 환제",
        packs=[("1박스 (30포 · 하루 3회 기준 10일분)", 99000), ("3박스 (90포 · 한 달분)", 270000)],
        from_txt="1박스 99,000원"),
    "bujong": dict(
        slug="bujong.html", name="부종환 엔오", theme="bujong", img="p-bujong.jpg", tag="붓기 · 순환",
        tagline="붓기와 순환을 위한 처방",
        lead="붓기와 다리의 당김·뭉침 같은 불편감을 관리하기 위한 한약 처방입니다. 전통 처방인 당귀작약산을 기본으로 하되 약재 비율을 달리하고 산화질소(NO)를 함께 구성했습니다.",
        extra="'서근이수(舒筋利水)', 즉 근육과 인대를 풀고 수분 배출을 돕는다는 한의학적 치료 원칙에 기반한 처방입니다.",
        facts=["10일 체험분 30포", "1개월분 90포", "저녁 늦은 복용 주의"],
        herbs=["당귀", "작약", "창출", "복령", "택사", "오약", "현호색", "산화질소(NO)"],
        herbnote="당귀·작약·창출·복령·택사가 기본 구성이며, 오약과 현호색, 산화질소(NO)를 더했습니다.",
        targets=["오래 서 있거나 앉아서 일하다 보면 다리가 붓는 경우", "종아리가 당기고 뭉치거나 다리가 저린 느낌이 있는 경우", "얼굴이나 몸이 자주 붓는 경우, 산후 붓기 관리가 필요한 경우", "식이 조절과 함께 붓기와 컨디션 관리를 하고 싶은 경우(식욕을 억제하는 처방은 아닙니다)"],
        how=["하루 3회 복용을 기준으로 1개월분은 90포입니다.", "처음에는 10일 체험분(30포)으로 복용감과 변화를 살펴볼 수 있습니다."],
        cautions="이뇨 작용이 있어 저녁 늦게 복용하면 잠자는 동안 소변으로 깰 수 있습니다. 복용 시간은 진찰 시 안내해 드립니다. 신장·심장 질환이 있거나 복용 중인 약이 있으면 알려 주세요. 복용 중 소화 불편이나 알레르기 반응이 있으면 상담해 주세요.",
        desc="붓기와 다리의 당김·뭉침 같은 불편감을 관리하기 위한 한약 처방",
        packs=[("10일 체험분 (30포)", 60000), ("1개월분 (90포)", 150000)],
        from_txt="10일 체험분 60,000원"),
}


def won(n):
    return f"{n:,}원"


def product_schema(key):
    pr = PRODUCTS[key]
    return {"@type": "Product", "name": pr["name"], "description": pr["desc"],
            "offers": [{"@type": "Offer", "name": l, "price": str(pv), "priceCurrency": "KRW",
                        "seller": {"@id": DOMAIN + "/#clinic"}} for l, pv in pr["packs"]]}


def price_cards(packs):
    return "<div class='pcards'>" + "".join(
        f"<div class='pcardp'><span>{esc(l.split(' (')[0])}</span><b>{won(v)}</b>" + (f"<small>{esc(l.split(' (')[1].rstrip(')'))}</small>" if ' (' in l else "") + "</div>"
        for l, v in packs) + "</div>"


def build_product(key):
    pr = PRODUCTS[key]
    chips = "".join(f"<li>{esc(h)}</li>" for h in pr["herbs"])
    facts = "".join(f"<li>{esc(f)}</li>" for f in pr["facts"])
    variant_html = ""
    if pr.get("variant"):
        vn, vt = pr["variant"]
        variant_html = f"""<section class="sec" style="padding-top:0">
  <div class="container narrow">
    <div class="variant"><span class="tag">ZERO</span><h3>{esc(vn)}</h3><p>{esc(vt)}</p>
</div>
  </div>
</section>"""
    body = f"""
<section class="pphero">
  <div class="container pphero-grid">
    <div class="pp-copy">
      {crumb_html(pr['name'])}
      <span class="pp-tag">{emblem(key, 'emb-s')} {pr['tag']}</span>
      <h1>{pr['name']}</h1>
      <p class="pp-tagline">{pr['tagline']}</p>
      <p class="pp-lead">{pr['lead']}</p>
      <ul class="pp-facts">{facts}</ul>
      <div class="btn-row">
        <a class="btn btn-white" href="{BOOKING}" {EXT}>네이버 예약 {ico('ext')}</a>
        <a class="btn btn-ghost" href="{TEL}">{ico('phone')} {CLINIC['phone']}</a>
      </div>
    </div>
    <figure class="pp-visual">
      <img src="assets/img/{pr['img']}" alt="" width="1400" height="1090" fetchpriority="high">
      <span class="pp-emb">{emblem(key)}</span>
    </figure>
  </div>
</section>

<section class="sec">
  <div class="container narrow">
    <div class="sec-head left"><span class="tag">COMPOSITION</span><h2>구성</h2>{('<p>' + pr['extra'] + '</p>') if pr['extra'] else ''}</div>
    <ul class="herb-chips">{chips}</ul>
    {('<p class="herb-note">' + pr['herbnote'] + '</p>') if pr['herbnote'] else ''}
  </div>
</section>

<section class="sec sec-tint">
  <div class="container narrow">
    <div class="sec-head left"><span class="tag">FOR YOU</span><h2>이런 경우 상담해 보세요</h2></div>
    {checks(pr['targets'])}
  </div>
</section>

<section class="sec">
  <div class="container narrow">
    <div class="sec-head left"><span class="tag">HOW TO</span><h2>복용 안내</h2></div>
    {checks(pr['how'])}
    {notice(pr['cautions'], '복용 시 참고')}
  </div>
</section>

{variant_html}
<section class="sec sec-tint">
  <div class="container narrow">
    <div class="sec-head left"><span class="tag">PRICE</span><h2>소비자가격</h2></div>
    {price_cards(pr['packs'])}
    <p class="price-note">※ 소비자가격이며 변동될 수 있습니다. 복용량과 기간은 진찰 후 정해 드립니다.</p>
    {disclaimer()}
  </div>
</section>
{cta_band()}"""
    page(pr["slug"], f"{pr['name']} 가격 · 복용법 | 구파발경희한의원",
         f"구파발경희한의원의 {pr['name']}. {pr['desc']}. 약재 구성, 복용 안내, 소비자가격({pr['from_txt']}부터)을 안내합니다.",
         body, current=pr["slug"], crumbs=[("홈", ""), (pr["name"], pr["slug"])],
         schema=[product_schema(key)], og=pr["img"], theme=pr["theme"])


def build_herbal_redirect():
    """예전 주소(herbal.html)는 홈의 처방 영역으로 이동"""
    page("herbal.html", "처방 안내 | 구파발경희한의원", "구파발경희한의원 처방 안내 페이지로 이동합니다.",
         "<section class='sec'><div class='container narrow center'><p class='lead'>처방별 페이지로 이동합니다. 자동으로 이동하지 않으면 아래 링크를 눌러 주세요.</p>"
         "<p><a class='btn btn-ink' href='index.html#products'>처방 보러 가기</a></p></div></section>",
         extra_head='<meta http-equiv="refresh" content="0;url=index.html#products">\n<meta name="robots" content="noindex">\n')


GONG = [
    dict(id="hwal", name="활력공진단",
         herbs=["녹용", "산수유", "당귀", "구기자", "황기", "향부자", "육계", "백출", "건강", "녹차", "감국", "박하"]),
]
GONG_PRICE = [("1환", 15000), ("30환", 450000)]
MUSK_PRICE = [("1환 (6g)", 70000)]


def build_gongjindan():
    chips = "".join(f"<li>{esc(h)}</li>" for h in GONG[0]["herbs"])
    price_rows = "".join(f"<div class='pcardp'><span>{l}</span><b>{won(v)}</b></div>" for l, v in GONG_PRICE)
    musk = "".join(f"<div class='pcardp'><span>사향 프리미엄 {l.split(' (')[0]}</span><b>{won(v)}</b><small>6g</small></div>" for l, v in MUSK_PRICE)
    body = f"""
<section class="pphero">
  <div class="container pphero-grid">
    <div class="pp-copy">
      {crumb_html("활력 · 해울 공진단")}
      <span class="pp-tag">{emblem('gong', 'emb-s')} 공진단</span>
      <h1>활력공진단</h1>
      <p class="pp-tagline">기운을 뿌리부터 채우는 처방</p>
      <p class="pp-lead">아무리 자도 피곤하고 몸이 무거울 때, 구파발경희한의원은 녹용을 비롯한 12가지 약재와 엔오를 더한 활력공진단을 처방합니다.</p>
      <ul class="pp-facts"><li>12가지 약재 + 엔오</li><li>5일 숙성 · 금박</li><li>1환 5.5g</li></ul>
      <div class="btn-row">
        <a class="btn btn-white" href="{BOOKING}" {EXT}>네이버 예약 {ico('ext')}</a>
        <a class="btn btn-ghost" href="{TEL}">{ico('phone')} {CLINIC['phone']}</a>
      </div>
    </div>
    <figure class="pp-visual"><img src="assets/img/p-gong.jpg" alt="" width="1400" height="1090" fetchpriority="high"><span class="pp-emb">{emblem('gong')}</span></figure>
  </div>
</section>

<section class="sec">
  <div class="container narrow story">
    <div class="sec-head left"><span class="tag">STORY</span><h2>피로가 잘 풀리지 않을 때</h2></div>
    <p class="quote">"아무리 자도 몸이 무겁고 집중이 잘 안 돼요."</p>
    <p>요즘 많은 분들이 이렇게 말씀하십니다. 비타민이나 영양제를 챙기고, 커피로 버티고, 힘들 땐 링거를 맞기도 합니다. 하지만 하루 이틀 나아지는 듯하다가도 일을 하고 나면 금세 다시 지치는 느낌이 들기도 합니다.</p>
    <p>구파발경희한의원은 잠깐의 보충보다 <b>기운의 뿌리</b>를 살피는 데 무게를 둡니다. 원기와 영양을 채워 주는 약재를 갖춘 활력공진단을 그래서 권해 드립니다.</p>
    <p>약재는 원장과 가족이 먹는 것과 같은 기준으로 고릅니다.</p>
  </div>
</section>

<section class="sec sec-tint">
  <div class="container narrow">
    <div class="sec-head left"><span class="tag">COMPOSITION</span><h2>12가지 약재와 엔오</h2><p>원기와 영양을 보충하는 약재를 바탕으로 하고, 엔오(NO, 산화질소)를 더했습니다.</p></div>
    <ul class="herb-chips">{chips}<li class="chip-no">엔오(NO)</li></ul>
  </div>
</section>

<section class="sec">
  <div class="container narrow">
    <div class="sec-head left"><span class="tag">PROCESS</span><h2>이렇게 만듭니다</h2></div>
    {steps([("12가지 약재와 엔오", "녹용, 산수유, 당귀 등 12가지 약재에 엔오(NO)를 더해 준비합니다."), ("초미세분말", "약재를 아주 곱게 갈아 입자를 고르게 합니다."), ("꿀 반죽", "곱게 간 약재를 꿀로 반죽해 환을 빚습니다."), ("5일 숙성", "5일간 숙성하는 과정을 거칩니다."), ("금박", "금박을 입혀 완성합니다.")])}
    <p class="muted">초미세분말로 갈아 5일간 숙성하는 방식으로 만듭니다.</p>
  </div>
</section>

<section class="sec sec-tint">
  <div class="container narrow">
    <div class="sec-head left"><span class="tag">FOR YOU</span><h2>이런 분께 상담을 권합니다</h2></div>
    {checks(["잠을 충분히 자도 피로가 잘 풀리지 않는 분", "몸이 무겁고 집중이 잘 안 되는 분", "영양제나 커피로 버티는 날이 많은 분", "수험생, 직장인 등 체력 관리가 필요한 분"])}
  </div>
</section>

<section class="sec haeul" id="haeul">
  <div class="container narrow">
    <div class="sec-head left"><span class="tag">ALTERNATIVE</span><h2>예민하고 스트레스가 많다면, 해울공진단</h2></div>
    <p class="lead-s">스트레스가 심하고 신경이 예민한 분은 활력공진단 대신 <b>해울공진단</b>이라는 대안이 있습니다.</p>
    <div class="alt-card">
      <figure><img src="assets/img/n-gong-haeul.jpg" alt="" loading="lazy" width="1600" height="1244"></figure>
      <div>
        <h3>해울공진단</h3>
        <p>활력공진단과 같은 방식으로 만들되, 기운을 순조롭게 하고 답답함을 풀어 주는 이기해울(理氣解鬱) 약재를 보강한 처방입니다.</p>
        <h4>구성</h4><p class="herbs">공진단 기본 처방(녹용 포함) + 향부자, 진피, 지각(용량 증대)</p>
        <h4>이런 분께 상담을 권합니다</h4>
        {checks(["스트레스가 많고 가슴이 답답한 느낌이 있는 분", "신경이 예민하고 긴장을 많이 하는 분", "긴장을 많이 하는 수험생"])}
        <p class="muted">1환은 5.5g이며, 녹용은 뉴질랜드산 분골을 사용합니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-tint" id="musk">
  <div class="container narrow">
    <div class="sec-head left"><span class="tag">PREMIUM</span><h2>사향 프리미엄 라인</h2></div>
    <p>활력공진단과 해울공진단에 <b>사향</b>을 더한 프리미엄 제품입니다. 사향활력공진단과 사향해울공진단 두 가지가 있으며, 선택 기준은 기존과 같습니다.</p>
    <ul class="plain"><li>구성: 기존 활력·해울 처방 + 사향 + 엔오(NO) 소량</li><li>1환은 6g으로, 일반 활력·해울(5.5g)보다 큽니다.</li></ul>
  </div>
</section>

<section class="sec">
  <div class="container narrow">
    <div class="sec-head left"><span class="tag">PRICE</span><h2>소비자가격</h2></div>
    <p class="muted">활력공진단 · 해울공진단 (일반)</p>
    <div class="pcards">{price_rows}</div>
    <p class="muted" style="margin-top:22px">사향활력공진단 · 사향해울공진단 (프리미엄)</p>
    <div class="pcards">{musk}</div>
    <p class="price-note">※ 소비자가격이며 변동될 수 있습니다. 복용 방법과 기간은 진찰 후 안내해 드립니다.</p>
    {notice("사향이 들어간 제품은 임신 중이시면 복용 전 반드시 상담해 주세요. 복용 중인 약이나 약재 알레르기가 있으면 진찰 시 알려 주세요.")}
    {disclaimer()}
  </div>
</section>
{cta_band()}"""
    prod_schema = [
        {"@type": "Product", "name": "활력공진단", "description": "녹용, 산수유, 당귀, 구기자, 황기, 향부자, 육계, 백출, 건강, 녹차, 감국, 박하 12가지 약재와 엔오를 더해 5일간 숙성하고 금박을 입힌 환제.",
         "offers": [{"@type": "Offer", "name": l, "price": str(v), "priceCurrency": "KRW", "seller": {"@id": DOMAIN + "/#clinic"}} for l, v in GONG_PRICE]},
        {"@type": "Product", "name": "해울공진단", "description": "활력공진단과 같은 방식으로 만들며 향부자, 진피, 지각을 보강한 환제. 스트레스가 많고 신경이 예민한 분을 위한 대안.",
         "offers": [{"@type": "Offer", "name": l, "price": str(v), "priceCurrency": "KRW", "seller": {"@id": DOMAIN + "/#clinic"}} for l, v in GONG_PRICE]},
        {"@type": "Product", "name": "사향 활력공진단 · 사향 해울공진단 (프리미엄)", "description": "활력·해울공진단에 사향과 엔오(소량)를 더한 프리미엄 제품. 1환 6g.",
         "offers": [{"@type": "Offer", "name": l, "price": str(v), "priceCurrency": "KRW", "seller": {"@id": DOMAIN + "/#clinic"}} for l, v in MUSK_PRICE]},
    ]
    page("gongjindan.html", "활력공진단 · 해울공진단 가격 | 구파발경희한의원",
         "구파발경희한의원의 활력공진단. 녹용 등 12가지 약재와 엔오를 더해 5일 숙성하는 공진단과, 스트레스가 많고 예민한 분을 위한 해울공진단, 사향 프리미엄 라인의 구성과 소비자가격(1환 15,000원)을 안내합니다.",
         body, current="gongjindan.html", crumbs=[("홈", ""), ("활력 · 해울 공진단", "gongjindan.html")],
         schema=prod_schema, og="p-gong.jpg", theme="gong")


def build_patch():
    body = hero_sub("엔오 리커버리 패치", "엔오 리커버리 패치",
                    "내원하지 않는 날에도 간편하게 사용할 수 있도록 만든 패치입니다. 의약품이 아닌 일반 제품(공산품)입니다.", "n-patch.jpg") + f"""
<section class="sec"><div class="container narrow prose">
  <h2>제품 소개</h2>
  <p>엔오 리커버리 패치(엔오패치)는 <b>하이드로콜로이드 소재</b>의 패치로, <b>멘톨이 함유</b>되어 있습니다. 진료를 보조하고, 내원하지 않는 날에도 집에서 간편하게 사용할 수 있도록 개발되었습니다.</p>
  <ul class="plain"><li>구성: 2장씩 8포, 1팩 총 16장</li><li>소비자가격: 1팩(16장) 15,900원</li><li>분류: 공산품 (의약품·의료기기가 아니며 진료를 대신하지 않습니다)</li></ul>
  <h2>사용 전 확인해 주세요</h2>
  {checks(["사용 부위와 연령 제한은 제품 사용설명서를 확인해 주세요.", "가려움, 화끈거림 등 자극이 느껴지면 바로 떼어 주세요. 하이드로콜로이드 소재에도 알레르기나 자극이 생길 수 있고, 밀폐와 땀 때문에 피부가 불편해질 수 있습니다.", "멘톨이 함유되어 있어 임신 중에는 사용을 권하지 않습니다.", "상처가 있거나 예민한 피부에는 사용을 피해 주세요.", "사용감과 반응에는 개인차가 있습니다."])}
  {notice("이 제품은 질병의 진단·치료·예방을 목적으로 하는 의약품이 아닙니다. 몸에 불편한 증상이 있으시면 먼저 진찰을 받아 보세요. 패치 사용 여부와 부위는 상담 시 안내해 드립니다.")}
</div></section>
{cta_band()}"""
    page("patch.html", "엔오 리커버리 패치 | 구파발경희한의원",
         "구파발경희한의원의 엔오 리커버리 패치(엔오패치). 하이드로콜로이드 소재, 멘톨 함유 패치 1팩 16장, 소비자가격 15,900원. 사용 전 주의사항을 확인해 주세요.",
         body, current="patch.html", crumbs=[("홈", ""), ("엔오 리커버리 패치", "patch.html")],
         schema=[{"@type": "Product", "name": "엔오 리커버리 패치(엔오패치)", "description": "하이드로콜로이드 소재, 멘톨 함유 패치. 1팩 16장(2장씩 8포). 공산품.",
                 "offers": {"@type": "Offer", "name": "1팩(16장)", "price": "15900", "priceCurrency": "KRW", "seller": {"@id": DOMAIN + "/#clinic"}}}], og="n-patch.jpg")


def build_yakchim():
    body = hero_sub("N약침 · 초음파 가이드 약침", "N약침(엔오약침)과<br>초음파 가이드 약침",
                    "산화질소(NO) 관련 성분을 함유한 약침과, 초음파 영상으로 위치를 확인하며 진행하는 약침 시술을 상담하실 수 있습니다.", "n-nyakchim.jpg") + f"""
<section class="sec" id="n"><div class="container split">
  <figure><img src="assets/img/n-nyakchim.jpg" alt="" loading="lazy" width="1600" height="1244"></figure>
  <div class="prose">
    <span class="tag">N-YAKCHIM</span>
    <h2>N약침 (엔오약침)</h2>
    <p>약침은 한약재에서 추출·정제한 약액을 치료 부위에 주입해 침의 자극과 약물의 작용을 함께 활용하는 치료입니다. N약침은 이 가운데 혈관·신경·림프 등과 관련된 신호전달물질인 <b>산화질소(NO) 관련 성분</b>을 함유한 약침입니다.</p>
    <h3>N약침 치료 대상</h3>
    <ul class="checks labeled">
      <li><b>근골격계 통증</b>테니스 엘보, 오십견, 퇴행성 관절염, 족저근막염 등 인대·힘줄·관절 주변의 통증</li>
      <li><b>신경계 증상</b>만성 두통, 어지럼증, 불면증, 원인을 알기 어려운 손발 저림과 신경통</li>
      <li><b>순환 관련 증상</b>수족냉증, 만성 소화불량, 생리통 등 혈액·림프 순환과 관련된 불편</li>
    </ul>
  </div>
</div></section>
<section class="sec sec-sand" id="us"><div class="container split rev">
  <figure><img src="assets/img/n-ultrasound.jpg" alt="" loading="lazy" width="1600" height="1244"></figure>
  <div class="prose">
    <span class="tag">ULTRASOUND GUIDED</span>
    <h2>초음파 가이드 약침</h2>
    <p>초음파는 방사선을 쓰지 않는 영상 검사입니다. 검사 부위에 젤을 바르고 프로브를 대어 피부 아래 구조물을 실시간 영상으로 확인합니다.</p>
    <p>초음파 가이드 약침은 이 영상을 보면서 <b>치료 부위와 주변 신경·혈관의 위치를 확인한 뒤</b> 약침을 주입하는 방식입니다. 관절과 척추 주변처럼 구조가 복잡한 부위에서 위치를 확인하며 진행할 수 있습니다.</p>
    <h3>진행 방법</h3>
    {steps([("문진 · 진찰", "통증 부위와 경과를 확인합니다."), ("초음파 확인", "영상으로 치료 부위를 확인합니다."), ("약침 시술", "영상을 보며 위치를 잡아 약침을 주입합니다."), ("경과 상담", "시술 후 주의사항과 다음 일정을 안내합니다.")])}
    <p class="muted">위치를 확인하는 과정이 있어 일반 시술보다 시간이 더 걸릴 수 있습니다. 사전 예약을 권해 드립니다.</p>
  </div>
</div></section>
<section class="sec"><div class="container narrow">{notice("출혈 경향이 있거나 항응고제를 복용 중이시거나 약물 알레르기가 있으시면 시술 전 꼭 알려 주세요.")}{disclaimer()}</div></section>
{faq_block([F["nyak"], F["nyak_diff"], F["us"], F["yak_pain"], F["yak_freq"]], "약침 관련 질문")}
{cta_band()}"""
    page("yakchim.html", "N약침(엔오약침) · 초음파 가이드 약침 | 은평구 구파발경희한의원",
         "서울 은평구 구파발경희한의원의 N약침(엔오약침)과 초음파 가이드 약침. 초음파 영상으로 위치를 확인하며 진행하는 약침 시술을 상담합니다.",
         body, current="yakchim.html", crumbs=[("홈", ""), ("N약침 · 초음파 가이드 약침", "yakchim.html")],
         schema=[faq_schema([F["nyak"], F["nyak_diff"], F["us"], F["yak_pain"], F["yak_freq"]])], og="n-ultrasound.jpg")


def build_growth():
    four = [("성조숙증 지연", "2차 성징이 일찍 나타나는 경우, 검사 결과를 바탕으로 진행 속도를 살피며 지연 방향의 치료를 상담합니다."),
            ("맞춤 한약", "나이, 성별, 체질, 소화·수면 상태를 고려해 개인별로 한약을 구성합니다."),
            ("성장침", "아이가 받아들일 수 있는 방식으로 성장과 관련된 혈위를 자극하는 침 치료입니다."),
            ("성장 추나", "자세와 척추·골반 균형을 살피는 수기 치료로, 바른 자세 관리를 돕습니다.")]
    fc = "".join(f"<div class='fcard reveal'><h3>{esc(t)}</h3><p>{esc(d)}</p></div>" for t, d in four)
    body = hero_sub("성장클리닉", "초음파 성장 검사와<br>맞춤 성장 상담",
                    "방사선을 사용하지 않는 초음파 성장 검사로 아이의 현재 성장 상태와 예상키를 확인하고, 나이와 성별에 맞춰 성장 치료를 상담합니다.", "n-growth2.jpg") + f"""
<section class="sec"><div class="container narrow prose">
  <h2>초음파 성장 검사 (RUF 방식)</h2>
  <p>방사선을 사용하지 않는 초음파 검사로 <b>예상키</b>를 확인합니다. 성장의 주요 뼈인 <b>요골, 척골, 대퇴골</b>의 연골과 골화 비율을 분석해 아이의 현재 성장 상태와 예상키를 안내해 드립니다.</p>
  <div class="fgrid f3 bones">
    <div class="fcard"><h3>요골</h3><p>아래팔에서 엄지손가락 쪽에 있는 뼈입니다.</p></div>
    <div class="fcard"><h3>척골</h3><p>아래팔에서 새끼손가락 쪽에 있는 뼈입니다.</p></div>
    <div class="fcard"><h3>대퇴골</h3><p>허벅지에 있는 가장 큰 뼈입니다.</p></div>
  </div>
  <h3>검사로 확인하는 것</h3>
  {checks(["세 뼈의 연골과 골화 비율로 본 현재 성장 상태", "현재 상태를 바탕으로 한 예상키", "방사선을 사용하지 않아 필요할 때 경과를 확인하기에 부담이 적은 검사"])}
  <p class="muted">예상키는 검사 시점의 성장 상태를 바탕으로 한 추정치이며 확정된 결과가 아닙니다. 영양, 수면, 운동, 사춘기 진행 등에 따라 달라질 수 있습니다.</p>
</div></section>
<section class="sec sec-sand"><div class="container">
  <div class="sec-head"><span class="tag">TREATMENT</span><h2>나이별 · 성별 성장 치료</h2><p>아이의 나이와 성별, 성장 단계에 따라 아래 치료를 조합합니다.</p></div>
  <div class="fgrid">{fc}</div>
  <div class="age-grid">
    <div class="panel"><h3>여아 · 만 8세 미만</h3><p>만 8세가 되기 전(8번째 생일 이전)에 <b>유방이 발달하기 시작</b>하면 성조숙증을 의심합니다. 이후 성장 속도, 뼈 나이, 초경 시기를 함께 살펴 상담합니다.</p></div>
    <div class="panel"><h3>남아 · 만 9세 미만</h3><p>만 9세가 되기 전(9번째 생일 이전)에 <b>고환이 커지기 시작</b>하면(고환 용적 4mL 이상) 성조숙증을 의심합니다. 겉으로 잘 드러나지 않아 놓치기 쉬워 성장 속도 변화를 함께 살펴봅니다.</p></div>
  </div>
  <p class="ref">※ 위 나이는 사춘기가 시작되는 시기에 대한 일반적인 기준(Marshall &amp; Tanner, 1969)이며, 대한소아내분비학회 「2022 중추성 성조숙증 임상진료지침」에서도 같은 기준을 제시합니다. 정확한 진단은 진찰과 뼈 나이, 성호르몬 검사 등으로 이루어지며, 성조숙증이 의심되면 소아청소년과(소아내분비) 진료가 필요할 수 있습니다.<br>참고: Ann Pediatr Endocrinol Metab 2023;28(3):168-177.</p>
</div></section>
<section class="sec"><div class="container narrow prose">
  <h2>진행 순서</h2>
  {steps([("상담", "키·체중 기록, 가족력, 식사·수면·운동 습관을 확인합니다."), ("초음파 성장 검사", "요골·척골·대퇴골의 연골과 골화 비율을 초음파로 분석합니다."), ("결과 상담", "현재 성장 상태와 예상키, 나이·성별을 바탕으로 방향을 설명드립니다."), ("맞춤 치료", "한약, 성장침, 성장 추나 중 필요한 치료를 조합합니다."), ("정기 확인", "성장 속도와 컨디션을 주기적으로 확인합니다.")])}
  {notice("성장에는 유전, 영양, 수면, 운동, 질환 등 여러 요인이 작용합니다. 치료로 키가 얼마나 자랄지 약속드릴 수 없습니다. 검사는 보호자와 함께 내원해 주세요. 검사·시술은 시간이 걸려 사전 예약을 권해 드립니다.")}
  {disclaimer()}
</div></section>
{faq_block([F["growth_us"], F["puberty"]], "성장 관련 질문")}
{cta_band()}"""
    page("growth.html", "성장클리닉 · 초음파 성장 검사 | 구파발경희한의원",
         "구파발경희한의원 성장클리닉. 방사선 없는 RUF 방식 초음파 성장 검사로 요골·척골·대퇴골의 연골과 골화 비율을 분석해 현재 성장 상태와 예상키를 확인합니다. 성조숙증 지연, 맞춤한약, 성장침, 성장추나 상담.",
         body, current="growth.html", crumbs=[("홈", ""), ("성장클리닉", "growth.html")],
         schema=[faq_schema([F["growth_us"], F["puberty"]])], og="n-growth2.jpg")


def build_accident():
    six = [("침", "근육과 관절 주변의 긴장을 살피며 통증 부위에 침을 놓습니다."),
           ("부항", "뭉친 근육과 결림이 있는 부위에 시행하는 보조 치료입니다."),
           ("물리치료", "온열·전기 등 물리치료로 통증 부위를 관리합니다."),
           ("추나요법", "목·허리·골반의 균형을 살피는 수기 치료입니다."),
           ("약침", "치료 부위에 약침액을 주입합니다. 필요하면 초음파로 위치를 확인합니다."),
           ("맞춤 한약", "회복 시기와 체력, 소화 상태에 맞춰 한약을 구성합니다.")]
    sc = "".join(f"<div class='fcard reveal'><h3>{esc(t)}</h3><p>{esc(d)}</p></div>" for t, d in six)
    body = hero_sub("교통사고 후유증", "교통사고 후유증,<br>상태에 맞는 치료를 조합합니다",
                    "침, 부항, 물리치료, 추나요법, 약침, 맞춤 한약을 진찰 후 상태에 맞게 조합해 진행합니다.", "n-accident.jpg") + f"""
<section class="sec"><div class="container narrow prose">
  <h2>이런 증상이 있으면 상담해 보세요</h2>
  {checks(["목·어깨·허리가 뻐근하고 결리는 경우", "두통, 어지럼, 메스꺼움이 이어지는 경우", "팔다리가 저리거나 힘이 빠지는 느낌이 있는 경우", "사고 직후에는 괜찮았는데 며칠 뒤 통증이 나타난 경우"])}
  {notice("의식을 잃었거나, 극심한 통증, 팔다리 마비, 호흡 곤란 같은 증상이 있으면 먼저 응급실을 방문해 주세요.", "먼저 확인하세요")}
</div></section>
<section class="sec sec-sand"><div class="container">
  <div class="sec-head"><span class="tag">TREATMENT</span><h2>치료 방법</h2></div>
  <div class="fgrid f3">{sc}</div>
</div></section>
<section class="sec"><div class="container narrow prose">
  <h2>자동차보험 진료</h2>
  <p>자동차보험으로 진료받으실 때 필요한 접수 방법과 서류는 상황에 따라 다를 수 있습니다. 내원 전에 전화(<a href="{TEL}">{CLINIC['phone']}</a>)로 문의해 주시면 안내해 드립니다.</p>
  {disclaimer()}
</div></section>
{faq_block([F["accident"]], "교통사고 관련 질문")}
{cta_band()}"""
    page("accident.html", "교통사고 후유증 한의원 | 은평구 구파발경희한의원",
         "구파발경희한의원 교통사고 후유증 진료. 침, 부항, 물리치료, 추나요법, 약침, 맞춤 한약을 상태에 맞게 조합합니다. 자동차보험 문의 가능.",
         body, current="accident.html", crumbs=[("홈", ""), ("교통사고 후유증", "accident.html")],
         schema=[faq_schema([F["accident"]])], og="n-accident.jpg")


def build_about():
    career = ["경희대학교 한의과대학 졸업", "횡성군보건소 한방진료과장", "경희대학교 침구경락센터 협력 한의사",
              "한국한의학연구원 임상연구협력 한의사", "국민건강보험공단 장기요양등급판정위원",
              "N약침 초음파 유도하 약침 정규과정 수료", "제중학회 학술부회장", "한방비만학회 회원", "대한스포츠한의학회 회원",
              "前) 으뜸경희한의원 진료원장", "前) 365경희솔한의원 대표원장"]
    body = f"""
<section class="phero"><div class="container phero-grid">
  <div>{crumb_html("원장소개")}<h1>대표원장 {CLINIC['doctor']}</h1>
  <p class="lead">환자 한 분 한 분의 이야기를 듣고, 직접 진찰하고, 쉽게 설명드립니다.</p></div>
  <figure class="phero-img round"><img src="assets/img/doctor.jpg" alt="구파발경희한의원 대표원장 최솔" width="1024" height="1024"></figure>
</div></section>
<section class="sec"><div class="container narrow prose">
  <h2>약력</h2>
  <ul class="timeline">{"".join(f"<li>{esc(c)}</li>" for c in career)}</ul>
  <h2>진료 철학</h2>
  <div class="trio t-flat">
    <div><span class="num">01</span><h3>듣는 진료</h3><p>증상뿐 아니라 생활 습관과 고민까지 충분히 듣겠습니다.</p></div>
    <div><span class="num">02</span><h3>과하지 않은 진료</h3><p>꼭 필요한 치료를 권하고 그 이유를 설명드립니다.</p></div>
    <div><span class="num">03</span><h3>꾸준한 관리</h3><p>치료 이후에도 생활 관리법을 안내해 드립니다.</p></div>
  </div>
</div></section>
<section class="sec sec-sand"><div class="container split"><figure><img src="assets/img/n-clinic.jpg" alt="상담실 예시 이미지" loading="lazy" width="1600" height="1244"><figcaption>상담실 예시 이미지 (AI 생성)</figcaption></figure>
  <div class="prose"><h2>구파발경희한의원</h2><p>{CLINIC['address']}에 있습니다. 지하철 3호선 구파발역 인근이며, 저칼로리 다이어트, N약침·초음파 가이드 약침, 성장클리닉, 교통사고 후유증 진료를 하고 있습니다.</p><p><a class="btn btn-line" href="hours-location.html">진료시간 · 오시는 길</a></p></div></div></section>
{cta_band()}"""
    page("about.html", "원장 소개 | 구파발경희한의원 대표원장 최솔",
         "구파발경희한의원 대표원장 최솔 약력 – 경희대학교 한의과대학 졸업, 횡성군보건소 한방진료과장, 한국한의학연구원 임상연구협력 한의사.",
         body, current="about.html", crumbs=[("홈", ""), ("원장소개", "about.html")], schema=[doctor_schema()], og="doctor.jpg")


def build_visit():
    body = f"""
<section class="phero phero-plain"><div class="container">{crumb_html("진료시간 · 오시는 길")}<h1>진료시간 · 오시는 길</h1><p class="lead">방문 전 확인해 주세요.</p></div></section>
<section class="sec"><div class="container info-grid">
  <div class="panel" id="hours"><h3>진료시간</h3><table class="hours"><tbody>{hours_rows()}</tbody></table>
    <p class="muted">공휴일과 임시 휴진은 달라질 수 있어 전화로 확인해 주세요.</p>
    <p><a class="btn btn-solid" href="{TEL}">{ico('phone')} {CLINIC['phone']}</a></p></div>
  <div class="panel" id="map"><h3>오시는 길</h3><p class="addr">{CLINIC['address']}</p>
    <p class="muted">은평뉴타운 상림마을 아이파크 708동 상가 1층 · 708동 앞 버스정류장 바로 뒤쪽</p>
    <div class="btn-row"><a class="btn btn-naver" href="{CLINIC['naver']}" target="_blank" rel="noopener">네이버지도</a><a class="btn btn-kakao" href="{CLINIC['kakao']}" target="_blank" rel="noopener">카카오맵</a></div>
    <h4 class="way">대중교통</h4>
    <p class="muted">지하철 3호선 구파발역 1번·2번 출구 사이에서 704번, 708번, 7211번, 7723번 버스를 타고 아이파크 701동 앞 정류장에서 내려 건너편으로 오시면 됩니다.</p>
    <h4 class="way">주차</h4>
    <p class="parking">708동 지하주차장 <b>무료 주차</b> 가능</p></div>
</div></section>
{cta_band()}"""
    page("hours-location.html", "진료시간 · 오시는 길 | 구파발경희한의원 (은평구 진관4로 47)",
         "구파발경희한의원 진료시간과 오시는 길. 서울 은평구 진관4로 47, 은평뉴타운 상림마을 708동 상가 115호, 구파발역 인근, 708동 지하주차장 무료 주차. 월·화·수·금 09:30–20:00, 목 14:00–20:00, 토 09:30–13:00.",
         body, current="hours-location.html", crumbs=[("홈", ""), ("진료시간 · 오시는 길", "hours-location.html")])


def build_faq():
    body = f"""
<section class="phero phero-plain"><div class="container">{crumb_html("자주 묻는 질문")}<h1>자주 묻는 질문</h1><p class="lead">환자분들이 많이 묻는 질문을 모았습니다.</p></div></section>
{faq_block(FAQS, "전체 질문")}
{cta_band()}"""
    page("faq.html", "자주 묻는 질문 | 구파발경희한의원",
         "구파발경희한의원 자주 묻는 질문 – 진료시간, 위치, 저칼로리 다이어트, N약침, 초음파 가이드 약침, 성장 검사, 교통사고 후유증.",
         body, current="faq.html", crumbs=[("홈", ""), ("자주 묻는 질문", "faq.html")], schema=[faq_schema(FAQS)])


def build_reservation():
    body = f"""
<section class="phero phero-plain"><div class="container">{crumb_html("예약 · 문의")}<h1>예약 · 문의</h1><p class="lead">네이버 예약으로 편하게 예약하시거나, 전화로 문의해 주세요.</p></div></section>
<section class="sec"><div class="container info-grid">
  <div class="panel"><h3>네이버 예약</h3>
    <p>원하시는 날짜와 시간을 선택해 예약하실 수 있습니다. 초음파 가이드 약침과 초음파 성장 검사는 확인과 준비에 시간이 더 걸려 사전 예약을 권해 드립니다.</p>
    <p><a class="btn btn-solid" href="{BOOKING}" {EXT}>네이버 예약하러 가기 →</a></p>
    <p class="muted">네이버 예약 페이지로 이동합니다. 예약 가능 시간은 진료시간과 같습니다.</p></div>
  <div class="panel"><h3>전화 상담</h3><p class="bigtel"><a href="{TEL}">{CLINIC['phone']}</a></p>
    <table class="hours"><tbody>{hours_rows()}</tbody></table>
    <p class="muted">공휴일과 임시 휴진은 달라질 수 있어 전화로 확인해 주세요.</p></div>
</div></section>
"""
    page("reservation.html", "예약 · 문의 | 구파발경희한의원 (네이버 예약)",
         "구파발경희한의원 예약·문의. 네이버 예약 또는 전화 02-355-4517. 초음파 가이드 약침·성장 검사는 사전 예약 권장.",
         body, current="reservation.html", crumbs=[("홈", ""), ("예약 · 문의", "reservation.html")])


PRIVACY_DATE = "2026년 11월 8일"


def build_privacy():
    c = CLINIC
    body = f"""
<section class="phero phero-plain"><div class="container">{crumb_html("개인정보처리방침")}<h1>개인정보처리방침</h1><p class="lead">시행일 {PRIVACY_DATE}</p></div></section>
<section class="sec"><div class="container narrow prose privacy">
  <p>{c['name']}(이하 '한의원')은 「개인정보 보호법」 등 관련 법령에 따라 정보주체의 개인정보를 보호하고, 이와 관련한 고충을 신속하고 원활하게 처리할 수 있도록 다음과 같이 개인정보 처리방침을 수립하여 공개합니다.</p>

  <h2>1. 개인정보의 처리 목적, 항목 및 보유기간</h2>
  <p>한의원은 아래 목적에 필요한 최소한의 개인정보를 처리하며, 목적 외의 용도로 이용하지 않습니다.</p>
  <div class="ptable-wrap"><table class="ptable">
    <thead><tr><th>구분</th><th>처리 목적</th><th>처리 항목</th><th>보유기간</th></tr></thead>
    <tbody>
      <tr><td>진료·상담 (내원·전화)</td><td>진료, 처방, 상담, 진료비 수납</td><td>성명, 생년월일, 성별, 연락처, 증상·병력 등 건강에 관한 정보</td><td>「의료법 시행규칙」에 따른 기간 (진료기록부 10년, 처방전 2년 등)</td></tr>
      <tr><td>예약 확인</td><td>예약 확인 및 안내, 진료 준비</td><td>성명, 연락처, 희망 일시, 문의 내용</td><td>목적 달성 후 지체 없이 파기 (진료로 이어진 경우 위 진료기록 기준)</td></tr>
      <tr><td>보험 청구</td><td>건강보험·자동차보험 진료비 청구</td><td>성명, 주민등록번호(법령에서 허용하는 경우), 보험 관련 정보</td><td>관련 법령에 따른 기간</td></tr>
    </tbody>
  </table></div>
  <p class="muted">건강에 관한 정보는 「개인정보 보호법」상 민감정보에 해당하며, 진료에 필요한 범위에서 정보주체의 동의 또는 법령에 근거하여 처리합니다.</p>

  <h2>2. 홈페이지 이용과 개인정보</h2>
  <ul>
    <li>이 홈페이지는 회원가입, 로그인, 문의 양식을 운영하지 않으며 이용자의 개인정보를 직접 수집하지 않습니다.</li>
    <li>홈페이지를 제공하는 호스팅 서비스(GitHub Pages)와 글꼴 제공 서비스(jsDelivr)에서 서비스 운영을 위해 접속 정보(IP 주소, 브라우저 정보 등)가 처리될 수 있습니다.</li>
    <li>한의원은 쿠키를 설치하거나 방문자 분석·광고 도구를 사용하지 않습니다. 다만 네이버 예약, 지도 등 외부 서비스로 이동하면 해당 서비스가 쿠키를 사용할 수 있으며, 이는 각 서비스의 개인정보처리방침이 적용됩니다.</li>
  </ul>

  <h2>3. 네이버 예약 이용 시</h2>
  <p>네이버 예약은 네이버(주)가 제공하는 서비스로, 이용자가 입력한 개인정보는 네이버의 개인정보처리방침에 따라 처리됩니다. 한의원은 예약 확인과 진료 준비를 위해 예약자 정보를 열람합니다.</p>

  <h2>4. 개인정보의 제3자 제공</h2>
  <p>한의원은 정보주체의 개인정보를 원칙적으로 외부에 제공하지 않습니다. 다만 다음의 경우에는 예외로 합니다.</p>
  <ul>
    <li>정보주체가 사전에 동의한 경우</li>
    <li>건강보험·자동차보험 진료비 청구 등 법령에서 정한 절차에 따라 건강보험공단, 건강보험심사평가원, 보험회사 등에 제공해야 하는 경우</li>
    <li>법령에 특별한 규정이 있거나 수사기관이 법령에서 정한 절차에 따라 요청하는 경우</li>
  </ul>

  <h2>5. 개인정보 처리의 위탁</h2>
  <p>한의원은 개인정보 처리업무를 외부에 위탁하는 경우 수탁자와 위탁하는 업무의 내용을 이 방침을 통해 공개하고, 수탁자가 개인정보를 안전하게 처리하도록 관리·감독합니다. 현재 이 방침에 공개할 위탁 업무는 없습니다.</p>

  <h2>6. 개인정보의 파기 절차 및 방법</h2>
  <ul>
    <li>보유기간이 지났거나 처리 목적을 달성한 개인정보는 지체 없이 파기합니다. 다만 법령에 따라 보존해야 하는 경우에는 다른 개인정보와 분리하여 보관합니다.</li>
    <li>전자적 파일은 복구할 수 없는 방법으로 영구 삭제하고, 종이 문서는 분쇄하거나 소각합니다.</li>
  </ul>

  <h2>7. 정보주체와 법정대리인의 권리·의무 및 행사 방법</h2>
  <ul>
    <li>정보주체는 한의원에 대해 언제든지 개인정보의 열람, 정정·삭제, 처리정지, 동의 철회를 요구할 수 있습니다.</li>
    <li>요구는 전화({c['phone']}) 또는 내원을 통해 하실 수 있으며, 한의원은 지체 없이 필요한 조치를 합니다. 열람은 요구를 받은 날부터 10일 이내에 처리합니다.</li>
    <li>법령에서 보존하도록 한 개인정보(진료기록 등)는 삭제를 요구하더라도 보존기간 동안 삭제할 수 없습니다.</li>
    <li>만 14세 미만 아동의 개인정보는 법정대리인(보호자)의 동의를 받아 처리하며, 법정대리인이 아동을 대리하여 위 권리를 행사할 수 있습니다.</li>
    <li>권리 행사는 대리인을 통해서도 할 수 있으며, 이 경우 위임장 등 대리 관계를 확인할 수 있는 자료가 필요합니다.</li>
  </ul>

  <h2>8. 개인정보의 안전성 확보 조치</h2>
  <ul>
    <li><b>관리적 조치</b>: 개인정보를 취급하는 직원을 최소한으로 지정하고 교육합니다.</li>
    <li><b>기술적 조치</b>: 개인정보 처리 시스템의 접근 권한을 관리하고, 비밀번호를 설정하며, 보안 프로그램을 설치·갱신합니다.</li>
    <li><b>물리적 조치</b>: 진료기록 등 개인정보가 담긴 문서와 장비는 잠금장치가 있는 장소에 보관합니다.</li>
  </ul>

  <h2>9. 개인정보 보호책임자</h2>
  <p>한의원은 개인정보 처리에 관한 업무를 총괄하고, 정보주체의 불만 처리와 피해 구제를 위해 아래와 같이 개인정보 보호책임자를 지정합니다.</p>
  <ul>
    <li>성명: {c['doctor']} (대표원장)</li>
    <li>연락처: <a href="{TEL}">{c['phone']}</a></li>
    <li>주소: {c['address']}</li>
  </ul>

  <h2>10. 권익침해 구제방법</h2>
  <p>정보주체는 개인정보 침해로 인한 구제를 받기 위해 아래 기관에 분쟁 해결이나 상담을 신청할 수 있습니다.</p>
  <ul>
    <li>개인정보분쟁조정위원회: 1833-6972 (www.kopico.go.kr)</li>
    <li>개인정보침해신고센터: 국번 없이 118 (privacy.kisa.or.kr)</li>
    <li>대검찰청: 국번 없이 1301 (www.spo.go.kr)</li>
    <li>경찰청: 국번 없이 182 (ecrm.police.go.kr)</li>
  </ul>

  <h2>11. 개인정보 처리방침의 변경</h2>
  <p>이 방침은 {PRIVACY_DATE}부터 적용됩니다. 내용이 바뀌는 경우 변경 사항을 이 페이지를 통해 알려 드립니다.</p>
</div></section>"""
    page("privacy.html", "개인정보처리방침 | 구파발경희한의원", f"{c['name']} 개인정보처리방침. 개인정보의 처리 목적·항목·보유기간, 정보주체의 권리, 개인정보 보호책임자 등을 안내합니다.",
         body, crumbs=[("홈", ""), ("개인정보처리방침", "privacy.html")])


def build_404():
    body = f"""<section class="sec"><div class="container narrow center"><p class="big404">404</p><h1>페이지를 찾을 수 없습니다</h1><p class="lead">주소가 바뀌었거나 삭제된 페이지입니다.</p><p><a class="btn btn-solid" href="/index.html">홈으로 가기</a></p></div></section>"""
    page("404.html", "페이지를 찾을 수 없습니다 | 구파발경희한의원", "요청하신 페이지를 찾을 수 없습니다.", body)


PAGES = ["index.html", "diet.html", "bopae.html", "anshim.html", "bujong.html", "gongjindan.html", "patch.html", "yakchim.html", "growth.html", "accident.html",
         "about.html", "hours-location.html", "faq.html", "reservation.html", "privacy.html"]


def build_meta():
    urls = "".join(f"  <url><loc>{DOMAIN}/{'' if p == 'index.html' else p}</loc><lastmod>{TODAY}</lastmod></url>\n" for p in PAGES)
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    bots = ["GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-User", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended"]
    robots = "User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {DOMAIN}/sitemap.xml\n"
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(robots)
    llms = f"""# {CLINIC['name']}

> 서울 은평구 구파발역 인근의 한의원입니다. 대표원장 {CLINIC['doctor']}.
> 주소: {CLINIC['address']} / 전화: {CLINIC['phone']}

## 진료시간
- 월·화·수·금 09:30–20:00 (점심시간 12:30–14:00)
- 목 14:00–20:00
- 토 09:30–13:00 (점심시간 없음)
- 일·공휴일 휴진

## 진료 프로그램
- [저칼로리 다이어트]({DOMAIN}/diet.html): 저칼로리 식단과 원내에서 직접 달이는 개별 맞춤 한약
- [보폐고 엔오]({DOMAIN}/bopae.html): 호흡기·목 관리 한약 처방. 1박스(45포) 170,000원. 꿀이 들어가지 않은 제로 버전도 있음
- [안심환 엔오]({DOMAIN}/anshim.html): 긴장·스트레스 관련 한약 환제. 1박스(30포) 99,000원
- [부종환 엔오]({DOMAIN}/bujong.html): 붓기·순환 관리 한약 처방. 1개월분(90포) 150,000원
- [활력공진단 · 해울공진단]({DOMAIN}/gongjindan.html): 녹용 포함, 1환 15,000원·30환 450,000원, 사향 프리미엄 1환 70,000원 (소비자가격)
- [엔오 리커버리 패치]({DOMAIN}/patch.html): 1팩 16장 15,900원, 공산품
- [N약침 · 초음파 가이드 약침]({DOMAIN}/yakchim.html)
- [성장클리닉 · 초음파 성장 검사]({DOMAIN}/growth.html): RUF 방식(요골·척골·대퇴골 연골과 골화 비율 분석)으로 현재 성장 상태와 예상키 확인, 성조숙증 지연·맞춤한약·성장침·성장추나
- [교통사고 후유증]({DOMAIN}/accident.html): 침, 부항, 물리치료, 추나요법, 약침, 맞춤 한약

## 예약
- 네이버 예약: {BOOKING}
- 전화: {CLINIC['phone']}
- 주차: 708동 지하주차장 무료 주차 가능
- 지도: {CLINIC['naver']} (네이버), {CLINIC['kakao']} (카카오)

## 기타
- [원장 소개]({DOMAIN}/about.html)
- [진료시간 · 오시는 길]({DOMAIN}/hours-location.html)
- [자주 묻는 질문]({DOMAIN}/faq.html)

치료 효과와 경과는 개인에 따라 다를 수 있으며, 본 정보는 진찰을 대신하지 않습니다.
"""
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write(llms)


if __name__ == "__main__":
    for fn in (build_home, build_diet, lambda: build_product("bopae"), lambda: build_product("anshim"), lambda: build_product("bujong"), build_herbal_redirect, build_gongjindan, build_patch, build_yakchim, build_growth, build_accident,
               build_about, build_visit, build_faq, build_reservation, build_privacy, build_404, build_meta):
        fn()
    print("built", len(PAGES) + 1, "pages")
