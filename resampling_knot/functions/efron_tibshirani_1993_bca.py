"""
Node B of the resampling knot -- Pydantic version.
Efron, B. & Tibshirani, R. (1993). An Introduction to the Bootstrap.
"""
from pydantic import BaseModel, field_validator
from typing import List
import random
import math

from registry import REGISTRY
from functions.efron_1979_bootstrap import FN_CID as EFRON_1979_FN_CID, BootstrapSEInput


class BCaInput(BaseModel):
    data: List[float]
    ci_level: float = 0.95
    n_resamples: int = 10_000
    seed: int = 0

    @field_validator("data")
    @classmethod
    def min_observations(cls, v):
        if len(v) < 5:
            raise ValueError("BCa needs at least 5 observations for a stable jackknife")
        return v

    @field_validator("ci_level")
    @classmethod
    def valid_ci_level(cls, v):
        if not (0.5 < v < 1.0):
            raise ValueError("ci_level must be between 0.5 and 1.0")
        return v


class BCaOutput(BaseModel):
    point_estimate: float
    ci_lower: float
    ci_upper: float
    bias_correction_z0: float
    acceleration_a: float
    n_resamples_used: int


FN_CID = "bafy_efron_tibshirani_1993_bca_v1"
PYODIDE_PACKAGES: List[str] = []
COMPUTE_CLASS = "cpu_only"
MEMORY_HINT_MB = 96
CITES = {EFRON_1979_FN_CID: "imports"}


def _jackknife_acceleration(data: List[float]) -> float:
    n = len(data)
    loo_means = [sum(data[:i] + data[i + 1:]) / (n - 1) for i in range(n)]
    mean_loo = sum(loo_means) / n
    num = sum((mean_loo - x) ** 3 for x in loo_means)
    den = 6.0 * (sum((mean_loo - x) ** 2 for x in loo_means) ** 1.5)
    return num / den if den != 0 else 0.0


def _norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _norm_ppf(p: float) -> float:
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    p_low = 0.02425
    if p < p_low:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    elif p <= 1 - p_low:
        q = p - 0.5
        r = q * q
        return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
               (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    else:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)


def bca_interval(payload: BCaInput, depth: int = 1) -> BCaOutput:
    base = REGISTRY.invoke(
        EFRON_1979_FN_CID,
        BootstrapSEInput(data=payload.data, n_resamples=payload.n_resamples, seed=payload.seed),
        depth=depth + 1,
    )

    rng = random.Random(payload.seed)
    n = len(payload.data)
    boot_means = sorted(
        sum(payload.data[rng.randrange(n)] for _ in range(n)) / n
        for _ in range(payload.n_resamples)
    )

    proportion_below = sum(1 for m in boot_means if m < base.point_estimate) / len(boot_means)
    proportion_below = min(max(proportion_below, 1e-6), 1 - 1e-6)
    z0 = _norm_ppf(proportion_below)
    a = _jackknife_acceleration(payload.data)

    alpha = 1 - payload.ci_level
    z_lo = _norm_ppf(alpha / 2)
    z_hi = _norm_ppf(1 - alpha / 2)

    def adjusted_percentile(z):
        return _norm_cdf(z0 + (z0 + z) / (1 - a * (z0 + z)))

    p_lo = adjusted_percentile(z_lo)
    p_hi = adjusted_percentile(z_hi)
    idx_lo = max(0, min(len(boot_means) - 1, int(p_lo * len(boot_means))))
    idx_hi = max(0, min(len(boot_means) - 1, int(p_hi * len(boot_means))))

    return BCaOutput(
        point_estimate=base.point_estimate,
        ci_lower=boot_means[idx_lo],
        ci_upper=boot_means[idx_hi],
        bias_correction_z0=z0,
        acceleration_a=a,
        n_resamples_used=payload.n_resamples,
    )
