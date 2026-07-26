"""
Registers the three-node resampling knot and runs the full chain:
  Davison & Hinkley (1997) --invokes--> Efron & Tibshirani (1993) --invokes--> Efron (1979)

Run with: python3 run_demo.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from registry import REGISTRY
from functions.efron_1979_bootstrap import bootstrap_se, FN_CID as A_CID
from functions.efron_tibshirani_1993_bca import bca_interval, FN_CID as B_CID, BCaInput
from functions.davison_hinkley_1997_double_bootstrap import (
    double_bootstrap_ci, FN_CID as C_CID, DoubleBootstrapInput,
)

REGISTRY.register(A_CID, bootstrap_se)
REGISTRY.register(B_CID, bca_interval)
REGISTRY.register(C_CID, double_bootstrap_ci)


def main():
    # a synthetic "reader's own dataset" -- the whole point being that
    # this is NOT the original papers' data, it's substituted at call time
    reader_data = [12.1, 14.3, 11.8, 15.9, 13.2, 10.7, 16.4, 12.9, 14.8, 11.2, 13.6, 15.1]

    print("=" * 70)
    print("Resampling knot -- live invocation chain")
    print("=" * 70)

    print("\n[Node A] Efron (1979) -- direct invocation, no citation chain")
    a_out = REGISTRY.invoke(A_CID, __import__(
        "functions.efron_1979_bootstrap", fromlist=["BootstrapSEInput"]
    ).BootstrapSEInput(data=reader_data, n_resamples=5000, seed=1))
    print(f"  point_estimate={a_out.point_estimate:.4f}  se={a_out.se:.4f}")

    print("\n[Node B] Efron & Tibshirani (1993) -- CITES Node A via registry.invoke()")
    b_out = REGISTRY.invoke(B_CID, BCaInput(data=reader_data, n_resamples=5000, seed=1))
    print(f"  point_estimate={b_out.point_estimate:.4f}  "
          f"95% BCa CI=[{b_out.ci_lower:.4f}, {b_out.ci_upper:.4f}]  "
          f"z0={b_out.bias_correction_z0:.4f}  a={b_out.acceleration_a:.6f}")

    print("\n[Node C] Davison & Hinkley (1997) -- CITES Node B, which CITES Node A")
    c_out = double_bootstrap_ci(
        DoubleBootstrapInput(data=reader_data, n_resamples=300, seed=1), depth=0
    )
    print(f"  point_estimate={c_out.point_estimate:.4f}")
    print(f"  inner BCa CI     =[{c_out.inner_bca_ci_lower:.4f}, {c_out.inner_bca_ci_upper:.4f}]")
    print(f"  calibrated CI    =[{c_out.ci_lower_calibrated:.4f}, {c_out.ci_upper_calibrated:.4f}]")

    print("\n" + "=" * 70)
    print("Invocation log summary -- proves the chain actually ran,")
    print("not just that the diagram claims it would:")
    log = REGISTRY.call_log()
    from collections import Counter
    counts = Counter(log)
    for (depth, cid), n in sorted(counts.items()):
        print(f"  depth={depth}  {cid}  (invoked {n}x)")
    print(f"  total invocations logged: {len(log)}")
    print("=" * 70)

    # sanity assertions -- this is the "unit test required before commit"
    # rule from the manifest spec, run for real
    assert a_out.se > 0, "bootstrap SE must be positive"
    assert b_out.ci_lower < b_out.point_estimate < b_out.ci_upper, "BCa CI must bracket the point estimate"
    assert c_out.ci_lower_calibrated <= c_out.ci_upper_calibrated, "calibrated CI must be well-ordered"
    max_depth_seen = max(d for d, _ in REGISTRY.call_log())
    assert max_depth_seen <= 3, "must respect MAX_INVOCATION_DEPTH"
    print(f"\nAll assertions passed. Max invocation depth reached: {max_depth_seen} (ceiling: 3)")


if __name__ == "__main__":
    main()
