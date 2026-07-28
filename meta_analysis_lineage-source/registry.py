"""
Generalized invocation registry -- v0.3 schema.

Replaces the old bare (depth, fn_cid) call log with structured Edge
objects: every invocation now carries a CiTO-vocabulary edge_type, a
proof-obligation tier (0-5, see verification_ontology_v0.3_synthesis.md
Part 4), a proof method, and a confidence level -- not just the fact
that a call happened.

Backward compatible: call_log() still returns the old (depth, fn_cid)
tuples so nothing that reads it breaks; edges() is the new, richer view.
"""
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Optional

MAX_INVOCATION_DEPTH = 3


class InvocationDepthExceeded(Exception):
    pass


@dataclass
class Edge:
    source_fn_cid: Optional[str]   # who made the call; None = reader-triggered top-level call
    target_fn_cid: str             # who was invoked
    edge_type: str                 # CiTO vocabulary, e.g. "cito:usesMethodIn"
    tier: int                      # proof-obligation tier, 0-5 (-1 = unspecified)
    proof_method: str              # e.g. "executable_invocation"
    confidence: str                # e.g. "verified"
    depth: int
    applicability_profile: Optional[Dict[str, Any]] = None


class Registry:
    def __init__(self):
        self._functions: Dict[str, Callable] = {}
        self._cites: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self._edges: List[Edge] = []
        self._call_log = []  # legacy (depth, fn_cid) view, kept for backward compatibility

    def register(self, fn_cid: str, fn: Callable) -> None:
        self._functions[fn_cid] = fn

    def register_cites(self, source_fn_cid: str, cites: Dict[str, Dict[str, Any]]) -> None:
        """Declare a function's outgoing typed edges, e.g.:
        registry.register_cites(BCA_FN_CID, {
            EFRON_1979_FN_CID: {"edge_type": "cito:usesMethodIn", "tier": 0,
                                 "proof_method": "executable_invocation", "confidence": "verified"}
        })
        """
        self._cites[source_fn_cid] = cites

    def invoke(self, fn_cid: str, payload, depth: int = 0, source_fn_cid: Optional[str] = None):
        if depth > MAX_INVOCATION_DEPTH:
            raise InvocationDepthExceeded(
                f"invocation chain exceeded max depth {MAX_INVOCATION_DEPTH} at {fn_cid}"
            )
        if fn_cid not in self._functions:
            raise KeyError(f"no function registered under CID {fn_cid}")

        meta = {}
        if source_fn_cid and source_fn_cid in self._cites:
            meta = self._cites[source_fn_cid].get(fn_cid, {})

        edge = Edge(
            source_fn_cid=source_fn_cid,
            target_fn_cid=fn_cid,
            edge_type=meta.get("edge_type", "unknown"),
            tier=meta.get("tier", -1),
            proof_method=meta.get("proof_method", "unspecified"),
            confidence=meta.get("confidence", "unspecified"),
            depth=depth,
            applicability_profile=meta.get("applicability_profile"),
        )
        self._edges.append(edge)
        self._call_log.append((depth, fn_cid))

        fn = self._functions[fn_cid]
        return fn(payload)

    def call_log(self):
        """Legacy view: list of (depth, fn_cid) tuples."""
        return list(self._call_log)

    def edges(self) -> List[Edge]:
        """Full structured view: every invocation as a typed, tiered Edge."""
        return list(self._edges)

    def edge_summary(self) -> Dict[tuple, int]:
        """Counts grouped by (depth, edge_type, tier, target_fn_cid) -- the
        structured equivalent of the old call-count summary."""
        from collections import Counter
        return Counter(
            (e.depth, e.edge_type, e.tier, e.target_fn_cid) for e in self._edges
        )


REGISTRY = Registry()
