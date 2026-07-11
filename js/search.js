/* Search + filter + sort page */
(function () {
  const grid = document.getElementById("resultsGrid");
  const countEl = document.getElementById("resultCount");
  const priceRange = document.getElementById("priceRange");
  const priceLabel = document.getElementById("priceLabel");
  const sortSelect = document.getElementById("sortSelect");

  const state = {
    q: (PH.param("q") || "").toLowerCase(),
    brands: new Set(PH.param("brand") ? [PH.param("brand")] : []),
    maxPrice: Number(priceRange.max),
    minRating: 0,
    sort: PH.param("sort") || "popularity"
  };
  sortSelect.value = ["popularity", "newest", "priceLow", "priceHigh", "rating"].includes(state.sort) ? state.sort : "popularity";

  // build brand checkboxes
  document.getElementById("brandFilters").innerHTML = (window.BRANDS || []).map((b) =>
    `<label><input type="checkbox" value="${b.id}" ${state.brands.has(b.id) ? "checked" : ""}> ${b.logo} ${b.name}</label>`
  ).join("");

  if (state.q) {
    document.getElementById("crumbLabel").textContent = `Search: "${state.q}"`;
  }

  function apply() {
    let list = PH.getPhones().filter((p) => {
      if (state.q) {
        const hay = (p.name + " " + PH.brandName(p) + " " + JSON.stringify(p.quickSpecs)).toLowerCase();
        if (!hay.includes(state.q)) return false;
      }
      if (state.brands.size && !state.brands.has(p.brand)) return false;
      if (PH.lowestPrice(p) > state.maxPrice) return false;
      if (p.rating < state.minRating) return false;
      return true;
    });

    const sorters = {
      popularity: (a, b) => b.popularity - a.popularity,
      newest: (a, b) => new Date(b.releaseDate) - new Date(a.releaseDate),
      priceLow: (a, b) => PH.lowestPrice(a) - PH.lowestPrice(b),
      priceHigh: (a, b) => PH.lowestPrice(b) - PH.lowestPrice(a),
      rating: (a, b) => b.rating - a.rating
    };
    list.sort(sorters[state.sort] || sorters.popularity);

    countEl.textContent = `${list.length} phone${list.length !== 1 ? "s" : ""}`;
    grid.innerHTML = list.length
      ? list.map(PH.phoneCard).join("")
      : `<div class="empty">No phones match your filters. Try widening them.</div>`;
  }

  // events
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
    state.brands.clear(); state.maxPrice = Number(priceRange.max); state.minRating = 0; state.q = "";
    priceRange.value = priceRange.max; priceLabel.textContent = PH.formatPrice(state.maxPrice);
    document.querySelectorAll("#brandFilters input").forEach((c) => (c.checked = false));
    document.querySelector("input[name=rating][value='0']").checked = true;
    apply();
  });

  priceLabel.textContent = PH.formatPrice(state.maxPrice);
  apply();
  const y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();
})();
