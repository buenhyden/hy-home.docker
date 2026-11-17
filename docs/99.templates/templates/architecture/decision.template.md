---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "architecture"
artifact_id: "{{ARTIFACT_ID}}"
parent_ids:
- "{{PARENT_ID}}"
created: "{{CREATED}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in English; keep headings, paths, identifiers, and commands unchanged. -->
<!-- Author prompt: Record one decision. State facts and the decision's authority only from evidence; never infer approval from the document's status alone. -->

# {{TITLE}}

## Context

### Problem and Drivers

<!-- Author prompt: State the problem and its drivers, and link the requirements, external sources and related architecture this decision rests on. -->

{{PROBLEM_DRIVERS_AND_CONSTRAINTS}}

### Decision Scope

<!-- Author prompt: Name what the decision covers, what it leaves out, and the consumers it affects. -->

{{DECISION_SCOPE_AND_AFFECTED_CONSUMERS}}

## Options

### Considered Options

{{OPTIONS_ACTUALLY_CONSIDERED}}

### Trade-offs

<!-- Author prompt: List every option in this table, the chosen one included: Option names it, Benefit its advantage, Cost and Risk what it costs or risks, and Reason why it was chosen or not. Detail follows the table. -->

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| {{OPTION}} | {{BENEFIT}} | {{COST_AND_RISK}} | {{REASON}} |

{{BENEFITS_RISKS_COSTS_AND_REASONS_NOT_CHOSEN}}

## Decision

### Chosen Option

{{CHOSEN_OPTION_CONDITIONS_AND_NORMATIVE_OWNER}}

### Authority and Effect

<!-- Author prompt: Name who decided, the approval evidence, and when the decision takes effect. Write "not recorded" for a fact the record does not hold. When this decision supersedes, amends or is superseded by another, summarize it here under a Supersession heading; historical links are non-authoritative. -->

{{DECIDER_APPROVAL_EVIDENCE_AND_EFFECTIVE_DATE}}

## Consequences

### Impacts

{{IMPLEMENTATION_OPERATIONS_AND_QUALITY_IMPACTS}}

### Follow-up

<!-- Author prompt: Name the follow-up work, how compliance is verified, and who owns each item. An owner-directed in-place amendment records its date and direction here. -->

{{FOLLOW_UP_VERIFICATION_AND_OWNERS}}
