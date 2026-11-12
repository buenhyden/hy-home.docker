---
title: "Stage 98 Archive Deletion"
version: "0.1.1"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0249"
parent_ids:
- "REQ-0026"
- "AD-0030"
created: "2026-11-03"
---

# Stage 98 Archive Deletion

## Overview

### Intent

SPEC-0248 stopped every gate from validating Stage 98, but current checks still
read archive files for retired lineage, identity allocation, retirement
exemptions, requirement gaps, and preserved predecessors. The user directed that
the archive files be deleted, keeping only the folder scheme and README, that
the still-current substance of the deleted records be summarized into Stage 01
and Stage 02 documents, that current references be removed, and that retired
numbers be kept as a minimal Registry list.

### Owning Requirements

This Spec makes concrete the frontmatter parents REQ-0026 (document retention and retirement) and AD-0030 (document lifecycle governance). The body cites no ADR and no REQ-####-FR or REQ-####-NFR identifier.

## Scope

### In Scope

Delete every file under `docs/98.archive/` except its README; summarize the
Stage 01 and Stage 02 records into their current owners; remove current links
into Stage 98 and typed references to retired identities; replace every reader
of Stage 98 files with the Registry `reserved_history` or remove it; and update
governance. Completed Spec packages in `docs/03.specs/` are out of scope; they
are the next phase.

### Non-goals

Completed Spec packages in `docs/03.specs/` are out of scope and form the next phase, as the In Scope text states; no other exclusion applies.

## Behavior Contract

### Normal Behavior

- `docs/98.archive/` tracks only `README.md`, which describes the disposition
  scheme and is validated like any other README.
- Each top-level identity space for Requirements, ADRs, architecture
  descriptions, and Specs records `reserved_history`: the sorted numbers no
  current document carries. A Stage 01 gap is legitimate exactly when its number
  is reserved, and a Stage 03 package removal is recorded exactly when its Spec
  number is reserved.
- No code reads a file under `docs/98.archive/`. Version history remains the
  record of the removed bodies.
- No current document links into `docs/98.archive/` or names a retired identity
  in `parent_ids`, `supersedes`, or `superseded_by`.
- The terminal-Task exemption of the links `commands` check keys on the
  Registry Task path profile, not on a self-declared `type`.

### Failure and Edge Cases

A current check that still opens a Stage 98 path, a typed reference to a retired
identity, or a summary that drops a still-current obligation fails this Spec.

## Acceptance Criteria

### Criteria

1. Every Stage 98 file except the README is deleted, and every Stage 01 and
   Stage 02 record's lineage is summarized in its current owner's Traceability.
2. No code reads Stage 98 files; requirement gaps and Stage 03 removals use the
   Registry `reserved_history`.
3. No current document links into Stage 98 or names a retired identity in a
   typed reference, and governance describes summarize-and-delete.
4. The document gates, the document-governance and lifecycle suites, the Script
   Manifest, and workflow-contract checks pass locally, with actual results in
   the Task.

### Evidence Requirements

- Each criterion is evidenced by rows in TSK-0001 under `tasks/`, recording the deletion, summary and reference-removal observations and the actual results of the document gates, document-governance and lifecycle suites, Script Manifest and workflow-contract checks.
- The Task owner runs those checks locally; version history is the record of the removed bodies.
- The frontmatter owner (`@buenhyden`) judges each criterion and records the decision in the Task's Criterion Acceptance table.

## References

### Normative and Evidence

- [Plan](plan.md)
- [Task](tasks/tsk-0001-stage98-archive-deletion.md)
- [Document retention requirement](../../01.requirements/0026-document-retention-and-retirement.md)
- [Document lifecycle architecture](../../02.architecture/descriptions/0030-document-lifecycle-governance.md)

### Historical and Navigation

No historical or navigation link applies; every link above is current authority or evidence.
