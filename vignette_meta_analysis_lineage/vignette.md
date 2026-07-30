---
title: A Vignette on Conditions That Travel With a Number
subtitle: A companion document to the DeScideratum meta-analysis lineage
authors:
  - name: Prasanna Varun Karmarkar
    orcid: 0009-0006-2284-6914
date: 2026-07-30
---

## Purpose

This is a vignette {cite}`leisch2002` — a short, self-contained illustrative document, real methods and original prose, a synthetic teaching example rather than any actual study's data.

The two prior DeScideratum vignettes established that a citation can run as live code inside MyST Markdown, and that a citation which correctly cannot run sits naturally beside ones that can. This document tests a third, different property: whether a citation's Applicability Profile — the conditions under which its number is actually valid — survives being stated in ordinary prose, or whether it only ever worked as a field in a table a reader could silently ignore.

## Part One: pooling five studies, told the classical way

Suppose five independent studies each estimate the same effect, with different precision and under different conditions. Cochran's method combines them into one weighted estimate, giving more precise studies more influence {cite}`cochran1954`. DerSimonian and Laird extended this by allowing for genuine disagreement between studies, not just each study's own sampling noise {cite}`dersimonianlaird1986`. Higgins and Thompson turned that disagreement into a single interpretable number, the percentage of total variation that reflects real heterogeneity rather than chance {cite}`higginsthompson2002`.

Read this way, pooling five studies into one number looks clean. It is also, without more context, incomplete: an average of five estimates says nothing about whether those five studies actually measured comparable things.

## Part Two: the same pooling, with the conditions attached

Below, the same three methods run live, on five studies you can edit directly. Each row carries more than an estimate and a standard error — a population, and the conditions under which that estimate was obtained.

```{cite-invoke} higginsthompson2002
:esm: widgets/meta_analysis_widget.js
{
  "default_data": "[{\"label\": \"Study 1\", \"estimate\": 0.42, \"se\": 0.08, \"population\": \"adults, urban clinic\", \"conditions\": \"6-week follow-up\"}, {\"label\": \"Study 2\", \"estimate\": 0.35, \"se\": 0.10, \"population\": \"adults, rural clinic\", \"conditions\": \"6-week follow-up\"}, {\"label\": \"Study 3\", \"estimate\": 0.51, \"se\": 0.09, \"population\": \"adults, mixed setting\", \"conditions\": \"8-week follow-up\"}, {\"label\": \"Study 4\", \"estimate\": 0.28, \"se\": 0.12, \"population\": \"adults, urban clinic\", \"conditions\": \"4-week follow-up\"}, {\"label\": \"Study 5\", \"estimate\": 0.45, \"se\": 0.07, \"population\": \"adults, urban clinic\", \"conditions\": \"6-week follow-up\"}]"
}
```

Two of these rows are worth reading, not just pooling. Study 3 measured its outcome at eight weeks, two weeks later than every other study in the set — a real, stated difference in what was actually measured, sitting inside the same pooled average as the rest. Study 4 was followed up earliest, at four weeks, with the widest uncertainty of any study here (SE = 0.12, nearly twice most of the others) — a signal, on its own, that this estimate carries less information than its neighbors, before any pooling happens at all.

None of this is hidden by the live citation above. It runs the same way regardless of whether a reader reads this paragraph — the difference is whether the reader *notices*. A conventional pooled estimate reports one number and asks for trust. This one reports the number and leaves the conditions sitting next to it, in the same object, available to whoever wants to check whether five studies were actually comparable enough to average.

## The cite-invoke directive

`cite-invoke` is the same plugin proven in the first two vignettes — installed here from its published release. Prasanna Varun Karmarkar directed its application here and verified its behavior; Claude (Sonnet 4.6/5, Anthropic) analyzed mystmd's MIT-licensed source and implemented the directive under that direction. What distinguishes this vignette is not the mechanism but the payload: the widget above carries a real Applicability Profile per study, and the prose above names two specific rows directly, testing whether that structured information can be discussed the way a real paper would discuss it — not just displayed in a table a reader could scroll past.

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
