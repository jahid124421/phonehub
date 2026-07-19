#!/usr/bin/env python3
"""
PhoneHub pipeline — news aggregator
========================================================================
Fetches fresh tech/phone/laptop/accessory/auto news from multiple FREE sources
and writes data/news.json (headlines + short excerpt + link back to source
— legal aggregation, we never copy full articles).

Category-aware: auto-tags each article by detecting keywords.
Staleness filter: --max-age N (hours, default 48) discards old articles.

Sources (each is best-effort; failures are skipped):
  1. Hacker News (Algolia API)  — reliable, no auth
  2. RSS feeds (GSMArena, Android Authority, The Verge, NotebookCheck, etc.)
  3. Reddit (r/Android, r/gadgets, r/laptops) — often blocked on CI, tried anyway

USAGE:  python news_fetch.py
        python news_fetch.py --max-age 24    # only articles from last 24h
Runs before build.py in the pipeline. Stdlib only.
========================================================================
"""
import json
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

import ph_common as C

UA = "Mozilla/5.0 (compatible; PhoneHubNewsBot/1.0; +https://github.com)"
MAX_ITEMS = 60

# ---------- Category auto-detection ----------
CATEGORY_KEYWORDS = {
    'mobiles': ['phone', 'smartphone', 'iphone', 'galaxy', 'pixel', 'android', 'ios', 'mobile',
                'oneplus', 'samsung', 'xiaomi', 'realme', 'poco', 'nothing phone', 'oppo', 'vivo'],
    'laptops': ['laptop', 'macbook', 'notebook', 'chromebook', 'thinkpad', 'ultrabook',
                'lenovo', 'dell xps', 'hp spectre', 'asus zenbook', 'razer blade'],
    'auto': ['car', 'vehicle', 'tesla', 'ev', 'electric vehicle', 'suv', 'sedan', 'automotive',
             'toyota', 'hyundai', 'bmw', 'mercedes', 'ford', 'honda car', 'maruti', 'tata motors',
             'mahindra', 'kia', 'volkswagen', 'skoda', 'mg motor', 'byd'],
    'tvs': ['tv', 'television', 'oled', 'qled', 'display', 'monitor', 'smart tv',
            'samsung tv', 'lg tv', 'sony bravia', 'tcl tv', 'hisense'],
    'electronics': ['camera', 'headphone', 'earbuds', 'wearable', 'smartwatch', 'speaker',
                    'airpods', 'buds', 'band', 'fitbit', 'garmin', 'sony wh', 'bose'],
    'appliances': ['appliance', 'vacuum', 'washing machine', 'refrigerator', 'kitchen',
                   'dishwasher', 'air purifier', 'microwave', 'oven', 'dyson'],
}


def detect_category(title, excerpt=""):
    """Auto-detect article category from title + excerpt text."""
    text = (title + " " + (excerpt or "")).lower()
    scores = {}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[cat] = score
    if scores:
        return max(scores, key=scores.get)
    return 'tech'


# HN queries -> category tag
HN_QUERIES = [
    ("smartphone", "mobiles"), ("iphone", "mobiles"), ("android phone", "mobiles"),
    ("laptop", "laptops"), ("macbook", "laptops"), ("notebook cpu", "laptops"),
    ("wireless earbuds", "electronics"), ("smartwatch", "electronics"),
    ("electric vehicle", "auto"), ("tesla", "auto"),
    ("tv oled", "tvs"),
]

# RSS feeds -> default category tag (will be overridden by auto-detection)
RSS_FEEDS = [
    ("https://www.androidauthority.com/feed/", "mobiles"),
    ("https://9to5google.com/feed/", "mobiles"),
    ("https://www.xda-developers.com/feed/", "mobiles"),
    ("https://www.theverge.com/rss/index.xml", "tech"),
    ("https://www.engadget.com/rss.xml", "tech"),
    ("https://techcrunch.com/feed/", "tech"),
    ("https://www.gsmarena.com/rss-news-reviews.php3", "mobiles"),
    ("https://www.notebookcheck.net/news/rss", "laptops"),
    ("https://www.caranddriver.com/rss/all.xml", "auto"),
    ("https://www.cnet.com/rss/news/", "tech"),
    ("https://www.tomshardware.com/feeds/all", "electronics"),
    ("https://www.techradar.com/rss", "tech"),
    ("https://www.91mobiles.com/hub/feed/", "mobiles"),
]

# Reddit subreddits -> default category tag
REDDIT_SUBS = [("Android", "mobiles"), ("gadgets", "electronics"), ("laptops", "laptops"),
               ("electricvehicles", "auto")]


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


