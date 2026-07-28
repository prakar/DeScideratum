"""
Node A of the meta-analysis lineage -- Pydantic version.
Cochran, W.G. (1954). "The Combination of Estimates from Different Experiments."
"""
from pydantic import BaseModel, field_validator
from typing import List

FN_CID = "bafy_cochran_1954_fixed_effect_v1"
PYODIDE_PACKAGES: List[str] = []
COMPUTE_CLASS = "cpu_only"
MEMORY_HINT_MB = 64


class ApplicabilityProfile(BaseModel):
    population: str = ""
    measurement_conditions: str = ""
    known_failure_modes: str = ""


class Study(BaseModel):
    label: str
    estimate: float
    se: float
    applicability: ApplicabilityProfile = ApplicabilityProfile()

    @field_validator("se")
    @classmethod
    def se_positive(cls, v):
        if v <= 0:
            raise ValueError("standard error must be positive")
        return v


class FixedEffectInput(BaseModel):
    studies: List[Study]

    @field_validator("studies")
    @classmethod
    def min_studies(cls, v):
        if len(v) < 2:
            raise ValueError("need at least 2 studies to pool")
        return v


class FixedEffectOutput(BaseModel):
    pooled_estimate: float
    pooled_se: float
    q_statistic: float
    k: int
    weights: List[float]


def fixed_effect_pool(payload: FixedEffectInput) -> FixedEffectOutput:
    studies = payload.studies
    k = len(studies)
    weights = [1.0 / (s.se ** 2) for s in studies]
    sum_w = sum(weights)
    pooled_estimate = sum(w * s.estimate for w, s in zip(weights, studies)) / sum_w
    pooled_se = (1.0 / sum_w) ** 0.5
    q_statistic = sum(w * (s.estimate - pooled_estimate) ** 2 for w, s in zip(weights, studies))

    return FixedEffectOutput(
        pooled_estimate=pooled_estimate,
        pooled_se=pooled_se,
        q_statistic=q_statistic,
        k=k,
        weights=weights,
    )
