---
title: "RedisInsight Valkey Inspection Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0223-PLAN-0001"
parent_ids:
- "SPEC-0223"
created: "2026-10-09"
---

# RedisInsight Valkey Inspection Plan

## Overview

Measure what RedisInsight needs, add the inspector roles and MNG ACL, close the
listener and register the connections, rehearse, document, roll out on HOME,
review the consumers, and validate.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | DEV inspector role and service-role table | None | TSK-0001 | Task evidence |
| W2 | 1 | MNG Valkey rendered ACL and inspector | W1 | TSK-0001 | Task evidence |
| W3 | 2 | RedisInsight listener, networks, pre-set connections, encryption, health | W1, W2 | TSK-0001 | Task evidence |
| W4 | 2 | Isolated rehearsal | W3 | TSK-0001 | Task evidence |
| W5 | 3, 4 | Guide, Policy, Runbook, READMEs; HOME rollout; consumer review | W4 | TSK-0001 | Task evidence |
| W6 | 5 | Changed gate, staged style check, candidate quality, merge | W5 | TSK-0001 | Task evidence |

## Verification Plan

Renderer unit tests, secret metadata and operations catalog checks, the
isolated rehearsal against the pinned images, HOME probes without secret
output, a client inventory of both Valkey servers, the changed gate, the staged
style check and the remote candidate.

## Risks and Rollback

- Recreating MNG Valkey drops every shared connection for a few seconds; AOF
  keeps the data and consumers reconnect.
- The first database request after RedisInsight starts can exceed the request
  timeout; checks retry once.
- Rollback: revert the commits and recreate the three services; restore
  RedisInsight `/data` from the owner-only copy taken before the rollout.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-redisinsight-valkey-inspection.md)
