---
title: "OpenBao Maintenance Window Readiness Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "specs"
artifact_id: "SPEC-0243-TSK-0001"
parent_ids:
- "SPEC-0243-PLAN-0001"
created: "2026-10-14"
---

# OpenBao Maintenance Window Readiness Task

## Objective

Make RUN-0085's maintenance window executable, as SPEC-0243 states.

## Inputs and Authorization

- **Request:** on 2026-10-14 the owner asked to review the maintenance window,
  then to review and proceed, and chose "readiness Spec 작성"
  (AskUserQuestion).
- **Baseline:** branch `claude/single-admin-host-custody` (PR #478) on
  `main` `4421d30f1`, because both change RUN-0085.
- **Not done:** no window step, HOME change or secret read. W0's read-only
  commands ran on 2026-10-14 (below).

## Work Log

### W0 Read-only Observation

On 2026-10-14 the security Compose validation passed (2 services);
`bao status` showed initialized, unsealed, active, Raft, version 2.6.2; the
pinned owned image is present locally with digest `46bf9b5c3ae3`; the system
disk is 88% used with 29 GB free; the last backup run (03:43 KST) failed only
on the known missing snapshot token; the audit and data directories match
their recorded device and inode; `/etc/logrotate.d/openbao` is absent. W0's
own image check matched nothing, because it searched `^openbao/openbao`
while the pin is `hy-home/openbao`; SPEC-0242 fixed it.

### W1 Window Text

From the `iac-reviewer` review, RUN-0085 (0.12.0) now states:

- SEC01's actual status for the owned image: admitted only for the next
  bounded native validation, HOME acceptance (criterion 15) pending.
- W0 prerequisites: pause or avoid the daily backup timer; deploy the Traefik
  CA mount before W4 (D1); compare running and declared Prometheus, Gatus and
  Traefik; decide on OpenBao-down alerts during W4.
- A new W1c that applies the renderer policies and token roles with root
  before W3 (D2), BLOCKED until a reviewed command exists.
- W4: stop if either the W3b receipt or the W3a restore is missing, record
  the Raft mount identity before and after, never confirm Compose's volume
  recreate prompt, and do not open W4 until a cut-over procedure or a
  fix-forward decision is recorded.
- W5: create the Agent with `up --no-start` so the helper finds it stopped,
  and recreate Prometheus with `up -d` only when its running image matches
  the pin, instead of `restart`, which cannot apply the CA mount (D4).
- Step 6 names the tracked restore tool and its likely image failure (D3).

The OpenBao README now lists `obs_net` for the Agent.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Readiness review | 7 | W1 | Independent `iac-reviewer` readiness review of RUN-0085 0.10.4: NOT READY | `f0984f3c0` | FAIL | Inputs and Authorization | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | pending | - | - |
| 2 | pending | - | - |
| 3 | pending | - | - |
| 4 | pending | - | - |
| 5 | pending | - | - |
| 6 | pending | - | - |
| 7 | pending | - | - |

## Review and Completion

No criterion is accepted until the owner accepts it. The window stays
NOT READY.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
