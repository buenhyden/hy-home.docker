---
title: "HOME Classification and Valkey Key Specification"
version: "0.5.0"
type: "sdlc/spec"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0189"
parent_ids:
- "REQ-0027"
- "AD-0031"
created: "2026-09-29"
---

# HOME Classification and Valkey Key Specification

## Overview

[SPEC-0188](../0188-compose-host-port-exposure/spec.md) deferred two
inconsistencies. This package resolves both.

- The `mng-valkey` host port key is spelled `VALKEY_MNG_HOST_POST`. Every other
  host port key ends in `_HOST_PORT`.
- Tempo and Pyroscope are `HOME` in
  [POL-0078](../../05.operations/policies/0078-compose-profile-vocabulary.md),
  where the owner added `tracing` and `profiling` to HOME in SPEC-0182 W6
  (2026-09-25). Ten other documents still call them `OPTIONAL`.

The owner ruled on 2026-09-29 to fix the key and to unify the classification.
The later HOME ruling wins.

## Boundaries and Inputs

In scope:

- `VALKEY_MNG_HOST_POST` in `infra/04-data/operational/mng-db/docker-compose.yml`,
  the root `.env.example` and `.env` (key only, value kept),
  GDE-0028, the `mng-db` README, and the m0021 service inventory row.
- The Tempo and Pyroscope classification in AD-0006 (observability
  architecture), GDE-0047, POL-0047, GDE-0049, POL-0049, POL-0021, the
  `06-observability`, `tempo`, and `pyroscope` READMEs, and the m0021 service
  inventory rows. Dated ledgers and snapshot tables in m0021 stay as recorded.

Out of scope:

- The completed SPEC-0188 records, which describe the misspelling as found.
- `registry`, `dcgm-exporter`, and `seaweedfs-s3`, which the m0021 inventory
  also lists as `OPTIONAL` although their profiles are in HOME. They need
  their own owner ruling.
- Starting, recreating, or stopping any service.

## Behavior Contract

1. `mng-valkey` publishes its host port from `VALKEY_MNG_HOST_PORT` with the
   same default, `26379`.
2. `.env` and `.env.example` keep identical keys in identical order.
3. Every current document classifies Tempo and Pyroscope as `HOME`, selected
   by `tracing` and `profiling`.

## Technical Approach

1. Rename the key in the Compose leaf, both environment files, and the
   documents in one commit.
2. Change the classification wording, and refresh the m0021 rows with the
   operations catalog renderer, replacing only the changed rows.

## Interfaces and Data

- One `.env` key renamed. An operator `.env` that still sets the old key falls
  back to the `26379` default until the key is renamed.

## Failure Modes and Guardrails

| Failure | Guard |
| --- | --- |
| A consumer still reads the old key | `git grep` finds no reference outside the completed SPEC-0188 records and the archive |
| An operator `.env` keeps the old key with a custom value | The Task records the rename; the default matches the documented port |
| The inventory renderer drops hand-written lines | Only drifted rows inside the inventory markers are replaced |

## Acceptance Contract

1. `VALKEY_MNG_HOST_POST` appears nowhere outside `docs/98.archive/` and the
   SPEC-0188 records, and `.env` and `.env.example` share keys and order.
2. No current document calls Tempo or Pyroscope `OPTIONAL`; m0021's dated
   ledgers and snapshot tables keep what they recorded.
3. `validate-docker-compose.sh`, `run-ci-gate.py --profile full`, `tests/lib`,
   and `tests/validation` pass.

## Traceability

- REQ-0027 and AD-0031: the HOME development host.
- POL-0078: the HOME profile selection.
- SPEC-0188: the Task that deferred both items.

## Open Questions

None.

## Operational Impact

None until an operator recreates `mng-valkey`. The live `.env` is renamed in
place with its value kept.
