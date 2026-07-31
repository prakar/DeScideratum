---
title: A Vignette on Honest Citation
subtitle: A companion document to the DeScideratum multiple-testing lineage
authors:
  - name: Prasanna Varun Karmarkar
    orcid: 0009-0006-2284-6914
date: 2026-07-30
---

[← DeScideratum](https://prakar.github.io/DeScideratum/) · [Full writeup on GitHub →](https://github.com/prakar/DeScideratum/blob/main/vignette_multiple_testing_lineage/README.md)

## Purpose

This is a vignette {cite}`leisch2002` — a short, self-contained illustrative document, real methods and original prose, a synthetic teaching example rather than any actual study's data.

The DeScideratum resampling vignette already established that a citation can run as live code inside MyST Markdown, through `cite-invoke`. This document tests something that one could not: whether a citation that correctly *cannot* become live code sits naturally in the same narrative as ones that can, without reading as an omission or a bug. A reader should be able to tell, from the text alone, which citation is which — and understand why.

## Part One: three citations, told the classical way

Suppose a genomics screen tests twenty candidate genes at once for association with a trait. Run twenty independent tests at the usual 5% threshold, and roughly one will look significant by chance alone, even if none of the genes matter. Benjamini and Hochberg's procedure controls this: of everything called significant, it bounds the expected fraction that is a false alarm {cite}`benjamini1995`. Storey's q-value method takes a related but distinct approach, estimating the proportion of genuinely null genes directly and using that estimate to make less conservative calls {cite}`storey2002`. A further paper addresses a complication neither of the first two considers: genes are rarely tested independently in practice, and Benjamini and Yekutieli proved that FDR control still holds when tests are positively correlated {cite}`benjaminiyekutieli2001`.

Read as prose, these are three ordinary citations — three names, three years, three pointers. Nothing in the text distinguishes which of the three methods a reader could, in principle, run themselves, and which is a claim about behavior under conditions the reader cannot directly execute.

## Part Two: two live, one honest

Below, Storey's q-value method runs as a `cite-invoke` call — the same directive proven in the resampling vignette. Its computation invokes Benjamini & Hochberg's procedure internally, exactly as the DeScideratum multiple-testing lineage's own code does: Storey's method cites BH's, not the reverse. A citation that stays deliberately inert sits beside it.

```{cite-invoke} storey2002
:esm: widgets/bh_storey_widget.js
{
  "default_data": "0.0001, 0.0004, 0.0012, 0.008, 0.011, 0.019, 0.021, 0.033, 0.041, 0.052, 0.078, 0.11, 0.14, 0.19, 0.24, 0.31, 0.42, 0.55, 0.71, 0.93"
}
```

Benjamini & Yekutieli {cite}`benjaminiyekutieli2001` is not wired to this widget, and this is not an omission. Their paper proves that FDR control extends to positively-dependent tests — a mathematical property, not a procedure a reader runs on data. Delete this citation, and neither number in the widget above changes; only the argument for why applying Benjamini-Hochberg or Storey's method to correlated genes remains valid loses its support. That is the dividing line `cite-invoke` runs on: a citation becomes live code only when deleting it would change a computed result. Everything else — including this one — stays exactly what citation has always been.

## The cite-invoke directive

`cite-invoke` is the same plugin proven in the resampling vignette — installed here from its published release, not rebuilt. Prasanna Varun Karmarkar directed its design and verified its behavior in both vignettes; Claude (Sonnet 4.6/5, Anthropic) analyzed mystmd's MIT-licensed source and implemented the directive under that direction. What this document adds is not a new mechanism but a new test of it: a real narrative in which two citations run and a third, correctly, does not — decided by the same rule the DeScideratum multiple-testing lineage itself already encodes.

```yaml
project:
  plugins:
    - https://github.com/prakar/DeScideratum/releases/download/v0.2.0/cite-invoke.mjs
```

## Acknowledgments

AI-use disclosure: Claude (Sonnet 4.6/5, Anthropic) assisted with source-code analysis and implementation as described above, under the direction and verification of the author, who takes full responsibility for the design, accuracy, and integrity of this work.

## References

```{bibliography}
```
