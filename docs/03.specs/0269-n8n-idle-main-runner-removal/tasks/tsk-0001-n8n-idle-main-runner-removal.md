---
title: "n8n Idle Main Runner Removal Task"
version: "0.2.0"
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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W1 | Draft HOME probes and source reference count | `main` `53880ad86`, HOME | NOT_RUN | Draft input only | optional | - |
| E2 | 1 | W1 | Source read of main's task-runner start in queue offload mode | n8n 2.43.6 image `sha256:222a7fd94f47…` | PASS | "W1 main-side runner need" | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | Awaiting W1 | @buenhyden |
| 2 | pending | - | Awaiting W2 | @buenhyden |
| 3 | pending | - | Awaiting W3 | @buenhyden |
| 4 | pending | - | Awaiting W4 | @buenhyden |
| 5 | pending | - | Awaiting W5 and its approval | @buenhyden |
| 6 | pending | - | Awaiting W6 and its approval | @buenhyden |

## Review and Completion

W1 source read done; the source removal follows.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [SPEC-0212 TSK-0042](../../0212-request-baseline-and-reconciliation/tasks/tsk-0042-models-runners-wiki.md)
