---
title: "Document Lifecycle Governance Architecture"
version: "2.0.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-28"
layer: "architecture"
artifact_id: "AD-0030"
parent_ids:
- "REQ-0026"
created: "2026-09-01"
---

# Document Lifecycle Governance Architecture

## Overview

### Overview

## Scope

### Scope

### Context and Stakeholders

Governance owns when documents remain current, leave active stages, are
reassessed, and may be removed from the working tree. This Description explains
which components read which authority and what their checks establish.
Maintainers and agents use the same contracts before claiming completion.

### System Boundaries

Inside the boundary are the Stage 99 Registry, current stage trees, Stage 98
capture catalog and optional current assessments, and registered document
validators. Git provides source objects and historical approval context. CI
chooses trusted comparison snapshots but does not grant disposition authority.
Runtime systems, secret access, remote integration, and actual archival removal
remain separately authorized actions.

### Traceability

- [REQ-0026 Document retention and retirement](../../01.requirements/0026-document-retention-and-retirement.md)
- ADR-0031, ADR-0033, ADR-0035, and ADR-0036 are superseded historical decisions.
- [ADR-0037 Archive lifecycle and preservation decision](../decisions/0037-package-disposition-wait-and-task-cancellation.md)
- [Documentation protocol](../../../.agents/governance/documentation-protocol.md)

## Architecture

### Architecture

### Components

- `scripts/lib/document_governance/registry.py` loads profiles, lifecycles,
  identity spaces, and archive contracts. The Registry is the machine authority
  for their shape and permitted values.
- `scripts/lib/document_governance/spec_packages.py` loads bounded current and
  historical package snapshots, validates completion receipts, and supplies the
  shared cancellation judgment and acceptance-criterion parser.
- `scripts/lib/document_governance/archive.py` resolves preservation units,
  occupancy, capture identity, current assessments, and recovery prerequisites.
  Capture facts and current assessment remain separate inputs.
- `scripts/lib/document_governance/references.py` derives Stage 90 package
  membership and enforces each protected package's preservation declaration.
- `scripts/lib/document_governance/links.py` applies the registered ordered
  citation policy. Current assessment and availability restrictions precede
  Incident/Postmortem exceptions; route records never gain a body exception.
- Registered metadata, document-link, and corpus-lifecycle entrypoints expose
  these judgments through gate profiles. `metadata/heading.py` enforces the
  Registry's section contracts so authored declarations and checks agree.
- `docs/98.archive/retention-catalog.md` owns unit capture rows and optional
  current assessments. The Archive README routes discovery without duplicating
  that catalog. Capture classes are completed, superseded, retired, and
  resolved; Tombstones and Migrations hold routes rather than original bodies.
  Disposition directories are created on first use.

### Data Flow

Load Registry contracts before classifying documents. Enumerate the selected
current snapshot and read the comparison base through bounded Git operations.
A member missing from a retained package differs from an entire package leaving
Stage 03. Withdrawal requires its unique record and a preserved original;
completed packages retain their Spec, Plan, and Task execution evidence.
A sealed paired Tombstone and a Retention Catalog row are alternative withdrawal
records, not duplicate records for one unit.

Completion and disposition are separate. Write permanent outcomes into current
owners and final evidence into the Task. A completed Spec may wait with a
completed Plan and only completed or validly cancelled Tasks. Its receipt must
already cover every numbered acceptance criterion and Plan work unit. In an
unfinished package, completed and validly cancelled Tasks may remain, but a
terminal Plan may not. Cancelled or superseded Specs keep no members in active
Stage 03. The occupancy branch reads per-profile terminal sets from Registry;
standalone documents retain their existing per-document rule.

Cancellation uses one pure judgment for occupancy and package validation. It
requires reason, approver, actual approval date, and a list of criterion
reassignments or withdrawal reasons. Reassignment stays in the package, cannot
point to itself or another cancelled Task, and never waives completion coverage.
An empty list records that no acceptance criterion was assigned.

