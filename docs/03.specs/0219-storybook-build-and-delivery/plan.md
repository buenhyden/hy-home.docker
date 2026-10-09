---
title: "Storybook Build and Delivery Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0219-PLAN-0001"
parent_ids:
- "SPEC-0219"
created: "2026-10-09"
---

# Storybook Build and Delivery Plan

## Overview

Fix the build contract first, then the ingress regression, then the shared
UI, then the dependencies, the remote MCP, the design export and the
documents; build the images from the last source commit, pin them, and prove
them in the rehearsal. Each unit is one commit.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Commit-only build context, revision record, image script | None | TSK-0001 | Task evidence |
| W2 | 2 | Storybook ingress rehearsal and static pin checks | W1 | TSK-0001 | Task evidence |
| W3 | 3 | Tokens, Button and AsyncState states, a11y errors, example removal | None | TSK-0001 | Task evidence |
| W4 | 3 | Latest dependencies on TypeScript 6.0.3; TypeScript 7 trial | W3 | TSK-0001 | Task evidence |
| W5 | 2, 3, 4, 5 | Remote docs MCP, design export and documents | W1, W2, W3 | TSK-0001 | Task evidence |
| W6 | 1, 2 | Build, push and pin both images; run the rehearsal | W5 | TSK-0001 | Task evidence |
| W7 | 5 | Changed gate and task evidence | W6 | TSK-0001 | Task evidence |

## Verification Plan

Unit tests for the image script, design export and token parity; Node tests
for the artifacts and the MCP authorization; Storybook story tests in
Chromium; lint, type and build checks; a real build pushed to the local
registry with attestation checks; the Storybook ingress rehearsal with real
Traefik, OAuth2 Proxy and Keycloak; and the changed-profile local gate.

## Risks and Rollback

The Button API changes incompatibly in 0.2.0; no consumer exists yet. The
remote MCP is reachable only after the operator creates the Keycloak client
and starts the profile; until then it is inert. Rollback is a revert of the
merge and, on HOME, the previous image pins.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-storybook-build-and-delivery.md)
