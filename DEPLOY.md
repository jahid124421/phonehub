# PhoneHub — launch online

The site is a static folder, so hosting is free and fast. Pick a path.

---

## Fastest: Netlify Drop (no account setup, ~2 minutes)

1. Go to https://app.netlify.com/drop
2. Drag the whole **`phonehub`** folder onto the page.
3. Done — you get a live URL like `https://random-name.netlify.app`.

Good for a first look. For a real site with auto-updates, use the Git path below.

---

## Recommended: Git + auto-deploy (Netlify / Vercel / Cloudflare Pages)

1. Push this project to a GitHub repo.
2. In your host, "Add new site" → "Import from Git" → pick the repo.
3. Set the **publish / output / root directory** to `phonehub`.
   (No build command needed — it's already static.)
4. Deploy. Every `git push` now redeploys automatically.

Host-specific "publish directory" setting:
- **Netlify**: Base directory `phonehub` (the included `netlify.toml` handles the rest)
- **Vercel**: Root Directory = `phonehub`, Framework preset = "Other"
- **Cloudflare Pages**: Build output directory = `phonehub`, build command empty

---

## After it's live (do these, in order)

### 1. Set your real domain in the data
Edit `phonehub/tools/config.json`:
```json
"site_url": "https://your-real-domain.com"
```
Then re-run the pipeline so canonicals + sitemap use the real domain:
```bash
cd phonehub/tools
python build.py      # rebuilds data.js, static pages, sitemap, robots
```
(Or just `python run_all.py` for a full data refresh.)

### 2. Point crawlers at your sitemap
- Add your domain to **Google Search Console** (https://search.google.com/search-console).
- Submit `https://your-domain.com/sitemap.xml`.
- Do the same in **Bing Webmaster Tools**.

### 3. Turn on the money
- **Affiliate**: put your Amazon Associates tag + Flipkart affiliate id in
  `config.json`, re-run `python run_all.py`. Every Buy button becomes a
  commission link. (See `SETUP_REAL_DATA.md` for PA-API live prices.)
- **Ads**: apply to Google AdSense once you have real content + traffic.
  The ad slots are already placed in the layout. Graduate to Ezoic /
  Mediavine as traffic grows.

### 4. Legal (required before AdSense approval)
- Add a **Privacy Policy** and **cookie consent** banner (GDPR + AdSense rule).
- Add an **affiliate disclosure** line in the footer.
- Use only your own / licensed images and the AI-written text (already original).

---

## Keeping it fresh automatically

`.github/workflows/update.yml` runs the full pipeline daily and commits the
new data + static pages; your host redeploys on the push. Add these GitHub
repo secrets (Settings → Secrets and variables → Actions):

| Secret | Value |
|--------|-------|
| `OPENROUTER_API_KEY` | your working LLM key |
| `SITE_URL` | `https://your-domain.com` |
| `SPECS_API_BASE` | URL of your hosted phone-specs-api |
| `AMAZON_PARTNER_TAG` | Amazon Associates tag |
| `FLIPKART_AFFILIATE_ID` | optional |
| `AMAZON_PAAPI_ACCESS_KEY` / `AMAZON_PAAPI_SECRET_KEY` | optional, live prices |

That's it — the site runs and updates itself.
