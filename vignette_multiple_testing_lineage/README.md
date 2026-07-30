# The multiple-testing vignette — proving the honest negative survives real prose

Where the resampling vignette proved `cite-invoke` works inside an independent authoring tool at all, this one tests something that first vignette never touched: whether a citation that correctly *cannot* become live code sits naturally in the same real narrative as ones that can, without reading as an omission.

Live page: [https://prakar.github.io/DeScideratum/multiple-testing-vignette/](https://prakar.github.io/DeScideratum/multiple-testing-vignette/) (deployed via GitHub Actions — see [`.github/workflows/deploy-pages.yml`](https://github.com/prakar/DeScideratum/blob/main/.github/workflows/deploy-pages.yml))
Source: `vignette.md`, built and served with [mystmd](https://mystmd.org)

## What's here

- **`vignette.md`** — the vignette itself: a synthetic genomics-screen narrative citing three real papers, two of which run live via `cite-invoke` (Storey's method, which internally invokes Benjamini & Hochberg's — matching the real lineage's actual dependency direction) and one of which — Benjamini & Yekutieli — stays a plain, deliberate `{cite}`, with the reasoning stated directly in the text.
- **`widgets/bh_storey_widget.js`** — the live widget; the Python inside is copied verbatim from the already-verified `docs/multiple-testing-lineage/index.html`, not re-derived.
- **`references.bib`** — includes the Benjamini-Yekutieli (2001) entry alongside the two invocable citations, since it's a real, ordinary reference — just not one wired to a widget.

## Status

Numerically cross-checked against the same known-good baseline as the hand-built multiple-testing lineage page (`n_significant=5`, `π₀=0.5000`) before this vignette shipped. Uses `cite-invoke` v0.2.0 installed from its published release, not a local copy — the first real second-consumer test of the plugin's persistent distribution URL.

## Acknowledgments

Prasanna Varun Karmarkar (ORCID: [0009-0006-2284-6914](https://orcid.org/0009-0006-2284-6914)) directed the design of this vignette and verified its behavior. Claude (Sonnet 4.6/5, Anthropic) analyzed the already-verified source it reuses and implemented the widget under the author's direction; the author takes full responsibility for the design, accuracy, and integrity of this work.