An authorized later capture names one prepared source commit/path. Existing
captures at `be949f338056ee05ca139ea72403576aa18f21d8` retain their legacy
member/mode/body comparison and registered lifecycle metadata allowances. The
explicit ADR-0036 bootstrap uses the same narrow allowance. Other new captures
compare complete raw blob bytes, modes, and member sets. The implementation
keeps raw Git identity distinct from checkout representation and never invokes
external filters or renormalizes frozen records. Frozen links resolve using
source revision and original path; current catalog links resolve currently.

A current assessment row supplements a capture; it does not rewrite it. One row
per unit records assessment, independent availability, decision, reason, date,
hold, and conditional current owner. No row defaults to unreviewed/retained.
Git retains previous judgments; removing an assessment to regain that default
is invalid. Superseded requires a real current successor; rehabilitation of
invalidated evidence requires an explicit reason and decision.

History-only removal additionally requires approval for the exact unit, action,
and date, verified in the pinned Task at its original revision. Reassessment,
no hold, current-consumer cutover, reachable source history, recoverable objects,
and whole-unit absence are all required. The capture envelope remains available
for discovery. An approver name or proposed ADR alone grants nothing. Past
valid approval is not invalidated merely because its authoring Task later
leaves the active stage. Destructive test fixtures never authorize real removal.

Citation resolution proceeds through path/profile/unit, assessment and
availability restrictions, route blocking, source-profile/class permissions,
current-owner or historical-context checks, and physical link integrity.
Withdrawn, invalidated, and history-only payloads are blocked before incident
exceptions. Archive index/catalog discovery is distinguished from normative
citation; retained completed and resolved bodies remain historical evidence.

### Deployment View

Validators are registered in `scripts/manifest.yaml` and selected by
`scripts/validation/run-ci-gate.py`. Local comparison normally uses `HEAD`; CI
supplies its trusted base. Evidence identifies whether validation examined the
worktree, index, target commit, or historical source context. These read-only
checks do not write to Stage 98 or operate services. Full gate or remote runs
retain their own authorization and execution evidence requirements.

### Risks

- Metadata `check-changed` compares current and base bodies with
  `changed_boundary=True` to reject newly introduced template instructions and
  tokens. Two template-source calls using `False` in `reference.py` do not
  disable that production path. Existing debt and introduced violations are
  distinct; a changed-only pass does not prove corpus-wide cleanup.
- `TARGET_TEMPLATE_LITERALS` retains the residual `<!-- Target:` marker rule.
  Current templates and metadata reports no longer generate the marker.
  SPEC-0173-TSK-0006 owns the historical cleanup evidence; its observed count is
  not a permanent contract.
- Eight domains were observed to have both base and optimization-hardening
  Descriptions without declared relationships. REQ-0026-FR-0005 requires clear
  ownership; unique content prevents resolving that known debt through simple
  retirement. It needs consolidation or an explicit hierarchy.
- A missing source object or insufficient history prevents a recovery claim.
  Unsupported object formats, gitlinks, external large-object content, and
  checkout conversions must remain explicit limits, not automatic fetches,
  filter execution, false success, or permission to change frozen bytes.
- History-only availability does not imply secure erasure of Git history,
  clones, caches, or forks. Security response remains a separate workflow.

## Quality Attributes

- Fail closed: unsafe traversal, missing approval, missing source objects, and
  unsupported recovery contexts yield findings instead of exemptions.
- Derived: membership and current judgments come from Registry, selected trees,
  and preserved history rather than fixed counts or invented digest ledgers.
- Bounded: Git reads, directory enumeration, and file data have resource limits;
  exceeding one is a diagnostic, never an automatic retention action.
- Immutable evidence: captures, original Task Commit Ledgers, and sealed records
  remain unchanged. Current assessment history is maintained through Git.
- Separable: governance explains the rule without loading a package; this
  Description explains enforcement without relying on a past execution Task.

## Related Documents

- [ADR-0032 Canonical agent governance home](../decisions/0032-canonical-agent-governance-home.md)
