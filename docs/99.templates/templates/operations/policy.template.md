---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/policy"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "operations"
artifact_id: "{{ARTIFACT_ID}}"
created: "{{CREATED}}"
next_review_at: "{{NEXT_REVIEW_AT}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in Korean; keep headings, paths, identifiers, and commands unchanged. -->

# {{TITLE}}

## Purpose

### Objective

{{POLICY_OBJECTIVE}}

### Authority

<!-- Author prompt: Link the implementation, requirement and decision that give this policy its authority. -->

{{SUBJECT_AND_AUTHORITY_LINKS}}

## Scope

### Applies To

{{SERVICES_SURFACES_AND_ACTORS_COVERED}}

### Exclusions

{{WHAT_THIS_POLICY_DOES_NOT_COVER}}

## Rules

### Requirements

<!-- Author prompt: For a service subject, cover only applicable fields; omit nonapplicable fields without filler. Specify activation, network exposure and trust boundaries, authentication and authorization, secret handling, least privilege, data retention, backup and restore expectations, resource limits, update ownership, upgrade and migration, and removal or decommission criteria. For a non-service workspace subject, keep only controls its implementation actually has. Distinguish an enforced control from pending runtime evidence; give exceptions an owner, risk and exit condition. -->

<!-- Author prompt: Compose/Dockerfile declarations own runtime image tags and dependency pins; the machine-readable registry is a derived projection. Link the implementation authority; do not copy exact patch versions into narrative inventories. A necessary compatibility, advisory, workaround, migration or history literal requires a same-line comment `runtime-version-exception: migration — explain the concrete migration boundary` with the applicable category and a concrete reason. Document frontmatter versions are independent. -->

{{CONTROLS}}

### Enforcement

<!-- Author prompt: Name the check, gate or review that enforces each control, and distinguish an enforced control from pending runtime evidence. -->

{{ENFORCEMENT_AND_VERIFICATION}}

## Exceptions

### Exception Conditions

<!-- Author prompt: Give each exception an owner, a risk and an exit condition; write "none" when there is none. -->

{{EXCEPTIONS}}

### Approval and Review

{{APPROVAL_AND_REVIEW_CADENCE}}

## Ownership

### Responsibilities

{{OWNERS_AND_RESPONSIBILITIES}}

### Change and Adoption

{{HOW_THIS_POLICY_CHANGES_AND_RELATED_DOCUMENTS}}
