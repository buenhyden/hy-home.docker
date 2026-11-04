---
title: "Implementation Alignment Batch 3 Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0259"
parent_ids:
- "REQ-0026"
- "AD-0030"
created: "2026-11-04"
---

# Implementation Alignment Batch 3 Specification

## Overview

### Intent

Audits found Stage 02 navigation lines whose label names a deleted Spec path
while the target is an Architecture Description, an OpenBao runbook sentence
that contradicts the Compose file, ADR-0038 still proposed, and Stage 05 and
Stage 01-02 documents left in draft. This change corrects the labels and the
sentence and promotes only documents that match the implementation.

### Background

The user directed that documents be corrected to the present state
("현재에 맞게 수정하고 보완한다") and that requirements not started but
executable now be reviewed and carried out. The user then decided to accept
ADR-0038 and to review the draft documents and promote only those that match.

## Scope

### In Scope

- Related Documents lines in Stage 02 that name a deleted Spec path.
- The RUN-0105 audit sentence, split into declared and observed state.
- ADR-0038 proposed to accepted, body unchanged.
- Draft to active for Stage 05 documents that match Compose and scripts.

### Out of Scope

- Accepted ADR decision bodies; `09-tooling` wording in ADR-0009 and ADR-0024.
- The body of GDE-0100 (open PR) and documents whose parent stays draft.
- Pushing, merging and any runtime or remote state change.

## Contracts

### Normal Behavior

Each label names its real target; the RUN-0105 sentence distinguishes Compose
declaration from live observation; promoted documents follow the Registry
lifecycle transitions.

### Error Behavior

A change that breaks metadata, lifecycle or link gates fails them.

### Boundary Behavior

No secret value is read or recorded; no live state is claimed.

### Constraints

A document whose parent or content is unproven stays draft with a reason.

## Acceptance Criteria

1. No Stage 02 link label names a deleted Spec path.
2. RUN-0105 separates Compose declaration from live observation.
3. ADR-0038 is accepted and promoted documents match the implementation.
4. The document gates pass locally, with actual results in the Task.

## Failure Conditions

### Observable Failures

A label still names a deleted path, or a promoted document contradicts Compose.

### Stop Boundaries

This Task pushes and merges nothing.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-implementation-alignment-batch3.md)
