---
title: "n8n Idle Main Runner Removal Task"
version: "0.4.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-08"
layer: "specs"
artifact_id: "SPEC-0269-TSK-0001"
parent_ids:
- "SPEC-0269-PLAN-0001"
created: "2026-11-08"
---

# n8n Idle Main Runner Removal Task

## Overview

### Objective

Execute W1–W6 of the Plan: remove the idle main runner from source and records,
align the runner rehearsal with the worker broker path, rehearse, and apply in
HOME under separate approvals.

## Inputs and Authorization

On 2026-11-08, after the SPEC-0212 W68 HOME apply, the owner chose to remove
the main runner and to fix the rehearsal fixture before another rerun. The Spec
and Plan are `draft`; no implementation starts until both are approved. The
native rehearsal (W5) and the HOME change (W6) each need their own approval.

## Work Log

### Draft inputs (2026-11-08)

Observed in HOME after the W68 apply (`main` `53880ad86`):

| Probe | Result |
| --- | --- |
| `n8n-task-runner` → `n8n:5678/healthz` | HTTP 200 |
| `n8n-task-runner` → `n8n:5679` | refused; main opens no broker |
| `n8n-task-runner-worker` → `n8n-worker:5678` | refused; the worker listens only on `10.250.23.2:5679` |
| `n8n-task-runner-worker` → `10.250.23.2:5679` | HTTP 404 from the broker |
| `n8n-task-runner-worker` → `n8n:5678` | name does not resolve |

Source references to the main runner: the root and n8n Compose files, 18
references in 10 test and script files, the SEC01 `update-ledger.json` and
`release-lookups.json`, `infra/09-platform-ops/restic/sets/state-include.txt`,
`.github/workflow-contract.yml`, AD-0007, AD-0026, GDE-0077, POL-0078, the n8n
guide, policy and runbook, and the service READMEs. The fixture's
`sweep_attempt` (`tests/validation/_opsflow_native_ownership.py`) detects but
does not remove residue, and the JS sandbox globals
(`js-task-runner.js` `getNativeVariables`) include no `fetch`.

### Approval and start (2026-11-08)

The owner approved the SPEC-0269 Spec and Plan on 2026-11-08 after the draft
merged in #808. W1 starts now; W5 and W6 keep their own approvals.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0269 | draft | approved | #approval-and-start-2026-11-08 |
| SPEC-0269-PLAN-0001 | draft | approved | #approval-and-start-2026-11-08 |
| SPEC-0269-TSK-0001 | draft | ready | #approval-and-start-2026-11-08 |
| SPEC-0269-TSK-0001 | ready | in-progress | #approval-and-start-2026-11-08 |

### W1 main-side runner need (2026-11-08)

Read offline (`--network none`) from the HOME n8n image
`sha256:222a7fd94f47…` (`/usr/local/lib/node_modules/n8n/dist`, 2.43.6):
`commands/start.js:152-158` sets `needsTaskRunner = false` when
`executions.mode` is `queue` and `OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS` is
`true`; `commands/base-command.js:163-169` starts the task-runner module only
when `needsTaskRunner` is set; and `workflow-runner.js:307-309` enqueues every
execution, manual included, under the same setting. Main therefore never runs
a Code node or opens a broker, which matches the HOME observation, and the
main runner has no consumer. The owner's HOME Code node test on 2026-11-08
ran executions 122–125 on `n8n-worker` with the worker's JS and Python task
runners registering and no runner error (SPEC-0212 TSK-0042).

### W1–W3 implementation (2026-11-08)

W1 test first: `test_main_has_no_runner_while_manual_executions_are_offloaded`
in `tests/validation/test_p03_runner_isolation.py` failed on the current
source. W1 then removed the `n8n-task-runner` service, main's
`N8N_RUNNERS_BROKER_LISTEN_ADDRESS` and `n8n_main_runner_net` attachment, and
the root `n8n_main_runner_net` network. Main keeps its `n8n_runner_auth_token`
grant, because the shared `N8N_RUNNERS_AUTH_TOKEN_FILE` setting would otherwise
point at a missing file; it keeps its broker port and `expose`, which do
nothing while main starts no runner. The detached `n8n-task-runner-data` volume
declaration and its restic line stay, as the existing tests require for
rollback data identity. Tests that listed the main runner now list the worker
runner only (runtime compatibility, outbox placement, version bundle and the
SPEC-0267 listener table).

