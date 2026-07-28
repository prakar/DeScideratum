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