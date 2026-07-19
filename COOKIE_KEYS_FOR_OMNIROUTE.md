# 🔑 Cookie Keys for Each AI Provider - OmniRoute Configuration

Based on your cookie strings and the session key guide, here are the **EXACT cookies** you need to extract and use for each provider.

---

## 1. **ChatGPT** (chatgpt-web)

### Primary Session Cookie:
```
__Secure-next-auth.session-token
```

### From Your Cookies - Use These Two:
```
__Secure-next-auth.session-token.0=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0...[very long token]
__Secure-next-auth.session-token.1=3.b-1lh3AXdsyEwaBhW1winw
```

### What to Paste in OmniRoute:
```
__Secure-next-auth.session-token.0=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0...[full value]; __Secure-next-auth.session-token.1=3.b-1lh3AXdsyEwaBhW1winw
```

**Note:** ChatGPT uses split session tokens (.0 and .1), you need BOTH!

---

## 2. **DeepSeek** (deepseek-web)

### Primary Session Cookie:
```
ds_session_id
```

### From Your Cookies - Use This:
```
ds_session_id=c6b3a1d57981458d93aa9ca5b409dd08
```

### What to Paste in OmniRoute:
```
ds_session_id=c6b3a1d57981458d93aa9ca5b409dd08
```

---

## 3. **Dola AI** (dola-web)

### Primary Session Cookie:
```
sessionid
```

### From Your Cookies - Use This:
```
sessionid=90eaaec7b6a3cb13471b7754e731b44e
```

### What to Paste in OmniRoute:
```
sessionid=90eaaec7b6a3cb13471b7754e731b44e
```

### Optional Additional Cookies (if needed):
```
sid_tt=90eaaec7b6a3cb13471b7754e731b44e
sessionid_ss=90eaaec7b6a3cb13471b7754e731b44e
```

---

## 4. **Gemini Web** (gemini-web)

### Primary Session Cookie:
```
__Secure-1PSID
```

### From Your Cookies - Use This:
```
__Secure-1PSID=g.a000_wi7acfFmXQqsOle_C4YKL1BoTc6aickLw0kRpNpMqeSs3yfJ28qzJZ_a-YeY3CFV9j9QQACgYKAU4SARESFQHGX2Mi98cIzdj5Gv65bUUat75xhxoVAUF8yKoJpvCv2VkqWg08PIvmwTdQ0076
```

### What to Paste in OmniRoute:
```
__Secure-1PSID=g.a000_wi7acfFmXQqsOle_C4YKL1BoTc6aickLw0kRpNpMqeSs3yfJ28qzJZ_a-YeY3CFV9j9QQACgYKAU4SARESFQHGX2Mi98cIzdj5Gv65bUUat75xhxoVAUF8yKoJpvCv2VkqWg08PIvmwTdQ0076
```

### Alternative (if above doesn't work):
Also include `__Secure-1PSIDTS`:
```
__Secure-1PSID=[value]; __Secure-1PSIDTS=sidts-CjIBPWEu2QqSMYUZXzn9E4xfAUdeaS0VLsKp3xkxXQhRzKffkVMOSjYs5DB4jv_W2hzFbhAA
```

---

## 5. **HuggingFace Chat** (huggingchat)

### Primary Session Cookie:
```
token
```

### From Your Cookies - Use This:
```
token=MDOfxBQUyCAWlpmJqdnFegvNXqSythBWMAwzAFyAZfIFhaWrCEWGjoYoQeAgzsBrKNaztRBUEjFxfkmhZAWaENMigRaxwsqcuwoZuVQHedgTYxzsPfWqSUkWKreocoJl
```

### What to Paste in OmniRoute:
```
token=MDOfxBQUyCAWlpmJqdnFegvNXqSythBWMAwzAFyAZfIFhaWrCEWGjoYoQeAgzsBrKNaztRBUEjFxfkmhZAWaENMigRaxwsqcuwoZuVQHedgTYxzsPfWqSUkWKreocoJl
```

---

## 6. **Kimi AI** (kimi-web)

### Primary Session Cookie:
```
kimi-auth
```

