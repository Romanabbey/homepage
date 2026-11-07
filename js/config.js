/* 한의원 정보 단일 소스 — 여기만 수정하면 모든 페이지에 반영됩니다.
   [수정 필요] 표시된 값은 임시(placeholder)입니다. */
window.CLINIC = {
  name: "구파발경희한의원",
  doctor: "최솔",
  address: "서울 은평구 진관4로 47, 708동 상가 115호",
  phone: "02-355-4517",
  bizNo: "218-90-15783",
  hours: [
    { day: "월 · 화 · 목 · 금", time: "09:30 – 20:00" },
    { day: "수", time: "14:00 – 20:00" },
    { day: "토", time: "09:30 – 13:00 (점심시간 없음)" },
    { day: "일 · 공휴일", time: "휴진" }
  ],
  lunch: "점심시간 12:30 – 14:00 (월~금, 토요일은 점심시간 없음)",
  naverMap: "https://map.naver.com/p/search/" + encodeURIComponent("서울 은평구 진관4로 47"),
  kakaoMap: "https://map.kakao.com/?q=" + encodeURIComponent("서울 은평구 진관4로 47"),
  sns: { blog: "#", instagram: "#", kakao: "#" } // [수정 필요]
};