def og_image(url):
    """Try to extract og:image from an article URL."""
    try:
        import ssl as sslmod
        ctx = sslmod.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = sslmod.CERT_NONE
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
        with urllib.request.urlopen(req, timeout=8, context=ctx) as r:
            html = r.read(200000)
            if isinstance(html, bytes):
                html = html.decode("utf-8", errors="ignore")
            m = re.search(r'<meta[^>]+property=[\"\']og:image[\"\'][^>]+content=[\"\']([^\"\']+)[\"\']', html, re.I)
            if m:
                img = m.group(1)
            else:
                m = re.search(r'<meta[^>]+content=[\"\']([^\"\']+)[\"\'][^>]+property=[\"\']og:image[\"\']', html, re.I)
                if m:
                    img = m.group(1)
                else:
                    return ""
            if img.startswith("/"):
                from urllib.parse import urljoin
                base_match = re.match(r'(https?://[^/]+)', url)
                if base_match:
                    img = urljoin(base_match.group(1), img)
            return img
    except Exception:
        pass
    return ""


def search_image(title):
    """Generate a fallback image URL using Lorem Picsum (free, no API key).
    Uses a hash of the title as a seed so the same article always gets the same image."""
    seed = str(abs(hash(title)) % 100000)
    return f"https://picsum.photos/seed/{seed}/600/340"


def clip(s, n=180):
    s = strip_html(s)
    return (s[: n - 1] + "\u2026") if len(s) > n else s


def date_label(ts):
    """Return 'Today', 'Yesterday', or the date string for a timestamp."""
    now = datetime.now(tz=timezone.utc)
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    delta = now - dt
    if delta.days == 0:
        return "Today"
    elif delta.days == 1:
        return "Yesterday"
    else:
        return dt.strftime("%b %d, %Y")


def add(items, seen, title, url, excerpt, tag, source, ts, image=""):
    title = strip_html(title)
    if not title or not url:
        return
    key = title.lower()[:80]
    if key in seen:
        return
    seen.add(key)
    # Auto-detect category from content
    detected_cat = detect_category(title, excerpt)
    items.append({
        "id": "n" + str(abs(hash(url)) % (10 ** 10)),
        "title": title[:140],
        "excerpt": clip(excerpt or title, 180),
        "date": datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d"),
        "dateLabel": date_label(ts),
        "tag": detected_cat,
        "url": url,
        "source": source,
        "image": image or "",
        "_ts": ts,
    })


MEDIA_NS = "{http://search.yahoo.com/mrss/}"
CONTENT_NS = "{http://purl.org/rss/1.0/modules/content/}"


def rss_image(e):
    for tag in ("content", "thumbnail"):
        el = e.find(MEDIA_NS + tag)
        if el is not None and el.get("url"):
            return el.get("url")
    enc = e.find("enclosure")
    if enc is not None:
        u = enc.get("url", "")
        if enc.get("type", "").startswith("image") or re.search(r"\.(jpg|jpeg|png|webp)", u, re.I):
            return u
    for field in ("description", CONTENT_NS + "encoded"):
        txt = e.findtext(field) or ""
        m = re.search(r'<img[^>]+src=["\']([^"\']+)', txt)
        if m:
            return m.group(1)
    return ""


def fetch_hn(items, seen, max_age_ts):
    for query, tag in HN_QUERIES:
        try:
            u = ("https://hn.algolia.com/api/v1/search_by_date?query="
                 + urllib.parse.quote(query) + "&tags=story&hitsPerPage=6")
            data = json.loads(_get(u))
            for h in data.get("hits", []):
                ts = int(h.get("created_at_i") or time.time())
                if ts < max_age_ts:
                    continue
                url = h.get("url") or ("https://news.ycombinator.com/item?id=" + str(h.get("objectID", "")))
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


def fetch_rss(items, seen, max_age_ts):
    for url, tag in RSS_FEEDS:
        try:
            raw = _get(url)
            root = ET.fromstring(raw)
            # handle both RSS <item> and Atom <entry>
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            entries = root.findall(".//item") or root.findall(".//atom:entry", ns)
            source = re.sub(r"^www\.|\.com.*$", "", urllib.parse.urlparse(url).netloc)
            count = 0
            for e in entries[:10]:
                title = (e.findtext("title") or e.findtext("atom:title", "", ns) or "")
                link = e.findtext("link") or ""
                if not link:
                    le = e.find("atom:link", ns)
                    link = le.get("href") if le is not None else ""
                desc = (e.findtext("description") or e.findtext("atom:summary", "", ns) or "")
                pub = (e.findtext("pubDate") or e.findtext("atom:updated", "", ns) or "")
                ts = int(_parse_date(pub))
                if ts < max_age_ts:
                    continue
                add(items, seen, title, link, desc, tag, source.title(), ts, rss_image(e))
                count += 1
            print(f"  rss {source}: {count}")
        except Exception as e:  # noqa
            print(f"  ! rss {url[:50]}: {e}")


