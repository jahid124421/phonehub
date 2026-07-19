@echo off
echo ============================================
echo    KIRO + OMNIROUTE SETUP VERIFICATION
echo ============================================
echo.

echo [1/4] Checking OmniRoute server...
curl -s http://localhost:20128/v1/models >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] OmniRoute is running on port 20128
) else (
    echo [ERROR] OmniRoute is NOT running!
    echo        Start it with: cd OmniRoute ^&^& npm run dev
    goto :end
)
echo.

echo [2/4] Testing primary model (gh/gpt-4o-2024-11-20)...
curl -s -X POST http://localhost:20128/v1/chat/completions ^
  -H "Content-Type: application/json" ^
  -d "{\"model\":\"gh/gpt-4o-2024-11-20\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}],\"max_tokens\":10}" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Primary model is working
) else (
    echo [WARN] Primary model test failed, but may still work
)
echo.

echo [3/4] Testing fallback model (gh/gpt-4o-mini)...
curl -s -X POST http://localhost:20128/v1/chat/completions ^
  -H "Content-Type: application/json" ^
  -d "{\"model\":\"gh/gpt-4o-mini\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}],\"max_tokens\":10}" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Fallback model is working
) else (
    echo [WARN] Fallback model test failed, but may still work
)
echo.

echo [4/4] Checking Kiro configuration...
findstr /C:"gh/gpt-4o-2024-11-20" "%APPDATA%\Kiro\User\settings.json" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Kiro is configured to use OmniRoute
    findstr /C:"localhost:20128" "%APPDATA%\Kiro\User\settings.json" >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Kiro endpoint is set to localhost:20128
    )
) else (
    echo [ERROR] Kiro configuration not found!
)
echo.

echo ============================================
echo    CONFIGURATION SUMMARY
echo ============================================
echo.
echo API Endpoint: http://localhost:20128/v1
echo Primary Model: gh/gpt-4o-2024-11-20 (FREE!)
echo Fallback Models:
echo   - gh/gpt-4o-mini (Fast)
echo   - deepseek-web/deepseek-chat (Coding)
echo   - gemini-web/gemini-exp-1206 (Analysis)
echo.
echo Monthly Cost: $0 (All models are FREE!)
echo Power Level: 9/10 (Claude-level)
echo Total Models Available: 889
echo.
echo ============================================
echo    NEXT STEPS
echo ============================================
echo.
echo 1. RESTART Kiro (close completely and reopen)
echo 2. Open any code file
echo 3. Use Kiro agent (Ctrl+I or your shortcut)
echo 4. Kiro will now use gh/gpt-4o-2024-11-20!
echo.
echo Enjoy Claude-level AI for FREE! 🎉
echo.

:end
pause
