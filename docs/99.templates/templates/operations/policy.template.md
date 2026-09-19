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

<!-- Author prompt: Specify exposure and trust boundaries, activation profiles, least privilege, resource budget, data retention, backup/restore expectations and update ownership. Distinguish an enforced control from pending runtime evidence; give exceptions an owner, risk and exit condition. -->

<!-- Author prompt: Compose/Dockerfile declarations own runtime image tags and dependency pins; the curated machine-readable registry is a derived projection. Link the implementation authority; do not copy exact patch versions into narrative inventories. A necessary compatibility, advisory, workaround, migration or history literal requires a same-line comment `runtime-version-exception: migration — explain the concrete migration boundary` with the applicable category and a concrete reason. Document frontmatter versions are independent. -->

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
