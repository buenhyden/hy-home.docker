---
title: "Document Lifecycle Governance Architecture"
version: "3.0.3"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "architecture"
artifact_id: "AD-0030"
parent_ids:
- "REQ-0026"
created: "2026-09-01"
---

# Document Lifecycle Governance Architecture

## Overview

### Purpose and Readers

The Registry defines document shape and retired numbers; current stage owners
retain durable meaning, Tasks record actual execution, and version history is the
record of removed bodies. Approval, criterion acceptance, and retirement are
separate facts.

Governance owns when documents remain current, leave active stages, are
reassessed, and may be removed from the working tree. This Description explains
which components read which authority and what their checks establish.
Maintainers and agents use the same contracts before claiming completion.

### System Boundary

Inside the boundary are the Stage 99 Registry, current stage trees, and
registered document validators. Stage 98 holds only its README. Git provides
removed bodies and historical approval context. CI chooses trusted comparison
snapshots but does not grant retirement authority. Runtime systems, secret
access, and remote integration remain separately authorized actions.

## Context and Constraints

### Context

Maintainers and agents read the Stage 99 Registry, current stage trees and registered validators. CI chooses trusted comparison snapshots, and Git supplies removed bodies and historical approval context.

### Constraints

Runtime systems, secret access and remote integration remain separately authorized actions. Validators are read-only, fail closed on unsafe traversal or an invalid Registry, and keep Git reads, enumeration and file data within resource limits.

## Current Structure

### Building Blocks

- `scripts/lib/document_governance/registry.py` loads profiles, lifecycles, and
  identity spaces, including each space's `reserved_history` of retired
  numbers. The Registry is the machine authority for their shape and permitted
  values.
- `scripts/lib/document_governance/spec_packages.py` loads bounded current and
  historical package snapshots, judges Evidence, criterion acceptance and
  removal readiness, accepts a Stage 03 removal only when its number is
  reserved in the checked tree's Registry, and supplies the shared cancellation
  judgment and acceptance-criterion parser.
- `scripts/lib/document_governance/requirements.py` accepts a Stage 01 gap only
  when its number is reserved, and `identity_history.py` rejects dropping a
  reserved number against the trusted base.
- `scripts/lib/document_governance/lifecycle/occupancy.py` judges Stage 03
  package occupancy and fails on any tracked Stage 98 file but its README.
- `scripts/lib/document_governance/references.py` derives Stage 90 package
  membership and enforces each protected package's preservation declaration.
- `scripts/lib/document_governance/links.py` checks current links, anchors,
  navigation, and fenced commands.
- Registered metadata, document-link, and corpus-lifecycle entrypoints expose
  these judgments through gate profiles. `metadata/heading.py` enforces the
  Registry's section contracts so authored declarations and checks agree.

### Runtime and Deployment

#### Runtime View

Load Registry contracts before classifying documents. Enumerate the selected
current snapshot and read the comparison base through bounded Git operations.
A member missing from a retained package differs from an entire package leaving
Stage 03. An entire package leaves only when its Spec number is reserved; a copy
elsewhere, including under Stage 98, grants nothing.

Completion and disposition are separate. Write permanent outcomes into current
owners and final evidence into the Task. A package with an approved Spec and
Plan may wait once it is ready for removal review as ADR-0048 defines it, and
is deleted once its removal is approved. In an
unfinished package, completed and validly cancelled Tasks may remain, but a
terminal Plan may not. Cancelled Specs keep no members in active Stage 03.
Stage 01 to 03 documents use no deprecated, superseded, retired, or archived
status; a replaced document is summarized into its owner and deleted. The occupancy branch reads per-profile terminal sets from Registry;
standalone documents retain their existing per-document rule.

Cancellation uses one pure judgment for occupancy and package validation. It
requires reason, approver, actual approval date, and a list of criterion
reassignments or withdrawal reasons. Reassignment stays in the package, cannot
point to itself or another cancelled Task, and never waives completion coverage.
An empty list records that no acceptance criterion was assigned.

Retirement summarizes the removed record's still-current substance into its
Stage 01 or Stage 02 owner's Traceability and deletes the original in the same
change. The Registry `reserved_history` gains its number and never loses one.
Current documents do not link into Stage 98 or name a retired identity in a
typed reference.

