# Pydantic upgrade -- how to apply

In your Codespaces terminal, from inside `resampling_knot/`:

```bash
pip install pydantic
```

Then replace these three files with the versions in this archive (same paths, same names):
- functions/efron_1979_bootstrap.py
- functions/efron_tibshirani_1993_bca.py
- functions/davison_hinkley_1997_double_bootstrap.py

`registry.py` and `run_demo.py` are unchanged -- Pydantic's `BaseModel` supports attribute access
(`base.point_estimate`) the same way the dataclasses did, so nothing calling into these functions
needs to change.

Then rerun:

```bash
python3 run_demo.py
```

Expect identical numeric output to before. What changes is invisible until something goes wrong on
purpose -- e.g. try calling `BootstrapSEInput(data=[1.0])` (only one point) from a Python shell in
that directory and you should get a real Pydantic `ValidationError` naming the failed field, not a
generic Python exception. That's the actual point of the upgrade: a validated, self-describing
contract instead of a `__post_init__` check.
