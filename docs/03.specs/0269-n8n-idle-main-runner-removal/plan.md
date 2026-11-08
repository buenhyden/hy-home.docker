---
title: "n8n Idle Main Runner Removal Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-08"
layer: "specs"
artifact_id: "SPEC-0269-PLAN-0001"
parent_ids:
- "SPEC-0269"
created: "2026-11-08"
---

# n8n Idle Main Runner Removal Plan

## Overview

Remove the idle n8n main runner and align the runner rehearsal with the worker
broker path, then apply in HOME.

## Scope

The service, network, records, fixture and exclusions of SPEC-0269. Source and
test changes are reviewed first; the native rehearsal and the HOME change each
need their own approval.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Remove the service, main's runner network and broker settings, and the network; add the offload render test with RED evidence | None | TSK-0001 | `test_p02_service_contracts`, `test_p03_runner_isolation`, `validate-docker-compose.sh` |
| W2 | 2 | Archive and rebind the SEC01 ledger and release lookups, and update the restic set, workflow contract and inventories | W1 | TSK-0001 | Supply-chain, update-gate, operations-catalog and workspace inventory checks |
| W3 | 3 | Update AD-0007, GDE-0077, POL-0078 and the n8n guide, policy, runbook and READMEs | W1 | TSK-0001 | Metadata, link and operations-catalog checks |
| W4 | 4 | Fixture: worker broker topology, container-level peer probe, wrong-token refusal evidence, late-listed container re-sweep, with static tests | None | TSK-0001 | `test_p03_runner_boundaries`, `test_p03_runner_isolation`, `test_opsflow_native_rehearsal` static tests |
| W5 | 5 | Native rehearsal under its own approval | W4 | TSK-0001 | Receipt recorded in the Task |
| W6 | 6 | HOME removal under its own approval, with checks and a rollback rehearsal | W1, W2, W3, W5 | TSK-0001 | Live observations recorded in the Task |

## Verification Plan

Each criterion closes only on PASS evidence for its Work Unit. W1 and W4 tests
are written first and shown to fail on the current source. W5 and W6 stay
NOT_RUN until approved.

## Risks and Recovery

### Risks and Rollback

- A part of n8n main still needs a runner in offload mode: W1 reads the n8n
  2.43.6 source for main-side code execution first, and W6 checks Code nodes
  after the removal.
- The SEC01 ledger rejects a removed service: W2 follows the existing archive
  form for retired bindings.
- Rollback is the previous revision's render, which recreates the runner and
  its network.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-n8n-idle-main-runner-removal.md)
