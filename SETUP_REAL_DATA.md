# PhoneHub — Making It Real (automation runbook)

This is the step-by-step for turning the demo into a live site with real,
auto-updating data. Read the "Legal reality" section first — it decides
which path you take.

---

## Legal reality (read this)

You **cannot** copy GSMArena / 91mobiles / Smartprix / MobileDokan content
and republish it on a commercial ad site. It is copyrighted, violates their
Terms of Service, and Google penalizes duplicate content (which destroys the
ad/traffic income you want). Scraping tools are fine for **learning and
seeding a dev database**, not for running a public clone.

The version that actually earns and survives:

| Layer | Legal source | Earns money? |
|-------|--------------|--------------|
| Specs | Licensed API (TechSpecs, mobileapi.dev) **or** your own data entry | No (cost) |
| Prices + Buy buttons | **Affiliate APIs** (Amazon PA-API, Flipkart Affiliate) | **Yes — commissions** |
| Reviews / guides | **Your own original writing** | Yes — SEO traffic → ads |

Your moat isn't "all their data merged." It's original content + live prices
+ a better experience. That's what ranks and pays.

---

## Architecture

```
[ Specs source ]           [ Price source ]
 self-hosted API   ┐        Amazon PA-API ┐
 or licensed API   ├──►  importer  ◄───────┤ Flipkart Affiliate
 or CSV dataset    ┘     (tools/)          ┘
                             │
                             ▼
                        js/data.js  ──►  static PhoneHub site  ──► host (Netlify/Vercel/Cloudflare Pages)
                             ▲
                        scheduled (Task Scheduler / cron / GitHub Actions)
```

Static generation keeps it fast + SEO-friendly. For thousands of phones,
graduate to a database + server-rendered framework (see "Scaling up").

---

## Step 1 — Get a specs source running

### Option A (fastest for dev): self-host the open-source specs API
Repo: `azharimm/phone-specs-api` (Node.js, serves GSMArena-format JSON).

```bash
git clone https://github.com/azharimm/phone-specs-api
cd phone-specs-api
npm install
npm start          # serves on http://localhost:3000, endpoints under /v2
```
Test: open `http://localhost:3000/v2/brands` in a browser.

> This scrapes GSMArena. Use it to **seed and learn**, not to power a public
> commercial clone. For production, use Option B.

Other open-source options found:
- `nordmarin/gsmarena-api`
- `ahthserhsluk/GSMARENA-Mobile-Data-Scapper` (Playwright + BeautifulSoup)
- `BssMsi/mobile-specs-webscraper` (Scrapy, ~10k devices)

### Option B (production): licensed specs API
- **TechSpecs API** — `github.com/techspecs/techspecs-api`
- **mobileapi.dev** — 12 spec categories, per-category endpoints
- **Apify** GSMArena / phones-specs-db actors — pay-per-run
- Downloadable datasets: Teoalida (13k+ models), Back4App, Kaggle

Point the importer at whichever base URL you choose.

---

## Step 2 — Import specs into the site

```bash
cd phonehub/tools
copy config.example.json config.json      # (Windows)  or: cp on mac/linux
# edit config.json -> set specs_api_base, brands, max_phones_per_brand
python import_specs.py --dry-run           # verify field mapping first
python import_specs.py                     # writes ../js/data.js
```

`--dry-run` prints the raw API JSON + how it maps. If your provider's field
names differ, adjust `map_phone()` in `import_specs.py` (one place).

---

## Step 3 — Add live prices + affiliate links (the money part)

1. Sign up: **Amazon Associates** → get PA-API keys. **Flipkart Affiliate**
   → get affiliate ID + token. (Both need an active account in good standing.)
2. Node client: `jorgerosal/amazon-paapi`. Python: `python-amazon-paapi`.
3. Write a `price_job` that, for each phone, searches the affiliate API by
   model name, and fills each phone's `prices: [{store, price, url}]` with the
   affiliate URL. Schedule it more often than specs (prices change daily).

> I can build this price job next once you have the affiliate keys — tell me
> Node or Python and which stores.

---

## Step 4 — Automate (the "agents")

Pick one:

- **Windows Task Scheduler** — run `python import_specs.py` daily. Simplest.
- **GitHub Actions** — cron workflow that runs the importer and commits the
  updated `js/data.js`; host auto-deploys. Fully hands-off, free.
- **n8n** (self-hosted workflow automation, open source) — visual scheduler
  that can also call an LLM to auto-write phone descriptions/news.
- **AI content agent** — a scheduled script that calls an LLM (you already
  have keys in the workspace) to draft original review text + buying guides
  from the raw specs. This is what makes the content original and SEO-safe.

Example GitHub Actions cron (`.github/workflows/update.yml`):
```yaml
on:
  schedule: [{ cron: "0 3 * * *" }]   # daily 03:00 UTC
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: python phonehub/tools/import_specs.py
      - run: |
          git config user.name "bot"
          git config user.email "bot@users.noreply.github.com"
          git commit -am "auto: refresh phone data" || echo "no changes"
          git push
```

---

## Step 5 — Host it + SEO

- **Host**: Netlify / Vercel / Cloudflare Pages (free tier, HTTPS, fast).
- **SEO essentials**: unique title/description per phone (already done),
  `sitemap.xml`, schema.org `Product`/`AggregateRating`/`Review` markup,
  submit to Google Search Console.
- **Monetize**: affiliate links on Buy buttons + Google AdSense (later Ezoic
  / Mediavine as traffic grows). Add a privacy policy + cookie consent first
  (required for AdSense/GDPR).

---

## Scaling up (when static isn't enough)

Thousands of phones with per-store live prices need a backend:
- DB: PostgreSQL or MongoDB
- API/SSR: Next.js or Astro (great SEO) / FastAPI
- Swap `js/data.js` for `fetch()` to your API; keep the importer as the
  ingestion pipeline into the DB.

---

## Repo shortlist (all found via research)

Specs: `azharimm/phone-specs-api`, `techspecs/techspecs-api`,
`nordmarin/gsmarena-api`, `BssMsi/mobile-specs-webscraper`,
`ahthserhsluk/GSMARENA-Mobile-Data-Scapper`
Prices/affiliate: `jorgerosal/amazon-paapi`, `python-amazon-paapi`,
`christophby/amazon-affiliate-api`
Automation: GitHub Actions (cron), n8n (self-hosted)
