---
title: "Document Retention and Retirement Requirements"
version: "2.0.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-28"
layer: "requirements"
artifact_id: "REQ-0026"
parent_ids: []
created: "2026-09-01"
---

# Document Retention and Retirement Requirements

## Problem and Goals

Retention rules must outlive the change that introduced them. A document remains
current while it owns current meaning; when it leaves, readers must still find
what existed, why it left, its current owner, and recoverable source evidence.
Capture facts, current assessment, and availability are distinct. Age, corpus
size, and absent incoming links cannot by themselves authorize deletion.

## Stakeholders and User Needs

- Maintainers need durable retention and review criteria independent of old Tasks.
- Agents need enforceable lifecycle, approval, preservation, and citation boundaries.
- Auditors need discoverable provenance and the original context of decisions.

## Functional Requirements

- **REQ-0026-FR-0001**: Retention uses lifecycle and ownership. Age and corpus
  size may trigger review but never determine automatic removal.
- **REQ-0026-FR-0002**: Withdrawal preserves the original unit under `retired/`
  and exactly one withdrawal record: its paired sealed Tombstone or its
  Retention Catalog row. Later approved history-only availability retains that
  capture evidence and satisfies all reassessment and removal preconditions.
- **REQ-0026-FR-0003**: Registered checks reject removal without its required
  record, regardless of incoming links, including removal of both payload and
  catalog row. Partial removal, renaming, and rewriting are not whole-unit
  disposition.
- **REQ-0026-FR-0004**: Still-current obligations, decisions, structure, and
  procedures move to their canonical governance, Stage 01, 02, or 05 owner before
  their source is retired.
- **REQ-0026-FR-0005**: Every implemented capability has a Stage 01 Requirement
  owner and a Stage 02 Description or ADR owner. Stage 03 retirement preserves
  that coverage.
- **REQ-0026-FR-0008**: A Tombstone mirrors its retired route's stage namespace.
  First use creates the namespace; its absence permits neither unrecorded
  removal nor a blanket prohibition on retirement.
- **REQ-0026-FR-0009**: Stage 03 occupancy is judged per package using registered
  Spec, Plan, and Task terminal sets. A completed Spec may wait in Stage 03 with
  a completed Plan and only completed or validly cancelled Tasks. Completion
  receipts cover every numbered Spec criterion and Plan work unit before any
  move. In an unfinished package, completed and validly cancelled Tasks may
  remain but a terminal Plan may not. A cancelled or superseded Spec keeps no
  member in the active stage. Other stages keep per-document disposition rules.
  Cancellation records a reason, approver, valid approval date, and criterion
  dispositions: reassignment to another non-cancelled package Task or approved
  withdrawal reason. Empty criteria means no assigned criteria; withdrawal
  never exempts a criterion still numbered in the Spec from PASS evidence.
  Waiting grants neither new work nor disposition permission. A separately
  authorized later move preserves the entire prepared package, including its
  Spec outcome, Plan, Tasks, receipts, and original Commit Ledgers.
- **REQ-0026-FR-0010**: Stage 03 packages contract bounded changes. Steady-state
  meaning belongs to Stage 02 Descriptions and Stage 05 subjects and transfers
  there before retirement.
- **REQ-0026-FR-0011**: Stages 01 through 05 maintain bidirectional traceability
  through cross-links; domain requirements need not duplicate this obligation.
- **REQ-0026-FR-0012**: Captured bodies and envelopes are immutable. New captures
  match one prepared source Git object exactly in full blob bytes, Git modes,
  and member set. Pre-cutover captures and the explicit ADR-0036 bootstrap
  retain only their registered legacy lifecycle-field allowances; they are
  never rewritten to the new format. Git canonical identity and checkout
  conversion are distinguished. External filters and frozen renormalization
  are not validation or repair methods. Source history must be reachable and
  required objects recoverable; missing history is not success. Current
  authoring templates are not retroactive requirements on frozen records.
- **REQ-0026-FR-0013**: Stage 98 capture classes are `completed/`, `superseded/`,
  `retired/`, and `resolved/`. Route dispositions `tombstones/` and `migrations/`
  hold no body. First use creates a disposition directory. Disposition requires
  separate approval; capture classification does not determine current use.
  A unit has at most one optional current assessment row
  in the existing catalog. Assessment is `unreviewed`, `usable`, `superseded`,
  `withdrawn`, or `invalidated`; availability is independently `retained` or
  `git-history-only`. No row means unreviewed/retained. Actual assessments record
  a decision, reason, date, hold, and conditional current owner; superseded
  requires a real successor. Keep earlier judgments in Git, forbid deletion
  merely to regain defaults, and require evidence for invalidated-to-usable.
  History-only removal requires separate approval scoped
  to the unit, action, and date; reassessment; no hold; consumer cutover;
  recoverability; and complete unit absence. Verify the pinned Task's authority
  and scope at its original revision. A named approver, unrelated Task, or
  proposed ADR is insufficient. Preserve the capture row and route discovery
  through it. History-only never claims erasure of clones or Git history;
  `purged` is not a supported availability. Actual removal is not authorized by
  test approval or standard adoption.

