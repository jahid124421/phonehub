#!/usr/bin/env python3
"""
PhoneHub pipeline — STAGE 5: static pre-renderer
========================================================================
Generates a REAL, self-contained HTML page for every phone at
    ../phone/<id>.html
with all content (specs, prices, review, pros/cons) and schema.org
JSON-LD baked into the static HTML. This is what makes the site
"full proof" for SEO: crawlers get complete content with zero JS.

The pages still load common.js + data.js so the compare bar and header
search stay interactive.

Reads data from data/merged.json (pipeline) or falls back to parsing
../js/data.js. Also refreshes sitemap.xml/robots.txt via gen_seo.

USAGE:  python prerender.py
Called automatically at the end of build.py. Stdlib only.
========================================================================
"""
import html
import os

import ph_common as C

OUT_DIR = os.path.join(C.HERE, "..", "phone")
DATA_JS = os.path.join(C.HERE, "..", "js", "data.js")


def rupee(n):
    if not n:
        return "Check price"
    s = str(int(n))
    if len(s) <= 3:
        return "\u20b9" + s
    last3 = s[-3:]
    rest = s[:-3]
    parts = []
    while len(rest) > 2:
        parts.insert(0, rest[-2:])
        rest = rest[:-2]
    if rest:
        parts.insert(0, rest)
    return "\u20b9" + ",".join(parts) + "," + last3


def esc(x):
    return html.escape(str(x if x is not None else ""))


def img_rel(src):
    """Image path as seen from a page inside /phone/ (relative gets ../)."""
    if not src:
        return ""
    if src.startswith(("http://", "https://", "data:")):
        return src
    return "../" + src


def img_abs(src, base):
    """Absolute image URL for og/JSON-LD when a site_url base is known."""
    if not src or src.startswith(("http://", "https://", "data:")):
        return src
    return (base + "/" + src) if base else "../" + src


def lowest_price(phone):
    known = [p.get("price") for p in phone.get("prices", []) if p.get("price")]
    return min(known) if known else (phone.get("basePrice") or 0)


def site_url():
    try:
        cfg = C.load_config()
        return (cfg.get("site_url") or "").rstrip("/")
    except SystemExit:
        return ""


def header_html():
    p = "../"
    return f"""  <header class="site-header">
    <div class="container header-inner">
      <a class="logo" href="{p}index.html">Phone<span>Hub</span></a>
      <nav class="nav-links" id="navLinks">
        <a href="{p}index.html">Home</a>
        <a href="{p}search.html">All Phones</a>
        <a href="{p}brands.html">Brands</a>
        <a href="{p}compare.html">Compare</a>
        <a href="{p}news.html">News</a>
      </nav>
      <form class="search-form" id="searchForm">
        <input type="text" placeholder="Search phones..." aria-label="Search phones">
        <button type="submit">Search</button>
      </form>
      <button class="nav-toggle" id="navToggle" aria-label="Menu">&#9776;</button>
    </div>
  </header>"""


def card_html(phone, brands):
    b = brands.get(phone["brand"], {"name": phone["brand"], "logo": "\U0001F4F1"})
    price = rupee(lowest_price(phone))
    rating = phone.get("rating")
    rating_html = (f'\u2605 {rating} <span>({phone.get("reviewCount", 0)})</span>'
                   if rating else "<span>Not yet rated</span>")
    img = img_rel(phone.get("image") or "")
    fb = img_rel(phone.get("fallbackImg") or "")
    return f"""      <article class="card">
        <a class="card-link" href="{esc(phone['id'])}.html">
          <div class="card-img"><img src="{esc(img)}" alt="{esc(phone['name'])}" loading="lazy" onerror="this.onerror=null;this.src='{esc(fb)}'"></div>
          <div class="card-body">
            <span class="card-brand">{esc(b['logo'])} {esc(b['name'])}</span>
            <h3 class="card-title">{esc(phone['name'])}</h3>
            <div class="card-rating">{rating_html}</div>
            <div class="card-price">{price}</div>
          </div>
        </a>
        <button class="btn-compare" data-compare="{esc(phone['id'])}">\u21c4 Compare</button>
      </article>"""


