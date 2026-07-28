# Verification Ontology for Scholarly Dependencies — v0.3
### Accretive synthesis: original rubric + Gemini + Grok + ChatGPT rounds

**Reframed thesis (adopted from the ChatGPT round, the sharpest formulation reached across four rounds):**

> CiTO already provides a mature vocabulary for *what relationship* a citation expresses. RO-Crate and nanopublications already model *what scholarly objects exist*. PROV-O already models *how artifacts were produced*. The remaining gap is orthogonal to all three: **how do we verify that a claimed relationship actually holds, and what level of evidence is appropriate for that verification?**

This is narrower than the original "citation is invocation" framing — and more defensible for exactly that reason. The project's contribution is a **verification layer**, not a replacement ontology.

---

## Part 1 — Coverage matrix (source: ChatGPT round, lightly reformatted)

| Capability | CiTO | RO-Crate / RO | Nanopub | PROV-O | This project |
|---|---|---|---|---|---|
| Typed citation relationships | ✓ | — | Partial | Partial | ✓ (reuses CiTO) |
| Paper decomposed into scholarly objects | — | ✓ | ✓ | — | ✓ (reuses RO-Crate/nanopub) |
| Provenance chain | Partial | Partial | Partial | ✓ | ✓ (reuses PROV-O) |
| Executable methods | ✗ | Partial (references only) | ✗ | ✗ | ✓ |
| Runtime invocation | ✗ | ✗ | ✗ | ✗ | ✓ |
| Invocation evidence (call log) | ✗ | ✗ | ✗ | ✗ | ✓ |
| **Verification obligations per relationship** | ✗ | ✗ | ✗ | ✗ | **target contribution** |
| Applicability constraints (Vogt) | ✗ | Partial | Partial | Partial | planned (Part 3) |

Row 7 is the paper's actual novelty claim. Everything else in the table is "reuse an existing standard," stated as such — that's a strength, not a hedge.

---

## Part 2 — The layered model

```
Layer 1 (WHY cited):        CiTO relationship type          e.g. cito:usesMethodIn
Layer 2 (WHAT is cited):    RO-Crate / nanopub object type    e.g. Method, Observation, Dataset
Layer 3 (HOW it was made):  PROV-O provenance chain           e.g. prov:wasGeneratedBy
Layer 4 (IS IT VALID HERE): Applicability Profile (Part 3)    e.g. population, conditions, version
Layer 5 (CAN WE CHECK IT):  Proof Obligation tier (Part 4)    e.g. Tier 0 invocation log, Tier 3 conformance tests
```

Layers 1–3 are adopt-don't-invent. Layers 4–5 are the actual research contribution.

---

## Part 3 — Applicability Profile (source: ChatGPT round, operationalizing Vogt's actionability/applicability distinction)

Every scholarly object that carries empirical content (not just executable functions) gets:

```yaml
applicability_profile:
  population: <who/what this was measured on or applies to>
  assumptions: <what must hold for this to be valid>
  measurement_conditions: <pH, temperature, dataset version, instrument, etc.>
  version: <content hash or semantic version of the exact artifact>
  dependencies: <upstream objects this assumes>
  known_failure_modes: <documented conditions under which this breaks>
```

This is what separates the corrected Bayesian-evidence-node idea (Gemini round, corrected: closed-form conjugate update, new CID per update rather than silent propagation) from a bare number — an effect size without an applicability profile is not safely invocable even if it's numerically well-typed.

---

## Part 4 — Proof Obligation tiers (source: ChatGPT round, verified sound; this is the core contribution)

