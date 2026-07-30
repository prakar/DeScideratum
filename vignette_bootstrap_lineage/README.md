# The bootstrap vignette — an authoring-integration reference implementation

Where the three lineages (`resampling_lineage-source/`, `multiple_testing_lineage-source/`, `meta_analysis_lineage-source/`) prove the citation-as-invocation *mechanism* works, this folder proves it works **inside an independent, existing authoring tool** — MyST Markdown — rather than only inside hand-built HTML pages this project controls end to end.

Live page: [https://prakar.github.io/DeScideratum/bootstrap-vignette/](https://prakar.github.io/DeScideratum/bootstrap-vignette/) (deployed via GitHub Actions — see [`.github/workflows/deploy-pages.yml`](https://github.com/prakar/DeScideratum/blob/main/.github/workflows/deploy-pages.yml))
Source: `vignette.md`, built and served with [mystmd](https://mystmd.org)

## What's here

- **`vignette.md`** — the vignette itself: a real, original document (not a reproduction of any paper) demonstrating a citation written the classical way and the invocable way, side by side, about the same real methods from the resampling lineage.
- **`plugins/cite-invoke.mjs`** — a MyST directive, built for this project, that unifies `{cite}` and `{anywidget}` into a single construct: citing a method and running it become the same authoring act. See the plugin's own header comments for what's confirmed against mystmd's real source versus inferred. **Released, install directly:**
  ```yaml
  project:
    plugins:
      - https://github.com/prakar/DeScideratum/releases/download/v0.2.0/cite-invoke.mjs
  ```
  Release notes: [github.com/prakar/DeScideratum/releases/tag/v0.2.0](https://github.com/prakar/DeScideratum/releases/tag/v0.2.0)
- **`widgets/bootstrap_widget.js`** — the live widget the directive runs; reuses the resampling lineage's already-verified bootstrap code.
- **`package_cite_invoke_plugin.sh`** — assembles a submission-ready bundle (plugin, README, MIT license, manifest) for distribution as a GitHub Release asset, per mystmd's own documented distribution guidance (there is no central plugin registry — a persistent URL, e.g. a Release asset, is the standard path).
- **`deploy_vignette_to_pages.sh`** — builds the vignette with the correct `BASE_URL` for GitHub Pages subfolder hosting.

## Status

Released as `cite-invoke` v0.2.0 (MIT license), confirmed working end to end via live build: the directive loads, the widget computes and displays the correct result, and the citation it emits renders with the same formatting and hover behavior as an ordinary `{cite}` reference. No prior implementation — including NeuroLibre, the closest comparable MyST-based effort — has been found to unify citation and execution into a single construct this way.

Known limitation, not caused by this plugin: MyST's current anywidget host throws `MystAnyModel.save_changes not implemented yet` if a widget attempts two-way model sync. `bootstrap_widget.js` handles this defensively (try/catch, non-fatal, logged).

## Acknowledgments

This work — including the design, implementation, and verification of the `cite-invoke` directive — was carried out through iterative human-AI collaboration between Prasanna Varun Karmarkar (ORCID: [0009-0006-2284-6914](https://orcid.org/0009-0006-2284-6914)) and Claude (Sonnet 4.6/5, Anthropic), directed and verified throughout by the author. The AI's role included source-code analysis of mystmd's public MIT-licensed repository, implementation of the directive against confirmed internals, and validation through live testing; all design decisions, verification, and final responsibility for the work rest with the author.
