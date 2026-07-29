// bootstrap_widget.js
// A real MyST {anywidget} module -- renders as a first-class AST node,
// Shadow-DOM isolated, native to the document (not raw HTML, not an iframe).
//
// Design choice, stated plainly: this widget does NOT rely on MyST wiring
// it to a live thebe-lite/Jupyter kernel for two-way data binding -- that
// integration is still maturing (MyST is listed as only a "potential"
// anywidget host as of the most recent source found). Instead the widget
// loads and runs its own Pyodide instance inside render(), reusing the
// exact, already-verified bootstrap code from the resampling lineage.
// This trades the "canonical" anywidget pattern for a much higher-
// confidence build: everything inside render() is code that has already
// been proven to work, four times over, in this project.
//
// model.get('default_data') reads the JSON "props" body passed in the
// MyST directive -- this IS real, confirmed data flow from the document
// into the widget, per mystmd's own {anywidget} directive spec.

const PY_SOURCE = `
import random, math, json
def bootstrap_se(data, n_resamples=5000, seed=1):
    rng = random.Random(seed); n = len(data)
    pe = sum(data)/n
    means = [sum(data[rng.randrange(n)] for _ in range(n))/n for _ in range(n_resamples)]
    m = sum(means)/len(means)
    var = sum((x-m)**2 for x in means)/(len(means)-1)
    return pe, math.sqrt(var)

def run(data):
    pe, se = bootstrap_se(data)
    return json.dumps({"point_estimate": pe, "se": se})
`;

function render({ model, el }) {
  console.log('[anywidget] render() called');

  let defaultData;
  try {
    defaultData = model.get('default_data') || '12.1, 14.3, 11.8, 15.9, 13.2, 10.7, 16.4, 12.9, 14.8, 11.2, 13.6, 15.1';
    console.log('[anywidget] model.get("default_data") ->', defaultData);
  } catch (err) {
    console.warn('[anywidget] model.get() failed, using fallback default data:', err);
    defaultData = '12.1, 14.3, 11.8, 15.9, 13.2, 10.7, 16.4, 12.9, 14.8, 11.2, 13.6, 15.1';
  }

  el.innerHTML = `
    <div style="font-family: 'JetBrains Mono', monospace; border: 1px solid #d8d3c6; border-radius: 6px; padding: 18px; background: #fff;">
      <div style="font-size: 11px; color: #b8791f; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px;">
        Live citation — native MyST widget, not raw HTML, not an iframe
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
        const nums = dataEl.value.split(',').map(s => parseFloat(s.trim())).filter(n => !isNaN(n));
        pyodide.globals.set('data_list', pyodide.toPy(nums));
        const r = JSON.parse(pyodide.runPython('run(data_list)'));
        console.log('[anywidget] computation result:', r);
        outEl.style.display = 'block';
        outEl.textContent = `point_estimate=${r.point_estimate.toFixed(4)}  se=${r.se.toFixed(4)}\n\nComputed just now, in this widget, native to the MyST document.`;

        // Optional: sync the result back into the widget model, for a future
        // host page that might want to read it out. Wrapped defensively --
        // MyST's current anywidget host throws "MystAnyModel.save_changes
        // not implemented yet" (confirmed live, 2026-07-29), so this must
        // never be allowed to break the widget the computation already
        // succeeded on. Logged either way so the state is never silent.
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
