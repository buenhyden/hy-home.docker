---
title: "Document Retention and Retirement Requirements"
version: "3.0.3"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "requirements"
artifact_id: "REQ-0026"
created: "2026-09-01"
---

# Document Retention and Retirement Requirements

## Overview

### Problem and Outcome

Retention rules must outlive the change that introduced them. A document remains
current while it owns current meaning; when it leaves, readers must still find
what it held, why it left, and its current owner. Its still-current substance is
summarized into a current owner, the original is deleted, version history is the
record of the removed body, and its number stays retired. Age, corpus size, and
absent incoming links cannot by themselves authorize deletion.

### Stakeholders

- Maintainers need durable retention and review criteria independent of old Tasks.
- Agents need enforceable lifecycle, approval, retirement, and citation boundaries.
- Auditors need discoverable lineage and the original context of decisions.

The owner, @buenhyden, writes, reviews and accepts this package.

## Scope

### In Scope

This package covers how documents are retained, retired and summarized into a current owner, and the registered checks that enforce it, as stated in the Overview.

### Constraints and Exclusions

- Retirement summarizes before it deletes: the lineage of a removed record lives
  in the Traceability of its Stage 01 or Stage 02 owner, never in a Stage 98
  copy.
- Retired numbers are recorded only in the Registry `reserved_history` of their
  identity space, and that list only grows.
- Distinguish worktree, index, and target commit. Missing objects and
  unavailable history are explicit verification limits, never success.
- Restore history into a separately explained current owner; do not silently
  recreate a removed record as current authority. Secret exposure requires
  separately authorized security response, not ordinary retirement.

## Requirements

### Functional Requirements

- **REQ-0026-FR-0001**: Retention uses lifecycle and ownership. Age and corpus
  size may trigger review but never determine automatic removal.
- **REQ-0026-FR-0002**: Retiring a package or standalone document summarizes its
  still-current substance into its Stage 01 or Stage 02 owner's Traceability,
  deletes the original in the same change, and, as an authoring rule, adds its
  number to its identity space's Registry `reserved_history`. Version history is
  the record of the removed body.
- **REQ-0026-FR-0003**: Registered checks reject a Stage 01 gap or a Stage 03
  package removal whose number is not reserved, regardless of incoming links;
  a copy of the removed document anywhere, including Stage 98, never stands in
  for the reserved number. For every identity space, they reject dropping a
  number from `reserved_history`. Other standalone removals rely on the
  retirement authoring rule above.
- **REQ-0026-FR-0004**: Still-current obligations, decisions, structure, and
  procedures move to their canonical governance, Stage 01, 02, or 05 owner before
  their source is retired.
- **REQ-0026-FR-0005**: Every implemented capability has a Stage 01 Requirement
  owner and a Stage 02 Description or ADR owner. Stage 03 retirement preserves
  that coverage.
- **REQ-0026-FR-0009**: Stage 03 occupancy is judged per package using registered
  Spec, Plan, and Task terminal sets. A package is ready for removal review
  when its Spec and Plan are approved (or validly cancelled or superseded),
  every Task or Execution Item is terminal, every numbered Spec criterion is
  accepted or `not-required`, and no required non-PASS observation is
  unresolved; an older Task format without the typed Criterion Acceptance table
  counts when it records every criterion as PASS or accepted and leaves no
  required non-PASS observation unresolved. Readiness is derived and never
  stored.
  A ready package with an approved Spec may wait in Stage 03 until its removal
  is approved, then is deleted with its number reserved. A terminal Task's link
  into a deleted package whose number is reserved is not a link failure. In
  an unfinished package, completed and validly cancelled Tasks may
  remain but a terminal Plan may not. A cancelled or superseded Spec keeps no
  member in the active stage. Other stages keep per-document disposition rules.
  Cancellation records a reason, approver, valid approval date, and criterion
  dispositions: reassignment to another non-cancelled package Task or approved
  withdrawal reason. Empty criteria means no assigned criteria; withdrawal
  never exempts a criterion still numbered in the Spec from PASS evidence.
  Waiting grants neither new work nor removal permission.
