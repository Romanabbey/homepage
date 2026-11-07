(function () {
  var C = window.CLINIC;
  var tel = "tel:" + C.phone.replace(/[^0-9+]/g, "");

  var logoSvg =
    '<svg class="logo-mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="#1560d8"/>' +
    '<path d="M20 9c-5 5-7 9-7 13a7 7 0 0014 0c0-4-2-8-7-13z" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"/>' +
    '<path d="M20 17v12M15 24h10" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>';

  var header =
    '<div class="topbar"><div class="container"><span class="hide-m">' + C.address + '</span>' +
    '<span><a href="' + tel + '">☎ ' + C.phone + '</a> &nbsp;·&nbsp; <a href="hours-location.html">진료시간</a></span></div></div>' +
    '<div class="container nav-wrap">' +
    '<a class="logo" href="index.html" aria-label="' + C.name + ' 홈">' + logoSvg +
    '<span>' + C.name + '<small>Gupabal Kyunghee Korean Medicine Clinic</small></span></a>' +
    '<ul class="gnb" id="gnb">' +
    '<li><a href="about.html">한의원소개</a><div class="mega"><a href="about.html">원장 인사말</a><a href="about.html#philosophy">진료 철학</a><a href="hours-location.html">오시는 길</a></div></li>' +
    '<li><a href="treatments.html">진료과목</a><div class="mega"><a href="treatments.html#spine">척추·관절</a><a href="treatments.html#accident">교통사고 후유증</a><a href="treatments.html#women">여성질환</a><a href="treatments.html#digest">소화기·비염</a></div></li>' +
    '<li><a href="treatments.html#methods">치료법</a><div class="mega"><a href="treatments.html#chuna">추나요법</a><a href="treatments.html#acu">침·약침</a><a href="treatments.html#herb">한약·보약</a><a href="treatments.html#cupping">부항·뜸</a></div></li>' +
    '<li><a href="hours-location.html">진료안내</a><div class="mega"><a href="hours-location.html#hours">진료시간</a><a href="hours-location.html#map">오시는 길</a><a href="reservation.html#faq">자주 묻는 질문</a></div></li>' +
    '<li><a href="notice.html">커뮤니티</a><div class="mega"><a href="notice.html">공지사항</a><a href="notice.html#health">건강정보</a></div></li>' +
    '<li><a href="reservation.html">예약·문의</a></li></ul>' +
    '<a class="cta-btn nav-cta" href="reservation.html">온라인 예약</a>' +
    '<button class="burger" id="burger" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button></div>';

  var footer =
    '<div class="container"><div class="foot-top"><div class="foot-links">' +
    '<a href="about.html">한의원소개</a><a href="treatments.html">진료과목</a><a href="hours-location.html">오시는 길</a><a href="notice.html">공지사항</a><a href="privacy.html">개인정보처리방침</a></div>' +
    '<div class="foot-sns"><a href="' + C.sns.blog + '">블로그</a><a href="' + C.sns.instagram + '">인스타그램</a><a href="' + C.sns.kakao + '">카카오톡</a></div></div>' +
    '<address><strong>' + C.name + '</strong><br>대표원장 ' + C.doctor + ' · 사업자등록번호 ' + C.bizNo + '<br>' +
    C.address + '<br>TEL ' + C.phone + '</address>' +
    '<p style="margin-top:14px;font-size:12.5px">본 사이트의 내용은 일반적인 건강 정보이며 개인별 진단·치료를 대신하지 않습니다. 정확한 진료는 내원 상담을 통해 받으시기 바랍니다.</p>' +
    '<p style="margin-top:10px;font-size:12.5px">© ' + new Date().getFullYear() + ' ' + C.name + '. All rights reserved.</p></div>';

  var fixed =
    '<div class="fixed-bar"><a class="call" href="' + tel + '">☎ 전화 상담</a><a class="rsv" href="reservation.html">📅 온라인 예약</a></div>' +
    '<button class="to-top" id="toTop" aria-label="맨 위로">↑</button>';

  var h = document.getElementById("site-header"); if (h) h.innerHTML = header;
  var f = document.getElementById("site-footer"); if (f) f.innerHTML = footer;
  document.body.insertAdjacentHTML("beforeend", fixed);

  // 설정값 주입: <span data-c="phone"> 등
  document.querySelectorAll("[data-c]").forEach(function (el) {
    var k = el.getAttribute("data-c"); if (C[k]) el.textContent = C[k];
  });
  document.querySelectorAll("[data-hours]").forEach(function (el) {
    el.innerHTML = C.hours.map(function (r) { return "<tr><td>" + r.day + "</td><td>" + r.time + "</td></tr>"; }).join("");
  });
  document.querySelectorAll("[data-href]").forEach(function (el) {
    var k = el.getAttribute("data-href"); el.href = k === "tel" ? tel : C[k];
  });

  // 모바일 메뉴
  var burger = document.getElementById("burger"), gnb = document.getElementById("gnb");
  if (burger) burger.addEventListener("click", function () {
    var o = gnb.classList.toggle("open");
    burger.setAttribute("aria-expanded", o);
  });

  // 히어로 슬라이더
  var slides = document.getElementById("slides");
  if (slides) {
    var n = slides.children.length, i = 0, timer;
    var dots = document.getElementById("dots");
    for (var d = 0; d < n; d++) {
      var b = document.createElement("button"); b.setAttribute("aria-label", (d + 1) + "번 슬라이드");
      (function (d) { b.onclick = function () { go(d, true); }; })(d);
      dots.appendChild(b);
    }
    function go(k, user) {
      i = (k + n) % n;
      slides.style.transform = "translateX(-" + i * 100 + "%)";
      [].forEach.call(dots.children, function (x, j) { x.classList.toggle("on", j === i); });
      if (user) restart();
    }
    function restart() { clearInterval(timer); timer = setInterval(function () { go(i + 1); }, 5500); }
    document.getElementById("prev").onclick = function () { go(i - 1, true); };
    document.getElementById("next").onclick = function () { go(i + 1, true); };
    go(0); restart();
  }

  // 스크롤: TOP 버튼 + reveal
  var top = document.getElementById("toTop");
  window.addEventListener("scroll", function () { top.classList.toggle("show", window.scrollY > 500); }, { passive: true });
  top.onclick = function () { window.scrollTo({ top: 0, behavior: "smooth" }); };
  var io = "IntersectionObserver" in window && new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { threshold: .12 });
  document.querySelectorAll(".reveal").forEach(function (el) { io ? io.observe(el) : el.classList.add("in"); });

  // 예약 폼 (서버 없음: 입력 확인 후 전화/문자 안내)
  var form = document.getElementById("rsvForm");
  if (form) form.addEventListener("submit", function (e) {
    e.preventDefault();
    var m = document.getElementById("formMsg");
    m.style.display = "block";
    m.textContent = "접수 요청이 확인되었습니다. 현재 온라인 접수는 준비 중이므로 " + C.phone + " 로 전화 주시면 빠르게 예약을 도와드립니다.";
  });
})();
