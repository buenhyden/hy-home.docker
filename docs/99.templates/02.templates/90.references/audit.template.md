---
title: "{{TITLE}}"
version: "0.1.0"
type: "reference/audit"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "references"
artifact_id: "{{ARTIFACT_ID}}"
parent_ids:
- "{{PARENT_ID}}"
created: "{{CREATED}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in English; keep headings, paths, identifiers, and commands unchanged. -->

# {{TITLE}}

## Scope

### Subject

<!-- Author prompt: Name the claim or surface audited and the criteria it is held to. -->

{{AUDIT_SUBJECT_AND_CRITERIA}}

### Read Coverage

<!-- Author prompt: Name what was actually read or run, at which revision, and what was not. -->

{{READ_AND_RUN_COVERAGE}}

## Findings

### Evidence

<!-- Author prompt: List each finding in the table: Finding ID a stable identifier within this member, Requirement the current obligation, Evidence what was directly checked, Classification one of confirmed, gap, conflict, unverified or not-applicable, Action the concrete fix, Owner who does it, and Acceptance the condition that closes it. -->

| Finding ID | Requirement | Evidence | Classification | Action | Owner | Acceptance |
| --- | --- | --- | --- | --- | --- | --- |
| {{FINDING_ID}} | {{REQUIREMENT}} | {{EVIDENCE}} | {{CLASSIFICATION}} | {{ACTION}} | {{OWNER}} | {{ACCEPTANCE}} |

### Conflicts and Gaps

<!-- Author prompt: Explain each conflict or gap between claim and evidence and its impact. -->

{{CONFLICTS_AND_GAPS}}

## Actions

### Owners

<!-- Author prompt: Name the current work and its owner for each finding that needs action. -->

{{OWNERS}}

### Acceptance Conditions

<!-- Author prompt: State the evidence that closes each action. -->

{{ACCEPTANCE_CONDITIONS}}
