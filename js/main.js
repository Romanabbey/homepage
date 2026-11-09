/* 내용(전화·진료시간 등)은 모두 HTML에 들어 있고, 이 스크립트는 동작만 담당합니다. */
(function () {
  document.documentElement.classList.add("js");

  // 모바일 메뉴 (전체 화면 오버레이)
  var burger = document.getElementById("burger");
  var nav = document.getElementById("mainnav");
  function setMenu(open) {
    if (!burger || !nav) return;
    nav.classList.toggle("open", open);
    burger.setAttribute("aria-expanded", open ? "true" : "false");
    burger.setAttribute("aria-label", open ? "메뉴 닫기" : "메뉴 열기");
    document.body.classList.toggle("menu-open", open);
  }
  if (burger && nav) {
    burger.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
    window.addEventListener("resize", function () { if (window.innerWidth > 920) setMenu(false); });
  }

  // 오늘 진료 여부 (한국 시간 기준)
  var SCHEDULE = { // 요일 0=일 … 6=토, [시작분, 종료분] 목록
    1: [[570, 750], [840, 1200]], 2: [[570, 750], [840, 1200]], 3: [[570, 750], [840, 1200]],
    4: [[840, 1200]], 5: [[570, 750], [840, 1200]], 6: [[570, 780]], 0: []
  };
  var LABEL = { 1: 0, 2: 0, 3: 0, 5: 0, 4: 1, 6: 2, 0: 3 };
  try {
    var now = new Date(new Date().toLocaleString("en-US", { timeZone: "Asia/Seoul" }));
    var d = now.getDay(), m = now.getHours() * 60 + now.getMinutes();
    var spans = SCHEDULE[d] || [];
    var open = spans.some(function (s) { return m >= s[0] && m < s[1]; });
    var el = document.getElementById("openNow");
    if (el) {
      if (!spans.length) el.textContent = "오늘 휴진";
      else if (open) el.textContent = "지금 진료 중";
      else if (m < spans[0][0]) el.textContent = "오늘 진료 예정";
      else if (m >= spans[spans.length - 1][1]) el.textContent = "오늘 진료 종료";
      else el.textContent = "점심시간";
    }
    document.querySelectorAll("table.hours tbody").forEach(function (tb) {
      var tr = tb.children[LABEL[d]];
      if (tr) tr.classList.add("today");
    });
  } catch (e) { /* 지원하지 않는 브라우저에서는 생략 */ }


  // 홈: 스크롤하면 헤더를 아이보리 바탕으로
  var hdr = document.querySelector(".site-header");
  if (hdr && document.body.classList.contains("home")) {
    var onS = function () { hdr.classList.toggle("scrolled", window.scrollY > 40); };
    window.addEventListener("scroll", onS, { passive: true }); onS();
  }

  // 맨 위로
  var top = document.getElementById("toTop");
  if (top) {
    window.addEventListener("scroll", function () { top.classList.toggle("show", window.scrollY > 500); }, { passive: true });
    top.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
  }

  // 스크롤 등장 효과
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: .1 });
    items.forEach(function (el) { io.observe(el); });
  } else { items.forEach(function (el) { el.classList.add("in"); }); }
})();
