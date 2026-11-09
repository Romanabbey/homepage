#!/usr/bin/env python3
"""매일 아침 날씨 한 줄을 data/weather.json 에 추가합니다.
키는 환경변수 DATA_GO_KR_KEY (공공데이터포털 일반 인증키)로만 받습니다. 파일에 저장하지 않습니다.
  - 기상청 단기예보 (VilageFcstInfoService_2.0/getVilageFcst), 격자 nx=59, ny=128 (구파발역 인근)
  - 에어코리아 측정소 '은평구' 실시간 측정값 (ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty)
사용: DATA_GO_KR_KEY=... python3 scripts/update_weather.py
"""
import os, sys, json, random, datetime, urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEATHER = os.path.join(ROOT, "data", "weather.json")
PHRASES = os.path.join(ROOT, "data", "weather_phrases.json")
KST = datetime.timezone(datetime.timedelta(hours=9))
NX, NY, STATION = 59, 128, "은평구"
GRADE = {"1": "좋음", "2": "보통", "3": "나쁨", "4": "매우나쁨"}
PTY = {"1": "비", "2": "비/눈", "3": "눈", "4": "소나기"}
SKY = {"1": "맑음", "3": "구름많음", "4": "흐림"}
PRIORITY = ["rain", "dust", "diurnal", "cold", "hot", "clear", "default"]
WINDOW = 14  # 이 기간(일) 안에 쓴 문구는 다시 쓰지 않음


def get(url, params):
    q = urllib.parse.urlencode(params)
    with urllib.request.urlopen(url + "?" + q, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def base_time(now):
    """발표 시각(0200,0500,...,2300) 중 지금 받을 수 있는 가장 최근 것 (발표 후 약 20분 뒤 제공)."""
    t = now - datetime.timedelta(minutes=20)
    hours = [h for h in (2, 5, 8, 11, 14, 17, 20, 23) if h <= t.hour]
    if hours:
        return t.strftime("%Y%m%d"), "%02d00" % hours[-1]
    y = t - datetime.timedelta(days=1)
    return y.strftime("%Y%m%d"), "2300"


def forecast(key, today, now):
    bdate, btime = base_time(now)
    d = get("http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst",
            {"serviceKey": key, "pageNo": 1, "numOfRows": 1000, "dataType": "JSON",
             "base_date": bdate, "base_time": btime, "nx": NX, "ny": NY})
    if "body" not in d.get("response", {}):
        raise RuntimeError("예보 응답 이상: " + json.dumps(d, ensure_ascii=False)[:200])
    items = d["response"]["body"]["items"]["item"]
    t = [i for i in items if i["fcstDate"] == today]
    def vals(cat, lo=0, hi=2400):
        return [(i["fcstTime"], i["fcstValue"]) for i in t if i["category"] == cat and lo <= int(i["fcstTime"]) <= hi]
    tmp = [float(v) for _, v in vals("TMP")]
    tmn = [float(v) for _, v in vals("TMN")] or tmp
    tmx = [float(v) for _, v in vals("TMX")] or tmp
    pop = [int(v) for _, v in vals("POP")]
    pty = [v for _, v in vals("PTY", 600, 2100) if v != "0"]
    sky = [v for _, v in vals("SKY", 900, 1800)]
    if not tmn or not tmx:
        raise RuntimeError("예보에서 기온을 찾지 못했습니다")
    if pty:
        codes = sorted(set(pty))
        label = PTY.get(codes[0]) if len(codes) == 1 else "비/눈" if set(codes) & {"2", "3"} else "비"
    else:
        label = SKY.get(max(set(sky), key=sky.count), "흐림") if sky else "흐림"
    return {"sky": label, "precip": bool(pty), "tmn": round(min(tmn)), "tmx": round(max(tmx)),
            "pop": max(pop) if pop else 0}


def air(key):
    d = get("http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty",
            {"serviceKey": key, "stationName": STATION, "returnType": "json", "numOfRows": 1,
             "pageNo": 1, "dataTerm": "DAILY", "ver": "1.3"})
    items = d["response"]["body"]["items"]
    if not items:
        return {"pm10": None, "pm25": None}
    it = items[0]
    g10 = it.get("pm10Grade1h") or it.get("pm10Grade")
    g25 = it.get("pm25Grade1h") or it.get("pm25Grade")
    return {"pm10": GRADE.get(str(g10)) if g10 else None, "pm25": GRADE.get(str(g25)) if g25 else None}


def category(w, a):
    bad = {"나쁨", "매우나쁨"}
    if w["precip"]:
        return "rain"
    if a["pm10"] in bad or a["pm25"] in bad:
        return "dust"
    if w["tmx"] - w["tmn"] >= 10:
        return "diurnal"
    if w["tmn"] <= 0:
        return "cold"
    if w["tmx"] >= 30:
        return "hot"
    if w["sky"] == "맑음" and a["pm10"] == "좋음" and a["pm25"] in (None, "좋음", "보통"):
        return "clear"
    return "default"


def pick(cat, today, history, pool):
    start = (datetime.datetime.strptime(today, "%Y%m%d") - datetime.timedelta(days=WINDOW)).strftime("%Y-%m-%d")
    day = "%s-%s-%s" % (today[:4], today[4:6], today[6:])
    recent = {h["phrase"]: h["date"] for h in history if h["date"] != day and h["date"] >= start}
    fresh = [p for p in pool[cat] if p not in recent]
    if fresh:
        return random.Random(today + cat).choice(fresh)
    # 모두 최근에 썼다면 가장 오래전에 쓴 문구 (이때만 겹칠 수 있음)
    return min(pool[cat], key=lambda p: recent.get(p, ""))


def main():
    key = os.environ.get("DATA_GO_KR_KEY", "").strip()
    if not key:
        sys.exit("DATA_GO_KR_KEY 환경변수가 없습니다")
    now = datetime.datetime.now(KST)
    today = now.strftime("%Y%m%d")
    w = forecast(key, today, now)
    try:
        a = air(key)
    except Exception as e:  # 대기 정보만 실패하면 날씨 줄은 올림
        print("대기 정보 실패:", e, file=sys.stderr)
        a = {"pm10": None, "pm25": None}
    pool = json.load(open(PHRASES, encoding="utf-8"))
    history = json.load(open(WEATHER, encoding="utf-8")) if os.path.exists(WEATHER) else []
    cat = category(w, a)
    phrase = pick(cat, today, history, pool)
    day = now.strftime("%Y-%m-%d")
    entry = {"date": day, **w, "pm10": a["pm10"], "pm25": a["pm25"], "category": cat, "phrase": phrase}
    history = [h for h in history if h["date"] != day] + [entry]
    history.sort(key=lambda h: h["date"])
    os.makedirs(os.path.dirname(WEATHER), exist_ok=True)
    json.dump(history, open(WEATHER, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("OK", json.dumps(entry, ensure_ascii=False))


if __name__ == "__main__":
    main()
