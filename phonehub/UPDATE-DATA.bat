@echo off
REM ===== PhoneHub — refresh all data (specs + AI reviews + prices) =====
cd /d "%~dp0tools"
python run_all.py %*
echo.
pause
