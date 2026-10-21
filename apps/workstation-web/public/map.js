// UNITESIS GIS view (spec 003): source geometry in projected coordinates, no basemap.
// Feature ids are the electrical ids, so selection is shared with the one-line diagram.
// Usage: UnitesisMap.render(el, geo, {busVm, branchLoading, onSelect}); UnitesisMap.select(id)
"use strict";

(function () {
  const NS = "http://www.w3.org/2000/svg";
  const state = { svg: null, onSelect: null };
  const vClass = (v) => (v === undefined ? "" : v < 0.95 ? "bad" : v < 0.97 ? "warn" : "ok");
  const lClass = (l) => (l === undefined || l === null ? "" : l > 100 ? "bad" : l > 80 ? "warn" : "ok");

  function render(container, geo, opts = {}) {
    const [xmin, ymin, xmax, ymax] = geo.extent || [0, 0, 1, 1];
    const w = Math.max(xmax - xmin, 1), h = Math.max(ymax - ymin, 1);
    const W = 900, H = Math.max(240, Math.min(700, Math.round((W * h) / w)));
    const sx = (x) => 10 + ((x - xmin) / w) * (W - 20);
    const sy = (y) => H - 10 - ((y - ymin) / h) * (H - 20);       // north up
    const svg = document.createElementNS(NS, "svg");
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    svg.setAttribute("width", "100%");
    svg.setAttribute("role", "img");
    svg.setAttribute("aria-label", `Vista GIS ${geo.network_id || ""} (${geo.crs || "CRS no declarado"})`);
    const busVm = opts.busVm || {}, loading = opts.branchLoading || {};
    for (const f of geo.features) {
      let el;
      if (f.geometry.type === "LineString") {
        el = document.createElementNS(NS, "polyline");
        el.setAttribute("points", f.geometry.coordinates.map(([x, y]) => `${sx(x).toFixed(1)},${sy(y).toFixed(1)}`).join(" "));
        el.setAttribute("class", `gis-section ${lClass(loading[f.id])}`);
      } else {
        el = document.createElementNS(NS, "circle");
        const [x, y] = f.geometry.coordinates;
        el.setAttribute("cx", sx(x).toFixed(1));
        el.setAttribute("cy", sy(y).toFixed(1));
        el.setAttribute("r", "2.2");
        el.setAttribute("class", `gis-node ${vClass(busVm[f.id])}`);
      }
      el.dataset.id = f.id;
      const t = document.createElementNS(NS, "title");
      const extra = busVm[f.id] !== undefined ? ` · ${busVm[f.id].toFixed(4)} pu`
        : loading[f.id] !== undefined && loading[f.id] !== null ? ` · ${loading[f.id].toFixed(1)} %` : "";
      t.textContent = `${f.id}${extra}`;
      el.appendChild(t);
      el.addEventListener("click", () => {
        select(f.id);
        if (state.onSelect) state.onSelect(f.id, f.properties.kind);
      });
      svg.appendChild(el);
    }
    container.replaceChildren(svg);
    state.svg = svg;
    state.onSelect = opts.onSelect || null;
    return svg;
  }

  function select(id) {
    if (!state.svg) return;
    state.svg.querySelectorAll(".gis-selected").forEach((e) => e.classList.remove("gis-selected"));
    state.svg.querySelectorAll(`[data-id="${CSS.escape(id)}"]`).forEach((e) => e.classList.add("gis-selected"));
  }

  window.UnitesisMap = { render, select };
})();
