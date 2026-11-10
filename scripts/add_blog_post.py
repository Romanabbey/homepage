#!/usr/bin/env python3
"""원장님이 고른 네이버 블로그 글 하나를 사이트에 올릴 목록(data/blog_posts.json)에 추가합니다.
사용: python3 scripts/add_blog_post.py <블로그 글 주소> --pages accident,diet
      python3 scripts/add_blog_post.py --remove <블로그 글 주소>
pages 키: accident, diet, growth, postpartum, yakchim, gongjindan, bopae, anshim, bujong, patch (홈에는 항상 최신 3편이 나옵니다)
제목·날짜·첫 이미지는 블로그 RSS(rss.blog.naver.com/365khsol.xml)에서 가져옵니다. RSS에 없으면 --title 로 직접 넣습니다.
"""
import argparse, json, os, re, sys, urllib.request, html
from email.utils import parsedate_to_datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "blog_posts.json")
RSS = "https://rss.blog.naver.com/365khsol.xml"
PAGES = {"accident", "diet", "growth", "postpartum", "yakchim", "gongjindan", "bopae", "anshim", "bujong", "patch"}


def post_id(url):
    m = re.search(r"(?:logNo=|/)(\d{9,})", url)
    return m.group(1) if m else None


def from_rss(pid):
    xml = urllib.request.urlopen(RSS, timeout=20).read().decode("utf-8")
    for it in re.findall(r"<item>(.*?)</item>", xml, re.S):
        link = re.search(r"<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>", it, re.S).group(1)
        if pid and pid in link:
            title = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", it, re.S).group(1).strip()
            date = re.search(r"<pubDate>(.*?)</pubDate>", it).group(1)
            img = re.search(r"<img[^>]+src=[\"']([^\"']+)", html.unescape(it))
            return {"title": html.unescape(title), "date": parsedate_to_datetime(date).strftime("%Y-%m-%d"),
                    "thumb": img.group(1) if img else ""}
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url", nargs="?")
    ap.add_argument("--pages", default="")
    ap.add_argument("--title")
    ap.add_argument("--remove")
    a = ap.parse_args()
    posts = json.load(open(DATA, encoding="utf-8")) if os.path.exists(DATA) else []
    if a.remove:
        pid = post_id(a.remove)
        n = len(posts)
        posts = [p for p in posts if post_id(p["url"]) != pid]
        json.dump(posts, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("삭제:", n - len(posts), "건"); return
    if not a.url:
        sys.exit("블로그 글 주소를 넣어 주세요")
    pages = [p.strip() for p in a.pages.split(",") if p.strip()]
    bad = [p for p in pages if p not in PAGES]
    if bad:
        sys.exit("알 수 없는 페이지 키: " + ", ".join(bad))
    pid = post_id(a.url)
    info = from_rss(pid) or {}
    if a.title:
        info["title"] = a.title
    if not info.get("title"):
        sys.exit("RSS에서 글을 찾지 못했습니다. --title 로 제목을 직접 넣어 주세요.")
    url = f"https://blog.naver.com/365khsol/{pid}" if pid else a.url
    posts = [p for p in posts if post_id(p["url"]) != pid]
    posts.append({"url": url, "title": info["title"], "date": info.get("date", ""), "thumb": info.get("thumb", ""), "pages": pages})
    json.dump(posts, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("추가:", info["title"], "| 페이지:", ", ".join(pages) or "(홈만)")


if __name__ == "__main__":
    main()