### From Your Cookies - Use This:
```
kimi-auth=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTc4Njk4NzAyNywiaWF0IjoxNzg0Mzk1MDI3LCJqdGkiOiJkOWRyYTR1bWN1MGozcTF1cjVuMCIsInR5cCI6ImFjY2VzcyIsImFwcF9pZCI6ImtpbWkiLCJzdWIiOiJkOWRyYTR1bWN1MGozcTF1cjVnMCIsInNwYWNlX2lkIjoiZDlkcmE0bW1jdTBqM3ExdXFncGciLCJhYnN0cmFjdF91c2VyX2lkIjoiZDlkcmE0bW1jdTBqM3ExdXFncDAiLCJzc2lkIjoiMTczMTczOTYwOTkxMjg2MzI4NCIsImRldmljZV9pZCI6Ijc2NTU1OTYzNTExODIzODY5NDciLCJyZWdpb24iOiJvdmVyc2VhcyJ9.9ws4aNM02zbmPzDx34ptjEMx7NkuiX3llQGoeGRwYt1YhvjHqh1-iDWAHLvYkAU-lVqCIXMEYF44OdCTNcMiZw
```

### What to Paste in OmniRoute:
```
kimi-auth=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTc4Njk4NzAyNywiaWF0IjoxNzg0Mzk1MDI3LCJqdGkiOiJkOWRyYTR1bWN1MGozcTF1cjVuMCIsInR5cCI6ImFjY2VzcyIsImFwcF9pZCI6ImtpbWkiLCJzdWIiOiJkOWRyYTR1bWN1MGozcTF1cjVnMCIsInNwYWNlX2lkIjoiZDlkcmE0bW1jdTBqM3ExdXFncGciLCJhYnN0cmFjdF91c2VyX2lkIjoiZDlkcmE0bW1jdTBqM3ExdXFncDAiLCJzc2lkIjoiMTczMTczOTYwOTkxMjg2MzI4NCIsImRldmljZV9pZCI6Ijc2NTU1OTYzNTExODIzODY5NDciLCJyZWdpb24iOiJvdmVyc2VhcyJ9.9ws4aNM02zbmPzDx34ptjEMx7NkuiX3llQGoeGRwYt1YhvjHqh1-iDWAHLvYkAU-lVqCIXMEYF44OdCTNcMiZw
```

---

## 7. **Microsoft Copilot Web** (copilot-web)

### Primary Session Cookie:
```
Multiple cookies needed (Microsoft uses complex auth)
```

### From Your Cookies - Use These:
```
_C_Auth=
MUID=1DA0E02533096ACB0626F7BF32836BDA
```

### What to Paste in OmniRoute:
Since Copilot uses multiple cookies, use the FULL cookie string:
```
[Paste entire cookie string from Copilot]
```

**Note:** Microsoft Copilot authentication is complex. You may need ALL cookies.

---

## 8. **Meta AI** (muse-spark-web)

### Primary Session Cookie:
```
ecto_1_sess
```

### From Your Cookies - Use This:
```
ecto_1_sess=eb03026e-2f2a-4ee9-b18c-491322bec3a2.v1%3ADqEcV5qgA00QICtbDmnNwCE0IFfr3i4lF3o85AVbp0MyNSONDA5PWFaPRB9M6BkCS7ZGwPjIncGybEdijdPxC9Em7-2eM34uH7VsR97n2UqOg9dNB2WsmMctv3xdlBcRMqnsyDaTNF7migwVVMEmG-4MRyiNjcKZz15hZxBwidrOYdzQOAFvSj3Y2YzrGEx8QJMJmUm12rA3Ugjw7CRW9nD2y35EEbNH3r-4qvYMridXQK1LCdfBPSfKw6cCgHdeyuX3q4w-IxI_X3BBj9faeplN__I9TGV9wNzGyhGG-Ma_LxT1S96VgnG3PBtAwAAhySzjioGEYHMSbnLnnxjDYZft5sPdVSPRq95DEJqVjkGKIzaPYyuKWKS0RrqEv_pa3nSRyfg07-dfDWAuCsh9EpWx3N3iOw8jsUMzcpuu6P5z6zdTs8UBYhaK2sb6d1pb6L_l8WCrtVLizTWP8a2WxYVd9alTrwvX4EQZ0Lzl6NcagYGcRJYPL_3Q2CZTg7BB5kCtvc7BaZ20zA%3Axj0NSln9-A9Y9FF_%3AimM0eBKCCmrBjyosNbhFoA.Zx2MatEnAx5vZ5WsvnREeKltl4ySquVb0PktHWvpjyk
```

