# Manuscript language: the cite-invoke plugin and AI-use disclosure

Drop-in text for whichever section structure the target venue uses. Adjust venue-specific phrasing (e.g. NEJM wants disclosure in two locations, Science in three — see notes below) but keep the substance: specific, verifiable, and framed as disclosure, not authorship.

---

## For Methods (or an "Implementation" subsection)

> The citation-as-invocation mechanism was extended into an existing, independent authoring tool to test whether it could be embedded in a document format this project did not control, rather than only demonstrated in purpose-built pages. MyST Markdown — an open-source (MIT-licensed), actively maintained scientific-publishing toolchain used by projects including NeuroLibre — was selected as the target. A directive, `cite-invoke`, was built by extending mystmd's public source directly: its type system (governing how a directive may emit abstract-syntax-tree nodes), its existing `{anywidget}` directive implementation, and its citation tokenizer were read and confirmed before implementation, rather than inferred from documentation alone. The resulting directive emits two sibling AST nodes from a single authoring call — a citation node, structurally identical to what MyST's native `{cite}` role produces, and a widget node, structurally identical to what its native `{anywidget}` directive produces — unifying citation and execution into one construct rather than two independently-authored, unrelated ones. The directive was confirmed working through a live build: correct citation rendering (formatting and hover behavior indistinguishable from a native `{cite}` reference), correct widget execution, and correct removal of both when the construct is deleted. The plugin is released under the MIT license as `cite-invoke` (v0.2.0), available at [github.com/prakar/DeScideratum/releases/tag/v0.2.0](https://github.com/prakar/DeScideratum/releases/tag/v0.2.0), installable directly via `https://github.com/prakar/DeScideratum/releases/download/v0.2.0/cite-invoke.mjs`.

## For Acknowledgments (or a dedicated "AI Use" section, if the venue requires one)

> This work — including the design, implementation, and verification of the `cite-invoke` MyST directive described in [SECTION REF] — was carried out through iterative human-AI collaboration between the author and Claude (Sonnet 4.6/5, Anthropic), directed and verified throughout by the author. The AI's role included analysis of mystmd's public MIT-licensed source code, implementation of the directive against confirmed internals, and validation through live testing. All design decisions, interpretation of results, and final responsibility for the accuracy and integrity of this work rest with the author. No AI system is an author of this work.

## Notes on placement, per current (Jan 2026 ICMJE) norms

- **AI is never listed as an author or co-author**, under any framing — this is now near-universal across major venues (ICMJE, Nature, Science, NEJM, BMJ, JAMA all converge on this). The disclosure above is written to be specific and informative without crossing into authorship framing.
- **Where disclosure goes varies by venue** — check the specific target journal's instructions before submission:
  - *Nature*-style: Methods section only.
  - *NEJM*-style: two locations (commonly: manuscript body + cover letter).
  - *Science*-style: three locations (cover letter, acknowledgments, methods).
  - Many venues now have a dedicated, structured "AI Use Disclosure" field at submission — if so, use that field's required format rather than free text, and keep the Acknowledgments language above as the human-readable version.
- **Cover letter language**, if required: *"AI-assisted technology (Claude, Anthropic) was used during this work; its use is disclosed in [Methods/Acknowledgments/Section X]. The author directed all design decisions and takes full responsibility for the accuracy and integrity of the submitted work."*
