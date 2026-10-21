// UNITESIS workstation: thin client over control-api v1. No electrical computation here.
"use strict";

const API = "/api/v1";
const state = { snapshot: null, sha: null, pending: null, basisExample: null };
const $ = (sel) => document.querySelector(sel);
const esc = (v) => String(v).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const fmt = (v, d = 4) => (v === null || v === undefined ? "—" : Number(v).toFixed(d));

async function api(path, opts = {}) {
  const res = await fetch(API + path, {
    headers: { "Content-Type": "application/json" }, ...opts,
    body: opts.body ? JSON.stringify(opts.body) : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const d = data.detail;
    const reason = typeof d === "string" ? d : d?.reason
      || (d?.quarantine ? d.quarantine.map((q) => `${q.element_id}.${q.field}: ${q.reason}`).join("; ") : JSON.stringify(d));
    throw new Error(`${res.status} · ${reason}`);
  }
  return data;
}

async function waitJob(job) {
  for (let i = 0; i < 600; i++) {
    const j = await api(`/jobs/${job.job_id}`);
    if (j.status === "finished" || j.status === "failed") return j;
    await new Promise((r) => setTimeout(r, 300));
  }
  throw new Error("tiempo de espera agotado");
}

function setMsg(el, text, kind = "") { el.textContent = text; el.className = "msg " + kind; }
function vClass(v) { return v < 0.95 ? "bad" : v < 0.97 ? "warn" : "ok"; }
function lClass(l) { return l === null || l === undefined ? "ok" : l > 100 ? "bad" : l > 80 ? "warn" : "ok"; }

// ---------- one-line diagram ----------
function drawDiagram(snap, result) {
  const buses = snap.buses.map((b) => b.bus_id);
  const branches = [
    ...snap.lines.map((l) => ({ id: l.line_id, a: l.from_bus, b: l.to_bus, kind: "line", closed: l.in_service })),
    ...snap.switches.map((s) => ({ id: s.switch_id, a: s.from_bus, b: s.to_bus, kind: "switch", closed: s.closed })),
  ];
  const adj = new Map(buses.map((b) => [b, []]));
  branches.forEach((br) => { adj.get(br.a).push(br); adj.get(br.b).push(br); });
  // closed branches first so the drawn tree follows the energized radial structure
  adj.forEach((list) => list.sort((x, y) => Number(y.closed) - Number(x.closed)));
  const roots = snap.slacks.map((s) => s.bus);
  const depth = new Map(), children = new Map(buses.map((b) => [b, []])), treeEdge = new Set();
  const queue = [...roots];
  roots.forEach((r) => depth.set(r, 0));
  while (queue.length) {
    const u = queue.shift();
    for (const br of adj.get(u)) {
      const v = br.a === u ? br.b : br.a;
      if (depth.has(v)) continue;
      depth.set(v, depth.get(u) + 1); children.get(u).push(v); treeEdge.add(br.id); queue.push(v);
    }
  }
  buses.filter((b) => !depth.has(b)).forEach((b) => { depth.set(b, 0); roots.push(b); });
  const row = new Map(); let next = 0;
  const place = (u) => {
    const ch = children.get(u);
    if (!ch.length) { row.set(u, next++); return; }
    ch.forEach(place);
    row.set(u, (row.get(ch[0]) + row.get(ch[ch.length - 1])) / 2);
  };
  roots.forEach(place);
  const DX = 170, DY = 70, PAD = 50;
  const pos = (b) => ({ x: PAD + depth.get(b) * DX, y: PAD + row.get(b) * DY });
  const maxD = Math.max(...depth.values());
  const W = PAD * 2 + maxD * DX + 140, H = PAD * 2 + Math.max(0, next - 1) * DY + 20;
  const vm = new Map((result?.buses || []).map((b) => [b.bus_id, b.vm_pu]));
  const br = new Map((result?.branches || []).map((b) => [b.branch_id, b]));
  const loads = new Map();
  snap.loads.forEach((l) => loads.set(l.bus, (loads.get(l.bus) || []).concat(l)));

  let svg = `<svg width="100%" style="max-width:${W}px;min-width:${Math.min(W, 560)}px" viewBox="0 0 ${W} ${H}" role="img" aria-label="Diagrama unifilar">`;
  branches.forEach((b) => {
    const p = pos(b.a), q = pos(b.b);
    const r = br.get(b.id);
    const color = !b.closed ? "var(--open)" : r ? `var(--${lClass(r.loading_percent)})` : "var(--muted)";
    const dash = !b.closed ? ' stroke-dasharray="6 5"' : "";
    const path = treeEdge.has(b.id) ? `M${p.x},${p.y} H${(p.x + q.x) / 2} V${q.y} H${q.x}` : `M${p.x},${p.y} C${p.x + 60},${p.y} ${q.x + 60},${q.y} ${q.x},${q.y}`;
    svg += `<path d="${path}" fill="none" stroke="${color}" stroke-width="${b.kind === "line" ? 3 : 2}"${dash}><title>${esc(b.id)}${r ? ` · ${fmt(r.i_ka * 1000, 1)} A · ${fmt(r.loading_percent, 1)} %` : ""}${b.closed ? "" : " · abierto"}</title></path>`;
    const mx = (p.x + q.x) / 2 + 6, my = (treeEdge.has(b.id) ? (p.y + q.y) / 2 : (p.y + q.y) / 2) - 4;
    const label = r && r.loading_percent !== null ? `${esc(b.id)} ${fmt(r.loading_percent, 0)}%` : esc(b.id);
    svg += `<text x="${mx}" y="${my}" class="sub">${label}</text>`;
    if (b.kind === "switch") svg += `<rect x="${(p.x + q.x) / 2 - 5}" y="${q.y - 5}" width="10" height="10" fill="${b.closed ? color : "var(--panel)"}" stroke="${color}"/>`;
  });
  buses.forEach((b) => {
    const { x, y } = pos(b);
    const v = vm.get(b);
    const deenergized = result && v === undefined;
    const color = deenergized ? "var(--open)" : v === undefined ? "var(--ink)" : `var(--${vClass(v)})`;
    const slack = roots.includes(b) && snap.slacks.some((s) => s.bus === b);
    svg += `<line x1="${x}" y1="${y - 16}" x2="${x}" y2="${y + 16}" stroke="${color}" stroke-width="6" stroke-linecap="round"><title>${esc(b)}${v !== undefined ? ` · ${fmt(v)} pu` : ""}</title></line>`;
    if (slack) svg += `<circle cx="${x - 26}" cy="${y}" r="11" fill="none" stroke="var(--accent)" stroke-width="2"/><text x="${x - 31}" y="${y + 4}">~</text>`;
    svg += `<text x="${x + 8}" y="${y - 20}">${esc(b)}</text>`;
    if (v !== undefined || deenergized) svg += `<text x="${x - 8}" y="${y + 30}" text-anchor="end" class="sub">${deenergized ? "sin tensión" : fmt(v, 4) + " pu"}</text>`;
    (loads.get(b) || []).forEach((l, i) => {
      const ly = y + 4 + i * 12;
      svg += `<path d="M${x},${ly} h18 l-5,-4 m5,4 l-5,4" stroke="var(--muted)" fill="none"/><text x="${x + 22}" y="${ly + 4}" class="sub">${esc(l.load_id)} ${fmt(l.p_mw, 2)} MW</text>`;
    });
  });
  $("#diagram").innerHTML = svg + "</svg>";
}

// ---------- rendering of results ----------
function cards(items) {
  return `<div class="cards">${items.map(([k, v, cls = ""]) => `<div class="card"><div class="k">${k}</div><div class="v ${cls}">${v}</div></div>`).join("")}</div>`;
}
function resultTables(res) {
  const buses = res.buses.map((b) => `<tr><td>${esc(b.bus_id)}</td><td class="c-${vClass(b.vm_pu)}">${fmt(b.vm_pu, 5)}</td><td>${fmt(b.va_deg, 3)}</td></tr>`).join("");
  const branches = res.branches.map((b) => `<tr><td>${esc(b.branch_id)}</td><td>${esc(b.from_bus)} → ${esc(b.to_bus)}</td><td>${fmt(b.i_ka * 1000, 2)}</td><td class="c-${lClass(b.loading_percent)}">${fmt(b.loading_percent, 1)}</td><td>${fmt(b.p_from_mw, 4)}</td><td>${fmt(b.p_loss_mw * 1000, 3)}</td></tr>`).join("");
  return `<div class="table-wrap"><table><thead><tr><th>Barra</th><th>V (pu)</th><th>Ángulo (°)</th></tr></thead><tbody>${buses}</tbody></table></div>
    <div class="table-wrap"><table><thead><tr><th>Rama</th><th>Tramo</th><th>I (A)</th><th>Carga (%)</th><th>P envío (MW)</th><th>Pérdidas (kW)</th></tr></thead><tbody>${branches}</tbody></table></div>`;
}
function summaryCards(res, job) {
  const minV = Math.min(...res.buses.map((b) => b.vm_pu));
  const maxL = Math.max(0, ...res.branches.map((b) => b.loading_percent ?? 0));
  return cards([
    ["Estado", esc(res.status), res.status === "computed" ? "c-ok" : "c-bad"],
    ["Contraste pandapower", esc(job.comparison ?? "—"), job.comparison === "passed" ? "c-ok" : "c-warn"],
    ["V mínima (pu)", fmt(minV, 4), "c-" + vClass(minV)],
    ["Carga máxima (%)", fmt(maxL, 1), "c-" + lClass(maxL)],
    ["Pérdidas (kW)", fmt(res.total_loss_p_mw * 1000, 2)],
    ["Slack P (MW)", fmt(res.slack_p_mw, 4)],
    ["Iteraciones", res.iterations],
    ["Balance (MVA)", Number(res.balance_mismatch_mva).toExponential(1)],
  ]);
}

async function runJob(path, body, out) {
  out.innerHTML = '<p class="muted">Ejecutando…</p>';
  const job = await waitJob(await api(path, { method: "POST", body }));
  if (job.status === "failed") throw new Error(job.error);
  return job;
}

// ---------- actions ----------
async function selectSnapshot(sha) {
  const data = await api(`/snapshots/${sha}`);
  state.snapshot = data.snapshot; state.sha = sha;
  $("#snap-id").textContent = `snapshot ${sha.slice(0, 16)}…`;
  drawDiagram(state.snapshot, null);
  const busOpts = state.snapshot.buses.map((b) => `<option>${esc(b.bus_id)}</option>`).join("");
  $("#nl-bus").innerHTML = busOpts;
  $("#alt-line").innerHTML = state.snapshot.lines.map((l) => `<option>${esc(l.line_id)}</option>`).join("");
  document.querySelectorAll("#run-flow, #newload-form button, #alt-form button").forEach((b) => (b.disabled = false));
  ["#flow-out", "#newload-out", "#alt-out"].forEach((s) => ($(s).innerHTML = ""));
  await refreshSnapshots();
}

async function refreshSnapshots() {
  const list = await api("/snapshots");
  $("#snapshots").innerHTML = list.length ? list.map((s) => `<li data-sha="${s.snapshot_sha256}" class="${s.snapshot_sha256 === state.sha ? "active" : ""}" title="${s.snapshot_sha256}">${esc(s.name || "(escenario)")} <span class="mono muted">${s.snapshot_sha256.slice(0, 8)}</span></li>`).join("") : '<li class="muted">Ninguno todavía</li>';
}

async function importPending() {
  const msg = $("#import-msg");
  try {
    const r = await api("/snapshots", { method: "POST", body: state.pending });
    setMsg(msg, `Importado (${r.state}).`, "okm");
    await selectSnapshot(r.snapshot_sha256);
  } catch (e) { setMsg(msg, "Rechazado: " + e.message, "err"); }
}

async function runFlow() {
  const out = $("#flow-out");
  try {
    const job = await runJob("/studies", { snapshot_sha256: state.sha }, out);
    const res = await api(`/results/${job.result_sha256[0]}`);
    drawDiagram(state.snapshot, res);
    out.innerHTML = summaryCards(res, job) + (res.messages?.length ? `<p class="muted">${res.messages.map(esc).join("<br>")}</p>` : "") + resultTables(res);
  } catch (e) { out.innerHTML = `<p class="msg err">${esc(e.message)}</p>`; }
}

async function runNewLoad(ev) {
  ev.preventDefault();
  const f = new FormData(ev.target), out = $("#newload-out");
  try {
    const body = { snapshot_sha256: state.sha, scenario_id: "new-load", load_id: f.get("load_id"), bus: f.get("bus"), p_mw: Number(f.get("p_mw")), q_mvar: Number(f.get("q_mvar")) };
    const job = await runJob("/studies/new-load", body, out);
    const res = await api(`/results/${job.result_sha256[0]}`);
    const scen = await api(`/snapshots/${job.scenario_snapshot_sha256}`);
    drawDiagram(scen.snapshot, res);
    const issues = [];
    res.buses.filter((b) => b.vm_pu < 0.95).forEach((b) => issues.push(`${b.bus_id}: ${fmt(b.vm_pu)} pu < 0.95`));
    res.branches.filter((b) => (b.loading_percent ?? 0) > 100).forEach((b) => issues.push(`${b.branch_id}: ${fmt(b.loading_percent, 1)} % > 100 %`));
    const verdict = res.status !== "computed" ? `<div class="violations">No calculado: ${esc((res.messages || []).join("; "))}</div>`
      : issues.length ? `<div class="violations"><strong>Violaciones detectadas</strong><br>${issues.map(esc).join("<br>")}</div>`
      : '<div class="clean">Sin violaciones detectadas con V ≥ 0.95 pu y carga ≤ 100 %. Requiere revisión humana.</div>';
    out.innerHTML = verdict + summaryCards(res, job) + resultTables(res);
  } catch (e) { out.innerHTML = `<p class="msg err">${esc(e.message)}</p>`; }
}

async function runAlternatives(ev) {
  ev.preventDefault();
  const f = new FormData(ev.target), out = $("#alt-out");
  try {
    const body = { snapshot_sha256: state.sha, scenario_id: "alternatives", line_id: f.get("line_id"), catalog_id: f.get("catalog_id"), economic_basis: JSON.parse(f.get("economic_basis")) };
    ["operating_temperature_c", "phase_gmd_m", "v_min_pu", "max_loading_percent"].forEach((k) => (body[k] = Number(f.get(k))));
    const job = await runJob("/studies/conductor-alternatives", body, out);
    const rep = job.report, cur = rep.economic_basis.currency;
    const npv = new Map(rep.ranking.map((r) => [r.alternative_id, r.npv_total_cost]));
    const rows = rep.alternatives.map((a) => {
      const s = a.screen;
      return `<tr class="${a.id === rep.recommended ? "best" : ""}"><td>${esc(a.id)}</td><td>${s.section_mm2}</td><td>${fmt(s.r_ohm_km, 4)}</td><td>${fmt(s.min_vm_pu, 4)}</td><td class="c-${lClass(s.line_loading_percent)}">${fmt(s.line_loading_percent, 1)}</td><td>${fmt((s.loss_p_mw ?? 0) * 1000, 2)}</td><td class="${a.technical_feasible ? "c-ok" : "c-bad"}">${a.technical_feasible ? "sí" : "no"}</td><td>${esc(a.independent_check)}</td><td>${a.npv_capex === undefined ? "—" : fmt(a.npv_capex, 0)}</td><td>${npv.has(a.id) ? fmt(npv.get(a.id), 0) : esc(a.unpriced_reason ?? "—")}</td></tr>`;
    }).join("");
    out.innerHTML = cards([
      ["Recomendada (mín. VPN)", esc(rep.recommended ?? "ninguna"), rep.recommended ? "c-ok" : "c-bad"],
      ["Menor sección factible", esc(rep.smallest_feasible_section ?? "ninguna")],
      ["Tasa / horizonte", `${fmt(rep.economic_basis.discount_rate * 100, 1)} % · ${rep.economic_basis.horizon_years} a`],
      ["Estado", "requiere revisión humana", "c-warn"],
    ]) + `<div class="table-wrap"><table><thead><tr><th>Conductor</th><th>mm²</th><th>R (Ω/km)</th><th>V mín</th><th>Carga línea (%)</th><th>Pérdidas red (kW)</th><th>Factible</th><th>Contraste</th><th>CAPEX (${esc(cur)})</th><th>VPN total (${esc(cur)})</th></tr></thead><tbody>${rows}</tbody></table></div>
      <p class="hint">Fuente de costos: ${esc(rep.economic_basis.source)}</p>`;
  } catch (e) { out.innerHTML = `<p class="msg err">${esc(e.message)}</p>`; }
}

// ---------- bootstrap ----------
async function init() {
  try {
    const h = await api("/health");
    $("#health").textContent = `API ${h.version} · solo local`; $("#health").className = "badge ok";
  } catch { $("#health").textContent = "API no disponible"; $("#health").className = "badge bad"; return; }
  const examples = await api("/examples");
  $("#example").innerHTML = examples.map((e) => `<option>${esc(e)}</option>`).join("");
  const cats = await api("/catalogs/conductors");
  $("#alt-catalog").innerHTML = cats.map((c) => `<option value="${esc(c.catalog_id)}">${esc(c.name)}</option>`).join("");
  state.basisExample = await api("/economic-basis/example");
  $("#alt-basis").value = JSON.stringify(state.basisExample, null, 2);
  await refreshSnapshots();

  $("#load-example").onclick = async () => {
    state.pending = await api(`/examples/${encodeURIComponent($("#example").value)}`);
    await importPending();
  };
  $("#file").onchange = async (ev) => {
    const file = ev.target.files[0];
    if (!file) return;
    try { state.pending = JSON.parse(await file.text()); $("#import").disabled = false; setMsg($("#import-msg"), `${file.name} listo para importar.`); }
    catch (e) { setMsg($("#import-msg"), "JSON inválido: " + e.message, "err"); }
  };
  $("#import").onclick = importPending;
  $("#snapshots").onclick = (ev) => { const li = ev.target.closest("li[data-sha]"); if (li) selectSnapshot(li.dataset.sha); };
  $("#run-flow").onclick = runFlow;
  $("#newload-form").onsubmit = runNewLoad;
  $("#alt-form").onsubmit = runAlternatives;
  document.querySelectorAll(".tabs button").forEach((b) => (b.onclick = () => {
    document.querySelectorAll(".tabs button").forEach((x) => x.setAttribute("aria-selected", String(x === b)));
    document.querySelectorAll(".tab").forEach((t) => (t.hidden = t.id !== "tab-" + b.dataset.tab));
  }));
}
init();