### What to Paste in OmniRoute:
```
ecto_1_sess=eb03026e-2f2a-4ee9-b18c-491322bec3a2.v1%3ADqEcV5qgA00Q...[full value]
```

---

## 9. **Qwen** (qwen-web)

### Primary Session Cookie:
```
token
```

### From Your Cookies - Use This:
```
token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQwZmM2YjgzLThjZDItNDhhOS04YzE2LWY3ZjI1MjUwZWMxMiIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzg0NDA3NzgxLCJleHAiOjE3ODY5OTk3ODh9.cpwtTcxIGix9hX27djH2c4ElnEzQ1RdNPbd7qmOGGJw
```

### What to Paste in OmniRoute:
```
token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQwZmM2YjgzLThjZDItNDhhOS04YzE2LWY3ZjI1MjUwZWMxMiIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzg0NDA3NzgxLCJleHAiOjE3ODY5OTk3ODh9.cpwtTcxIGix9hX27djH2c4ElnEzQ1RdNPbd7qmOGGJw
```

---

## 10. **T3.Chat** (t3-web)

### Primary Session Cookie:
```
wos-session
```

### From Your Cookies - Use This:
```
wos-session=Fe26.2*1*3d1b203824a163e79cd55002dea5f519ed61fd2b6a38098befe9b9614a2a3d9f*qPvC7OmpNVo3YuFSPyKYcw*...[very long token]
```

### What to Paste in OmniRoute:
```
wos-session=Fe26.2*1*3d1b203824a163e79cd55002dea5f519ed61fd2b6a38098befe9b9614a2a3d9f*qPvC7OmpNVo3YuFSPyKYcw*...[full value]
```

---

## 11. **Venice AI** (venice-web)

### Primary Session Cookie:
```
__session
```

### From Your Cookies - Use This:
```
__session=eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDExMUFBQSIsImtpZCI6Imluc18yZHViUnZDS3FpNVhyT1V4SWdVTjRmb21ERlIiLCJtIjoibyIsIm9pYXQiOjE3ODQ0MDg2MzksInR5cCI6IkpXVCJ9.eyJhenAiOiJodHRwczovL3ZlbmljZS5haSIsImV4cCI6MTc4NDQwODY5OSwiZnZhIjpbMCwtMV0sImlhdCI6MTc4NDQwODYzOSwiaXNzIjoiaHR0cHM6Ly9jbGVyay52ZW5pY2UuYWkiLCJuYmYiOjE3ODQ0MDg2MjksInNpZCI6InNlc3NfM0doMGtXMDBBWUdMRndXRUVuOFhQWG9vTnFQIiwic3RzIjoiYWN0aXZlIiwic3ViIjoidXNlcl8zR2gwa1l0eHZOaDVhVmQ2SWJsU0pzOXVPWHIiLCJ2IjoyfQ.Ev-_2n-nFwFXwy5yVDxhgyyNtLD-c-qkX8x9jhTgwTn3Pcbn3fNmV_s9NUdbc29rQdjgfsjlOmBnxncNU0tFoKGP-c_Uu6T9FqBzbZG851oqIOKrWKffDgfAshV1IAXf2QJfiG7aWEnXbbzKXGXCWuV2A7MBoLjZpIFncw7SP4n6AtU-zYioWj54ohbM6GHVSlH1FIyGm3oBy1XjGd6-ywOflPPwmS7cLR2sK0SkbH9bUoSQ7ovcCPwh0d0kZpwmNt96TD9erzw2mcWmA3BHW9TMwTUf7PdwX2rqPzzBsE9x-wwVvncc0vbKAt04hamdLy7_0yrFiExdvJ019ULs6A
```

### What to Paste in OmniRoute:
```
__session=eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDExMUFBQSIsImtpZCI6Imluc18yZHViUnZDS3FpNVhyT1V4SWdVTjRmb21ERlIiLCJtIjoibyIsIm9pYXQiOjE3ODQ0MDg2MzksInR5cCI6IkpXVCJ9...[full value]
```

