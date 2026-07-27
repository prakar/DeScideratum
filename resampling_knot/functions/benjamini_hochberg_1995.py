"""
Node A of the multiple-testing knot.
Benjamini, Y. & Hochberg, Y. (1995). "Controlling the False Discovery Rate:
A Practical and Powerful Approach to Multiple Testing." JRSS-B, 57(1), 289-300.

Rubric verdict (see citation_invocability_rubric_v0.1.md):
E1 PASS -- any citing paper applying BH correction to its own p-values is
running this exact procedure on new data; deleting the citation changes
the citing paper's reported significance calls.
E2 PASS -- pure sorting/arithmetic, no GPU, no threading, trivial memory.
"""
from dataclasses import dataclass
from typing import List

FN_CID = "bafy_benjamini_hochberg_1995_bh_v1"
PYODIDE_PACKAGES: List[str] = []
COMPUTE_CLASS = "cpu_only"
MEMORY_HINT_MB = 64


@dataclass
class BHInput:
    pvalues: List[float]
    alpha: float = 0.05

    def __post_init__(self):
        if len(self.pvalues) < 1:
            raise ValueError("need at least one p-value")
        if any(p < 0 or p > 1 for p in self.pvalues):
            raise ValueError("p-values must be in [0, 1]")
        if not (0 < self.alpha < 1):
            raise ValueError("alpha must be in (0, 1)")


@dataclass
class BHOutput:
    rejected: List[bool]          # same order as input
    adjusted_pvalues: List[float]  # same order as input
    n_significant: int


def bh_adjust(payload: BHInput) -> BHOutput:
    m = len(payload.pvalues)
    indexed = sorted(range(m), key=lambda i: payload.pvalues[i])
    sorted_p = [payload.pvalues[i] for i in indexed]

    # BH adjusted p-values: cumulative minimum from the largest rank down
    adjusted_sorted = [0.0] * m
    adjusted_sorted[m - 1] = sorted_p[m - 1]
    for k in range(m - 2, -1, -1):
        candidate = sorted_p[k] * m / (k + 1)
        adjusted_sorted[k] = min(candidate, adjusted_sorted[k + 1])
        adjusted_sorted[k] = min(adjusted_sorted[k], 1.0)

    # largest k such that sorted_p[k] <= (k+1)/m * alpha  (0-indexed)
    largest_k = -1
    for k in range(m):
        threshold = (k + 1) / m * payload.alpha
        if sorted_p[k] <= threshold:
            largest_k = k

    rejected_sorted = [i <= largest_k for i in range(m)]

    # map back to original order
    rejected = [False] * m
    adjusted = [0.0] * m
    for pos, orig_i in enumerate(indexed):
        rejected[orig_i] = rejected_sorted[pos]
        adjusted[orig_i] = adjusted_sorted[pos]

    return BHOutput(
        rejected=rejected,
        adjusted_pvalues=adjusted,
        n_significant=sum(rejected),
    )
