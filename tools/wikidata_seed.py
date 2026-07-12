#!/usr/bin/env python3
"""
PhoneHub — Wikidata catalog seeder (FREE, no key, no rate-limit hassle)
========================================================================
Adds products from any Wikidata category (phones, tablets, laptops, TVs,
smartwatches, earbuds...) and MERGES them into data/specs.json without
touching existing entries. Free, unlimited, current, with Commons images.

USAGE:
    python wikidata_seed.py --category phone   --qid Q19723451 --per-brand 40
    python wikidata_seed.py --category tablet  --qid Q155972   --per-brand 25 --any-brand
    python wikidata_seed.py --category laptop  --qid Q3962     --per-brand 25 --any-brand
    python wikidata_seed.py --category tv      --qid Q564635   --per-brand 20 --any-brand
    python wikidata_seed.py --category smartwatch --qid Q5362345 --per-brand 20 --any-brand
    python wikidata_seed.py --all            # seed every category in CATEGORIES

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

# category -> (Wikidata QID, per-brand cap, restrict to known phone brands?)
CATEGORIES = {
    "phone":      ("Q19723451", 40, True),
    "tablet":     ("Q155972",   25, False),
    "laptop":     ("Q3962",     25, False),
    "tv":         ("Q564635",   20, False),
    "smartwatch": ("Q5362345",  20, False),
    "earbuds":    ("Q113711206", 15, False),
}

# known phone brands (used when restrict=True)
BRAND_MAP = [
    ("apple", "apple", "Apple"), ("samsung", "samsung", "Samsung"), ("google", "google", "Google"),
    ("xiaomi", "xiaomi", "Xiaomi"), ("redmi", "xiaomi", "Xiaomi"), ("poco", "xiaomi", "Xiaomi"),
    ("oneplus", "oneplus", "OnePlus"), ("nothing", "nothing", "Nothing"), ("vivo", "vivo", "Vivo"),
    ("realme", "realme", "Realme"), ("oppo", "oppo", "Oppo"), ("motorola", "motorola", "Motorola"),
    ("sony", "sony", "Sony"), ("nokia", "nokia", "Nokia"), ("honor", "honor", "Honor"),
    ("asus", "asus", "Asus"), ("huawei", "huawei", "Huawei"),
]

# clean brand names from manufacturer labels (for --any-brand categories)
BRAND_CLEAN = re.compile(r"\b(inc|corporation|corp|co|ltd|limited|electronics|mobile|mobiles|technologies|technology|group|company|gmbh|international)\b\.?", re.I)


def sparql(qid, limit, require_image=True):
    img_line = "?item wdt:P18 ?image ." if require_image else "OPTIONAL { ?item wdt:P18 ?image. }"
    query = ("SELECT ?itemLabel ?brandLabel ?date ?image ?osLabel WHERE { "
             "?item wdt:P31 wd:%s . %s "
             "OPTIONAL { ?item wdt:P176 ?brand. } OPTIONAL { ?item wdt:P577 ?date. } "
             "OPTIONAL { ?item wdt:P306 ?os. } "
             'SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } } '
             "ORDER BY DESC(?date) LIMIT %d" % (qid, img_line, limit))
    url = ENDPOINT + "?format=json&query=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/sparql-results+json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.URLError as e:
        if "CERTIFICATE" in str(e).upper() or "SSL" in str(e).upper():
            import ssl
            ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=90, context=ctx) as r:
                return json.loads(r.read().decode("utf-8"))
        raise


def brand_known(label):
    low = (label or "").lower()
    for kw, slug, disp in BRAND_MAP:
        if kw in low:
            return slug, disp
    return None, None


def brand_any(label):
    if not label or label.startswith("Q"):
        return None, None
    name = BRAND_CLEAN.sub("", label).strip(" .,-")
    name = re.split(r"[,(]", name)[0].strip()
    if not name or len(name) < 2:
        return None, None
    slug = C.slugify(name.split()[0])
    disp = name.split()[0].capitalize() if name.split()[0].islower() else name.split()[0]
    return slug, disp


def thumb(img_url):
    if not img_url:
        return ""
    u = img_url.replace("http://", "https://")
    return u + ("&" if "?" in u else "?") + "width=500"


def seed_category(cat, qid, per_brand, restrict, existing, ids, names, brand_ids):
    print(f"[wikidata] {cat} (qid {qid})...")
    data = sparql(qid, per_brand * 50 + 300, require_image=(cat == "phone"))
    rows = data.get("results", {}).get("bindings", [])
    per_brand_count = {}
    added = 0
    for row in rows:
        name = row.get("itemLabel", {}).get("value", "").strip()
        if not name or name.startswith("Q") or len(name) < 2:
            continue
        blabel = row.get("brandLabel", {}).get("value", "")
        slug, disp = (brand_known(blabel) if restrict else brand_any(blabel))
        if not slug and restrict:
            slug, disp = brand_known(name)
        if not slug:
            continue
        if per_brand_count.get(slug, 0) >= per_brand:
            continue
        pid = C.slugify(cat + "-" + name) if cat != "phone" else C.slugify(name)
        norm = re.sub(r"[^a-z0-9]", "", (cat + name).lower())
        if pid in ids or norm in names:
            continue
        date = row.get("date", {}).get("value", "")[:10]
        os_name = row.get("osLabel", {}).get("value", "")
        image = thumb(row.get("image", {}).get("value", ""))
        specs = {"Launch": {"Announced": date or "\u2014"}, "Misc": {"Brand": disp, "Category": cat.title()}}
        if os_name and not os_name.startswith("Q"):
            specs["Platform"] = {"OS": os_name}
        existing["phones"].append({
            "id": pid, "brand": slug, "name": name, "category": cat,
            "image": image, "images": [image] if image else [],
            "releaseDate": date,
            "quickSpecs": {"display": "", "processor": "", "ram": "", "storage": "", "camera": "", "battery": ""},
            "specs": specs,
        })
        ids.add(pid); names.add(norm)
        per_brand_count[slug] = per_brand_count.get(slug, 0) + 1
        if slug not in brand_ids:
            existing["brands"].append({"id": slug, "name": disp, "logo": C.BRAND_EMOJI.get(slug, "\U0001F4F1")})
            brand_ids.add(slug)
        added += 1
    print(f"  added {added} {cat}s")
    return added


def main():
    args = sys.argv[1:]
    existing = C.read_json("specs.json") or {"brands": [], "phones": []}
    ids = {p["id"] for p in existing["phones"]}
    names = {re.sub(r"[^a-z0-9]", "", ((p.get("category", "phone")) + p["name"]).lower()) for p in existing["phones"]}
    brand_ids = {b["id"] for b in existing["brands"]}

    if "--all" in args:
        jobs = [(c, q, pb, r) for c, (q, pb, r) in CATEGORIES.items()]
    else:
        cat = args[args.index("--category") + 1] if "--category" in args else "phone"
        qid = args[args.index("--qid") + 1] if "--qid" in args else CATEGORIES.get(cat, ("Q19723451",))[0]
        pb = int(args[args.index("--per-brand") + 1]) if "--per-brand" in args else CATEGORIES.get(cat, (None, 25))[1]
        restrict = ("--any-brand" not in args) and CATEGORIES.get(cat, (None, None, True))[2]
        jobs = [(cat, qid, pb, restrict)]

    total = 0
    for cat, qid, pb, restrict in jobs:
        try:
            total += seed_category(cat, qid, pb, restrict, existing, ids, names, brand_ids)
        except Exception as e:  # noqa
            print(f"  ! {cat}: {e}")

    C.write_json("specs.json", existing)
    print(f"[wikidata] +{total} items. Total {len(existing['phones'])} across {len(existing['brands'])} brands.")


if __name__ == "__main__":
    main()