def render_phone(phone, brands, phones_all, base):
    b = brands.get(phone["brand"], {"name": phone["brand"], "logo": "\U0001F4F1"})
    low = lowest_price(phone)
    name = phone["name"]

    # quick specs
    qs = "".join(
        f'<div class="qs"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div></div>'
        for k, v in phone.get("quickSpecs", {}).items() if v
    )

    # price rows (known first)
    prices = sorted(phone.get("prices", []), key=lambda p: p.get("price") or float("inf"))
    first_known = next((i for i, p in enumerate(prices) if p.get("price")), -1)
    if prices:
        rows = ""
        for i, p in enumerate(prices):
            best = " · Best" if i == first_known else ""
            cls = "best" if i == first_known else ""
            rows += (f'<tr><td>{esc(p.get("store",""))}</td>'
                     f'<td class="{cls}">{rupee(p.get("price"))}{best}</td>'
                     f'<td><a class="btn btn-primary" href="{esc(p.get("url","#"))}" '
                     f'rel="nofollow sponsored" target="_blank">Buy</a></td></tr>')
    else:
        rows = '<tr><td colspan="3" style="color:var(--muted)">No store links yet.</td></tr>'

    pros = "".join(f"<li>{esc(x)}</li>" for x in phone.get("pros", [])) or "<li>&mdash;</li>"
    cons = "".join(f"<li>{esc(x)}</li>" for x in phone.get("cons", [])) or "<li>&mdash;</li>"
    review = (f'<p style="margin:0 0 16px;font-size:15px;line-height:1.6">{esc(phone["review"])}</p>'
              if phone.get("review") else "")

    # spec blocks
    spec_blocks = ""
    for section, kv in phone.get("specs", {}).items():
        trs = "".join(f"<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>" for k, v in kv.items())
        spec_blocks += (f'<div class="spec-block"><h3>{esc(section)}</h3>'
                        f'<table class="spec-table">{trs}</table></div>')

    # similar phones
    similar = sorted([p for p in phones_all if p["id"] != phone["id"]],
                     key=lambda p: abs(lowest_price(p) - low))[:4]
    similar_cards = "\n".join(card_html(p, brands) for p in similar)

    # rating display
    rating = phone.get("rating")
    rating_line = (f'\u2605 {rating} <span style="color:var(--muted);font-size:15px;font-weight:400">'
                   f'based on {phone.get("reviewCount",0)} reviews</span>'
                   if rating else '<span style="color:var(--muted)">Not yet rated</span>')

    # JSON-LD
    canonical = f"{base}/phone/{phone['id']}.html" if base else f"{phone['id']}.html"
    ld = {
        "@context": "https://schema.org", "@type": "Product", "name": name,
        "image": img_abs(phone.get("image", ""), base), "brand": {"@type": "Brand", "name": b["name"]},
        "description": phone.get("review") or f"{name} specifications and price.",
    }
    if rating:
        ld["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": str(rating),
                                 "reviewCount": str(phone.get("reviewCount", 1)),
                                 "bestRating": "5", "worstRating": "1"}
    if low:
        ld["offers"] = {"@type": "AggregateOffer", "priceCurrency": "INR",
                        "lowPrice": str(low), "offerCount": str(len(phone.get("prices", [])) or 1)}
    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{base}/index.html" if base else "../index.html"},
            {"@type": "ListItem", "position": 2, "name": b["name"], "item": f"{base}/search.html?brand={phone['brand']}" if base else f"../search.html?brand={phone['brand']}"},
            {"@type": "ListItem", "position": 3, "name": name},
        ],
    }
    import json as _json
    ld_script = f'<script type="application/ld+json">{_json.dumps(ld)}</script>'
    bc_script = f'<script type="application/ld+json">{_json.dumps(breadcrumb)}</script>'

    desc = (phone.get("review") or
            f"{name}: {phone.get('quickSpecs',{}).get('display','')}, "
            f"{phone.get('quickSpecs',{}).get('processor','')}, "
            f"{phone.get('quickSpecs',{}).get('camera','')}.").strip()
    img = img_rel(phone.get("image") or "")
    fb_img = img_rel(phone.get("fallbackImg") or "")
    og_img = img_abs(phone.get("image") or "", base)
    gallery_imgs = phone.get("images") or ([phone.get("image")] if phone.get("image") else [])
    thumbs = "".join(
        f'<img src="{esc(img_rel(u))}" alt="" loading="lazy" '
        f'onclick="var m=document.getElementById(\'mainImg\');if(m)m.src=this.src" '
        f'onerror="this.style.display=\'none\'">'
        for u in gallery_imgs[:6]
    )
    thumbs_html = f'<div class="thumbs">{thumbs}</div>' if len(gallery_imgs) > 1 else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(name)} — Specs, Price &amp; Review | PhoneHub</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{esc(canonical)}">
  <meta property="og:title" content="{esc(name)} — PhoneHub">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:image" content="{esc(og_img)}">
  <meta property="og:type" content="product">
  <script>(function(){{try{{var t=localStorage.getItem("ph_theme")||((window.matchMedia&&matchMedia("(prefers-color-scheme: light)").matches)?"light":"dark");document.documentElement.setAttribute("data-theme",t);}}catch(e){{document.documentElement.setAttribute("data-theme","dark");}}}})();</script>
  <link rel="stylesheet" href="../css/styles.css">
  {ld_script}
  {bc_script}
