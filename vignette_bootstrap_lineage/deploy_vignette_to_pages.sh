#!/bin/bash
# deploy_vignette_to_pages.sh
#
# Builds the vignette as a static site with the correct base URL for
# GitHub Pages subfolder hosting, then stages it for copying into docs/.
#
# Run from inside vignette_bootstrap_lineage/, after `pip install mystmd`
# if not already installed. Requires network (fetches Pyodide/thebe
# assets at build time) -- run this in Codespaces, not offline.

set -e

# GitHub Pages serves this repo at https://prakar.github.io/DeScideratum/
# -- a build meant to live at .../DeScideratum/bootstrap-vignette/ needs
# every asset path in the built HTML to be prefixed accordingly, or CSS/
# JS/Pyodide assets will 404 once deployed (they'd resolve fine locally,
# where there's no prefix, which is exactly the kind of bug that only
# shows up after deploying -- setting this now avoids that entirely).
export BASE_URL="/DeScideratum/bootstrap-vignette"

echo "== Building with BASE_URL=$BASE_URL =="
myst build --html

echo "== Staging output =="
REPO_ROOT="$(cd .. && pwd)"
DEST="$REPO_ROOT/docs/bootstrap-vignette"

rm -rf "$DEST"
mkdir -p "$DEST"
cp -r _build/html/* "$DEST/"

echo ""
echo "== Done =="
echo "Staged at $DEST"
echo "Next: git add docs/bootstrap-vignette, commit, push."
echo "Then update docs/index.html to link to it (see chat for the card to add)."
