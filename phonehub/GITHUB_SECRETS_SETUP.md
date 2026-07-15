# GitHub Actions Secrets Setup

## Add These Secrets to GitHub

Go to: **https://github.com/jahid124421/phonehub/settings/secrets/actions**

Click **"New repository secret"** for each:

### Required Secrets

| Secret Name | Value | Notes |
|-------------|-------|-------|
| `SCRAPERAPI_KEY` | `afaad3915b7af8e2c870eb553fe03ccb` | Bypass GSMArena blocks |
| `RAINFOREST_API_KEY` | `AFBE6DC1BD434953BDBE2DE5C087C283` | Real Amazon prices |
| `PEXELS_API_KEY` | `zq1IpMu2JDgy9J636d61vnSSqXgKpMkrTyEnlqoJVQXIokrlkhQIfaGQ` | Product images |
| `PIXABAY_API_KEY` | `55412861-a4ab9cc546398a2c9c06e0cbf` | Backup images |
| `NEWSAPI_KEY` | `ea5d3f63e0f74c2cb89755f3e1505326` | Tech news |
| `OPENROUTER_API_KEY` | Get from `../../ai-bots-package/my-keys.env` | AI reviews |

## How to Add Secrets

1. Go to your repo: https://github.com/jahid124421/phonehub
2. Click **Settings** (top right)
3. In left sidebar: **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Name: Enter secret name (e.g., `SCRAPERAPI_KEY`)
6. Value: Paste the API key
7. Click **Add secret**
8. Repeat for all 6 secrets

## Verify Setup

After adding secrets, go to:
**https://github.com/jahid124421/phonehub/actions**

You should see the workflow **"PhoneHub Auto Update & Deploy"**

## Manual Trigger

1. Go to Actions tab
2. Click "PhoneHub Auto Update & Deploy"
3. Click "Run workflow"
4. Choose branch: main
5. Optional: Set limit (default 100)
6. Click "Run workflow"

## Automatic Schedule

The workflow runs automatically:
- **Daily at 2 AM UTC**
- **On every push to main**
- **Manual trigger anytime**

## What It Does

1. ✅ Seeds new products from Wikidata
2. ✅ Fetches real Amazon prices  
3. ✅ Downloads high-quality images
4. ✅ Generates AI reviews
5. ✅ Fetches latest tech news
6. ✅ Builds site files
7. ✅ Commits and pushes changes
8. ✅ Triggers Cloudflare Pages deploy

## Cloudflare Pages Setup

1. Go to https://dash.cloudflare.com
2. Click **Pages**
3. Click **Create a project**
4. Connect to GitHub → Select `jahid124421/phonehub`
5. Build settings:
   - Framework preset: **None**
   - Build command: *leave empty*
   - Build output directory: `/`
6. Click **Save and Deploy**

Done! Cloudflare will auto-deploy on every GitHub push.

## Monitoring

- **GitHub Actions**: https://github.com/jahid124421/phonehub/actions
- **Cloudflare Pages**: https://dash.cloudflare.com → Pages
- **Live Site**: https://jahid124421.github.io/phonehub

## Troubleshooting

### "Secret not found" error
- Check secret names match exactly (case-sensitive)
- Re-add the secret if needed

### "API key invalid" error  
- Test keys locally first
- Check quotas haven't been exceeded

### "Git push failed" error
- Check repo permissions
- Ensure `GITHUB_TOKEN` has write access (auto-enabled)

## Cost

**All FREE tiers!**
- GitHub Actions: 2,000 minutes/month (enough for daily runs)
- API quotas: See IMPLEMENTATION_COMPLETED.md

**Total: $2/month** (just OpenRouter for AI reviews)
