# Push PhoneHub to GitHub + turn on Pages

Push the **contents of the `phonehub` folder** as the repository root, so the
site is served at `https://USERNAME.github.io/REPO/`.

## 1. Create the repo on GitHub
- Go to https://github.com/new
- Name it e.g. `phonehub`  → **Public** (public repos get unlimited free
  Actions minutes) → **Create repository**. Don't add a README.

## 2. Push from your PC
Open a terminal **inside the phonehub folder**:
```bash
cd "C:\Users\96650\OneDrive\Desktop\AI_BA_WORKSPACE\phonehub"
git init
git add .
git commit -m "PhoneHub: initial site + automation"
git branch -M main
git remote add origin https://github.com/USERNAME/phonehub.git
git push -u origin main
```
(Replace `USERNAME`. `tools/config.json` and key files are git-ignored, so no
secrets are pushed.)

## 3. Add your secrets
Repo → **Settings → Secrets and variables → Actions → New repository secret**.
Add:

| Secret | Value |
|--------|-------|
| `OPENROUTER_API_KEY` | your working key |
| `SITE_URL` | `https://USERNAME.github.io/phonehub` |
| `AMAZON_PARTNER_TAG` | your Amazon tag (optional) |
| `FLIPKART_AFFILIATE_ID` | optional |

> No `SPECS_API_BASE` needed — the workflow runs the specs API inside GitHub
> Actions for free during each build. No Railway, no server, no cost.

## 4. Turn on Pages
Repo → **Settings → Pages → Build and deployment → Source = GitHub Actions**.

## 5. Run it
Repo → **Actions** tab → "Build data & deploy to GitHub Pages" → **Run workflow**.
It will:
1. spin up the specs API inside the runner (free) and pull specs
2. write AI reviews (OpenRouter) + affiliate prices
3. build the site + static phone pages + sitemap
4. commit the fresh data
5. deploy to Pages

When it finishes, your site is live at **https://USERNAME.github.io/phonehub/**.
After that it re-runs and redeploys automatically every day.

## Notes
- The `mastertools/` folder inside phonehub is unrelated to this project — you
  can delete it before pushing if you don't want it in the repo.
- The specs API runs inside GitHub Actions each build — nothing to host, $0.
- First deploy uses the current sample data if scraping is blocked — the site
  still goes live, then fills with real data on a run that succeeds.
- `RAILWAY-SETUP.md` is now OPTIONAL — only if GitHub's IPs ever get blocked by
  the specs source and you want a more reliable fetch.
```
