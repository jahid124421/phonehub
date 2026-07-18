# 🍪 Cookie Extractor Extension - Installation Guide

A Firefox browser extension that instantly extracts cookies from any website you visit.

## ✨ Features

- **Instant Cookie Extraction** - Click the extension icon on any website to see all cookies
- **Copy Cookie Header** - One-click copy of formatted cookie string (ready to use in API requests)
- **Download Cookies** - Save detailed cookie information to a text file
- **Beautiful Interface** - Modern, easy-to-read popup with cookie statistics
- **Automatic Detection** - Works on ANY website you visit
- **Detailed Information** - See cookie values, domains, expiration, security flags, and more

## 📥 Installation Instructions for Firefox

### Step 1: Open Firefox Add-ons Page
1. Open Firefox browser
2. Type `about:debugging` in the address bar and press Enter
3. Click on "**This Firefox**" in the left sidebar

### Step 2: Load the Extension
1. Click the "**Load Temporary Add-on...**" button
2. Navigate to the `cookie-extractor-extension` folder
3. Select the `manifest.json` file
4. Click "**Open**"

### Step 3: Verify Installation
- You should see "Cookie Extractor" listed in the extensions
- The extension icon (🍪) should appear in your Firefox toolbar

## 🚀 How to Use

### Extract Cookies from Any Website

1. **Visit any website** (e.g., your own websites where you're logged in)
2. **Click the Cookie Extractor icon** (🍪) in your toolbar
3. **View the cookies** instantly in the popup:
   - See cookie count, secure cookies, and HttpOnly cookies
   - Read the formatted cookie header string
   - View detailed information for each cookie

### Copy Cookie Header

1. Open the extension on any website
2. Click the "**📋 Copy Cookie Header**" button
3. The cookie string is copied to your clipboard (ready to paste in API requests, curl commands, etc.)

### Download Cookie Details

1. Open the extension on any website
2. Click the "**💾 Download**" button
3. Save the detailed cookie report as a text file
4. File includes:
   - Website URL
   - Formatted cookie header
   - Detailed information for each cookie (domain, path, expiration, security flags)

## 📊 What You'll See

### Popup Interface Shows:

```
🍪 Cookie Extractor
Current URL

Statistics:
- Total Cookies
- Secure Cookies
- HttpOnly Cookies

Cookie Header (Ready to Use):
session=abc123; token=xyz789; user_id=12345

Detailed Cookie List:
- Cookie name with security badges
- Cookie value
- Domain, path, and expiration info
```

## 🔐 Security & Privacy

- ✅ **Local Only** - All cookie extraction happens locally in your browser
- ✅ **No Data Transmission** - No cookies are sent to any server
- ✅ **Your Websites Only** - Use this for websites you own or have permission to access
- ⚠️ **Keep Output Secure** - Cookie files contain authentication credentials

## 💡 Use Cases

Perfect for:
- **Managing multiple websites** - Quickly extract cookies from your 50+ sites
- **API Testing** - Get cookie headers for API requests
- **Development** - Debug cookie issues
- **Authentication** - Copy session tokens for testing
- **Documentation** - Export cookie information for reference

## 🛠️ Troubleshooting

### Extension Not Showing Up
- Make sure you selected the correct `manifest.json` file
- Reload the extension in `about:debugging`

### No Cookies Found
- Make sure you're logged into the website
- Some sites use localStorage instead of cookies
- Try refreshing the page and opening the extension again

### Copy Button Not Working
- Modern Firefox versions support clipboard API
- If it fails, try manually selecting and copying the cookie header text

## 📝 Output Format Examples

### Cookie Header (One-Line Format):
```
session_id=abc123xyz; auth_token=def456uvw; user_pref=theme_dark
```

### Downloaded File Format:
```
Cookie Extraction Report
Generated: 2026-07-19T01:45:00.000Z
============================================================

URL: https://example.com
Domain: example.com
Cookie Count: 3

============================================================
COOKIE HEADER (Ready to Use)
============================================================
session_id=abc123xyz; auth_token=def456uvw; user_pref=theme_dark

============================================================
DETAILED COOKIE INFORMATION
============================================================

[1] session_id
    Value: abc123xyz
    Domain: .example.com
    Path: /
    Secure: true
    HttpOnly: true
    SameSite: lax
    Expires: 2026-08-19T01:45:00.000Z

[2] auth_token
    Value: def456uvw
    Domain: .example.com
    Path: /
    Secure: true
    HttpOnly: false
    SameSite: strict
    Expires: Session
```

## 🔄 Updating the Extension

If you make changes to the extension files:
1. Go to `about:debugging`
2. Click "**Reload**" next to the Cookie Extractor extension
3. Changes will take effect immediately

## ⚠️ Important Notes

- **Temporary Installation**: In Firefox, temporary extensions are removed when you close the browser. You'll need to reload it each time you start Firefox.
- **Permanent Installation**: To make it permanent, you'd need to sign it through Mozilla's add-on store (or use Firefox Developer Edition with `xpinstall.signatures.required` set to false in `about:config`).
- **Chrome/Edge**: This extension uses Firefox's `browser` API. For Chrome/Edge, you'd need to modify it to use `chrome` API instead.

## 📂 Extension Files

- `manifest.json` - Extension configuration
- `popup.html` - User interface
- `popup.js` - Cookie extraction logic
- `icon.png` - Extension icon

## 🎯 Quick Start Summary

1. Open Firefox → `about:debugging` → "This Firefox"
2. Click "Load Temporary Add-on"
3. Select `manifest.json` from the extension folder
4. Visit any website and click the 🍪 icon
5. Copy or download cookies!

---

**Enjoy easy cookie extraction across all your websites!** 🍪✨
