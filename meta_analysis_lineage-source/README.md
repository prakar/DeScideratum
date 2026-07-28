# The meta-analysis lineage — pooling evidence, with the conditions attached

Three papers, thirty-plus years apart, on the problem of combining several independent estimates into one. This folder is the working code; [`docs/meta-analysis-lineage/index.html`](../docs/meta-analysis-lineage/index.html) is the same thing running zero-install in a browser, with a plain-language walkthrough and a full glossary.

Run: `python3 run_demo.py`

Sibling lineages: `../resampling_lineage-source/` and `../multiple_testing_lineage-source/`. All three are linked from `docs/index.html`.

## Terminology note, stated once so it doesn't drift

This lineage's citations are **Tier 0** (`cito:usesMethodIn`, verified via invocation log) — the exact same evidentiary category as the resampling and multiple-testing lineages. It is *separately*, and independently, the **first lineage where the Applicability Profile field carries real data** — each input study declares the conditions under which its estimate holds. Tier and Applicability Profile are two different axes; this lineage doesn't sit at a "higher tier" for exercising the second one.

## The problem all three papers are answering a piece of

You have several independent estimates of the same underlying quantity — five studies' effect sizes, say. None of them alone is fully trustworthy; some are more precise than others; they may not even agree with each other. How do you combine them into one number, honestly?

## Cochran (1954) — the base case

Weight each study's estimate by the inverse of its variance (`1/se²`) — more precise studies (smaller SE) count for more — and take the weighted average. This is inverse-variance pooling, the foundational method, implemented in `functions/cochran_1954.py`. It also computes **Cochran's Q**, a statistic measuring how much the studies disagree with each other — needed downstream by both later papers.

## DerSimonian & Laird (1986) — random effects, and why it cannot run without Cochran's code

Cochran's method assumes every study is estimating the exact same true effect, just with different precision. DerSimonian & Laird's insight: studies often differ for real reasons (different populations, protocols, conditions) — there's a genuine *between-study* variance, called **τ² (tau-squared)**, on top of each study's own uncertainty. Their method-of-moments estimator for τ² is defined directly in terms of Cochran's Q statistic, the study count, and the fixed-effect weights — **there is no way to compute it without those already existing.** `functions/dersimonian_laird_1986.py` calls `functions/cochran_1954.py` through `registry.invoke(fn_cid, ...)` for exactly this reason — a real, structural, two-hop-capable citation, one of the most-cited papers in medical statistics.

## Higgins & Thompson (2002) — quantifying how much the studies actually disagree

**I²** turns Q into a percentage: what fraction of the total variation across studies is real disagreement rather than each study's own sampling noise. Built directly on the same Q and study count DerSimonian-Laird already needed — `functions/higgins_thompson_2002.py` invokes the 1986 code (not the 1954 code directly) specifically so the I² reported is guaranteed consistent with whatever random-effects estimate is reported alongside it, rather than being recomputed independently and risking drift.

## What's new here, concretely, beyond a third working chain

Every input `Study` carries a real `ApplicabilityProfile` — `population`, `measurement_conditions`, `known_failure_modes` — populated with actual (illustrative/synthetic) data, not just described in a spec. This is the first lineage to exercise that part of the v0.3 schema in working code rather than prose.

The demo also asserts something the first two lineages didn't test: that **Node C's Q statistic, arrived at via two real hops, is bit-identical to Node A's original Q.** That's a stronger claim than "the citation happened" — it's "the value survived two hops of real computation unchanged," which is the actual content-addressing promise being tested, not just its mechanism.

## Honest caveats

- **Illustrative data, not real trial data.** The five studies are synthetic, clearly labeled as such — consistent with how the other two lineages use a reader's own numbers rather than any paper's actual dataset. No specific real trial's numbers are claimed here.
- **Why these three papers specifically** is not yet justified in writing anywhere in this project — flagged as an open item for the manuscript, since a reviewer will reasonably ask.
- **Pydantic: delivered for this lineage** (`BaseModel` + `field_validator`, matching the resampling lineage's status) — **still outstanding for the multiple-testing lineage**, which remains dataclass-only. Not yet consistent across all three.
- **Pydantic and Pyodide are parallel, unmerged tracks, for every lineage so far — including this one.** The browser page at `docs/meta-analysis-lineage/index.html` runs plain Python dicts inside Pyodide, matching the *original* dataclass logic, not the Pydantic version delivered above. Running Pydantic itself inside Pyodide would need `micropip.install('pydantic')` at page-load time — untested, not yet attempted for any lineage.
- **`fn_cid` values are literal strings, not real content hashes**, same as the other two.

## Rubric application

Both citations here pass Stage 1 (E1: deleting either changes a real reported number — Node B's tau², Node C's I²; E2: pure arithmetic, no exotic dependencies) at Q1=2/Q2=2. `cito:usesMethodIn` at Tier 0, same as the resampling lineage's worked example. See `citation_invocability_rubric_v0.1.md` and `verification_ontology_v0.3_synthesis.md` for the full instrument.
