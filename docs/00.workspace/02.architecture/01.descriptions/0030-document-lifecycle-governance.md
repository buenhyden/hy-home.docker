---
title: "Document Lifecycle Governance Architecture"
version: "3.1.1"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "architecture"
artifact_id: "AD-0030"
parent_ids:
- "REQ-0026"
created: "2026-09-01"
---

# Document Lifecycle Governance Architecture

## Context and Boundaries

### System Boundary

Inside the boundary are the Stage 99 Registry, current stage trees, and
registered document validators. Stage 98 holds only its README. Git provides
removed bodies and historical approval context. CI chooses trusted comparison
snapshots but does not grant retirement authority. Runtime systems, secret
access, and remote integration remain separately authorized actions.

#### Purpose and Readers

The Registry defines document shape and retired numbers; current stage owners
retain durable meaning, Tasks record actual execution, and version history is the
record of removed bodies. Approval, criterion acceptance, and retirement are
separate facts.

Governance owns when documents remain current, leave active stages, are
reassessed, and may be removed from the working tree. This Description explains
which components read which authority and what their checks establish.
Maintainers and agents use the same contracts before claiming completion.

#### Context

Maintainers and agents read the Stage 99 Registry, current stage trees and registered validators. CI chooses trusted comparison snapshots, and Git supplies removed bodies and historical approval context.

### Constraints

Runtime systems, secret access and remote integration remain separately authorized actions. Validators are read-only, fail closed on unsafe traversal or an invalid Registry, and keep Git reads, enumeration and file data within resource limits.

## Structure

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

### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Stage 99 Registry contract | [Stage 99 Registry](../../../99.templates/registry.json) loaded by `scripts/lib/document_governance/registry.py` | Document validators and `metadata/heading.py` | [Stage 99 Registry](../../../99.templates/registry.json) | A missing, symlinked, unreadable or invalid Registry yields findings. |
| Metadata, document-link and corpus-lifecycle gate entrypoints | Registered validators in `scripts/manifest.yaml` | `scripts/validation/run-ci-gate.py` and maintainers and agents | `scripts/manifest.yaml` | Unsafe traversal yields findings; exceeding a resource limit is a diagnostic. |
| Git comparison base | Git (`HEAD` locally, trusted base supplied by CI) | `spec_packages.py` and `identity_history.py` | The description links no contract for this interface. | A missing source object or insufficient history prevents recovering a removed body, and the checker reports that limit. |
| Task approval references | Current Task approval headings | The cancellation reader | [Approval Boundaries](../../04.quality/approval-boundaries.md#authorization-source-and-records) | Unresolved required approval references and unsupported source labels yield findings. |

- The Registry is the machine authority for profile shape, lifecycles, identity spaces and each space's `reserved_history`.
- Metadata, document-link and corpus-lifecycle entrypoints expose the judgments through gate profiles registered in `scripts/manifest.yaml` and selected by `scripts/validation/run-ci-gate.py`.
- `metadata/heading.py` enforces the Registry's section contracts.

## Runtime Behavior

### Normal Flow

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

Cancellation uses one structural judgment for occupancy and package validation.
The current Task shape requires `reason`, `authorization_ref`, and
`criteria_disposition`. Each disposition names a criterion and either a
`successor` or a `withdrawal_ref`. Reassignment stays in the package and cannot
point to the same Task or another cancelled Task. The criterion keeps its
completion obligations. An empty list records that no acceptance criterion
was assigned. The reader checks that approval references
resolve to unique same-Task headings with supported source labels. The current
trusted approval is resolved through
[Approval Boundaries](../../04.quality/approval-boundaries.md#authorization-source-and-records).

Retirement summarizes the removed record's still-current substance into its
Stage 01 or Stage 02 owner's lineage section and deletes the original in the same
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

### Failure and Recovery

Unsafe traversal, unresolved required approval references, unsupported source
labels, and a missing, symlinked, unreadable or invalid Registry yield findings.
Exceeding a resource limit is a diagnostic. A missing source object or
insufficient history prevents recovering a removed body, and the checker
reports that limit.

## Quality Scenarios

### Scenarios

#### Quality Attributes

- Fail closed: unsafe traversal, invalid recorded approval references and
  a missing, symlinked, unreadable or invalid Registry yield findings.
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

### Trade-offs

- Retirement summarizes and deletes instead of keeping copies, so version
  history is the only record of removed bodies; a missing source object or
  insufficient history prevents recovery and remains an explicit limit, never
  a reason to keep a copy in Stage 98 (Runtime View, Risks).
- Git reads, enumeration and file data are bounded; exceeding a limit is a
  diagnostic, never an automatic retention action (Quality Attributes).
- Metadata `check-changed` judges only introduced violations, so a
  changed-only pass does not prove corpus-wide cleanup (Risks).
- Eight tier and optimization-hardening Description pairs stay unconsolidated
  because their unique content prevents resolving them through simple
  retirement (Risks).
- Deleting a document does not erase Git history, clones, caches or forks;
  security response remains a separate workflow (Risks).

## Decisions and Adoption

### Decisions

- [ADR-0037 Package waiting and Task cancellation](../02.decisions/0037-package-disposition-wait-and-task-cancellation.md)
- [ADR-0051 Summarize-and-delete retirement](../02.decisions/0051-summarize-and-delete-retirement.md)
- [ADR-0032 Canonical agent governance home](../02.decisions/0032-canonical-agent-governance-home.md)
- [ADR-0048 Authority parents and criterion acceptance](../02.decisions/0048-authority-parents-and-criterion-acceptance.md)

### Adoption Boundaries

#### Requirement Mapping

- [REQ-0026 Document retention and retirement](../../../01.requirements/0026-document-retention-and-retirement.md)

#### Currentness and Lineage

- ADR-0030, ADR-0031, ADR-0033, ADR-0035 and ADR-0036 were retired; their numbers are reserved and version history holds their bodies.
- SPEC-0257 and SPEC-0261 (retired; version history) delivered the second implementation-alignment corrections of paths, links, Registry exceptions and secret names, and the REQ-0027 approval with the promotion of its dependent documents.
- SPEC-0259 (retired; version history) delivered the third implementation-alignment corrections: Stage 02 labels that named deleted Spec paths, the OpenBao audit wording, the ADR-0038 acceptance and the promotion of matching Stage 05 documents.
- SPEC-0256 (retired; version history) removed the legacy statuses and lineage keys from the Stage 01 to 03 lifecycles and profiles, the archive profiles and templates, and ADR-0011.
- SPEC-0248, SPEC-0249, SPEC-0250 and SPEC-0260 (retired; version history) delivered the Stage 98 check removal and deletion, the completed-package deletion rule and the generation 6 proof source.
- [Documentation protocol](../../03.process/documentation-protocol.md)

#### Evolution

- A new lifecycle rule enters through the Registry and its validator together,
  so the declaration and the check never diverge.
