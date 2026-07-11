#!/usr/bin/env python3
"""
PhoneHub — SEO generator
========================================================================
Reads ../js/data.js and generates:
  ../sitemap.xml   (home + all list pages + every phone page + brands)
  ../robots.txt    (points crawlers to the sitemap)

Set your live domain in config.json:  "site_url": "https://yourdomain.com"
Falls back to a placeholder if not set.

USAGE:  python gen_seo.py
Called automatically at the end of build.py. Stdlib only.
========================================================================
"""
import json
import os
import re
import sys
import datetime

import ph_common as C

DATA_JS = os.path.join(C.HERE, "..", "js", "data.js")


def array_text(js_text, var_name):
    """Return the `[ ... ]` substring assigned to window.<var> via bracket matching.
    Works whether the file is strict JSON (pipeline output) or JS (hand-written)."""
    idx = js_text.find(f"window.{var_name}")
    if idx == -1:
        return ""
    start = js_text.find("[", idx)
    if start == -1:
        return ""
    depth, i, in_str, esc, quote = 0, start, False, False, ""
    while i < len(js_text):
        ch = js_text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                in_str = False
        else:
            if ch in ('"', "'"):
                in_str, quote = True, ch
            elif ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    return js_text[start:i + 1]
        i += 1
    return ""


def ids_from(js_text, var_name):
    """Extract each top-level record's `id` value (quoted or unquoted key)."""
    block = array_text(js_text, var_name)
    if not block:
        return []
    return re.findall(r'["\']?id["\']?\s*:\s*["\']([^"\']+)["\']', block)


def url_tag(loc, changefreq="weekly", priority="0.6"):
    return (f"  <url>\n    <loc>{loc}</loc>\n"
            f"    <changefreq>{changefreq}</changefreq>\n"
            f"    <priority>{priority}</priority>\n  </url>")


def main():
    if not os.path.exists(DATA_JS):
        print(f"{DATA_JS} not found.")
        sys.exit(1)
    with open(DATA_JS, "r", encoding="utf-8-sig") as f:
        js = f.read()

    phone_ids = ids_from(js, "PHONES")
    brand_ids = ids_from(js, "BRANDS")

    try:
        cfg = C.load_config()
    except SystemExit:
        cfg = {}
    site = (cfg.get("site_url") or "https://your-domain.example").rstrip("/")

    urls = [
        url_tag(f"{site}/", "daily", "1.0"),
        url_tag(f"{site}/search.html", "daily", "0.8"),
        url_tag(f"{site}/brands.html", "weekly", "0.6"),
        url_tag(f"{site}/compare.html", "weekly", "0.6"),
        url_tag(f"{site}/news.html", "daily", "0.7"),
        url_tag(f"{site}/about.html", "monthly", "0.3"),
        url_tag(f"{site}/contact.html", "monthly", "0.3"),
        url_tag(f"{site}/privacy.html", "yearly", "0.2"),
        url_tag(f"{site}/terms.html", "yearly", "0.2"),
        url_tag(f"{site}/disclosure.html", "yearly", "0.2"),
    ]
    for bid in brand_ids:
        urls.append(url_tag(f"{site}/search.html?brand={bid}", "weekly", "0.6"))
    for pid in phone_ids:
        urls.append(url_tag(f"{site}/phone/{pid}.html", "weekly", "0.8"))

    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "\n".join(urls) + "\n</urlset>\n")
    out_sitemap = os.path.join(C.HERE, "..", "sitemap.xml")
    with open(out_sitemap, "w", encoding="utf-8") as f:
        f.write(sitemap)

    robots = (f"User-agent: *\nAllow: /\n\nSitemap: {site}/sitemap.xml\n")
    out_robots = os.path.join(C.HERE, "..", "robots.txt")
    with open(out_robots, "w", encoding="utf-8") as f:
        f.write(robots)

    print(f"[seo] sitemap.xml — {len(urls)} urls ({len(phone_ids)} phones, {len(brand_ids)} brands)")
    print(f"[seo] robots.txt  — sitemap at {site}/sitemap.xml")
    if "your-domain.example" in site:
        print('[seo] NOTE: set "site_url" in config.json to your real domain, then re-run.')


if __name__ == "__main__":
    main()
