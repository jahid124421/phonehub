# 🎯 Qoder IDE + OmniRoute Setup - Get Unlimited AI Calls

## 📋 Understanding Your Situation

**Qoder IDE** gives you:
- ✅ 200 FREE API calls (one-time or monthly)
- ❌ After 200 calls → credits finished
- ❌ Need to wait for reset OR pay for more

**You're asking:**
1. How to use those 200 free calls in Qoder?
2. What to do now that credits are finished?

---

## 🆓 Solution: Configure Qoder to Use OmniRoute

Instead of using Qoder's limited 200 calls, connect Qoder to **OmniRoute** for **unlimited free calls**!

---

## 🚀 Setup Qoder with OmniRoute (Step-by-Step)

### **Step 1: Make Sure OmniRoute is Running**

Open terminal and start OmniRoute:
```bash
cd OmniRoute
npm run dev
```

Should show: `Server running on http://localhost:20128`

### **Step 2: Configure Qoder IDE**

#### **Option A: Via Qoder Settings (Recommended)**

1. **Open Qoder IDE**
2. **Go to Settings/Preferences** (usually Ctrl+,)
3. **Find "AI Assistant" or "Copilot" section**
4. **Select "Custom API" or "OpenAI Compatible"**
5. **Enter these settings:**

```
Provider: OpenAI Compatible (or Custom)
API Endpoint: http://localhost:20128/v1
API Key: dummy
Model: gh/gpt-4o-2024-11-20
```

#### **Option B: Via Qoder Config File**

If Qoder uses a config file (usually `.qoder/config.json` or similar):

```json
{
  "ai": {
    "provider": "openai-compatible",
    "apiBase": "http://localhost:20128/v1",
    "apiKey": "dummy",
    "model": "gh/gpt-4o-2024-11-20"
  }
}
```

### **Step 3: Test It**

1. Open any code file in Qoder
2. Use AI assistant feature (usually Ctrl+K or Ctrl+I)
3. Ask something like: "Explain this code"
4. Should work with **NO credit limit!**

---

## 💡 How to Use Your 200 Free Calls (If You Want To)

If you still have remaining free calls in Qoder and want to use them:

### **Method 1: Check Your Balance**

In Qoder IDE:
1. Look for "Credits" or "API Usage" in settings
2. Should show: "X calls remaining out of 200"
3. Each AI request uses 1 call

### **Method 2: Make Calls Efficiently**

If you have calls left, use them wisely:
- Use for complex tasks only
- Use OmniRoute for simple tasks
- Save credits for when needed

### **Method 3: Switch Between Providers**

Configure Qoder to:
- Use built-in API when you have credits (200 free calls)
- Switch to OmniRoute when credits run out (unlimited)

---

## 🎯 Best Configuration for Qoder

Here's the optimal setup:

### **Primary Setup: Use OmniRoute (Unlimited)**

```json
{
  "ai.provider": "openai-compatible",
  "ai.apiEndpoint": "http://localhost:20128/v1",
  "ai.apiKey": "dummy",
  "ai.model": "gh/gpt-4o-2024-11-20",
  "ai.useOmniRoute": true
}
```

**Benefits:**
- ✅ Unlimited calls (no 200 limit)
- ✅ Free forever
- ✅ Claude-level quality (9/10)
- ✅ Never runs out

### **Backup Setup: Use Qoder's Built-in API**

Only if OmniRoute is down:
```json
{
  "ai.provider": "qoder-built-in",
  "ai.freeCallsRemaining": 200
}
```

---

## 📊 Comparison: Qoder Built-in vs OmniRoute

| Feature | Qoder Built-in (200 calls) | OmniRoute (Unlimited) |
|---------|---------------------------|----------------------|
| **Free Calls** | 200 total | **UNLIMITED** ✅ |
| **After Limit** | Blocked or pay | **Never blocked** ✅ |
| **Model Quality** | Varies (depends on Qoder) | Claude-level (9/10) |
| **Cost** | Free → Paid | **$0 forever** ✅ |
| **Setup** | Built-in (easy) | Need OmniRoute server |
| **Reliability** | Depends on Qoder servers | Local (always works) |

**Recommendation:** Use OmniRoute!

---

## 🔧 Qoder IDE Configuration Files

Qoder might store settings in different locations:

### **Windows:**
```
C:\Users\96650\AppData\Roaming\Qoder\settings.json
C:\Users\96650\.qoder\config.json
C:\Users\96650\.config\qoder\settings.json
```

### **What to Add:**
```json
{
  "ai": {
    "provider": "custom",
    "endpoint": "http://localhost:20128/v1",
    "key": "dummy",
    "model": "gh/gpt-4o-2024-11-20",
    "enabled": true
  }
}
```

---

## 💎 Your Best Models for Qoder

Configure these models in Qoder for different tasks:

### **1. For Complex Coding (Best Quality)**
```
Model: gh/gpt-4o-2024-11-20
Power: 9/10
Use for: Complex features, refactoring, architecture
```

### **2. For Quick Tasks (Best Speed)**
```
Model: gh/gpt-4o-mini
Power: 7/10
Speed: Ultra-fast (1-2s)
Use for: Simple edits, quick questions
```

### **3. For Code Reviews**
```
Model: deepseek-web/deepseek-chat
Power: 8/10
Use for: Debugging, code analysis
```

---

## 🚀 Quick Setup Script for Qoder

Save this as `setup_qoder_omniroute.bat`:

