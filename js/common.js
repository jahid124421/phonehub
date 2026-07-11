/* ============================================================
   PhoneHub — shared helpers used by every page
   ============================================================ */
(function () {
  "use strict";

  const PH = {};

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

  /* ---------- data access ---------- */
  PH.getPhones = () => window.PHONES || [];
  PH.getPhone = (id) => PH.getPhones().find((p) => p.id === id) || null;
  PH.getBrand = (id) => (window.BRANDS || []).find((b) => b.id === id) || { name: id, logo: "📱" };

  /* ---------- formatting ---------- */
  PH.formatPrice = (n) =>
    n ? "₹" + Number(n).toLocaleString("en-IN") : "Check price";

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

  /* ---------- reusable phone card ---------- */
  PH.phoneCard = (phone) => {
    const b = PH.getBrand(phone.brand);
    const price = PH.formatPrice(PH.lowestPrice(phone));
    const active = PH.inCompare(phone.id) ? "active" : "";
    return `
      <article class="card">
        <a class="card-link" href="${PH.phoneUrl(phone.id)}">
          <div class="card-img"><img src="${PH.imgUrl(phone.image)}" alt="${phone.name}" loading="lazy" data-fb="${phone.fallbackImg || ""}" onerror="this.onerror=null;this.src=PH.imgUrl(this.dataset.fb)"></div>
          <div class="card-body">
            <span class="card-brand">${b.logo} ${b.name}</span>
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

  /* ---------- cookie consent (required for AdSense / GDPR) ---------- */
  const COOKIE_KEY = "phonehub_cookie_consent";
  PH.renderCookieBanner = () => {
    if (localStorage.getItem(COOKIE_KEY)) return;
    const p = PH.linkPrefix();
    const bar = document.createElement("div");
    bar.className = "cookie-banner show";
    bar.innerHTML =
      `<p>We use cookies for functionality, analytics and ads. See our ` +
      `<a href="${p}privacy.html">Privacy Policy</a>.</p>` +
      `<div class="cookie-actions">` +
      `<button class="btn btn-ghost" id="cookieDecline">Decline</button>` +
      `<button class="btn btn-primary" id="cookieAccept">Accept</button></div>`;
    document.body.appendChild(bar);
    const close = (v) => { localStorage.setItem(COOKIE_KEY, v); bar.remove(); };
    bar.querySelector("#cookieAccept").addEventListener("click", () => close("accepted"));
    bar.querySelector("#cookieDecline").addEventListener("click", () => close("declined"));
  };

  document.addEventListener("DOMContentLoaded", () => {
    PH.renderCompareBar();
    PH.wireSearch();
    PH.renderFooterLegal();
    PH.renderCookieBanner();
    // mobile nav toggle
    const t = document.getElementById("navToggle");
    if (t) t.addEventListener("click", () => document.getElementById("navLinks").classList.toggle("open"));
  });

  window.PH = PH;
})();
