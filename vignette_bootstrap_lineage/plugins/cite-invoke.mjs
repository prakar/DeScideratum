// cite-invoke.mjs
//
// A MyST directive that unifies {cite} and {anywidget} into one construct:
// citing a method and running it become the same authoring act, producing
// two sibling AST nodes from a single directive call.
//
// Built directly against confirmed mystmd source (commit 4de8d726, provided
// by the user, fetched from packages/myst-common/src/types.ts and
// packages/myst-directives/src/anywidget.ts):
//
//   - DirectiveSpec.run() returns GenericNode[] -- CONFIRMED. This is what
//     makes emitting two sibling nodes from one directive possible at all.
//   - The anywidget node shape -- CONFIRMED, copied exactly:
//     { type: 'anywidget', esm, model, css?, class?, id }
//   - The cite node shape { type: 'cite', label, kind } -- was an inference
//     at write time, based on the markdown-it tokenizer's { label, kind }
//     meta shape and this codebase's consistent 1:1 token-to-node naming.
//     CONFIRMED as of a live build (2026-07-29): the emitted citation
//     rendered with correct formatting and hover behavior, indistinguishable
//     from an ordinary {cite} reference on the same page.
//
// Known, confirmed limitation, not caused by this plugin: MyST's current
// anywidget host throws "MystAnyModel.save_changes not implemented yet" if
// a widget attempts two-way model sync. Not this directive's concern --
// any widget module used with {cite-invoke} should treat model writes as
// best-effort and non-fatal (see widgets/bootstrap_widget.js for the
// pattern: try/catch around model.set()/save_changes(), computation and
// display already complete before that call is attempted).
//
// Deliberately does not import nanoid, unlike the real anywidget.ts --
// that import resolves fine inside mystmd's own package but is an
// unverified risk for a standalone plugin file loaded from outside it.
// A small local ID generator removes that risk entirely.

// Version 0.2.0 (0.1.0 was pre-live-test; 0.2.0 = confirmed working end to
// end, per the header notes above). Recorded here and in the package
// manifest, not in the exported plugin object -- MystPlugin's confirmed
// type (myst-common/src/types.ts) has no version field, and this build has
// stayed disciplined about not adding anything unconfirmed to the runtime
// object MyST actually consumes.

function localId() {
  return 'ci-' + Math.random().toString(36).slice(2, 10);
}

const citeInvokeDirective = {
  name: 'cite-invoke',
  doc: 'A citation that is also a live, executable widget. Emits both a real citation node (participates in the bibliography) and a real anywidget node (runs live), from one call.',
  arg: {
    type: String,
    required: true,
    doc: 'The BibTeX citation key -- identical to what you would pass to {cite}',
  },
  options: {
    esm: {
      type: String,
      required: true,
      doc: 'Path or URL to the ESM JS module for the live widget',
    },
    kind: {
      type: String,
      required: false,
      doc: "'narrative' or 'parenthetical' citation style -- default 'parenthetical'",
    },
    css: {
      type: String,
      required: false,
      doc: 'Path or URL to a CSS file for the widget (passed through to anywidget, unmodified)',
    },
    class: {
      type: String,
      required: false,
      doc: 'Space-delimited class names for the widget (passed through to anywidget, unmodified)',
    },
  },
  body: {
    type: String,
    required: false,
    doc: 'JSON (or JSON5) props to pass down to the widget -- same convention as {anywidget}',
  },
  validate(data, vfile) {
    if (typeof data.arg !== 'string' || !data.arg) {
      vfile.message('cite-invoke requires a citation key as its argument.');
    }
    if (!data.options?.esm) {
      vfile.message('cite-invoke requires :esm: pointing at a widget module.');
    }
    return data;
  },
  run(data, vfile, _ctx) {
    const citeKey = data.arg;
    const kind = data.options?.kind === 'narrative' ? 'narrative' : 'parenthetical';

    let model = {};
    if (data.body !== undefined) {
      try {
        model = JSON.parse(data.body);
      } catch (e) {
        vfile.message('Invalid JSON supplied in cite-invoke body -- widget will render with an empty model.');
      }
    }

    // Node 1: the citation. Real participation in the bibliography is the
    // point of this whole plugin -- this is not a decorative label sitting
    // next to the widget, it is the same node type {cite} itself produces.
    const citeNode = {
      type: 'cite',
      kind,
      label: citeKey,
    };

    // Node 2: the widget. Field-for-field identical to what the real
    // {anywidget} directive emits (see anywidget.ts) -- deliberately not
    // reinvented, just constructed directly rather than via the directive
    // fence syntax.
    const widgetNode = {
      type: 'anywidget',
      esm: data.options.esm,
      model,
      css: data.options?.css,
      class: data.options?.class,
      id: localId(),
    };

    return [citeNode, widgetNode];
  },
};

const plugin = {
  name: 'cite-invoke',
  // Author: Prasanna Varun Karmarkar (ORCID: 0009-0006-2284-6914).
  // Built through human-AI collaboration -- design directed and verified
  // by the author; implementation and mystmd source analysis assisted by
  // Claude (Sonnet 4.6/5, Anthropic). Full disclosure in README.md.
  author: 'Prasanna Varun Karmarkar (ORCID: 0009-0006-2284-6914)',
  license: 'MIT',
  directives: [citeInvokeDirective],
};

export default plugin;
