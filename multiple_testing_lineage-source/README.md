# The false-discovery lineage — a working proof, including an honest "no"

Two papers on the multiple-testing problem, cited into each other as a live function call — plus a third, equally real citation that deliberately does **not** become one. This folder is the working code; [`docs/multiple-testing-lineage/index.html`](../docs/multiple-testing-lineage/index.html) is the same thing running zero-install in a browser, titled **"How Many of These Discoveries Are Real?"**, with a plain-language walkthrough, a full glossary, and a dedicated section explaining the honest-negative case.

Run: `python3 run_demo.py`

The sibling demonstration — the bootstrap lineage (Efron 1979 → Efron & Tibshirani 1993 → Davison & Hinkley 1997) — lives in `../resampling_knot/`. Both are linked from the project landing page, `docs/index.html`.

## The problem both real papers here are answering

Run one statistical test, and a "significant" result at the usual 5% threshold means there's a 1-in-20 chance it's a fluke. Run twenty tests at once — common in genomics, neuroimaging, any large screening study — and by chance alone, roughly one of them will look significant even if **nothing real is happening anywhere**. This is the multiple-testing problem, and it's a real, well-documented source of false "discoveries" in published science.

## Benjamini & Hochberg (1995) — the base case

Their procedure controls the **false discovery rate**: of everything you call significant, what fraction is expected to be a false alarm. Sort your p-values, find the largest one that's still below a sliding threshold, and call everything up to that point significant. It's a real, still-standard, widely-taught procedure — implemented here exactly as published, in `functions/benjamini_hochberg_1995.py`.

## Storey (2002) — a different approach, and a real, checkable citation

Storey's q-value method takes a different angle: instead of a sliding threshold, it first estimates **π₀**, the proportion of tests where nothing real is actually happening, then uses that estimate to make less conservative calls than BH's method does. But Storey's implementation here doesn't just cite BH's 1995 result in prose — it **calls it directly**, as a comparison baseline, via `registry.invoke(BH_FN_CID, ...)` in `functions/storey_2002_qvalue.py`. The demo asserts that this cited baseline number matches Benjamini & Hochberg's own direct-call result on the same data, exactly — proof that it's a real invocation, not a coincidentally similar reimplementation sitting next to it.

## Benjamini & Yekutieli (2001) — a real citation, deliberately not wired up, and why

This paper proves that FDR control still holds even when your tests are correlated rather than independent — a real, commonly cited follow-up to the 1995 paper. It is **not** implemented as a callable function here, on purpose. Run it through the invocability rubric and it fails the intent gate cleanly: a paper citing B&Y (2001) is invoking a mathematical *proof* about a procedure's properties, not running a function on data. Delete the citation, and the paper's own reported numbers don't change at all — only its *argument* for why those numbers can be trusted under correlated tests loses its support. That's the dividing line this whole prototype runs on, stated honestly rather than smoothed over: a citation becomes live code only when deleting it would change a computed result. `citation_records.py` encodes this verdict explicitly, with the reasoning printed as part of the demo's own output — not silently omitted.

## What this actually proves, structurally

- `functions/benjamini_hochberg_1995.py` — Benjamini & Hochberg (1995), "Controlling the False Discovery Rate."
- `functions/storey_2002_qvalue.py` — Storey (2002), "A Direct Approach to False Discovery Rates." **Cites the 1995 code by invoking it through `registry.invoke(fn_cid, ...)`**, with an assertion that the cited baseline matches the source's own direct output.
- `citation_records.py` — the rubric applied, in writing, to all three citations in this lineage, including the one that fails on purpose.

**As of the v0.3 schema update**, the real citation (Storey → BH) is a structured `Edge`: `edge_type="cito:usesMethodIn"`, `tier=0`, `proof_method="executable_invocation"`, `confidence="verified"` — same schema as the bootstrap lineage, same CiTO vocabulary, declared in `functions/storey_2002_qvalue.py`'s `_declare_edges()`.

## What's honestly still missing before this is the real thing

- **Pydantic vs. dataclasses:** native version here uses `@dataclass` + `__post_init__` validation, matching the contract shape but not yet upgraded to `BaseModel`/`field_validator` the way the bootstrap lineage has been.
- **Native Python vs. Pyodide:** this folder proves the mechanism; `docs/multiple-testing-lineage/index.html` proves the browser-native portability claim, running the same logic compiled to WASM.
- **`fn_cid` values are literal strings, not real content hashes** — same caveat as the bootstrap lineage.
- **Only one real edge here (Tier 0).** Benjamini & Yekutieli sits outside the tier system entirely by design — it's not a lower tier, it's correctly not a citation-as-invocation candidate at all.

## Rubric application

Storey citing Benjamini & Hochberg passes Stage 1 (E1: genuine Method/Uses — deleting the citation removes a real, reported number from Storey's own output, not just an argument; E2: stdlib-only pi0 estimator and monotone q-value construction, no exotic dependencies) at Q1=2/Q2=2. Benjamini & Yekutieli fails E1 cleanly and is reported as such — see `citation_records.py` for the full verdict table and reasoning, and `verification_ontology_v0.3_synthesis.md` Part 4 for how this maps onto the broader 0–5 proof-obligation tier system.