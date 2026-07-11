#!/usr/bin/env python3
"""
PhoneHub — local placeholder image generator
========================================================================
Creates a clean, branded SVG image per phone in ../img/<id>.svg so every
phone always shows a picture with NO external dependency (external image
hosts go down or block hotlinking). Used by build.py.

A phone keeps its real image if it has a usable http(s) URL that isn't a
known-dead placeholder host; otherwise it gets a local SVG.
========================================================================
"""
import html
import os

import ph_common as C

IMG_DIR = os.path.join(C.HERE, "..", "img")

BRAND_COLORS = {
    "apple": "#555555", "samsung": "#1428a0", "google": "#4285f4",
    "xiaomi": "#ff6900", "oneplus": "#eb0028", "nothing": "#111111",
    "vivo": "#415fff", "realme": "#ffc915", "oppo": "#1ba784",
    "motorola": "#5c92fc", "asus": "#00539b", "sony": "#000000",
}

DEAD_HOSTS = ("placeholder.com", "via.placeholder.com")


def _wrap(text, width=14):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= width:
            cur = (cur + " " + w).strip()
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:4]


def make_svg(name, brand):
    color = BRAND_COLORS.get(brand, "#4c7dff")
    initial = html.escape((name.strip()[:1] or "?").upper())
    lines = _wrap(name)
    # vertically center the name block
    start_y = 300 - (len(lines) - 1) * 14
    tspans = "".join(
        f'<tspan x="150" y="{start_y + i*30}">{html.escape(l)}</tspan>'
        for i, l in enumerate(lines)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="300" height="400" viewBox="0 0 300 400">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{color}"/>
      <stop offset="1" stop-color="#0f1115"/>
    </linearGradient>
  </defs>
  <rect width="300" height="400" fill="url(#g)"/>
  <rect x="90" y="70" width="120" height="150" rx="16" fill="rgba(255,255,255,0.12)" stroke="rgba(255,255,255,0.25)"/>
  <text x="150" y="165" font-family="Segoe UI, Arial, sans-serif" font-size="64" font-weight="700" fill="#ffffff" text-anchor="middle">{initial}</text>
  <text font-family="Segoe UI, Arial, sans-serif" font-size="20" font-weight="600" fill="#ffffff" text-anchor="middle">{tspans}</text>
</svg>
"""


def good_image(url):
    return bool(url) and url.startswith(("http://", "https://")) and \
        not any(h in url for h in DEAD_HOSTS)


def ensure_image(phone):
    """Return a usable image path for the phone, creating a local SVG if needed."""
    img = phone.get("image", "")
    if good_image(img):
        return img
    os.makedirs(IMG_DIR, exist_ok=True)
    fname = f"{phone['id']}.svg"
    with open(os.path.join(IMG_DIR, fname), "w", encoding="utf-8") as f:
        f.write(make_svg(phone.get("name", "Phone"), phone.get("brand", "")))
    return "img/" + fname


if __name__ == "__main__":
    data = C.read_json("merged.json") or C.load_site_data(os.path.join(C.HERE, "..", "js", "data.js"))
    n = 0
    for p in data["phones"]:
        if not good_image(p.get("image", "")):
            ensure_image(p)
            n += 1
    print(f"[images] generated {n} local placeholder images -> img/*.svg")
