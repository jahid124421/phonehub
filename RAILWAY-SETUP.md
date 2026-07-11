# Run the specs API on Railway (the trial month)

Railway's 30-day / $5 trial can run the Node specs API for about a month.
This gives your GitHub Action a real URL to pull phone specs from. When the
trial ends, swap the specs source (see "When the trial ends" below).

## Steps

1. **Fork the specs API** on GitHub:
   https://github.com/azharimm/phone-specs-api  →  click **Fork**.

2. Go to https://railway.com  →  sign in with GitHub  →  start the free trial.

3. **New Project → Deploy from GitHub repo** → pick your fork of
   `phone-specs-api`. Railway auto-detects Node.js and runs `npm install`.

4. If it doesn't start automatically, set the start command in
   **Settings → Deploy → Start Command**:
   ```
   npm start
   ```
   (The app must listen on `process.env.PORT` — Railway sets `PORT` for you.
   azharimm's app already does this.)

5. **Settings → Networking → Generate Domain**. You'll get a public URL like:
   ```
   https://phone-specs-api-production-xxxx.up.railway.app
   ```

6. **Test it** — open in a browser:
   ```
   https://YOUR-URL.up.railway.app/v2/brands
   ```
   You should see JSON with a list of brands. 

7. Copy that base URL — it becomes your **`SPECS_API_BASE`** GitHub secret
   (see PUSH-TO-GITHUB.md). Use the base only, no trailing `/v2`.

## Watch your usage

- The trial is ~$5 of credit or 30 days, whichever comes first.
- A tiny API like this uses very little, but check **Railway → Usage** now
  and then so it doesn't surprise you.
- If Cloudflare blocks the scraper on Railway too (rare, but possible), tell
  me and we'll switch to the dataset-seed method (fully free, no scraping).

## When the trial ends (your migration options)

Since the specs rarely change, the cheapest long-term move is to **stop
needing the server at all**:

- **Option A (recommended, free forever):** run the importer once now while
  Railway is up, commit the resulting `tools/data/specs.json` to your repo.
  After that the daily Action only refreshes **prices + AI content** and never
  needs the specs API again. New phones get added occasionally by a manual run.
- **Option B:** move the specs API to another free-tier host, or a $5/mo box.
- **Option C:** switch to a licensed specs API URL (just change the secret).

Nothing else in the project changes — only the `SPECS_API_BASE` secret.
