---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/requirement"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "requirements"
artifact_id: "{{ARTIFACT_ID}}"
created: "{{CREATED}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in English; keep headings, paths, identifiers, and commands unchanged. -->

# {{TITLE}}

## Overview

### Problem and Outcome

{{PROBLEM_AND_OUTCOME}}

### Stakeholders

{{STAKEHOLDERS}}

## Scope

### In Scope

{{IN_SCOPE}}

### Constraints and Exclusions

<!-- Author prompt: State constraints, assumptions, risks and non-goals. Write "None" with a reason when one does not apply. -->

{{CONSTRAINTS_AND_EXCLUSIONS}}

## Requirements

### Functional Requirements

<!-- Author prompt: Give each requirement its rationale and priority. Write an interface need as a functional requirement; no IF identity is issued. -->

- **REQ-####-FR-####**: {{FUNCTIONAL_REQUIREMENT}}

### Quality Requirements

<!-- Author prompt: Include this section only when a quality requirement applies; otherwise delete it. -->

- **REQ-####-NFR-#### — {{QUALITY_CHARACTERISTIC}}**: {{QUALITY_REQUIREMENT}}; measure: {{MEASURE_UNIT_ENVIRONMENT_AND_ACCEPTANCE}}

## Acceptance Criteria

### Acceptance Conditions

{{ACCEPTANCE_CONDITIONS}}

### Verification Method

<!-- Author prompt: Name how each condition is judged, the evidence it needs and who decides. -->

{{VERIFICATION_METHOD}}

## Traceability

### Source and Constraints

{{SOURCES_AND_GOVERNING_CONSTRAINTS}}

### Downstream Links

<!-- Author prompt: Link only existing architecture, Spec and verification documents. -->

{{ARCHITECTURE_SPEC_AND_VERIFICATION_LINKS}}
