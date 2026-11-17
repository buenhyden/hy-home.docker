---
title: "Output Style"
version: "1.3.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
---

# Output Style

## Purpose and Scope

### Objective

Supported agents communicate outcomes first, use plain language, cite concrete
repository evidence, and distinguish verified facts from assumptions. Long-work
updates are concise. Final reports include changed scope, validation, residual
risks, and blockers without copying sensitive output.

#### Authority

This policy is the canonical owner of agent outcome, findings, procedure, and completion-report style under [bootstrap precedence](bootstrap.md#authority-and-precedence).

### Applies To

Conversational outcomes, findings, procedures, and completion reports from supported agents.

#### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| OUTPUT-STYLE-R1 | Conversational responses | Required: follow the user's active language; artifact language is routed through the documentation protocol and no provider surface may set either rule | none | none |
| OUTPUT-STYLE-R2 | Reporting a finding or review issue | Required: state claim plus evidence cited by repository path and line, one severity from `blocker`/`high`/`medium`/`low`, explicit assumptions and tradeoffs; `BLOCK`/`WARN` are not severities | manual | none |
| OUTPUT-STYLE-R3 | Writing an instruction or procedure | Required: active voice, one action and one expected result per step, runnable commands, non-executable snippets marked explicitly | manual | none |

#### Language

Conversational responses follow the user's active language. Artifact language is
not a presentation choice: it is routed by document role through
[documentation protocol](documentation-protocol.md#document-language). A provider
surface may not set either rule.

#### Findings

State a finding as a claim plus its evidence, not as narrative. Cite evidence by
repository path and line so a reader can verify it directly. Tag a review issue
with one severity: `blocker`, `high`, `medium`, or `low`. State an assumption
explicitly and surface a tradeoff rather than resolving it silently.

`BLOCK` and `WARN` are hook and gate action names (enforcement outcomes), distinct
from the finding severity vocabulary `blocker`, `high`, `medium`, and `low`.

#### Procedures

Write an instruction in the active voice with one action per step and one
expected result. Keep a command runnable as written; mark a non-executable
snippet explicitly.

### Exceptions

#### Exception Conditions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

#### Approval and Review

None: no exception exists to approve.

## Enforcement

### Mechanisms

#### Completion Reporting

Report outcomes faithfully. Show failing output rather than summarizing it, name
a skipped step, and state completion only after the check that proves it has
run. Completion obligations themselves belong to
[task checklists](task-checklists.md); this policy owns only how the result is
reported.

Name `FAIL`, `BLOCKED`, `SKIPPED`, `NOT_RUN`, missing or revoked approval, and
partial results explicitly. Label static, configured, native, hosted, and
operational evidence by the observation actually made; one does not prove
another.

Provider-native presentation may adapt rendering but may not change governance
authority, language routing, or acceptance criteria.

### Limits

No check is named for these style rules; they rest on review and agent adherence.

- Language routing, finding format, severity tags and procedure style name no script or gate.
- Faithful completion reporting rests on review; completion obligations themselves belong to the task checklists.
- Provider-native presentation limits depend on provider rendering behavior.

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- [Provider capability matrix](provider-capability-matrix.md)
- [Documentation protocol](documentation-protocol.md)
- [Task checklists](task-checklists.md)
- [AI agent standards](standards.md)
