---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/runbook"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "operations"
artifact_id: "{{ARTIFACT_ID}}"
created: "{{CREATED}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in Korean; keep headings, paths, identifiers, and commands unchanged. -->

# {{TITLE}}

## Purpose

### Trigger and Outcome

{{WHEN_TO_USE_AND_EXPECTED_OUTCOME}}

### Scope

<!-- Author prompt: Name the exact targets, environments and services this runbook covers, what it leaves out, and link the implementation and policy that own them. -->

{{TARGETS_BOUNDARIES_AND_AUTHORITY_LINKS}}

## Preconditions

### Authority and Access

<!-- Author prompt: Name the approval this runbook needs, who may run it, and the access and secret names (never values) required. -->

{{APPROVAL_OPERATOR_ACCESS_AND_SECRET_NAMES}}

### Safety Checks

{{BACKUP_STARTING_STATE_AND_READ_ONLY_PREFLIGHT}}

## Steps

### Actions

<!-- Author prompt: For a service subject, cover only applicable fields; omit nonapplicable fields without filler. State exact targets, preconditions, approval and safety boundaries, static checks, symptom-led diagnosis and logs, authorized start, stop, and restart actions, backup and restore, upgrade and migration, ordered commands, expected results, stop conditions, verification, rollback or recovery, escalation, and evidence handoff. Use only commands proven executable in the current image or host implementation. For a non-service workspace subject, keep only actions its implementation actually supports. Separate read-only checks from runtime mutations; never print secrets or full rendered private configuration. Preserve data during rollback; backup restoration requires an isolated rehearsal before claiming recovery. -->

<!-- Author prompt: Compose/Dockerfile declarations own runtime image tags and dependency pins; the machine-readable registry is a derived projection. Link the implementation authority; do not copy exact patch versions into narrative inventories. A necessary compatibility, advisory, workaround, migration or history literal requires a same-line comment `runtime-version-exception: migration — explain the concrete migration boundary` with the applicable category and a concrete reason. Document frontmatter versions are independent. -->

{{ORDERED_ACTIONS_AND_EXPECTED_RESULTS}}

### Stop Conditions

{{CONDITIONS_THAT_STOP_THE_PROCEDURE}}

## Validation

### Service Checks

{{SERVICE_HEALTH_AND_FUNCTIONAL_CHECKS}}

### Evidence

<!-- Author prompt: Say what evidence to record and where; never record secrets or full rendered private configuration. -->

{{EVIDENCE_TO_RECORD_AND_LOCATION}}

## Recovery

### Rollback

<!-- Author prompt: Keep this section only when the procedure changes state that can be rolled back; preserve data, and require an isolated rehearsal before claiming backup recovery. Otherwise delete it. -->

{{ROLLBACK_OR_RECOVERY}}

### Escalation

{{ESCALATION_OWNER_AND_HANDOFF}}
