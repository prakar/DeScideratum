// meta_analysis_widget.js
//
// Same proven pattern as the other two vignettes' widgets: loads its own
// Pyodide instance inside render(), doesn't depend on MyST's live-kernel
// wiring, defensively wraps model.save_changes(). Python copied verbatim
// from the already-verified docs/meta-analysis-lineage/index.html.
//
// What's new here: props (default_data) carry a JSON array of studies,
// each with a real Applicability Profile (population, conditions,
// failure_modes) -- not just a number. The widget renders these as an
// editable table, same fields the hand-built browser page has, so the
// vignette's prose can point at specific rows and explain what they mean.

const PY_SOURCE = `
import json

class Registry:
    def __init__(self):
        self._fns = {}
        self._cites = {}
        self._edges = []
    def register(self, cid, fn):
        self._fns[cid] = fn
    def register_cites(self, source_cid, cites):
        self._cites[source_cid] = cites
    def invoke(self, cid, payload, depth=0, source_fn_cid=None):
        if depth > 3:
            raise Exception(f"exceeded depth 3 at {cid}")
        meta = {}
        if source_fn_cid and source_fn_cid in self._cites:
            meta = self._cites[source_fn_cid].get(cid, {})
        self._edges.append({"depth": depth, "source": source_fn_cid, "target": cid,
                             "edge_type": meta.get("edge_type", "unknown"), "tier": meta.get("tier", -1)})
        return self._fns[cid](payload, depth)
    def edges(self):
        return list(self._edges)

REGISTRY = Registry()
A_CID = "bafy_cochran_1954_fixed_effect_v1"
B_CID = "bafy_dersimonian_laird_1986_random_effects_v1"
C_CID = "bafy_higgins_thompson_2002_i_squared_v1"

def fixed_effect_pool(payload, depth=0):
    studies = payload["studies"]
    k = len(studies)
    weights = [1.0/(s["se"]**2) for s in studies]
    sum_w = sum(weights)
    pooled = sum(w*s["estimate"] for w,s in zip(weights, studies)) / sum_w
    pooled_se = (1.0/sum_w) ** 0.5
    Q = sum(w*(s["estimate"]-pooled)**2 for w,s in zip(weights, studies))
    return {"pooled_estimate": pooled, "pooled_se": pooled_se, "q_statistic": Q, "k": k, "weights": weights}

def random_effects_pool(payload, depth=1):
    studies = payload["studies"]
    base = REGISTRY.invoke(A_CID, {"studies": studies}, depth=depth+1, source_fn_cid=B_CID)
    weights = base["weights"]
    sum_w = sum(weights); sum_w2 = sum(w**2 for w in weights)
    c = sum_w - (sum_w2/sum_w)
    tau2 = max(0.0, (base["q_statistic"] - (base["k"]-1)) / c) if c != 0 else 0.0
    re_w = [1.0/(s["se"]**2 + tau2) for s in studies]
    sum_rw = sum(re_w)
    pooled = sum(w*s["estimate"] for w,s in zip(re_w, studies)) / sum_rw
    pooled_se = (1.0/sum_rw) ** 0.5
    return {"pooled_estimate": pooled, "pooled_se": pooled_se, "tau_squared": tau2,
            "q_statistic": base["q_statistic"], "k": base["k"]}

def heterogeneity_i2(payload, depth=0):
    studies = payload["studies"]
    base = REGISTRY.invoke(B_CID, {"studies": studies}, depth=depth+1, source_fn_cid=C_CID)
    Q = base["q_statistic"]; k = base["k"]
    i2 = max(0.0, (Q-(k-1))/Q) * 100 if Q != 0 else 0.0
    if i2 < 25: interp = "low heterogeneity -- studies broadly agree"
    elif i2 < 50: interp = "moderate heterogeneity"
    elif i2 < 75: interp = "substantial heterogeneity -- pooling should be interpreted cautiously"
    else: interp = "considerable heterogeneity -- pooling a single estimate may be misleading"
    return {"i_squared_pct": i2, "q_statistic": Q, "k": k, "interpretation": interp, "tau_squared": base["tau_squared"], "pooled_estimate": base["pooled_estimate"], "pooled_se": base["pooled_se"]}

REGISTRY.register(A_CID, fixed_effect_pool)
REGISTRY.register(B_CID, random_effects_pool)
REGISTRY.register(C_CID, heterogeneity_i2)
REGISTRY.register_cites(B_CID, {A_CID: {"edge_type": "cito:usesMethodIn", "tier": 0}})
REGISTRY.register_cites(C_CID, {B_CID: {"edge_type": "cito:usesMethodIn", "tier": 0}})

def run_chain(studies):
    a = REGISTRY.invoke(A_CID, {"studies": studies})
    b = random_effects_pool({"studies": studies}, depth=0)
    c = heterogeneity_i2({"studies": studies}, depth=0)
    from collections import Counter
    counts = Counter((e["depth"], e["edge_type"], e["tier"], e["target"]) for e in REGISTRY.edges())
    log_lines = [f"depth={d}  {et}  tier={t}  -> {tgt}  ({n}x)" for (d,et,t,tgt), n in sorted(counts.items())]
    assert b["q_statistic"] == a["q_statistic"], "Node B Q must match Node A Q exactly"
    assert c["q_statistic"] == a["q_statistic"], "Node C Q (via 2 hops) must match Node A Q exactly"
    return json.dumps({"a": a, "b": b, "c": c, "log": log_lines, "total": len(REGISTRY.edges())})
`;

