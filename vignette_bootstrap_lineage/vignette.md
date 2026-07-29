---
title: A Vignette Concerning Its Own Citability
subtitle: A companion document to the DeScideratum resampling lineage
authors:
  - name: The DeScideratum Project
date: 2026-07-28
---

## Purpose

This is a vignette: a short, self-contained illustrative document. The term is borrowed from the R and Bioconductor statistical computing world, where it has meant exactly this for decades — real methods, original prose, and a synthetic teaching example, clearly identified as a companion piece rather than the source material itself. Nothing here reproduces the text of any paper under discussion; the data below is illustrative, not drawn from any actual study. Everything else is original.

The purpose is narrow: to demonstrate that a citation can be written two ways in the same document, about the same real statistical methods, in a form a reader can distinguish on sight. One form is the standard citation, unchanged for centuries. The other is the subject of the project this vignette belongs to — and, unlike the project's other demonstrations, this one is not hand-built HTML. It runs inside an independent, open-source authoring tool (MyST Markdown), through a directive written for this purpose and confirmed working against MyST's own source code.

## Part One: the classic citation

Suppose you have a small sample of measurements and want to know how much its average can be trusted. The oldest rigorous answer is the bootstrap {cite}`efron1979`: resample the data with replacement, repeatedly, and let the spread of those resamples stand in for the uncertainty that cannot be observed directly. Two refinements followed — a bias-and-skew correction that sharpens the resulting interval {cite}`efron1993`, and a further calibration step that resamples the correction itself to test its stability {cite}`davison1997`.

This is ordinary scholarly writing: three names, three years, three pointers, asking the reader to trust that the author understood the underlying methods correctly. This is how citation has functioned for centuries, and it has been sufficient to build the great majority of scientific knowledge. It is also, for the project this document belongs to, the limit of what a citation has traditionally been able to do.

## Part Two: the same lineage, cited differently

MyST Markdown already provides two separate mechanisms relevant here: `{cite}`, an inline role that produces a citation — hoverable, linked, entered into the document's bibliography — and `{anywidget}`, a directive that embeds a live, interactive, in-browser component. Used together, as in an earlier draft of this document, a citation and a widget can sit next to each other on the page. They remain, however, two separate objects in MyST's own document model: deleting one leaves the other untouched, and nothing in the document records that they were ever related.

`{cite-invoke}` is a new directive, written for this project, that closes that gap. It does not choose between citing and running — it does both from a single call, by returning two sibling nodes from one directive: a citation node, indistinguishable from what `{cite}` itself produces, and a widget node, indistinguishable from what `{anywidget}` itself produces. Below, `{cite-invoke}` both cites {cite}`efron1979` in the ordinary sense — hoverable, entered into the reference list below, exactly as in Part One — and runs the same, already-verified bootstrap code used throughout this project, live, on data drawn from this document's own content. Delete this block, and both the citation and the execution disappear together, because as far as MyST's document model is concerned, they are now one object rather than two adjacent ones.

```{cite-invoke} efron1979
:esm: widgets/bootstrap_widget.js
{
  "default_data": "12.1, 14.3, 11.8, 15.9, 13.2, 10.7, 16.4, 12.9, 14.8, 11.2, 13.6, 15.1"
}
```

An earlier version of this section used `{cite}` and `{anywidget}` side by side, as two separate constructs, rather than the single `{cite-invoke}` call above — the citation appeared in the sentence, and the widget sat in its own block beneath it, with no structural relationship between them in the document itself. That version is no longer shown here, since the point it made is now made directly by the block above; the distinction is described here in words rather than duplicated in a second live copy.

## What building this actually required

`{cite-invoke}` did not exist before this project. It was built by reading MyST's own source code directly — the real implementation of `{anywidget}`, the type definitions governing how a MyST directive is permitted to emit AST nodes, and the tokenizer that parses `{cite}` — rather than inferring its behavior from documentation alone, and it was confirmed working through a live build: the plugin loads cleanly, the widget computes and displays the correct result, and the citation it emits renders with the same formatting and hover behavior as an ordinary `{cite}` reference elsewhere on this page. As far as this project has been able to determine, including a direct check against the closest comparable effort in the field (NeuroLibre, built on the same MyST foundation), no prior implementation unifies citation and execution into a single MyST construct this way.

The plugin is being prepared, separately from this document, for submission back to the MyST project itself.

## References

```{bibliography}
```
