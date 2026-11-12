---
title: "Shared Memory Capacity and Search Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0270-PLAN-0001"
parent_ids:
- "SPEC-0270"
created: "2026-11-10"
---

# Shared Memory Capacity and Search Plan

## Overview

### Goal and Boundary

Implement the owner-approved follow-up through separate memory, backup,
documentation and integration writers. Source tests precede activation.

The Spec's local source, synthetic tests and documents only. Real memory
inventory, backup execution, native providers and runtime remain separate.

Parent Spec: [Spec](spec.md)

### Assumptions

The plan works under the approved SPEC-0270 (local source, synthetic tests and documents only); it assumes no authority beyond it.

## Dependencies

### Prerequisites

The approved Spec.

### Dependency Order

W1 and W3 have no dependencies; W2 and W4 start after W1; W5 starts after W1-W4; W6 starts after W1-W5.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Implement independent capacity ledger, shared lock, reservations and result reconciliation | None | TSK-0001 | RED/GREEN concurrency, crash, inventory and capacity cases |
| W2 | 2 | Admit memory put, backup and restore without changing the memory snapshot schema | W1 | TSK-0001 | Existing memory suite plus legacy, restore and refusal regressions |
| W3 | 3 | Add bounded read-only lexical search and status | None | TSK-0001 | Current/stale/eligibility, ordering, limit and filesystem no-write assertions |
| W4 | 4 | Host backup coordinator and manual/daily/local/offsite caller integration | W1 | TSK-0001 | Synthetic command transport, snapshot inventory, reservation and failure tests |
| W5 | 6 | Update current policy and operations without changing historical bodies | W1, W2, W3, W4 | TSK-0001 | Metadata, links and independent governance/document review |
| W6 | 5 | Register scripts/tests, measure branch coverage and independently review exact diff | W1, W2, W3, W4, W5 | TSK-0001 | Focused tests, manifest, workflow contract, metadata and review evidence |

### Change and Rollback

A source rollback never deletes or silently rewinds an initialized capacity
ledger. Do not restore a memory snapshot over the capacity ledger. Operational
recovery requires a separately reviewed exact target and approval.

## Verification Plan

### Verification Matrix

Use temporary fixture stores and injected command transports. Run the existing
memory regressions and new capacity/search/backup tests with meaningful branch
coverage at least 80 percent. Check manifest, workflow routing, changed-document
metadata, lifecycle and links. The parent integrates shared registrations once.
Hosted CI, actual backup adoption and native-runtime claims remain NOT_RUN
until their own actual evidence exists.

### Stage Placement

The Plan places no stage-specific checks beyond the Verification Matrix; hosted CI, actual backup adoption and native-runtime claims remain NOT_RUN until their own evidence exists.

## Risks

### Risks and Mitigations

Fail closed on unknown inventory without deleting data. Preserve pending
reservations through crashes and require result reconciliation before reuse.

### Escalation

Unknown inventory fails closed; operational recovery requires a separately reviewed exact target and approval, and work stops at the owner until then.

## Promotion Map

### Durable Meaning

The capacity ledger, search and backup contract lives in the memory source, current policy and operations documents.

### Owner and Receipt

Owner @buenhyden. The receipt is TSK-0001, named in the Work Breakdown Task column.

- [Task](tasks/tsk-0001-capacity-search-and-backup.md)
