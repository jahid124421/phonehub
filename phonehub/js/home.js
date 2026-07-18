/* Homepage rendering */
(function () {
  const phones = PH.getPhones();

  if (!phones.length) {
    const g = document.getElementById("popularGrid");
    if (g) g.innerHTML = '<div class="empty">No phones loaded yet. Run the data pipeline (tools/run_all.py) or check js/data.js.</div>';
  }

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

  // news (latest 6 on home)
  document.getElementById("newsGrid").innerHTML =
    (window.NEWS || []).slice(0, 6).map(PH.newsCard).join("");

  const y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();
})();
