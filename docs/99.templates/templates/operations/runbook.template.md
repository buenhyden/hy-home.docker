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

<!-- Author prompt: State exact service targets, prerequisites, approval boundary, ordered commands, expected results and stop conditions. Separate read-only checks from runtime mutations; never print secrets or full rendered private configuration. Include persistence verification and rollback that preserves data; backup restoration requires an isolated rehearsal before claiming recovery. -->

<!-- Author prompt: Compose/Dockerfile declarations own runtime image tags and dependency pins; the curated machine-readable registry is a derived projection. Link the implementation authority; do not copy exact patch versions into narrative inventories. A necessary compatibility, advisory, workaround, migration or history literal requires a same-line comment `runtime-version-exception: migration — explain the concrete migration boundary` with the applicable category and a concrete reason. Document frontmatter versions are independent. -->

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
