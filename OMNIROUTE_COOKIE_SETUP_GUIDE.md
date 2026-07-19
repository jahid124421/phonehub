# OmniRoute Cookie Setup & Test Results

## 🎯 Executive Summary

**Status:** ✅ Successfully created cookie extraction and testing system for OmniRoute  
**OmniRoute Status:** 🟢 Running (detected at http://localhost:20128)  
**Cookies Extracted:** 7 major AI provider cookies ready for configuration  
**Date:** 2026-07-19

---

## 📊 Test Results Summary

### OmniRoute Connection Status
- **Endpoint:** http://localhost:20128
- **Status:** Running (HTTP 401 - requires authentication)
- **Action Required:** Configure API key or login to dashboard

### Cookie Inventory
The following cookies have been extracted and documented in `COOKIE_KEYS_FOR_OMNIROUTE.md`:

1. ✅ **ChatGPT Web** - `__Secure-next-auth.session-token`
2. ✅ **DeepSeek Web** - `token` 
3. ✅ **Gemini Web** - `__Secure-1PSID`
4. ✅ **Claude Web** - `sessionKey`
5. ✅ **Perplexity Web** - `__Secure-next-auth.session-token`
6. ✅ **Grok Web** - `sso`
7. ✅ **Poe Web** - `p-b`

---

## 🚀 Quick Start Guide

### Step 1: Start OmniRoute Dashboard
```bash
cd OmniRoute
npm run dev
```

The dashboard will open at: **http://localhost:20128**

### Step 2: Login to OmniRoute
1. Open http://localhost:20128 in your browser
2. Login with your credentials
3. If first time, use default password from `.env` file

### Step 3: Add Cookie Providers

For each provider you want to use:

1. **Navigate to Providers**
   - Click "Providers" in the sidebar
   - Click "Add Provider" button

2. **Select Provider Type**
   - Choose "Web Cookie" category
   - Select the provider (e.g., "ChatGPT Web")

3. **Paste Cookie Value**
   - Open `COOKIE_KEYS_FOR_OMNIROUTE.md`
   - Copy the cookie value for that provider
   - Paste it into the "API Key / Cookie" field
   - Click "Save"

4. **Test Connection**
   - Click "Test" button next to the provider
   - If successful, you'll see ✅ green indicator
   - If failed, check cookie expiration and re-extract

### Step 4: Verify Connections
Run the test script:
```bash
node test_omniroute_connections.js
```

Or use the OmniRoute dashboard built-in testing.

---

## 📋 Detailed Provider Configuration

### ChatGPT Web (`chatgpt-web`)
- **Cookie Name:** `__Secure-next-auth.session-token`
- **Source:** chatgpt.com
- **Models Available:** gpt-4o, gpt-4-turbo, gpt-3.5-turbo
- **Setup:**
  1. Login to chatgpt.com
  2. Open DevTools → Application → Cookies
  3. Copy `__Secure-next-auth.session-token` value
  4. Paste in OmniRoute provider settings

### DeepSeek Web (`deepseek-web`)
- **Cookie Name:** `token`
- **Source:** chat.deepseek.com
- **Models Available:** deepseek-chat, deepseek-coder
- **Note:** Requires both token and email

### Gemini Web (`gemini-web`)
- **Cookie Name:** `__Secure-1PSID`
- **Source:** gemini.google.com
- **Models Available:** gemini-pro, gemini-pro-vision
- **Optional:** `__Secure-1PSIDTS` for extended sessions

### Claude Web (`claude-web`)
- **Cookie Name:** `sessionKey`
- **Source:** claude.ai
- **Models Available:** claude-3-opus, claude-3-sonnet, claude-3-haiku

### Perplexity Web (`perplexity-web`)
- **Cookie Name:** `__Secure-next-auth.session-token`
- **Source:** perplexity.ai
- **Models Available:** sonar, sonar-pro

### Grok Web (`grok-web`)
- **Cookie Name:** `sso` (and `sso-rw`)
- **Source:** grok.com
- **Models Available:** grok-2, grok-2-mini
- **Important:** Must include both `sso` and `sso-rw` cookies

### Poe Web (`poe-web`)
- **Cookie Name:** `p-b`
- **Source:** poe.com
- **Models Available:** Multiple (Claude, GPT-4, etc.)

---

## 🔧 Troubleshooting

### Issue: "OmniRoute not running"
**Solution:**
```bash
cd OmniRoute
npm install  # First time only
npm run dev
```

### Issue: "Cookie expired" or 401/403 errors
**Solution:**
1. Re-login to the provider website
2. Extract fresh cookies using the extension
3. Update in OmniRoute dashboard
4. Test connection again

### Issue: "Cannot connect to provider"
**Possible Causes:**
- Cookie expired (most common)
- Provider changed authentication method
- IP restrictions or rate limiting
- Subscription expired

**Solution:**
1. Check provider website directly
2. Verify account status
3. Extract new cookies
4. Consider using OAuth providers instead

### Issue: Test script fails with authentication error
**Solution:**
1. Create an API key in OmniRoute dashboard:
   - Go to Settings → API Keys
   - Create new key
   - Copy the key value
   
2. Set environment variable:
   ```bash
   # Windows CMD
   set OMNIROUTE_API_KEY=your-api-key-here
   node test_omniroute_connections.js
   
   # Windows PowerShell
   $env:OMNIROUTE_API_KEY="your-api-key-here"
   node test_omniroute_connections.js
   
   # Linux/Mac
   export OMNIROUTE_API_KEY=your-api-key-here
   node test_omniroute_connections.js
   ```

---

## 🎯 Expected Results

### Successful Connection Test Output:
```
🚀 OmniRoute Cookie Connection Tester
════════════════════════════════════════════════════════════
✅ OmniRoute is running
════════════════════════════════════════════════════════════

📋 Loading extracted cookies...
Found 7 cookies in COOKIE_KEYS_FOR_OMNIROUTE.md

════════════════════════════════════════════════════════════
🔍 Testing Provider Connections...

Testing ChatGPT Web... ✅ SUCCESS
Testing DeepSeek Web... ✅ SUCCESS
Testing Gemini Web... ✅ SUCCESS
Testing Claude Web... ✅ SUCCESS
Testing Perplexity Web... ✅ SUCCESS
Testing Grok Web... ✅ SUCCESS
Testing Poe Web... ✅ SUCCESS

════════════════════════════════════════════════════════════
📊 TEST SUMMARY

✅ Successful Connections: 7
   • ChatGPT Web (gpt-4o)
   • DeepSeek Web (deepseek-chat)
   • Gemini Web (gemini-pro)
   • Claude Web (claude-3-sonnet)
   • Perplexity Web (sonar)
   • Grok Web (grok-2)
   • Poe Web (claude-3-opus)

❌ Failed Connections: 0

⚠️  Not Configured: 0
```

---

## 📁 Files Created

1. **COOKIE_KEYS_FOR_OMNIROUTE.md** - Cookie reference guide with all extracted values
2. **test_omniroute_connections.js** - Automated connection testing script
3. **OMNIROUTE_COOKIE_SETUP_GUIDE.md** - This comprehensive setup guide
4. **omniroute_test_results.json** - Test results (generated after running tests)

---

## 🔐 Security Notes

### Important Security Practices:

1. **Cookie Expiration:**
   - Most web cookies expire after 30-90 days
   - Re-extract cookies when they expire
   - OmniRoute will show "Session Expired" errors

2. **Cookie Storage:**
   - Cookies are stored in OmniRoute's SQLite database
   - Database is encrypted (if STORAGE_ENCRYPTION_KEY is set)
   - Never commit `.env` or database files to git

3. **Access Control:**
   - Use strong dashboard password
   - Enable API key authentication (REQUIRE_API_KEY=true)
   - Consider IP whitelisting for production

4. **Sharing:**
   - ⚠️ NEVER share cookies publicly
   - Each cookie is tied to your account
   - Sharing cookies = sharing account access

---

## 🎉 Success Criteria

You'll know everything is working when:

- ✅ All 7 providers show green status in dashboard
- ✅ Test script reports 7 successful connections
- ✅ Can make API calls to each provider through OmniRoute
- ✅ No authentication errors in logs

---

## 📞 Support & Resources

### OmniRoute Documentation:
- Main docs: `OmniRoute/README.md`
- Environment config: `OmniRoute/.env.example`
- Provider docs: `OmniRoute/docs/`

### Getting Help:
1. Check OmniRoute GitHub issues
2. Review provider-specific documentation
3. Test cookies directly on provider websites
4. Check OmniRoute logs for detailed errors

### Useful Commands:
```bash
# Start OmniRoute in development mode
cd OmniRoute && npm run dev

# Check OmniRoute logs
cd OmniRoute && npm run dev | grep -i error

# Test specific provider
node test_omniroute_connections.js

# View OmniRoute configuration
cat OmniRoute/.env
```

---

## 🚀 Next Steps

1. **Complete OmniRoute Setup:**
   - Configure remaining providers (OAuth, API keys)
   - Set up combos (multi-provider routing)
   - Enable compression (RTK, Caveman)

2. **Integrate with Your Tools:**
   - Configure Claude Code to use OmniRoute
   - Point Cursor to OmniRoute endpoint
   - Set up Cline, Copilot, etc.

3. **Monitor Usage:**
   - Check provider quotas regularly
   - Monitor cookie expiration dates
   - Track token usage in dashboard

4. **Optimize:**
   - Enable token compression
   - Configure auto-fallback
   - Set up provider priorities

---

## 📈 Connection Success Tracking

| Provider | Status | Last Tested | Models Working | Notes |
|----------|--------|-------------|----------------|-------|
| ChatGPT Web | ⏳ Pending | Not yet tested | - | Cookies ready |
| DeepSeek Web | ⏳ Pending | Not yet tested | - | Cookies ready |
| Gemini Web | ⏳ Pending | Not yet tested | - | Cookies ready |
| Claude Web | ⏳ Pending | Not yet tested | - | Cookies ready |
| Perplexity Web | ⏳ Pending | Not yet tested | - | Cookies ready |
| Grok Web | ⏳ Pending | Not yet tested | - | Cookies ready |
| Poe Web | ⏳ Pending | Not yet tested | - | Cookies ready |

**Update this table after running tests with actual results!**

---

## 🎯 Conclusion

Your OmniRoute cookie extraction and testing system is now complete! All cookies have been documented in `COOKIE_KEYS_FOR_OMNIROUTE.md` and are ready to be added to OmniRoute.

**To proceed:**
1. Start OmniRoute: `cd OmniRoute && npm run dev`
2. Open dashboard: http://localhost:20128
3. Add each provider using the cookies from the reference guide
4. Run tests: `node test_omniroute_connections.js`
5. Update this guide with actual test results

---

*Generated: 2026-07-19*  
*OmniRoute Version: Latest*  
*Node.js Version: 24.18.0*
