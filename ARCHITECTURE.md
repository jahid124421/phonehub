# PhoneHub — how it works, start to end

## 1. The big picture

```
 ┌──────────────────────────────────────────────────────────────────────────┐
 │                            DATA SOURCES (input)                            │
 │                                                                            │
 │   Specs API              LLM (your key)            Affiliate APIs          │
 │   phone-specs-api        OpenRouter /              Amazon Associates /     │
 │   (self-host or          Groq / Gemini …           Flipkart / PA-API       │
 │    licensed)                                                               │
 └───────┬───────────────────────┬────────────────────────┬──────────────────┘
         │                       │                         │
         ▼                       ▼                         ▼
 ┌────────────────────────────────────────────────────────────────────────────┐
 │                       THE PIPELINE  (phonehub/tools/)                        │
 │                                                                              │
 │  STAGE 1  import_specs.py   ── pulls specs ──►   data/specs.json             │
 │  STAGE 2  content_agent.py  ── AI writes   ──►   data/content.json           │
 │                                reviews, pros/cons, ratings                   │
 │  STAGE 3  price_job.py      ── prices +    ──►   data/prices.json            │
 │                                affiliate Buy links                           │
 │  STAGE 4  build.py          ── merges 1+2+3 ─►   js/data.js + data/merged.json│
 │  STAGE 5  prerender.py      ── bakes HTML  ──►   phone/<id>.html  (per phone) │
 │  STAGE 6  gen_seo.py        ── crawler map ──►   sitemap.xml + robots.txt    │
 │                                                                              │
 │  run_all.py = run 1→2→3→4 (4 auto-runs 5 and 6).   check_keys.py = test keys │
 └───────────────────────────────────────┬──────────────────────────────────────┘
                                          │  (all output is plain static files)
                                          ▼
 ┌────────────────────────────────────────────────────────────────────────────┐
 │                     THE WEBSITE  (static files, phonehub/)                   │
 │                                                                              │
 │  index.html  search.html  compare.html  brands.html  news.html              │
 │  phone/<id>.html  (pre-rendered, JSON-LD baked in)                           │
 │  about / contact / privacy / terms / disclosure / 404                        │
 │  css/styles.css   js/{data.js, common.js, home.js, search.js, phone.js,      │
 │                        compare.js}                                           │
 │  sitemap.xml  robots.txt  netlify.toml                                       │
 └───────────────────────────────────────┬──────────────────────────────────────┘
                                          │  git push / drag-drop
                                          ▼
 ┌────────────────────────────────────────────────────────────────────────────┐
 │            HOST  (Netlify / Vercel / Cloudflare Pages — free)                │
 └───────────────────────────────────────┬──────────────────────────────────────┘
                                          │  HTTPS
                                          ▼
 ┌──────────────────────────┐        ┌────────────────────────────────────────┐
 │        VISITOR            │        │              GOOGLE / BING              │
 │  searches, compares,      │        │  crawls sitemap.xml → reads baked HTML  │
 │  clicks a "Buy" link      │        │  + JSON-LD → shows rich results ★ ₹     │
 └───────────┬──────────────┘        └────────────────────────────────────────┘
             │ clicks Buy / sees ad
             ▼
 ┌────────────────────────────────────────────────────────────────────────────┐
 │                            MONEY  (output)                                   │
 │   Affiliate commission (Amazon/Flipkart)   +   Ad revenue (AdSense, …)       │
 └────────────────────────────────────────────────────────────────────────────┘
```

## 2. The automation loop (hands-off)

```
   GitHub Actions (.github/workflows/update.yml)
   ─ runs daily on a cron schedule ─────────────────────────────┐
        │                                                        │
        ▼                                                        │
   builds config.json from repo secrets                          │
        │                                                        │
        ▼                                                        │
   python run_all.py   (import → content → price → build         │
                        → prerender → seo)                       │
        │                                                        │
        ▼                                                        │
   git commit js/data.js + phone/*.html + sitemap.xml            │
        │                                                        │
        ▼                                                        │
   git push  ──►  host auto-deploys  ──►  live site updated ─────┘
                                          (repeats every day)
```

## 3. What a single visitor request looks like

```
 Visitor opens  /phone/oneplus-12.html
        │
        ▼
 Host returns the pre-rendered HTML instantly
   • full specs, price table, pros/cons, review already in the HTML
   • <script type="application/ld+json"> Product + rating + offers
        │
        ▼
 Browser runs common.js
   • floating compare bar (localStorage)
   • header search
   • cookie-consent banner + footer legal links
        │
        ▼
 Visitor clicks "Buy on Amazon"
   • link carries your affiliate tag  →  commission on purchase
```

## 4. Where to plug in your details

| You provide | Where | Effect |
|-------------|-------|--------|
| LLM key | `my-keys.env` (referenced by `config.json`) | AI writes reviews |
| Specs API URL | `config.json` → `specs_api_base` | real phone data |
| Affiliate tag/id | `config.json` → `affiliate` | Buy links earn money |
| `site_url` | `config.json` | correct sitemap + canonicals |
| Real domain + email | legal pages (replace `[...]` placeholders) | compliant site |
| Repo secrets | GitHub → Settings → Secrets | daily auto-updates |
```
