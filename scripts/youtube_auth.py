#!/usr/bin/env python3
"""유튜브 연동 허가(한 번만): python3 scripts/youtube_auth.py
- ~/.config/youtube-client.json(구글 클라우드 데스크톱 앱 열쇠)을 읽어 크롬에서 허가 화면을 연다.
- 허가가 끝나면 ~/.config/youtube-token.json(권한 600)에 갱신용 토큰을 저장한다. 값은 화면에 출력하지 않는다.
- 외부 라이브러리 없이 표준 라이브러리만 쓴다.
"""
import http.server, json, os, secrets, subprocess, sys, threading, time, urllib.parse, urllib.request

CLIENT = os.path.expanduser("~/.config/youtube-client.json")
TOKEN = os.path.expanduser("~/.config/youtube-token.json")
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]


def load_client():
    d = json.load(open(CLIENT, encoding="utf-8"))
    return d["installed"]


def post(url, data):
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(), method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def authorize():
    c = load_client()
    state = secrets.token_urlsafe(16)
    box = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if q.get("state", [""])[0] == state and "code" in q:
                box["code"] = q["code"][0]
                msg = "허가가 완료되었습니다. 이 창을 닫고 Claude 화면으로 돌아가세요."
            else:
                box["error"] = q.get("error", ["unknown"])[0]
                msg = "허가가 취소되었거나 실패했습니다: " + box["error"]
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
            self.wfile.write(f"<meta charset=utf-8><body style='font:20px sans-serif;padding:40px'>{msg}</body>".encode())

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    port = srv.server_address[1]
    redirect = f"http://127.0.0.1:{port}"
    url = c["auth_uri"] + "?" + urllib.parse.urlencode({
        "client_id": c["client_id"], "redirect_uri": redirect, "response_type": "code",
        "scope": " ".join(SCOPES), "access_type": "offline", "prompt": "consent", "state": state})
    threading.Thread(target=srv.handle_request, daemon=True).start()
    print("허가 화면을 엽니다(크롬). 채널 계정을 고르고 허용을 눌러 주세요.", flush=True)
    subprocess.run(["open", "-a", "Google Chrome", url])
    t0 = time.time()
    while "code" not in box and "error" not in box and time.time() - t0 < 300:
        time.sleep(0.5)
    if "code" not in box:
        print("허가 실패 또는 시간 초과:", box.get("error", "timeout")); sys.exit(1)
    tok = post(c["token_uri"], {"code": box["code"], "client_id": c["client_id"], "client_secret": c["client_secret"],
                                "redirect_uri": redirect, "grant_type": "authorization_code"})
    if "refresh_token" not in tok:
        print("갱신 토큰을 받지 못했습니다:", {k: v for k, v in tok.items() if k not in ("access_token", "id_token")}); sys.exit(1)
    tok["obtained_at"] = int(time.time())
    fd = os.open(TOKEN, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(tok, f)
    print("✅ 허가 완료. 토큰을 ~/.config/youtube-token.json 에 저장했습니다(권한 600). 범위:", tok.get("scope"))


def access_token():
    """저장된 갱신 토큰으로 새 액세스 토큰을 받는다."""
    c = load_client(); t = json.load(open(TOKEN, encoding="utf-8"))
    r = post(c["token_uri"], {"client_id": c["client_id"], "client_secret": c["client_secret"],
                              "refresh_token": t["refresh_token"], "grant_type": "refresh_token"})
    return r["access_token"]


if __name__ == "__main__":
    authorize()
