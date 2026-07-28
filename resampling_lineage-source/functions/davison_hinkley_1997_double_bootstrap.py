"""
Node C of the resampling knot -- Pydantic version.
Davison, A.C. & Hinkley, D.V. (1997). Bootstrap Methods and Their Application.
"""
from pydantic import BaseModel, field_validator
from typing import List
import random

from registry import REGISTRY
from functions.efron_tibshirani_1993_bca import FN_CID as BCA_FN_CID, BCaInput


class DoubleBootstrapInput(BaseModel):
    data: List[float]
    ci_level: float = 0.95
    n_resamples: int = 2_000
    seed: int = 0

    @field_validator("data")
    @classmethod
    def min_observations(cls, v):
        if len(v) < 5:
            raise ValueError("needs at least 5 observations")
        return v

    @field_validator("n_resamples")
    @classmethod
    def bounded_cost(cls, v):
        if v > 5_000:
            raise ValueError(
                "double bootstrap is O(n_resamples^2) work -- capped to keep "
                "this within a sane browser-tab time budget"
            )
        return v


class DoubleBootstrapOutput(BaseModel):
    point_estimate: float
    ci_lower_calibrated: float
    ci_upper_calibrated: float
    inner_bca_ci_lower: float
    inner_bca_ci_upper: float
    outer_resamples_used: int


FN_CID = "bafy_davison_hinkley_1997_double_bootstrap_v1"
PYODIDE_PACKAGES: List[str] = []
COMPUTE_CLASS = "cpu_only"
MEMORY_HINT_MB = 256
CITES = {BCA_FN_CID: "imports"}


def double_bootstrap_ci(payload: DoubleBootstrapInput, depth: int = 0) -> DoubleBootstrapOutput:
    inner = REGISTRY.invoke(
        BCA_FN_CID,
        BCaInput(data=payload.data, ci_level=payload.ci_level,
                 n_resamples=max(500, payload.n_resamples // 4), seed=payload.seed),
        depth=depth + 1,
    )

    rng = random.Random(payload.seed + 1)
    n = len(payload.data)
    outer_lowers, outer_uppers = [], []
    for _ in range(payload.n_resamples):
        resample = [payload.data[rng.randrange(n)] for _ in range(n)]
        outer_inner = REGISTRY.invoke(
            BCA_FN_CID,
            BCaInput(data=resample, ci_level=payload.ci_level,
                     n_resamples=200, seed=rng.randrange(1_000_000)),
            depth=depth + 1,
        )
        outer_lowers.append(outer_inner.ci_lower)
        outer_uppers.append(outer_inner.ci_upper)

    outer_lowers.sort()
    outer_uppers.sort()
    calibrated_lo = outer_lowers[int(0.025 * len(outer_lowers))]
    calibrated_hi = outer_uppers[int(0.975 * len(outer_uppers)) - 1]

    return DoubleBootstrapOutput(
        point_estimate=inner.point_estimate,
        ci_lower_calibrated=calibrated_lo,
        ci_upper_calibrated=calibrated_hi,
        inner_bca_ci_lower=inner.ci_lower,
        inner_bca_ci_upper=inner.ci_upper,
        outer_resamples_used=payload.n_resamples,
    )
