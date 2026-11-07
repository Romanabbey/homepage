/* 한의원 정보 단일 소스 — 여기만 수정하면 모든 페이지에 반영됩니다.
   [수정 필요] 표시된 값은 임시(placeholder)입니다. */
window.CLINIC = {
  name: "구파발경희한의원",
  doctor: "최솔",
  address: "서울 은평구 진관4로 47, 708동 상가 115호",
  phone: "02-000-0000",            // [수정 필요] 실제 전화번호
  bizNo: "000-00-00000",           // [수정 필요] 사업자등록번호
  hours: [                         // [수정 필요] 실제 진료시간
    { day: "월 · 화 · 목 · 금", time: "09:30 – 18:30" },
    { day: "수", time: "09:30 – 20:00 (야간진료)" },
    { day: "토", time: "09:30 – 14:00" },
    { day: "일 · 공휴일", time: "휴진" }
  ],
  lunch: "점심시간 13:00 – 14:00",  // [수정 필요]
  naverMap: "https://map.naver.com/p/search/" + encodeURIComponent("서울 은평구 진관4로 47"),
  kakaoMap: "https://map.kakao.com/?q=" + encodeURIComponent("서울 은평구 진관4로 47"),
  sns: { blog: "#", instagram: "#", kakao: "#" } // [수정 필요]
};
