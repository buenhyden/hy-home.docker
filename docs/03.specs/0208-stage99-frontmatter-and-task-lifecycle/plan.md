---
title: "Stage 99 Frontmatter and Task Lifecycle Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0208-PLAN-0001"
parent_ids:
- "SPEC-0208"
created: "2026-10-04"
---

# Stage 99 Frontmatter and Task Lifecycle Plan

## Overview

### Objective

Deliver the minimum Stage 99 contract, validator implementation and tests,
current-document migration, the v3 checkpoint, and the v4 evidence amendment
for truthful Task lifecycle evidence and completion-item receipts.

### Dependencies

- SPEC-0208 and its approved Requirement and Architecture inputs.
- Registry/profile-schema/template owners and their existing validators.
- Recorded facts in nonterminal SPEC-0182 and SPEC-0204 documents.
- Read-only review and focused validation before completion. Commit and remote
  integration require their separately recorded authorization and evidence.


## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Inventory Stage 99 | None | TSK-0001 | Completed Task evidence |
| W2 | 2, 3, 4 | Align contract and consumers | W1 | TSK-0001 | Completed Task evidence |
| W3 | 5 | Migrate current records | W2 | TSK-0001 | Completed Task evidence |
| W4 | 5 | Record checkpoint and review | W3 | TSK-0001 | Completed Task evidence |

### Work Details


1. W1: inventory Stage 99 profiles, templates, schemas, roles, consumers,
   named lifecycle families, pure-navigation READMEs, and current Stage 03
   records; record every file's disposition in the Task.
2. W2: add the minimal Registry and profile-schema contract, implement and test
   its validator consumers, align the Spec, Plan, and Task templates, and add
   result/review/generation and direct-parent contracts.
   Preserve frontmatter value grammar and existing completion-receipt headers.
3. W3: migrate actual terminology, direct Task parents, and derived states in
   current SPEC-0182, SPEC-0204, SPEC-0207, and SPEC-0208 records; align
   pure-navigation README profiles and route SPEC-0208 from the Stage 03 README.
4. W4: record the v3 checkpoint, run owner-selected validation and review for
   the v4 amendment, record observed results and limitations, then create the
   v4 local conventional commit when its required receipts exist. Push, PR,
   merge, and remote checks remain separately authorized.

### Rulings

Queued is a planned/ready summary label, not a lifecycle enum. Existing durable
authority remains in REQ-0024, REQ-0026, AD-0027, AD-0030, and ADR-0037.

This Plan completed on 2026-10-05 after Task 0001 recorded completed W1--W4
receipts, accepted Review Evidence, the verified local gate, independent
review, and the past v4 local source commit. Remote integration and live
operations remain outside this Plan's closure.

## Verification Plan

### Verification

Use the registered metadata, lifecycle, and link checks selected by the owning
validation work, then independently review the diff. Record each actual command
and result in Task 0001; no structural check proves approval or execution.

## Risks and Rollback

### Risk and Rollback

An over-broad schema or template can turn descriptive prose into a parallel
machine contract. Roll back the bounded working-tree changes before integration
if validation or review finds that risk. Do not alter frozen records, terminal
Task bodies, Commit Ledgers, or status facts; approved parent-ID and actual
updated-date normalization remains allowed. Do not invent unobserved lifecycle
facts.

## Related Documents

- [Specification](spec.md)
- [Task 0001](tasks/tsk-0001-stage99-and-task-lifecycle.md)
