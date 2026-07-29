# Running node --check on CLI
# extract everything between <script> (the one after pyodide.js) and </script>
    python3 -c "
    import re
    html = open('docs/resampling_knot_browser_v4.html').read()
    start = html.index('<script>', html.index('pyodide.js'))
    script = html[start+len('<script>'):html.index('</script>', start)]
    open('/tmp/check.js', 'w').write(script)
    "
    node --check /tmp/check.js

# Built the same into a script
    cat > check_html_js.sh << 'EOF'
    #!/bin/bash
    # extracts the inline <script> block from an HTML file and syntax-checks it with node
    python3 -c "
    html = open('$1').read()
    start = html.index('<script>', html.index('pyodide.js'))
    script = html[start+len('<script>'):html.index('</script>', start)]
    open('/tmp/check.js', 'w').write(script)
    " && node --check /tmp/check.js && echo "OK: $1"
    EOF
    chmod +x check_html_js.sh

# remove and prevent .pyc and _pycache_ from git tracking
    # 1. confirm the ignore rules are actually there — add if missing
    grep -qxF '__pycache__/' .gitignore || echo '__pycache__/' >> .gitignore
    grep -qxF '*.pyc' .gitignore || echo '*.pyc' >> .gitignore

    # 2. untrack anything already committed, without deleting it from disk
    git rm -r --cached '**/__pycache__' 2>/dev/null
    git rm --cached '**/*.pyc' 2>/dev/null

    git add .gitignore
    git commit -m "stop tracking __pycache__ / .pyc files"
    git push

        ```
        git rm --cached removes a file from git's tracking while leaving the actual file untouched on disk — important distinction from a plain rm, which would delete it locally too. After this, Python regenerating __pycache__ on every run (which it will, automatically, every time) won't show up as a change in git status again.
        ```
# Verifying JS syntax when the browser hangs with zero error output
    # a JS syntax error kills the ENTIRE script silently — nothing runs,
    # nothing logs, the page just sits frozen. node --check catches this
    # instantly instead of guessing.
    python3 -c "
    html = open('docs/resampling-lineage/index.html').read()
    start = html.index('<script>', html.index('pyodide.js'))
    script = html[start+len('<script>'):html.index('</script>', start)]
    open('/tmp/check.js', 'w').write(script)
    "
    node --check /tmp/check.js && echo "JS: VALID"

    Real bug this caught: a string like "One simulated \\"what if..." — a
    double-escaped backslash-then-quote instead of a single escaped quote
    (\") — closes the JS string early. node --check names the exact line;
    a frozen browser tab tells you nothing.

# Verifying the Python INSIDE that same script, without a browser at all
    # Pyodide runs Python embedded as a JS template literal (PY_SOURCE).
    # You can pull it out and run it as plain CPython to check the actual
    # computation is correct, before ever touching a browser.
    python3 -c "
    import re
    html = open('docs/resampling-lineage/index.html').read()
    m = re.search(r'const PY_SOURCE = \`(.*?)\`;', html, re.DOTALL)
    exec(m.group(1))
    print(run_chain([12.1,14.3,11.8,15.9,13.2,10.7,16.4,12.9,14.8,11.2,13.6,15.1], 1))
    "
    This is how every number on the live page got cross-checked against
    the terminal version before shipping — same inputs in, compare output
    by eye (or diff it) against a known-good run.

# Regression-testing "did my edit change the actual output" (not just "did it run")
    # run the OLD version and the NEW version, save both outputs, diff them.
    # Only the parts that matter (numbers), not log formatting noise.
    python3 run_demo.py > /tmp/before.txt   # from the old/working copy
    cd ../new_version && python3 run_demo.py > /tmp/after.txt
    grep -E "point_estimate|se=|CI=" /tmp/before.txt > /tmp/b1.txt
    grep -E "point_estimate|se=|CI=" /tmp/after.txt  > /tmp/b2.txt
    diff /tmp/b1.txt /tmp/b2.txt && echo "NUMBERS MATCH EXACTLY"

    Used every time the registry/schema got restructured — proves a
    refactor didn't quietly change behavior, rather than assuming it.

# Verifying a zip from the OUTSIDE before handing it over
    # don't trust the working directory — unzip fresh, into a clean temp
    # folder, and run it from there. Catches "works on my machine because
    # of a leftover file" bugs.
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
    zip -r project.zip project_folder -x "*__pycache__*"

    cd /tmp && rm -rf verify && mkdir verify && cd verify
    unzip -q ~/project.zip && cd project_folder
    python3 run_demo.py | tail -10   # should look identical to the original run

    This is the difference between "I built it" and "I confirmed the
    exact file you're about to receive actually works."

# Scrubbing git history completely (not just deleting files going forward)
    # git rm --cached (above) stops tracking a file GOING FORWARD but the
    # old commits still contain it, recoverable forever. For a full scrub
    # of a solo/unpushed-or-just-created repo:
    git checkout --orphan clean-main
    git add -A
    git commit -m "clean start"
    git branch -D main
    git branch -m main
    git push -f origin main   # only if already pushed to a remote

    --orphan creates a branch with ZERO parent commits — there's no
    history left for the old files to hide in. Nuclear option: only do
    this on a repo with no collaborators who've already cloned it, since
    a force-push doesn't reach copies other people already pulled.

# Remove and suppress MyST build from git

    echo "_build/" >> .gitignore
    git rm -r --cached vignette_bootstrap_lineage/_build
    git add .gitignore
    git commit -m "stop tracking MyST build output"
    git push