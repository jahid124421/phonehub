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

  // brands
  document.getElementById("brandsGrid").innerHTML = (window.BRANDS || []).map((b) =>
    `<a class="brand-tile" href="search.html?brand=${b.id}"><span class="b-logo">${b.logo}</span>${b.name}</a>`
  ).join("");

  // news
  document.getElementById("newsGrid").innerHTML = (window.NEWS || []).map((n) =>
    `<article class="news-card">
       <span class="tag">${n.tag}</span>
       <h3>${n.title}</h3>
       <p>${n.excerpt}</p>
       <span class="date">${new Date(n.date).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" })}</span>
     </article>`
  ).join("");

  const y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();
})();
