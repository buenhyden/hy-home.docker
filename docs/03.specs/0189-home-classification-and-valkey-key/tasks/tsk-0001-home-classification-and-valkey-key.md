---
title: "HOME Classification and Valkey Key"
version: "0.4.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0189-TSK-0001"
parent_ids:
- "SPEC-0189"
- "SPEC-0189-PLAN-0001"
created: "2026-09-29"
---

# HOME Classification and Valkey Key

## Objective

Execute W1 through W3 of the [Plan](../plan.md) and record the evidence for
every acceptance criterion of [SPEC-0189](../spec.md).

## Inputs

- The two Deferred Items of the SPEC-0188 Task.
- The owner's request of 2026-09-29 to fix the `VALKEY_MNG_HOST_POST` spelling
  and to unify the Tempo and Pyroscope `OPTIONAL` and `HOME` wording.

## Work Log

- 2026-09-29: Spec, Plan, and Task drafted on branch
  `fix/home-classification-and-valkey-key`.
- 2026-09-29: W1 renamed the key. `.env` is untracked: its one key line was
  renamed in place with the value kept, and a key-order and comment-line
  comparison against `.env.example` matched. No value was printed.
- 2026-09-29: W2 found three observability READMEs beyond the Spec's first
  list with a line-wide search and added them to the scope. m0021's dated
  ledgers and snapshot tables (the 2026-09-20 judgment narrative and the
  runtime snapshot table) were left as recorded.
- 2026-09-29: W3 ran the verification below.

## Verification Evidence

Checks were static; no service was started, stopped, or recreated.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: `git grep VALKEY_MNG_HOST_POST` finds only the archive, SPEC-0188, this package, and its Stage 03 README row; `.env` and `.env.example` keys, order, and comment lines identical; `docker compose --profile mng config --quiet` rc 0 (`84f891034`) | [mng-db Compose](../../../../infra/04-data/operational/mng-db/docker-compose.yml) |
| 2 | W2 | PASS: a line-wide search finds no current `OPTIONAL` classification of Tempo or Pyroscope outside m0021's dated ledgers; `check-operations-catalog.py` PASS (`323675466`) | [POL-0078](../../../05.operations/policies/0078-compose-profile-vocabulary.md) |
| 3 | W3 | PASS: `validate-docker-compose.sh` selections=72, services_total=355; `run-ci-gate.py --profile full` rc 0 (Conftest 294 passed, 0 warnings); `tests/lib` 945 OK; `tests/validation` 675 OK, 23 skipped; `pre-commit run --from-ref origin/main --to-ref HEAD` rc 0 | N/A: run evidence for this change |

## Review Evidence

- The m0021 Consumer and Disposition cells for Tempo and Pyroscope are
  hand-written; they now use the "Owner-required HOME" and "retain HOME"
  wording of the other HOME rows. The renderer confirmed no projected cell
  drifted.
- An operator `.env` that still sets `VALKEY_MNG_HOST_POST` falls back to the
  `26379` default until the key is renamed.

## Commit Ledger

| Commit | Unit | Change |
| --- | --- | --- |
| `06376ef01` | Package | Spec, Plan, and Task drafted; registry allocation |
| `84f891034` | W1 | `VALKEY_MNG_HOST_PORT` rename |
| `323675466` | W2 | Tempo and Pyroscope classified as HOME |

## Rulings

- 2026-09-29: Owner ruled to fix the key spelling and to unify the Tempo and
  Pyroscope classification; POL-0078's later HOME selection decides it.

## Deferred Items

- `registry`, `dcgm-exporter`, and `seaweedfs-s3` are `OPTIONAL` in the m0021
  inventory while their profiles are in HOME.
