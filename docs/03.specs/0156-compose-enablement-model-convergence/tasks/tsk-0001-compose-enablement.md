---
title: Converge Compose Enablement onto Profiles
version: 1.0.0
type: sdlc/task
layer: specs
status: draft
owner: "@buenhyden"
artifact_id: SPEC-0156-TSK-0001
parent_ids: [SPEC-0156, SPEC-0156-PLAN-0001]
created: 2026-09-02
updated: 2026-09-04
---

# Converge Compose Enablement onto Profiles

## Objective

Execute the five steps in the Plan so that stack membership is expressed by
Compose profiles alone and every `infra/` Compose file is reachable.

## Inputs

- `docker-compose.yml` and its `include:` list
- `infra/**/docker-compose*.yml`
- `scripts/operations/generate-compose-profile-service-coverage.sh`
- `scripts/validation/validate-docker-compose.sh`
- `docs/90.references/data/0059-compose-profile-service-coverage/README.md`

## Work Log

Not started. The Spec's measured inputs were re-verified on 2026-09-02 against
the tree and still hold exactly, so the Spec needs no restatement before
execution:

| Acceptance item | Measured now | Target |
| :--- | :--- | :--- |
| Commented root includes | 20 | 0 |
| Compose files under `infra/` | 46 | all included |
| Active root include entries | 17 | 46 |
| `docker-compose.yml.format` tracked | 1 | 0 |
| `docker compose version` | v5.4.0 | available |

The per-pair topology decisions required by Plan step 3 are recorded here as
they are made, each with the measured difference that justified it.

## Verification Evidence

Pending. Every numbered item in the Spec's Acceptance Contract must be recorded
here with its command and output before this Task moves to `completed`.

## Review Evidence

Pending.

## Commit Ledger

| Commit | Scope |
| :--- | :--- |
| — | not started |

## Rulings

- The package was completed and activated on 2026-09-02 without executing it.
  A Spec with no Plan and no Task cannot be executed by the governance flow, and
  the enablement change itself rewrites service selection across 46 stacks, so
  it is its own reviewed unit rather than a rider on a documentation change.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