function defaultStudies() {
  return [
    {label: "Study 1", estimate: 0.42, se: 0.08, population: "adults, urban clinic", conditions: "6-week follow-up", failure_modes: "high dropout in original sample"},
    {label: "Study 2", estimate: 0.35, se: 0.10, population: "adults, rural clinic", conditions: "6-week follow-up", failure_modes: ""},
    {label: "Study 3", estimate: 0.51, se: 0.09, population: "adults, mixed setting", conditions: "8-week follow-up", failure_modes: ""},
    {label: "Study 4", estimate: 0.28, se: 0.12, population: "adults, urban clinic", conditions: "4-week follow-up", failure_modes: "underpowered, wide CI"},
    {label: "Study 5", estimate: 0.45, se: 0.07, population: "adults, urban clinic", conditions: "6-week follow-up", failure_modes: ""},
  ];
}

function render({ model, el }) {
  console.log('[anywidget] render() called');

  let studies;
  try {
    const raw = model.get('default_data');
    studies = raw ? JSON.parse(raw) : defaultStudies();
    console.log('[anywidget] model.get("default_data") ->', studies);
  } catch (err) {
    console.warn('[anywidget] model.get() failed or unparsable, using fallback studies:', err);
    studies = defaultStudies();
  }

  const rowsHtml = studies.map((s, i) => `
    <tr>
      <td><input class="ma-label" data-i="${i}" value="${s.label}" style="width:70px; font-family:inherit; font-size:12px; border:1px solid #d8d3c6; border-radius:2px; padding:3px;"></td>
      <td><input class="ma-estimate" data-i="${i}" type="number" step="0.01" value="${s.estimate}" style="width:55px; font-family:inherit; font-size:12px; border:1px solid #d8d3c6; border-radius:2px; padding:3px;"></td>
      <td><input class="ma-se" data-i="${i}" type="number" step="0.01" value="${s.se}" style="width:50px; font-family:inherit; font-size:12px; border:1px solid #d8d3c6; border-radius:2px; padding:3px;"></td>
      <td><input class="ma-population" data-i="${i}" value="${s.population}" style="width:130px; font-family:inherit; font-size:12px; border:1px solid #d8d3c6; border-radius:2px; padding:3px;"></td>
      <td><input class="ma-conditions" data-i="${i}" value="${s.conditions}" style="width:110px; font-family:inherit; font-size:12px; border:1px solid #d8d3c6; border-radius:2px; padding:3px;"></td>
    </tr>
  `).join('');

  el.innerHTML = `
    <div style="font-family: 'JetBrains Mono', monospace; border: 1px solid #d8d3c6; border-radius: 6px; padding: 18px; background: #fff;">
      <div style="font-size: 11px; color: #b8791f; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px;">
        Live citation — native MyST widget · each row carries an Applicability Profile
      </div>
      <table style="width:100%; border-collapse: collapse; font-size: 11px;">
        <thead><tr style="text-align:left; color:#4a5468;">
          <th>Label</th><th>Estimate</th><th>SE</th><th>Population</th><th>Conditions</th>
        </tr></thead>
        <tbody class="ma-rows">${rowsHtml}</tbody>
      </table>
      <div style="margin-top: 10px;">
        <button class="aw-run" disabled style="font-family: inherit; font-size: 13px; font-weight: 600; background: #1c2430; color: #f7f5f0; border: none; padding: 8px 16px; border-radius: 3px; cursor: pointer;">Loading Python runtime…</button>
        <span class="aw-status" style="font-size: 12px; color: #4a5468; margin-left: 10px;">fetching Pyodide</span>
      </div>
      <pre class="aw-output" style="margin-top: 12px; font-size: 12.5px; background: #1c2430; color: #f0e2c8; padding: 12px; border-radius: 4px; display: none; white-space: pre-wrap;"></pre>
    </div>
  `;

  const statusEl = el.querySelector('.aw-status');
  const btn = el.querySelector('.aw-run');
  const outEl = el.querySelector('.aw-output');

  function readStudiesFromTable() {
    const rows = [];
    el.querySelectorAll('.ma-rows tr').forEach((tr, i) => {
      rows.push({
        label: tr.querySelector('.ma-label').value,
        estimate: parseFloat(tr.querySelector('.ma-estimate').value),
        se: parseFloat(tr.querySelector('.ma-se').value),
        population: tr.querySelector('.ma-population').value,
        conditions: tr.querySelector('.ma-conditions').value,
      });
    });
    return rows;
  }

  console.log('[anywidget] loading Pyodide inside widget render()...');

  const scriptTag = document.createElement('script');
  scriptTag.src = 'https://cdn.jsdelivr.net/pyodide/v0.26.1/full/pyodide.js';
  scriptTag.onload = async () => {
    try {
      const pyodide = await window.loadPyodide();
      pyodide.runPython(PY_SOURCE);
      console.log('[anywidget] Pyodide ready.');
      statusEl.textContent = 'ready — Python running in this tab';
      btn.disabled = false;
      btn.textContent = 'Run the live citation';
      btn.onclick = () => {
        console.log('[anywidget] run clicked');
        const currentStudies = readStudiesFromTable();
        if (currentStudies.some(s => isNaN(s.estimate) || isNaN(s.se) || s.se <= 0)) {
          alert('Every study needs a numeric estimate and a positive SE.');
          return;
        }
        pyodide.globals.set('studies_py', pyodide.toPy(currentStudies));
        const r = JSON.parse(pyodide.runPython('run_chain(studies_py)'));
        console.log('[anywidget] computation result:', r);
        outEl.style.display = 'block';
        outEl.textContent =
          `A · Cochran: pooled=${r.a.pooled_estimate.toFixed(4)}  Q=${r.a.q_statistic.toFixed(4)}\n` +
          `B · DerSimonian & Laird (cites A): τ²=${r.b.tau_squared.toFixed(4)}\n` +
          `C · Higgins & Thompson (cites B): I²=${r.c.i_squared_pct.toFixed(1)}% (${r.c.interpretation})\n\n` +
          `Computed just now, in this widget, native to the MyST document.`;

        try {
          model.set('last_result', outEl.textContent);
          model.save_changes();
          console.log('[anywidget] model.save_changes() succeeded');
        } catch (err) {
          console.warn('[anywidget] model.save_changes() not available in this host (non-fatal, computation already displayed):', err.message);
        }
      };
    } catch (err) {
      console.error('[anywidget] boot FAILED:', err);
      statusEl.textContent = 'failed to load — see browser console';
    }
  };
  scriptTag.onerror = () => {
    console.error('[anywidget] failed to fetch pyodide.js from CDN');
    statusEl.textContent = 'failed to fetch Pyodide — see browser console';
  };
  document.head.appendChild(scriptTag);
}

export default { render };
