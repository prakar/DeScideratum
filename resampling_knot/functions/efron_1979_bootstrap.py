"""
Node A of the resampling knot -- Pydantic version.
Efron, B. (1979). "Bootstrap Methods: Another Look at the Jackknife."
Annals of Statistics, 7(1), 1-26.
"""
from pydantic import BaseModel, field_validator
from typing import List
import random
import math


class BootstrapSEInput(BaseModel):
    data: List[float]
    n_resamples: int = 10_000
    seed: int = 0

    @field_validator("data")
    @classmethod
    def min_observations(cls, v):
        if len(v) < 3:
            raise ValueError("need at least 3 observations")
        return v

    @field_validator("n_resamples")
    @classmethod
    def min_resamples(cls, v):
        if v < 100:
            raise ValueError("n_resamples must be at least 100 for a stable estimate")
        return v


class BootstrapSEOutput(BaseModel):
    point_estimate: float
    se: float
    n_resamples_used: int


FN_CID = "bafy_efron1979_bootstrap_se_v1"
PYODIDE_PACKAGES: List[str] = []
COMPUTE_CLASS = "cpu_only"
MEMORY_HINT_MB = 64


def bootstrap_se(payload: BootstrapSEInput) -> BootstrapSEOutput:
    rng = random.Random(payload.seed)
    data = payload.data
    n = len(data)
    point_estimate = sum(data) / n

    resample_means = []
    for _ in range(payload.n_resamples):
        resample = [data[rng.randrange(n)] for _ in range(n)]
        resample_means.append(sum(resample) / n)

    mean_of_means = sum(resample_means) / len(resample_means)
    variance = sum((m - mean_of_means) ** 2 for m in resample_means) / (len(resample_means) - 1)
    se = math.sqrt(variance)

    return BootstrapSEOutput(
        point_estimate=point_estimate,
        se=se,
        n_resamples_used=payload.n_resamples,
    )
