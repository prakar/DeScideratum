# DeScideratum

A research prototype exploring a different way to cite scientific work: instead of a citation being a name and a year you have to trust, a citation can be a live function call — verifiable, runnable, and checkable by anyone, on their own data, with nothing installed.

**Start here:** [`docs/index.html`](docs/index.html) — the live demo hub, two working demonstrations, zero-install, runs entirely in your browser.

## What's live right now

| Lineage | Live demo | Source + methodology |
|---|---|---|
| **How Much Should You Trust an Average?** — Efron (1979) → Efron & Tibshirani (1993) → Davison & Hinkley (1997) | [`docs/resampling-lineage/index.html`](docs/resampling-lineage/index.html) | [`resampling_lineage-source/README.md`](resampling_lineage-source/README.md) |
| **How Many of These Discoveries Are Real?** — Benjamini & Hochberg (1995) → Storey (2002), plus a real citation that honestly does *not* become live code | [`docs/multiple-testing-lineage/index.html`](docs/multiple-testing-lineage/index.html) | [`multiple_testing_lineage-source/README.md`](multiple_testing_lineage-source/README.md) |

Each subfolder README owns the actual detail — what each paper's method computes, why the citation between them is structural rather than stylistic, what's honestly still missing, and how the invocability rubric scores it. This file only orients; it doesn't duplicate that content; treat the subfolder READMEs as the source of truth if anything here ever looks out of date against them.

## The theory underneath the demos

- **`citation_invocability_rubric_v0.1.md`** — the two-stage instrument (E1 intent / E2 portability gates, Q1/Q2 quality scores) used to decide whether a given citation can honestly become a live function call.
- **`verification_ontology_v0.3_synthesis.md`** — the current, broader framing: citation relationships get their type from CiTO, scholarly objects get their shape from RO-Crate/nanopublications, provenance chains come from PROV-O — and this project's actual contribution is the layer none of those provide, a proof-obligation tier (0–5) and verification method attached to each relationship. Both demos above are Tier 0.

*(If either file isn't already at repo root, they exist as standalone deliverables from earlier work — add them here so the links above resolve.)*

## Honest status

Two lineages built, both regression-tested (native Python, Pydantic-validated, and browser-native Pyodide versions all producing identical numbers), both scored against the rubric, one deliberately including a citation that fails the rubric on purpose rather than only showing wins. Everything live so far is Tier 0 (`cito:usesMethodIn` — direct method reuse). Next in the build queue: a lineage exercising Tier 2 (dataset/model citation) and the Applicability Profile (validity conditions on empirical claims) — see `verification_ontology_v0.3_synthesis.md` Part 7 for the full open-items list.