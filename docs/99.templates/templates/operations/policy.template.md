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

## Purpose and Scope

### Objective

<!-- Author prompt: State the objective and link the implementation, requirement and decision that give this policy its authority. -->

{{POLICY_OBJECTIVE_AND_AUTHORITY_LINKS}}

### Applies To

<!-- Author prompt: Name the services, surfaces and actors covered and what this policy does not cover. -->

{{SERVICES_SURFACES_ACTORS_AND_EXCLUSIONS}}

## Rules

### Requirements

<!-- Author prompt: For a service subject, cover only applicable fields; omit nonapplicable fields without filler. Specify activation, network exposure and trust boundaries, authentication and authorization, secret handling, least privilege, data retention, backup and restore expectations, resource limits, update ownership, upgrade and migration, and removal or decommission criteria. For a non-service workspace subject, keep only controls its implementation actually has. Distinguish an enforced control from pending runtime evidence; give exceptions an owner, risk and exit condition. -->

<!-- Author prompt: Compose/Dockerfile declarations own runtime image tags and dependency pins; the machine-readable registry is a derived projection. Link the implementation authority; do not copy exact patch versions into narrative inventories. A necessary compatibility, advisory, workaround, migration or history literal requires a same-line comment `runtime-version-exception: migration — explain the concrete migration boundary` with the applicable category and a concrete reason. Document frontmatter versions are independent. -->

<!-- Author prompt: List each rule in the table: Rule ID is a stable identifier within this policy, Condition when it applies, Requirement starting with "Required:", "Forbidden:" (the forbidden act, never a negated sentence) or "Allowed:", Enforcement a check only where the policy ties it to that rule, "manual" only where the policy says the rule rests on review, otherwise "none", and Evidence a record only where the policy says it confirms that rule, otherwise "none". One row per rule statement under Requirements and its subsections. Detail follows the table. -->

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| {{RULE_ID}} | {{CONDITION}} | {{REQUIREMENT}} | {{ENFORCEMENT}} | {{EVIDENCE}} |

{{CONTROLS}}

### Exceptions

<!-- Author prompt: Give each exception an owner, a risk, an exit condition and its approval and review; write "none" when there is none. -->

{{EXCEPTIONS_APPROVAL_AND_REVIEW}}

## Enforcement

### Mechanisms

<!-- Author prompt: Name the check, gate or review that enforces each control, and distinguish an enforced control from pending runtime evidence. -->

{{ENFORCEMENT_AND_VERIFICATION}}

### Limits

<!-- Author prompt: Name what is not mechanically enforced: rules that rest on manual review, pending runtime evidence, or no check at all. -->

{{UNENFORCED_PARTS}}

## Ownership

### Owner

{{OWNERS_AND_RESPONSIBILITIES}}

### Review Triggers

{{WHEN_AND_HOW_THIS_POLICY_CHANGES_AND_RELATED_DOCUMENTS}}
