"""
Toy stand-in for the Custodian's resolve()/record_invocation() path.
This is what makes the demo actually test "citation is invocation"
mechanically, rather than just letting node B `import` node A the
normal Python way -- every cross-node call here goes through a
CID lookup and a depth check, exactly like a real cross-document
invocation would over IPFS + the Custodian in the full system.
"""
from typing import Callable, Dict

MAX_INVOCATION_DEPTH = 3


class InvocationDepthExceeded(Exception):
    pass


class Registry:
    def __init__(self):
        self._functions: Dict[str, Callable] = {}
        self._call_log = []

    def register(self, fn_cid: str, fn: Callable) -> None:
        self._functions[fn_cid] = fn

    def invoke(self, fn_cid: str, payload, depth: int = 0):
        if depth > MAX_INVOCATION_DEPTH:
            raise InvocationDepthExceeded(
                f"invocation chain exceeded max depth {MAX_INVOCATION_DEPTH} at {fn_cid}"
            )
        if fn_cid not in self._functions:
            raise KeyError(f"no function registered under CID {fn_cid} -- "
                            f"in the real system this is where a CORS-gated "
                            f"IPFS fetch would happen")
        self._call_log.append((depth, fn_cid))
        fn = self._functions[fn_cid]
        return fn(payload)

    def call_log(self):
        return list(self._call_log)


REGISTRY = Registry()