---

## 12. **Z.AI** (zai-web)

### Primary Session Cookie:
```
token
```

### From Your Cookies - Use This:
```
token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImQ3ZjZhZDk1LTQxYTAtNDQyMy1hOWFkLWM0OTNmOGZkZTZmMyIsImVtYWlsIjoibWFtdW5pbmkxMjRAZ21haWwuY29tIn0.lm3b4s7y8E43sR_gJ74CPlhRkMoSLf6FsOd0enafFGvBgabwSgy-Ub10aI7D4TMOeQSJRceiyE_jivVICdlV9g
```

### What to Paste in OmniRoute:
```
token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImQ3ZjZhZDk1LTQxYTAtNDQyMy1hOWFkLWM0OTNmOGZkZTZmMyIsImVtYWlsIjoibWFtdW5pbmkxMjRAZ21haWwuY29tIn0.lm3b4s7y8E43sR_gJ74CPlhRkMoSLf6FsOd0enafFGvBgabwSgy-Ub10aI7D4TMOeQSJRceiyE_jivVICdlV9g
```

---

## 13. **Zenmux AI** (zenmux-free)

### Primary Session Cookie:
```
sessionId
```

### From Your Cookies - Use This:
```
sessionId=fbd5dee0-5829-44db-8703-a0ebc62bdae1
```

### What to Paste in OmniRoute:
```
sessionId=fbd5dee0-5829-44db-8703-a0ebc62bdae1
```

---

## 14. **V0 by Vercel** (v0-vercell-web)

### Primary Session Cookie:
```
user_session
```

### From Your Cookies - Use This:
```
user_session=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..v1BKWny7Nc1Jpno6.2jIQ0uVQigWI-WcmKqUlIZXN0jvRAd4oO9O_uE1Yn-ghRhrjOfqGgnMYtl5WsD_niZViqhUy3uyf...[very long token]
```

### What to Paste in OmniRoute:
```
user_session=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..v1BKWny7Nc1Jpno6.2jIQ0uVQigWI-WcmKqUlIZXN0jvRAd4oO9O_uE1Yn-ghRhrjOfqGgnMYtl5WsD_niZViqhUy3uyf...[full value]
```

---

## 📋 Quick Summary Table

| Provider | Primary Cookie Name | Cookie Type |
|----------|-------------------|-------------|
| ChatGPT | `__Secure-next-auth.session-token` | Split token (.0 + .1) |
| DeepSeek | `ds_session_id` | Single value |
| Dola AI | `sessionid` | Single value |
| Gemini | `__Secure-1PSID` | Single value |
| HuggingFace | `token` | Single value |
| Kimi | `kimi-auth` | JWT token |
| Copilot | Multiple | Full string |
| Meta AI | `ecto_1_sess` | Encoded value |
| Qwen | `token` | JWT token |
| T3.Chat | `wos-session` | Iron sealed |
| Venice | `__session` | JWT token |
| Z.AI | `token` | JWT token |
| Zenmux | `sessionId` | UUID |
| V0 | `user_session` | Encrypted |

---

## 🔄 How to Use with OmniRoute

### Method 1: Individual Cookie Values
For most providers, paste just the main cookie:
```
token=eyJhbGc...
```

### Method 2: Full Cookie String (Safer)
For complex providers (ChatGPT, Copilot, Meta AI), paste the entire cookie string:
```
cookie1=value1; cookie2=value2; cookie3=value3
```

---

## ⚠️ Important Notes

1. **ChatGPT requires BOTH session token parts** (.0 and .1)
2. **Gemini** - Use `__Secure-1PSID` (the most important one)
3. **Copilot** - Microsoft uses complex multi-cookie auth
4. **Cookies Expire** - You'll need to refresh these periodically
5. **Security** - Never share these cookies publicly (they're like passwords!)

---

## 🎯 Testing Your Cookies

After pasting into OmniRoute:
1. Test each provider individually
2. If it fails, try using the FULL cookie string instead of just the main cookie
3. If still failing, get fresh cookies (log out and log back in)

---

**Generated:** 2026-07-19  
**Total Providers Configured:** 14
