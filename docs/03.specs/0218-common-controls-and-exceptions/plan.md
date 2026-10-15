---
title: "Common Controls and Exceptions Plan"
version: "0.1.3"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-15"
layer: "specs"
artifact_id: "SPEC-0218-PLAN-0001"
parent_ids:
- "SPEC-0218"
created: "2026-10-09"
---

# Common Controls and Exceptions Plan

## Overview

Convert the schema and validator first, then fix leaves one control at a
time, each proven by a real run, then record budgets and the remaining
exceptions. Each unit is one commit.

W1–W8 below preserve the earlier source/LAB/initial-budget execution contract
and TSK-0001 evidence. P07 continues through TSK-0002, which owns criterion3's
open HOME residual and criteria6–10. Public preparation may begin now;
measurements and mutation wait for each service's exact readiness and lease.

## Scope

W1–W8 establish schema-v2 exceptions and effective-control validation with
targeted leaf, Conftest and operations changes. P07 W9–W16 reuse the root
inventory for consumer assessment, read-only observations, measured budgets
and least privilege, then reviewed leaf changes and bounded recovery/rollout;
no new LAB execution or blanket resource adjustment is included.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 2 | Schema v2, effective-control validator, quick-win retirement | None | TSK-0001 | Task evidence |
| W2 | 3 | Healthchecks the images can run | W1 | TSK-0001 | Task evidence |
| W3 | 3 | Secrets group only where a secret is read | W1 | TSK-0001 | Task evidence |
| W4 | 4 | Conftest URL-credential rule and LAB corpus | None | TSK-0001 | Task evidence |
| W5 | 2, 3 | DB templates drop all capabilities; proven leaf sets; data-group exceptions | W3 | TSK-0001 | Task evidence |
| W6 | 3 | GPU template security base and GPU exceptions | W1 | TSK-0001 | Task evidence |
| W7 | 3 | PID limits as initial budgets | W5 | TSK-0001 | Task evidence |
| W8 | 5 | Documents, ledger and changed gate | W1, W2, W3, W4, W5, W6, W7 | TSK-0001 | Task evidence |
| W9 | 6 | Admit P07; classify current root consumers, roles and demand using the existing inventory | None | TSK-0002 | Input-bound classification and blocker record |
| W10 | 7 | Public measurement schema, synthetic fixtures and bounded source assessment with TDD after W9 admission; final classification may remain blocked | W9 | TSK-0002 | RED/GREEN, refusal boundaries and meaningful coverage |
| W11 | 6, 7, 8 | Sanitized read-only baseline observations with exact attribution, read-only tool permission and a recorded window against concurrent rollout | W9, W10 | TSK-0002 | Exact target, numeric facts and observation receipts; no load or mutation |
| W12 | 7 | Measure resource/application overhead and existing GPU workloads after workload/recovery readiness | W11 | TSK-0002 | Before/after latency, throughput, OOM, throttling, PID and recovery facts |
| W13 | 8 | Prove per-service UID/capability/rootfs/secret/socket least privilege after functional/recovery readiness | W11 | TSK-0002 | Functional and negative permission evidence; no blanket mutation |
| W14 | 9 | Single-writer leaf changes and exact common-control/exception proposals after owner lease and independent review | W12, W13 | TSK-0002 | Effective root model and exact reviewed exception evidence |
| W15 | 3, 10 | Changed-service rollout, rollback, backup and empty-target recovery after exact target authorization | W14 | TSK-0002 | Actual bounded service receipts and restored usability/function |
| W16 | 9, 10 | Reconcile owned projections and current-head review/delivery after inventory integration | W9, W10, W11, W12, W13, W14, W15 | TSK-0002 | Selected registered gates, local-staged and independent reviews |

## Verification Plan

Unit tests for the validator, the Conftest verify run, real LAB runs through
`lab.py` with synthetic inputs, exact-image runs for root services that are
not running, read-only checks of running HOME containers, and the
changed-profile local gate in a clean worktree.

That paragraph describes the earlier slice; P07 runs no LAB runtime checks.
Reuse the registered ComposeControlsTests and new dedicated source tests after
their files exist. Measure representative root workloads only after recording
the service window, budgets, output sanitization and restoration boundary.
The initial helper admits bounded public numeric/JSON inputs and refuses
private environment, raw logs, credentials and ambient runtime access.

At admission main `4c83f14b11a77e13e582eb85d0bf256685472a95`, the coordinator's
official `check-operations-catalog.py` run failed with exit1 and 22 findings
in 16.593 seconds: one include drift, seven missing profile declarations,
seven Guide bindings and seven inventory membership entries for the P04
overlay. The earlier pure `validate_service_inventory` subset returned 14
findings despite its wrapper exiting0; that is a semantic FAIL, not the
official gate result. These describe the existing overlay, not seven new
services. P04/coordinator owns typed overlay projection repair without blanket
include/profile acceptance or a P04 native change. W10 requires W9's admission
substep, not completed classification or inventory GREEN. Public W9/W10 can
proceed while final inventory and full operations acceptance remain blocked.

The existing ComposeControlsTests passed 11 UNIT tests in 0.042 seconds,
exit0, at that baseline. This confirms source reuse only, with no Docker or
native execution. Actual receipts and document validation history belong in
TSK-0002; neither that UNIT result nor a fixture PASS replaces the operations
FAIL or proves measured resource or least-privilege acceptance.

Prefer exact root leaf changes. A proposed common-template change requires
a static comparison proving zero LAB effective-config delta and preservation
of existing LAB exception rows; no LAB runtime execution is authorized.

Future delivery uses one PR for its owning Spec. Before that PR merges, refresh
it to the current target head and obtain its applicable current-head CI and an
independent review. Formal Task issuance remains a logical commit on the
isolated admission branch; its reviewed SHA can start public source/synthetic
preparation, not delivery acceptance. Do not merge before the P04/coordinator
repair and relevant gates and review. Source admission is not full main-gate
acceptance.

## Risks and Recovery

### Risks and Rollback

The template changes reach HOME services only when they are recreated. The
group removal could break a service that reads or writes through group 1000;
mounts of the running services were checked, and the data-directory writers
keep the group. Rollback is a revert of the merge; recreated services then
return to their previous definitions on the next recreation.

For P07, a source revert does not restore data, privileges or application
state. Each changed service needs its own compatible rollback and verified
backup/empty-target restore plan. Preserve accepted outbox/data and other
writers. Never use whole-stack up/down, volume deletion, prune, recursive
chown, broad credential rotation or a historical recreation list as rollback.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-common-controls-and-exceptions.md)
- [P07 root resource optimization](tasks/tsk-0002-p07-root-resource-optimization.md)
