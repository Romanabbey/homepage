#!/bin/bash
# 오늘 자 생활 날씨가 아직 없으면 data/weather-trigger.txt 를 푸시해 GitHub Actions 를 바로 실행시킨다.
# 이 맥의 launchd(com.gupabal.weather-trigger)가 매일 아침 호출한다. 비밀키는 쓰지 않는다.
set -u
today=$(TZ=Asia/Seoul date +%F)
if [ "${1:-}" != "--force" ] && curl -fsS --max-time 20 "https://gupabalhani.org/data/weather.json?t=$(date +%s)" | grep -q "\"date\": \"$today\""; then
  echo "$(date '+%F %T') 오늘($today) 자료가 이미 있어 건너뜀"; exit 0
fi
cd "$(dirname "$0")/.." || exit 1
git pull -q --no-rebase origin main || exit 1
echo "$(date '+%F %T')" > data/weather-trigger.txt
git add data/weather-trigger.txt
git commit -qm "날씨 갱신 요청 $today" || exit 0
git push -q origin main && echo "$(date '+%F %T') 갱신 요청 푸시 완료"