W2: the n8n source binding in `update-ledger.json` and `build-inputs.json` was
archived and rehashed. In `update-ledger.json` the `n8n-task-runner` row moved
unchanged into a new `source_refreshes` entry (`removed_services`,
`removed_entries`), `expected_services` dropped it, and
`p08_public_release_observations` records the denominator change in
`removed_root_service_mapping`, as SPEC-0262 did for relocated LAB services.
Rows in `release-lookups.json` and `verification.json` that name the service
are dated observation records and stay. `test_update_gates` has 58 failures on
`main` from source hash drift that predates this Task; after W2 it has 57, the
main runner's own row failure resolved and no new failure.

W3: AD-0007, AD-0026, GDE-0077, GDE-0053, RUN-0053, POL-0054, POL-0078, the
n8n, 07-workflow and Grafana READMEs, and the m0021 inventory describe the
worker-only runner; GDE-0077 and AD-0026 keep `10.250.22.0/24` out of reuse.

### W4 fixture (2026-11-08)

Written by a delegated agent and reviewed here; static tests came first.
`start_worker_broker_topology` builds `ctl` and `runner` networks only:
Postgres and Valkey on `ctl`, main on `ctl` with `EXECUTIONS_MODE=queue`,
`OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS=true` and no broker setting, the worker
on `ctl` and `runner` with the broker, and the runner on `runner` with
`http://n8n-worker:5679`; every registration wait reads the worker log. The
peer step runs busybox `wget` from the runner container against `n8n:5678`
and `n8n-worker:5678`: an HTTP status line fails the step, resolution failure,
refusal, timeout or no route pass, and anything else is TEST_RESIDUAL. The
wrong-token step baselines the worker log, then waits up to 30 s for a
refusal class (`unauthorized`, `forbidden`, `invalid_token`,
`unauthenticated`, `http_401`, `http_403`) in the runner log or a new one in
the worker log; a registration fails it, and registration is checked again
after the wrong runner is removed. Shared cleanup removes swept ids only after
re-checking their identity and owner and attempt labels, then re-sweeps after
2, 3 and 5 seconds; an ambiguous create always earns one delayed re-sweep, and
PASS needs an empty last sweep. Remaining fixture differences:
`shared_internal_ctl_network`, `worker_broker_listens_on_all_interfaces`,
`runner_network_without_home_ipam_or_gateway_mode`, `fixture_specific_tmpfs`
and `fixture_specific_resource_caps`. No denial category, needle, allowed
category map or attribution gate changed.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W1 | Draft HOME probes and source reference count | `main` `53880ad86`, HOME | NOT_RUN | Draft input only | optional | - |
| E2 | 1 | W1 | Source read of main's task-runner start in queue offload mode | n8n 2.43.6 image `sha256:222a7fd94f47…` | PASS | "W1 main-side runner need" | required | - |
| E3 | 1 | W1 | `test_main_has_no_runner_while_manual_executions_are_offloaded` before and after; `validate-docker-compose.sh`; `check-all-hardening.sh`; 11 related suites | `1c6625973` then this branch | PASS | 1 failure before; 430 tests OK after, 34 opt-in skips; 65 selections valid (323 services); all hardening tiers pass | required | - |
| E4 | 2 | W2 | Source binding rehash and `test_update_gates` against `main` | This branch | PASS | Version bundle tests OK; update gates 57 failures, all present on `main` (58), none new | required | - |
| E5 | 3 | W3 | Operations catalog, metadata and lifecycle checks | This branch | PASS | `check-operations-catalog.py` PASS after the m0021 re-render and POL-0078 rows | required | - |
| E6 | 4 | W4 | Static fixture tests before and after | `eb2c5886b` then this branch | PASS | RED: `test_p03_runner_boundaries` 10 failures and 1 error, `test_opsflow_native_boundaries` 3 failures and 2 errors (late-listed container reported PASS); GREEN: 12 related suites 162 tests OK, 2 native skips; `ruff` clean | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | E2, E3 | Source change done; awaiting owner acceptance | @buenhyden |
| 2 | pending | E4 | Records updated; pre-existing ledger drift is outside this Task | @buenhyden |
| 3 | pending | E5 | Documents updated; awaiting owner acceptance | @buenhyden |
| 4 | pending | E6 | Fixture changed and statically tested; native proof is W5 | @buenhyden |
| 5 | pending | - | Awaiting W5 and its approval | @buenhyden |
| 6 | pending | - | Awaiting W6 and its approval | @buenhyden |

## Review and Completion

W1–W4 are done in source. The owner approved W5 and W6 in Plan order on 2026-11-08.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [SPEC-0212 TSK-0042](../../0212-request-baseline-and-reconciliation/tasks/tsk-0042-models-runners-wiki.md)
