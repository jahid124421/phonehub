/* ============================================================
   PhoneHub — shared helpers used by every page
   ============================================================ */
(function () {
  "use strict";

  const PH = {};

  /* ---------- cookie consent key (shared) ---------- */
  const COOKIE_KEY = "phonehub_cookie_consent";

  /* ---------- Google Analytics 4 ---------- */
  const GA_MEASUREMENT_ID = 'G-XXXXXXXXXX';

  PH.initGA4 = () => {
    // Set default consent to denied until user explicitly accepts
    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag('consent', 'default', {
      analytics_storage: 'denied'
    });

    const raw = localStorage.getItem(COOKIE_KEY);
    let accepted = false;
    if (raw) {
      try {
        const parsed = JSON.parse(raw);
        accepted = parsed && parsed.analytics;
      } catch (_) {
        // Legacy format: simple "accepted" / "declined" string
        accepted = raw === 'accepted';
      }
    }
    if (accepted) {
      PH.loadGA4Script();
    }
    // If no choice yet, GA4 will be loaded when user accepts via cookie banner
  };

  PH.loadGA4Script = () => {
    if (document.getElementById('ga4-script')) return; // already loaded

    // Update consent to granted
    window.gtag('consent', 'update', {
      analytics_storage: 'granted'
    });

    // Inject gtag.js script
    const script = document.createElement('script');
    script.id = 'ga4-script';
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
    document.head.appendChild(script);

    // Configure GA4
    window.gtag('js', new Date());
    window.gtag('config', GA_MEASUREMENT_ID);
  };

  /* ---------- image fallback (shown if a phone image fails to load) ---------- */
  PH.IMG_FALLBACK =
    "data:image/svg+xml;charset=UTF-8," +
    encodeURIComponent(
      '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="400">' +
      '<rect width="100%" height="100%" fill="#eef1f6"/>' +
      '<text x="50%" y="50%" font-family="sans-serif" font-size="18" fill="#9aa2b1" ' +
      'text-anchor="middle" dominant-baseline="middle">No image</text></svg>'
    );

  /* ---------- link helpers (work from root pages and from /phone/ pages) ----------
     Static prerendered pages set window.LINK_PREFIX="../" and window.PHONE_PREFIX=""  */
  PH.linkPrefix = () => (window.LINK_PREFIX != null ? window.LINK_PREFIX : "");
  PH.phoneUrl = (id) => (window.PHONE_PREFIX != null ? window.PHONE_PREFIX : "phone/") + id + ".html";
  // resolve an image path: leave http/data URLs alone, prefix relative ones
  PH.imgUrl = (src) => {
    if (!src) return PH.IMG_FALLBACK;
    if (/^(https?:|data:)/.test(src)) return src;
    return PH.linkPrefix() + src;
  };

  /* ---------- premium brand badges with actual logos ---------- */
  PH.BRAND_COLORS = {
    apple: "#7d7d7d", samsung: "#1428a0", google: "#1a73e8", xiaomi: "#ff6900",
    oneplus: "#eb0028", nothing: "#111111", vivo: "#4d5bff", realme: "#ffc915",
    oppo: "#1ba784", motorola: "#5c92fc", asus: "#31009c", sony: "#0b0b0b",
    nokia: "#124191", honor: "#00b0e9", huawei: "#c7000b"
  };
  
  PH._monogram = (brandId, letter, big) => {
    const color = PH.BRAND_COLORS[brandId] || "#5b8cff";
    return `<span class="brand-badge${big ? " brand-badge-lg" : ""}" style="--bc:${color}">${(letter || "?").toUpperCase()}</span>`;
  };
  
  PH.brandBadge = (brandId, name, big) => {
    const letter = ((name || brandId || "?").trim()[0] || "?").toUpperCase();
    const brand = PH.getBrand(brandId);
    
    // Use actual brand logo URL if available (not emoji)
    if (brand && brand.logo && !brand.logo.match(/[\u{1F300}-\u{1F9FF}]/u)) {
      return `<img class="brand-logo${big ? " brand-logo-lg" : ""}" src="${brand.logo}" ` +
        `alt="${name || brandId}" loading="lazy" ` +
        `onerror="this.outerHTML=PH._monogram('${brandId}','${letter}',${big ? 1 : 0})">`;
    }
    
    // Fallback to monogram
    return PH._monogram(brandId, letter, big);
  };

  /* ================= multi-currency ================= */
  PH.CCY = {
    USD: { s: "$", n: "US Dollar" }, EUR: { s: "\u20ac", n: "Euro" }, GBP: { s: "\u00a3", n: "British Pound" },
    INR: { s: "\u20b9", n: "Indian Rupee" }, NGN: { s: "\u20a6", n: "Nigerian Naira" }, JPY: { s: "\u00a5", n: "Japanese Yen" },
    CNY: { s: "\u00a5", n: "Chinese Yuan" }, AUD: { s: "A$", n: "Australian Dollar" }, CAD: { s: "C$", n: "Canadian Dollar" },
    AED: { s: "\u062f.\u0625", n: "UAE Dirham" }, PKR: { s: "\u20a8", n: "Pakistani Rupee" }, BDT: { s: "\u09f3", n: "Bangladeshi Taka" },
    BRL: { s: "R$", n: "Brazilian Real" }, ZAR: { s: "R", n: "South African Rand" }, RUB: { s: "\u20bd", n: "Russian Ruble" },
    KRW: { s: "\u20a9", n: "Korean Won" }, IDR: { s: "Rp", n: "Indonesian Rupiah" }, TRY: { s: "\u20ba", n: "Turkish Lira" },
    SAR: { s: "\ufdfc", n: "Saudi Riyal" }, MXN: { s: "MX$", n: "Mexican Peso" }, PHP: { s: "\u20b1", n: "Philippine Peso" }
  };
  PH._ccy = { code: "USD", rate: 1 };

  PH.money = (usd) => {
    if (!usd) return "Check price";
    const c = PH._ccy, info = PH.CCY[c.code] || { s: "$" };
    const val = usd * (c.rate || 1);
    const dec = ["JPY", "KRW", "IDR", "NGN"].includes(c.code) ? 0 : (val >= 1000 ? 0 : 2);
    return info.s + val.toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec });
  };

  PH._loadCcyCache = () => {
    try {
      const saved = JSON.parse(localStorage.getItem("ph_ccy") || "null");
      if (saved && saved.code && PH.CCY[saved.code]) PH._ccy = saved;
    } catch (e) {}
  };
  PH._saveCcy = () => localStorage.setItem("ph_ccy", JSON.stringify(PH._ccy));

  PH._fetchRates = async () => {
    const cached = JSON.parse(localStorage.getItem("ph_rates") || "null");
    const fresh = cached && (Date.now() - cached.t < 24 * 3600 * 1000);
    if (fresh) return cached.rates;
    try {
      const r = await fetch("https://open.er-api.com/v6/latest/USD");
      const d = await r.json();
      if (d && d.rates) { localStorage.setItem("ph_rates", JSON.stringify({ t: Date.now(), rates: d.rates })); return d.rates; }
    } catch (e) {}
    return cached ? cached.rates : null;
  };

  PH._detectCountryCcy = async () => {
    try {
      const r = await fetch("https://ipwho.is/?fields=currency_code");
      const d = await r.json();
      if (d && d.currency_code && PH.CCY[d.currency_code]) return d.currency_code;
    } catch (e) {}
    return "USD";
  };

  PH.setCurrency = (code, rates) => {
    if (!PH.CCY[code]) code = "USD";
    PH._ccy = { code, rate: (rates && rates[code]) ? rates[code] : (code === "USD" ? 1 : PH._ccy.rate) };
    PH._saveCcy();
  };

  PH.initCurrency = async () => {
    PH._loadCcyCache();               // returning visitors keep their choice; new visitors default to USD
    PH.renderCurrencyPicker();        // show the switcher immediately
    const rates = await PH._fetchRates();   // refresh rates in the background for accurate conversion
    if (rates && PH._ccy.code !== "USD") { PH.setCurrency(PH._ccy.code, rates); }
  };

  PH.renderCurrencyPicker = () => {
    const header = document.querySelector(".header-inner");
    if (!header) return;
    let sel = document.getElementById("ccyPicker");
    if (!sel) {
      sel = document.createElement("select");
      sel.id = "ccyPicker";
      sel.className = "ccy-picker";
      sel.setAttribute("aria-label", "Currency");
      header.insertBefore(sel, document.getElementById("navToggle") || null);
      sel.addEventListener("change", () => {
        const rates = JSON.parse(localStorage.getItem("ph_rates") || "null");
        PH.setCurrency(sel.value, rates && rates.rates);
        location.reload();
      });
    }
    sel.innerHTML = Object.keys(PH.CCY).map((c) =>
      `<option value="${c}" ${c === PH._ccy.code ? "selected" : ""}>${c} ${PH.CCY[c].s}</option>`).join("");
  };

  /* ---------- data access ---------- */
  PH.getPhones = () => window.PHONES || [];
  PH.getPhone = (id) => PH.getPhones().find((p) => p.id === id) || null;
  PH.getBrand = (id) => (window.BRANDS || []).find((b) => b.id === id) || { name: id, logo: "📱" };

  /* ---------- formatting (prices are stored in USD, shown in chosen currency) ---------- */
  PH.formatPrice = (n) => PH.money(n);

  PH.lowestPrice = (phone) => {
    const known = (phone.prices || []).map((p) => p.price).filter((x) => x);
    if (known.length) return Math.min(...known);
    return phone.basePrice || 0;
  };

  PH.brandName = (phone) => PH.getBrand(phone.brand).name;

  /* ---------- URL params ---------- */
  PH.param = (key) => new URLSearchParams(location.search).get(key);

  /* ---------- compare list (localStorage) ---------- */
  const CK = "phonehub_compare";
  PH.getCompare = () => {
    try { return JSON.parse(localStorage.getItem(CK)) || []; }
    catch (e) { return []; }
  };
  PH.saveCompare = (arr) => localStorage.setItem(CK, JSON.stringify(arr.slice(0, 4)));
  PH.toggleCompare = (id) => {
    let list = PH.getCompare();
    if (list.includes(id)) list = list.filter((x) => x !== id);
    else if (list.length < 4) list.push(id);
    PH.saveCompare(list);
    PH.renderCompareBar();
    return list;
  };
  PH.inCompare = (id) => PH.getCompare().includes(id);

  /* ---------- recently viewed (localStorage, last 5) ---------- */
  const VK = "phonehub_viewed";
  PH.getViewed = () => {
    try { return JSON.parse(localStorage.getItem(VK)) || []; }
    catch (e) { return []; }
  };
  PH.trackViewed = (id) => {
    let list = PH.getViewed().filter((x) => x !== id);
    list.unshift(id);
    localStorage.setItem(VK, JSON.stringify(list.slice(0, 5)));
  };

  /* ---------- reusable phone card ---------- */
  PH.hasSpecs = (phone) => Object.values(phone.quickSpecs || {}).some((v) => v);
  PH.phoneCard = (phone) => {
    const b = PH.getBrand(phone.brand);
    const price = PH.formatPrice(PH.lowestPrice(phone));
    const active = PH.inCompare(phone.id) ? "active" : "";
    return `
      <article class="card">
        <a class="card-link" href="${PH.phoneUrl(phone.id)}">
          <div class="card-img"><img src="${PH.imgUrl(phone.image)}" alt="${phone.name}" loading="lazy" data-fb="${phone.fallbackImg || ""}" onerror="this.onerror=null;this.src=PH.imgUrl(this.dataset.fb)"></div>
          <div class="card-body">
            <span class="card-brand">${PH.brandBadge(phone.brand, b.name)} ${b.name}</span>
            <h3 class="card-title">${phone.name}</h3>
            <div class="card-rating">${phone.rating ? `★ ${phone.rating} <span>(${phone.reviewCount})</span>` : "<span>Not yet rated</span>"}</div>
            <div class="card-price">${price}</div>
          </div>
        </a>
        <button class="btn-compare ${active}" data-compare="${phone.id}">
          ${PH.inCompare(phone.id) ? "✓ Added" : "⇄ Compare"}
        </button>
      </article>`;
  };

  /* ---------- reusable news card ---------- */
  PH.NEWS_DEFAULT_IMG =
    "data:image/svg+xml;charset=UTF-8," +
    encodeURIComponent(
      '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="340">' +
      '<defs><linearGradient id="ng" x1="0%" y1="0%" x2="100%" y2="100%">' +
      '<stop offset="0%" stop-color="#1a1a2e"/><stop offset="100%" stop-color="#16213e"/>' +
      '</linearGradient></defs>' +
      '<rect width="100%" height="100%" fill="url(#ng)"/>' +
      '<text x="50%" y="45%" font-family="sans-serif" font-size="48" fill="#4a6cf7" ' +
      'text-anchor="middle" dominant-baseline="middle">📰</text>' +
      '<text x="50%" y="62%" font-family="sans-serif" font-size="14" fill="#6b7280" ' +
      'text-anchor="middle" dominant-baseline="middle">Tech News</text></svg>'
    );
  PH.newsCard = (n) => {
    const date = n.date
      ? new Date(n.date).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" })
      : "";
    const meta = [n.source, date].filter(Boolean).join(" \u00b7 ");
    const imgSrc = n.image || PH.NEWS_DEFAULT_IMG;
    const hero = `<div class="news-hero"><img src="${imgSrc}" alt="" loading="lazy" onerror="this.src='${PH.NEWS_DEFAULT_IMG}'"><span class="news-hero-tag">${n.tag || "News"}</span></div>`;
    const inner = `
       ${hero}
       <div class="news-body">
         <h3>${n.title}</h3>
         <p>${n.excerpt || ""}</p>
         <span class="date">${meta}</span>
       </div>`;
    return n.url
      ? `<a class="news-card has-hero" href="${n.url}" target="_blank" rel="noopener nofollow">${inner}</a>`
      : `<article class="news-card has-hero">${inner}</article>`;
  };

  /* ---------- floating compare bar ---------- */
  PH.renderCompareBar = () => {
    let bar = document.getElementById("compareBar");
    const list = PH.getCompare();
    if (!bar) {
      bar = document.createElement("div");
      bar.id = "compareBar";
      bar.className = "compare-bar";
      document.body.appendChild(bar);
    }
    if (!list.length) { bar.classList.remove("show"); bar.innerHTML = ""; return; }
    const chips = list.map((id) => {
      const p = PH.getPhone(id);
      return `<span class="chip">${p ? p.name : id}<button data-remove="${id}">×</button></span>`;
    }).join("");
    bar.innerHTML = `
      <div class="compare-bar-inner">
        <div class="compare-chips">${chips}</div>
        <div class="compare-actions">
          <a class="btn btn-primary" href="${PH.linkPrefix()}compare.html?ids=${list.join(",")}">Compare ${list.length}</a>
          <button class="btn btn-ghost" id="clearCompare">Clear</button>
        </div>
      </div>`;
    bar.classList.add("show");
  };

  /* ---------- global click handling ---------- */
  document.addEventListener("click", (e) => {
    const cmp = e.target.closest("[data-compare]");
    if (cmp) {
      e.preventDefault();
      PH.toggleCompare(cmp.getAttribute("data-compare"));
      const on = PH.inCompare(cmp.getAttribute("data-compare"));
      cmp.classList.toggle("active", on);
      cmp.textContent = on ? "✓ Added" : "⇄ Compare";
      return;
    }
    const rm = e.target.closest("[data-remove]");
    if (rm) { PH.toggleCompare(rm.getAttribute("data-remove")); return; }
    if (e.target.id === "clearCompare") { PH.saveCompare([]); PH.renderCompareBar(); }
  });

  /* ---------- header search wiring ---------- */
  PH.wireSearch = () => {
    const form = document.getElementById("searchForm");
    if (!form) return;
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const q = form.querySelector("input").value.trim();
      location.href = PH.linkPrefix() + "search.html?q=" + encodeURIComponent(q);
    });
  };

  /* ---------- footer legal links (added to every page) ---------- */
  PH.renderFooterLegal = () => {
    document.querySelectorAll(".footer-bottom").forEach((fb) => {
      if (fb.querySelector(".footer-legal")) return;
      const p = PH.linkPrefix();
      const div = document.createElement("div");
      div.className = "footer-legal";
      div.innerHTML =
        `<a href="${p}about.html">About</a>·` +
        `<a href="${p}contact.html">Contact</a>·` +
        `<a href="${p}privacy.html">Privacy</a>·` +
        `<a href="${p}terms.html">Terms</a>·` +
        `<a href="${p}disclosure.html">Affiliate Disclosure</a>`;
      fb.appendChild(div);
    });
  };

  /* ---------- cookie consent (GDPR-compliant with categories) ---------- */
  PH.renderCookieBanner = () => {
    const saved = localStorage.getItem(COOKIE_KEY);
    if (saved) return;
    const p = PH.linkPrefix();

    /* Overlay + panel */
    const overlay = document.createElement("div");
    overlay.className = "cookie-overlay show";

    const panel = document.createElement("div");
    panel.className = "cookie-panel show";
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-label", "Cookie preferences");

    /* Main view */
    const mainView = document.createElement("div");
    mainView.className = "cookie-main-view";
    mainView.innerHTML =
      `<h3 style="margin:0 0 8px">We value your privacy</h3>` +
      `<p style="margin:0 0 14px;font-size:14px;color:var(--muted)">We use cookies to improve your experience, measure traffic, and show relevant ads. Choose your preferences below. See our <a href="${p}privacy.html">Privacy Policy</a>.</p>` +
      `<div class="cookie-actions" style="display:flex;gap:8px;flex-wrap:wrap">` +
        `<button class="btn btn-ghost" id="cookieRejectAll" style="font-size:13px">Reject All</button>` +
        `<button class="btn btn-ghost" id="cookieCustomize" style="font-size:13px">Customize</button>` +
        `<button class="btn btn-primary" id="cookieAcceptAll" style="font-size:13px">Accept All</button>` +
      `</div>`;

    /* Preferences view (hidden initially) */
    const prefsView = document.createElement("div");
    prefsView.className = "cookie-prefs-view";
    prefsView.style.display = "none";
    prefsView.innerHTML =
      `<h3 style="margin:0 0 12px">Cookie Preferences</h3>` +
      `<div class="cookie-category">` +
        `<label class="cookie-cat-row"><input type="checkbox" id="ckFunctional" checked disabled>` +
        `<div><strong>Functional</strong><br><span style="font-size:12px;color:var(--muted)">Required for site features like compare lists and theme. Cannot be disabled.</span></div></label>` +
      `</div>` +
      `<div class="cookie-category">` +
        `<label class="cookie-cat-row"><input type="checkbox" id="ckAnalytics">` +
        `<div><strong>Analytics</strong><br><span style="font-size:12px;color:var(--muted)">Help us understand how visitors use the site (e.g. Google Analytics).</span></div></label>` +
      `</div>` +
      `<div class="cookie-category">` +
        `<label class="cookie-cat-row"><input type="checkbox" id="ckAdvertising">` +
        `<div><strong>Advertising</strong><br><span style="font-size:12px;color:var(--muted)">Allow personalized ads from partners like Google AdSense.</span></div></label>` +
      `</div>` +
      `<div class="cookie-actions" style="display:flex;gap:8px;margin-top:14px">` +
        `<button class="btn btn-ghost" id="cookieBackMain" style="font-size:13px">Back</button>` +
        `<button class="btn btn-primary" id="cookieSavePrefs" style="font-size:13px">Save Preferences</button>` +
      `</div>`;

    panel.appendChild(mainView);
    panel.appendChild(prefsView);
    document.body.appendChild(overlay);
    document.body.appendChild(panel);

    const storePrefs = (analytics, advertising) => {
      const val = JSON.stringify({ functional: true, analytics, advertising });
      localStorage.setItem(COOKIE_KEY, val);
      // Also set the simple key for backward compat with GA4 init
      if (analytics || advertising) {
        localStorage.setItem(COOKIE_KEY + "_simple", "accepted");
      } else {
        localStorage.setItem(COOKIE_KEY + "_simple", "declined");
      }
      overlay.remove();
      panel.remove();
      if (analytics && typeof PH.loadGA4Script === "function") {
        PH.loadGA4Script();
      }
    };

    /* Accept All */
    mainView.querySelector("#cookieAcceptAll").addEventListener("click", () => storePrefs(true, true));
    /* Reject All */
    mainView.querySelector("#cookieRejectAll").addEventListener("click", () => storePrefs(false, false));
    /* Customize */
    mainView.querySelector("#cookieCustomize").addEventListener("click", () => {
      mainView.style.display = "none";
      prefsView.style.display = "block";
    });
    /* Back */
    prefsView.querySelector("#cookieBackMain").addEventListener("click", () => {
      prefsView.style.display = "none";
      mainView.style.display = "block";
    });
    /* Save Preferences */
    prefsView.querySelector("#cookieSavePrefs").addEventListener("click", () => {
      const analytics = prefsView.querySelector("#ckAnalytics").checked;
      const advertising = prefsView.querySelector("#ckAdvertising").checked;
      storePrefs(analytics, advertising);
    });
  };

  /* ---------- light / dark theme toggle ---------- */
  PH.initTheme = () => {
    const root = document.documentElement;
    if (!root.getAttribute("data-theme")) root.setAttribute("data-theme", "dark");
    const header = document.querySelector(".header-inner");
    if (!header || document.getElementById("themeToggle")) return;
    const icon = () => (root.getAttribute("data-theme") === "light" ? "\u{1F319}" : "\u2600\uFE0F");
    const btn = document.createElement("button");
    btn.id = "themeToggle";
    btn.className = "theme-toggle";
    btn.setAttribute("aria-label", "Toggle light/dark theme");
    btn.textContent = icon();
    header.insertBefore(btn, document.getElementById("navToggle") || null);
    btn.addEventListener("click", () => {
      const now = root.getAttribute("data-theme") === "light" ? "dark" : "light";
      root.setAttribute("data-theme", now);
      try { localStorage.setItem("ph_theme", now); } catch (e) {}
      btn.textContent = icon();
    });
  };

  /* ---------- discussion box (Giscus, backed by GitHub Discussions) ---------- */
  PH.GISCUS = { repo: "jahid124421/phonehub", repoId: "R_kgDOTVjQ_g", category: "General", categoryId: "DIC_kwDOTVjQ_s4DBB9a" };
  PH.mountDiscussion = () => {
    const box = document.getElementById("giscusBox");
    if (!box || box.dataset.loaded) return;
    box.dataset.loaded = "1";
    const s = document.createElement("script");
    s.src = "https://giscus.app/client.js";
    const attrs = {
      "data-repo": PH.GISCUS.repo, "data-repo-id": PH.GISCUS.repoId,
      "data-category": PH.GISCUS.category, "data-category-id": PH.GISCUS.categoryId,
      "data-mapping": "pathname", "data-strict": "0", "data-reactions-enabled": "1",
      "data-emit-metadata": "0", "data-input-position": "top", "data-lang": "en",
      "data-theme": document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark_dimmed"
    };
    Object.entries(attrs).forEach(([k, v]) => s.setAttribute(k, v));
    s.crossOrigin = "anonymous";
    s.async = true;
    box.appendChild(s);
  };

  /* ---------- scroll-to-top button ---------- */
  PH.mountScrollTop = () => {
    const btn = document.createElement("button");
    btn.className = "to-top";
    btn.setAttribute("aria-label", "Back to top");
    btn.innerHTML = "\u2191";
    btn.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
    document.body.appendChild(btn);
    window.addEventListener("scroll", () => btn.classList.toggle("show", window.scrollY > 500), { passive: true });
  };

  document.addEventListener("DOMContentLoaded", () => {
    PH.initTheme();
    PH.initCurrency();
    PH.mountDiscussion();
    PH.mountScrollTop();
    PH.renderCompareBar();
    PH.wireSearch();
    PH.renderFooterLegal();
    PH.initGA4();
    PH.renderCookieBanner();
    // mobile nav toggle
    const t = document.getElementById("navToggle");
    if (t) t.addEventListener("click", () => document.getElementById("navLinks").classList.toggle("open"));
  });

  window.PH = PH;
})();
