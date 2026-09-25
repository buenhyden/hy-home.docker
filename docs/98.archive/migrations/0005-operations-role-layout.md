---
title: "Operations Role Layout Migration"
version: "1.0.0"
type: "archive/migration"
status: "sealed"
owner: "@buenhyden"
updated: "2026-09-26"
layer: "archive"
artifact_id: "MIG-0005"
parent_ids:
- "ADR-0043"
created: "2026-09-26"
---

# Operations Role Layout Migration

## Purpose

Tell a consumer outside this repository where Stage 05 Operations documents
went when ADR-0043 replaced the domain catalog with role directories. This
record names the moved scope and its current owner; it carries no document
body and is not a redirect.

## Moved Scope

Every Guide, Policy, and Runbook moved by one rule, keeping its artifact
identifier:

| Former route | Current route |
| --- | --- |
| `docs/05.operations/catalog/<domain>/<subject>/guide.md` | `docs/05.operations/guides/<artifact number>-<slug>.md` |
| `docs/05.operations/catalog/<domain>/<subject>/policy.md` | `docs/05.operations/policies/<artifact number>-<slug>.md` |
| `docs/05.operations/catalog/<domain>/<subject>/runbook.md` | `docs/05.operations/runbooks/<artifact number>-<slug>.md` |
| `docs/05.operations/catalog/README.md` and each `catalog/<domain>/README.md` | `docs/05.operations/README.md` and the three role indexes |

The slug is the subject folder name without its number, with two kinds of
exception:

- The seven `optimization-hardening` subjects take their domain word as a
  prefix: `data-`, `messaging-`, `observability-`, `workflow-`, `ai-`,
  `tooling-`, and `laboratory-optimization-hardening`.
- `POL-0052`, the Policy of subject `0051-airflow-dag-lifecycle`, is
  `policies/0052-airflow-dag-lifecycle.md`, because the file number is the
  artifact number.

Incident packets under `docs/05.operations/incidents/` did not move.

## Current Owner

The Stage 05 README and the Guide, Policy, and Runbook indexes under
`docs/05.operations/` own current navigation; each document's `artifact_id`
is unchanged and identifies it across the move.

## Approval

The owner's request of 2026-09-26 authorizes the move as a local change.
No runtime, secret, remote, or deployment action is authorized by this
migration, and links in other repositories are updated by their owners.

## Traceability

- [Archive index](../README.md)
- ADR-0043 and SPEC-0183, reached through the Stage 02 and Stage 03 indexes
