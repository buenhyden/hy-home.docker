---
title: "{{TITLE}}"
version: "0.1.0"
type: "governance/policy"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in English; keep headings, paths, identifiers, and commands unchanged. -->

# {{TITLE}}

## Purpose and Scope

### Objective

<!-- Author prompt: State the control's purpose and link the bootstrap policy and the owning policy that give it authority. -->

{{CONTROL_PURPOSE_AND_AUTHORITY_LINKS}}

### Applies To

<!-- Author prompt: Name the surfaces and actors under this control and those outside it. -->

{{SURFACES_ACTORS_AND_EXCLUSIONS}}

## Rules

### Requirements

<!-- Author prompt: List each rule in the table: Rule ID is a stable identifier within this policy, Condition when it applies, Requirement starting with "Required:", "Forbidden:" (the forbidden act, never a negated sentence) or "Allowed:", Enforcement a check only where the policy ties it to that rule, "manual" only where the policy says the rule rests on review, otherwise "none", and Evidence a record only where the policy says it confirms that rule, otherwise "none". One row per rule statement under Requirements and its subsections. Detail follows the table. -->

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| {{RULE_ID}} | {{CONDITION}} | {{REQUIREMENT}} | {{ENFORCEMENT}} | {{EVIDENCE}} |

{{REQUIRED_AND_PROHIBITED_BEHAVIOR}}

### Exceptions

<!-- Author prompt: Name the scoped exceptions and the authorization boundary that approves them; write "None" when there is none. -->

{{SCOPED_EXCEPTIONS_AND_AUTHORIZATION}}

## Enforcement

### Mechanisms

<!-- Author prompt: Name the scoped checks, their expected signals, and the limits of what that evidence proves. -->

{{CHECKS_SIGNALS_AND_EVIDENCE_LIMITS}}

### Limits

<!-- Author prompt: Name what is not mechanically enforced: rules that rest on review, provider behavior, or no check at all. -->

{{UNENFORCED_PARTS}}

## Ownership

### Owner

{{OWNER_AND_ENFORCING_ROLES}}

### Review Triggers

{{WHEN_AND_HOW_THIS_POLICY_CHANGES_AND_RELATED_DOCUMENTS}}