- **REQ-0026-FR-0014**: Citation follows the registered ordered policy: resolve
  path/profile/unit; apply assessment and availability restrictions; block route
  records; apply source-profile/class permissions; resolve current owner or
  historical context; validate link integrity. `withdrawn`, `invalidated`, and
  history-only units cannot be ordinary direct payload targets, including from
  Incident/Postmortem. Retained completed/resolved bodies are historical
  evidence; current rules cite current owners. Incident/Postmortem may cite
  other retained classes subject to the preceding restrictions. Route records
  have no such exception. Frozen links use source commit and original path;
  current catalog and assessment links use the current tree.
- **REQ-0026-FR-0015**: No second Archive recovery ledger is introduced. A unit's
  capture envelope names its source Git object once; Git supplies historical
  recovery. Existing Task Commit Ledgers remain original execution evidence.
- **REQ-0026-FR-0016**: A resolved Incident carries its actual nonempty
  `resolved_at` value. Its bundle and corrective-work owner preserve closure
  evidence without claiming all corrective work is complete.

## Non-functional Requirements

- **REQ-0026-NFR-0006**: Checks derive judgments from the selected tree,
  Registry, catalog, and preservation history. Fixed corpus counts and custom
  digest or expected-commit ledgers do not decide retention. Explicit contract
  cutovers identify verification generations rather than permitted content.
- **REQ-0026-NFR-0007**: One preservation unit has one capture record, not one
  record per package member. Resource bounds protect validation, never justify
  deleting records to satisfy a limit.

## Constraints

- The exact-preservation cutover is the registered baseline
  `be949f338056ee05ca139ea72403576aa18f21d8`; captures already present there retain
  legacy comparison. The named ADR-0036 bootstrap exception permits only its
  registered metadata transition. All other new captures use prepared full-byte
  originals. Do not invent source commits without commit authorization.
- Packages captured while ADR-0031 was accepted may historically contain only
  their Spec. Preserve that scope; do not manufacture missing members.
- Keep sealed Tombstones and Migrations in their original form. Assessment does
  not change capture disposition, source envelope, or original terminal status.
- Distinguish worktree, index, target commit, and original-link context. Missing
  objects, unsupported object formats, gitlinks, and external large-object
  recovery are explicit verification limits. Do not fetch or execute filters
  merely to conceal a limit.
- Restore history into a separately explained current owner; do not silently
  recreate a removed frozen unit as current authority. Secret exposure requires
  separately authorized security response, not ordinary archive removal.

## Acceptance Criteria

- Unrecorded whole-unit and partial removal fail, even when the catalog row is
  removed with the payload.
- Withdrawal records remain unique and source objects resolve at their original
  paths. History-only approval is verified at its pinned original revision.
- A waiting completed package passes occupancy only with terminal members,
  valid cancellations, and complete PASS receipts. Withdrawal alone never
  satisfies a still-numbered criterion.
- Preservation rules can be read from governance without loading a Spec Package.
- New captures preserve full Git identity; legacy captures and original Task
  execution evidence remain unchanged. Whole-package captures include all
  registered members.
- Reassessment does not mutate capture facts; holds, missing approval, missing
  history, and unresolved consumers block removal.
- Ordered citation checks apply assessment restrictions before Incident
  exceptions, and no current link points at a removed payload.
- Current metadata, lifecycle, catalog, link, and affected regression checks
  pass on the explicitly selected snapshot; unavailable checks are reported.

## Traceability

- [Documentation protocol](../../.agents/governance/documentation-protocol.md)
- [Document lifecycle architecture](../02.architecture/descriptions/0030-document-lifecycle-governance.md)
- ADR-0031, ADR-0033, ADR-0035, and ADR-0036 are superseded historical decisions.
- [ADR-0037 Archive lifecycle and preservation decision](../02.architecture/decisions/0037-package-disposition-wait-and-task-cancellation.md)

## Related Documents

- [Stage authoring matrix](../../.agents/governance/stage-authoring-matrix.md)
- [Stage 99 registry](../99.templates/registry.json)
