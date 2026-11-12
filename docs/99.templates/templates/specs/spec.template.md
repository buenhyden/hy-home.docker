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

### Intent

{{INTENT_AND_USER_VALUE}}

### Owning Requirements

<!-- Author prompt: Name the Requirement IDs and Architecture or ADR constraints this Spec makes concrete; list them in frontmatter `parent_ids` when the Registry requires it. -->

{{OWNING_REQUIREMENTS_AND_CONSTRAINTS}}

## Scope

### In Scope

{{IN_SCOPE}}

### Non-goals

{{NON_GOALS_AND_WITHHELD_AUTHORITY}}

## Behavior Contract

### Normal Behavior

{{PRECONDITIONS_INPUTS_OUTPUTS_AND_INVARIANTS}}

### Failure and Edge Cases

<!-- Author prompt: State violations, boundaries, cancellation, observable failures, recovery and the points where work stops for a human. -->

{{FAILURE_EDGE_AND_STOP_CASES}}

## Acceptance Criteria

### Criteria

<!-- Author prompt: Use a numbered list of observable criteria; keep those numbers stable while Plan and Task evidence refers to them. -->
<!-- Author prompt: An accepted criterion needs PASS evidence and no unresolved FAIL in its Task; only a `not-required` decision closes it without PASS. Cancellation disposition never closes a criterion. -->

{{ACCEPTANCE_CRITERIA}}

### Evidence Requirements

<!-- Author prompt: Use bullets, never a numbered list: every numbered line in this H2 is read as a criterion. Name the observation, the verification method and who judges. -->

{{EVIDENCE_REQUIREMENTS}}

## References

### Normative and Evidence

{{CURRENT_REQUIREMENTS_DESIGN_POLICY_AND_EVIDENCE_LINKS}}

### Historical and Navigation

<!-- Author prompt: Mark historical links as non-authoritative; navigation links only help readers find related documents. -->

{{HISTORICAL_AND_NAVIGATION_LINKS}}