</head>
<body>
{header_html()}
  <main class="container">
    <p class="crumb"><a href="../index.html">Home</a> / <a href="../search.html?brand={esc(phone['brand'])}">{esc(b['name'])}</a> / {esc(name)}</p>

    <div class="phone-top">
      <div class="phone-gallery"><img id="mainImg" src="{esc(img)}" alt="{esc(name)}" onerror="this.onerror=null;this.src='{esc(fb_img)}'"></div>{thumbs_html}
      <div class="phone-info">
        <h1>{esc(name)}</h1>
        <div class="phone-meta">{esc(b['logo'])} {esc(b['name'])} · Released {esc(phone.get('releaseDate',''))}</div>
        <div class="big-rating">{rating_line}</div>
        <div style="margin:14px 0;font-size:26px;font-weight:800">{rupee(low)} <span style="font-size:14px;color:var(--muted);font-weight:400">lowest price</span></div>
        <button class="btn btn-ghost" data-compare="{esc(phone['id'])}">\u21c4 Add to compare</button>
        <div class="quick-specs">{qs}</div>
      </div>
    </div>

    <div class="ad-slot">Advertisement <small>in-content responsive unit</small></div>

    <section>
      <h2>\U0001F4B0 Price comparison</h2>
      <table class="price-table">
        <thead><tr><th>Store</th><th>Price</th><th></th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </section>

    <section>
      <h2>Expert verdict</h2>
      {review}
      <div class="proscons">
        <div class="pros"><h4>\U0001F44D Pros</h4><ul>{pros}</ul></div>
        <div class="cons"><h4>\U0001F44E Cons</h4><ul>{cons}</ul></div>
      </div>
    </section>

    <section>
      <h2>Full specifications</h2>
      {spec_blocks}
    </section>

    <section>
      <div class="section-head"><h2>Similar phones</h2></div>
      <div class="grid">
{similar_cards}
      </div>
    </section>

    <section>
      <h2>\U0001F4AC Discussion</h2>
      <p style="color:var(--muted);margin-top:-6px">Ask questions or share your experience with the {esc(name)}.</p>
      <div id="giscusBox"></div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container"><div class="footer-bottom">© <span id="year"></span> PhoneHub.</div></div>
  </footer>

  <script>window.PHONE_PREFIX = ""; window.LINK_PREFIX = "../";</script>
  <script src="../js/data.js"></script>
  <script src="../js/common.js"></script>
  <script>var y=document.getElementById("year"); if(y) y.textContent=new Date().getFullYear();</script>
</body>
</html>
"""


def main():
    data = C.read_json("merged.json")
    if not data:
        data = C.load_site_data(DATA_JS)
    phones = data["phones"]
    brands = {b["id"]: b for b in data["brands"]}
    base = site_url()
    if "your-domain.example" in base:
        base = ""  # placeholder -> use relative canonical

    os.makedirs(OUT_DIR, exist_ok=True)
    for p in phones:
        htmlp = render_phone(p, brands, phones, base)
        with open(os.path.join(OUT_DIR, f"{p['id']}.html"), "w", encoding="utf-8") as f:
            f.write(htmlp)
    print(f"[prerender] wrote {len(phones)} static pages -> phone/*.html")


if __name__ == "__main__":
    main()
