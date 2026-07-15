@echo off
REM PhoneHub - One-Click Deploy
REM This script runs the full pipeline and deploys to GitHub + Cloudflare

echo.
echo ========================================
echo   PHONEHUB AUTO-DEPLOY
echo ========================================
echo.
echo This will:
echo  1. Seed catalog from Wikidata
echo  2. Fetch real prices from Amazon
echo  3. Get high-quality images
echo  4. Generate AI reviews  
echo  5. Fetch latest news
echo  6. Build everything
echo  7. Push to GitHub
echo  8. Auto-deploy to Cloudflare Pages
echo.
echo Estimated time: 10-15 minutes
echo.

set /p confirm="Continue? (Y/N): "
if /i not "%confirm%"=="Y" goto :end

cd tools

echo.
echo [1/7] Seeding catalog from Wikidata...
python wikidata_seed.py --all

echo.
echo [2/7] Fetching real Amazon prices...
python price_job.py

echo.
echo [3/7] Generating AI reviews...
python content_agent.py --limit 50

echo.
echo [4/7] Fetching latest tech news...
python news_fetch.py

echo.
echo [5/7] Building site...
python build.py

cd ..

echo.
echo [6/7] Committing changes...
git add -A
git commit -m "auto: refresh data %date% %time%"

echo.
echo [7/7] Pushing to GitHub...
git push origin main

if errorlevel 1 (
    echo.
    echo ERROR: Git push failed
    echo Try: git pull --rebase origin main
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo.
echo Your PhoneHub has been updated and deployed!
echo.
echo GitHub: https://github.com/jahid124421/phonehub
echo Live Site: https://jahid124421.github.io/phonehub
echo Cloudflare: Will auto-deploy in 1-2 minutes
echo.
echo The site will now auto-update daily at 2 AM UTC.
echo.

:end
pause
