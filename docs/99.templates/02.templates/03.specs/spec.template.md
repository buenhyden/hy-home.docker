---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "specs"
artifact_id: "{{ARTIFACT_ID}}"
parent_ids:
- "{{PARENT_ID}}"
created: "{{CREATED}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in English; keep headings, paths, identifiers, and commands unchanged. -->
<!-- Author prompt: Contract observable behavior only. Approval, review, and execution are separate facts and must not be inferred from document structure. -->

# {{TITLE}}

## Overview

### Goal

<!-- Author prompt: State the change and its value, and name the Requirement IDs and Architecture or ADR constraints this Spec makes concrete; list them in frontmatter `parent_ids` when the Registry requires it. -->

{{GOAL_PARENT_REQUIREMENTS_AND_VALUE}}

### Consumers

<!-- Author prompt: Name the people, documents, scripts and services that read or act on this contract. -->

{{CONSUMERS}}

## Scope

### In Scope

{{IN_SCOPE}}

### Out of Scope

<!-- Author prompt: Name what this Spec excludes and the authority it withholds. -->

{{OUT_OF_SCOPE_AND_WITHHELD_AUTHORITY}}

## Behavior Contract

### Inputs and Outputs

<!-- Author prompt: State the preconditions, inputs, outputs and invariants of normal behavior. -->

{{PRECONDITIONS_INPUTS_OUTPUTS_AND_INVARIANTS}}

### Failure Behavior

<!-- Author prompt: State violations, boundaries, cancellation, observable failures, recovery and the points where work stops for a human. -->

{{FAILURE_EDGE_AND_STOP_CASES}}

## Acceptance Criteria

### Criteria

<!-- Author prompt: Use a numbered list of observable criteria; keep those numbers stable while Plan and Task evidence refers to them. -->
<!-- Author prompt: An accepted criterion needs PASS evidence and no unresolved FAIL in its Task; only a `not-required` decision closes it without PASS. Cancellation disposition never closes a criterion. -->

{{ACCEPTANCE_CRITERIA}}

### Verification Strategy

<!-- Author prompt: Use bullets or the table, never a numbered list: every numbered line in this H2 is read as a criterion. List each check the criteria need: Check ID is a stable identifier in this Spec, Guarantee what only that check proves, Input what it reads, Trust Boundary what it does not prove, Required When the condition that selects it, and Evidence the kind of observation it must produce. -->

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| {{CHECK_ID}} | {{GUARANTEE}} | {{INPUT}} | {{TRUST_BOUNDARY}} | {{REQUIRED_WHEN}} | {{EVIDENCE}} |

{{VERIFICATION_STRATEGY}}
