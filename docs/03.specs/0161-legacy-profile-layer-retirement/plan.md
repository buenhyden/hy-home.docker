---
title: Legacy Profile Layer Retirement Plan
version: 1.0.0
type: sdlc/plan
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0161-PLAN-0001
parent_ids: [SPEC-0161]
created: 2026-09-03
updated: 2026-09-03
---

# Legacy Profile Layer Retirement Plan

## Objective

Remove the second profile authority in five increments ordered by measured
reach, so each step is small enough to verify and revert alone.

## Dependencies

- SPEC-0160 put 145 of 149 tracked READMEs under Registry classification, which
  is what makes the legacy README half removable.
- The measurement must be environment-independent: the gate admits only an
  allowlisted environment, so an env-var probe silently records nothing.

## Execution Sequence

1. `archive_profiles` (0 reads) - remove the section, its three helpers, and the
   two consumer branches. Verify: no Stage 98 document classifies as `archive`.
2. `readme_profiles` (5 reads) - point the one live consumer at the Registry and
   delete the five unreachable entrypoints. Verify: the advisory inventory names
   a registered profile.
3. `document_families` (1689 reads) - derive `_typed_target_types` from
   `registry.profiles`. Verify: the two sets differ only by legacy-only names
   that own no document.
4. `common` (9 of 11 keys read) - move the section into `registry.json` verbatim
   and build the reader envelope from the Registry alone.
5. Delete the loader once nothing calls it, plus the constants that existed only
   to validate it.

## Risk and Rollback

Each step is one commit with a green full gate, so any step reverts alone. The
riskiest is step 4: it changes how every consumer receives `common`. Moving the
values verbatim keeps behavior identical and confines the risk to wiring.

## Verification

`python3 scripts/validation/run-ci-gate.py --profile full` after every step.

## Related Documents

- [Specification](./spec.md)
- [Task](./tasks/tsk-0001-legacy-layer-retirement.md)
