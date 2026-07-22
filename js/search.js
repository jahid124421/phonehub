/* Catalog: search + category + brand + rating filters + sort + pagination */
(function () {
  const grid = document.getElementById("resultsGrid");
  const countEl = document.getElementById("resultCount");
  const priceRange = document.getElementById("priceRange");
  const priceLabel = document.getElementById("priceLabel");
  const sortSelect = document.getElementById("sortSelect");
  const paginationEl = document.getElementById("pagination");

  const PER_PAGE = 20;

  const CAT_LABELS = { phone: "Phones", tablet: "Tablets", laptop: "Laptops",
    tv: "TVs", smartwatch: "Watches", earbuds: "Earbuds", headphones: "Headphones",
    camera: "Cameras", console: "Consoles", appliance: "Appliances", auto: "Auto" };

  const state = {
    q: (PH.param("q") || "").toLowerCase(),
    cat: PH.param("cat") || "all",
    brands: new Set(PH.param("brand") ? [PH.param("brand")] : []),
    maxPrice: Number(priceRange.max),
    minRating: 0,
    sort: PH.param("sort") || "popularity",
    page: 1
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
      state.page = 1; apply();
    });
  }

  // brand checkboxes (with real logos)
  document.getElementById("brandFilters").innerHTML = (window.BRANDS || []).map((b) =>
    `<label><input type="checkbox" value="${b.id}" ${state.brands.has(b.id) ? "checked" : ""}> ${PH.brandBadge(b.id, b.name)} ${b.name}</label>`
  ).join("");

  const crumb = document.getElementById("crumbLabel");
  if (state.q && crumb) crumb.textContent = `Search: "${state.q}"`;
  else if (state.cat !== "all" && crumb) crumb.textContent = CAT_LABELS[state.cat] || state.cat;

  /* ---- helpers ---- */
  function renderPagination(totalItems) {
    const totalPages = Math.ceil(totalItems / PER_PAGE);
    if (totalPages <= 1) { paginationEl.innerHTML = ""; return; }

    let html = "";
    // Previous
    html += `<button data-page="prev" ${state.page === 1 ? "disabled" : ""}>← Prev</button>`;

    // Page numbers with ellipsis
    const pages = buildPageNumbers(state.page, totalPages);
    pages.forEach((p) => {
      if (p === "…") {
        html += `<span class="pg-ellipsis">…</span>`;
      } else {
        html += `<button data-page="${p}" ${p === state.page ? 'class="active"' : ""}>${p}</button>`;
      }
    });

    // Next
    html += `<button data-page="next" ${state.page === totalPages ? "disabled" : ""}>Next →</button>`;

    paginationEl.innerHTML = html;
  }

  function buildPageNumbers(current, total) {
    // Show first, last, and up to 2 neighbours around current
    const delta = 2;
    const range = [];
    const rangeWithDots = [];
    let l;
    for (let i = 1; i <= total; i++) {
      if (i === 1 || i === total || (i >= current - delta && i <= current + delta)) {
        range.push(i);
      }
    }
    range.forEach((i) => {
      if (l) {
        if (i - l === 2) rangeWithDots.push(l + 1);
        else if (i - l > 2) rangeWithDots.push("…");
      }
      rangeWithDots.push(i);
      l = i;
    });
    return rangeWithDots;
  }

  function goToPage(p, totalPages) {
    if (p === "prev") state.page = Math.max(1, state.page - 1);
    else if (p === "next") state.page = Math.min(totalPages, state.page + 1);
    else state.page = Number(p);
    renderPage();
    // scroll to top of results
    const top = grid.closest(".layout") || grid;
    top.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  paginationEl.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-page]");
    if (!btn || btn.disabled) return;
    const totalPages = Math.ceil(filteredCache.length / PER_PAGE);
    goToPage(btn.getAttribute("data-page"), totalPages);
  });

  /* ---- filter + sort + render ---- */
  let filteredCache = []; // keep reference for pagination clicks

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

    filteredCache = list;
    renderPage();
  }

  function renderPage() {
    const list = filteredCache;
    const total = list.length;
    const totalPages = Math.ceil(total / PER_PAGE);
    if (state.page > totalPages) state.page = Math.max(1, totalPages);

    const start = (state.page - 1) * PER_PAGE;
    const pageItems = list.slice(start, start + PER_PAGE);

    // Update count label: "Showing 1-20 of 347 products"
    if (total === 0) {
      countEl.textContent = "0 products";
    } else {
      const from = start + 1;
      const to = Math.min(start + PER_PAGE, total);
      countEl.textContent = `Showing ${from}–${to} of ${total} ${total !== 1 ? "products" : "product"}`;
    }

    grid.innerHTML = pageItems.length
      ? pageItems.map(PH.phoneCard).join("")
      : `<div class="empty">Nothing matches your filters. Try widening them.</div>`;

    renderPagination(total);
  }

  /* ---- event listeners (reset page to 1 on filter change) ---- */
  document.getElementById("brandFilters").addEventListener("change", (e) => {
    const v = e.target.value;
    if (e.target.checked) state.brands.add(v); else state.brands.delete(v);
    state.page = 1; apply();
  });
  priceRange.addEventListener("input", () => {
    state.maxPrice = Number(priceRange.value);
    priceLabel.textContent = PH.formatPrice(state.maxPrice);
    state.page = 1; apply();
  });
  document.querySelectorAll("input[name=rating]").forEach((r) =>
    r.addEventListener("change", () => { state.minRating = Number(r.value); state.page = 1; apply(); }));
  sortSelect.addEventListener("change", () => { state.sort = sortSelect.value; state.page = 1; apply(); });
  document.getElementById("resetFilters").addEventListener("click", () => {
    state.brands.clear(); state.maxPrice = Number(priceRange.max); state.minRating = 0; state.q = ""; state.cat = "all"; state.page = 1;
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
