/* Homepage rendering */
(function () {
  const phones = PH.getPhones();
  // Only consider actual phones (not cars, laptops, etc.) for guides
  const onlyPhones = phones.filter((p) => p.category === "phone" || !p.category);

  if (!phones.length) {
    const g = document.getElementById("popularGrid");
    if (g) g.innerHTML = '<div class="empty">No phones loaded yet. Run the data pipeline (tools/run_all.py) or check js/data.js.</div>';
  }

  // trending carousel (top 8 by rating × popularity blend)
  const trending = [...onlyPhones]
    .sort((a, b) => (b.rating * b.popularity) - (a.rating * a.popularity))
    .slice(0, 8);
  const trendingEl = document.getElementById("trendingScroll");
  if (trendingEl) trendingEl.innerHTML = trending.map(PH.phoneCard).join("");

  // popular
  const popular = [...phones].sort((a, b) => b.popularity - a.popularity).slice(0, 8);
  document.getElementById("popularGrid").innerHTML = popular.map(PH.phoneCard).join("");

  // latest
  const latest = [...phones].sort((a, b) => new Date(b.releaseDate) - new Date(a.releaseDate)).slice(0, 8);
  document.getElementById("latestGrid").innerHTML = latest.map(PH.phoneCard).join("");

  // brands - grouped by category
  const brandsByCategory = {};
  const categoryOrder = ["Premium", "Gaming", "Mid-Range", "Value", "Budget", "Auto", "Other"];
  
  (window.BRANDS || []).forEach((b) => {
    const cat = b.category || "Other";
    if (!brandsByCategory[cat]) brandsByCategory[cat] = [];
    brandsByCategory[cat].push(b);
  });
  
  let brandsHTML = "";
  categoryOrder.forEach((category) => {
    const brands = brandsByCategory[category];
    if (!brands || brands.length === 0) return;
    
    brandsHTML += `<div class="brand-category">
      <h3 class="category-title">${category}</h3>
      <div class="category-brands">`;
    
    brands.forEach((b) => {
      brandsHTML += `<a class="brand-tile" href="search.html?brand=${b.id}">
        ${PH.brandBadge(b.id, b.name, true)}
        <div>${b.name}</div>
      </a>`;
    });
    
    brandsHTML += `</div></div>`;
  });
  
  document.getElementById("brandsGrid").innerHTML = brandsHTML;

  /* ---------- Best Phones buying guides ---------- */
  const guideConfigs = [
    {
      title: "Best Phones Under $200",
      desc: "Top value picks that punch above their weight",
      icon: "💰",
      filter: (p) => PH.lowestPrice(p) > 0 && PH.lowestPrice(p) <= 200,
      sort: (a, b) => b.rating - a.rating,
      why: (p) => p.rating >= 4.3 ? "Excellent value for money" : p.rating >= 4 ? "Great specs for the price" : "Budget-friendly pick"
    },
    {
      title: "Best Phones Under $500",
      desc: "Premium features without the flagship price tag",
      icon: "⭐",
      filter: (p) => PH.lowestPrice(p) > 0 && PH.lowestPrice(p) <= 500,
      sort: (a, b) => b.rating - a.rating,
      why: (p) => p.rating >= 4.4 ? "Top-rated in this range" : p.rating >= 4 ? "Best bang for your buck" : "Strong all-rounder"
    },
    {
      title: "Best Flagship Phones",
      desc: "No-compromise premium devices",
      icon: "👑",
      filter: (p) => PH.lowestPrice(p) >= 700,
      sort: (a, b) => b.rating - a.rating,
      why: (p) => p.rating >= 4.5 ? "Editor's choice" : p.rating >= 4.2 ? "Top-tier performance" : "Premium experience"
    },
    {
      title: "Best Camera Phones",
      desc: "For photography enthusiasts and content creators",
      icon: "📸",
      filter: (p) => {
        const cam = (p.quickSpecs && p.quickSpecs.camera) || "";
        // Match MP numbers >= 48 in camera spec string
        const mpMatch = cam.match(/(\d+)\s*MP/);
        return mpMatch && parseInt(mpMatch[1]) >= 48 && p.rating >= 4.0;
      },
      sort: (a, b) => b.rating - a.rating,
      why: (p) => p.rating >= 4.5 ? "Outstanding photo quality" : p.rating >= 4.2 ? "Pro-level camera system" : "Great camera for the price"
    },
    {
      title: "Best Battery Life Phones",
      desc: "All-day power for heavy users",
      icon: "🔋",
      filter: (p) => {
        const bat = (p.quickSpecs && p.quickSpecs.battery) || "";
        // Match mAh values >= 4500
        const mahMatch = bat.match(/(\d{3,5})\s*mAh/i);
        return mahMatch && parseInt(mahMatch[1]) >= 4500;
      },
      sort: (a, b) => b.rating - a.rating,
      why: (p) => {
        const bat = (p.quickSpecs && p.quickSpecs.battery) || "";
        const mahMatch = bat.match(/(\d{3,5})\s*mAh/i);
        const mah = mahMatch ? parseInt(mahMatch[1]) : 0;
        return mah >= 5500 ? "Massive battery — 2-day usage" : mah >= 5000 ? "All-day heavy use" : "Reliable all-day battery";
      }
    }
  ];

  const guidesEl = document.getElementById("guidesGrid");
  if (guidesEl) {
    let guidesHTML = "";
    guideConfigs.forEach((cfg) => {
      const items = onlyPhones
        .filter(cfg.filter)
        .sort(cfg.sort)
        .slice(0, 5);
      if (!items.length) return;

      guidesHTML += `<div class="guide-card">
        <div class="guide-header">
          <h3>${cfg.icon} ${cfg.title}</h3>
          <p>${cfg.desc}</p>
        </div>
        <div class="guide-list">`;

      items.forEach((p) => {
        const price = PH.formatPrice(PH.lowestPrice(p));
        const img = PH.imgUrl(p.image);
        const fb = p.fallbackImg || "";
        guidesHTML += `<a class="guide-item" href="${PH.phoneUrl(p.id)}">
          <img src="${img}" alt="${p.name}" loading="lazy" onerror="this.onerror=null;this.src=PH.imgUrl('${fb}')">
          <div class="guide-item-info">
            <div class="guide-item-name">${p.name}</div>
            <div class="guide-item-meta">★ ${p.rating} · ${price}</div>
            <div class="guide-item-why">${cfg.why(p)}</div>
          </div>
        </a>`;
      });

      guidesHTML += `</div></div>`;
    });
    guidesEl.innerHTML = guidesHTML;
  }

  // news (latest 6 on home)
  document.getElementById("newsGrid").innerHTML =
    (window.NEWS || []).slice(0, 6).map(PH.newsCard).join("");

  const y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();
})();
