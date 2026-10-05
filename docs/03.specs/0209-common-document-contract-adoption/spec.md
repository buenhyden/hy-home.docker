---
title: "Common Document Contract Adoption Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "blocked"
owner: "@buenhyden"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0209"
parent_ids:
- "REQ-0024"
- "REQ-0026"
- "AD-0027"
- "AD-0030"
- "ADR-0037"
created: "2026-10-05"
---

# Common Document Contract Adoption Specification

## Overview

Adopt the approved `SDLC-COMMON-v4` contract as Stage 99 generation 5. Align
the Registry, schemas, templates, current document families, and their
consumers without rewriting frozen or sealed records.

## Scope

Inputs are REQ-0024, REQ-0026, AD-0027, AD-0030, ADR-0037, the verified
contract attachment (`f19249ad20d9f05e29cd63ac547dbb2984fb7c9b01c79b747cb8545820fca179`),
and the current Stage 99 contract. The initial allocation is `208` high-water
and `209` next number. The approved package includes Registry, schemas,
templates, authored-document migration, consumers, tests, and generated
projections; assigned ownership separates those work units. Runtime actions,
archive disposition, pushes, PRs, and provider calls remain out of scope.

## Contracts

1. Stage 99 adopts the attachment's 28 document profiles, lifecycle values,
   direct edges, core headings, frontmatter, table shapes, and result and
   acceptance vocabularies, retaining the existing scalar `superseded_by`.
2. Current authored documents migrate to their declared profile only when they
   are not frozen, sealed, or completed Task bodies. Current active inbound
   links follow renamed headings.
3. A Spec has its issued Requirement and Architecture parents; a Plan has one
   Spec parent; a Task has one Plan parent. Task frontmatter is the only status
   source for new and migrated nonterminal Tasks.
4. Completion requires `PASS` and accepted evidence for each required
   criterion. Cancellation records a real reason, authorization reference, and
   criterion disposition; it never invents authorization or waives Spec work.

## Acceptance Criteria

1. The Task inventories the whole Stage 99 surface, owners, consumers, and
   migration dispositions before changes are represented as complete.
2. Registry, schemas, and templates express the exact approved common contract
   and preserve required extensions and legacy compatibility.
3. Current authored Markdown uses the adopted profile cores, envelope,
   headings, and links while preserved historical bodies remain unchanged.
4. QA-owned consumers, tests, and generated projections support generations
   3, 4, and 5 and validate the new shapes.
5. Focused document checks and the final changed gate have recorded actual
   results, review, and acceptance before closure.

## Related Documents

- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md)
- [REQ-0026](../../01.requirements/0026-document-retention-and-retirement.md)
- [AD-0027](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- [AD-0030](../../02.architecture/descriptions/0030-document-lifecycle-governance.md)
- [ADR-0037](../../02.architecture/decisions/0037-package-disposition-wait-and-task-cancellation.md)
- [Plan](plan.md)
- [Task 0001](tasks/tsk-0001-common-document-contract-adoption.md)

The Registry declares lifecycle generation `5` and `SDLC-COMMON-v4`; the two
JSON schemas and templates carry the same authoring shape. Evidence tables use
`Evidence | Criteria | Work Unit | Check | Input | Result | Location |
Acceptance`; Plan tables use `Work Unit | Criteria | Work | Dependencies |
Task | Verification`. Do not add a parallel runtime registry, empty forms,
profiles, types, roles, or progress ledgers. Preserve native provider envelope
extensions, completed SPEC-0208 Task and Commit Ledger facts, archive bodies,
scalar successor semantics, and actual source date and revision evidence.
