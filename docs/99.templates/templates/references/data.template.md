---
title: "{{TITLE}}"
version: "0.1.0"
type: "reference/data"
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

# {{TITLE}}

## Purpose

### Consumers

<!-- Author prompt: Name who uses this data and for what. -->

{{CONSUMERS}}

### Boundaries

<!-- Author prompt: State what this data is not authority for. -->

{{NON_AUTHORITY_BOUNDARIES}}

## Provenance

### Collection

<!-- Author prompt: Name the inputs and the generator or method that produced the data. -->

{{INPUTS_AND_GENERATOR}}

### Versions and Dates

<!-- Author prompt: Give the input versions and the observation and generation dates. -->

{{INPUT_VERSIONS_AND_DATES}}

## Interpretation

### Schema and Units

<!-- Author prompt: List each field in the table: Field its name, Type its value type, Unit its unit or "none", Meaning what it means, and Limits its precision, missing values or cost. -->

| Field | Type | Unit | Meaning | Limits |
| --- | --- | --- | --- | --- |
| {{FIELD}} | {{TYPE}} | {{UNIT}} | {{MEANING}} | {{LIMITS}} |

### Limits

<!-- Author prompt: State the range, constraints, refresh trigger and known errors of the data. -->

{{DATA_LIMITS}}
