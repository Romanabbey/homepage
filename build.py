#!/usr/bin/env python3
"""구파발경희한의원 사이트 생성기.
사용법: python3 build.py   (이 폴더에 HTML, sitemap.xml, robots.txt, llms.txt 생성)
정보(전화/시간/주소)는 아래 CLINIC 한 곳에서만 수정하세요."""
import json, html, datetime, os

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://gupabalhani.org"
TODAY = datetime.date.today().isoformat()

CLINIC = dict(
    name="구파발경희한의원",
    doctor="최솔",
    address="서울 은평구 진관4로 47, 708동 상가 115호",
    street="진관4로 47, 708동 상가 115호",
    phone="02-355-4517",
    phone_intl="+82-2-355-4517",
    biz="218-90-15783",
    naver="https://map.naver.com/p/search/" + "%EC%84%9C%EC%9A%B8%20%EC%9D%80%ED%8F%89%EA%B5%AC%20%EC%A7%84%EA%B4%804%EB%A1%9C%2047",
    kakao="https://map.kakao.com/?q=" + "%EC%84%9C%EC%9A%B8%20%EC%9D%80%ED%8F%89%EA%B5%AC%20%EC%A7%84%EA%B4%804%EB%A1%9C%2047",
)
TEL = "tel:" + CLINIC["phone"].replace("-", "")

# (표시용 요일, 시간, 비고)
HOURS = [
    ("월 · 화 · 수 · 금", "09:30 – 20:00", "점심시간 12:30 – 14:00"),
    ("목", "14:00 – 20:00", "오후 진료"),
    ("토", "09:30 – 13:00", "점심시간 없음"),
    ("일 · 공휴일", "휴진", ""),
]

DISCLAIMER = "치료 효과와 경과는 개인에 따라 다를 수 있습니다. 이 페이지는 일반적인 안내이며, 실제 치료는 진찰 후 개인별로 안내드립니다."

NAV = [
    ("진료 프로그램", "#", [
        ("저칼로리 다이어트", "diet.html"),
        ("맞춤 한약 · 엔오 시리즈", "herbal.html"),
        ("엔오 리커버리 패치", "patch.html"),
        ("N약침 · 초음파 가이드 약침", "yakchim.html"),
    ]),
    ("성장클리닉", "growth.html", []),
    ("교통사고 후유증", "accident.html", []),
    ("원장소개", "about.html", []),
    ("진료안내", "hours-location.html", [
        ("진료시간 · 오시는 길", "hours-location.html"),
        ("자주 묻는 질문", "faq.html"),
    ]),
]

