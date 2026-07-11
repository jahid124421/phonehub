# PhoneHub — 4-in-1 Phone Specs / Prices / Reviews Site

A working foundation that combines the core features of GSMArena, 91mobiles,
Smartprix and MobileDokan into one site:

- **Phone database** with detailed, GSMArena-style spec sheets
- **Search + filters** (brand, price, rating) and sorting
- **Side-by-side comparison** (up to 4 phones, differences highlighted)
- **Price comparison** across multiple stores (Smartprix/91mobiles style)
- **Reviews / ratings + pros & cons** verdicts
- **News & buying guides** feed
- **Ad slots** placed for monetization
- Fully **responsive** + SEO-friendly page titles/descriptions

## Run it locally

It's a static site — just open `index.html` in a browser, or serve it:

```
# from the phonehub/ folder
python -m http.server 8000
# then open http://localhost:8000
```

## Project structure

```
phonehub/
  index.html        Home (popular, latest, brands, news)
  search.html       All phones + filters + sort
  phone.html        Phone detail (specs, prices, reviews)
  compare.html      Side-by-side comparison
  brands.html       Browse by brand
  news.html         News & guides
  css/styles.css    All styling (dark theme, responsive)
  js/
    data.js         The phone dataset (edit this to add phones)
    common.js       Shared helpers (cards, compare bar, search)
    home.js         Homepage logic
    search.js       Filter/sort logic
    phone.js        Detail page logic (+ schema.org rich-result data)
    compare.js      Comparison logic
  404.html          Friendly not-found page
  sitemap.xml       Auto-generated (all pages + every phone)
  robots.txt        Auto-generated (points crawlers to the sitemap)
  tools/            The automation pipeline (see PIPELINE.md)
    check_keys.py   Test which LLM keys work
    import_specs.py Stage 1: pull specs
    content_agent.py Stage 2: AI reviews/pros/cons/ratings
    price_job.py    Stage 3: affiliate links + live prices
    build.py        Stage 4: merge -> js/data.js
    gen_seo.py      Generate sitemap.xml + robots.txt
    run_all.py      Run the whole pipeline
```

Add a phone = copy one object in `js/data.js` and change the fields.

## Making it real (roadmap)

This foundation uses sample data. To turn it into a live, revenue-generating
site, here's the honest path:

### 1. Get real, legal data
You **cannot** copy content from GSMArena/91mobiles etc. (copyright + Google
duplicate-content penalties). Legitimate options:
- **Licensed spec APIs**: e.g. paid phone-spec datasets / product APIs.
- **Affiliate product feeds**: Amazon Product Advertising API, Flipkart
  Affiliate, etc. — these give you prices *and* your monetization link.
- **Manual/assisted data entry** for a focused niche (a strong niche beats a
  thin clone of everything).

### 2. Add a backend + database
Static JSON won't scale to thousands of phones with live prices. Recommended:
- **Database**: PostgreSQL or MongoDB for phones, specs, prices, reviews.
- **Backend**: Node.js/Express or Python/FastAPI serving a JSON API.
- **Price updater**: scheduled job that refreshes prices from affiliate feeds.
- Swap `js/data.js` for `fetch()` calls to your API.

### 3. SEO (this is where the traffic/money comes from)
- Server-side render pages (Next.js / Astro) so Google indexes real HTML.
- Unique titles/descriptions per phone (already scaffolded here).
- Add structured data (`Product`, `AggregateRating`, `Review` schema.org).
- Generate a `sitemap.xml` and submit to Google Search Console.

### 4. Monetization
- **Affiliate links** on every "Buy" button (biggest earner for these sites).
- **Display ads**: Google AdSense to start, then Ezoic/Mediavine/AdThrive as
  traffic grows. Ad slots are already marked in the layout.
- Keep ads/affiliate disclosures compliant (FTC + AdSense policies).

### 5. Legal must-haves before launch
- Privacy policy + cookie consent (required for AdSense/GDPR).
- Affiliate disclosure.
- Your own original content and images (or properly licensed ones).

## Suggested next step
Pick a niche and a data source. Tell me which (e.g. "Amazon affiliate feed +
Node/Express + Postgres") and I'll wire up the backend and swap the sample
data for live data.
```
