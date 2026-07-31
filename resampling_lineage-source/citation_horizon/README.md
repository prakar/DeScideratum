# Citation horizon report — resampling lineage

The verification layer, not yet the interactive page. This documents a real, independently-verified citation chain upstream of the resampling lineage's own root paper, Efron (1979), classifying each edge into one of the subtypes Section 9.4 of the manuscript formalizes.

## What this is

`citation_horizon_report.json` — four classified edges, each with the claim commonly made, what was actually verified against the primary source, a confidence level, and the evidence itself. Three real findings, not smoothed into one:

1. **Efron → Miller (1974)**, not Efron → Quenouille/Tukey as almost universally assumed. Efron's own reference list was read directly; the widely-drawn edge does not exist in it.
2. **Tukey (1958)** is a real DOI resolving to a single-page abstract, commonly cited with a fabricated page range ("614–623"). A separate, automatable defect, distinct from the classification work.
3. **Quenouille (1949)** is a verified genuine horizon — its own reference list was checked, not merely left unsearched.

One edge (Miller → Quenouille/Tukey) is explicitly marked **unverified**, not filled in with a plausible assumption: the only available copy of Miller (1974) is a scanned image with no extractable text layer. This is a real, stated gap, not a smoothed-over one.

## What this is not, yet

This is a provenance and verification artifact, not a runnable lineage. Unlike the resampling, multiple-testing, and meta-analysis lineages, nothing here invokes Quenouille's (1949) or Miller's (1974) actual statistical procedures as live code — that would be new implementation work, not yet started, and shouldn't be conflated with this verification pass.

## Next steps, in order

1. An interactive citation-horizon page, presenting this same classification live — likely as an extension of the resampling lineage's own site rather than a fourth standalone lineage, since it documents that lineage's own upstream provenance.
2. If a text-layer copy of Miller (1974) becomes available, resolve the one unverified edge.
3. Longer-term, and separate: implementing Quenouille's (1949) split-half serial-correlation procedure as real, runnable code, which would let the chain extend as a genuine invocation lineage rather than only a verified provenance record.

## Provenance of this artifact

The underlying research was produced by a dedicated verification pass handed to a higher-capability model, specifically because the task — accurate recall and verification of obscure mid-20th-century statistics bibliography — is knowledge-density-bound, where a confident but wrong claim is costly and hard to catch. Prasanna Karmarkar directed and reviewed the handoff; Claude synthesized the findings into this structured artifact.
