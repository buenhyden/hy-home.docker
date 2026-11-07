---
title: "Secondary Listener Hardening Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-07"
layer: "specs"
artifact_id: "SPEC-0267-PLAN-0001"
parent_ids:
- "SPEC-0267"
created: "2026-11-07"
---

# Secondary Listener Hardening Plan

## Overview

Bind six unauthenticated secondary listeners to consumer-only addresses, add
Grafana metrics authentication, declare the Pyroscope and ComfyUI data volumes, and
record the exposures that stay.

## Scope

The listeners, consumers, files and exclusions of SPEC-0267. Source and test
changes are reviewed as one unit; HOME recreation is a separate, separately
approved step.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 6 | Read each listener's bind setting, consumers and health checks from source; choose its network and fixed address; write the accepted-risk records | None | TSK-0001 | Inventory table in the Task with a source line per row |
| W2 | 2, 3, 4 | Declare the networks and addresses, set each bind option, move consumers and health checks, add Grafana metrics authentication, declare the Pyroscope metastore volume and the ComfyUI state mounts | W1 | TSK-0001 | All-profile public render; `validate-docker-compose.sh`; `check-all-hardening.sh` |
| W3 | 5 | Add the render tests, with RED evidence before W2 | W1 | TSK-0001 | `test_p02_service_contracts` and the affected wiring suites |
| W4 | 6 | Update GDE-0077 and the affected READMEs | W2, W3 | TSK-0001 | Metadata, link and operations-catalog checks |
| W5 | 7 | Recreate the affected HOME services under their own approval, copy the Pyroscope and ComfyUI data after a backup, and check consumers, refusal and rollback | W2, W3, W4 | TSK-0001 | Live observations recorded in the Task |

## Verification Plan

Each criterion closes only on PASS evidence for its Work Unit. W3's tests are
written first and shown to fail on the current render. W5 needs the owner's
approval and a recorded previous state; until then it stays NOT_RUN.

## Risks and Recovery

### Risks and Rollback

- A health check or consumer still uses the old address: W1 names every one,
  and the change is one revertible commit.
- The Traefik ping health check may not reach an address-bound entrypoint:
  W1 tests it before W2 binds the entrypoint.
- A Pyroscope or ComfyUI data copy loses data: W5 copies from a verified
  backup and keeps the anonymous volume until the new volume is shown to work.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-secondary-listener-hardening.md)
