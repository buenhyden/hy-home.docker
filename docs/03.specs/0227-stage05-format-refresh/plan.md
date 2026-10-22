---
title: "Stage 05 Format Refresh Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-22"
layer: "specs"
artifact_id: "SPEC-0227-PLAN-0001"
parent_ids:
- "SPEC-0227"
created: "2026-10-10"
---

# Stage 05 Format Refresh Plan

## Overview

Add the validator rule first, convert the documents in subject batches with
one writer per file, repair links and bindings, then verify the full list.

## Scope

W1 defines section-shape validation; W2 restructures the tracked Guide,
Policy and Runbook bodies in subject batches; W3 repairs renamed anchors and
service bindings. W4–W5 compare the processed corpus and content-loss account
before review and gates, preserving README profiles, incidents, archives and
historical Task links.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Profile flags, schema, validator and unit tests | None | TSK-0001 | Task evidence |
| W2 | 2, 3 | Nine subject batches, one commit each (ten with the returned files) | W1 | TSK-0001 | Task evidence |
| W3 | 4 | Inbound anchors and Guide service bindings | W2 | TSK-0001 | Task evidence |
| W4 | 2, 3 | Full-list section, lint, metadata, language and content-loss audit | W3 | TSK-0001 | Task evidence |
| W5 | 5 | Review, changed gate, staged style check, candidate quality, merge | W4 | TSK-0001 | Task evidence |

## Verification Plan

The rule's unit tests, a direct run of the rule over all 230 files,
markdownlint, the metadata, link and operations catalog checks, a
before-and-after comparison of fenced blocks, links and inline code per
subject, an independent review, the changed gate, the staged style check and
the remote candidate.

## Risks and Recovery

### Risks and Rollback

- Batch agents worked in parallel; each owned disjoint files and none ran Git,
  and every batch was checked again before its commit.
- A restructure can drop content; the loss audit compares every file with
  `origin/main` and a reviewer samples the result.
- Renamed anchors can break links; the full link check runs after all batches.
- Rollback: revert the commits; documents only, no runtime change.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-stage05-format-refresh.md)
