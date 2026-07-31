---
title: A Vignette Concerning Its Own Citability
subtitle: A companion document to the DeScideratum resampling lineage
authors:
  - name: The DeScideratum Project
date: 2026-07-28
---

[← DeScideratum](https://prakar.github.io/DeScideratum/) · [Full writeup on GitHub →](https://github.com/prakar/DeScideratum/blob/main/vignette_bootstrap_lineage/README.md)

## Purpose

This is a vignette {cite}`leisch2002` — a short, self-contained illustrative document. The term comes from the R and Bioconductor statistical computing world: real methods, original prose, and a synthetic teaching example, identified as a companion piece rather than the source material itself. Nothing here reproduces the text of any paper under discussion; the data below is illustrative, not drawn from any actual study.

A citation can be written two ways in the same document, about the same real statistical methods, in a form a reader can distinguish on sight. One form is the standard citation, unchanged for centuries. The other is DeScideratum's subject: citation as invocation, demonstrated here inside an independent, open-source authoring tool, MyST Markdown, through a directive built for this purpose and confirmed against MyST's own source.

## Part One: the classic citation

Suppose you have a small sample of measurements and want to know how much its average can be trusted. The oldest rigorous answer is the bootstrap {cite}`efron1979`: resample the data with replacement, repeatedly, and let the spread of those resamples stand in for the uncertainty that cannot be observed directly. Two refinements followed — a bias-and-skew correction that sharpens the resulting interval {cite}`efron1993`, and a further calibration step that resamples the correction itself to test its stability {cite}`davison1997`.

This is ordinary scholarly writing: three names, three years, three pointers, asking the reader to trust that the author understood the underlying methods correctly. Citation has functioned this way for centuries, and it has been sufficient to build the great majority of scientific knowledge. It is also the limit of what a citation has traditionally been able to do.

## Part Two: the same lineage, cited differently

MyST Markdown provides two separate mechanisms relevant here: `{cite}`, an inline role that produces a citation — hoverable, linked, entered into the document's bibliography — and `{anywidget}`, a directive that embeds a live, interactive, in-browser component. Used side by side, a citation and a widget sit next to each other on the page, but remain two separate objects in MyST's own document model: deleting one leaves the other untouched, and nothing in the document records that they were ever related.

`{cite-invoke}` closes that gap. It does not choose between citing and running — it does both from a single call, by returning two sibling nodes from one directive: a citation node, indistinguishable from what `{cite}` itself produces, and a widget node, indistinguishable from what `{anywidget}` itself produces. Below, `{cite-invoke}` both cites {cite}`efron1979` in the ordinary sense — hoverable, entered into the reference list below, exactly as in Part One — and runs the resampling lineage's bootstrap code, live, on data drawn from this document's own content. Delete this block, and the citation and the execution disappear together: they are one object, not two adjacent ones.

```{cite-invoke} efron1979
:esm: widgets/bootstrap_widget.js
{
  "default_data": "12.1, 14.3, 11.8, 15.9, 13.2, 10.7, 16.4, 12.9, 14.8, 11.2, 13.6, 15.1"
}
```

Citing and running a method separately — `{cite}` in the sentence, `{anywidget}` in its own block beneath it — leaves no structural relationship between them: two adjacent objects, not one. `{cite-invoke}` above is the alternative.

## The cite-invoke directive

Prasanna Varun Karmarkar (ORCID: [0009-0006-2284-6914](https://orcid.org/0009-0006-2284-6914)) directed the design of `{cite-invoke}` and verified its behavior. Claude (Sonnet 4.6/5, Anthropic) read mystmd's MIT-licensed source directly — the `{anywidget}` implementation, the type definitions governing how a directive emits AST nodes, and the tokenizer that parses `{cite}` — and implemented the directive against those confirmed internals, rather than inferring behavior from documentation alone. Karmarkar confirmed the result through a live build: the plugin loads, the widget computes and displays the correct result, and the citation it emits renders with the same formatting and hover behavior as an ordinary `{cite}` reference elsewhere on this page. No prior implementation, including NeuroLibre — the closest comparable MyST-based effort — unifies citation and execution into a single construct this way.

Karmarkar released the plugin under an open license as `cite-invoke`, distributed as a single dependency-free module. Install it directly from its published release — no build step, no registry:

```yaml
project:
  plugins:
    - https://github.com/prakar/DeScideratum/releases/download/v0.2.0/cite-invoke.mjs
```

Full release notes: [github.com/prakar/DeScideratum/releases/tag/v0.2.0](https://github.com/prakar/DeScideratum/releases/tag/v0.2.0)

## Acknowledgments

AI-use disclosure: Claude (Sonnet 4.6/5, Anthropic) assisted with source-code analysis and implementation as described above, under the direction and verification of the author, who takes full responsibility for the design, accuracy, and integrity of this work.

## References

```{bibliography}
```
