# Script Inventory and Invocation Contract

`scripts/manifest.yaml` is the sole machine-readable authority for every
tracked file under `scripts/`. It is sorted by `path`; each path appears
exactly once. `scripts/validation/check-script-manifest.py` enforces the
working-tree inventory and typed row contract fail closed.
The manifest records the script's `kind`, canonical `authority`, current
`lifecycle`, mutation class, evidenced `consumers`, intended `disposition`,
`successor`, and evidenced `tests`.

During this approved convergence wave, `retain`, `rewrite`, `merge`, and
`delete` describe a precise action. A retained row has no successor. Every
other row names its current successor. When a Task removes a file, it removes
the live row in the same commit and preserves historical disposition evidence
in the approved migration record.

## Invocation Safety

Check-only validators use `mutation: none`. Generators and synchronizers use
`mutation: check-write`: their default invocation must check or render without
changing repository state, while an explicit `--write` is required for a
repository update. A retained check-write generator registers a safe argv
`check_command` and the exact tracked `outputs` that it owns. `mutation:
runtime` scripts are Operations entrypoints;
they are not run during document migration and require a current Runbook plus
the declared test evidence before explicit invocation.

Do not invoke a `mutation: runtime` row from inventory or migration evidence;
follow its current Runbook and explicit operator boundary. Do not invoke a
default-write generator without its documented non-mutating check option;
rows that lack safe defaults are classified for rewrite or merge. Consumers
and tests require semantic invocation/import evidence: a manifest mention,
generated index, archive record, or ownership glob is not consumption.

The canonical LLM Wiki generator is
`python3 scripts/knowledge/generate-llm-wiki.py`. It owns both tracked outputs,
defaults to `--check`, and mutates them only with explicit `--write`.

## Verification

Run the manifest and generated-output gates with:

```bash
python3 scripts/validation/check-script-manifest.py
python3 scripts/validation/check-script-manifest.py --check-generated
python3 scripts/knowledge/generate-llm-wiki.py --check
PYTHONPATH=. .venv/bin/python tests/validation/test_script_manifest.py
PYTHONPATH=. .venv/bin/python tests/validation/test_generate_llm_wiki.py
```

The gate derives coverage from tracked plus present non-ignored Task-local
paths, verifies exact field and vocabulary contracts, checks deterministic
ordering, and requires all declared consumer and test paths to contain
invocation/import evidence. `--check-generated` runs only retained check-write
generators; it never invokes runtime-changing rows.
