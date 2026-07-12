/* Compare page — side by side spec table */
(function () {
  const area = document.getElementById("compareArea");

  // ids can come from ?ids=a,b,c or from the saved compare list
  const fromUrl = (PH.param("ids") || "").split(",").filter(Boolean);
  let ids = fromUrl.length ? fromUrl : PH.getCompare();
  if (fromUrl.length) PH.saveCompare(fromUrl);

  function render() {
    ids = PH.getCompare();
    const phones = ids.map(PH.getPhone).filter(Boolean);

    if (phones.length < 2) {
      area.innerHTML = `<div class="empty">
        Add at least 2 phones to compare.<br><br>
        <a class="btn btn-primary" href="search.html">Browse phones →</a>
      </div>`;
      PH.renderCompareBar();
      return;
    }

    // full specs live in window.SPECS (loaded via specs-data.js)
    const specsOf = (p) => (window.SPECS && window.SPECS[p.id]) || p.specs || {};

    // collect every spec section+key across selected phones so rows align
    const sections = {};
    phones.forEach((p) => {
      Object.entries(specsOf(p)).forEach(([sec, rows]) => {
        sections[sec] = sections[sec] || new Set();
        Object.keys(rows).forEach((k) => sections[sec].add(k));
      });
    });

    const headCells = phones.map((p) =>
      `<th>
         <a href="${PH.phoneUrl(p.id)}"><img src="${PH.imgUrl(p.image)}" alt="${p.name}" data-fb="${p.fallbackImg || ""}" onerror="this.onerror=null;this.src=PH.imgUrl(this.dataset.fb)" style="height:120px;object-fit:contain;background:#fff;border-radius:8px;padding:6px"></a>
         <div style="margin-top:8px">${p.name}</div>
         <button class="btn btn-ghost" data-remove="${p.id}" style="margin-top:8px;padding:4px 10px">Remove</button>
       </th>`).join("");

    // top summary rows
    const summary = [
      ["Lowest price", (p) => `<strong>${PH.formatPrice(PH.lowestPrice(p))}</strong>`],
      ["Rating", (p) => `★ ${p.rating} (${p.reviewCount})`],
      ["Released", (p) => new Date(p.releaseDate).toLocaleDateString("en-IN", { month: "short", year: "numeric" })]
    ].map(([label, fn]) =>
      `<tr><td>${label}</td>${phones.map((p) => `<td>${fn(p)}</td>`).join("")}</tr>`).join("");

    // detailed spec rows, highlighting differences
    const specRows = Object.entries(sections).map(([sec, keys]) => {
      const header = `<tr><th colspan="${phones.length + 1}" style="text-align:left;background:var(--surface-2)">${sec}</th></tr>`;
      const rows = [...keys].map((k) => {
        const vals = phones.map((p) => { const s = specsOf(p); return (s[sec] && s[sec][k]) || "—"; });
        const allSame = vals.every((v) => v === vals[0]);
        const cells = vals.map((v) =>
          `<td style="${allSame ? "" : "background:rgba(76,125,255,.08)"}">${v}</td>`).join("");
        return `<tr><td>${k}</td>${cells}</tr>`;
      }).join("");
      return header + rows;
    }).join("");

    area.innerHTML = `
      <div class="ad-slot">Advertisement <small>above-the-fold unit</small></div>
      <div class="compare-scroll">
        <table class="compare-table">
          <thead><tr><th></th>${headCells}</tr></thead>
          <tbody>
            ${summary}
            ${specRows}
          </tbody>
        </table>
      </div>
      <p style="color:var(--muted);font-size:13px;margin-top:10px">Highlighted cells indicate where the phones differ.</p>
    `;
    PH.renderCompareBar();
  }

  // re-render when compare list changes via the global handlers
  const origToggle = PH.toggleCompare;
  PH.toggleCompare = function (id) { const r = origToggle(id); render(); return r; };

  render();
  const y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();
})();
