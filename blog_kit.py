#!/usr/bin/env python3
"""네이버 블로그 복사용 페이지 만들기.
사용: python3 blog_kit.py blog_out/글이름.txt [이미지폴더]
초안 형식: [제목] [본문] [참고 문헌] [맺음 안내] [추천 태그] 구역, 본문 안에 {{img:파일이름.png}} 로 이미지 위치 표시.
결과: 같은 폴더에 글이름-copy.html 생성, 이미지는 ~/Downloads/블로그이미지/글이름/ 에 복사 후 폴더를 엽니다."""
import sys, os, re, html, shutil, subprocess, base64

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

def img(name):
    p = os.path.join(img_dir, name)
    if not os.path.exists(p):
        return f"<p style='color:#c00'>[이미지 없음: {html.escape(name)}]</p>"
    b = base64.b64encode(open(p, "rb").read()).decode()
    return f'<p style="text-align:center"><img src="data:image/png;base64,{b}" width="540" alt=""></p>'

H = 'font-size:22px;font-weight:700;margin:40px 0 2px'
Q = 'background:#f3f6f4;border-left:4px solid #1d6a4a;padding:12px 16px;margin:20px 0;border-radius:6px'
used = []
def blk(b):
    mm = re.fullmatch(r"\{\{img:(.+?)\}\}", b.strip())
    if mm:
        used.append(mm.group(1)); return img(mm.group(1))
    return para(b)
out = []
for s in re.split(r"\n\s*\n\s*\n", body.strip("\n")):
    blocks = [b for b in re.split(r"\n\s*\n", s.strip()) if b.strip()]
    if not blocks:
        continue
    first = blocks[0].split("\n")[0]
    m = re.fullmatch(r"\{\{img:(.+?)\}\}", blocks[0].strip())
    if m:
        used.append(m.group(1)); out.append(img(m.group(1))); continue
    if re.match(r"\d+\. ", first):
        out.append(f'<p style="{H}"><b>{html.escape(first)}</b></p>')
        rest = blocks[0].split("\n")[1:]
        if rest: out.append(para("\n".join(rest)))
        for b in blocks[1:]:
            mm = re.fullmatch(r"\{\{img:(.+?)\}\}", b.strip())
            if mm: used.append(mm.group(1)); out.append(img(mm.group(1)))
            else: out.append(para(b))
    elif first.startswith("▶"):
        inner = f'<b>{html.escape(first)}</b>'
        if len(blocks) > 1:
            inner += "<br><br>" + "<br>".join(link(l) for l in blocks[1].split("\n"))
        out.append(f'<div style="{Q}">{inner}</div>')
        for b in blocks[2:]:
            out.append(blk(b))
    else:
        for b in blocks:
            mm = re.fullmatch(r"\{\{img:(.+?)\}\}", b.strip())
            if mm: used.append(mm.group(1)); out.append(img(mm.group(1)))
            else: out.append(para(b))

page = ['<!doctype html><meta charset="utf-8"><title>네이버 블로그 복사용</title>',
 '<style>body{font-family:-apple-system,"Apple SD Gothic Neo",sans-serif;max-width:640px;margin:30px auto;padding:0 18px;line-height:1.85;color:#111;font-size:16px}p{margin:12px 0}hr{margin:34px 0;border:0;border-top:1px dashed #bbb}.box{background:#fff7e0;border-radius:10px;padding:14px 16px;font-size:14px}a{color:#1d6a4a}</style>',
 '<div class="box"><b>사용법</b><br>① 제목 복사 → 블로그 제목 칸 ② 본문 영역 전체 복사 → 본문에 붙여넣기 ③ 이미지는 붙여넣기가 안 되면 <b>다운로드 폴더</b>의 이미지를 사진 버튼으로 올려 표시된 위치에 넣기 ④ 태그 입력 ⑤ <b>장소 첨부</b>(구파발경희한의원) ⑥ 모바일 미리보기 확인 후 예약 발행</div>',
 f'<hr><h3>제목</h3><p><b>{html.escape(title)}</b></p><hr><h3>본문 (여기부터 복사)</h3><div id="body">']
page += out
if refs:
    page.append("<p style='font-size:13px;color:#555'><b>[참고 문헌]</b><br>" + "<br>".join(link(l) for l in refs.split("\n") if l.strip()) + "</p>")
if end:
    for b in re.split(r"\n\s*\n", end.strip()):
        page.append(blk(b))
page.append('</div><hr><h3>태그 (복사해서 태그 칸에)</h3><p><b>' + html.escape(tags.strip()) + '</b></p>')
page.append('<p style="color:#888;font-size:13px">블로그 편집기에서 소제목 크기·인용구는 붙여넣기 후 일부 사라질 수 있습니다. 사라지면 소제목은 19~24pt+굵게, 박스 부분은 인용구 서식으로 다시 지정하세요.</p>')
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
