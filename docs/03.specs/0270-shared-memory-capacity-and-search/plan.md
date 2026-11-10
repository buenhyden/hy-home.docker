---
title: "Shared Memory Capacity and Search Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-10"
layer: "specs"
artifact_id: "SPEC-0270-PLAN-0001"
parent_ids:
- "SPEC-0270"
created: "2026-11-10"
---

# Shared Memory Capacity and Search Plan

## Overview

Implement the owner-approved follow-up through separate memory, backup,
documentation and integration writers. Source tests precede activation.

## Scope

The Spec's local source, synthetic tests and documents only. Real memory
inventory, backup execution, native providers and runtime remain separate.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Implement independent capacity ledger, shared lock, reservations and result reconciliation | None | TSK-0001 | RED/GREEN concurrency, crash, inventory and capacity cases |
| W2 | 2 | Admit memory put, backup and restore without changing the memory snapshot schema | W1 | TSK-0001 | Existing memory suite plus legacy, restore and refusal regressions |
| W3 | 3 | Add bounded read-only lexical search and status | None | TSK-0001 | Current/stale/eligibility, ordering, limit and filesystem no-write assertions |
| W4 | 4 | Host backup coordinator and manual/daily/local/offsite caller integration | W1 | TSK-0001 | Synthetic command transport, snapshot inventory, reservation and failure tests |
| W5 | 6 | Update current policy and operations without changing historical bodies | W1, W2, W3, W4 | TSK-0001 | Metadata, links and independent governance/document review |
| W6 | 5 | Register scripts/tests, measure branch coverage and independently review exact diff | W1, W2, W3, W4, W5 | TSK-0001 | Focused tests, manifest, workflow contract, metadata and review evidence |

## Verification Plan

Use temporary fixture stores and injected command transports. Run the existing
memory regressions and new capacity/search/backup tests with meaningful branch
coverage at least 80 percent. Check manifest, workflow routing, changed-document
metadata, lifecycle and links. The parent integrates shared registrations once.
Hosted CI, actual backup adoption and native-runtime claims remain NOT_RUN
until their own actual evidence exists.

## Risks and Recovery

### Risks and Rollback

Fail closed on unknown inventory without deleting data. Preserve pending
reservations through crashes and require result reconciliation before reuse.
A source rollback never deletes or silently rewinds an initialized capacity
ledger. Do not restore a memory snapshot over the capacity ledger. Operational
recovery requires a separately reviewed exact target and approval.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-capacity-search-and-backup.md)
