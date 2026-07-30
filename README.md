# DeScideratum

A research prototype exploring a different way to cite scientific work: instead of a citation being a name and a year you have to trust, a citation can be a live function call — verifiable, runnable, and checkable by anyone, on their own data, with nothing installed.

**Start here:** [`docs/index.html`](docs/index.html) — the live demo hub, three working demonstrations, zero-install, runs entirely in your browser.

## What's live right now

| Lineage | Live demo | Source + methodology |
|---|---|---|
| **How Much Should You Trust an Average?** — Efron (1979) → Efron & Tibshirani (1993) → Davison & Hinkley (1997) | [`docs/resampling-lineage/index.html`](docs/resampling-lineage/index.html) | [`resampling_lineage-source/README.md`](resampling_lineage-source/README.md) |
| **How Many of These Discoveries Are Real?** — Benjamini & Hochberg (1995) → Storey (2002), plus a real citation that honestly does *not* become live code | [`docs/multiple-testing-lineage/index.html`](docs/multiple-testing-lineage/index.html) | [`multiple_testing_lineage-source/README.md`](multiple_testing_lineage-source/README.md) |
| **What Happens When You Combine Evidence?** — Cochran (1954) → DerSimonian & Laird (1986) → Higgins & Thompson (2002), the first lineage where every input carries a real Applicability Profile | [`docs/meta-analysis-lineage/index.html`](docs/meta-analysis-lineage/index.html) | [`meta_analysis_lineage-source/README.md`](meta_analysis_lineage-source/README.md) |

*(Source folder names use the `<name>_lineage-source` convention; if your repo still has earlier names like `resampling_knot`, rename to match — see project notes.)*

Each subfolder README owns the actual detail — what each paper's method computes, why the citation between them is structural rather than stylistic, what's honestly still missing, and how the invocability rubric scores it. This file only orients; it doesn't duplicate that content; treat the subfolder READMEs as the source of truth if anything here ever looks out of date against them.

## Authoring integration — a different kind of demonstration

The three lineages above are hand-built HTML — proof the citation-as-invocation mechanism works. [`vignette_bootstrap_lineage/`](vignette_bootstrap_lineage/README.md) is different: it proves the mechanism works **inside an independent, existing authoring tool** rather than only inside pages this project controls end to end. Live at [`docs/bootstrap-vignette/`](docs/bootstrap-vignette/).

Building this required `cite-invoke`, a MyST Markdown directive that unifies `{cite}` and `{anywidget}` into one construct — citing a method and running it become the same authoring act. Prasanna Varun Karmarkar (ORCID: [0009-0006-2284-6914](https://orcid.org/0009-0006-2284-6914)) directed the design and confirmed it working end to end via live build, with Claude (Sonnet 4.6/5, Anthropic) implementing the directive against mystmd's own source under that direction — see [`vignette_bootstrap_lineage/README.md`](vignette_bootstrap_lineage/README.md) for the full account. No prior implementation found anywhere, including NeuroLibre, unifies MyST's citation and widget systems this way. **Released, MIT-licensed, install directly** — MyST has no central plugin registry, so this URL is the actual distribution mechanism:

```yaml
project:
  plugins:
    - https://github.com/prakar/DeScideratum/releases/download/v0.2.0/cite-invoke.mjs
```

Release notes: [github.com/prakar/DeScideratum/releases/tag/v0.2.0](https://github.com/prakar/DeScideratum/releases/tag/v0.2.0)

## The theory underneath the demos

- **`citation_invocability_rubric_v0.1.md`** — the two-stage instrument (E1 intent / E2 portability gates, Q1/Q2 quality scores) used to decide whether a given citation can honestly become a live function call.
- **`verification_ontology_v0.3_synthesis.md`** — the current, broader framing: citation relationships get their type from CiTO, scholarly objects get their shape from RO-Crate/nanopublications, provenance chains come from PROV-O — and this project's actual contribution is the layer none of those provide, a proof-obligation tier (0–5) and verification method attached to each relationship.

**Terminology note, locked down and worth repeating here:** *tier* and *Applicability Profile* are two separate, independent properties of an edge, not one axis. Tier measures how hard a relationship *type* is to mechanically verify (all three demos above are Tier 0 — `cito:usesMethodIn`, invocation-log-verified). Applicability Profile measures whether the *cited content* carries validity conditions (population, measurement context, failure modes) — orthogonal to tier, and only populated with real data in the third demo so far.

*(If the two theory files above aren't already at repo root, they exist as standalone deliverables from earlier work — add them here so the links above resolve.)*

## Honest status

Three lineages built, all regression-tested (native Python, Pydantic-validated, and browser-native Pyodide versions all producing identical numbers — cross-checked against independent from-scratch reimplementations, not just internal consistency), all scored against the rubric. The second lineage deliberately includes a citation that fails the rubric on purpose, not just wins. The third exercises the Applicability Profile field with real per-study data for the first time. Still open: a genuine Tier 2 demonstration (citing a specific, hashable dataset artifact — different from anything built so far), and — flagged directly by early feedback on this project — a written justification for why these specific papers were chosen in each lineage, needed before any of this goes into a manuscript.
