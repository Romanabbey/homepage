#!/usr/bin/env python3
"""네이버 블로그 복사용 페이지 만들기.
사용: python3 blog_kit.py blog_out/글이름.txt [이미지폴더]
초안 형식: [제목] [본문] [참고 문헌] [맺음 안내] [추천 태그] 구역, 본문 안에 {{img:파일이름.png}} 로 이미지 위치 표시.
결과: 같은 폴더에 글이름-copy.html 생성, 이미지는 ~/Downloads/블로그이미지/글이름/ 에 복사 후 폴더를 엽니다."""
import json, sys, os, re, html, shutil, subprocess, base64

src_path = sys.argv[1]
base = os.path.splitext(os.path.basename(src_path))[0]
img_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(src_path) or ".", "images")
src = open(src_path, encoding="utf-8").read()

def sec(name):
    m = re.search(r"\[" + name + r"\]\n(.*?)(?=\n\[[^\]\n]+\]\n|\Z)", src, re.S)
    return m.group(1).strip("\n") if m else ""

title, body, refs, end, tags = (sec(n) for n in ("제목", "본문", "참고 문헌", "맺음 안내", "추천 태그"))
title = title.strip()

def link(t):
    t = html.escape(t)
    return re.sub(r"(https?://[^\s<]+)", r'<a href="\1">\1</a>', t)

def para(blk):
    return "<p>" + "<br>".join(link(l) for l in blk.split("\n")) + "</p>"

IMGS = []   # (파일명, base64) 순서대로

def img(name):
    """본문에는 '[이미지 n 자리]' 표시만 넣고, 실제 이미지는 위쪽 '이미지 복사' 버튼으로 붙여넣습니다."""
    p = os.path.join(img_dir, name)
    if not os.path.exists(p):
        return f"<p style='color:#c00'>[이미지 없음: {html.escape(name)}]</p>"
    if name not in [n for n, _ in IMGS]:
        IMGS.append((name, base64.b64encode(open(p, "rb").read()).decode()))
    n = [x for x, _ in IMGS].index(name) + 1
    return f'<p style="margin:0;font-size:15px;line-height:1.8;text-align:center;color:#000"><b>[이미지 {n} 자리]</b></p>'

P = 'margin:0;font-size:15px;line-height:1.8;color:#000'
PH = 'margin:0;font-size:24px;line-height:1.6;font-weight:700;color:#000'
Q = 'background:#f3f6f4;border-left:4px solid #1d6a4a;padding:14px 18px;margin:0;border-radius:6px'
used = []

def inline(t):
    """'이름: 주소' 줄은 이름 글자에만 링크를 걸고 주소 글자는 보이지 않게 합니다."""
    m = re.fullmatch(r"(.*?)\s*:\s*(https?://\S+)", t)
    if m:
        return f'<a href="{m.group(2)}">{html.escape(m.group(1))}</a>'
    return link(t)

def line(t):
    if not t.strip():
        return f'<p style="{P}"><br></p>'
    return f'<p style="{P}">{inline(t)}</p>'

def render(text):
    """줄 단위로 네이버 에디터 문단 구조(한 줄 = 한 문단, 빈 줄 = 빈 문단)에 맞춰 만듭니다."""
    lines = text.strip("\n").split("\n")
    out = []
    i = 0
    prev_heading = False
    while i < len(lines):
        t = lines[i]
        m = re.fullmatch(r"\{\{img:(.+?)\}\}", t.strip())
        if m:
            used.append(m.group(1)); out.append(img(m.group(1))); prev_heading = False; i += 1; continue
        if re.match(r"\d+\. ", t):                                   # 소제목: 위 빈 줄 2개, 아래 빈 줄 없음
            while out and out[-1] == line(""): out.pop()
            out += [line(""), line("")]
            out.append(f'<p style="{PH}">{html.escape(t)}</p>')
            prev_heading = True; i += 1; continue
        if re.match(r"▶ (한눈에 보기|마무리)\s*$", t):                 # 안내 박스(인용구 모양)
            box = [f'<p style="{P}"><b>{html.escape(t)}</b></p>', line("")]
            i += 1
            while i < len(lines) and lines[i].strip() == "": i += 1
            while i < len(lines) and lines[i].strip() != "":
                if lines[i].startswith("▶ ") or re.fullmatch(r"\{\{img:.+?\}\}", lines[i].strip()): break
                box.append(f'<p style="{P}">{inline(lines[i])}</p>'); i += 1
            out.append(f'<div style="{Q}">' + "".join(box) + "</div>")
            prev_heading = False; continue
        if not t.strip():
            if prev_heading: i += 1; continue                        # 소제목 바로 아래 빈 줄 제거
            if out and out[-1] == line("") and len(out) >= 2 and out[-2] == line(""):
                i += 1; continue                                     # 빈 줄은 최대 2개까지
        out.append(line(t)); prev_heading = False; i += 1
    return out

out = render(body)

