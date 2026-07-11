# PhoneHub — the automated data pipeline

Four stages turn raw specs into a monetized, SEO-safe site. Each stage
caches its work in `tools/data/`, so re-runs are cheap and the AI only
writes each phone once.

```
STAGE 1  import_specs.py   specs API      -> data/specs.json
STAGE 2  content_agent.py  LLM (your key) -> data/content.json   (reviews, pros/cons, rating)
STAGE 3  price_job.py      affiliate/PAAPI-> data/prices.json     (Buy links, live prices)
STAGE 4  build.py          merge all three-> js/data.js  + data/merged.json
           └─ then automatically runs:
STAGE 5  prerender.py      -> phone/<id>.html   (static pages, content + JSON-LD baked in)
STAGE 6  gen_seo.py        -> sitemap.xml + robots.txt
```

So `python build.py` alone rebuilds the data file, every static phone page,
the sitemap and robots.txt in one shot.

Run everything with one command (or double-click `UPDATE-DATA.bat`):

```bash
cd phonehub/tools
copy config.example.json config.json     # first time only, then edit it
python check_keys.py                      # STEP 0: find a working LLM key
python run_all.py
```

`build.py` also regenerates `sitemap.xml` + `robots.txt` automatically at the
end of every run (via `gen_seo.py`).

### Step 0 — verify a working LLM key (do this first)

```bash
python check_keys.py
```
It tests every key in your env file and prints which providers work, e.g.:
```
  OK groq        : works  (model llama-3.3-70b-versatile)  ->  "ok"
  X  cerebras    : HTTP 403 ...
```
Put the working one in `config.json` (`llm.provider` + `llm.model`). No specs
API needed for this check.

Useful variants:
```bash
python import_specs.py --dry-run     # verify the specs API field mapping
python content_agent.py --limit 5    # only write 5 new phones this run
python content_agent.py --force      # regenerate all AI content
python run_all.py --skip-content     # refresh prices only (fast/frequent)
```

## What each stage needs

| Stage | Requirement | Notes |
|-------|-------------|-------|
| 1 Specs | a running specs API URL in `config.json` | self-host `azharimm/phone-specs-api` (dev) or a licensed API (prod) |
| 2 Content | an LLM key in your env file | default provider `groq`; also supports gemini/openrouter/together/cerebras |
| 3 Prices | affiliate tag / id | **works immediately** as monetized search links; add PA-API keys later for live prices |
| 4 Build | nothing | pure local merge |

## Provider note (important)

If a provider returns **HTTP 403 / Cloudflare error 1010**, that provider is
blocking the machine's IP/signature (common on shared/CI IPs) or the key is
invalid — it is NOT a bug. Switch `llm.provider` in `config.json` to another
key you own, or run from a normal network. Verify a key fast with:

```bash
python content_agent.py --limit 1 --force
```

## Full automation (hands-off)

`.github/workflows/update.yml` runs the whole pipeline daily and commits the
refreshed `js/data.js`. Add these repo secrets (Settings > Secrets > Actions):

- `SPECS_API_BASE` — your hosted specs API URL
- `GROQ_API_KEY` — (or your chosen provider's key)
- `AMAZON_PARTNER_TAG`, `FLIPKART_AFFILIATE_ID` — affiliate ids
- `AMAZON_PAAPI_ACCESS_KEY`, `AMAZON_PAAPI_SECRET_KEY` — optional, live prices

Then any static host (Netlify/Vercel/Cloudflare Pages) auto-deploys on push.

See `SETUP_REAL_DATA.md` for hosting, SEO, and the legal ground rules.
