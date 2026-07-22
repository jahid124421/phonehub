/* Phone detail page */
(function () {
  const main = document.getElementById("phoneMain");
  const phone = PH.getPhone(PH.param("id"));

  if (!phone) {
    main.innerHTML = `<div class="empty">Phone not found. <a href="search.html">Browse all phones →</a></div>`;
    return;
  }

  // canonical -> the static prerendered page (avoids duplicate-content issues)
  const canon = document.createElement("link");
  canon.rel = "canonical";
  canon.href = "phone/" + phone.id + ".html";
  document.head.appendChild(canon);

  document.getElementById("pageTitle").textContent = `${phone.name} — Specs, Price & Review | PhoneHub`;
  document.getElementById("pageDesc").setAttribute("content",
    `${phone.name} full specifications: ${phone.quickSpecs.display}, ${phone.quickSpecs.processor}, ${phone.quickSpecs.camera}. Compare prices and read reviews.`);

  const b = PH.getBrand(phone.brand);
  const lowest = PH.lowestPrice(phone);

  // Track recently viewed
  PH.trackViewed(phone.id);

  // quick specs
  const qs = Object.entries(phone.quickSpecs).map(([k, v]) =>
    `<div class="qs"><div class="k">${k}</div><div class="v">${v}</div></div>`).join("");

  // price table — known prices first (cheapest flagged), unknown after
  const sortedPrices = [...(phone.prices || [])].sort((a, b) => {
    const pa = a.price || Infinity, pb = b.price || Infinity;
    return pa - pb;
  });
  const firstKnown = sortedPrices.findIndex((p) => p.price);
  const priceRows = sortedPrices.length
    ? sortedPrices.map((p, i) =>
      `<tr>
         <td>${p.store}</td>
         <td class="${i === firstKnown ? "best" : ""}">${PH.formatPrice(p.price)}${i === firstKnown ? " · Best" : ""}</td>
         <td><a class="btn btn-primary" href="${p.url}" rel="nofollow sponsored" target="_blank">Buy</a></td>
       </tr>`).join("")
    : `<tr><td colspan="3" style="color:var(--muted)">No store links yet.</td></tr>`;

  // pros/cons
  const pros = (phone.pros || []).map((x) => `<li>${x}</li>`).join("") || "<li>—</li>";
  const cons = (phone.cons || []).map((x) => `<li>${x}</li>`).join("") || "<li>—</li>";
  const reviewHtml = phone.review
    ? `<p style="margin:0 0 16px;font-size:15px;line-height:1.6">${phone.review}</p>`
    : "";

  // full specs (lite data.js may omit specs; static /phone/ pages have them baked)
  const specBlocks = Object.entries(phone.specs || {}).map(([section, rows]) => {
    const trs = Object.entries(rows).map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`).join("");
    return `<div class="spec-block"><h3>${section}</h3><table class="spec-table">${trs}</table></div>`;
  }).join("");

  // similar phones (same brand or nearby price)
  const similar = PH.getPhones()
    .filter((p) => p.id !== phone.id)
    .sort((a, b) => Math.abs(PH.lowestPrice(a) - lowest) - Math.abs(PH.lowestPrice(b) - lowest))
    .slice(0, 4);

  // recently viewed
  const viewedIds = PH.getViewed();
  const recentlyViewed = viewedIds
    .filter((id) => id !== phone.id)
    .map((id) => PH.getPhone(id))
    .filter(Boolean)
    .slice(0, 5);

  // video reviews
  const ytQuery = encodeURIComponent(phone.name + " review");
  const ytUrl = `https://www.youtube.com/results?search_query=${ytQuery}`;

  main.innerHTML = `
    <p class="crumb"><a href="index.html">Home</a> / <a href="search.html?brand=${phone.brand}">${b.name}</a> / ${phone.name}</p>

    <div class="phone-top">
      <div class="phone-gallery"><img src="${PH.imgUrl(phone.image)}" alt="${phone.name}" data-fb="${phone.fallbackImg || ""}" onerror="this.onerror=null;this.src=PH.imgUrl(this.dataset.fb)"></div>
      <div class="phone-info">
        <h1>${phone.name}</h1>
        <div class="phone-meta">${b.logo} ${b.name} · Released ${new Date(phone.releaseDate).toLocaleDateString("en-IN", { month: "short", year: "numeric" })}</div>
        <div class="big-rating">★ ${phone.rating} <span style="color:var(--muted);font-size:15px;font-weight:400">based on ${phone.reviewCount} reviews</span></div>
        <div style="margin:14px 0;font-size:26px;font-weight:800">${PH.formatPrice(lowest)} <span style="font-size:14px;color:var(--muted);font-weight:400">lowest price</span></div>
        <button class="btn ${PH.inCompare(phone.id) ? "btn-primary" : "btn-ghost"}" data-compare="${phone.id}">${PH.inCompare(phone.id) ? "✓ Added to compare" : "⇄ Add to compare"}</button>
        <div class="quick-specs">${qs}</div>
      </div>
    </div>

    <section>
      <h2>💰 Price comparison</h2>
      <table class="price-table">
        <thead><tr><th>Store</th><th>Price</th><th></th></tr></thead>
        <tbody>${priceRows}</tbody>
      </table>
    </section>

    <section>
      <h2>Expert verdict</h2>
      ${reviewHtml}
      <div class="proscons">
        <div class="pros"><h4>👍 Pros</h4><ul>${pros}</ul></div>
        <div class="cons"><h4>👎 Cons</h4><ul>${cons}</ul></div>
      </div>
    </section>

    <section>
      <div class="video-section">
        <h2>🎬 Video reviews</h2>
        <p>Watch hands-on reviews and unboxing videos for the ${phone.name} on YouTube.</p>
        <a class="video-btn" href="${ytUrl}" target="_blank" rel="noopener nofollow">
          <svg viewBox="0 0 24 24"><path d="M23.5 6.2c-.3-1-1-1.8-2-2.1C19.7 3.5 12 3.5 12 3.5s-7.7 0-9.5.6c-1 .3-1.7 1.1-2 2.1C0 8.1 0 12 0 12s0 3.9.5 5.8c.3 1 1 1.8 2 2.1 1.8.6 9.5.6 9.5.6s7.7 0 9.5-.6c1-.3 1.7-1.1 2-2.1.5-1.9.5-5.8.5-5.8s0-3.9-.5-5.8zM9.6 15.6V8.4l6.4 3.6-6.4 3.6z"/></svg>
          Watch reviews on YouTube
        </a>
      </div>
    </section>

    <section>
      <h2>Full specifications</h2>
      ${specBlocks}
    </section>

    ${recentlyViewed.length ? `
    <section>
      <div class="section-head"><h2>🕐 Recently viewed</h2></div>
      <div class="recently-viewed-scroll">${recentlyViewed.map(PH.phoneCard).join("")}</div>
    </section>` : ""}

    <section>
      <div class="section-head"><h2>Similar phones</h2></div>
      <div class="grid">${similar.map(PH.phoneCard).join("")}</div>
    </section>
  `;

  // ---- schema.org structured data (rich results in Google) ----
  const ld = {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": phone.name,
    "image": phone.image,
    "brand": { "@type": "Brand", "name": b.name },
    "description": phone.review ||
      `${phone.name}: ${phone.quickSpecs.display}, ${phone.quickSpecs.processor}, ${phone.quickSpecs.camera}.`
  };
  if (phone.rating) {
    ld.aggregateRating = {
      "@type": "AggregateRating",
      "ratingValue": String(phone.rating),
      "reviewCount": String(phone.reviewCount || 1),
      "bestRating": "5", "worstRating": "1"
    };
  }
  if (lowest) {
    ld.offers = {
      "@type": "AggregateOffer",
      "priceCurrency": "INR",
      "lowPrice": String(lowest),
      "offerCount": String((phone.prices || []).length || 1)
    };
  }
  const breadcrumb = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Home", "item": location.origin + "/index.html" },
      { "@type": "ListItem", "position": 2, "name": b.name, "item": location.origin + "/search.html?brand=" + phone.brand },
      { "@type": "ListItem", "position": 3, "name": phone.name }
    ]
  };
  [ld, breadcrumb].forEach((obj) => {
    const s = document.createElement("script");
    s.type = "application/ld+json";
    s.textContent = JSON.stringify(obj);
    document.head.appendChild(s);
  });

  const y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();
})();
