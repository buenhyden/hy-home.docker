---
title: "Document Retention and Retirement Requirements"
version: "3.2.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-17"
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

| Requirement ID | Statement | Rationale | Acceptance | Priority |
| --- | --- | --- | --- | --- |
| REQ-0026-FR-0001 | Retention uses lifecycle and ownership; age and corpus size may trigger review but never determine automatic removal. | Age, corpus size and absent incoming links cannot by themselves authorize deletion. | No document is removed automatically because of its age or the corpus size; those only trigger review. | must |
| REQ-0026-FR-0002 | Retiring a package or standalone document summarizes its still-current substance into its Stage 01 or Stage 02 owner's Traceability, deletes the original in the same change, and adds its number to its identity space's Registry `reserved_history`. | When a document leaves, readers must still find what it held, why it left and its current owner; version history is the record of the removed body. | A retired document's still-current substance appears in its Stage 01 or Stage 02 owner's Traceability, the original is deleted in the same change, and its number is in its identity space's `reserved_history`. | must |
| REQ-0026-FR-0003 | Registered checks reject a Stage 01 gap or a Stage 03 package removal whose number is not reserved, regardless of incoming links, never accept a copy of the removed document as a substitute, and reject dropping a number from any identity space's `reserved_history`. | A retired document's number stays retired, and absent incoming links cannot by themselves authorize deletion. | A Stage 03 removal or Stage 01 gap passes only when its number is reserved in the checked tree's Registry, an archive copy or branch receipt does not substitute, and dropping a number from any `reserved_history` fails against the trusted base. | must |
| REQ-0026-FR-0004 | Still-current obligations, decisions, structure and procedures move to their canonical governance, Stage 01, 02 or 05 owner before their source is retired. | Retention rules must outlive the change that introduced them, and maintainers need durable criteria independent of old Tasks. | Retirement rules can be read from governance without loading a Spec Package. | must |
| REQ-0026-FR-0005 | Every implemented capability has a Stage 01 Requirement owner and a Stage 02 Description or ADR owner, and Stage 03 retirement preserves that coverage. | This package records no rationale for this requirement. | Every implemented capability names a Stage 01 Requirement owner and a Stage 02 Description or ADR owner, and no Stage 03 retirement removes either. | must |
| REQ-0026-FR-0009 | Stage 03 occupancy is judged per package from registered Spec, Plan and Task terminal sets; a package is ready for removal review when its Spec and Plan are approved or validly cancelled, every Task or Execution Item is terminal and every criterion is accepted or `not-required`, and Task cancellation requires a trusted approval with recorded authority, date, reason and criterion dispositions. | Agents need enforceable lifecycle, approval, retirement and citation boundaries. | A waiting package passes occupancy only with terminal members and valid cancellations, and withdrawal alone never satisfies a still-numbered criterion. | must |
| REQ-0026-FR-0010 | Stage 03 packages contract bounded changes; steady-state meaning belongs to Stage 02 Descriptions and Stage 05 subjects and transfers there before retirement. | This package records no rationale for this requirement. | Before a Stage 03 package retires, its steady-state meaning is present in a Stage 02 Description or Stage 05 subject. | must |
| REQ-0026-FR-0011 | Stages 01 through 05 maintain bidirectional traceability through cross-links; domain requirements need not duplicate this obligation. | Auditors need discoverable lineage and the original context of decisions. | Cross-links between Stages 01 to 05 resolve in both directions under the registered link checks. | must |
| REQ-0026-FR-0013 | Stage 98 holds no records; only its README is tracked there, and a registered check fails on any other tracked file under `docs/98.archive/`. | The lineage of a removed record lives in the Traceability of its Stage 01 or Stage 02 owner, never in a Stage 98 copy. | Any tracked file under `docs/98.archive/` other than its README fails the corpus lifecycle occupancy check. | must |
| REQ-0026-FR-0014 | Current documents do not link into `docs/98.archive/` and do not name a retired identity in `parent_ids`, `supersedes` or `superseded_by`; a retired identity may appear in prose that explains lineage. | This package records no rationale for this requirement. | No current document links into Stage 98 or names a retired identity in a typed reference. | must |
| REQ-0026-FR-0015 | No recovery ledger is introduced; version history is the record of removed bodies, and existing Task Commit Ledgers remain original execution evidence. | Version history is the record of the removed body. | No recovery ledger exists in the tree, and existing Task Commit Ledgers are left unchanged. | must |
| REQ-0026-FR-0016 | A resolved Incident carries its actual nonempty `resolved_at` value, and its bundle and corrective-work owner preserve closure evidence without claiming all corrective work is complete. | This package records no rationale for this requirement. | Every resolved Incident has a nonempty `resolved_at`, and its bundle does not claim all corrective work complete. | must |
| REQ-0026-NFR-0006 | Checks derive judgments from the selected tree and that tree's own Registry; a missing, symlinked, unreadable or invalid Registry reserves nothing, and fixed corpus counts or custom digest or expected-commit ledgers do not decide retention. | This package records no rationale for this requirement. | The same tree and Registry give the same verdict, a missing, symlinked, unreadable or invalid Registry reserves nothing, and current metadata, lifecycle, link and affected regression checks pass on the explicitly selected snapshot with unavailable checks reported. | must |

