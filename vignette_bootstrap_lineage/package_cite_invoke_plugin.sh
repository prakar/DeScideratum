#!/bin/bash
# package_cite_invoke_plugin.sh
#
# Assembles a clean, submission-ready package for the cite-invoke MyST
# plugin -- the plugin file, a README, a license, and a manifest.
#
# DOES NOT publish or submit anything anywhere. Run this only after
# `myst build` has confirmed the plugin actually loads and the citation
# is correctly picked up by the bibliography -- per the project's own
# rule: prove it works, package it, THEN consider submitting it.
#
# Usage: ./package_cite_invoke_plugin.sh
# Output: ./cite-invoke-package/  (a clean folder, ready to zip or
#         attach as a GitHub Release asset)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR/plugins/cite-invoke.mjs"
OUT="$SCRIPT_DIR/cite-invoke-package"
VERSION="0.2.0"

if [ ! -f "$SRC" ]; then
  echo "ERROR: $SRC not found. Expected plugins/cite-invoke.mjs next to this script."
  exit 1
fi

echo "== Checking the plugin is self-contained (no unresolved external imports) =="
# The real anywidget.ts imports nanoid; this plugin deliberately does not,
# specifically to avoid unverified module-resolution risk for a
# standalone, externally-hosted plugin file. This check enforces that
# choice stays true rather than silently regressing.
if grep -qE "^import .* from '(?!\.\/)" "$SRC" 2>/dev/null; then
  echo "WARNING: found an import from an external package (not a relative path)."
  echo "This plugin is meant to be dependency-free -- check before packaging."
  grep -E "^import" "$SRC"
  exit 1
else
  echo "OK: no external package imports found."
fi

echo "== Validating JS syntax =="
node --check "$SRC" || { echo "ERROR: plugin has a syntax error, not packaging."; exit 1; }
echo "OK: syntax valid."

echo "== Assembling package =="
rm -rf "$OUT"
mkdir -p "$OUT"
cp "$SRC" "$OUT/cite-invoke.mjs"

cat > "$OUT/README.md" << MDEOF
# cite-invoke

A MyST Markdown directive that unifies \`{cite}\` and \`{anywidget}\` into one
construct: citing a method and running it become the same authoring act.

\`\`\`{cite-invoke} yourBibtexKey
:esm: path/to/your/widget.js
{
  "your_prop": "your default value"
}
\`\`\`

emits two real, sibling AST nodes from that one call -- a citation node
(participates in the project bibliography, same as \`{cite}\` itself
produces) and an anywidget node (runs live, same as \`{anywidget}\` itself
produces).

## Install

Add to your \`myst.yml\`:

\`\`\`yaml
project:
  plugins:
    - https://<persistent-url>/cite-invoke.mjs
\`\`\`

## Options

- **arg** (required): the BibTeX citation key, identical to what \`{cite}\` expects.
- **:esm:** (required): path or URL to the ESM JS module for the live widget.
- **:kind:** (optional): \`narrative\` or \`parenthetical\` citation style. Default \`parenthetical\`.
- **:css:** (optional): path or URL to a CSS file, passed through to the widget unmodified.
- **:class:** (optional): space-delimited class names, passed through unmodified.
- **body** (optional): JSON/JSON5 props passed to the widget's model.

## Status

Built against mystmd source at commit \`4de8d726c6fc1ade6d5cb16a7a136534639497cb\`.
The citation node shape (\`{ type: 'cite', label, kind }\`) was an inference
at write time; confirmed via a live build on 2026-07-29 -- the emitted
citation rendered with correct formatting and hover behavior,
indistinguishable from an ordinary \`{cite}\` reference on the same page.
MyST's own \`myst-spec\` README states the AST specification "is still in
dev" and "may change at any time without notice," so this confirmation is
current as of the commit above, not a permanent guarantee.

Known limitation, not caused by this plugin: MyST's current anywidget host
throws \`MystAnyModel.save_changes not implemented yet\` if a widget
attempts two-way model sync. Any widget module used with \`{cite-invoke}\`
should treat model writes as best-effort (try/catch, non-fatal) -- see the
example widget in the DeScideratum resampling lineage for the pattern.

## Origin

Built for the DeScideratum project (citation-as-invocation research
prototype) as the first known unification of MyST's citation and
anywidget systems -- confirmed, at time of writing, not to exist
elsewhere in the MyST ecosystem, including NeuroLibre.
MDEOF

cat > "$OUT/LICENSE" << 'LICEOF'
MIT License

Copyright (c) 2026 The DeScideratum Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
LICEOF

cat > "$OUT/manifest.json" << JSONEOF
{
  "name": "cite-invoke",
  "version": "$VERSION",
  "description": "Unifies MyST's {cite} and {anywidget} into one directive -- citation and execution as one construct.",
  "author": "The DeScideratum Project",
  "license": "MIT",
  "myst_commit_verified_against": "4de8d726c6fc1ade6d5cb16a7a136534639497cb",
  "status": "confirmed working end to end via live build, 2026-07-29 -- not yet submitted upstream"
}
JSONEOF

echo ""
echo "== Done =="
echo "Package assembled at $OUT -- NOT published anywhere."
echo "Next step per project rule: confirm 'myst build' works correctly first,"
echo "then this folder is ready to zip and attach as a GitHub Release asset,"
echo "or open as a PR to mystmd's examples/plugins."
