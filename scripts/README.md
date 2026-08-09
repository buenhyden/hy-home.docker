# Script Inventory and Invocation Contract

`scripts/manifest.yaml` is the machine-readable authority for every tracked
file under `scripts/`. It is sorted by `path`; each path appears exactly once.
The manifest records the script's `kind`, canonical `authority`, current
`lifecycle`, mutation class, evidenced `consumers`, intended `disposition`,
`successor`, and evidenced `tests`.

During this approved convergence wave, `retain`, `rewrite`, `merge`, and
`delete` describe a precise future action. A retained row has no successor.
Every other row names its current successor. When a later Task removes a file,
it removes the live row in the same commit and preserves its final disposition
in the Stage 98 migration ledger.

## Invocation Safety

Check-only validators use `mutation: none`. Generators and synchronizers use
`mutation: check-write`: their default invocation must check or render without
changing repository state, while an explicit `--write` is required for a
repository update. `mutation: runtime` scripts are Operations entrypoints;
they are not run during document migration and require a current Runbook plus
the declared test evidence before explicit invocation.

Do not invoke a `mutation: runtime` row from inventory or migration evidence;
follow its current Runbook and explicit operator boundary. Do not invoke a
default-write generator without its documented non-mutating check option;
rows that lack safe defaults are classified for rewrite or merge. Consumers
and tests require semantic invocation/import evidence: a manifest mention,
generated index, archive record, or ownership glob is not consumption.

## Verification

Run the focused inventory contract with:

```bash
PYTHONPATH=. .venv/bin/python tests/validation/test_script_manifest.py
```

The test derives tracked coverage from `git ls-files scripts`, verifies exact
field and vocabulary contracts, checks deterministic ordering, and requires
all declared consumer and test paths to contain invocation/import evidence.
