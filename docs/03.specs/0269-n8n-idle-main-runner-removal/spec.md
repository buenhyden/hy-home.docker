---
title: "n8n Idle Main Runner Removal Specification"
version: "0.2.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-08"
layer: "specs"
artifact_id: "SPEC-0269"
parent_ids:
- "REQ-0023"
- "AD-0007"
created: "2026-11-08"
---

# n8n Idle Main Runner Removal Specification

## Overview

### Intent

The n8n main container has no task runner, because it never runs code in
offload mode, and the runner rehearsal proves the worker broker path that HOME
uses, with positive evidence for each step and a cleanup that cannot report a
leftover container as clean.

### Background

SPEC-0212 TSK-0042 W68 applied runner isolation in HOME on 2026-11-08. n8n
main runs `EXECUTIONS_MODE=queue` with `OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS=true`
and opens no broker on `5679`; its runner `n8n-task-runner` waits for a broker
indefinitely, as it did before the change (Loki, 2026-11-02). That idle runner
shares `n8n_main_runner_net` with main and reaches main's `5678` UI and REST
API (HTTP 200 from the runner container), while the worker runner reaches only
the worker broker. The native rehearsal (`opsflow-native-b675571b…`) passed
with two TEST_RESIDUAL steps: `peer_nonbroker_port` never tested the network,
because the JS sandbox has no `fetch`, and `wrong_token_registration` only
checked that no registration appeared within 3 seconds. Its fixture models a
main broker, which HOME no longer uses. An earlier attempt under host load
left a `secret-prep` container that the daemon listed only after cleanup's
label sweep, so the receipt said `cleanup: PASS`. On 2026-11-08 the owner chose
to remove the main runner and to fix the fixture before another rerun.

## Scope

### In Scope

- Removing the `n8n-task-runner` service, main's `n8n_main_runner_net`
  attachment and broker settings, and the network itself.
- A render test that keeps `OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS=true` while no
  main runner exists.
- The SEC01 security-update ledger, release lookups, restic set, workflow
  contract, service inventory, AD-0007, GDE-0077 and the n8n documents.
- The native fixture: a worker broker topology, a container-level non-broker
  peer probe, positive evidence for wrong-token refusal, and a bounded
  re-sweep that adopts and removes late-listed owned containers.

### Out of Scope

- Turning offload off or changing the worker runner.
- The n8n image, version or credentials.

## Contracts

### Normal Behavior

- Main starts without a runner and serves its UI, API and queue as before.
- The worker runner registers with the worker broker and runs Code nodes.
- The rehearsal reports each step from a positive observation.

### Error Behavior

- A render that keeps a main runner, or that turns offload off without one,
  fails the test.
- A runner container that reaches a non-broker port fails the peer step.
- A wrong runner token that registers fails the rehearsal.
- An owned container that appears after cleanup's first sweep is adopted and
  removed, or cleanup reports FAIL.

### Boundary Behavior

- Ledger history for the removed service is archived, not deleted.

### Constraints

- No secret value is printed or committed.
- GDE-0077 stops listing `n8n_main_runner_net` (`10.250.22.0/24`) and the
  range is not reused (ADR-0055).

## Acceptance Criteria

1. The render has no `n8n-task-runner` and no `n8n_main_runner_net`, main has
   no broker setting, and a test pins offload while no main runner exists.
2. The SEC01 ledger, release lookups, restic set, workflow contract and
   inventories no longer bind the removed service, with its history archived.
3. AD-0007, GDE-0077, POL-0078 and the n8n documents describe the worker-only
   runner.
4. The fixture rehearses the worker broker path; the peer step probes the
   network from the runner container; the wrong-token step records the
   broker's refusal; cleanup adopts or reports a late-listed owned container.
5. A native rehearsal under its own approval passes with no TEST_RESIDUAL step
   other than those the owner accepts.
6. In HOME, under its own approval, the main runner is removed; main and the
   worker stay healthy, the worker runner still registers, and a rollback is
   rehearsed.

## Failure Conditions

### Observable Failures

- Main or the worker fails to start, or a Code node fails, after the removal.
- The ledger or inventory checks fail on the removed service.

### Stop Boundaries

- Stop before any HOME change or native rehearsal without its own approval.
- Do not weaken a rehearsal step to make it pass.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-n8n-idle-main-runner-removal.md)
- [SPEC-0212 TSK-0042](../0212-request-baseline-and-reconciliation/tasks/tsk-0042-models-runners-wiki.md)
- [SPEC-0267](../0267-secondary-listener-hardening/spec.md)
- [AD-0007](../../02.architecture/descriptions/0007-workflow-architecture.md)
- [REQ-0023](../../01.requirements/0023-standardize-infra-net.md)
- [GDE-0077](../../05.operations/guides/02-gateway-and-networking/0077-ip-address-management.md)
