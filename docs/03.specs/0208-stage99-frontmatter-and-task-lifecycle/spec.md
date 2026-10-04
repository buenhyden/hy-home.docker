---
title: "Stage 99 Frontmatter and Task Lifecycle Specification"
version: "1.0.0"
type: "sdlc/spec"
status: "active"
owner: "@buenhyden"
updated: "2026-10-04"
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

Make Stage 99's existing Spec completion receipt and Task lifecycle record
machine-readable without changing the frontmatter value grammar or inventing
a lifecycle state. This package owns the bounded contract, validator behavior
and tests, template and navigation migration, and one local logical commit.

## Boundaries and Inputs

Inputs are REQ-0024, REQ-0026, AD-0027, AD-0030, ADR-0037, the Stage 99
Registry and document-profile schema, the three Stage 03 templates, and current
SPEC-0182 and SPEC-0204 package records. The initial observed registry allocation
is `SPEC-0207` high-water and `SPEC-0208` next number. No archive rewrite,
terminal Task rewrite, service execution, secret access, remote action, push,
PR, or merge is in scope. One local logical commit spans the inseparable
contract, consumer, test, and documentation changes.

## Behavior Contract

1. The Registry retains the four existing completion-receipt headers and adds
   optional item headers for criterion-to-work-unit Task evidence, plus the
   exact optional `Work Log`/`Lifecycle Events` event table contract.
2. The profile schema represents those Registry-owned fields as optional typed
   data so historical registries remain valid. The frontmatter schema remains
   unchanged because no frontmatter value shape changes.
3. A four-column Task receipt uses its frontmatter status as the source. A
   multi-item five-column receipt uses its Status cells as the source and
   stores the validated derived Task summary in frontmatter under the
   [SDLC](../../../.agents/governance/sdlc.md) precedence, without a new state.
4. A completed criterion requires observed `PASS:` evidence. Cancellation
   requires the existing valid disposition for its criterion and never waives
   Spec completion evidence. Lifecycle events are recorded only for observed
   registered direct transitions in the same package and cite a real Task anchor.

## Technical Approach

Inventory the registered profile/template/schema surfaces and their consumers,
then add the minimal Registry and profile-schema fields, implement and test the
registered validators, align the templates, and migrate only current
nonterminal Task/Plan prose that has recorded facts. Update the Stage 03 index
to route the new active package and prepare one local conventional commit. Keep
the existing requirements, descriptions, and accepted ADR unchanged because
they already own the durable boundaries.

## Interfaces and Data

The Registry's `common.spec_completion_evidence` retains `table_headers` and
adds `item_table_headers`. `common.task_lifecycle_events` declares `Work Log`,
`Lifecycle Events`, and the four headers `Artifact`, `From`, `To`, and
`Evidence`. The profile schema receives typed optional counterparts. Markdown
templates render these contracts; validators remain their existing consumers.

## Failure Modes and Guardrails

Do not infer approval, review, execution, transition, PASS evidence, or a
commit from structural fields. Do not create lifecycle events for unobserved
stages. A mixed terminal/nonterminal multi-item Task or any in-progress item
remains in-progress; queued means planned/ready and does not become a new enum.
The
known completed Task 0001 in SPEC-0182 with review pending remains a limitation
recorded here, not a reason to reopen it.

## Acceptance Contract

1. The Task inventories every affected registry, profile, schema, template,
   document, and consumer with its owner and disposition.
2. Stage 99 defines the optional completion-item and lifecycle-event shapes
   exactly, preserving the existing frontmatter schema and four-column receipt.
3. Spec, Plan, and Task templates express authoring, approval, review, and
   execution boundaries without seeded approvals or timestamps.
4. The validator reads the new five-column item rows and event table through
   both package and metadata paths, preserves historical compatibility, and
   rejects invalid PASS, cancellation, transition, and summary combinations.
5. Current nonterminal SPEC-0182 and SPEC-0204 records and the Stage 03 index
   use the new terminology only where an actual recorded fact supports it;
   focused validation, review, and the local-finish boundary are recorded in
   this Task. The containing logical Git commit records its actual receipt
   without a self-referential Task SHA.

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