page = ['<!doctype html><meta charset="utf-8"><title>네이버 블로그 복사용</title>',
 '<style>body{font-family:-apple-system,"Apple SD Gothic Neo",sans-serif;max-width:640px;margin:30px auto;padding:0 18px;line-height:1.85;color:#111;font-size:16px}p{margin:12px 0}hr{margin:34px 0;border:0;border-top:1px dashed #bbb}.cp{margin-left:10px;padding:6px 12px;border:1px solid #1d6a4a;background:#fff;color:#1d6a4a;border-radius:6px;font-size:13px;font-weight:700;cursor:pointer}.cp.ok{background:#1d6a4a;color:#fff}.imgbar{background:#eef6f1;border-radius:10px;padding:12px 14px;font-size:14px;margin:10px 0}.ib{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}.ib .cp{margin:0;display:inline-flex;align-items:center;gap:8px}.ib .cp img{border-radius:4px}.box{background:#fff7e0;border-radius:10px;padding:14px 16px;font-size:14px}a{color:#1d6a4a}</style>',
 '<div class="box"><b>사용법</b><br>(각 칸의 <b>복사 버튼</b>을 누르면 바로 복사됩니다) ① 제목 복사 → 블로그 제목 칸 ② 본문 영역 전체 복사 → 본문에 붙여넣기 ③ 이미지는 붙여넣기가 안 되면 <b>다운로드 폴더</b>의 이미지를 사진 버튼으로 올려 표시된 위치에 넣기 ④ 태그 입력 ⑤ <b>장소 첨부</b>(구파발경희한의원) ⑥ 모바일 미리보기 확인 후 예약 발행</div>',
 f'<hr><h3>제목 <button class="cp" onclick="cp(\'ttl\')">제목 복사</button></h3><p id="ttl"><b>{html.escape(title)}</b></p><hr><h3>본문 <button class="cp" onclick="cp(\'body\')">본문 복사(서식 포함)</button></h3>@@IMGBAR@@<div id="body">']
page += out
if refs:
    page.append(line("")); page.append(f'<p style="{PH}">참고 문헌</p>')
    page += [line(l) for l in refs.split("\n") if l.strip()]
if end:
    page.append(line(""))
    page += render(end)
page.append('</div><hr><h3>태그 <button class="cp" onclick="cp(\'tags\')">태그 복사</button></h3><p id="tags"><b>' + html.escape(tags.strip()) + '</b></p>')
page.append('<p style="color:#888;font-size:13px">블로그 편집기에서 소제목 크기·인용구는 붙여넣기 후 일부 사라질 수 있습니다. 사라지면 소제목은 19~24pt+굵게, 박스 부분은 인용구 서식으로 다시 지정하세요.</p>')
page.append('<script>function cp(id){var el=document.getElementById(id);var r=document.createRange();r.selectNodeContents(el);var s=window.getSelection();s.removeAllRanges();s.addRange(r);var ok=false;try{ok=document.execCommand("copy")}catch(e){}s.removeAllRanges();var b=event.target;var t=b.textContent;b.textContent=ok?"복사됨 ✓":"복사 실패 – 드래그해서 복사하세요";b.classList.toggle("ok",ok);setTimeout(function(){b.textContent=t;b.classList.remove("ok")},1800)}</script>')
bar = '<div class="imgbar"><b>이미지</b> 본문을 붙여넣은 뒤, 본문의 <b>[이미지 n 자리]</b> 줄을 세 번 클릭해 선택하고 해당 번호의 버튼을 눌러 복사한 다음 Cmd+V 하면 그 자리에 이미지가 들어갑니다.<div class="ib">' + "".join(f'<button class="cp" onclick="cpimg({i})"><img src="data:image/png;base64,{b64}" width="44" height="44" alt=""> 이미지 {i+1} 복사</button>' for i, (nm, b64) in enumerate(IMGS)) + '</div></div>'
page = [x.replace("@@IMGBAR@@", bar) for x in page]
page.append('<script>var IMGS=' + json.dumps([b64 for _, b64 in IMGS]) + ';function cpimg(i){var b=event.currentTarget;var bin=atob(IMGS[i]),u=new Uint8Array(bin.length);for(var k=0;k<bin.length;k++)u[k]=bin.charCodeAt(k);var blob=new Blob([u],{type:"image/png"});var done=function(ok){var t=b.lastChild.textContent;b.classList.toggle("ok",ok);b.lastChild.textContent=ok?" 복사됨 ✓ 이제 Cmd+V":" 복사 실패";setTimeout(function(){b.classList.remove("ok");b.lastChild.textContent=t},2200)};try{navigator.clipboard.write([new ClipboardItem({"image/png":blob})]).then(function(){done(true)},function(){done(false)})}catch(e){done(false)}}</script>')
res = os.path.join(os.path.dirname(src_path) or ".", base + "-copy.html")
open(res, "w", encoding="utf-8").write("\n".join(page))

# 이미지 → 다운로드 폴더
dl = os.path.expanduser(f"~/Downloads/블로그이미지/{base}")
os.makedirs(dl, exist_ok=True)
for n in dict.fromkeys(used):
    p = os.path.join(img_dir, n)
    if os.path.exists(p): shutil.copy(p, dl)
print("복사용 페이지:", res); print("이미지 폴더:", dl, "(", len(set(used)), "장 )")
if sys.platform == "darwin":
    subprocess.run(["open", res]); subprocess.run(["open", dl])
