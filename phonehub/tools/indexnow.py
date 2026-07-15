#!/usr/bin/env python3
"""
PhoneHub — IndexNow auto-submit (SEO automation)
========================================================================
Pings IndexNow (Bing, Yandex, Seznam) with all site URLs so new/updated
pages get discovered fast — free, no verification beyond a key file.
Runs at the end of build.py. Google doesn't use IndexNow yet (submit the
sitemap in Search Console for Google), but this covers the rest instantly.

Stdlib only.
========================================================================
"""
import json
import os
import re
import urllib.request
import urllib.error

import ph_common as C

KEY = "8f4c2a1e9b7d6350f1a2c3b4d5e6f708"
SITEMAP = os.path.join(C.HERE, "..", "sitemap.xml")


def main():
    try:
        cfg = C.load_config()
    except SystemExit:
        cfg = {}
    site = (cfg.get("site_url") or "").rstrip("/")
    if not site or "your-domain" in site:
        print("[indexnow] site_url not set; skipping")
        return
    host = re.sub(r"^https?://", "", site).split("/")[0]

    if not os.path.exists(SITEMAP):
        print("[indexnow] no sitemap; skipping")
        return
    with open(SITEMAP, "r", encoding="utf-8") as f:
        urls = re.findall(r"<loc>([^<]+)</loc>", f.read())
    if not urls:
        print("[indexnow] no urls; skipping")
        return

    payload = json.dumps({
        "host": host,
        "key": KEY,
        "keyLocation": f"{site}/{KEY}.txt",
        "urlList": urls[:10000],
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "PhoneHubBot/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"[indexnow] submitted {len(urls)} urls -> HTTP {r.status}")
    except urllib.error.HTTPError as e:
        # 200/202 = ok; others are informational
        print(f"[indexnow] {len(urls)} urls -> HTTP {e.code} ({e.reason})")
    except Exception as e:  # noqa
        print(f"[indexnow] skipped: {e}")


if __name__ == "__main__":
    main()
