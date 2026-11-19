---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/architecture-description"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "architecture"
artifact_id: "{{ARTIFACT_ID}}"
parent_ids:
- "{{PARENT_ID}}"
created: "{{CREATED}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in English; keep headings, paths, identifiers, and commands unchanged. -->
<!-- Author prompt: Describe the current structure only. Link decisions to their ADRs instead of restating them, and mark historical material as non-authoritative. -->

# {{TITLE}}

## Context and Boundaries

### System Boundary

<!-- Author prompt: State the purpose and readers, the system, version and environment boundary, and the external actors, neighbouring systems and data flows across it. -->

{{PURPOSE_BOUNDARY_ACTORS_AND_DATA_FLOWS}}

### Constraints

{{REQUIREMENT_QUALITY_TECHNICAL_AND_SECURITY_CONSTRAINTS}}

## Structure

### Building Blocks

<!-- Author prompt: When a diagram shows the structure, review it against the [C4 diagram review checklist](https://c4model.com/diagrams/checklist). -->

{{COMPONENTS_RESPONSIBILITIES_AND_OWNERS}}

### Interfaces

<!-- Author prompt: When the structure has an external interface, list it in this table: Interface is the boundary, Producer and Consumer its two sides, Contract a link to its input and output meaning, and Failure how a failure is handled. Otherwise delete the table. -->

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| {{INTERFACE}} | {{PRODUCER}} | {{CONSUMER}} | {{CONTRACT}} | {{FAILURE}} |

{{INPUTS_OUTPUTS_CALLS_SCHEMAS_AND_COMPATIBILITY}}

## Runtime Behavior

### Normal Flow

{{RUNTIME_DEPLOYMENT_AND_ENVIRONMENT_DIFFERENCES}}

### Failure and Recovery

{{FAILURE_RETRY_ISOLATION_AND_RECOVERY_BOUNDARIES}}

## Quality Scenarios

### Scenarios

{{QUALITY_SCENARIOS_RISKS_AND_OWNERS}}

### Trade-offs

<!-- Author prompt: Name the quality trade-offs the structure accepts and what each one costs. -->

{{QUALITY_TRADE_OFFS}}

## Decisions and Adoption

### Decisions

{{EFFECTIVE_ADRS_AND_REASONS}}

### Adoption Boundaries

<!-- Author prompt: Map the requirements and design constraints this structure meets, and state what is current, what it replaced and where history lives; historical links are non-authoritative. -->

{{REQUIREMENT_MAPPING_CURRENTNESS_AND_LINEAGE}}
