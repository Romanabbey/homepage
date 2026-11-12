#!/usr/bin/env python3
"""유튜브 업로드: python3 scripts/youtube_upload.py <spec.json>
spec 예: {"video": "...mp4", "thumbnail": "...png", "title": "...", "description": "...", "tags": ["..."],
          "privacy": "private", "category": "27", "synthetic": true, "playlist": "호흡기 건강 이야기"}
- 표준 라이브러리만 사용. 토큰은 scripts/youtube_auth.py 가 만든 ~/.config/youtube-token.json.
- 기본은 비공개(private). 공개 전환은 원장이 스튜디오에서 하거나, 따로 요청한다.
"""
import json, os, sys, urllib.error, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import youtube_auth as ya

API = "https://www.googleapis.com/youtube/v3"


def call(method, url, tok, body=None, headers=None, raw=None):
    h = {"Authorization": "Bearer " + tok}
    h.update(headers or {})
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    if body is not None:
        h["Content-Type"] = "application/json; charset=UTF-8"
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        r = urllib.request.urlopen(req, timeout=600)
        return r.status, r.headers, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read()


def upload(spec):
    tok = ya.access_token()
    path = spec["video"]; size = os.path.getsize(path)
    meta = {
        "snippet": {"title": spec["title"], "description": spec["description"], "tags": spec.get("tags", []),
                    "categoryId": spec.get("category", "27"), "defaultLanguage": "ko", "defaultAudioLanguage": "ko"},
        "status": {"privacyStatus": spec.get("privacy", "private"), "selfDeclaredMadeForKids": False,
                   "containsSyntheticMedia": bool(spec.get("synthetic", True)), "embeddable": True, "publicStatsViewable": True},
    }
    s, h, b = call("POST", "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status", tok,
                   body=meta, headers={"X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
    if s != 200:
        print("업로드 시작 실패", s, b.decode()[:500]); sys.exit(1)
    loc = h["Location"]
    print(f"업로드 중… {size/1e6:.1f}MB", flush=True)
    with open(path, "rb") as f:
        s, h, b = call("PUT", loc, tok, raw=f.read(), headers={"Content-Type": "video/mp4"})
    if s not in (200, 201):
        print("업로드 실패", s, b.decode()[:500]); sys.exit(1)
    vid = json.loads(b)["id"]
    print("✅ 영상 업로드 완료:", vid, "| 상태:", json.loads(b)["status"].get("privacyStatus"), flush=True)
    if spec.get("thumbnail"):
        with open(spec["thumbnail"], "rb") as f:
            s, h, b = call("POST", f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}", tok,
                           raw=f.read(), headers={"Content-Type": "image/png"})
        print("썸네일:", "완료" if s == 200 else f"실패 {s} {b.decode()[:300]}", flush=True)
    if spec.get("playlist"):
        s, h, b = call("GET", API + "/playlists?part=snippet&mine=true&maxResults=50", tok)
        pid = next((it["id"] for it in json.loads(b).get("items", []) if it["snippet"]["title"] == spec["playlist"]), None)
        if not pid:
            s, h, b = call("POST", API + "/playlists?part=snippet,status", tok,
                           body={"snippet": {"title": spec["playlist"], "description": spec.get("playlist_desc", ""), "defaultLanguage": "ko"},
                                 "status": {"privacyStatus": "public"}})
            pid = json.loads(b).get("id")
            print("재생목록 만듦:", spec["playlist"], pid, flush=True)
        s, h, b = call("POST", API + "/playlistItems?part=snippet", tok,
                       body={"snippet": {"playlistId": pid, "resourceId": {"kind": "youtube#video", "videoId": vid}}})
        print("재생목록 추가:", "완료" if s == 200 else f"실패 {s} {b.decode()[:300]}", flush=True)
    print("스튜디오:", f"https://studio.youtube.com/video/{vid}/edit")
    return vid


if __name__ == "__main__":
    upload(json.load(open(sys.argv[1], encoding="utf-8")))