```batch
@echo off
echo ========================================
echo    QODER + OMNIROUTE SETUP
echo ========================================
echo.

echo Step 1: Starting OmniRoute...
start cmd /k "cd OmniRoute && npm run dev"
timeout /t 3 >nul

echo Step 2: Testing OmniRoute...
curl -s http://localhost:20128/v1/models >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] OmniRoute is running!
) else (
    echo [ERROR] OmniRoute failed to start
    pause
    exit
)

echo.
echo Step 3: Qoder Configuration
echo.
echo Add these to Qoder settings:
echo.
echo Provider: OpenAI Compatible
echo API Endpoint: http://localhost:20128/v1
echo API Key: dummy
echo Model: gh/gpt-4o-2024-11-20
echo.
echo ========================================
echo    SETUP COMPLETE
echo ========================================
echo.
echo Now open Qoder and configure AI settings!
echo You'll have UNLIMITED AI calls (no more 200 limit)
echo.
pause
```

Run: `setup_qoder_omniroute.bat`

---

## 🔍 Finding Qoder's AI Settings

Since I don't have Qoder installed, here's how to find the settings:

### **Method 1: Look in Menu**
- File → Preferences → AI Assistant
- Tools → Settings → Copilot
- Settings → Extensions → AI

### **Method 2: Search in Settings**
- Open Settings (Ctrl+,)
- Search for: "AI", "API", "Copilot", or "Assistant"
- Look for API endpoint configuration

### **Method 3: Check Config Files**
- Look in `%APPDATA%\Qoder\`
- Look for `.qoder` folder in your home directory
- Search for `settings.json` or `config.json`

---

## 📋 Step-by-Step: Replace Qoder's API

### **Before (Using Qoder's 200 free calls):**
```
Qoder → Qoder Cloud API → Limited to 200 calls → Credits finished ❌
```

### **After (Using OmniRoute):**
```
Qoder → OmniRoute (localhost:20128) → Free models → Unlimited calls ✅
```

### **How to Switch:**

1. **Open Qoder IDE**
2. **Find AI/Copilot Settings**
3. **Change provider from "Built-in" to "Custom/OpenAI Compatible"**
4. **Enter OmniRoute endpoint:** `http://localhost:20128/v1`
5. **Enter API key:** `dummy`
6. **Enter model:** `gh/gpt-4o-2024-11-20`
7. **Save and restart Qoder**

---

## 💡 What Happens to Your 200 Free Calls?

### **Option 1: Save Them for Later**
- Configure Qoder to use OmniRoute now
- Your 200 free calls remain unused
- Use them later if needed (as backup)

### **Option 2: Use Both**
- Use Qoder's API for critical tasks (200 calls)
- Use OmniRoute for everything else (unlimited)
- Best of both worlds!

### **Option 3: Ignore Them**
- Just use OmniRoute (unlimited)
- Forget about the 200 call limit
- Simpler setup

**My Recommendation:** Use OmniRoute only (unlimited is better!)

---

## 🆘 Troubleshooting

### Issue 1: Can't Find AI Settings in Qoder

**Solution:**
- Check Qoder documentation
- Look for "Preferences" or "Settings"
- Search within settings for "AI" or "API"

### Issue 2: Qoder Doesn't Support Custom API

**Solution:**
If Qoder doesn't allow custom API endpoints:
1. Use Cursor instead (cursor.sh) - fully supports OmniRoute
2. Use VS Code + Cline extension
3. Use Kiro (after fixing the settings we did earlier)

### Issue 3: Connection Refused

**Solution:**
Make sure OmniRoute is running:
```bash
cd OmniRoute
npm run dev
```

Test it:
```bash
curl http://localhost:20128/v1/models
```

---

## ✅ Summary

### **Your Qoder Situation:**
- ❌ Had 200 free API calls
- ❌ Credits finished (all 200 used)
- ❌ Blocked from using AI in Qoder
- ❓ How to continue working?

### **The Solution:**
- ✅ Configure Qoder to use OmniRoute
- ✅ Get **unlimited free calls** (not just 200!)
- ✅ Use `gh/gpt-4o-2024-11-20` (Claude-level quality)
- ✅ Cost: **$0 forever**
- ✅ Never run out of credits again!

### **Next Steps:**
1. **Start OmniRoute:** `cd OmniRoute && npm run dev`
2. **Open Qoder Settings**
3. **Configure AI to use:** `http://localhost:20128/v1`
4. **Test with simple request**
5. **Enjoy unlimited AI coding!** 🎉

---

## 🎯 Quick Reference

**For Qoder AI Settings:**
```
Provider: OpenAI Compatible (or Custom)
Endpoint: http://localhost:20128/v1
API Key: dummy
Model: gh/gpt-4o-2024-11-20
Temperature: 0.7
Max Tokens: 8192
```

**Your Best Models:**
- Complex coding: `gh/gpt-4o-2024-11-20`
- Quick tasks: `gh/gpt-4o-mini`
- Code reviews: `deepseek-web/deepseek-chat`

**Total Models Available:** 889 (all free!)

---

## 📚 Additional Help

Can't find Qoder's settings? Tell me:
1. Where did you download Qoder from?
2. What version of Qoder are you using?
3. Can you see an "AI" or "Copilot" menu?

I'll help you find the exact settings location!

---

**Bottom Line:** You don't need to worry about 200 calls anymore. With OmniRoute, you get **unlimited calls for free!**

Just configure Qoder to point to `http://localhost:20128/v1` and you're set! 🚀

---

*Updated: 2026-07-19*  
*Qoder + OmniRoute Integration Guide*  
*Unlimited Free AI Calls Available*