- **REQ-0026-FR-0010**: Stage 03 packages contract bounded changes. Steady-state
  meaning belongs to Stage 02 Descriptions and Stage 05 subjects and transfers
  there before retirement.
- **REQ-0026-FR-0011**: Stages 01 through 05 maintain bidirectional traceability
  through cross-links; domain requirements need not duplicate this obligation.
- **REQ-0026-FR-0013**: Stage 98 holds no records. Only its README, which
  describes the disposition scheme, is tracked there, and a registered check
  fails on any other tracked file under `docs/98.archive/`. No gate validates
  Stage 98 content beyond that.
- **REQ-0026-FR-0014**: Current documents do not link into `docs/98.archive/` and
  do not name a retired identity in `parent_ids`, `supersedes`, or
  `superseded_by`. A retired identity may appear in prose where it explains
  lineage.
- **REQ-0026-FR-0015**: No recovery ledger is introduced: version history is the
  record of removed bodies. Existing Task Commit Ledgers remain original
  execution evidence.
- **REQ-0026-FR-0016**: A resolved Incident carries its actual nonempty
  `resolved_at` value. Its bundle and corrective-work owner preserve closure
  evidence without claiming all corrective work is complete.

### Quality Requirements

- **REQ-0026-NFR-0006 — Determinism**: Checks derive judgments from the selected tree and that
  tree's own Registry. A missing, symlinked, unreadable, or invalid Registry
  reserves nothing. Fixed corpus counts and custom digest or expected-commit
  ledgers do not decide retention; measure: the same
  tree and Registry give the same verdict.

## Acceptance Criteria

### Acceptance Conditions

- A Stage 03 removal or Stage 01 gap passes only when its number is reserved in
  the checked tree's Registry; an archive copy or a branch receipt does not
  substitute.
- Dropping a number from any identity space's `reserved_history` fails against
  the trusted base.
- Any tracked file under `docs/98.archive/` other than its README fails the
  corpus lifecycle occupancy check.
- No current document links into Stage 98 or names a retired identity in a typed
  reference.
- A waiting package passes occupancy only with terminal members and valid
  cancellations. Withdrawal alone never satisfies a still-numbered criterion.
- Retirement rules can be read from governance without loading a Spec Package.
- Current metadata, lifecycle, link, and affected regression checks pass on the
  explicitly selected snapshot; unavailable checks are reported.

### Verification Method

Each condition is judged by running the registered metadata, lifecycle, link and regression checks on the explicitly selected snapshot; unavailable checks are reported, not treated as passing. The Spec Packages that list REQ-0026 as a parent, such as SPEC-0248, SPEC-0249 and SPEC-0250, record the check results in their Task evidence rows. The owner named in the frontmatter, @buenhyden, judges each condition from that evidence. The same owner accepts the requirement once every condition is judged met.

## Traceability

### Source and Constraints

- [Documentation protocol](../../.agents/governance/documentation-protocol.md)
- [Stage authoring matrix](../../.agents/governance/stage-authoring-matrix.md)
- [Stage 99 registry](../99.templates/registry.json)

### Downstream Links

- [Document lifecycle architecture](../02.architecture/descriptions/0030-document-lifecycle-governance.md)
- [ADR-0051 Summarize-and-delete retirement](../02.architecture/decisions/0051-summarize-and-delete-retirement.md)
- [ADR-0037 Package waiting and Task cancellation](../02.architecture/decisions/0037-package-disposition-wait-and-task-cancellation.md)
- [ADR-0048 Authority parents and criterion acceptance](../02.architecture/decisions/0048-authority-parents-and-criterion-acceptance.md)
- ADR-0031, ADR-0033, ADR-0035, and ADR-0036 are superseded historical decisions.
- SPEC-0249 retired three earlier items, whose numbers stay reserved in the
  Registry: a Tombstone namespace rule, immutable Stage 98 captures, and one
  capture record per unit. Stage 98 no longer holds records.
