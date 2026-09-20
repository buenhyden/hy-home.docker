---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/policy"
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

## Overview

{{OVERVIEW}}

## Policy Scope

{{POLICY_SCOPE}}

## Controls

<!-- Author prompt: For a service subject, cover only applicable fields; omit nonapplicable fields without filler. Specify activation, network exposure and trust boundaries, authentication and authorization, secret handling, least privilege, data retention, backup and restore expectations, resource limits, update ownership, upgrade and migration, and removal or decommission criteria. For a non-service workspace subject, keep only controls its implementation actually has. Distinguish an enforced control from pending runtime evidence; give exceptions an owner, risk and exit condition. -->

<!-- Author prompt: Compose/Dockerfile declarations own runtime image tags and dependency pins; the machine-readable registry is a derived projection. Link the implementation authority; do not copy exact patch versions into narrative inventories. A necessary compatibility, advisory, workaround, migration or history literal requires a same-line comment `runtime-version-exception: migration — explain the concrete migration boundary` with the applicable category and a concrete reason. Document frontmatter versions are independent. -->

{{CONTROLS}}

## Exceptions

{{EXCEPTIONS}}

## Verification

{{VERIFICATION}}

## Review Cadence

{{REVIEW_CADENCE}}

## Traceability

{{SUBJECT_AND_AUTHORITY_LINKS}}

## Related Documents

{{RELATED_DOCUMENTS}}
