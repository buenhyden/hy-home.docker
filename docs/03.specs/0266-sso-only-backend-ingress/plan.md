---
title: "SSO-Only Backend Ingress Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-07"
layer: "specs"
artifact_id: "SPEC-0266-PLAN-0001"
parent_ids:
- "SPEC-0266"
created: "2026-11-07"
---

# SSO-Only Backend Ingress Plan

## Overview

Move each SSO-only Traefik backend off the shared `edge_net` onto its own
internal ingress network, after first confirming from source which backends
qualify and which flows they need.

## Scope

The in-scope backends, flows, files and exclusions of SPEC-0266. Source and
test changes come first and are reviewed as one unit; HOME recreation is a
separate, separately approved step.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Read each `edge_net` backend's configuration for its own authentication and every inbound/outbound flow, and record the confirmed in-scope list and the `edge_net`-only flows | None | TSK-0001 | Inventory table in the Task with a source line per row |
| W2 | 2, 3 | Declare the ingress and flow networks in the root Compose, move each in-scope backend and set `traefik.docker.network`, attach Traefik and flow peers | W1 | TSK-0001 | All-profile public render; `validate-docker-compose.sh`; `check-all-hardening.sh` |
| W3 | 4 | Add the render test for ingress isolation and flow peers, with RED evidence before W2 | W1 | TSK-0001 | `test_p02_service_contracts` and the affected wiring suites |
| W4 | 5 | Update GDE-0077, AD-0026 and the affected READMEs; move ADR-0061 to accepted | W2, W3 | TSK-0001 | Metadata, link and operations-catalog checks |
| W5 | 6 | Recreate the affected HOME services under their own approval; check SSO routes, direct-reach refusal, flows and rollback | W2, W3, W4 | TSK-0001 | Live observations recorded in the Task |

## Verification Plan

Each criterion closes only on PASS evidence for its Work Unit. W3's test is
written first and shown to fail on the current render. W5 needs the owner's
approval, a maintenance window and the recorded previous network membership;
until then it stays NOT_RUN.

## Risks and Recovery

### Risks and Rollback

- A route breaks after the move: the network change is one revertible commit,
  and W5 records the previous membership so `docker compose up -d` of the
  previous revision restores it.
- A flow missed by W1 breaks: W1 must name every flow before W2 starts, and W5
  checks each one.
- Traefik joins many networks: each is internal and explicitly addressed, and
  the render test bounds Traefik's peers on each.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-sso-only-backend-ingress.md)
- [ADR-0061](../../02.architecture/decisions/0061-dedicated-ingress-for-sso-only-backends.md)
