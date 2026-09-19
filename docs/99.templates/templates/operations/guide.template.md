---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/guide"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "operations"
artifact_id: "{{ARTIFACT_ID}}"
parent_ids: []
created: "{{CREATED}}"
---

<!-- Author prompt: Service Guides add optional `implementation_services` frontmatter as a mapping from each repo-relative active Compose path to its nonempty list of owned service names; workspace and process Guides omit it. -->

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->

# {{TITLE}}

## Usage

<!-- Author prompt: For a service subject, cover only applicable fields; omit nonapplicable fields without filler. Identify the actual implementation and Compose ownership, service profiles and HOME/DEV/OPTIONAL/LAB classification, network and exposure, data and persistence, dependencies, environment and secret names (never values), resources, security and authentication, normal use, backup prerequisites and recovery, upgrade and migration, observable readiness, and official sources. For a non-service workspace subject, keep only the fields its implementation actually has. Route executable maintenance and recovery to the Runbook; do not duplicate its commands. -->

<!-- Author prompt: Compose/Dockerfile declarations own runtime image tags and dependency pins; the machine-readable registry is a derived projection. Link the implementation authority; do not copy exact patch versions into narrative inventories. A necessary compatibility, advisory, workaround, migration or history literal requires a same-line comment `runtime-version-exception: migration — explain the concrete migration boundary` with the applicable category and a concrete reason. Document frontmatter versions are independent. -->

<!-- Author prompt: State the reader goal and primary tutorial, how-to, reference or explanation need. -->

{{USAGE}}

## Common Checks

{{COMMON_CHECKS}}

## Runbook Handoff

<!-- Author prompt: Keep this optional section only when an actual runbook owns executable steps; link it without copying commands. -->

{{RUNBOOK_HANDOFF}}

## Traceability

{{SUBJECT_AND_AUTHORITY_LINKS}}

## Related Documents

{{RELATED_DOCUMENTS}}
