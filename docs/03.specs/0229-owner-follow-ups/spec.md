---
title: "Owner Follow-ups"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0229"
parent_ids:
- "REQ-0026"
- "ADR-0041"
created: "2026-10-10"
---

# Owner Follow-ups

## Overview

Three items left open by SPEC-0226 and SPEC-0228 were approved by the owner
on 2026-10-10: the repeated Keycloak refresh errors from
`storybook-mcp-client`, the Grype scan of the pinned AI images, and the
missing OpenBao snapshot token that makes every backup skip the Raft
snapshot. The Ollama model store stays on the HDD.

## Scope

In scope: diagnosing the refresh errors and documenting the client-side fix,
making the Grype database seed accept the current database and scanning the
two images offline, and giving the owner exact commands to issue the snapshot
token. Out of scope: changing user-global Codex settings, committing a network
approval, holding or using the OpenBao admin token, and changing image pins.

## Contracts

1. Storybook MCP refresh errors are fixed on the client by signing in again;
   GDE-0101 names the symptom and the commands.
2. The Grype seed cap fits the current database; the tracked approval surface
   still grants nothing.
3. RUN-0021 issues the snapshot token with the admin token passed on stdin only,
   never echoed or stored, and proves the new token with one snapshot.

## Acceptance Criteria

1. The source of the refresh errors is identified and the fix documented.
2. Both pinned AI images are scanned and the results recorded.
3. The snapshot-token commands parse and follow the backup's token handling.
4. The changed gate, the staged style check and `candidate-quality` pass.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-owner-follow-ups.md)
