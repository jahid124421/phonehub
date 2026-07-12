#!/usr/bin/env python3
"""
PhoneHub pipeline — news aggregator
========================================================================
Fetches fresh tech/phone/laptop/accessory news from multiple FREE sources
and writes data/news.json (headlines + short excerpt + link back to source
— legal aggregation, we never copy full articles).

Sources (each is best-effort; failures are skipped):
  1. Hacker News (Algolia API)  — reliable, no auth
  2. RSS feeds (GSMArena, Android Authority, The Verge, 9to5, Notebookcheck)
  3. Reddit (r/Android, r/gadgets, r/laptops) — often blocked on CI, tried anyway

USAGE:  python news_fetch.py
Runs before build.py in the pipeline. Stdlib only.
========================================================================
"""
import json
import re
import time
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import ph_common as C

UA = "Mozilla/5.0 (compatible; PhoneHubNewsBot/1.0; +https://github.com)"
MAX_ITEMS = 45

# HN queries -> category tag
HN_QUERIES = [
    ("smartphone", "Phones"), ("iphone", "Phones"), ("android phone", "Phones"),
    ("laptop", "Laptops"), ("macbook", "Laptops"), ("notebook cpu", "Laptops"),
    ("wireless earbuds", "Accessories"), ("smartwatch", "Accessories"),
]

# RSS feeds -> category tag
RSS_FEEDS = [
    ("https://www.androidauthority.com/feed/", "Phones"),
    ("https://9to5google.com/feed/", "Phones"),
    ("https://www.xda-developers.com/feed/", "Phones"),
    ("https://www.theverge.com/rss/index.xml", "Tech"),
    ("https://www.engadget.com/rss.xml", "Tech"),
    ("https://techcrunch.com/feed/", "Tech"),
]

# Reddit subreddits -> category tag
REDDIT_SUBS = [("Android", "Phones"), ("gadgets", "Accessories"), ("laptops", "Laptops")]


def _get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except urllib.error.URLError as e:
        # public news headlines are not security-sensitive: retry ignoring
        # cert issues (some runners have stale CA bundles / clock skew)
        if "CERTIFICATE" in str(e).upper() or "SSL" in str(e).upper():
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                return r.read()
        raise


def strip_html(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    s = re.sub(r"&[a-z#0-9]+;", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def clip(s, n=180):
    s = strip_html(s)
    return (s[: n - 1] + "\u2026") if len(s) > n else s


def add(items, seen, title, url, excerpt, tag, source, ts):
    title = strip_html(title)
    if not title or not url:
        return
    key = title.lower()[:80]
    if key in seen:
        return
    seen.add(key)
    items.append({
        "id": "n" + str(abs(hash(url)) % (10 ** 10)),
        "title": title[:140],
        "excerpt": clip(excerpt or title, 180),
        "date": datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d"),
        "tag": tag,
        "url": url,
        "source": source,
        "_ts": ts,
    })


def fetch_hn(items, seen):
    for query, tag in HN_QUERIES:
        try:
            u = ("https://hn.algolia.com/api/v1/search_by_date?query="
                 + urllib.parse.quote(query) + "&tags=story&hitsPerPage=6")
            data = json.loads(_get(u))
            for h in data.get("hits", []):
                url = h.get("url") or ("https://news.ycombinator.com/item?id=" + str(h.get("objectID", "")))
                ts = int(h.get("created_at_i") or time.time())
                add(items, seen, h.get("title", ""), url, h.get("story_text", ""),
                    tag, "Hacker News", ts)
            time.sleep(0.2)
        except Exception as e:  # noqa
            print(f"  ! HN '{query}': {e}")


def _parse_date(s):
    for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z",
                "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.strptime(s.strip(), fmt).timestamp()
        except Exception:  # noqa
            continue
    return time.time()


def fetch_rss(items, seen):
    for url, tag in RSS_FEEDS:
        try:
            raw = _get(url)
            root = ET.fromstring(raw)
            # handle both RSS <item> and Atom <entry>
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            entries = root.findall(".//item") or root.findall(".//atom:entry", ns)
            source = re.sub(r"^www\.|\.com.*$", "", urllib.parse.urlparse(url).netloc)
            count = 0
            for e in entries[:8]:
                title = (e.findtext("title") or e.findtext("atom:title", "", ns) or "")
                link = e.findtext("link") or ""
                if not link:
                    le = e.find("atom:link", ns)
                    link = le.get("href") if le is not None else ""
                desc = (e.findtext("description") or e.findtext("atom:summary", "", ns) or "")
                pub = (e.findtext("pubDate") or e.findtext("atom:updated", "", ns) or "")
                add(items, seen, title, link, desc, tag, source.title(), int(_parse_date(pub)))
                count += 1
            print(f"  rss {source}: {count}")
        except Exception as e:  # noqa
            print(f"  ! rss {url[:40]}: {e}")


def fetch_reddit(items, seen):
    for sub, tag in REDDIT_SUBS:
        try:
            u = f"https://www.reddit.com/r/{sub}/top.json?limit=6&t=week"
            data = json.loads(_get(u))
            for c in data.get("data", {}).get("children", []):
                d = c.get("data", {})
                url = "https://www.reddit.com" + d.get("permalink", "")
                add(items, seen, d.get("title", ""), url, d.get("selftext", ""),
                    tag, "Reddit r/" + sub, int(d.get("created_utc") or time.time()))
            time.sleep(0.3)
        except Exception as e:  # noqa
            print(f"  ! reddit r/{sub}: {e}")


def main():
    items, seen = [], set()
    print("[news] Hacker News...")
    fetch_hn(items, seen)
    print("[news] RSS feeds...")
    fetch_rss(items, seen)
    print("[news] Reddit...")
    fetch_reddit(items, seen)

    items.sort(key=lambda x: x.get("_ts", 0), reverse=True)
    items = items[:MAX_ITEMS]
    for it in items:
        it.pop("_ts", None)

    if not items:
        print("[news] no items fetched; keeping existing news.json")
        return
    C.write_json("news.json", items)
    print(f"[news] wrote data/news.json — {len(items)} items")


if __name__ == "__main__":
    main()
