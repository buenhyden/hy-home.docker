---
title: "Observability CA Execution Plan"
version: "0.1.2"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-21"
layer: "specs"
artifact_id: "SPEC-0245-PLAN-0001"
parent_ids:
- "SPEC-0245"
created: "2026-10-16"
---

# Observability CA Execution Plan

## Overview

Run the two services in fixed order: Prometheus, then Gatus. Each service must
pass its own backup and isolated restore gate before its CA recreation. No
execution command is inferred from this Plan: the operation owner records the
reviewed, exact command selection in the Task before running it.

## Scope

W1 establishes a value-free preflight contract. W2 and W3 complete the
Prometheus and Gatus backup/isolated-restore gates before any CA recreation.
W4 then recreates Prometheus and W5 recreates Gatus. W6 records stop or
rollback outcomes. W7 obtains independent review and selected checks. The Plan
does not execute the OpenBao window, use OpenBao secrets, change a certificate,
or select services beyond the two named targets.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 7 | Record current-host and two-service value-free preflight identities, isolation design, and stop gates | None | TSK-0001 | Operations implementer record; independent review |
| W2 | 2, 7 | Create and prove a reviewed Prometheus consistent backup through isolated restore; retain the installed v3.15.0 identity | W1 | TSK-0001 | Operations implementer evidence; QA verification |
| W3 | 3, 4, 7 | Create and prove a reviewed Gatus SQLite backup; create the no-network/no-pull minimal delta image with `FROM` the exact current running immutable base and `COPY` only the tracked CA-aware entrypoint, leaving the binary unchanged | W1 | TSK-0001 | Operations implementer evidence; IaC, security, and QA review |
| W4 | 5, 6, 7 | Apply the reviewed Prometheus CA selection and recreate only Prometheus after both W2 and W3 PASS | W2, W3 | TSK-0001 | Operations implementer evidence; QA verification |
| W5 | 5, 6, 7 | Apply the reviewed Gatus CA selection and recreate only Gatus after W4 PASS | W3, W4 | TSK-0001 | Operations implementer evidence; QA verification |
| W6 | 6 | Record a stopped service path or reviewed rollback when a gate fails | W1, W2, W3, W4, W5 | TSK-0001 | Sanitized Task evidence |
| W7 | 7 | Independent operational, security, and recovery reviews; selected source and document checks | W1, W2, W3, W4, W5, W6 | TSK-0001 | QA, IaC, and security evidence |

## Verification Plan

- Before each service action, compare the preflight identity with current
  Compose, image, mount, and persistent-data boundary; stop on a mismatch.
- Use a reviewed, service-specific consistent backup method and a separate
  Compose/storage definition for an isolated restore. The isolated target must
  have no production data path, route, external network, notification delivery,
  remote-write, or production credential attachment.
- Verify restored state with bounded health/readiness and data-shape checks;
  do not copy payloads into the Task.
- Recreate exactly one service only after its own recovery gate. Verify health,
  intended CA consumer behavior, and the recorded image/mount identity.
- Capture only sanitized durable receipts in the Task. Keep private operation
  artifacts in the QA-selected protected custody path; an ignored, mode-0700
  repository-local path is permissible when its custody review approves it.

## Risks and Recovery

### Risks and Rollback

- **Prometheus data loss or incompatible restore.** Preserve the installed v3.15.0
  identity and stop before recreation until the service-specific backup and
  isolated restore pass. Never delete or manually manipulate TSDB/WAL files.
- **Gatus image trust gap.** A same-image recreation cannot prove CA handling.
  Build a no-network/no-pull delta from the exact current immutable image,
  copying only the reviewed tracked CA-aware entrypoint; record the delta and
  old immutable identities and use a one-service image override for rollback.
- **SQLite inconsistency.** Do not copy a live SQLite database as proof. Use
  reviewed quiescence or an approved consistent backup method, then restore
  only into the isolated target.
- **Service failure.** Stop before the next service. Use only the recorded,
  reviewed rollback path; retain production volume and evidence for escalation.
- **Rollback.** Restoring source or an image does not replace data. A
  production-data replacement needs a new explicit approval after a successful
  isolated rehearsal and review.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-observability-ca-execution.md)
