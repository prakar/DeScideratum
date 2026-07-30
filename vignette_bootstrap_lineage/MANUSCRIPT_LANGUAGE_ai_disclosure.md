# Manuscript language: the cite-invoke plugin and AI-use disclosure

Drop-in text for whichever section structure the target venue uses. Adjust venue-specific phrasing (e.g. NEJM wants disclosure in two locations, Science in three — see notes below) but keep the substance: specific, verifiable, and framed as disclosure, not authorship.

---

## For Methods (or an "Implementation" subsection)

> [AUTHOR NAME] extended the citation-as-invocation mechanism into an existing, independent authoring tool to test whether it could be embedded in a document format this work did not control, rather than only demonstrated in purpose-built pages. [AUTHOR NAME] selected MyST Markdown — an open-source (MIT-licensed), actively maintained scientific-publishing toolchain used by projects including NeuroLibre — as the target, and built a directive, `cite-invoke`, by extending mystmd's public source directly: reading and confirming its type system (governing how a directive may emit abstract-syntax-tree nodes), its existing `{anywidget}` directive implementation, and its citation tokenizer before implementation, rather than inferring behavior from documentation alone. The resulting directive emits two sibling AST nodes from a single authoring call — a citation node, structurally identical to what MyST's native `{cite}` role produces, and a widget node, structurally identical to what its native `{anywidget}` directive produces — unifying citation and execution into one construct rather than two independently-authored, unrelated ones. [AUTHOR NAME] confirmed the directive working through a live build: correct citation rendering (formatting and hover behavior indistinguishable from a native `{cite}` reference), correct widget execution, and correct removal of both when the construct is deleted. [AUTHOR NAME] released the plugin under the MIT license as `cite-invoke` (v0.2.0), available at [github.com/prakar/DeScideratum/releases/tag/v0.2.0](https://github.com/prakar/DeScideratum/releases/tag/v0.2.0), installable directly via `https://github.com/prakar/DeScideratum/releases/download/v0.2.0/cite-invoke.mjs`.

## For Acknowledgments (or a dedicated "AI Use" section, if the venue requires one)

> [AUTHOR NAME] directed the design, implementation, and verification of the `cite-invoke` MyST directive described in [SECTION REF], in collaboration with Claude (Sonnet 4.6/5, Anthropic). Claude analyzed mystmd's public MIT-licensed source code and implemented the directive against confirmed internals; [AUTHOR NAME] verified the result through live testing. [AUTHOR NAME] made all design decisions and interpreted all results, and takes full responsibility for the accuracy and integrity of this work. No AI system is an author of this work.

## Notes on placement, per current (Jan 2026 ICMJE) norms

- **AI is never listed as an author or co-author**, under any framing — this is now near-universal across major venues (ICMJE, Nature, Science, NEJM, BMJ, JAMA all converge on this). The disclosure above is written to be specific and informative without crossing into authorship framing.
- **Where disclosure goes varies by venue** — check the specific target journal's instructions before submission:
  - *Nature*-style: Methods section only.
  - *NEJM*-style: two locations (commonly: manuscript body + cover letter).
  - *Science*-style: three locations (cover letter, acknowledgments, methods).
  - Many venues now have a dedicated, structured "AI Use Disclosure" field at submission — if so, use that field's required format rather than free text, and keep the Acknowledgments language above as the human-readable version.
- **Cover letter language**, if required: *"AI-assisted technology (Claude, Anthropic) was used during this work; its use is disclosed in [Methods/Acknowledgments/Section X]. The author directed all design decisions and takes full responsibility for the accuracy and integrity of the submitted work."*
