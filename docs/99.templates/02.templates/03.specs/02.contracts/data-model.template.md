---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/data-model"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "specs"
parent_ids:
- "{{PARENT_ID}}"
created: "{{CREATED}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in English; keep headings, paths, identifiers, and commands unchanged. -->

# {{TITLE}}

## Purpose

{{DATA_MODEL_PURPOSE}}

## Entities

{{ENTITY_DEFINITIONS}}

## Attributes

### Types

{{ATTRIBUTE_TYPES}}

### Nullability and Defaults

{{NULLABILITY_AND_DEFAULTS}}

## Relationships

### Cardinality

{{CARDINALITY}}

### Ownership

{{OWNERSHIP}}

## Constraints

### Keys and Uniqueness

{{KEYS_AND_UNIQUENESS}}

### Referential Rules

{{REFERENTIAL_RULES}}

## Lifecycle

### Creation and Mutation

{{CREATION_AND_MUTATION_RULES}}

### Retention

{{RETENTION_RULES}}

## Traceability

{{SPEC_AND_INTERFACE_CONTRACT_LINKS}}
