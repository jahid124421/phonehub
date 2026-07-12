#!/usr/bin/env python3
"""
PhoneHub — Wikidata phone seeder (FREE, no key, no rate-limit hassle)
========================================================================
Adds many current phones (name, brand, release date, freely-licensed
image, OS) from Wikidata's SPARQL endpoint and MERGES them into
data/specs.json WITHOUT touching existing GSMArena full-spec phones.

Why: GSMArena rate-limits scraping. Wikidata is free, unlimited, current,
and its images (Wikimedia Commons) are hotlink-friendly. Specs are thinner
than GSMArena, but every phone gets a real page + image + AI review.

USAGE:  python wikidata_seed.py [--per-brand 25] [--limit 500]
Then:   python build.py
Stdlib only.
========================================================================
"""
import json
import re
import sys
import urllib.parse
import urllib.request
import urllib.error

import ph_common as C

ENDPOINT = "https://query.wikidata.org/sparql"
UA = "PhoneHubBot/1.0 (https://github.com/jahid124421/phonehub)"

# our brand set (keyword in Wikidata brand label -> slug, display)
BRAND_MAP = [
    ("apple", "apple", "Apple"), ("samsung", "samsung", "Samsung"), ("google", "google", "Google"),
    ("xiaomi", "xiaomi", "Xiaomi"), ("redmi", "xiaomi", "Xiaomi"), ("poco", "xiaomi", "Xiaomi"),
    ("oneplus", "oneplus", "OnePlus"), ("nothing", "nothing", "Nothing"), ("vivo", "vivo", "Vivo"),
    ("realme", "realme", "Realme"), ("oppo", "oppo", "Oppo"), ("motorola", "motorola", "Motorola"),
    ("sony", "sony", "Sony"), ("nokia", "nokia", "Nokia"), ("honor", "honor", "Honor"),
    ("asus", "asus", "Asus"), ("huawei", "huawei", "Huawei"),
]

QUERY = """
SELECT ?itemLabel ?brandLabel ?date ?image ?osLabel WHERE {
  ?item wdt:P31 wd:Q19723451 .
  ?item wdt:P18 ?image .
  OPTIONAL { ?item wdt:P176 ?brand. }
  OPTIONAL { ?item wdt:P577 ?date. }
  OPTIONAL { ?item wdt:P306 ?os. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY DESC(?date)
LIMIT %d
"""


def sparql(limit):
    url = ENDPOINT + "?format=json&query=" + urllib.parse.quote(QUERY % limit)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/sparql-results+json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.URLError as e:
        if "CERTIFICATE" in str(e).upper() or "SSL" in str(e).upper():
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=90, context=ctx) as r:
                return json.loads(r.read().decode("utf-8"))
        raise


def map_brand(label):
    low = (label or "").lower()
    for kw, slug, disp in BRAND_MAP:
        if kw in low:
            return slug, disp
    return None, None


def thumb(img_url):
    # Wikidata P18 -> Commons Special:FilePath; request a sane thumbnail width
    if not img_url:
        return ""
    u = img_url.replace("http://", "https://")
    return u + ("&" if "?" in u else "?") + "width=500"


def main():
    args = sys.argv[1:]
    per_brand = int(args[args.index("--per-brand") + 1]) if "--per-brand" in args else 25
    limit = int(args[args.index("--limit") + 1]) if "--limit" in args else 600

    print(f"[wikidata] querying up to {limit} phone models...")
    data = sparql(limit)
    rows = data.get("results", {}).get("bindings", [])
    print(f"[wikidata] {len(rows)} rows")

    existing = C.read_json("specs.json") or {"brands": [], "phones": []}
    existing_ids = {p["id"] for p in existing["phones"]}
    existing_names = {re.sub(r"[^a-z0-9]", "", p["name"].lower()) for p in existing["phones"]}
    brand_ids = {b["id"] for b in existing["brands"]}
    per_brand_count = {}

    added = 0
    for row in rows:
        name = row.get("itemLabel", {}).get("value", "").strip()
        if not name or name.startswith("Q"):   # skip unlabeled items
            continue
        slug, disp = map_brand(row.get("brandLabel", {}).get("value", ""))
        # some items have brand only in the name
        if not slug:
            slug, disp = map_brand(name)
        if not slug:
            continue
        if per_brand_count.get(slug, 0) >= per_brand:
            continue
        pid = C.slugify(name)
        norm = re.sub(r"[^a-z0-9]", "", name.lower())
        if pid in existing_ids or norm in existing_names:
            continue

        date = row.get("date", {}).get("value", "")[:10]
        os_name = row.get("osLabel", {}).get("value", "")
        image = thumb(row.get("image", {}).get("value", ""))

        specs = {"Launch": {"Announced": date or "\u2014", "Status": "Available"},
                 "Misc": {"Brand": disp}}
        if os_name and not os_name.startswith("Q"):
            specs["Platform"] = {"OS": os_name}

        existing["phones"].append({
            "id": pid, "brand": slug, "name": name,
            "image": image, "images": [image] if image else [],
            "releaseDate": date,
            "quickSpecs": {"display": "", "processor": os_name, "ram": "", "storage": "",
                           "camera": "", "battery": ""},
            "specs": specs,
        })
        existing_ids.add(pid)
        existing_names.add(norm)
        per_brand_count[slug] = per_brand_count.get(slug, 0) + 1
        if slug not in brand_ids:
            existing["brands"].append({"id": slug, "name": disp, "logo": C.BRAND_EMOJI.get(slug, "\U0001F4F1")})
            brand_ids.add(slug)
        added += 1

    C.write_json("specs.json", existing)
    print(f"[wikidata] added {added} phones. Total now {len(existing['phones'])} across {len(existing['brands'])} brands.")


if __name__ == "__main__":
    main()
