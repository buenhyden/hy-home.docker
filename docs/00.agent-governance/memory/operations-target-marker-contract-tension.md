---
layer: agentic
status: active
---

# Operations Target Marker Contract Tension

- Date: 2026-08-20
- Layer: agentic
- Status: active
- Applies To: `docs/05.operations/catalog/`, `scripts/lib/document_governance/metadata_validator.py`, `scripts/validation/check-repo-contracts.sh`
- Tags: contracts, operations-catalog, document-metadata, migration
- Retrieval Keywords: Target marker, template-instruction-in-target, TARGET_TEMPLATE_LITERALS, operations catalog, self-reference marker
- Last Verified: 2026-08-20

## Problem

Three tracked contracts disagree about the `<!-- Target: ... -->` self-reference
marker in Operations catalog leaves, and no single edit satisfies all three.

- `metadata_validator.py:911` lists `<!-- Target:` in `TARGET_TEMPLATE_LITERALS`.
  A changed target-stage body containing it reports
  `template-instruction-in-target`, so the marker must **not** exist.
- `check-repo-contracts.sh:594` requires that a marker, **if present**, equal the
  file's own path. It does not require the marker to exist.
- `operations_catalog.py:1502-1504` rewrites the marker from the legacy path to
  the final path during executed-mode semantic rewrite, so the migration design
  expects the marker to **survive** the move.

## Context

The condition is pre-existing and repo-wide, not introduced by any one slice.
At commit `3f3d4b4e`, 184 files under `docs/05.operations/catalog/` already
carried the marker, and prevalence is uniform across executed and unexecuted
domains alike: `00-workspace` 7 of 14 files, `01-gateway` 6 of 8, `02-auth`
6 of 7, `03-security` 3 of 4, `04-data` 50 of 52, `05-messaging` 9 of 10.
Task 10D executed the first four domains and repointed rather than deleted.

The tension is invisible until a file changes. The metadata deficit scan runs
only under `changed_boundary`, so an unchanged leaf is never scanned. Executing
a migration slice moves its files into the changed set and surfaces the whole
domain's share of the debt at once, which reads as a regression the slice caused.

## Resolution

Task 10E's `04-data` slice repointed all 50 markers to their own final paths and
did not delete them, following the Task 10D precedent and satisfying
`check-repo-contracts.sh`. Leaving a marker stale would have violated that
contract; deleting one would satisfy both it and the metadata contract but is a
184-file decision spanning domains the slice does not own.

The residual is 50 `template-instruction-in-target` violations reported by
`check-document-metadata.py --mode check-changed`, recorded as pre-existing debt
surfaced rather than introduced.

## Prevention

Before treating a changed-file metadata violation as slice-caused, measure the
same predicate at the pre-change commit and across domains the slice does not
touch. A `changed_boundary` gate reports where the debt became visible, not
where it originated.

Resolving the tension belongs to a unit that owns all three contracts. Deleting
the marker repo-wide is compatible with `check-repo-contracts.sh` and with the
`_subject_path_marker_rule` in `operations_catalog.py`, which omits its path
invariant when the source carries no marker; the blocking question is whether
the executed-mode rewrite at `operations_catalog.py:1502-1504` should stop
emitting it.

## Evidence

- Marker prevalence at `3f3d4b4e`: `git grep -l "<!-- Target:" HEAD -- 'docs/05.operations/catalog/*' | wc -l` returns 184.
- `04-data` marker self-consistency after the slice: 50 self-consistent, 0 mismatched.
- `check-document-metadata.py --mode check-changed`: `selected=61 violations=50`.

## Related Documents

- [Spec 136 taxonomy convergence Task](../../03.specs/spec-0136-sdlc-taxonomy-convergence/task.md)
- [Operations catalog migration ledger](../../98.archive/migrations/mig-0002-operations-catalog-convergence.md)
- [Memory template](../../99.templates/templates/governance/memory.template.md)
