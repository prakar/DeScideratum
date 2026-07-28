# Citation Invocability Rubric v0.1
### A scoring instrument for whether a given citation can be a "browser-invocable citation" — deliberately sized to be applied by one researcher, to one paper, in an afternoon, not maintained as infrastructure.

**Provenance, so every clause is traceable to something real rather than asserted:** this rubric formalizes the four conditions established in this conversation, which were themselves built by triangulating three existing lineages — citation-intent classification (SciCite/ACL-ARC), the Explorable Explanations line (Victor 2011 → Dragicevic et al., CHI 2019 Best Paper → Hinsen, 2025), and the runtime constraints of browser-native WASM execution (Pyodide). Nothing here is invented from a blank page.

---

## Design decision: two stages, not one flat score

Eligibility and quality are different questions and get conflated by a single score. A citation can be a *perfect* candidate for invocation (right intent, technically executable) but rendered with a bad, opaque widget — or a *poor* candidate (wrong intent) implemented beautifully. **Stage 1 is a gate: fail either clause and the citation is not browser-invocable, full stop, no partial credit.** Stage 2 only runs on citations that clear Stage 1, and scores how good the resulting reader experience is.

---

## Stage 1 — Eligibility (binary; both must pass)

### E1. Intent Gate — is this citation Method/Uses-shaped?

A citation passes E1 iff the citing paper is applying the cited paper's procedure to the citing paper's own data/problem, and the procedure's output feeds the citing paper's own downstream claim — not merely situating, motivating, or comparing against the cited work.

Decision procedure:
1. Locate the specific sentence(s) doing the citing.
2. Ask: if this citation were deleted, would the citing paper's own reported numbers change? (If yes → likely E1-pass. If the paper's argument survives untouched → likely E1-fail, it was Background/Motivation.)
3. Ask: does the citing paper report a result that is *the cited procedure's output*, not just a reference to the cited procedure's *existence*? (E1-pass requires yes.)
4. Explicitly check for the two failure patterns from prior analysis: **Background** ("prior work has explored X using method M") and **Critique/Extends** ("we show M's assumption fails under condition C") both fail E1 — the second is not a lesser case of the first, it is citing the cited work's *properties*, not its output.

### E2. Portability Gate — is this technically executable client-side, honestly?

A citation passes E2 iff the cited procedure, as actually implemented, satisfies every clause below — not "could probably be made to," but does, checked against the actual Pyodide package index and actual constraint profile established earlier in this project:

- `compute_class: cpu_only` — no GPU/CUDA dependency anywhere in the call path.
- No `threading`/`multiprocessing`/unpatched `joblib` parallelism in the implementation.
- Every import resolves against the current WASM-compiled package set or is pure-Python (checked, not assumed — a package "probably being fine" is a fail until verified).
- A `memory_hint_mb` can be honestly declared for realistic input sizes the citing community actually uses (not just the toy example in the original paper) — if the field's typical dataset size is known to blow past a single-tab memory budget (see: t-SNE on real single-cell data), this clause fails even though the *algorithm* is otherwise portable, and that failure must be recorded, not hidden.
- The function can be served from a CORS-enabled origin (an engineering fact about the hosting plan, not the algorithm, but still a hard gate — an uncitable-in-practice function is not invocable regardless of how clean the math is).

**A citation that fails either E1 or E2 is not scored further. It remains a conventional prose citation, correctly, and that outcome should be stated explicitly wherever the rubric is applied — the rubric's job includes producing honest negatives, not just finding wins.**

---

## Stage 2 — Quality (0–2 per dimension, run only on E1+E2 passes)

### Q1. Interaction Design (Dragicevic/EMAR standard)

| Score | Criterion |
|---|---|
| 0 | Reader must interact to get any value; no sensible default rendering |
| 1 | Renders sensibly as static prose by default, but parameter exploration is clunky, unbounded, or unguided |
| 2 | Readable as normal prose without interacting (EMAR's own stated bar — "the reader is not forced to interact in order to learn"), *and* rewards active engagement with a bounded, guided, non-destructive re-derivation |

### Q2. Execution Transparency (Hinsen's correction to Victor)

| Score | Criterion |
|---|---|
| 0 | Output only; implementation is a black box the reader must trust |
| 1 | Source is available via a link or separate repo, but not inline/inspectable at the point of use |
| 2 | The exact code producing the displayed result is inline-inspectable at the moment of use — not a simplified explainer standing in for the real computation (Hinsen's specific complaint about Victor's own examples) |

**Reporting convention:** state the Stage 1 result first (pass/fail on E1, pass/fail on E2, with the specific reason for any fail), then the Stage 2 scores only if both gates passed. A citation that's "E1 pass, E2 fail (memory)" is a materially different, more useful finding than a flat "not invocable" — it tells you exactly what would need to change (a smaller reference dataset default, a declared size warning) rather than discarding the citation as hopeless.

---

## Worked examples (dogfooding the instrument before trusting it)

**Example A — Benjamini & Hochberg (1995) cited by a genomics paper applying BH correction to its own p-value vector.**
- E1: **Pass.** Deleting the citation changes the paper's own reported significance calls.
- E2: **Pass.** Pure arithmetic/sorting, no GPU, no threading, trivial memory footprint at any realistic input size, pure-Python implementable.
- Q1: **2.** Renders as a normal results sentence ("N genes significant at FDR<0.05") by default; a reader can substitute their own p-value vector and watch the call list update.
- Q2: **2.** The adjustment procedure is ~15 lines; fully inline-inspectable, no simplification needed.
- **Result: browser-invocable, high quality (Stage 2: 4/4).**

**Example B — Benjamini & Yekutieli (2001) cited by a paper arguing BH's independence assumption doesn't hold in their data.**
- E1: **Fail.** The citation is to B&Y's *proof* that FDR control extends to positive dependence — the citing paper is engaging with a mathematical property, not running a function on data. Deleting the citation would change the paper's *argument*, not its *reported numbers* — this is the diagnostic that separates Method/Uses from Critique/Extends.
- **Result: not browser-invocable. Correctly remains a conventional citation.** This is the rubric working as intended, not a limitation of it.

**Example C — a hypothetical citation applying t-SNE to a real 50,000-cell single-cell RNA-seq matrix, using the field's actual typical dataset size.**
- E1: **Pass.** Genuine Method/Uses citation.
- E2: **Fail — memory clause specifically.** The algorithm is portable in principle (numpy/sklearn-compatible), but the *realistic* input size for this citing community exceeds a safe single-tab memory budget. Note the failure is scoped: this is not "t-SNE is uninvocable," it's "t-SNE is uninvocable *at this community's typical scale* without a declared size ceiling and a smaller default demo dataset."
- **Result: not currently browser-invocable as cited; conditionally invocable if the demo defaults to a bounded subsample and warns above it.** This is exactly the finding from two turns ago, now produced by the instrument rather than by ad hoc discussion — which is the actual test of whether the rubric is doing real work.

---

*v0.1 — expect revision once run against the resampling knot's actual implementation and the physics knot's boundary case.*
