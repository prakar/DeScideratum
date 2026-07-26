# Resampling knot — working proof, not a diagram

Run: `python3 run_demo.py`

## What this actually proves

Three real functions, each mapping to a real paper:

- **Node A** — Efron (1979), "Bootstrap Methods: Another Look at the Jackknife." `functions/efron_1979_bootstrap.py`
- **Node B** — Efron & Tibshirani (1993), *An Introduction to the Bootstrap*, BCa intervals. `functions/efron_tibshirani_1993_bca.py` — **cites Node A by invoking it through `registry.invoke(fn_cid, ...)`, not by reimplementing it or linking to it.**
- **Node C** — Davison & Hinkley (1997), *Bootstrap Methods and Their Application*, double bootstrap. `functions/davison_hinkley_1997_double_bootstrap.py` — cites Node B the same way, producing a real two-hop chain.

`registry.py` is a deliberately toy stand-in for the Custodian's `resolve()`/`record_invocation()` path — content-addressed lookup by `fn_cid`, with `MAX_INVOCATION_DEPTH` enforced exactly as specified in the platform spec's §4.4. Running the demo against a synthetic reader dataset (not either paper's original data) and printing the invocation log is the actual test of the mechanism: it's not a sequence diagram of what invocation *would* look like, it's the invocation happening, with an assertion suite checked at the end.

## What's honestly still missing before this is the real thing

- **Not Pydantic.** This sandbox has no network access to install it; `@dataclass` + `__post_init__` validation is used instead, matching the contract shape (typed input, typed output, validated preconditions) exactly. Swapping to `BaseModel` + `field_validator` in the real Codespaces build is mechanical, not a redesign — flagged rather than silently substituted.
- **Not Pyodide.** This runs as native CPython. It proves the *invocation mechanism* (CID lookup, cross-document call, depth limit) is real and correct; it does not yet prove the *browser-native* portability claim from the runtime-constraints work. Every function here is deliberately built stdlib-only (no numpy/scipy) specifically so the port to Pyodide should be closer to trivial than for a function with heavier dependencies — worth verifying, not assuming, once ported.
- **`fn_cid` values are literal strings, not real content hashes.** The real system hashes the function's code + schema; here they're readable placeholders for demo clarity.

## Rubric application

Both Node B's citation of Node A, and Node C's citation of Node B, pass Stage 1 (E1: genuine Method/Uses — deleting either citation changes the reported numbers; E2: pure stdlib, no GPU, no threading, trivial memory) at Q1=2/Q2=2 by the same reasoning as Worked Example A in `citation_invocability_rubric_v0.1.md`. This knot was chosen first specifically because it should score cleanly — see that file for the harder cases (multiple-testing, dimensionality-reduction) still queued.
