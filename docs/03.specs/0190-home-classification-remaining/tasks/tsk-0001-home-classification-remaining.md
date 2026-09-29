---
title: "Remaining HOME Classification"
version: "0.2.0"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190-TSK-0001"
parent_ids:
- "SPEC-0190"
- "SPEC-0190-PLAN-0001"
created: "2026-09-29"
---

# Remaining HOME Classification

## Objective

Execute W1 and W2 of the [Plan](../plan.md) and record the evidence for every
acceptance criterion of [SPEC-0190](../spec.md).

## Inputs

- The Deferred Item of the SPEC-0189 Task.
- The owner's request of 2026-09-29 to resolve the same `OPTIONAL` and `HOME`
  mismatch for the three remaining services.
- The resolved HOME selection: `docker compose config --services` with the
  POL-0078 HOME profiles lists 44 services, including `registry`,
  `dcgm-exporter`, and `seaweedfs-s3`.

## Work Log

- 2026-09-29: Spec, Plan, and Task drafted on branch
  `fix/home-classification-remaining`.
- 2026-09-29: W1 changed the wording and the three m0021 rows. POL-0065 had
  excluded `registry` from HOME, and GDE-0045 said HOME did not start
  `dcgm-exporter`; both now cite the SPEC-0182 W6 HOME addition.
  `seaweedfs-s3` cites the HOME `storage` selection, which predates W6.
- 2026-09-29: W2 ran the verification below.
- 2026-09-29: Operational note, outside this package's scope: at the owner's
  request, the running SPEC-0188 targets were recreated so their new bindings
  apply. Each running image ID matched its Compose tag, and a
  `docker compose --dry-run up -d --no-deps --no-build` showed only the
  recreates. `mng-valkey`, `mng-pg`, `kafka-1`, `loki`, `tempo`, and `alloy`
  came back healthy through `--wait`; `pyroscope`, unhealthy since
  2026-09-25, came back healthy. Afterwards no container was unhealthy or
  restarting. The other SPEC-0188 targets were not running and were not
  started; `traefik`'s resolved binding did not change.

## Verification Evidence

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: a line-wide search of each owner for `OPTIONAL`, `opt-in`, on-demand, and HOME exclusion finds only `pushgateway`, which is `OPTIONAL`; the renderer reports no drifted row; `check-operations-catalog.py` PASS (`b5babb26e`) | [POL-0078](../../../05.operations/policies/0078-compose-profile-vocabulary.md) |
| 2 | W2 | PASS: `run-ci-gate.py --profile full` rc 0 (Conftest 294 passed, 0 warnings); `tests/lib` 945 OK; `tests/validation` 675 OK, 23 skipped; `pre-commit run --from-ref origin/main --to-ref HEAD` rc 0 | N/A: run evidence for this change |

## Review Evidence

- The m0021 Consumer and Disposition cells are hand-written; they now use the
  wording of the other HOME rows.

## Commit Ledger

| Commit | Unit | Change |
| --- | --- | --- |
| `7f2fde07f` | Package | Spec, Plan, and Task drafted; registry allocation |
| `b5babb26e` | W1 | Three services classified as HOME |

## Rulings

- 2026-09-29: Owner ruled to resolve the mismatch; the HOME selection decides
  it.
