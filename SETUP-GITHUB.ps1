# ============================================================
#  PhoneHub — one-shot GitHub setup
#  Run this INSIDE the phonehub folder:
#     Right-click > Run with PowerShell   (or:  ./SETUP-GITHUB.ps1)
#
#  It sets your git identity, commits, connects your repo, and pushes.
#  When it pushes, a GitHub login window opens in YOUR browser — that's
#  how you authenticate securely. No credentials are shared with anyone.
# ============================================================

Write-Host "`n=== PhoneHub GitHub setup ===`n" -ForegroundColor Cyan

# 1. Identity
$name  = git config user.name
$email = git config user.email
if (-not $name)  { $name  = Read-Host "Your name (for git commits)"; git config user.name  "$name" }
if (-not $email) { $email = Read-Host "Your GitHub email";           git config user.email "$email" }
Write-Host "Identity: $name <$email>" -ForegroundColor Green

# 2. Make sure we're a repo on main
if (-not (Test-Path ".git")) { git init -b main | Out-Null }
git checkout -B main | Out-Null

# 3. Stage + commit
git add .
git commit -m "PhoneHub: site + automation" 2>$null
if ($LASTEXITCODE -ne 0) { Write-Host "Nothing new to commit (that's fine)." -ForegroundColor Yellow }

# 4. Remote
Write-Host "`nCreate an EMPTY public repo first at https://github.com/new (name it e.g. phonehub, no README)." -ForegroundColor Yellow
$user = Read-Host "Your GitHub username"
$repo = Read-Host "Repo name (default: phonehub)"
if (-not $repo) { $repo = "phonehub" }
$url = "https://github.com/$user/$repo.git"

git remote remove origin 2>$null
git remote add origin $url
Write-Host "Remote set to $url" -ForegroundColor Green

# 5. Push (this opens the GitHub login in your browser the first time)
Write-Host "`nPushing... a browser login may open — approve it.`n" -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -eq 0) {
  Write-Host "`nDONE. Now in the GitHub website:" -ForegroundColor Green
  Write-Host "  1. Settings > Secrets and variables > Actions:" -ForegroundColor White
  Write-Host "       OPENROUTER_API_KEY = your key"
  Write-Host "       SITE_URL           = https://$user.github.io/$repo"
  Write-Host "  2. Settings > Pages > Source = 'GitHub Actions'"
  Write-Host "  3. Actions tab > Run 'Build data & deploy to GitHub Pages'"
  Write-Host "`n  Your site will be live at: https://$user.github.io/$repo/`n" -ForegroundColor Cyan
} else {
  Write-Host "`nPush failed. Common fixes:" -ForegroundColor Red
  Write-Host "  - Make sure the repo exists and is empty at $url"
  Write-Host "  - If it asks to authenticate, complete the browser login and re-run."
}
