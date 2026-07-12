#!/usr/bin/env python3
"""
PhoneHub pipeline — STAGE 1: import specs
========================================================================
Pulls phone specs from a `phone-specs-api` compatible instance (the
open-source azharimm/phone-specs-api format, /v2 endpoints) and writes
them to data/specs.json.

USAGE:
    python import_specs.py                # uses config.json
    python import_specs.py --dry-run      # print one phone's raw+mapped JSON, write nothing

Stdlib only. If your API's field names differ, run --dry-run and adjust
map_phone() below (one place).
========================================================================
"""
import json
import re
import sys
import time
import urllib.request
import urllib.parse

import ph_common as C


def api_get(base, path, params=None, retries=3):
    url = base.rstrip("/") + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "PhoneHub-Importer/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"GET {url} failed after {retries} tries: {last}")


def dig_specs(specifications):
    out = {}
    for block in specifications or []:
        title = block.get("title") or block.get("name") or "Misc"
        rows = {}
        for spec in block.get("specs", []):
            key = spec.get("key") or spec.get("name") or ""
            val = spec.get("val")
            if isinstance(val, list):
                val = ", ".join(str(v) for v in val if v)
            rows[key] = val or ""
        if rows:
            out[title] = rows
    return out


def first_spec(specs, section, key_contains=None):
    sec = specs.get(section, {})
    if not sec:
        return ""
    if key_contains is None:
        return next(iter(sec.values()), "")
    for k, v in sec.items():
        if key_contains.lower() in k.lower():
            return v
    return next(iter(sec.values()), "")


def map_phone(detail, brand_slug):
    """Convert one API phone-detail payload into a PhoneHub 'specs' record.
    Adjust the .get() paths here if --dry-run shows a different shape."""
    data = detail.get("data", detail)
    name = data.get("phone_name") or data.get("name") or "Unknown"
    images = data.get("phone_images") or ([data["thumbnail"]] if data.get("thumbnail") else [])
    image = images[0] if images else "https://via.placeholder.com/300x400?text=" + urllib.parse.quote(name)
    specs = dig_specs(data.get("specifications"))
    quick = {
        "display": first_spec(specs, "Display", "Size") or first_spec(specs, "Display"),
        "processor": first_spec(specs, "Platform", "Chipset"),
        "ram": first_spec(specs, "Memory", "Internal"),
        "storage": first_spec(specs, "Memory", "Internal"),
        "camera": first_spec(specs, "Main Camera"),
        "battery": first_spec(specs, "Battery"),
    }
    return {
        "id": C.slugify(name),
        "brand": brand_slug.split("-")[0].lower(),
        "name": name,
        "image": image,
        "releaseDate": data.get("release_date", ""),
        "quickSpecs": quick,
        "specs": specs,
    }


def discover_brand_slug(base, prefix, brand):
    res = api_get(base, f"{prefix}/brands")
    data = res.get("data")
    items = data.get("brands") if isinstance(data, dict) else (data or [])
    for b in items:
        slug = b.get("brand_slug") or b.get("slug") or ""
        name = (b.get("brand_name") or b.get("name") or "").lower()
        # match exact brand name or the leading token of the slug (e.g. 'apple-phones-48')
        if brand.lower() == name or slug.lower().startswith(brand.lower() + "-"):
            return slug, (b.get("brand_name") or brand.title())
    return None, brand.title()


SKIP_RE = re.compile(r"\b(iPad|Tab|Tablet|Watch|Book|Band|Buds|Pad|TV|Glass)\b", re.I)


def list_phones(base, prefix, brand_slug, limit):
    res = api_get(base, f"{prefix}/brands/{brand_slug}")
    data = res.get("data")
    phones = data.get("phones") if isinstance(data, dict) else (data or [])
    phones = [p for p in phones if not SKIP_RE.search(p.get("phone_name", ""))]
    return phones[:limit]


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    cfg = C.load_config()
    base = cfg["specs_api_base"]
    prefix = cfg.get("specs_api_prefix", "/v2")
    want = cfg.get("brands", [])
    cap = int(cfg.get("max_phones_per_brand", 12))

    print(f"[import] specs API: {base}{prefix or '/'}")
    brands_out, phones_out = [], []

    for brand in want:
        try:
            slug, display = discover_brand_slug(base, prefix, brand)
            if not slug:
                print(f"  ! brand '{brand}' not found, skipping")
                continue
            brands_out.append({"id": brand, "name": display, "logo": C.BRAND_EMOJI.get(brand, "📱")})
            listing = list_phones(base, prefix, slug, cap)
            print(f"  {display}: {len(listing)} phones")
            for entry in listing:
                pslug = entry.get("slug") or entry.get("phone_slug")
                if not pslug:
                    continue
                detail = api_get(base, f"{prefix}/{pslug}")
                if dry:
                    print(json.dumps(detail, indent=2)[:1500])
                    print("\n--- mapped ---")
                    print(json.dumps(map_phone(detail, brand), indent=2)[:1500])
                    print("\nDry run complete. Adjust map_phone() if fields look off.")
                    return
                phone = map_phone(detail, brand)
                phone["brand"] = brand
                phones_out.append(phone)
                time.sleep(0.3)
        except Exception as e:  # noqa
            print(f"  ! error on '{brand}': {e}")

    if not phones_out:
        print("No phones imported. Check specs_api_base and try --dry-run.")
        sys.exit(1)

    C.write_json("specs.json", {"brands": brands_out, "phones": phones_out})
    print(f"[import] wrote data/specs.json — {len(phones_out)} phones, {len(brands_out)} brands")


if __name__ == "__main__":
    main()
