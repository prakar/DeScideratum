// bh_storey_widget.js
//
// A real MyST {anywidget} module, same pattern as the resampling vignette's
// widgets/bootstrap_widget.js: loads its own Pyodide instance inside
// render(), doesn't depend on MyST's live-kernel wiring, defensively wraps
// model.save_changes() (unimplemented in MyST's current anywidget host as
// of 2026-07-29 -- see the resampling vignette's plugin for the confirming
// console evidence).
//
// The Python below is copied verbatim from docs/multiple-testing-lineage/
// index.html's already-verified PY_SOURCE, not rewritten -- same
// discipline as the first vignette: reuse proven code, don't re-derive it.

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
        self._edges.append({
            "depth": depth, "source": source_fn_cid, "target": cid,
            "edge_type": meta.get("edge_type", "unknown"),
            "tier": meta.get("tier", -1),
        })
        return self._fns[cid](payload, depth)
    def edges(self):
        return list(self._edges)

REGISTRY = Registry()
A_CID = "bafy_benjamini_hochberg_1995_bh_v1"
B_CID = "bafy_storey_2002_qvalue_v1"

def bh_adjust(payload, depth=0):
    pvalues = payload["pvalues"]; alpha = payload.get("alpha", 0.05)
    m = len(pvalues)
    indexed = sorted(range(m), key=lambda i: pvalues[i])
    sorted_p = [pvalues[i] for i in indexed]
    adjusted_sorted = [0.0]*m
    adjusted_sorted[m-1] = sorted_p[m-1]
    for k in range(m-2, -1, -1):
        candidate = sorted_p[k]*m/(k+1)
        adjusted_sorted[k] = min(candidate, adjusted_sorted[k+1])
        adjusted_sorted[k] = min(adjusted_sorted[k], 1.0)
    largest_k = -1
    for k in range(m):
        if sorted_p[k] <= (k+1)/m*alpha:
            largest_k = k
    rejected_sorted = [i <= largest_k for i in range(m)]
    rejected = [False]*m; adjusted = [0.0]*m
    for pos, orig_i in enumerate(indexed):
        rejected[orig_i] = rejected_sorted[pos]
        adjusted[orig_i] = adjusted_sorted[pos]
    return {"rejected": rejected, "adjusted_pvalues": adjusted, "n_significant": sum(rejected)}

def storey_qvalues(payload, depth=1):
    pvalues = payload["pvalues"]; lam = payload.get("lambda_fixed", 0.9)
    alpha_baseline = payload.get("alpha_for_baseline", 0.05)
    m = len(pvalues)
    bh_baseline = REGISTRY.invoke(A_CID, {"pvalues": pvalues, "alpha": alpha_baseline}, depth=depth+1, source_fn_cid=B_CID)
    n_above = sum(1 for p in pvalues if p > lam)
    pi0_hat = min(1.0, n_above/(m*(1-lam)))
    indexed = sorted(range(m), key=lambda i: pvalues[i])
    sorted_p = [pvalues[i] for i in indexed]
    q_sorted = [0.0]*m
    q_sorted[m-1] = min(pi0_hat*sorted_p[m-1], 1.0)
    for k in range(m-2, -1, -1):
        candidate = pi0_hat*m*sorted_p[k]/(k+1)
        q_sorted[k] = min(candidate, q_sorted[k+1])
        q_sorted[k] = min(q_sorted[k], 1.0)
    qvalues = [0.0]*m
    for pos, orig_i in enumerate(indexed):
        qvalues[orig_i] = q_sorted[pos]
    return {"qvalues": qvalues, "pi0_hat": pi0_hat,
            "naive_bh_n_significant": bh_baseline["n_significant"],
            "naive_bh_rejected": bh_baseline["rejected"]}

REGISTRY.register(A_CID, bh_adjust)
REGISTRY.register(B_CID, storey_qvalues)
REGISTRY.register_cites(B_CID, {A_CID: {"edge_type": "cito:usesMethodIn", "tier": 0}})

def run_chain(pvalues_list):
    a = REGISTRY.invoke(A_CID, {"pvalues": pvalues_list, "alpha": 0.05})
    b = storey_qvalues({"pvalues": pvalues_list, "lambda_fixed": 0.9}, depth=0)
    from collections import Counter
    counts = Counter((e["depth"], e["edge_type"], e["tier"], e["target"]) for e in REGISTRY.edges())
    log_lines = [f"depth={d}  {et}  tier={t}  -> {tgt}  ({n}x)" for (d,et,t,tgt), n in sorted(counts.items())]
    return json.dumps({"a": a, "b": b, "log": log_lines, "total": len(REGISTRY.edges())})
`;

function render({ model, el }) {
  console.log('[anywidget] render() called');

  let defaultData;
  try {
    defaultData = model.get('default_data') || '0.0001, 0.0004, 0.0012, 0.008, 0.011, 0.019, 0.021, 0.033, 0.041, 0.052, 0.078, 0.11, 0.14, 0.19, 0.24, 0.31, 0.42, 0.55, 0.71, 0.93';
    console.log('[anywidget] model.get("default_data") ->', defaultData);
  } catch (err) {
    console.warn('[anywidget] model.get() failed, using fallback default data:', err);
    defaultData = '0.0001, 0.0004, 0.0012, 0.008, 0.011, 0.019, 0.021, 0.033, 0.041, 0.052, 0.078, 0.11, 0.14, 0.19, 0.24, 0.31, 0.42, 0.55, 0.71, 0.93';
  }

  el.innerHTML = `
    <div style="font-family: 'JetBrains Mono', monospace; border: 1px solid #d8d3c6; border-radius: 6px; padding: 18px; background: #fff;">
      <div style="font-size: 11px; color: #b8791f; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px;">
        Live citation — native MyST widget
      </div>
      <textarea class="aw-data" rows="2" style="width:100%; font-family: inherit; font-size: 13px; padding: 8px; border: 1px solid #d8d3c6; border-radius: 3px; box-sizing: border-box;">${defaultData}</textarea>
      <div style="margin-top: 10px;">
        <button class="aw-run" disabled style="font-family: inherit; font-size: 13px; font-weight: 600; background: #1c2430; color: #f7f5f0; border: none; padding: 8px 16px; border-radius: 3px; cursor: pointer;">Loading Python runtime…</button>
        <span class="aw-status" style="font-size: 12px; color: #4a5468; margin-left: 10px;">fetching Pyodide</span>
      </div>
      <pre class="aw-output" style="margin-top: 12px; font-size: 12.5px; background: #1c2430; color: #f0e2c8; padding: 12px; border-radius: 4px; display: none; white-space: pre-wrap;"></pre>
    </div>
  `;

  const statusEl = el.querySelector('.aw-status');
  const btn = el.querySelector('.aw-run');
  const dataEl = el.querySelector('.aw-data');
  const outEl = el.querySelector('.aw-output');

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
        const pvals = dataEl.value.split(',').map(s => parseFloat(s.trim())).filter(n => !isNaN(n) && n >= 0 && n <= 1);
        pyodide.globals.set('pvals_list', pyodide.toPy(pvals));
        const r = JSON.parse(pyodide.runPython('run_chain(pvals_list)'));
        console.log('[anywidget] computation result:', r);
        outEl.style.display = 'block';
        outEl.textContent =
          `A · Benjamini & Hochberg: n_significant=${r.a.n_significant} / ${pvals.length}\n` +
          `B · Storey (cites A): π₀=${r.b.pi0_hat.toFixed(4)}  naive_bh_n_significant=${r.b.naive_bh_n_significant}\n\n` +
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
