---
title: "Legacy Document Status Ban Specification"
version: "0.1.1"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0256"
parent_ids:
- "REQ-0026"
- "AD-0030"
created: "2026-11-04"
---

# Legacy Document Status Ban Specification

## Overview

### Intent

ADR-0051 retires a document by summarizing it into its current owner and
deleting it. Stage 01 to 03 lifecycles still offered `deprecated`,
`superseded`, `retired`, and `archived`, and the Registry still carried the
archive profiles and keys that SPEC-0249 left as scheme definitions. The user
directed that Stage 01 to 03 documents allow no legacy or deprecated status or
format, and that existing ones be cleaned up.

### Owning Requirements

SPEC-0256 has parent_ids REQ-0026 and AD-0030. It makes concrete REQ-0026 (document retention and retirement), the AD-0030 document lifecycle architecture and the ADR-0051 summarize-and-delete retirement rule for Stage 01 to 03 documents. The body cites no REQ-0026-FR or NFR identifier.

## Scope

### In Scope

The Stage 01 to 03 lifecycles and profiles in the Registry, the frontmatter and
profile schemas, the Spec Package loader, ADR-0011 (the only `deprecated`
document), the inert `branch_integration_receipts` field, the archive profiles
and templates, and the governance text that names these states. Operational,
reference, and governance profiles keep their own lifecycles.
SPEC-0251 and SPEC-0253 are on main, and SPEC-0252 was never issued.
SPEC-0254 belongs to PR #733 and SPEC-0255 to PR #732, so this package takes
SPEC-0256 and the Registry Spec `high_water` is 256.

### Non-goals

Operational, reference and governance profiles keep their own lifecycles and are outside this Spec, as the last sentences of the In Scope paragraph state.

## Behavior Contract

### Normal Behavior

- The requirement, architecture-description, architecture-decision, Spec,
  Plan, and contract lifecycles have no `deprecated`, `superseded`, `retired`,
  or `archived` status, and their profiles accept no `supersedes` or
  `superseded_by` key.
- A Stage 01 to 03 document that declares one of those statuses fails metadata
  validation with `invalid-status`.
- A replaced or withdrawn Stage 01 to 03 document is summarized into its
  current owner's Traceability and deleted, and its number is reserved.
- `common.archive_retention` keeps only `disposition_entry_statuses`; no
  archive profile, archive template, or branch-integration receipt field
  remains.
- A terminal Task body that records an older format stays unchanged; the rule
  governs current and edited documents.

### Failure and Edge Cases

A Stage 01 to 03 document that can still declare a legacy status, an edited
terminal Task body, or a deleted document whose number is not reserved fails
this Spec.

## Acceptance Criteria

### Criteria

1. No Stage 01 to 03 lifecycle or profile offers a legacy status or lineage
   key, and a document that declares one is rejected.
2. ADR-0011 is summarized into AD-0011 and deleted, its number is reserved, and
   no current document links to it.
3. The archive profiles, templates, unread archive keys, and receipt field are
   gone, and governance states the rule.
4. The document-governance, lifecycle, gate, and CI routing suites pass
   locally, with actual results in the Task.

### Evidence Requirements

- Criterion 1 is observed in the Registry lifecycles, profiles and schemas, and by metadata validation rejecting a legacy status with `invalid-status`.
- Criteria 2 and 3 are observed in the tree and the Registry reserved numbers, and by reading the governance text.
- Criterion 4 is verified by running the document-governance, lifecycle, gate and CI routing suites locally; the actual results go in the Task.
- The frontmatter owner judges each criterion and accepts the Spec.

## References

### Normative and Evidence

- [Plan](plan.md)
- [Task](tasks/tsk-0001-legacy-document-status-ban.md)
- [Document retention requirement](../../01.requirements/0026-document-retention-and-retirement.md)
- [Document lifecycle architecture](../../02.architecture/descriptions/0030-document-lifecycle-governance.md)
- [Summarize-and-delete retirement](../../02.architecture/decisions/0051-summarize-and-delete-retirement.md)

### Historical and Navigation

No historical or navigation link applies; every link below is current authority or evidence.
