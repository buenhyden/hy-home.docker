---
title: "REQ-0027 Approval Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0261"
parent_ids:
- "REQ-0026"
- "AD-0030"
created: "2026-11-04"
---

# REQ-0027 Approval Specification

## Overview

### Intent

REQ-0027 stayed draft, and AD-0031, AD-0032 and nine Stage 05 documents under
it stayed draft only because of that parent. The owner approved REQ-0027, so
this change approves it and promotes the dependent documents that match the
implementation.

### Background

On 2026-11-04 the owner decided "REQ-0027 승인". Earlier the same day the owner
chose "Review, then promote (recommended)" for documents that are implemented
but still draft. SPEC-0259 left these documents draft and named the REQ-0027
decision as the unblocker.

## Scope

### In Scope

- REQ-0027 draft to approved, with its draft self-description reworded.
- AD-0031 and AD-0032 draft to active when they match Compose and scripts.
- Policy, guide and runbook for 0086, 0087 and 0100 draft to active when their
  concrete claims match Compose, scripts and configuration.

### Out of Scope

- The requirements themselves; backup and restore, OpenBao bootstrap and
  resource acceptance remain unverified acceptance conditions.
- Pushing, merging, deployment and any runtime or remote state change.

## Contracts

### Normal Behavior

Each transition follows the Registry lifecycle for its document type. A
document is promoted only after its service names, profiles, ports,
healthchecks, secret names and commands were compared with the source.

### Error Behavior

A document with an unmatched claim stays draft and the Task records the reason.

### Boundary Behavior

No secret value is read or recorded. No live state is claimed.

### Constraints

Static comparison proves declaration only, not runtime behavior.

## Acceptance Criteria

1. REQ-0027 is approved and no longer calls itself a draft.
2. AD-0031 and AD-0032 are active only if they match the implementation.
3. The 0086, 0087 and 0100 documents are active only if their claims match.
4. The document gates pass locally, with actual results in the Task.

## Failure Conditions

### Observable Failures

A promoted document contradicts Compose, a script or configuration.

### Stop Boundaries

This Task pushes and merges nothing.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-req-0027-approval.md)
