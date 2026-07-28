# The resampling knot — a working proof, not a diagram

Three papers, forty years apart, cited into each other as live function calls instead of footnotes. This folder contains the working code; `docs/resampling_knot_browser_v4.html` (repo root) is the same thing running zero-install in a browser, with a plain-language walkthrough and a glossary built in — the explanation below is the same story, for anyone reading the code directly.

Run: `python3 run_demo.py`

## The question all three papers answer a piece of

Twelve numbers — pick your own when you run it — average to some value. Call it 13.5. The question every one of these three papers is trying to answer is the one that comes up any time you have a small sample: **you have an average, but how much do you trust it?** If you'd measured twelve different things, you wouldn't get exactly the same average again — so how far off could the true value plausibly be?

## Efron (1979) — the base case

The classical answer is a formula: standard error = (sample standard deviation) / √n — trustworthy only if your data roughly follows specific distributional assumptions, which for a small, messy real-world sample you often can't verify. Efron's 1979 insight, and the actual thing this code cites: **treat your own sample as a stand-in for the population, and simulate "what if I'd drawn a different sample" by resampling from your own data, with replacement.** The code draws 12 numbers at random from your 12 (repeats allowed), averages them, repeats that 5,000 times, and the spread of those 5,000 "what-if" averages *is* the uncertainty estimate — no distributional assumption required. `se=0.5150` in a typical run is the standard deviation of those 5,000 resampled averages. That's the entire 1979 contribution, executing in `functions/efron_1979_bootstrap.py`.

## Efron & Tibshirani (1993) — BCa, and why it cannot run without Efron's code

The plain 1979 bootstrap has two known imperfections, and this is what makes the citation *structural*, not just intellectual lineage:

- **Bias** (`z0`): the center of the 5,000 resampled averages doesn't always land exactly on the original estimate. Near zero means little correction was needed.
- **Acceleration** (`a`): how much the estimate wobbles can itself depend on the true value — asymmetric uncertainty. Computed via the jackknife (leave one data point out, twelve times, see how much the average shifts each time).

**BCa's published math is defined as a correction applied to the 1979 bootstrap's output — there is no way to compute it without that output first existing.** That's not a stylistic choice in how this was implemented; it's true of the method as published. Which is why `functions/efron_tibshirani_1993_bca.py` has no choice but to call `functions/efron_1979_bootstrap.py` through `registry.invoke(fn_cid, ...)` rather than reimplementing or merely linking to it — a real, working two-hop citation.

## Davison & Hinkley (1997) — the same move, one level up

Even BCa's stated 95% confidence is only approximately accurate, since `z0` and `a` are themselves estimated with error. The double bootstrap's answer: **treat the entire BCa procedure as a thing to be tested by resampling too.** Resample the data again at an "outer" level, and for each outer resample, rerun the *whole* BCa machinery — which means rerunning the 1979 bootstrap inside it — to see how much the BCa interval's own edges jump around. That spread-of-spreads calibrates a final, wider interval: more conservative, and more honest, because it accounts for uncertainty in the bias-correction itself. This is `functions/davison_hinkley_1997_double_bootstrap.py`, invoking the 1993 code, which invokes the 1979 code.

## The invocation log is the receipt for all of the above

When you run this, `registry.py`'s call log shows exactly how many times each paper's code actually executed — not a diagram of what *should* happen. A typical run: the 1993 code invoked ~61 times (once directly, plus once per outer resample), and the 1979 code invoked an equal number of times underneath *that*. The final interval is wider than the plain BCa interval specifically *because* of that real, logged, extra computation — not because the code asserts it should be.

## Why this is a different claim than a normal citation makes

A conventional citation to Davison & Hinkley (1997) asks you to trust that a citing work correctly implements a method described in a book — verifiable only by independently obtaining the source and re-deriving it yourself. Here the dependency is executed, not asserted: the double-bootstrap's output is provably a function of the BCa output, which is provably a function of the plain bootstrap output, on data of your choosing, with a call log as evidence. The citation doesn't describe what happened. It *is* what happened.

---

## What this actually proves, structurally

Three real functions, each mapping to a real paper:

- `functions/efron_1979_bootstrap.py` — Efron (1979), "Bootstrap Methods: Another Look at the Jackknife."
- `functions/efron_tibshirani_1993_bca.py` — Efron & Tibshirani (1993), *An Introduction to the Bootstrap*, BCa intervals. **Cites the 1979 code by invoking it through `registry.invoke(fn_cid, ...)`, not by reimplementing it or linking to it.**
- `functions/davison_hinkley_1997_double_bootstrap.py` — Davison & Hinkley (1997), *Bootstrap Methods and Their Application*. Cites the 1993 code the same way, producing a real two-hop chain.

`registry.py` is a deliberately toy stand-in for the Custodian's `resolve()`/`record_invocation()` path — content-addressed lookup by `fn_cid`, with `MAX_INVOCATION_DEPTH` enforced exactly as specified in the platform spec's §4.4. Running the demo against a synthetic dataset (not any paper's original data) and printing the invocation log is the actual test of the mechanism, with an assertion suite checked at the end.

## What's honestly still missing before this is the real thing

- **Pydantic vs. dataclasses:** this repo's native version uses `@dataclass` + `__post_init__` validation; a Pydantic-upgraded version exists (see the `pydantic_upgrade` patch applied earlier) matching the contract shape exactly (typed input, typed output, validated preconditions).
- **Native Python vs. Pyodide:** this folder proves the *invocation mechanism* — CID lookup, cross-document call, depth limit — is real and correct. The browser-native, zero-install version proving the actual portability claim lives at `docs/resampling_knot_browser_v3.html`, running the same logic compiled to WASM.
- **`fn_cid` values are literal strings, not real content hashes.** The real system hashes the function's code + schema; here they're readable placeholders for demo clarity.

## Rubric application

Both citations here — 1993 citing 1979, 1997 citing 1993 — pass Stage 1 of the invocability rubric (E1: genuine Method/Uses, since deleting either citation changes the reported numbers; E2: pure stdlib, no GPU, no threading, trivial memory) at Q1=2/Q2=2, by the same reasoning as Worked Example A in `citation_invocability_rubric_v0.1.md`. This knot was built first specifically because it should score cleanly — see that file for the harder cases (multiple-testing, dimensionality-reduction) in the build queue.