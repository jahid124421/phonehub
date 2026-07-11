#!/usr/bin/env python3
"""
PhoneHub — seed specs from a public dataset (one-time / occasional)
========================================================================
Reads a GSMArena-format device dataset (the vigvisw/devicedataparser JSON:
{ "Brand": { "0": {device_name, device_info, device_img_link, device_link,
device_specs:{Section:{key:val}}}, ... }, ... }) and writes data/specs.json
in PhoneHub's schema. Replaces the need to scrape live.

USAGE:
    python seed_dataset.py PATH_TO_devices_data.txt
    python seed_dataset.py PATH --max 15

After running, do:  python build.py   (or run_all.py)
Stdlib only.
========================================================================
"""
import json
import os
import re
import sys

import ph_common as C

# dataset brand key (case-insensitive) -> (slug, display, emoji)
WANTED = [
    ("Apple", "apple", "Apple", "🍎"),
    ("Samsung", "samsung", "Samsung", "📱"),
    ("Google", "google", "Google", "🔵"),
    ("Xiaomi", "xiaomi", "Xiaomi", "🟠"),
    ("OnePlus", "oneplus", "OnePlus", "🔴"),
    ("Oppo", "oppo", "Oppo", "🟢"),
    ("vivo", "vivo", "Vivo", "🔷"),
    ("Realme", "realme", "Realme", "🟡"),
    ("Motorola", "motorola", "Motorola", "🔶"),
    ("Nothing", "nothing", "Nothing", "⚪"),
    ("Asus", "asus", "Asus", "🟣"),
    ("Sony", "sony", "Sony", "⬛"),
    ("Nokia", "nokia", "Nokia", "🔵"),
    ("Honor", "honor", "Honor", "🔵"),
]

MAX_PER_BRAND = 12

# names/categories that are not phones
SKIP_RE = re.compile(r"\b(Tab|Pad|Watch|Book|Band|Buds|TV|Glass|Enjoy Tab|MatePad)\b", re.I)
SKIP_INFO = ("tablet", "smartwatch", "laptop", "wearable", "earbuds", "watch")


def year_of(specs):
    ann = (specs.get("Launch", {}) or {}).get("Announced", "")
    if not isinstance(ann, str):
        ann = str(ann)
    m = re.search(r"(19|20)\d{2}", ann)
    return int(m.group(0)) if m else 0


def is_phone(name, info, specs):
    if SKIP_RE.search(name or ""):
        return False
    low = (info or "").lower()
    if any(w in low for w in SKIP_INFO):
        return False
    # a phone should have Battery + Display sections
    return "Display" in specs and "Battery" in specs


def clean_specs(specs):
    out = {}
    for section, rows in (specs or {}).items():
        if not isinstance(rows, dict):
            continue
        clean = {}
        for k, v in rows.items():
            if not k or k == "NaN":
                continue
            if not isinstance(v, str):   # drop NaN floats / non-string values
                continue
            v = v.strip()
            if v in ("", "N/A", "-", "- "):
                continue
            clean[k] = v
        if clean:
            out[section] = clean
    return out


def first_val(specs, section, key_sub=None):
    sec = specs.get(section, {})
    if not sec:
        return ""
    if key_sub:
        for k, v in sec.items():
            if key_sub.lower() in k.lower():
                return v
    return next(iter(sec.values()), "")


def quick_specs(specs):
    return {
        "display": first_val(specs, "Display", "Size") or first_val(specs, "Display", "Type"),
        "processor": first_val(specs, "Platform", "Chipset") or first_val(specs, "Platform", "CPU"),
        "ram": first_val(specs, "Memory", "Internal"),
        "storage": first_val(specs, "Memory", "Internal"),
        "camera": first_val(specs, "Main Camera"),
        "battery": first_val(specs, "Battery", "Type") or first_val(specs, "Battery"),
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python seed_dataset.py PATH_TO_devices_data.txt [--max N]")
        sys.exit(1)
    src = sys.argv[1]
    cap = MAX_PER_BRAND
    if "--max" in sys.argv:
        cap = int(sys.argv[sys.argv.index("--max") + 1])

    with open(src, "r", encoding="utf-8", errors="replace") as f:
        data = json.load(f)

    # case-insensitive brand lookup
    lower_map = {k.lower(): k for k in data.keys()}

    brands_out, phones_out = [], []
    for ds_key, slug, display, emoji in WANTED:
        real_key = lower_map.get(ds_key.lower())
        if not real_key:
            print(f"  ! brand '{ds_key}' not in dataset, skipping")
            continue
        devices = list(data[real_key].values())
        cand = []
        for d in devices:
            specs = clean_specs(d.get("device_specs", {}))
            name = d.get("device_name", "")
            if not is_phone(name, d.get("device_info", ""), specs):
                continue
            cand.append((year_of(specs), d, specs))
        cand.sort(key=lambda x: x[0], reverse=True)
        chosen = cand[:cap]
        if not chosen:
            continue
        brands_out.append({"id": slug, "name": display, "logo": emoji})
        for _, d, specs in chosen:
            name = d.get("device_name", "").strip()
            full = name if name.lower().startswith(display.lower()) else f"{display} {name}"
            phones_out.append({
                "id": C.slugify(full),
                "brand": slug,
                "name": full,
                "image": d.get("device_img_link", ""),
                "releaseDate": (specs.get("Launch", {}) or {}).get("Announced", ""),
                "quickSpecs": quick_specs(specs),
                "specs": specs,
            })
        print(f"  {display}: {len(chosen)} phones")

    # de-dup ids
    seen, uniq = set(), []
    for p in phones_out:
        if p["id"] in seen:
            continue
        seen.add(p["id"])
        uniq.append(p)

    C.write_json("specs.json", {"brands": brands_out, "phones": uniq})
    print(f"\n[seed] wrote data/specs.json — {len(uniq)} phones across {len(brands_out)} brands")


if __name__ == "__main__":
    main()
