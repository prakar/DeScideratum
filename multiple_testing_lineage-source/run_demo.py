"""
Registers the multiple-testing knot's two invocable nodes and runs the
chain, then prints the rubric verdict table -- including the citation
that's deliberately NOT wired up as a function.

Run with: python3 run_demo.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from registry import REGISTRY
from functions.benjamini_hochberg_1995 import bh_adjust, FN_CID as A_CID, BHInput
from functions.storey_2002_qvalue import storey_qvalues, FN_CID as B_CID, QValueInput
from citation_records import print_rubric_table

REGISTRY.register(A_CID, bh_adjust)
REGISTRY.register(B_CID, storey_qvalues)


def main():
    # a synthetic "reader's own p-values" -- 20 tests, a mix of clearly
    # significant, borderline, and null results
    reader_pvalues = [
        0.0001, 0.0004, 0.0012, 0.008, 0.011, 0.019, 0.021, 0.033, 0.041,
        0.052, 0.078, 0.11, 0.14, 0.19, 0.24, 0.31, 0.42, 0.55, 0.71, 0.93,
    ]

    print("=" * 78)
    print("Multiple-testing knot -- live invocation chain")
    print("=" * 78)

    print("\n[Node A] Benjamini & Hochberg (1995) -- direct invocation")
    a_out = REGISTRY.invoke(A_CID, BHInput(pvalues=reader_pvalues, alpha=0.05))
    print(f"  n_significant={a_out.n_significant} / {len(reader_pvalues)}")
    print(f"  adjusted p-values (first 5): {[round(p, 4) for p in a_out.adjusted_pvalues[:5]]}")

    print("\n[Node B] Storey (2002) -- CITES Node A via registry.invoke()")
    b_out = storey_qvalues(QValueInput(pvalues=reader_pvalues, lambda_fixed=0.9), depth=0)
    print(f"  pi0_hat={b_out.pi0_hat:.4f}")
    print(f"  q-values (first 5): {[round(q, 4) for q in b_out.qvalues[:5]]}")
    print(f"  naive_bh_n_significant (cited from Node A) = {b_out.naive_bh_n_significant}")

    print("\n" + "=" * 78)
    print("Invocation log:")
    for depth, cid in REGISTRY.call_log():
        print(f"  depth={depth}  {cid}")
    print("=" * 78)

    # sanity assertions
    assert a_out.n_significant <= len(reader_pvalues)
    assert 0 <= b_out.pi0_hat <= 1
    assert b_out.naive_bh_n_significant == a_out.n_significant, \
        "Node B's cited baseline must match Node A's own direct result on the same data"
    max_depth_seen = max(d for d, _ in REGISTRY.call_log())
    assert max_depth_seen <= 3
    print(f"\nAll assertions passed. Max invocation depth reached: {max_depth_seen} (ceiling: 3)")
    print("(Node B's cited BH count matches Node A's direct-call count on the same data --")
    print(" confirms the citation is a real invocation, not a coincidentally-similar reimplementation.)")

    print("\n")
    print_rubric_table()


if __name__ == "__main__":
    main()
