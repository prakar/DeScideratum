# Citation horizon report — resampling lineage

The verification layer behind [the live page](https://prakar.github.io/DeScideratum/citation-horizon/). This documents a real, independently-verified citation chain upstream of the resampling lineage's own root paper, Efron (1979), classifying each edge into one of the subtypes Section 9.4 of the manuscript formalizes.

## Why this matters, read before the data below

The page makes one argument in three layers. Layer one, the chain itself: three papers, Efron (1979) → Miller (1974) → Quenouille (1949), each arrow labeled with what actually connects them rather than what's commonly assumed. Layer two, the four evidence cards: for each edge, what's commonly asserted (shown struck through) versus what's actually verified (shown in bold) — a direct, visual "here's the myth, here's the check" contrast. Layer three, the honest exception: the Miller→Quenouille/Tukey edge is the one card that looks visually different (dashed border, gray badge) — because unlike the other three, this one couldn't be verified at all (the only available copy of Miller's paper is a scanned image with no extractable text), and rather than assume it's true because "everyone says so," the page states plainly that it's unconfirmed.

The actual finding underneath all that design: the citation everyone assumes exists — Efron citing Quenouille and Tukey directly — isn't in Efron's paper. He routes through a review article instead. That's not a minor bibliographic footnote; it's the entire point made concrete. A claim repeated by hundreds of downstream papers turns out not to be what the primary source actually says, and the only way to know that was to go read the primary source directly, not trust the folklore.

This is a genuine project milestone, and specifically because it's the first artifact in the whole project that verifies something about the citation graph itself, rather than making a citation run. It is tracked as its own category — not folded into "the lineages" above it, and not folded into the authoring-integration vignettes either.

## What this is

`citation_horizon_report.json` — four classified edges, each with the claim commonly made, what was actually verified against the primary source, a confidence level, and the evidence itself. Three real findings, not smoothed into one:

1. **Efron → Miller (1974)**, not Efron → Quenouille/Tukey as almost universally assumed. Efron's own reference list was read directly; the widely-drawn edge does not exist in it.
2. **Tukey (1958)** is a real DOI resolving to a single-page abstract, commonly cited with a fabricated page range ("614–623"). A separate, automatable defect, distinct from the classification work.
3. **Quenouille (1949)** is a verified genuine horizon — its own reference list was checked, not merely left unsearched.

One edge (Miller → Quenouille/Tukey) is explicitly marked **unverified**, not filled in with a plausible assumption: the only available copy of Miller (1974) is a scanned image with no extractable text layer. This is a real, stated gap, not a smoothed-over one.

## What this is not

This is a provenance and verification artifact, not a runnable lineage. Unlike the resampling, multiple-testing, and meta-analysis lineages, nothing here invokes Quenouille's (1949) or Miller's (1974) actual statistical procedures as live code — that would be new implementation work, not yet started, and shouldn't be conflated with this verification pass.

**Discovery versus verification, stated plainly:** finding this chain required a human reading primary sources directly — not anything DeScideratum's own registry or rubric currently automate. Only one of the findings above (the Tukey page-range defect) is currently mechanically checkable without that kind of reading. The other three are honest expert verification of a chain a human found, not a chain the platform discovered on its own. See the live page's own "What this platform did, and what a human did" section for the same distinction, stated for a general reader.

## Status and next steps

The interactive page is live: [prakar.github.io/DeScideratum/citation-horizon/](https://prakar.github.io/DeScideratum/citation-horizon/).

1. If a text-layer copy of Miller (1974) becomes available, resolve the one unverified edge.
2. Longer-term, and separate: implementing Quenouille's (1949) split-half serial-correlation procedure as real, runnable code, which would let the chain extend as a genuine invocation lineage rather than only a verified provenance record.

## Provenance of this artifact

The underlying research was produced by a dedicated verification pass handed to a higher-capability model, specifically because the task — accurate recall and verification of obscure mid-20th-century statistics bibliography — is knowledge-density-bound, where a confident but wrong claim is costly and hard to catch. Prasanna Karmarkar directed and reviewed the handoff; Claude synthesized the findings into this structured artifact.
