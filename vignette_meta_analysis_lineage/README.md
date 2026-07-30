# The meta-analysis vignette — testing whether conditions travel with a number

Where the first vignette proved `cite-invoke` works inside an independent authoring tool, and the second proved a deliberately non-invocable citation reads naturally beside live ones, this one tests a third, distinct property: whether a citation's Applicability Profile — the conditions under which its number is valid — survives being stated in real prose, rather than only existing as a field in a UI table a reader could ignore.

Live page: [https://prakar.github.io/DeScideratum/meta-analysis-vignette/](https://prakar.github.io/DeScideratum/meta-analysis-vignette/) (deployed via GitHub Actions — see [`.github/workflows/deploy-pages.yml`](https://github.com/prakar/DeScideratum/blob/main/.github/workflows/deploy-pages.yml))
Source: `vignette.md`, built and served with [mystmd](https://mystmd.org)

## What's here

- **`vignette.md`** — a synthetic five-study pooling narrative, citing three real papers (Cochran 1954 → DerSimonian & Laird 1986 → Higgins & Thompson 2002) via a single `cite-invoke` call. Two specific studies' Applicability Profiles are named directly in the prose (differing follow-up duration, an unusually wide standard error) — the actual test this vignette exists to run.
- **`widgets/meta_analysis_widget.js`** — the live widget; Python copied verbatim from the already-verified `docs/meta-analysis-lineage/index.html`. Renders an editable per-study table (label, estimate, SE, population, conditions), not just a single number field.

## Status

Numerically cross-checked against the same known-good baseline as the hand-built meta-analysis lineage page (`pooled=0.4208`, `Q=3.0344`, `τ²=0.0000`, `I²=0.0%`) and the independent from-scratch numpy implementation, before this vignette shipped. Uses `cite-invoke` v0.2.0 installed from its published release.

## Acknowledgments

Prasanna Varun Karmarkar (ORCID: [0009-0006-2284-6914](https://orcid.org/0009-0006-2284-6914)) directed the design of this vignette and verified its behavior. Claude (Sonnet 4.6/5, Anthropic) analyzed the already-verified source it reuses and implemented the widget under the author's direction; the author takes full responsibility for the design, accuracy, and integrity of this work.
