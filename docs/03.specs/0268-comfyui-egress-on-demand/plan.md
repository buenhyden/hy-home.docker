---
title: "ComfyUI Egress on Demand Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-08"
layer: "specs"
artifact_id: "SPEC-0268-PLAN-0001"
parent_ids:
- "SPEC-0268"
created: "2026-11-08"
---

# ComfyUI Egress on Demand Plan

## Overview

Take ComfyUI's outbound access out of the default render and attach it through
an opt-in overlay during maintenance windows.

## Scope

The network, overlay, documents and exclusions of SPEC-0268. Source and test
changes are reviewed as one unit; HOME recreation is a separate, separately
approved step.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Read ComfyUI's entrypoint, ComfyUI-Manager start-up behavior and the installed custom nodes for outbound calls at start and at workflow run time | None | TSK-0001 | Dependency table in the Task with a source per row |
| W2 | 2, 3 | Remove `comfyui_egress_net` and the loopback port from the default ComfyUI service and add the opt-in overlay | W1 | TSK-0001 | Default and overlay renders; `validate-docker-compose.sh`; `check-all-hardening.sh` |
| W3 | 4 | Add the render tests, with RED evidence before W2 | W1 | TSK-0001 | `test_p02_service_contracts` and the affected wiring suites |
| W4 | 5 | Update RUN-0081, the ComfyUI README, GDE-0077 and the operations inventory | W2, W3 | TSK-0001 | Metadata, link and operations-catalog checks |
| W5 | 6 | Recreate ComfyUI in HOME under its own approval; check health, route, data and refusal; rehearse attach and detach | W2, W3, W4 | TSK-0001 | Live observations recorded in the Task |

## Verification Plan

Each criterion closes only on PASS evidence for its Work Unit. W3's tests are
written first and shown to fail on the current render. W5 needs the owner's
approval and a recorded previous state; until then it stays NOT_RUN.

## Risks and Recovery

### Risks and Rollback

- ComfyUI or a custom node needs outbound access at start: W1 looks for it
  first, and W5 checks start-up and a local workflow before closing.
- An operator forgets to detach after maintenance: the README step ends with
  a recreate on the default render, and W5 rehearses it.
- Rollback is the previous revision's render, which attaches
  `comfyui_egress_net` again; ComfyUI's data volumes do not change.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-comfyui-egress-on-demand.md)
