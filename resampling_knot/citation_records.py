"""
Rubric verdicts for every citation in this knot, applied and stated
explicitly -- including the one that fails on purpose.

This module deliberately contains NO callable function for
Benjamini & Yekutieli (2001). That is the point of this knot: proving
the invocability rubric produces honest negatives, not just wins.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RubricVerdict:
    citation: str
    year: int
    cited_by_relationship: str
    e1_intent: str            # "PASS" or "FAIL"
    e1_reasoning: str
    e2_portability: Optional[str] = None   # None if E1 already failed -- not scored further
    e2_reasoning: Optional[str] = None
    fn_cid: Optional[str] = None
    verdict: str = ""

    def __post_init__(self):
        if self.e1_intent == "PASS":
            self.verdict = "BROWSER-INVOCABLE" if self.e2_portability == "PASS" else "NOT INVOCABLE (E2 fail)"
        else:
            self.verdict = "NOT INVOCABLE (E1 fail) -- remains a conventional citation"


CITATION_RECORDS: List[RubricVerdict] = [
    RubricVerdict(
        citation="Benjamini & Hochberg (1995), 'Controlling the False Discovery Rate'",
        year=1995,
        cited_by_relationship="base case -- no citation dependency",
        e1_intent="PASS",
        e1_reasoning="Any paper applying BH correction to its own p-values is running "
                      "this exact procedure on new data; deleting the citation changes "
                      "the citing paper's reported significance calls.",
        e2_portability="PASS",
        e2_reasoning="Pure sorting/arithmetic. No GPU, no threading, trivial memory at "
                      "any realistic input size.",
        fn_cid="bafy_benjamini_hochberg_1995_bh_v1",
    ),
    RubricVerdict(
        citation="Storey (2002), 'A Direct Approach to False Discovery Rates'",
        year=2002,
        cited_by_relationship="cites BH (1995) by invoking it for a comparison baseline",
        e1_intent="PASS",
        e1_reasoning="Storey's q-value procedure genuinely runs BH's rejection rule as "
                      "part of its own reported output (naive_bh_n_significant); deleting "
                      "the BH citation removes a real number from this function's output, "
                      "not just an argument.",
        e2_portability="PASS",
        e2_reasoning="Fixed-lambda pi0 estimator + monotone q-value construction, "
                      "stdlib-only, no exotic dependencies.",
        fn_cid="bafy_storey_2002_qvalue_v1",
    ),
    RubricVerdict(
        citation="Benjamini & Yekutieli (2001), 'The Control of the False Discovery Rate "
                  "in Multiple Testing under Dependency'",
        year=2001,
        cited_by_relationship="cited by a hypothetical paper applying BH to CORRELATED "
                               "tests, to justify that FDR control still holds",
        e1_intent="FAIL",
        e1_reasoning="This citation is to B&Y's PROOF that FDR control extends to "
                      "positive regression dependence (PRDS) -- the citing paper is "
                      "invoking a mathematical property, not running a function on data. "
                      "Deleting this citation would change the citing paper's ARGUMENT "
                      "for why its BH usage is valid under dependency, not any reported "
                      "number. This is the diagnostic that separates Method/Uses from "
                      "Critique/Extends, applied honestly rather than skipped.",
    ),
]


def print_rubric_table():
    print("=" * 78)
    print("Rubric verdicts applied to this knot's citations")
    print("=" * 78)
    for rec in CITATION_RECORDS:
        print(f"\n{rec.citation}")
        print(f"  relationship: {rec.cited_by_relationship}")
        print(f"  E1 (intent):       {rec.e1_intent} -- {rec.e1_reasoning}")
        if rec.e2_portability:
            print(f"  E2 (portability):  {rec.e2_portability} -- {rec.e2_reasoning}")
        print(f"  VERDICT: {rec.verdict}")
    print("\n" + "=" * 78)
