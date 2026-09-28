---
title: "Package Waiting, Cancellation and Archive Reassessment"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-28"
layer: "architecture"
artifact_id: "ADR-0037"
parent_ids:
- "AD-0030"
supersedes:
- "ADR-0036"
created: "2026-09-17"
---

# ADR-0037: Package Waiting, Cancellation and Archive Reassessment

## Context

ADR-0036 admitted completed Tasks inside unfinished packages but rejected
cancelled Tasks and completed packages in Stage 03. Completion and disposition
therefore shared an integration, and source comparison allowed narrowly defined
lifecycle metadata changes. Reassessment and history-only availability had no
registered contract. These constraints made truthful cancellation, independent
completion approval, and exact capture preparation difficult.

On 2026-09-28 the repository owner explicitly approved this decision's acceptance,
waiting/cancellation, reassessment/history-only adoption, and completing Standard
3.0.0 adoption. The still-proposed decision and SPEC-0179 were expanded together
before acceptance. This approval does not authorize actual payload removal,
commits, remote integration, runtime operations or secret access.

## Decision Drivers

- Status records actual lifecycle facts; cancellation must retain evidence and
  account for acceptance criteria.
- Completion, promotion and disposition approval are distinct events.
- Captured facts and present assessment have different owners and must not overwrite
  each other. Existing originals and execution ledgers remain immutable.
- Identity and recoverability must be established from Git objects, not a duplicate
  digest or recovery ledger. Incomplete history cannot establish success.
- Current citation permission depends on assessment before source-profile exceptions.
- Registry owns shapes, states and ordered judgments; code implements those contracts.

## Options Considered

1. **Keep retained-only storage and simultaneous completion/disposition.** Rejected:
   this cannot express approved waiting, truthful cancellation or reassessment.
2. **Add a waiting status and duplicate machine catalog.** Rejected: waiting is
   derivable from member statuses, and a second catalog creates conflicting authority.
3. **Extend existing package judgments, Task metadata and Markdown catalog.** Selected:
   preserves identities and historical rows while making current management explicit.
4. **Rewrite all old captures to exact bytes.** Rejected: original lifecycle evidence
   and historical transformations cannot be retroactively manufactured.

## Decision

1. A completed Spec may wait in Stage 03 when its Plan is completed and
   every Task is completed or validly cancelled. Nonterminal members fail. Waiting
   is a calculated index label, not a status or permission to resume execution.
   Cancelled/superseded Spec packages do not gain this exception. Whole-package
   disposition still requires approval and preserves every member.
2. In an unfinished package, completed and validly cancelled Tasks may remain;
   terminal Plans may not. `cancellation` requires a nonblank reason and approver,
   a real date and a criterion list. Each numbered criterion belongs to the Spec
   and has exactly one nonblank withdrawal reason or a same-package Task target
   that exists, is not itself and is not cancelled. An empty list means no criteria
   were assigned. Withdrawal never exempts the completed Spec's PASS receipt.
3. Registry profile lifecycles determine member terminality. Disposition-entry
   statuses are registered separately; a union of all terminal lifecycles is invalid.
   Templates do not seed approvals. Completion receipts are checked before moving.
4. Existing Retention Catalog capture rows remain immutable. Optional `Current
   Assessments` rows record one actual evaluation per unit. Assessment values are
   `unreviewed`, `usable`, `superseded`, `withdrawn`, `invalidated`; availability is
   `retained` or `git-history-only`. No row means unreviewed/retained, never approved.
   A superseded assessment resolves a unique current owner. Existing rows cannot
   disappear; changed assessments need fresh evidence and rehabilitation is explicit.
5. History-only removal requires a separate unit/action/date-scoped approval, no hold,
   complete unit absence, consumer cutover and recoverable source objects. The pinned
   Task revision must have the registered status, owner, structured authorization and
   actual approval quotation. A proposed ADR, unrelated Task or this general adoption
   cannot authorize a unit's removal. Historical approval is verified at its own
   revision even after its Task moves. Capture/assessment rows survive removal;
   partial removal and unexplained resurrection fail. `purged` is not supported.
6. Captures present at Registry's `legacy_capture_revision` retain their original
   generation. Only the explicitly named ADR-0036 bootstrap capture also permits
   the former lifecycle-field comparison, using exactly that revision and original
   path. Its final superseded metadata cannot exist in a source commit without
   separately authorized committing. This finite exception cannot label arbitrary
   new captures legacy. Every other new capture preserves the exact prepared source
   commit/path, complete member set, Git modes and raw blob bytes.
7. HEAD/target, index and worktree are separate snapshots with their own catalogs.
   Canonical identity uses raw Git objects; checkout line-ending representation is
   checked separately. External filters never run. Unsupported encoding, filter,
   LFS/gitlink, missing objects or shallow history produce explicit limitations or
   failures. Resource limits never authorize deletion. Reachable history exposes
   units even when both payload and catalog rows disappear.
8. Citation order is unit resolution, assessment/availability blocking, route-record
   blocking, source-profile/disposition permission, context resolution, then physical
   integrity. Withdrawn, invalidated and history-only payloads are blocked before
   Incident exceptions. Current rules cite current owners; completed/resolved bodies
   are historical evidence. Tombstone/Migration bodies are never direct evidence.
9. Frozen outbound links are evaluated at the source revision/path without editing
   the original. Legacy broken or unavailable historical links are explicit
   observations; new exact captures must pass. Current catalog/index links remain
   current links, and unavailable bodies are navigated through their catalog.
10. Original Task Commit Ledgers, capture paths and dated facts are preserved. Current
    metadata, authoring guidance and indexes change in place. Incident `resolved_at`,
    Postmortem `reviewed_at`, whole-unit preservation and external-route-only records
    remain required. No new document ID or second recovery ledger is needed.

## Consequences

- Authors can record cancellation and completion without inventing execution states.
- Assessment is mutable management information; captured lifecycle facts are immutable.
- Exact capture needs a prepared source commit. Without commit authorization the agent
  prepares changes and reports the integration boundary instead of inventing a source.
- Git availability is required for verification. Local static success is not hosted
  CI, service health, deployment, or actual removal evidence.
- Existing legacy verification limits remain visible; adopting a new generation does
  not certify previously unavailable history.
- Rollback restores the scoped current-contract diff before integration; later rollback
  uses an approved change and never rewrites frozen records or published history.

## Traceability

- [AD-0030](../descriptions/0030-document-lifecycle-governance.md)
- [REQ-0026](../../01.requirements/0026-document-retention-and-retirement.md)
- [SPEC-0179](../../03.specs/0179-package-disposition-wait-and-task-cancellation/spec.md)
- [Archive index, including predecessor ADR-0036](../../98.archive/README.md)
- [Retention policy](../../../.agents/governance/documentation-protocol.md#retention-by-status)

## Compliance

Policy owns meaning; Registry owns shapes and generation boundaries; validators own
executable judgments. SPEC-0179 records actual RED/GREEN, snapshot, metadata, corpus,
link and independent review evidence, with S01–S16 and V01–V40 scope and limitations.
This accepted decision is not itself a test result or per-unit removal authorization.

## Follow-up

SPEC-0179 owns implementation and local verification. Its lifecycle must still follow
registered integration edges; the adoption approval does not fabricate intervening
commits or authorize remote integration. A real unit disposition remains a separate
scoped operation after recoverability and consumer checks.
