---
title: "Stage 99 Frontmatter and Task Lifecycle Specification"
version: "1.0.0"
type: "sdlc/spec"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0208"
parent_ids:
- "REQ-0024"
- "REQ-0026"
- "AD-0027"
- "AD-0030"
- "ADR-0037"
created: "2026-10-04"
---

# Stage 99 Frontmatter and Task Lifecycle Specification

## Overview

Make Stage 99's Spec completion receipt, Task lifecycle record, and current
document-family lifecycle contract machine-readable without changing the
frontmatter value grammar. This package owns the bounded contract, validator
behavior and tests, template and navigation migration, the v3 checkpoint, and
the v4 evidence amendment.

## Boundaries and Inputs

Inputs are REQ-0024, REQ-0026, AD-0027, AD-0030, ADR-0037, the Stage 99
Registry and document-profile schema, the three Stage 03 templates, and current
SPEC-0182, SPEC-0204, and SPEC-0207 package records. The initial observed
registry allocation is `SPEC-0207` high-water and `SPEC-0208` next number; the
Registry now retains `208`/`209`. No archive rewrite, terminal Task body or
Commit Ledger rewrite, service execution, secret access, remote action, push,
PR, or merge is in scope. The successful v3 checkpoint and the v4 amendment
are separately recorded local commits when their actual receipts exist.

## Behavior Contract

1. The Registry retains the four existing completion-receipt headers and adds
   optional item headers, exact Task-result and Review Evidence vocabularies,
   lifecycle generation `4`, and the optional `Work Log` event and contract
   migration table shapes.
2. The profile schema represents those Registry-owned fields as optional typed
   data so historical registries remain valid. The frontmatter schema remains
   unchanged because no frontmatter value shape changes.
3. A four-column Task receipt uses its frontmatter status as the source. A
   multi-item five-column receipt uses its Status cells as the source and
   stores the validated derived Task summary in frontmatter under the
   [SDLC](../../../.agents/governance/sdlc.md) precedence, without a new state.
4. A completed execution item can record observed `PASS` while Review Evidence
   remains pending in a nonterminal Task. Task and Spec closure require `PASS`
   plus accepted Review Evidence for every numbered criterion. Cancellation
   requires the existing valid disposition for its criterion and never waives
   Spec completion evidence. Lifecycle events are recorded only for observed
   registered direct transitions in the same package and cite a real Task anchor.

## Technical Approach

Inventory the registered profile/template/schema surfaces and their consumers,
then add the minimal Registry and profile-schema fields, implement and test the
registered validators, align templates and pure-navigation README profiles,
and migrate current document-family lifecycles and Plan-only Task parents from
recorded facts. Keep requirements, architecture descriptions, and accepted ADR
traceability unchanged because they already own those boundaries.

## Interfaces and Data

The Registry's `common.spec_completion_evidence` retains `table_headers` and
adds `item_table_headers` and Task-result values. `common.review_evidence`
defines its three-column table and acceptance values. `common.task_lifecycle_events`
declares `Work Log`, `Lifecycle Events`, and the four headers `Artifact`,
`From`, `To`, and `Evidence`, with a generation-4 migration proof shape. The
profile schema receives typed optional counterparts. Markdown templates render
these contracts; validators remain their existing consumers.

## Failure Modes and Guardrails

Do not infer approval, review, execution, transition, PASS evidence, or a
commit from structural fields. Do not create lifecycle events for unobserved
stages. A mixed terminal/nonterminal multi-item Task or any in-progress item
remains in-progress; queued means planned/ready and does not become a new enum.
Task and Plan parents are direct and singular only where this contract assigns
them. The known completed Task 0001 in SPEC-0182 with review pending remains a
limitation, not a reason to reopen it.

## Acceptance Contract

1. The Task inventories every affected named family, Registry/profile/schema,
   template, pure-navigation README, document, and consumer with owner and
   disposition, retaining unspecified profiles unless they are pure navigation.
2. Stage 99 defines the optional completion-item, result, review, generation,
   lifecycle-event, and migration-proof shapes exactly, preserving the existing
   frontmatter grammar and four-column receipt.
3. Spec, Plan, and Task templates express the approved lifecycle families,
   direct parent cardinality, authoring, review, and execution boundaries
   without seeded approvals or timestamps.
4. The validator reads five-column item rows, result/review values, parent
   cardinality, and lifecycle generation through package and metadata paths,
   preserving frozen historical compatibility and rejecting invalid summary,
   PASS, acceptance, cancellation, or transition combinations.
5. Current SPEC-0182 and SPEC-0204 packages derive blocked Spec/Plan states;
   SPEC-0207 retains in-progress while its sole Task is terminal; SPEC-0208
   remains in-progress. Focused validation, review, and both local-commit
   boundaries are recorded without a self-referential Task SHA.

## Traceability

- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md)
- [REQ-0026](../../01.requirements/0026-document-retention-and-retirement.md)
- [AD-0027](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- [AD-0030](../../02.architecture/descriptions/0030-document-lifecycle-governance.md)
- [ADR-0037](../../02.architecture/decisions/0037-package-disposition-wait-and-task-cancellation.md)
- [Plan](plan.md)
- [Task 0001](tasks/tsk-0001-stage99-and-task-lifecycle.md)

## Open Questions

The validator source and tests are implemented by the assigned W2 owner under
this package; this documentation work records their source contract and actual
receipts without duplicating implementation ownership.

## Operational Impact

This changes documentation contracts and their validators. It does not operate
services or alter deployment, credential, or archive state.
