"""
Node C of the meta-analysis lineage -- Pydantic version.
Higgins, J.P.T. & Thompson, S.G. (2002). "Quantifying Heterogeneity in a Meta-Analysis."
"""
from pydantic import BaseModel
from typing import List

from registry import REGISTRY
from functions.dersimonian_laird_1986 import FN_CID as DL_FN_CID, RandomEffectsInput
from functions.cochran_1954 import Study

FN_CID = "bafy_higgins_thompson_2002_i_squared_v1"
PYODIDE_PACKAGES: List[str] = []
COMPUTE_CLASS = "cpu_only"
MEMORY_HINT_MB = 64


def _declare_edges():
    REGISTRY.register_cites(FN_CID, {
        DL_FN_CID: {
            "edge_type": "cito:usesMethodIn",
            "tier": 0,
            "proof_method": "executable_invocation",
            "confidence": "verified",
        }
    })


class HeterogeneityInput(BaseModel):
    studies: List[Study]


class HeterogeneityOutput(BaseModel):
    i_squared_pct: float
    q_statistic: float
    k: int
    interpretation: str


def heterogeneity_i2(payload: HeterogeneityInput, depth: int = 0) -> HeterogeneityOutput:
    base = REGISTRY.invoke(
        DL_FN_CID,
        RandomEffectsInput(studies=payload.studies),
        depth=depth + 1,
        source_fn_cid=FN_CID,
    )

    i_squared = max(0.0, (base.q_statistic - (base.k - 1)) / base.q_statistic) * 100 \
        if base.q_statistic != 0 else 0.0

    if i_squared < 25:
        interp = "low heterogeneity -- studies broadly agree"
    elif i_squared < 50:
        interp = "moderate heterogeneity"
    elif i_squared < 75:
        interp = "substantial heterogeneity -- pooling should be interpreted cautiously"
    else:
        interp = "considerable heterogeneity -- pooling a single estimate may be misleading"

    return HeterogeneityOutput(
        i_squared_pct=i_squared,
        q_statistic=base.q_statistic,
        k=base.k,
        interpretation=interp,
    )
