---
title: "AI Runtime Pin Verification Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0226-PLAN-0001"
parent_ids:
- "SPEC-0226"
created: "2026-10-10"
---

# AI Runtime Pin Verification Plan

## Overview

Record the source facts, pin and bound the runtime, rehearse restore and
features in isolation, roll the two services out on HOME, document and
validate.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Releases, digests, licences, advisories, CUDA and driver facts | None | TSK-0001 | Task evidence |
| W2 | 2 | Digest pins, projection, Renovate, Ollama and WebUI limits, contract tests | W1 | TSK-0001 | Task evidence |
| W3 | 3 | Ollama catalog in the state set; isolated WebUI and catalog restore | W2 | TSK-0001 | Task evidence |
| W4 | 4 | Isolated feature rehearsal; GPU memory and load measurement | W2 | TSK-0001 | Task evidence |
| W5 | 5 | Key preservation, persisted-setting fix, HOME recreation and checks; Stage 05 documents | W3, W4 | TSK-0001 | Task evidence |
| W6 | 6 | Changed gate, staged style check, candidate quality, merge | W5 | TSK-0001 | Task evidence |

## Verification Plan

Registry and upstream queries, contract tests, Compose rendering, the
isolated restore and feature rehearsals, the GPU measurement, HOME health and
log checks, the changed gate, the staged style check and the remote
candidate.

## Risks and Rollback

- Recreating Open WebUI signs users out unless the running key is copied into
  the volume first; the rollout copies it before recreation.
- Recreating Ollama unloads models; the next request reloads from the HDD.
- Image rollback: the previous digests are recorded in the Task. Open WebUI
  v0.11.3 has the same migration head, so it needs no data restore but brings
  back four fixed advisories. Data restore uses the restic state set.
- Rollback of this change: revert the commits and recreate the two services.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-ai-runtime-pin-verification.md)