| Tier | Relationship | Evidence | Difficulty | Status |
|---|---|---|---|---|
| 0 | `EXECUTES` | invocation log, hash, arguments, timestamp | Solved | **Already built** — resampling & multiple-testing knots |
| 1 | `RESOLVES_TO`, `VERSION_OF` | content hash, semantic version, hash ancestry | Easy | "Equivalent to Git" |
| 2 | `USES_DATASET`, `USES_MODEL` | dataset/subset/manifest hash; model/weights hash, prompt, runtime | Moderate | Emerging practice in ML reproducibility (model cards, dataset cards) |
| 3 | `IMPLEMENTS`, `REPRODUCES` | conformance tests, property-based testing, reference-implementation equivalence, statistical equivalence within tolerance | Hard | `IMPLEMENTS` bounded by Rice's theorem — no general algorithm decides semantic equivalence of arbitrary programs; only restricted languages, formal specs, or proof assistants give stronger guarantees. `REPRODUCES` is graded, not binary. |
| 4 | `VALIDATES`, `GENERALIZES`, `EXPLAINS` | scientific judgment, replication, meta-analysis, expert consensus | Very high | Essentially epistemology — no universally accepted mechanical proof exists, and this is stated as a feature of the model, not a bug to fix later |
| 5 | `CITES_AS_AUTHORITY`, `PROVIDES_BACKGROUND`, `MOTIVATES` | — | N/A | Cannot be mechanically proven; requires community judgment; maps directly onto Moravcsik & Murugesan's ~40% perfunctory-citation finding |

**Design rule carried through every round:** a relationship's tier is a property of what kind of claim it is, not something to be argued up by clever engineering. Tier 4/5 staying manual is the model working correctly, the same way Tier 0 being fully automatic is.

---

## Part 5 — Manifest schema update

The existing `FunctionHook.CITES` field (`{fn_cid: "imports"}`) is replaced with a structured edge object using CiTO vocabulary for the relationship type and the tier table for the proof obligation:

```yaml
edge:
  type: cito:usesMethodIn        # was the private "imports" string — now interoperable with CiTO
  target: bafy_efron1979_bootstrap_se_v1
  proof:
    method: executable_invocation
    confidence: verified
    tier: 0
```

```yaml
edge:
  type: cito:citesAsEvidence     # non-invocable, typed provenance claim — new capability
  target: nanopub:smith_2018_ic50
  applicability_profile:
    population: "Receptor Y, in vitro"
    measurement_conditions: {pH: 7.4, temp_c: 37}
  proof:
    method: none
    confidence: unverified
    tier: 5
```

Both forms coexist in one manifest. The old binary "invocable or not" rubric outcome is now a **five-tier classification with an explicit proof method per tier**, not a pass/fail gate.

---

## Part 6 — Provenance of every idea in this document, so nothing gets flattened into "ours"

- **CiTO** (Shotton, 2010) — relationship vocabulary. Verified real, production-used by OpenCitations; adoption in publishing broadly is narrow (one journal pilot), not widespread — cite accurately.
- **Nanopublications** (Groth et al., 2010) and **RO-Crate** — object decomposition ("paper as container"). Already in the project's own novelty search before Gemini/Grok/ChatGPT were consulted.
- **PROV-O** (W3C) — provenance chains.
- **Vogt** (arXiv 2605.01564, May 2026) — actionability/applicability distinction, operationalized here as the Applicability Profile.
- **Gemini round** — Bayesian evidence-node concept (adopted, corrected: closed-form conjugate math not PyMC/Stan; versioned re-citation not silent propagation). Z3/OWL and GNN-oracle proposals rejected with reasons on file.
- **Grok round** — nanopub/CiTO as the right non-executable shape (adopted); GraphQL-as-query-not-model correction (adopted).
- **ChatGPT round** — the reframed thesis, the coverage matrix, the six-example gap audit, the Applicability Profile schema, and the tiered Proof Obligation table. This is the load-bearing contribution of this version.
- **This project's own prior work** — the resampling and multiple-testing knots are the existing, working Tier 0 proof.

---

## Part 7 — What's still open

1. `obtainsBackgroundFrom` and other specific CiTO term names used in the gap audit need a direct check against CiTO's published term list before the manuscript cites them as confirmed.
2. Datalog for inferring `EXECUTION_DEPENDS_ON`-style derived edges (ChatGPT round) — plausible, likely runnable as plain JS without Pyodide, not yet verified hands-on.
3. No knot yet exercises Tier 2 (`USES_DATASET`/`USES_MODEL`) or the Applicability Profile in working code — natural candidate: the parameter/evidence knot already queued from the Gemini round, rebuilt against this corrected schema.
4. Tier 3's `REPRODUCES` ("statistical equivalence within tolerance") needs an actual tolerance-setting methodology before it's implementable, not just named.