#### Deployment View

Validators are registered in `scripts/manifest.yaml` and selected by
`scripts/validation/run-ci-gate.py`. Local comparison normally uses `HEAD`; CI
supplies its trusted base. Evidence identifies whether validation examined the
worktree, index, target commit, or historical source context. These read-only
checks do not write documents or operate services. Full gate or remote runs
retain their own authorization and execution evidence requirements.

## Interfaces

### Contracts

- The Registry is the machine authority for profile shape, lifecycles, identity spaces and each space's `reserved_history`.
- Metadata, document-link and corpus-lifecycle entrypoints expose the judgments through gate profiles registered in `scripts/manifest.yaml` and selected by `scripts/validation/run-ci-gate.py`.
- `metadata/heading.py` enforces the Registry's section contracts.

### Failure Boundaries

Unsafe traversal, missing approval, and a missing, symlinked, unreadable or invalid Registry yield findings instead of exemptions. Exceeding a resource limit is a diagnostic, never an automatic retention action. A missing source object or insufficient history prevents recovering a removed body, and that limit is explicit.

## Decisions

### Decision Links

- [ADR-0037 Package waiting and Task cancellation](../decisions/0037-package-disposition-wait-and-task-cancellation.md)
- [ADR-0051 Summarize-and-delete retirement](../decisions/0051-summarize-and-delete-retirement.md)
- [ADR-0032 Canonical agent governance home](../decisions/0032-canonical-agent-governance-home.md)
- [ADR-0048 Authority parents and criterion acceptance](../decisions/0048-authority-parents-and-criterion-acceptance.md)

### Quality and Risks

#### Quality Attributes

- Fail closed: unsafe traversal, missing approval, and a missing, symlinked,
  unreadable, or invalid Registry yield findings instead of exemptions.
- Derived: membership and current judgments come from the Registry and the
  selected tree rather than fixed counts or invented digest ledgers.
- Bounded: Git reads, directory enumeration, and file data have resource limits;
  exceeding one is a diagnostic, never an automatic retention action.
- Immutable evidence: original Task Commit Ledgers remain unchanged, and version
  history is the record of removed bodies.
- Separable: governance explains the rule without loading a package; this
  Description explains enforcement without relying on a past execution Task.

#### Risks

- Metadata `check-changed` compares current and base bodies with
  `changed_boundary=True` to reject newly introduced template instructions and
  tokens. Two template-source calls using `False` in `reference.py` do not
  disable that production path. Existing debt and introduced violations are
  distinct; a changed-only pass does not prove corpus-wide cleanup.
- `TARGET_TEMPLATE_LITERALS` retains the residual `<!-- Target:` marker rule.
  Current templates and metadata reports no longer generate the marker.
  SPEC-0173-TSK-0006 recorded the historical cleanup evidence (retired; version history); its observed count is
  not a permanent contract.
- Eight domains have both a tier and an optimization-hardening Description.
  REQ-0026-FR-0005 requires clear ownership; the hardening Descriptions link
  their tier Description, but the pairs are not consolidated, and their unique
  content prevents resolving that through simple retirement.
- A missing source object or insufficient history prevents recovering a removed
  body. It remains an explicit limit, never a reason to keep a copy in Stage 98.
- Deleting a document does not erase Git history, clones, caches, or forks.
  Security response remains a separate workflow.

## Traceability

### Requirement Mapping

- [REQ-0026 Document retention and retirement](../../01.requirements/0026-document-retention-and-retirement.md)

### Currentness and Lineage

- ADR-0030, ADR-0031, ADR-0033, ADR-0035 and ADR-0036 were retired; their numbers are reserved and version history holds their bodies.
- SPEC-0248, SPEC-0249, SPEC-0250 and SPEC-0260 (retired; version history) delivered the Stage 98 check removal and deletion, the completed-package deletion rule and the generation 6 proof source.
- [Documentation protocol](../../../.agents/governance/documentation-protocol.md)

#### Evolution

- A new lifecycle rule enters through the Registry and its validator together,
  so the declaration and the check never diverge.
