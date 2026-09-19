---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/runbook"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "operations"
artifact_id: "{{ARTIFACT_ID}}"
parent_ids: []
created: "{{CREATED}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->

# {{TITLE}}

## When to Use

{{WHEN_TO_USE}}

## Procedure

<!-- Author prompt: For a service subject, cover only applicable fields; omit nonapplicable fields without filler. State exact targets, preconditions, approval and safety boundaries, static checks, symptom-led diagnosis and logs, authorized start, stop, and restart actions, backup and restore, upgrade and migration, ordered commands, expected results, stop conditions, verification, rollback or recovery, escalation, and evidence handoff. Use only commands proven executable in the current image or host implementation. For a non-service workspace subject, keep only actions its implementation actually supports. Separate read-only checks from runtime mutations; never print secrets or full rendered private configuration. Preserve data during rollback; backup restoration requires an isolated rehearsal before claiming recovery. -->

<!-- Author prompt: Compose/Dockerfile declarations own runtime image tags and dependency pins; the machine-readable registry is a derived projection. Link the implementation authority; do not copy exact patch versions into narrative inventories. A necessary compatibility, advisory, workaround, migration or history literal requires a same-line comment `runtime-version-exception: migration — explain the concrete migration boundary` with the applicable category and a concrete reason. Document frontmatter versions are independent. -->

{{PROCEDURE}}

## Evidence

{{EVIDENCE}}

## Rollback or Recovery

{{ROLLBACK_OR_RECOVERY}}

## Escalation

{{ESCALATION}}

## Traceability

{{SUBJECT_AND_AUTHORITY_LINKS}}

## Related Documents

{{RELATED_DOCUMENTS}}
