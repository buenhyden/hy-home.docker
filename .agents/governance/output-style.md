---
title: "Output Style"
version: "2.0.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: Output Style
  layer: agent
updated: "2026-11-20"
---

# Output Style

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the policy payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose and Scope

##### Objective

Supported agents communicate outcomes first, use plain language, cite concrete
repository evidence, and distinguish verified facts from assumptions. Long-work
updates are concise. Final reports include changed scope, validation, residual
risks, and blockers without copying sensitive output.

###### Authority
<!-- core-payload-level:4 -->

This policy is the canonical owner of agent outcome, findings, procedure, and completion-report style under [bootstrap precedence](bootstrap.md#authority-and-precedence).

##### Applies To

Conversational outcomes, findings, procedures, and completion reports from supported agents.

###### Exclusions
<!-- core-payload-level:4 -->

None: this document states no exclusion.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| OUTPUT-STYLE-R1 | Conversational responses | Required: follow the user's active language | none | none |
| OUTPUT-STYLE-R2 | Artifact language | Required: route it by document role through the documentation protocol, not as a presentation choice | none | none |
| OUTPUT-STYLE-R3 | Always | Forbidden: a provider surface setting either language rule | none | none |
| OUTPUT-STYLE-R4 | Stating a finding | Required: state it as a claim plus its evidence, not as narrative | none | none |
| OUTPUT-STYLE-R5 | Citing evidence | Required: cite it by repository path and line | none | none |
| OUTPUT-STYLE-R6 | Tagging a review issue | Required: use one severity from `blocker`, `high`, `medium` or `low` | none | none |
| OUTPUT-STYLE-R7 | A finding rests on an assumption | Required: state the assumption explicitly | none | none |
| OUTPUT-STYLE-R8 | A finding involves a tradeoff | Forbidden: resolving the tradeoff silently instead of surfacing it | none | none |
| OUTPUT-STYLE-R9 | Writing an instruction | Required: use the active voice with one action per step and one expected result | none | none |
| OUTPUT-STYLE-R10 | Writing a command | Required: keep it runnable as written | none | none |
| OUTPUT-STYLE-R11 | Non-executable snippet | Required: mark it explicitly | none | none |

###### Language
<!-- core-payload-level:4 -->

Conversational responses follow the user's active language. Artifact language is
not a presentation choice: it is routed by document role through
[documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md#document-language). A provider
surface may not set either rule.

###### Findings
<!-- core-payload-level:4 -->

State a finding as a claim plus its evidence, not as narrative. Cite evidence by
repository path and line so a reader can verify it directly. Tag a review issue
with one severity: `blocker`, `high`, `medium`, or `low`. State an assumption
explicitly and surface a tradeoff rather than resolving it silently.

`BLOCK` and `WARN` are hook and gate action names (enforcement outcomes), distinct
from the finding severity vocabulary `blocker`, `high`, `medium`, and `low`.

###### Procedures
<!-- core-payload-level:4 -->

Write an instruction in the active voice with one action per step and one
expected result. Keep a command runnable as written; mark a non-executable
snippet explicitly.

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

No exception is granted here; a separately authorized operation follows [Approval boundaries](../../docs/00.workspace/04.quality/approval-boundaries.md).

###### Approval and Review
<!-- core-payload-level:4 -->

None: no exception exists to approve.

#### Enforcement

##### Mechanisms

###### Completion Reporting
<!-- core-payload-level:4 -->

Report outcomes faithfully. Show failing output rather than summarizing it, name
a skipped step, and state completion only after the check that proves it has
run. Completion obligations themselves belong to
[task checklists](../../docs/00.workspace/04.quality/task-checklists.md); this policy owns only how the result is
reported.

Name `FAIL`, `BLOCKED`, `SKIPPED`, `NOT_RUN`, missing or revoked approval, and
partial results explicitly. Label static, configured, native, hosted, and
operational evidence by the observation actually made; one does not prove
another.

Provider-native presentation may adapt rendering but may not change governance
authority, language routing, or acceptance criteria.

##### Limits

This policy names no check for its style rules, so none of them is mechanically enforced:

- Language routing: R1-R3.
- Finding format, evidence citation and severity: R4-R8.
- Procedure style: R9-R11.
- Rules stated under Enforcement (Completion Reporting) are outside this table.

#### Ownership

##### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](../../docs/00.workspace/04.quality/approval-boundaries.md#authorization-source-and-records)).

##### Review Triggers

Changes land in place with Task evidence; related documents:

- [Provider capability matrix](provider-capability-matrix.md)
- [Documentation protocol](../../docs/00.workspace/03.process/documentation-protocol.md)
- [Task checklists](../../docs/00.workspace/04.quality/task-checklists.md)
- [AI agent standards](standards.md)

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
