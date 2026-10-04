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

{{OVERVIEW}}

## Boundaries and Inputs

{{BOUNDARIES_AND_INPUTS}}

## Behavior Contract

{{OBSERVABLE_BEHAVIOR}}

## Technical Approach

{{CHANGE_SCOPED_DESIGN}}

## Interfaces and Data

{{INTERFACES_AND_DATA}}

## Failure Modes and Guardrails

{{FAILURE_MODES_AND_GUARDRAILS}}

## Acceptance Contract

<!-- Author prompt: Use a numbered list of observable criteria; keep those numbers stable while Plan and Task evidence refers to them. -->
<!-- Author prompt: A completed criterion needs observed PASS evidence in its Task. Cancellation disposition never waives Spec completion evidence. -->

{{ACCEPTANCE_CONTRACT}}

## Traceability

{{FULL_REQUIREMENT_AND_ARCHITECTURE_IDS}}

## Open Questions

{{OPEN_QUESTIONS}}

## Operational Impact

{{OPERATIONAL_IMPACT}}
