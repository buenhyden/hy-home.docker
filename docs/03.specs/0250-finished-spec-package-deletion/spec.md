---
title: "Completed Spec Package Deletion"
version: "0.1.2"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0250"
parent_ids:
- "REQ-0026"
- "AD-0030"
created: "2026-11-03"
---

# Completed Spec Package Deletion

## Overview

### Intent

SPEC-0249 deleted Stage 98 and moved retired numbers into the Registry
`reserved_history`. The user directed that completed Spec, Plan, and Task
documents in `docs/03.specs/` be deleted too, and chose to keep every package
that still has an unfinished Task, together with its completed Tasks.

### Owning Requirements

SPEC-0250 has parent_ids REQ-0026 and AD-0030. It makes concrete REQ-0026 (document retention and retirement) and the AD-0030 document lifecycle architecture constraint that a completed package is removed and its number reserved. The body cites no REQ-0026-FR or NFR identifier.

## Scope

### In Scope

Delete each package whose Spec, Plan, and every Task are terminal; reserve its
number; turn current links to it into plain text; drop typed references to it;
and let the checks accept the result. Packages with any non-terminal Task stay
whole. The branch-integration receipt handoff and other Stage 98 readers belong
to the PR #723 review fix, not to this Spec.

### Non-goals

The branch-integration receipt handoff and other Stage 98 readers named at the end of the In Scope paragraph are outside this Spec.

## Behavior Contract

### Normal Behavior

- A deleted package's Spec number is in the Registry Spec `reserved_history`.
- No current document links into a deleted package or names it in
  `parent_ids`, `supersedes`, or `superseded_by`; prose may name the ID for
  lineage.
- A terminal Task body stays unchanged. Link alignment excuses a missing target
  only for a link from a terminal Task at a registered Task path into a package
  whose number the checked root's Registry reserves.
- Generation 7 historical admission reads only packages still in the tree.
- SPEC-0209 and SPEC-0231 stayed in this batch, because current terminal
  Tasks were admitted through the migration proofs they carried; SPEC-0260
  later read those proofs from the generation 6 revision and deleted both.
- A package is deleted only when it is ready for removal review and its
  removal is approved; the user's instruction approves this batch, and the Task
  records it with each package's criterion state.

### Failure and Edge Cases

An edited terminal Task body, a deleted package with a non-terminal Task, an
unreserved deleted number, or a link exemption that excuses any other missing
target fails this Spec.

## Acceptance Criteria

### Criteria

1. Every removal-ready package except the two proof carriers is deleted and its
   number reserved; every package with a non-terminal Task remains.
2. No current document links into a deleted package or names one in a typed
   reference, and governance describes the deletion rule.
3. Link alignment, corpus lifecycle, and metadata checks pass without editing
   any terminal Task body.
4. The document-governance, lifecycle, gate, and CI plan suites pass locally,
   with actual results in the Task.

### Evidence Requirements

- Criterion 1 is observed in the package tree and the Registry Spec `reserved_history`; the Task records each package's criterion state.
- Criteria 2 and 3 are verified through the link alignment, corpus lifecycle and metadata checks, with results recorded in the Task evidence rows.
- Criterion 4 is verified by running the document-governance, lifecycle, gate and CI plan suites locally; the actual results go in the Task.
- The frontmatter owner judges each criterion and records the decision in the Task's Criterion Acceptance table.

## References

### Normative and Evidence

- [Plan](plan.md)
- [Task](tasks/tsk-0001-finished-spec-package-deletion.md)
- [Stage 98 archive deletion](../0249-stage98-archive-deletion/spec.md)
- [Document retention requirement](../../01.requirements/0026-document-retention-and-retirement.md)
- [Document lifecycle architecture](../../02.architecture/descriptions/0030-document-lifecycle-governance.md)

### Historical and Navigation

No historical or navigation link applies.
