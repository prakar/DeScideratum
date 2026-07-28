"""
Node B of the meta-analysis lineage -- Pydantic version.
DerSimonian, R. & Laird, N. (1986). "Meta-analysis in Clinical Trials."
"""
from pydantic import BaseModel
from typing import List

from registry import REGISTRY
from functions.cochran_1954 import FN_CID as COCHRAN_FN_CID, FixedEffectInput, Study

FN_CID = "bafy_dersimonian_laird_1986_random_effects_v1"
PYODIDE_PACKAGES: List[str] = []
COMPUTE_CLASS = "cpu_only"
MEMORY_HINT_MB = 64


def _declare_edges():
    REGISTRY.register_cites(FN_CID, {
        COCHRAN_FN_CID: {
            "edge_type": "cito:usesMethodIn",
            "tier": 0,
            "proof_method": "executable_invocation",
            "confidence": "verified",
        }
    })


class RandomEffectsInput(BaseModel):
    studies: List[Study]


class RandomEffectsOutput(BaseModel):
    pooled_estimate: float
    pooled_se: float
    tau_squared: float
    q_statistic: float
    k: int


def random_effects_pool(payload: RandomEffectsInput, depth: int = 1) -> RandomEffectsOutput:
    base = REGISTRY.invoke(
        COCHRAN_FN_CID,
        FixedEffectInput(studies=payload.studies),
        depth=depth + 1,
        source_fn_cid=FN_CID,
    )

    weights = base.weights
    sum_w = sum(weights)
    sum_w2 = sum(w ** 2 for w in weights)
    c = sum_w - (sum_w2 / sum_w)

    tau_squared = max(0.0, (base.q_statistic - (base.k - 1)) / c) if c != 0 else 0.0

    re_weights = [1.0 / (s.se ** 2 + tau_squared) for s in payload.studies]
    sum_rw = sum(re_weights)
    pooled_estimate = sum(w * s.estimate for w, s in zip(re_weights, payload.studies)) / sum_rw
    pooled_se = (1.0 / sum_rw) ** 0.5

    return RandomEffectsOutput(
        pooled_estimate=pooled_estimate,
        pooled_se=pooled_se,
        tau_squared=tau_squared,
        q_statistic=base.q_statistic,
        k=base.k,
    )