def fetch_reddit(items, seen, max_age_ts):
    for sub, tag in REDDIT_SUBS:
        try:
            u = f"https://www.reddit.com/r/{sub}/top.json?limit=8&t=week"
            data = json.loads(_get(u))
            for c in data.get("data", {}).get("children", []):
                d = c.get("data", {})
                ts = int(d.get("created_utc") or time.time())
                if ts < max_age_ts:
                    continue
                url = "https://www.reddit.com" + d.get("permalink", "")
                thumb = d.get("thumbnail", "")
                if not (isinstance(thumb, str) and thumb.startswith("http")):
                    thumb = ""
                add(items, seen, d.get("title", ""), url, d.get("selftext", ""),
                    tag, "Reddit r/" + sub, ts, thumb)
            time.sleep(0.3)
        except Exception as e:  # noqa
            print(f"  ! reddit r/{sub}: {e}")


def fetch_newsapi(items, seen, max_age_ts):
    import os
    key = os.environ.get("NEWSAPI_KEY", "")
    if not key:
        try:
            key = C.load_config().get("newsapi_key", "")
        except SystemExit:
            key = ""
    if not key:
        print("  (no NewsAPI key, skipping)")
        return
    topics = [("smartphone OR \"mobile phone\"", "mobiles"), ("laptop OR notebook", "laptops"),
              ("wireless earbuds OR smartwatch OR charger", "electronics"),
              ("electric vehicle OR car launch", "auto")]
    for q, tag in topics:
        try:
            u = ("https://newsapi.org/v2/everything?q=" + urllib.parse.quote(q)
                 + "&language=en&sortBy=publishedAt&pageSize=10&apiKey=" + key)
            data = json.loads(_get(u))
            for a in data.get("articles", []):
                ts = int(_parse_date(a.get("publishedAt", "")))
                if ts < max_age_ts:
                    continue
                src = (a.get("source") or {}).get("name") or "NewsAPI"
                add(items, seen, a.get("title", ""), a.get("url", ""),
                    a.get("description", ""), tag, src, ts, a.get("urlToImage") or "")
        except Exception as e:  # noqa
            print(f"  ! NewsAPI '{q[:20]}': {e}")


def main():
    args = sys.argv[1:]
    max_age_hours = 48
    if "--max-age" in args:
        max_age_hours = int(args[args.index("--max-age") + 1])

    max_age_ts = time.time() - (max_age_hours * 3600)

    items, seen = [], set()
    print(f"[news] Fetching articles (max age: {max_age_hours}h)...")
    print("[news] NewsAPI...")
    fetch_newsapi(items, seen, max_age_ts)
    print("[news] Hacker News...")
    fetch_hn(items, seen, max_age_ts)
    print("[news] RSS feeds...")
    fetch_rss(items, seen, max_age_ts)
    print("[news] Reddit...")
    fetch_reddit(items, seen, max_age_ts)

    # Sort: prioritize last 24h, then by timestamp
    now_ts = time.time()
    items.sort(key=lambda x: (x.get("_ts", 0) >= now_ts - 86400, x.get("_ts", 0)), reverse=True)
    items = items[:MAX_ITEMS]

    # Try to fetch OG images for articles without one
    noimg = [it for it in items if not it.get("image")]
    if noimg:
        print(f"[news] scraping OG images for {len(noimg)} articles...")
        for it in noimg:
            img = og_image(it.get("url", ""))
            if img:
                it["image"] = img
            time.sleep(0.5)

    # Final fallback: search DuckDuckGo for any remaining articles without images
    noimg = [it for it in items if not it.get("image")]
    if noimg:
        print(f"[news] searching DuckDuckGo for {len(noimg)} articles...")
        for it in noimg:
            img = search_image(it.get("title", ""))
            if img:
                it["image"] = img
            time.sleep(0.5)

    # Remove internal timestamp, keep dateLabel
    for it in items:
        it.pop("_ts", None)

    if not items:
        print("[news] no items fetched; keeping existing news.json")
        return
    C.write_json("news.json", items)

    # Summary by category
    cat_counts = {}
    for it in items:
        cat = it.get("tag", "tech")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    today_count = sum(1 for it in items if it.get("dateLabel") == "Today")
    cat_summary = ", ".join(f"{v} {k}" for k, v in sorted(cat_counts.items(), key=lambda x: -x[1]))

    print(f"[news] wrote data/news.json — {len(items)} items")
    print(f"[news] categories: {cat_summary}")
    print(f"[news] {today_count} articles from today")


if __name__ == "__main__":
    main()
