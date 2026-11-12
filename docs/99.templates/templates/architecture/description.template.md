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

## Overview

### Purpose and Readers

{{PURPOSE_AND_READERS}}

### System Boundary

{{SYSTEM_VERSION_AND_ENVIRONMENT_BOUNDARY}}

## Context and Constraints

### Context

<!-- Author prompt: Name the external actors, neighbouring systems and data flows across the boundary. -->

{{EXTERNAL_ACTORS_SYSTEMS_AND_DATA_FLOWS}}

### Constraints

{{REQUIREMENT_QUALITY_TECHNICAL_AND_SECURITY_CONSTRAINTS}}

## Current Structure

### Building Blocks

{{COMPONENTS_RESPONSIBILITIES_AND_OWNERS}}

### Runtime and Deployment

{{RUNTIME_DEPLOYMENT_AND_ENVIRONMENT_DIFFERENCES}}

## Interfaces

### Contracts

{{INPUTS_OUTPUTS_CALLS_SCHEMAS_AND_COMPATIBILITY}}

### Failure Boundaries

{{FAILURE_RETRY_ISOLATION_AND_RECOVERY_BOUNDARIES}}

## Decisions

### Decision Links

{{EFFECTIVE_ADRS_AND_REASONS}}

### Quality and Risks

{{QUALITY_SCENARIOS_RISKS_AND_OWNERS}}

## Traceability

### Requirement Mapping

{{REQUIREMENT_AND_DESIGN_CONSTRAINT_LINKS}}

### Currentness and Lineage

<!-- Author prompt: State what is current, what it replaced and where history lives; historical links are non-authoritative. -->

{{CURRENT_VERSION_REPLACEMENTS_AND_HISTORY}}
