---
title: "Observability CA Execution Task"
version: "0.1.2"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0245-TSK-0001"
parent_ids:
- "SPEC-0245-PLAN-0001"
created: "2026-10-16"
---

# Observability CA Execution Task

## Overview

### Objective

Complete service-specific backup and isolated-recovery rehearsals for
Prometheus and Gatus before either CA recreation, then recreate Prometheus
before Gatus while preserving production data boundaries.

## Inputs and Authorization

- **Request:** on 2026-10-16 the owner authorized the current host's
  Prometheus and Gatus backup/restore validation followed by their bounded CA
  application and recreation.
- **Authorization boundary:** this Task covers only the two named services,
  one at a time, in Plan order. It excludes secret or raw-data capture,
  OpenBao operations, a stack-wide restart, an unreviewed image pull, a
  Prometheus upgrade, manual data manipulation, volume deletion, and
  production-data restoration or replacement.
- **Baseline:** `main` `89eb43f683a11587cf4f125be534ae720c20a55c`.
- **Known starting observation:** Prometheus was observed on its 3.14 rollback
  image and both named services lacked the required CA mount at runtime. Gatus
  requires a no-network/no-pull minimal delta image with `FROM` its exact
  current running immutable base and `COPY` of only the reviewed tracked
  CA-aware entrypoint, with its binary unchanged, before recreation; a
  same-image recreation is not accepted as CA evidence.
- **Planned protected artifacts:** the reviewed backup/isolated-restore packet
  selects `/home/hyunyoun/storage/backups/r13-observability-ca-20261016-01`.
  Workspace artifacts require mode 0700 and isolated-restore tar siblings mode
  0400. The path shares device 2064 with production data, so it is a
  pre-recreate recovery gate only, not a disk-failure disaster-recovery claim.

## Work Log

### Initial State

The approved Spec and Plan define the execution order. No backup, isolated
restore, image build, CA application, recreation, or operational review has
run under this Task.

### Ready Transition

On 2026-10-16, W1 bound the exact, value-free backup phase contract and its
two guard helpers to the selected host-local protected artifact path. The
contract specifies the two recovery gates before either CA recreation, the
Prometheus-then-Gatus recreation order, same-device non-DR limitation, and
the mode-0700 workspace/mode-0400 tar-sibling controls. This makes the Task
`ready` to begin a reviewed W2 or W4 gate; it is not a backup, restore, image
build, service recreation, or operational-review result.

The Task transitions to `in-progress` only when an approved W2 or W4 recovery
gate actually starts. The reviewed recovery packet must still pass its
independent IaC/security review before the relevant operation proceeds.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0245-TSK-0001 | draft | ready | Ready backup packet binding |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Initial operational execution state | 1, 2, 3, 4, 5, 6, 7 | W1, W2, W3, W4, W5, W6, W7 | No preflight, backup, isolated restore, image build, recreation, review, or selected gate had run when this Task was created | Initial record on `89eb43f683a11587cf4f125be534ae720c20a55c` | NOT_RUN | Initial State | optional | - |
| Ready backup packet binding | 1 | W1 | SHA-256 binding of the frozen backup phase contract and guard helpers | Contract `98a93a8ac0454bdf080c0d97f9e46f39882b53b84245f5754eed7130721ab1e3`; phase script `4728e8408a4531b9577ab5ada31cda6282a1eed0ad81656f43485c94fd97ae98`; archive guard `a85ab831c3369f1d04b5dc6abd14fa83ae5bb4ced495f594d85955474c42b385` | PASS | Ready Transition | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | Await W1 preflight | @buenhyden |
| 2 | pending | - | Await W2 backup and isolated restore | @buenhyden |
| 3 | pending | - | Await W4 backup and isolated restore | @buenhyden |
| 4 | pending | - | Await W4 build identity | @buenhyden |
| 5 | pending | - | Await W3 and W5 service results | @buenhyden |
| 6 | pending | - | Await W6 outcome if a gate fails | @buenhyden |
| 7 | pending | - | Await W7 reviews and checks | @buenhyden |

## Review and Completion

This draft has no accepted criterion. Completion requires the service-specific
execution evidence listed in SPEC-0245; a source-only check, image build, or
Compose render does not prove a production backup, isolated restore, or CA
application.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
