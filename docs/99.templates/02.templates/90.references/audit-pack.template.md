---
title: "{{TITLE}}"
version: "0.1.0"
type: "reference/audit-pack"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "references"
artifact_id: "{{ARTIFACT_ID}}"
created: "{{CREATED}}"
observed_at: "{{OBSERVED_AT}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: `observed_at` is the observation date and keeps its original value; add optional `reviewed_at` (and `next_review_at` for research and data) after it only when a later review happens. -->
<!-- Author prompt: Write body prose in Korean; keep headings, paths, identifiers, and commands unchanged. -->

# {{TITLE}}

## Responsibility

### Purpose

<!-- Author prompt: State the audit objective and the scope of this package. -->

{{OBJECTIVE_AND_SCOPE}}

### Excluded Responsibilities

<!-- Author prompt: Name what this audit does not cover and its limitations. -->

{{EXCLUSIONS_AND_LIMITATIONS}}

## Current Contents

### Paths

<!-- Author prompt: List each member that exists now, one Path and Purpose row per member. -->

| Path | Purpose |
| --- | --- |
| {{DIRECT_CHILD_PATH}} | {{AUDIT_MEMBER_PURPOSE}} |

### Owners

<!-- Author prompt: Name the owner of this README and the owner of a listed document only where that document or this README states it; say so in a sentence when it records none. -->

{{OWNERS}}

## Usage

### Entry Points

<!-- Author prompt: Link the current authority documents and the actions this audit assigns. -->

{{ACTIONS_AND_AUTHORITY_LINKS}}

### Checks

<!-- Author prompt: State the criteria, the evidence and the conformance result. -->

{{CRITERIA_EVIDENCE_AND_CONFORMANCE}}