# ------------------------------------------------------------------ FAQ
FAQS = [
    ("진료시간은 어떻게 되나요?",
     "월·화·수·금요일은 09:30~20:00(점심시간 12:30~14:00), 목요일은 14:00~20:00, 토요일은 09:30~13:00(점심시간 없음)입니다. 일요일과 공휴일은 휴진입니다. 휴진 일정이 바뀔 수 있어 방문 전 전화(02-355-4517)로 확인하시면 가장 정확합니다."),
    ("위치와 가는 방법을 알려 주세요.",
     "서울 은평구 진관4로 47, 708동 상가 115호에 있으며 지하철 3호선 구파발역 인근입니다. 네이버지도·카카오맵에서 '구파발경희한의원'을 검색하시면 길 안내를 받으실 수 있습니다."),
    ("예약 없이 방문해도 되나요?",
     "방문은 가능하지만 초음파 가이드 약침이나 초음파 성장 검사는 확인과 준비에 시간이 더 걸려 사전 예약을 권해 드립니다. 전화 02-355-4517 또는 온라인 예약으로 문의해 주세요."),
    ("저칼로리 다이어트는 어떻게 진행되나요?",
     "상담과 진찰로 현재 상태를 확인한 뒤, 저칼로리 식단과 함께 개인별로 구성한 맞춤 한약을 원내에서 직접 달여 드립니다. 진행 중에는 경과를 확인하며 식단과 처방을 조정하고, 이후 유지 관리까지 상담합니다. 건강 상태에 따라 적합하지 않을 수 있어 사전 진찰이 필요합니다."),
    ("'원내에서 직접 달이는 개별 맞춤 한약'은 무슨 뜻인가요?",
     "진찰을 마친 뒤 환자분의 체질과 상태에 맞춰 약재를 구성하고, 한의원 안에서 직접 달여 조제한다는 뜻입니다. 구성과 복용 기간은 진찰 결과에 따라 달라집니다."),
    ("N약침(엔오약침)은 무엇인가요?",
     "한약재에서 추출·정제한 약액을 치료 부위에 주입하는 약침 가운데, 산화질소(NO) 관련 성분을 함유한 약침입니다. 어떤 약침이 적합한지는 진찰 후 상태에 맞춰 정합니다."),
    ("초음파 가이드 약침은 일반 약침과 무엇이 다른가요?",
     "초음파 영상으로 치료 부위와 주변 구조물을 실시간으로 확인하면서 시술하는 방식입니다. 위치를 영상으로 확인하며 진행한다는 점이 다르며, 확인 과정에 시간이 조금 더 걸릴 수 있습니다."),
    ("초음파 성장 검사에도 방사선을 쓰나요?",
     "초음파 검사는 방사선을 사용하지 않습니다. 구파발경희한의원의 성장 검사는 RUF 연골 측정 방식의 초음파 검사로 진행합니다. 결과는 성장 상담의 참고 자료로 쓰이며, 성장 결과를 보장하는 것은 아닙니다."),
    ("성조숙증은 몇 살부터 의심하나요?",
     "일반적으로 여아는 만 8세 이전, 남아는 만 9세 이전에 2차 성징이 나타나면 성조숙증을 의심해 확인해 볼 것을 권합니다. 정확한 판단은 진찰과 검사를 통해 이루어지므로 걱정되시면 상담을 받아 보세요."),
    ("교통사고 후유증 치료는 어떻게 받나요?",
     "침, 부항, 물리치료, 추나요법, 약침, 맞춤 한약 중 상태에 맞는 치료를 조합해 진행합니다. 자동차보험 접수 방법은 전화로 문의해 주세요. 의식 소실, 극심한 통증, 팔다리 마비 같은 증상이 있으면 먼저 응급실을 방문하셔야 합니다."),
    ("엔오(NO) 시리즈 한약은 누구나 복용할 수 있나요?",
     "체질과 상태, 복용 중인 약에 따라 맞지 않을 수 있습니다. 임신·수유 중이거나 다른 약을 복용 중이시면 진찰 시 꼭 알려 주세요."),
    ("치료 효과는 얼마나 기대할 수 있나요?",
     "증상과 경과는 사람마다 다르므로 특정 효과를 약속드릴 수 없습니다. 진찰 후 예상되는 치료 방향과 기간, 생활 관리법을 설명드립니다."),
]


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
    services = ["저칼로리 다이어트 맞춤 한약", "맞춤 한약", "엔오 리커버리 패치", "N약침(엔오약침)",
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
        "areaServed": ["서울특별시 은평구", "구파발", "진관동"],
        "openingHoursSpecification": spec,
        "availableService": [{"@type": "MedicalTherapy", "name": s} for s in services],
        "founder": {"@id": DOMAIN + "/#doctor"},
        "medicalSpecialty": "TraditionalChineseMedicine",
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
        active = " class='active'" if current and (href == current or any(u == current for _, u in subs)) else ""
        if subs:
            sub = "".join(f"<a href='{u}'>{esc(n)}</a>" for n, u in subs)
            top = f"<a href='{href}'{active}>{esc(label)}</a>" if href != "#" else f"<button type='button' class='navbtn'{active}>{esc(label)}</button>"
            items.append(f"<li class='has-sub'>{top}<div class='sub'>{sub}</div></li>")
        else:
            items.append(f"<li><a href='{href}'{active}>{esc(label)}</a></li>")
    nav = "".join(items)
    return f"""<a class="skip" href="#main">본문 바로가기</a>
<header class="site-header">
  <div class="topbar"><div class="container">
    <span class="tb-addr">📍 {CLINIC['address']}</span>
    <span><a href="{TEL}">☎ {CLINIC['phone']}</a><span class="tb-sep">·</span><span id="openNow" class="open-now">진료시간 확인</span></span>
  </div></div>
  <div class="container nav-wrap">
    <a class="brand" href="index.html" aria-label="{CLINIC['name']} 홈">
      <svg viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="12" fill="#1d4a3a"/><path d="M12 28c0-9 6-15 17-16 0 10-6 16-15 16" fill="none" stroke="#f6f1e7" stroke-width="2" stroke-linejoin="round"/><path d="M11 29l10-10" stroke="#e7b89b" stroke-width="2" stroke-linecap="round"/></svg>
      <span><b>{CLINIC['name']}</b><small>구파발 한의원 · 대표원장 {CLINIC['doctor']}</small></span>
    </a>
    <nav aria-label="주 메뉴"><ul class="gnb" id="gnb">{nav}</ul></nav>
    <a class="btn btn-solid nav-cta" href="reservation.html">예약 · 문의</a>
    <button class="burger" id="burger" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>"""


def footer_html():
    links = "".join(f"<a href='{u}'>{esc(n)}</a>" for n, u in [
        ("저칼로리 다이어트", "diet.html"), ("맞춤 한약", "herbal.html"), ("엔오 리커버리 패치", "patch.html"),
        ("N약침 · 초음파 가이드 약침", "yakchim.html"), ("성장클리닉", "growth.html"),
        ("교통사고 후유증", "accident.html"), ("원장소개", "about.html"), ("진료시간 · 오시는 길", "hours-location.html"),
        ("자주 묻는 질문", "faq.html"), ("개인정보처리방침", "privacy.html")])
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="foot-grid">
      <div>
        <p class="foot-brand">{CLINIC['name']}</p>
        <address>
          대표원장 {CLINIC['doctor']} · 사업자등록번호 {CLINIC['biz']}<br>
          {CLINIC['address']}<br>
          TEL <a href="{TEL}">{CLINIC['phone']}</a>
        </address>
        <p class="foot-hours">월·화·수·금 09:30–20:00 (점심 12:30–14:00) · 목 14:00–20:00 · 토 09:30–13:00 · 일·공휴일 휴진</p>
      </div>
      <nav class="foot-links" aria-label="푸터 메뉴">{links}</nav>
    </div>
    <p class="foot-note">본 사이트의 내용은 일반적인 건강 정보이며 개인별 진단·치료를 대신하지 않습니다. {DISCLAIMER.split('. ')[0]}. 일부 이미지는 AI로 생성한 예시 이미지이며 실제 한의원 모습과 다를 수 있습니다.</p>
    <p class="foot-note">© {datetime.date.today().year} {CLINIC['name']}. All rights reserved.</p>
  </div>
</footer>
<div class="fab" aria-label="빠른 메뉴">
  <a class="fab-call" href="{TEL}"><span aria-hidden="true">☎</span> 전화 상담</a>
  <a class="fab-rsv" href="reservation.html"><span aria-hidden="true">📅</span> 온라인 예약</a>
</div>
<button class="to-top" id="toTop" aria-label="맨 위로">↑</button>
<script src="js/main.js" defer></script>"""


def page(slug, title, desc, body, current=None, schema=None, crumbs=None, og="n-og.jpg", home=False):
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
<link rel="stylesheet" href="css/style.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{header_html(current)}
<main id="main">
{body}
</main>
{footer_html()}
</body>
</html>
"""
    if slug == "404.html":  # 어떤 경로에서 열려도 깨지지 않도록 절대경로 사용
        for a in ("css/", "js/", "favicon.svg", "index.html", "about.html", "diet.html", "herbal.html", "patch.html",
                  "yakchim.html", "growth.html", "accident.html", "hours-location.html", "faq.html", "reservation.html", "privacy.html"):
            out = out.replace(f"href='{a}", f"href='/{a}").replace(f'href="{a}', f'href="/{a}').replace(f'src="{a}', f'src="/{a}')
        out = out.replace('href="//index.html"', 'href="/index.html"')
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
        <a class="btn btn-solid" href="reservation.html">예약 · 문의</a>
        <a class="btn btn-line" href="{TEL}">☎ {CLINIC['phone']}</a>
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
    <div class="btn-row"><a class="btn btn-light" href="{TEL}">☎ {CLINIC['phone']}</a><a class="btn btn-ghost" href="reservation.html">온라인 예약</a></div>
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
    programs = [
        ("n-diet.jpg", "저칼로리 다이어트", "저칼로리 식단과 원내에서 직접 달이는 개별 맞춤 한약으로 진행합니다.", "diet.html"),
        ("n-decoction.jpg", "맞춤 한약 · 엔오 시리즈", "보폐고 엔오, 안심환 엔오, 부종환 엔오를 진찰 후 안내합니다.", "herbal.html"),
        ("n-patch.jpg", "엔오 리커버리 패치", "붙여서 사용하는 외용 패치로, 사용 부위와 방법을 안내합니다.", "patch.html"),
        ("n-nyakchim.jpg", "N약침 (엔오약침)", "산화질소(NO) 관련 성분을 함유한 약침 치료입니다.", "yakchim.html#n"),
        ("n-ultrasound.jpg", "초음파 가이드 약침", "초음파 영상으로 위치를 확인하며 진행하는 약침 시술입니다.", "yakchim.html#us"),
        ("n-growth2.jpg", "성장클리닉 · 초음파 성장 검사", "RUF 연골 측정 방식의 검사와 나이·성별 맞춤 성장 상담을 진행합니다.", "growth.html"),
        ("n-accident.jpg", "교통사고 후유증", "침·부항·물리치료·추나·약침·맞춤 한약을 상태에 맞게 조합합니다.", "accident.html"),
    ]
    cards = "".join(f"""<a class="pcard reveal" href="{h}"><img src="assets/img/{i}" alt="" loading="lazy" width="1600" height="1244">
<div><h3>{esc(t)}</h3><p>{esc(d)}</p><span class="more">자세히 보기 →</span></div></a>""" for i, t, d, h in programs)
    body = f"""
<section class="hero">
  <div class="container hero-grid">
    <div class="hero-copy">
      <span class="eyebrow">서울 은평구 구파발역 인근 한의원</span>
      <h1>진찰은 꼼꼼하게,<br>한약은 <em>원내에서 직접</em> 달입니다</h1>
      <p class="lead">구파발경희한의원은 저칼로리 다이어트, 초음파 가이드 약침, 성장클리닉, 교통사고 후유증 진료를 대표원장 {CLINIC['doctor']}이 직접 살핍니다.</p>
      <div class="btn-row">
        <a class="btn btn-solid" href="{TEL}">☎ 전화 상담 {CLINIC['phone']}</a>
        <a class="btn btn-line" href="reservation.html">온라인 예약</a>
      </div>
      <ul class="hero-chips">
        <li>📍 구파발역 인근</li><li>🕘 평일 저녁 8시까지</li><li>🌿 개별 맞춤 한약</li>
      </ul>
    </div>
    <figure class="hero-img"><img src="assets/img/n-hero.jpg" alt="구파발경희한의원 접수 공간 예시 이미지" width="1600" height="914" fetchpriority="high"></figure>
  </div>
</section>

<section class="quick"><div class="container quick-grid">
  <a href="hours-location.html#hours"><span class="qi">🕘</span><b>진료시간</b><small>월·화·수·금 09:30–20:00<br>목 14:00–20:00 · 토 09:30–13:00</small></a>
  <a href="hours-location.html#map"><span class="qi">📍</span><b>오시는 길</b><small>은평구 진관4로 47<br>708동 상가 115호</small></a>
  <a href="{TEL}"><span class="qi">☎</span><b>전화 상담</b><small>{CLINIC['phone']}</small></a>
  <a href="reservation.html"><span class="qi">📅</span><b>온라인 예약</b><small>초음파 검사·시술은 사전 예약 권장</small></a>
</div></section>

<section class="sec">
  <div class="container">
    <div class="sec-head"><span class="tag">PROGRAMS</span><h2>진료 프로그램</h2><p>구파발경희한의원에서 상담하실 수 있는 진료입니다.</p></div>
    <div class="pgrid">{cards}</div>
    {disclaimer()}
  </div>
</section>

<section class="sec sec-sand">
  <div class="container">
    <div class="sec-head"><span class="tag">PRINCIPLES</span><h2>진료 원칙</h2></div>
    <div class="trio">
      <div class="reveal"><span class="num">01</span><h3>충분히 듣고, 직접 진찰합니다</h3><p>증상뿐 아니라 생활 습관과 걱정까지 듣고, 대표원장이 직접 진찰합니다.</p></div>
      <div class="reveal"><span class="num">02</span><h3>개인별로 구성해 원내에서 달입니다</h3><p>진찰 결과에 맞춰 약재를 구성하고, 한의원 안에서 직접 달여 조제합니다.</p></div>
      <div class="reveal"><span class="num">03</span><h3>영상으로 확인하고 설명드립니다</h3><p>초음파로 부위를 확인하고, 치료 방향과 기간, 관리법을 알기 쉽게 설명드립니다.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="container doc-grid">
    <figure class="doc-photo reveal"><img src="assets/img/doctor.jpg" alt="구파발경희한의원 대표원장 최솔" width="1024" height="1024" loading="lazy"></figure>
    <div class="reveal">
      <span class="tag">DOCTOR</span>
      <h2>대표원장 {CLINIC['doctor']}</h2>
      <p>경희대학교 한의과대학을 졸업하고 횡성군보건소 한방진료과장, 경희대학교 침구경락센터 협력 한의사, 한국한의학연구원 임상연구협력 한의사로 근무했습니다. 초음파 유도하 약침 정규과정을 수료했습니다.</p>
      <ul class="plain"><li>국민건강보험공단 장기요양등급판정위원</li><li>제중학회 학술부회장</li><li>한방비만학회 · 대한스포츠한의학회 회원</li></ul>
      <p><a class="btn btn-line" href="about.html">원장 소개 · 약력 전체 보기</a></p>
    </div>
  </div>
</section>

{faq_block(FAQS[:5])}
<div class="container narrow more-faq"><a class="btn btn-line" href="faq.html">질문 더 보기</a></div>

<section class="sec sec-sand" id="visit">
  <div class="container">
    <div class="sec-head"><span class="tag">VISIT</span><h2>진료시간 · 오시는 길</h2></div>
    <div class="info-grid">
      <div class="panel"><h3>진료시간</h3>
        <table class="hours"><tbody>{hours_rows()}</tbody></table></div>
      <div class="panel"><h3>오시는 길</h3>
        <p class="addr">{CLINIC['address']}</p>
        <p class="muted">지하철 3호선 구파발역 인근</p>
        <div class="btn-row"><a class="btn btn-solid" href="{CLINIC['naver']}" target="_blank" rel="noopener">네이버지도</a><a class="btn btn-line" href="{CLINIC['kakao']}" target="_blank" rel="noopener">카카오맵</a></div>
        <p class="muted">전화 <a href="{TEL}">{CLINIC['phone']}</a></p></div>
    </div>
  </div>
</section>
{cta_band()}
"""
    page("index.html",
         "구파발 한의원 | 구파발경희한의원 – 맞춤 한약·초음파 가이드 약침·성장클리닉",
         "서울 은평구 구파발역 인근 구파발경희한의원. 저칼로리 다이어트 맞춤 한약, N약침, 초음파 가이드 약침, 성장클리닉, 교통사고 후유증 진료. 대표원장 최솔.",
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
  {notice("저칼로리 식단은 모든 분께 적합하지 않습니다. 임신·수유 중이거나, 소아·청소년, 간·신장 질환, 당뇨 등으로 약을 복용 중이시면 반드시 진찰 시 알려 주세요. 감량 폭과 기간은 개인별로 다르며 특정 결과를 약속드리지 않습니다.")}
  {disclaimer()}
</div></section>
{faq_block([FAQS[3], FAQS[4], FAQS[11]], "다이어트 관련 질문")}
{cta_band()}"""
    page("diet.html", "저칼로리 다이어트 한약 | 구파발경희한의원 (은평구)",
         "구파발경희한의원의 저칼로리 다이어트. 저칼로리 식단과 원내에서 직접 달이는 개별 맞춤 한약으로 진행합니다. 진료 전 상담 필수.",
         body, current="diet.html", crumbs=[("홈", ""), ("저칼로리 다이어트", "diet.html")],
         schema=[faq_schema([FAQS[3], FAQS[4], FAQS[11]])], og="n-diet.jpg")


def build_herbal():
    def prod(id_, name, img, tag, lead, herbs, targets, cautions):
        return f"""<article class="prod" id="{id_}">
  <figure><img src="assets/img/{img}" alt="" loading="lazy" width="1600" height="1244"></figure>
  <div>
    <span class="tag">{tag}</span>
    <h2>{name}</h2>
    <p>{lead}</p>
    {('<h3>주요 약재 구성</h3><p class="herbs">' + herbs + '</p>') if herbs else ''}
    <h3>상담이 필요한 경우</h3>
    {checks(targets)}
    <h3>복용 시 참고</h3>
    <p>{cautions}</p>
  </div>
</article>"""
    body = hero_sub("맞춤 한약 · 엔오 시리즈", "맞춤 한약과<br>엔오(NO) 시리즈",
                    "진찰 후 상태에 맞춰 한약을 구성합니다. 보폐고 엔오, 안심환 엔오, 부종환 엔오를 상담하실 수 있습니다.", "n-decoction.jpg") + f"""
<section class="sec"><div class="container narrow prose">
  <p>엔오(NO)는 산화질소(Nitric Oxide)의 약어로, 엔오 시리즈는 한약 처방의 작용을 보조하는 목적으로 구성한 처방입니다. 어떤 처방이 맞는지, 복용량과 기간은 진찰 후 정해 드립니다.</p>
</div></section>
<section class="sec sec-sand"><div class="container prods">
{prod("bopae", "보폐고 엔오", "n-bopae.jpg", "호흡기 · 목 관리",
      "호흡기와 목의 불편감을 관리하기 위한 한약 처방입니다. 영양제처럼 꾸준히 복용하는 방식으로 상담합니다.",
      "길경, 대청엽, 우방자, 금은화, 연교, 죽엽, 포공영, 박하, 오미자, 사삼, 맥문동, 유근피, 산약, 감초, 건강",
      ["만성적인 코막힘, 후비루 등 코·목 불편", "기침과 가래가 오래 가는 경우", "목이 칼칼하거나 쉰 목소리가 잦은 경우", "말을 많이 하는 직업(교사, 강사 등)으로 목 관리가 필요한 경우"],
      "복용 횟수와 기간은 상태에 따라 진찰 후 안내합니다. 위염·식도염이 있어 속쓰림이 나타나면 식후 복용을 상담하세요. 박하(멘톨)에 알레르기가 있으면 복용 전 꼭 알려 주세요.")}
{prod("anshim", "안심환 엔오", "n-anshim.jpg", "긴장 · 스트레스 · 수면",
      "신경과민, 불안, 긴장, 스트레스와 관련된 불편감을 관리하기 위한 한약 처방입니다.",
      "복령, 시호, 황련, 야교등, 백자인, 합환피, 용골, 모려, 산조인, 원지, 석창포, 용안육, 향부자, 조구등, 유근피, 산약, 건강, 후박",
      ["작은 자극에도 예민해지고 긴장이 잘 풀리지 않는 경우", "스트레스로 근육이 굳거나 소화가 불편한 경우", "생각이 많아 잠들기 어렵거나 숙면이 어려운 경우"],
      "복용 초기에 대소변 횟수가 달라지거나 나른할 수 있습니다. 고카페인 식품(커피, 녹차, 홍차, 콜라, 초콜릿, 에너지 음료)은 신경을 예민하게 할 수 있어 줄이시길 권합니다.")}
{prod("bujong", "부종환 엔오", "n-bujong.jpg", "붓기 · 순환 관리",
      "몸이 붓거나 무겁게 느껴지는 불편감을 관리하기 위한 한약 처방입니다.",
      "",
      ["몸이 자주 붓거나 무거운 느낌이 드는 경우", "오래 서 있거나 앉아 있은 뒤 다리가 붓는 경우"],
      "구성 약재와 적합 여부는 진찰 후 안내합니다. 신장·심장 질환이 있으시거나 복용 중인 약이 있으면 반드시 알려 주세요.")}
</div></section>
<section class="sec"><div class="container narrow">{notice("한약은 체질과 상태, 복용 중인 약에 따라 맞지 않을 수 있습니다. 임신·수유 중이시면 반드시 진찰 시 알려 주세요.")}{disclaimer()}</div></section>
{faq_block([FAQS[10], FAQS[4], FAQS[11]], "한약 관련 질문")}
{cta_band()}"""
    page("herbal.html", "맞춤 한약 · 보폐고 안심환 부종환 엔오 | 구파발경희한의원",
         "구파발경희한의원의 맞춤 한약과 엔오(NO) 시리즈 – 보폐고 엔오, 안심환 엔오, 부종환 엔오. 진찰 후 개인별로 안내합니다.",
         body, current="herbal.html", crumbs=[("홈", ""), ("맞춤 한약 · 엔오 시리즈", "herbal.html")],
         schema=[faq_schema([FAQS[10], FAQS[4], FAQS[11]])], og="n-decoction.jpg")


def build_patch():
    body = hero_sub("엔오 리커버리 패치", "엔오 리커버리 패치",
                    "붙여서 사용하는 외용 패치입니다. 사용 부위와 방법은 진찰 후 안내해 드립니다.", "n-patch.jpg") + f"""
<section class="sec"><div class="container narrow prose">
  <h2>엔오 리커버리 패치란?</h2>
  <p>엔오(NO) 처방의 개념을 적용한 외용 패치입니다. 피부에 붙여 사용하며, 몸이 뻐근하거나 회복이 필요한 부위를 관리하는 용도로 상담하실 수 있습니다.</p>
  <h2>이런 경우 상담해 보세요</h2>
  {checks(["운동이나 업무 후 몸이 뻐근하고 회복이 더딘 느낌이 드는 경우", "침·약침 치료와 함께 집에서 관리할 방법이 필요한 경우"])}
  <h2>사용 시 참고</h2>
  <ul class="plain"><li>사용 부위, 시간, 기간은 진찰 후 안내합니다.</li><li>피부가 예민하시거나 붙인 부위에 가려움·발진이 생기면 즉시 떼어 내고 상담해 주세요.</li><li>상처가 있는 피부에는 사용하지 않습니다.</li></ul>
  {notice("효과와 사용감은 개인에 따라 다릅니다. 임신 중이거나 피부 질환이 있으시면 사용 전 진찰 시 알려 주세요.")}
</div></section>
{cta_band()}"""
    page("patch.html", "엔오 리커버리 패치 | 구파발경희한의원",
         "구파발경희한의원의 엔오 리커버리 패치. 붙여서 사용하는 외용 패치로 사용 부위와 방법을 진찰 후 안내합니다.",
         body, current="patch.html", crumbs=[("홈", ""), ("엔오 리커버리 패치", "patch.html")], og="n-patch.jpg")


def build_yakchim():
    body = hero_sub("N약침 · 초음파 가이드 약침", "N약침(엔오약침)과<br>초음파 가이드 약침",
                    "산화질소(NO) 관련 성분을 함유한 약침과, 초음파 영상으로 위치를 확인하며 진행하는 약침 시술을 상담하실 수 있습니다.", "n-nyakchim.jpg") + f"""
<section class="sec" id="n"><div class="container split">
  <figure><img src="assets/img/n-nyakchim.jpg" alt="" loading="lazy" width="1600" height="1244"></figure>
  <div class="prose">
    <span class="tag">N-YAKCHIM</span>
    <h2>N약침 (엔오약침)</h2>
    <p>약침은 한약재에서 추출·정제한 약액을 치료 부위에 주입해 침의 자극과 약물의 작용을 함께 활용하는 치료입니다. N약침은 이 가운데 혈관·신경·림프 등과 관련된 신호전달물질인 <b>산화질소(NO) 관련 성분</b>을 함유한 약침입니다.</p>
    <h3>상담하실 수 있는 증상 예시</h3>
    {checks(["테니스엘보, 오십견, 족저근막염 등 근골격계 통증", "두통, 어지럼, 손발 저림", "수족냉증, 소화 불편, 생리통 등 순환과 관련된 불편"])}
    <p>어떤 약침이 적합한지, 횟수와 간격은 진찰 후 상태에 맞춰 정합니다. 통증에 예민하시면 얇은 바늘을 쓰고 농도를 조절해 진행합니다.</p>
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
<section class="sec"><div class="container narrow">{notice("출혈 경향이 있거나 항응고제를 복용 중이시거나, 임신 중이시거나, 약물 알레르기가 있으시면 시술 전 꼭 알려 주세요.")}{disclaimer()}</div></section>
{faq_block([FAQS[5], FAQS[6], FAQS[2]], "약침 관련 질문")}
{cta_band()}"""
    page("yakchim.html", "N약침(엔오약침) · 초음파 가이드 약침 | 은평구 구파발경희한의원",
         "서울 은평구 구파발경희한의원의 N약침(엔오약침)과 초음파 가이드 약침. 초음파 영상으로 위치를 확인하며 진행하는 약침 시술을 상담합니다.",
         body, current="yakchim.html", crumbs=[("홈", ""), ("N약침 · 초음파 가이드 약침", "yakchim.html")],
         schema=[faq_schema([FAQS[5], FAQS[6], FAQS[2]])], og="n-ultrasound.jpg")


def build_growth():
    four = [("성조숙증 지연", "2차 성징이 일찍 나타나는 경우, 검사 결과를 바탕으로 진행 속도를 살피며 지연 방향의 치료를 상담합니다."),
            ("맞춤 한약", "나이, 성별, 체질, 소화·수면 상태를 고려해 개인별로 한약을 구성합니다."),
            ("성장침", "아이가 받아들일 수 있는 방식으로 성장과 관련된 혈위를 자극하는 침 치료입니다."),
            ("성장 추나", "자세와 척추·골반 균형을 살피는 수기 치료로, 바른 자세 관리를 돕습니다.")]
    fc = "".join(f"<div class='fcard reveal'><h3>{esc(t)}</h3><p>{esc(d)}</p></div>" for t, d in four)
    body = hero_sub("성장클리닉", "초음파 성장 검사와<br>맞춤 성장 상담",
                    "RUF 연골 측정 방식의 초음파 성장 검사를 바탕으로, 나이와 성별에 맞춰 성장 치료를 상담합니다.", "n-growth2.jpg") + f"""
<section class="sec"><div class="container narrow prose">
  <h2>초음파 성장 검사 (RUF 연골 측정 방식)</h2>
  <p>초음파로 성장과 관련된 연골을 측정하는 검사입니다. <b>방사선을 사용하지 않아</b> 아이에게 부담을 줄이고, 필요할 때 경과를 확인하며 반복해서 검사할 수 있습니다. 검사 결과는 성장 상담과 치료 계획을 세우는 참고 자료로 활용합니다.</p>
  <p class="muted">검사 결과가 성장 결과를 보장하거나 예측을 확정하는 것은 아닙니다.</p>
</div></section>
<section class="sec sec-sand"><div class="container">
  <div class="sec-head"><span class="tag">TREATMENT</span><h2>나이별 · 성별 성장 치료</h2><p>아이의 나이와 성별, 성장 단계에 따라 아래 치료를 조합합니다.</p></div>
  <div class="fgrid">{fc}</div>
  <div class="age-grid">
    <div class="panel"><h3>여아</h3><p>일반적으로 만 8세 이전에 가슴 발달 등 2차 성징이 나타나면 성조숙증을 의심해 확인합니다. 초경 시기와 성장 속도를 함께 살펴 상담합니다.</p></div>
    <div class="panel"><h3>남아</h3><p>일반적으로 만 9세 이전에 고환 크기 증가 등 2차 성징이 나타나면 성조숙증을 의심해 확인합니다. 성장 속도와 사춘기 진행 정도를 함께 살펴 상담합니다.</p></div>
  </div>
</div></section>
<section class="sec"><div class="container narrow prose">
  <h2>진행 순서</h2>
  {steps([("상담", "키·체중 기록, 가족력, 식사·수면·운동 습관을 확인합니다."), ("초음파 성장 검사", "RUF 연골 측정 방식으로 검사합니다."), ("결과 상담", "나이·성별·검사 결과를 바탕으로 방향을 설명드립니다."), ("맞춤 치료", "한약, 성장침, 성장 추나 중 필요한 치료를 조합합니다."), ("정기 확인", "성장 속도와 컨디션을 주기적으로 확인합니다.")])}
  {notice("성장에는 유전, 영양, 수면, 운동, 질환 등 여러 요인이 작용합니다. 치료로 키가 얼마나 자랄지 약속드릴 수 없습니다. 검사는 보호자와 함께 내원해 주세요. 검사·시술은 시간이 걸려 사전 예약을 권해 드립니다.")}
  {disclaimer()}
</div></section>
{faq_block([FAQS[7], FAQS[8], FAQS[11]], "성장 관련 질문")}
{cta_band()}"""
    page("growth.html", "성장클리닉 · 초음파 성장 검사 | 구파발경희한의원",
         "구파발경희한의원 성장클리닉. RUF 연골 측정 방식의 초음파 성장 검사와 나이·성별 맞춤 성조숙증 지연, 맞춤한약, 성장침, 성장추나 상담.",
         body, current="growth.html", crumbs=[("홈", ""), ("성장클리닉", "growth.html")],
         schema=[faq_schema([FAQS[7], FAQS[8], FAQS[11]])], og="n-growth2.jpg")


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
{faq_block([FAQS[9], FAQS[6], FAQS[11]], "교통사고 관련 질문")}
{cta_band()}"""
    page("accident.html", "교통사고 후유증 한의원 | 은평구 구파발경희한의원",
         "구파발경희한의원 교통사고 후유증 진료. 침, 부항, 물리치료, 추나요법, 약침, 맞춤 한약을 상태에 맞게 조합합니다. 자동차보험 문의 가능.",
         body, current="accident.html", crumbs=[("홈", ""), ("교통사고 후유증", "accident.html")],
         schema=[faq_schema([FAQS[9], FAQS[6], FAQS[11]])], og="n-accident.jpg")


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
    <p><a class="btn btn-solid" href="{TEL}">☎ {CLINIC['phone']}</a></p></div>
  <div class="panel" id="map"><h3>오시는 길</h3><p class="addr">{CLINIC['address']}</p>
    <p class="muted">지하철 3호선 구파발역 인근 · 708동 상가 1층 115호</p>
    <div class="btn-row"><a class="btn btn-solid" href="{CLINIC['naver']}" target="_blank" rel="noopener">네이버지도</a><a class="btn btn-line" href="{CLINIC['kakao']}" target="_blank" rel="noopener">카카오맵</a></div>
    <p class="muted">주차 가능 여부와 자세한 길 안내는 전화로 문의해 주세요.</p></div>
</div></section>
{faq_block(FAQS[:3], "방문 관련 질문")}
{cta_band()}"""
    page("hours-location.html", "진료시간 · 오시는 길 | 구파발경희한의원 (은평구 진관4로 47)",
         "구파발경희한의원 진료시간과 오시는 길. 서울 은평구 진관4로 47, 708동 상가 115호, 구파발역 인근. 월·화·수·금 09:30–20:00, 목 14:00–20:00, 토 09:30–13:00.",
         body, current="hours-location.html", crumbs=[("홈", ""), ("진료시간 · 오시는 길", "hours-location.html")],
         schema=[faq_schema(FAQS[:3])])


def build_faq():
    body = f"""
<section class="phero phero-plain"><div class="container">{crumb_html("자주 묻는 질문")}<h1>자주 묻는 질문</h1><p class="lead">환자분들이 많이 묻는 질문을 모았습니다.</p></div></section>
{faq_block(FAQS, "전체 질문")}
{cta_band()}"""
    page("faq.html", "자주 묻는 질문 | 구파발경희한의원",
         "구파발경희한의원 자주 묻는 질문 – 진료시간, 위치, 저칼로리 다이어트, N약침, 초음파 가이드 약침, 성장 검사, 교통사고 후유증.",
         body, current="faq.html", crumbs=[("홈", ""), ("자주 묻는 질문", "faq.html")], schema=[faq_schema(FAQS)])


def build_reservation():
    opts = "".join(f"<option>{o}</option>" for o in ["저칼로리 다이어트", "맞춤 한약 · 엔오 시리즈", "엔오 리커버리 패치", "N약침 · 초음파 가이드 약침", "성장클리닉 · 초음파 성장 검사", "교통사고 후유증", "기타 상담"])
    body = f"""
<section class="phero phero-plain"><div class="container">{crumb_html("예약 · 문의")}<h1>예약 · 문의</h1><p class="lead">전화가 가장 빠릅니다. 아래 양식으로도 문의하실 수 있습니다.</p></div></section>
<section class="sec"><div class="container info-grid">
  <div class="panel"><h3>문의 양식</h3>
    <form class="rsv" id="rsvForm">
      <div class="row2"><div class="field"><label for="n">성함</label><input id="n" required autocomplete="name"></div><div class="field"><label for="p">연락처</label><input id="p" type="tel" required autocomplete="tel" placeholder="010-0000-0000"></div></div>
      <div class="row2"><div class="field"><label for="d">희망 일자</label><input id="d" type="date"></div><div class="field"><label for="s">관심 진료</label><select id="s">{opts}</select></div></div>
      <div class="field"><label for="m">문의 내용</label><textarea id="m" rows="4"></textarea></div>
      <label class="agree"><input type="checkbox" required> 개인정보 수집·이용에 동의합니다. (<a href="privacy.html">내용 보기</a>)</label>
      <button class="btn btn-solid" type="submit">문의하기</button>
      <div class="form-msg" id="formMsg" role="status"></div>
    </form></div>
  <div class="panel"><h3>전화 상담</h3><p class="bigtel"><a href="{TEL}">{CLINIC['phone']}</a></p>
    <table class="hours"><tbody>{hours_rows()}</tbody></table>
    <p class="muted">초음파 가이드 약침과 초음파 성장 검사는 사전 예약을 권해 드립니다.</p></div>
</div></section>"""
    page("reservation.html", "예약 · 문의 | 구파발경희한의원",
         "구파발경희한의원 예약·문의. 전화 02-355-4517 또는 온라인 문의. 초음파 가이드 약침·성장 검사는 사전 예약 권장.",
         body, current="reservation.html", crumbs=[("홈", ""), ("예약 · 문의", "reservation.html")])


def build_privacy():
    body = f"""
<section class="phero phero-plain"><div class="container">{crumb_html("개인정보처리방침")}<h1>개인정보처리방침</h1></div></section>
<section class="sec"><div class="container narrow prose">
  <p>{CLINIC['name']}은 예약·상담 접수를 위해 최소한의 개인정보(성함, 연락처, 문의 내용)를 수집하며, 목적 달성 후 지체 없이 파기합니다.</p>
  <h2>1. 수집 항목 및 목적</h2><ul><li>성함, 연락처: 예약 확인 및 상담 회신</li><li>문의 내용: 진료 상담</li></ul>
  <h2>2. 보유 기간</h2><p>상담 완료 후 [기간 입력]까지 보관 후 파기합니다.</p>
  <h2>3. 문의</h2><p>개인정보 관련 문의: <a href="{TEL}">{CLINIC['phone']}</a></p>
  <p class="muted">※ 임시 문안입니다. 시행 전 법률 기준에 맞는 실제 방침으로 교체해 주세요.</p>
</div></section>"""
    page("privacy.html", "개인정보처리방침 | 구파발경희한의원", "구파발경희한의원 개인정보처리방침.", body, crumbs=[("홈", ""), ("개인정보처리방침", "privacy.html")])


def build_404():
    body = f"""<section class="sec"><div class="container narrow center"><p class="big404">404</p><h1>페이지를 찾을 수 없습니다</h1><p class="lead">주소가 바뀌었거나 삭제된 페이지입니다.</p><p><a class="btn btn-solid" href="/index.html">홈으로 가기</a></p></div></section>"""
    page("404.html", "페이지를 찾을 수 없습니다 | 구파발경희한의원", "요청하신 페이지를 찾을 수 없습니다.", body)


PAGES = ["index.html", "diet.html", "herbal.html", "patch.html", "yakchim.html", "growth.html", "accident.html",
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
- [맞춤 한약 · 엔오 시리즈]({DOMAIN}/herbal.html): 보폐고 엔오, 안심환 엔오, 부종환 엔오
- [엔오 리커버리 패치]({DOMAIN}/patch.html)
- [N약침 · 초음파 가이드 약침]({DOMAIN}/yakchim.html)
- [성장클리닉 · 초음파 성장 검사]({DOMAIN}/growth.html): RUF 연골 측정 방식, 성조숙증 지연·맞춤한약·성장침·성장추나
- [교통사고 후유증]({DOMAIN}/accident.html): 침, 부항, 물리치료, 추나요법, 약침, 맞춤 한약

## 기타
- [원장 소개]({DOMAIN}/about.html)
- [진료시간 · 오시는 길]({DOMAIN}/hours-location.html)
- [자주 묻는 질문]({DOMAIN}/faq.html)

치료 효과와 경과는 개인에 따라 다를 수 있으며, 본 정보는 진찰을 대신하지 않습니다.
"""
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write(llms)


if __name__ == "__main__":
    for fn in (build_home, build_diet, build_herbal, build_patch, build_yakchim, build_growth, build_accident,
               build_about, build_visit, build_faq, build_reservation, build_privacy, build_404, build_meta):
        fn()
    print("built", len(PAGES) + 1, "pages")
