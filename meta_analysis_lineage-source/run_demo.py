"""
Registers the meta-analysis lineage and runs the full chain:
  Higgins & Thompson (2002) --invokes--> DerSimonian & Laird (1986) --invokes--> Cochran (1954)

The five "studies" below are illustrative/synthetic -- stand-ins for a
reader's own data, exactly like the resampling and multiple-testing
lineages use synthetic numbers, not a claim about any real trial.

Run with: python3 run_demo.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from registry import REGISTRY
from functions.cochran_1954 import (
    fixed_effect_pool, FN_CID as A_CID, FixedEffectInput, Study, ApplicabilityProfile,
)
from functions.dersimonian_laird_1986 import (
    random_effects_pool, FN_CID as B_CID, RandomEffectsInput, _declare_edges as _declare_b_edges,
)
from functions.higgins_thompson_2002 import (
    heterogeneity_i2, FN_CID as C_CID, HeterogeneityInput, _declare_edges as _declare_c_edges,
)

REGISTRY.register(A_CID, fixed_effect_pool)
REGISTRY.register(B_CID, random_effects_pool)
REGISTRY.register(C_CID, heterogeneity_i2)
_declare_b_edges()  # DerSimonian-Laird --cito:usesMethodIn(tier 0)--> Cochran
_declare_c_edges()  # Higgins-Thompson --cito:usesMethodIn(tier 0)--> DerSimonian-Laird


def main():
    # illustrative/synthetic studies -- each carries a real Applicability
    # Profile, the actual new thing this lineage tests
    studies = [
        Study("Study 1", estimate=0.42, se=0.08,
              applicability=ApplicabilityProfile(
                  population="adults, urban clinic",
                  measurement_conditions="6-week follow-up",
                  known_failure_modes="high dropout in original sample")),
        Study("Study 2", estimate=0.35, se=0.10,
              applicability=ApplicabilityProfile(
                  population="adults, rural clinic",
                  measurement_conditions="6-week follow-up")),
        Study("Study 3", estimate=0.51, se=0.09,
              applicability=ApplicabilityProfile(
                  population="adults, mixed setting",
                  measurement_conditions="8-week follow-up")),
        Study("Study 4", estimate=0.28, se=0.12,
              applicability=ApplicabilityProfile(
                  population="adults, urban clinic",
                  measurement_conditions="4-week follow-up",
                  known_failure_modes="underpowered, wide CI")),
        Study("Study 5", estimate=0.45, se=0.07,
              applicability=ApplicabilityProfile(
                  population="adults, urban clinic",
                  measurement_conditions="6-week follow-up")),
    ]

    print("=" * 78)
    print("Meta-analysis lineage -- live invocation chain")
    print("=" * 78)
    print("\nInput studies (illustrative/synthetic, each with an Applicability Profile):")
    for s in studies:
        print(f"  {s.label}: estimate={s.estimate}, se={s.se}  "
              f"[{s.applicability.population}; {s.applicability.measurement_conditions}]"
              + (f"  ⚠ {s.applicability.known_failure_modes}" if s.applicability.known_failure_modes else ""))

    print("\n[Node A] Cochran (1954) -- direct invocation, fixed-effect pooling")
    a_out = REGISTRY.invoke(A_CID, FixedEffectInput(studies=studies))
    print(f"  pooled_estimate={a_out.pooled_estimate:.4f}  pooled_se={a_out.pooled_se:.4f}  "
          f"Q={a_out.q_statistic:.4f}  k={a_out.k}")

    print("\n[Node B] DerSimonian & Laird (1986) -- CITES Node A via registry.invoke()")
    b_out = random_effects_pool(RandomEffectsInput(studies=studies), depth=0)
    print(f"  pooled_estimate={b_out.pooled_estimate:.4f}  pooled_se={b_out.pooled_se:.4f}  "
          f"tau²={b_out.tau_squared:.4f}")

    print("\n[Node C] Higgins & Thompson (2002) -- CITES Node B, which CITES Node A")
    c_out = heterogeneity_i2(HeterogeneityInput(studies=studies), depth=0)
    print(f"  I²={c_out.i_squared_pct:.1f}%  ({c_out.interpretation})")

    print("\n" + "=" * 78)
    print("Structured edge summary (v0.3 schema):")
    for (depth, edge_type, tier, target), n in sorted(REGISTRY.edge_summary().items()):
        print(f"  depth={depth}  {edge_type}  tier={tier}  -> {target}  ({n}x)")
    print("=" * 78)

    # sanity assertions
    assert a_out.pooled_se > 0
    assert b_out.tau_squared >= 0, "tau^2 cannot be negative (method-of-moments floor at 0)"
    assert b_out.q_statistic == a_out.q_statistic, \
        "Node B's Q must match Node A's own direct output -- confirms real invocation, not reimplementation"
    assert c_out.q_statistic == a_out.q_statistic, \
        "Node C's Q (via Node B) must also match Node A's original -- confirms the full two-hop chain is consistent"
    assert 0 <= c_out.i_squared_pct <= 100

    typed_edges = [e for e in REGISTRY.edges() if e.source_fn_cid is not None]
    assert all(e.edge_type == "cito:usesMethodIn" and e.tier == 0 for e in typed_edges)
    max_depth_seen = max(d for d, _, _, _ in REGISTRY.edge_summary().keys())
    assert max_depth_seen <= 3

    print(f"\nAll assertions passed, including cross-node Q-statistic consistency. "
          f"Max invocation depth: {max_depth_seen} (ceiling: 3)")


if __name__ == "__main__":
    main()
