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

<!-- Author prompt: List every FR and NFR in this table: Requirement ID is its full identity, Statement the needed behaviour or quality, Rationale why it is needed, Acceptance the judgeable condition, and Priority must, should or could. Statement repeats the declaration. Priority follows its modal verb: a declaration without one binds as must in an approved package. The declarations follow under their subsections; keep this table directly under Requirements so it is not read as a declaration. -->

| Requirement ID | Statement | Rationale | Acceptance | Priority |
| --- | --- | --- | --- | --- |
| {{REQUIREMENT_ID}} | {{STATEMENT}} | {{RATIONALE}} | {{ACCEPTANCE}} | {{PRIORITY}} |

<!-- Author prompt: When a quality requirement applies, measure each NFR in this table: Attribute is the quality characteristic, Measure the measurement definition, Unit its unit, Environment where it is measured, and Criterion the accepted value. Otherwise delete the table. -->

| Requirement ID | Attribute | Measure | Unit | Environment | Criterion |
| --- | --- | --- | --- | --- | --- |
| {{QUALITY_REQUIREMENT_ID}} | {{ATTRIBUTE}} | {{MEASURE}} | {{UNIT}} | {{ENVIRONMENT}} | {{CRITERION}} |

### Functional Requirements

<!-- Author prompt: Give each requirement its rationale and priority. Write an interface need as a functional requirement; no IF identity is issued. -->

- **REQ-####-FR-####**: {{FUNCTIONAL_REQUIREMENT}}

### Quality Requirements

<!-- Author prompt: Declare each quality requirement here; when none applies, say so and why. -->

- **REQ-####-NFR-#### — {{QUALITY_CHARACTERISTIC}}**: {{QUALITY_REQUIREMENT}}; measure: {{MEASURE_UNIT_ENVIRONMENT_AND_ACCEPTANCE}}

## Traceability

### Sources

<!-- Author prompt: Name the sources and governing constraints this package rests on. -->

{{SOURCES_AND_GOVERNING_CONSTRAINTS}}

### Verification Links

<!-- Author prompt: State each acceptance condition, how it is judged, the evidence it needs and who decides, and link only existing architecture, Spec and verification documents. -->

{{ACCEPTANCE_VERIFICATION_AND_DOWNSTREAM_LINKS}}
