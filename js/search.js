/* Catalog: search + category + brand + rating filters + sort */
(function () {
  const grid = document.getElementById("resultsGrid");
  const countEl = document.getElementById("resultCount");
  const priceRange = document.getElementById("priceRange");
  const priceLabel = document.getElementById("priceLabel");
  const sortSelect = document.getElementById("sortSelect");

  const CAT_LABELS = { phone: "Phones", tablet: "Tablets", laptop: "Laptops",
    tv: "TVs", smartwatch: "Watches", earbuds: "Earbuds", headphones: "Headphones",
    camera: "Cameras", console: "Consoles", appliance: "Appliances", auto: "Auto" };

  const state = {
    q: (PH.param("q") || "").toLowerCase(),
    cat: PH.param("cat") || "all",
    brands: new Set(PH.param("brand") ? [PH.param("brand")] : []),
    maxPrice: Number(priceRange.max),
    minRating: 0,
    sort: PH.param("sort") || "popularity"
  };
  sortSelect.value = ["popularity", "newest", "priceLow", "priceHigh", "rating"].includes(state.sort) ? state.sort : "popularity";

  const catOf = (p) => p.category || "phone";

  // category chips (only categories that exist in the data)
  const cats = Array.from(new Set(PH.getPhones().map(catOf)));
  const catBar = document.getElementById("catFilters");
  if (catBar) {
    const chips = ["all"].concat(cats);
    catBar.innerHTML = chips.map((c) =>
      `<button class="news-chip ${c === state.cat ? "active" : ""}" data-cat="${c}">${c === "all" ? "All" : (CAT_LABELS[c] || c)}</button>`
    ).join("");
    catBar.addEventListener("click", (e) => {
      const b = e.target.closest("[data-cat]"); if (!b) return;
      state.cat = b.getAttribute("data-cat");
      catBar.querySelectorAll(".news-chip").forEach((x) => x.classList.toggle("active", x === b));
      apply();
    });
  }

  // brand checkboxes (with real logos)
  document.getElementById("brandFilters").innerHTML = (window.BRANDS || []).map((b) =>
    `<label><input type="checkbox" value="${b.id}" ${state.brands.has(b.id) ? "checked" : ""}> ${PH.brandBadge(b.id, b.name)} ${b.name}</label>`
  ).join("");

  const crumb = document.getElementById("crumbLabel");
  if (state.q && crumb) crumb.textContent = `Search: "${state.q}"`;
  else if (state.cat !== "all" && crumb) crumb.textContent = CAT_LABELS[state.cat] || state.cat;

  function apply() {
    let list = PH.getPhones().filter((p) => {
      if (state.cat !== "all" && catOf(p) !== state.cat) return false;
      if (state.q) {
        const hay = (p.name + " " + PH.brandName(p) + " " + JSON.stringify(p.quickSpecs)).toLowerCase();
        if (!hay.includes(state.q)) return false;
      }
      if (state.brands.size && !state.brands.has(p.brand)) return false;
      const lp = PH.lowestPrice(p);
      if (lp && lp > state.maxPrice) return false;
      if (p.rating < state.minRating) return false;
      return true;
    });

    const sorters = {
      popularity: (a, b) => b.popularity - a.popularity,
      newest: (a, b) => new Date(b.releaseDate) - new Date(a.releaseDate),
      priceLow: (a, b) => (PH.lowestPrice(a) || 1e12) - (PH.lowestPrice(b) || 1e12),
      priceHigh: (a, b) => PH.lowestPrice(b) - PH.lowestPrice(a),
      rating: (a, b) => b.rating - a.rating
    };
    list.sort(sorters[state.sort] || sorters.popularity);

    countEl.textContent = `${list.length} ${list.length !== 1 ? "products" : "product"}`;
    grid.innerHTML = list.length
      ? list.map(PH.phoneCard).join("")
      : `<div class="empty">Nothing matches your filters. Try widening them.</div>`;
  }

  document.getElementById("brandFilters").addEventListener("change", (e) => {
    const v = e.target.value;
    if (e.target.checked) state.brands.add(v); else state.brands.delete(v);
    apply();
  });
  priceRange.addEventListener("input", () => {
    state.maxPrice = Number(priceRange.value);
    priceLabel.textContent = PH.formatPrice(state.maxPrice);
    apply();
  });
  document.querySelectorAll("input[name=rating]").forEach((r) =>
    r.addEventListener("change", () => { state.minRating = Number(r.value); apply(); }));
  sortSelect.addEventListener("change", () => { state.sort = sortSelect.value; apply(); });
  document.getElementById("resetFilters").addEventListener("click", () => {
    state.brands.clear(); state.maxPrice = Number(priceRange.max); state.minRating = 0; state.q = ""; state.cat = "all";
    priceRange.value = priceRange.max; priceLabel.textContent = PH.formatPrice(state.maxPrice);
    document.querySelectorAll("#brandFilters input").forEach((c) => (c.checked = false));
    document.querySelector("input[name=rating][value='0']").checked = true;
    if (catBar) catBar.querySelectorAll(".news-chip").forEach((x) => x.classList.toggle("active", x.getAttribute("data-cat") === "all"));
    apply();
  });

  priceLabel.textContent = PH.formatPrice(state.maxPrice);
  apply();
  const y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();
})();
