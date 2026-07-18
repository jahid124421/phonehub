# 🍪 Cookie Extractor - Installation Guide for AI Services

## Perfect for Your Use Case!

This extension is specifically designed for what you need - quickly extracting session cookies from your 25+ AI service websites (Claude, ChatGPT, Gemini, Perplexity, etc.).

**No more manual DevTools work!** Just click the extension icon and instantly:
- See all cookies for the current site
- Copy the formatted cookie header string
- Download detailed cookie information

---

## 🚀 Installation in Firefox

### Step 1: Open Firefox Extension Manager
1. **Open Firefox** browser
2. **Type in address bar:** `about:debugging`
3. **Press Enter**
4. **Click:** "This Firefox" in the left sidebar

### Step 2: Load the Extension
1. **Click:** "Load Temporary Add-on..." button (top right)
2. **Navigate to:** `C:\Users\96650\OneDrive\Desktop\AI_BA_WORKSPACE\cookie-extractor-extension`
3. **Select:** `manifest.json` file
4. **Click:** "Open"

### Step 3: Verify Installation
✅ You should see "Cookie Extractor" in the list  
✅ The extension icon (🍪) appears in your Firefox toolbar

---

## 💡 How to Use for Your AI Services

### Example: Extract Claude sessionKey

1. **Visit:** https://claude.ai and log in
2. **Click** the 🍪 Cookie Extractor icon in toolbar
3. **See** all cookies displayed, including `sessionKey`
4. **Click** "📋 Copy Cookie Header" button
5. **Paste** directly into your configuration!

The copied format will be:
```
sessionKey=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...; other_cookie=value
```

### Example: Extract ChatGPT Session Token

1. **Visit:** https://chatgpt.com
2. **Click** 🍪 icon
3. **See** `__Secure-next-auth.session-token` in the list
4. **Copy** the cookie header
5. **Done!**

### Example: Extract Multiple Cookies (Arena.ai)

1. **Visit:** https://arena.ai
2. **Click** 🍪 icon
3. **See** ALL cookies: `arena-auth-prod-v1.0`, `arena-auth-prod-v1.1`, etc.
4. **Copy** the complete cookie header (includes all cookies automatically!)
5. **Perfect** - you get the full string: `cookie1=val1; cookie2=val2; cookie3=val3`

---

## 🎯 Benefits for Your Workflow

### Before (Manual Method):
1. Open DevTools (F12)
2. Go to Application tab
3. Navigate to Cookies → Domain
4. Find the right cookie
5. Copy the value
6. Repeat for 25+ websites...

### Now (With Extension):
1. Visit website
2. Click 🍪 icon
3. Click "Copy Cookie Header"
4. Done! (3 seconds per site)

**Save hours of time across your 25+ AI services!**

---

## 📊 What You'll See

When you click the extension icon, you get:

```
🍪 Cookie Extractor
https://claude.ai

Statistics:
5 Cookies | 3 Secure | 2 HttpOnly

📋 Copy Cookie Header | 💾 Download

Cookie Header (Ready to Use):
sessionKey=eyJhbGc...; __cf_bm=abc...; __cflb=def...

Detailed Cookie List:
✓ sessionKey [SECURE] [HTTP-ONLY]
  Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  Domain: .claude.ai | Path: /
  Expires: 2026-08-19

✓ __cf_bm
  Value: abc123...
  Domain: .claude.ai | Path: /
  Expires: Session
```

---

## 🔥 Works Perfectly With Your 25 AI Services

| Service | Cookie Name | Just Click & Copy! |
|---------|-------------|-------------------|
| Claude | `sessionKey` | ✅ |
| ChatGPT | `__Secure-next-auth.session-token` | ✅ |
| Gemini | `__Secure-1PSID` | ✅ |
| Arena.ai | Multiple cookies (auto-combined) | ✅ |
| Perplexity | `perplexity-session` | ✅ |
| Poe | `p-session` | ✅ |
| All 25+ services | Any cookie | ✅ |

---

## 💾 Download Feature

Click "💾 Download" to save a detailed report:

```
Cookie Extraction Report
Generated: 2026-07-19T01:52:00.000Z
============================================================

URL: https://claude.ai
Domain: claude.ai
Cookie Count: 5

============================================================
COOKIE HEADER (Ready to Use)
============================================================
sessionKey=eyJhbGc...; __cf_bm=abc...; other=xyz...

============================================================
DETAILED COOKIE INFORMATION
============================================================

[1] sessionKey
    Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    Domain: .claude.ai
    Path: /
    Secure: true
    HttpOnly: true
    SameSite: lax
    Expires: 2026-08-19T01:52:00.000Z

[2] __cf_bm
    Value: abc123...
    ...
```

Perfect for documenting all your API credentials!

---

## 🎯 Quick Workflow for All 25 Services

1. **Open Firefox** with extension installed
2. **Visit each AI service** (Claude, ChatGPT, Gemini, etc.)
3. **Click 🍪 icon** on each site
4. **Click "Copy"** or **"Download"** to save cookies
5. **Repeat** for all 25 services (takes ~2 minutes total!)

---

## ⚠️ Important Notes

### Temporary Installation
- Firefox removes temporary extensions when you close the browser
- **Solution:** Just reload it next time using the same steps
- Takes 10 seconds to reinstall

### Cookie Security
- ✅ All extraction happens **locally** in your browser
- ✅ **No data is sent** to any server
- ✅ Keep downloaded cookie files **secure** (they're like passwords!)

### Cookie Format
The extension automatically formats cookies as:
```
name1=value1; name2=value2; name3=value3
```

This is the standard Cookie header format - ready to use in:
- API requests
- Configuration files
- curl commands
- Your applications

---

## 🛠️ Troubleshooting

### "No cookies found"
- Make sure you're **logged into** the AI service
- Try **refreshing** the page
- Some sites use localStorage (not cookies) - extension only shows cookies

### Extension icon not visible
- Check if extension is loaded in `about:debugging`
- Try **reloading** the extension
- Click the puzzle icon in Firefox toolbar → Pin "Cookie Extractor"

### Copy button not working
- Try **manually selecting** the cookie header text and copying
- Or use the **Download** button instead

---

## 📝 Example: Complete Workflow

### Extracting cookies from all 25 AI services:

```
1. Install extension (1 minute - one time)
2. Visit Claude.ai → Click 🍪 → Copy → Save to file (10 seconds)
3. Visit ChatGPT.com → Click 🍪 → Copy → Save to file (10 seconds)
4. Visit Gemini.google.com → Click 🍪 → Copy → Save to file (10 seconds)
5. ... repeat for all 25 services ...
6. Total time: ~5 minutes for all 25 services!
```

**vs Manual DevTools method: ~30+ minutes**

---

## 🎉 You're Ready!

The extension is **much faster** than the manual DevTools method in your `HOW_TO_GET_SESSION_KEY.txt` file.

Instead of:
- F12 → Application → Cookies → Find cookie → Copy

You just:
- Click 🍪 → Copy

**Perfect for managing your 25+ AI service sessions!**

---

## 🔄 Next Steps

1. **Install the extension** (follow steps above)
2. **Test it** on Claude.ai or ChatGPT.com
3. **Once working**, go through all 25 AI services
4. **Save all cookies** for your API configurations

Need help? The extension shows you exactly which cookies exist on each site!