| Requirement ID | Attribute | Measure | Unit | Environment | Criterion |
| --- | --- | --- | --- | --- | --- |
| REQ-0026-NFR-0006 | Determinism | The same tree and Registry give the same verdict. | The package records no unit for this measure. | The selected tree and that tree's own Registry, on an explicitly selected snapshot. | The same verdict for the same tree and Registry; a missing, symlinked, unreadable or invalid Registry reserves nothing; unavailable checks are reported. |

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
  when its Spec and Plan are approved (or validly cancelled),
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
  remain but a terminal Plan may not. A cancelled Spec keeps no member in the
  active stage. Other stages keep per-document disposition rules.
  Cancelling a Task requires a trusted approval and a record of its approving
  authority and date. The Task records the reason, an authorization reference
  and each criterion disposition. A disposition identifies a successor
  non-cancelled package Task or references an approved withdrawal. An empty
  disposition list means there were no assigned criteria. A criterion still
  numbered in the Spec keeps its completion obligations after withdrawal.
  A separate `not-required` decision may close it without PASS evidence.
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

## Traceability

### Sources

- [Documentation protocol](../../.agents/governance/documentation-protocol.md)
- [Stage authoring matrix](../../.agents/governance/stage-authoring-matrix.md)
- [Stage 99 registry](../99.templates/registry.json)

### Verification Links

#### Acceptance Conditions

- **REQ-0026-FR-0001**: No document is removed automatically because of its age
  or the corpus size; those only trigger review.
- **REQ-0026-FR-0002**: A retired package or standalone document's
  still-current substance appears in its Stage 01 or Stage 02 owner's
  Traceability, the original is deleted in the same change, and its number is
  in its identity space's `reserved_history`.
- **REQ-0026-FR-0003**: A Stage 03 removal or Stage 01 gap passes only when its
  number is reserved in the checked tree's Registry; an archive copy or a
  branch receipt does not substitute. Dropping a number from any identity
  space's `reserved_history` fails against the trusted base.
- **REQ-0026-FR-0004**: Retirement rules can be read from governance without
  loading a Spec Package.
- **REQ-0026-FR-0005**: Every implemented capability names a Stage 01
  Requirement owner and a Stage 02 Description or ADR owner, and no Stage 03
  retirement removes either.
- **REQ-0026-FR-0009**: A waiting package passes occupancy only with terminal
  members and valid cancellations. Withdrawal alone never satisfies a
  still-numbered criterion.
- **REQ-0026-FR-0010**: Before a Stage 03 package retires, its steady-state
  meaning is present in a Stage 02 Description or Stage 05 subject.
- **REQ-0026-FR-0011**: Cross-links between Stages 01 to 05 resolve in both
  directions under the registered link checks.
- **REQ-0026-FR-0013**: Any tracked file under `docs/98.archive/` other than
  its README fails the corpus lifecycle occupancy check.
- **REQ-0026-FR-0014**: No current document links into Stage 98 or names a
  retired identity in a typed reference.
- **REQ-0026-FR-0015**: No recovery ledger exists in the tree, and existing
  Task Commit Ledgers are left unchanged.
- **REQ-0026-FR-0016**: Every resolved Incident has a nonempty `resolved_at`,
  and its bundle does not claim all corrective work complete.
- **REQ-0026-NFR-0006**: The same tree and Registry give the same verdict, and
  a missing, symlinked, unreadable or invalid Registry reserves nothing.
  Current metadata, lifecycle, link and affected regression checks pass on the
  explicitly selected snapshot; unavailable checks are reported.

#### Verification Method

Each condition is judged by running the registered metadata, lifecycle, link and regression checks on the explicitly selected snapshot; unavailable checks are reported, not treated as passing. The Spec Packages that list REQ-0026 as a parent, such as SPEC-0212, record the check results in their Task evidence rows. The owner named in the frontmatter, @buenhyden, judges each condition from that evidence. The same owner accepts the requirement once every condition is judged met.

#### Downstream Links

- [Document lifecycle architecture](../02.architecture/descriptions/0030-document-lifecycle-governance.md)
- [ADR-0051 Summarize-and-delete retirement](../02.architecture/decisions/0051-summarize-and-delete-retirement.md)
- [ADR-0037 Package waiting and Task cancellation](../02.architecture/decisions/0037-package-disposition-wait-and-task-cancellation.md)
- [ADR-0048 Authority parents and criterion acceptance](../02.architecture/decisions/0048-authority-parents-and-criterion-acceptance.md)
- ADR-0031, ADR-0033, ADR-0035, and ADR-0036 are superseded historical decisions.
- SPEC-0257 and SPEC-0261 (retired; version history) delivered the second implementation-alignment corrections of paths, links, Registry exceptions and secret names, and the REQ-0027 approval with the promotion of its dependent documents.
- SPEC-0259 (retired; version history) delivered the third implementation-alignment corrections: Stage 02 labels that named deleted Spec paths, the OpenBao audit wording, the ADR-0038 acceptance and the promotion of matching Stage 05 documents.
- SPEC-0256 (retired; version history) removed the legacy statuses and lineage keys from the Stage 01 to 03 lifecycles and profiles, the archive profiles and templates, and ADR-0011.
- SPEC-0248, SPEC-0249, SPEC-0250 and SPEC-0260 (retired; version history)
  delivered the archive-check removal, the Stage 98 deletion, the completed
  package deletion and the proof-source change. SPEC-0249 retired three
  earlier items, whose numbers stay reserved in the Registry: a Tombstone
  namespace rule, immutable Stage 98 captures, and one capture record per
  unit. Stage 98 no longer holds records.
