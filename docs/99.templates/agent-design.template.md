---
status: draft
---
<!-- Target: docs/03.specs/<feature-id>/agent-design.md -->

# [Feature Name] Agent Design

> Use this template for `docs/03.specs/<feature-id>/agent-design.md`.
>
> Rules:
>
> - This document is a child design document under the feature spec.
> - Keep product intent in PRD and system-wide constraints in ARD.
> - Keep implementation tasks in `04.execution/tasks/`.
> - This document focuses on AI Agent behavior, orchestration, safety, and evaluation.
> - Target-relative links in `## Related Documents` are calculated from the copied target path, not from `docs/99.templates/`.

---

## Overview (KR)

이 문서는 [기능명]의 AI Agent 설계를 정의한다. Agent 역할, 입력/출력 계약, 도구 사용, 컨텍스트 관리, 안전 장치, 평가 전략을 구체화한다.

## Parent Documents

- **Spec**: `[./spec.md]`
- **PRD**: `[../../01.requirements/YYYY-MM-DD-feature.md]`
- **ARD**: `[../../02.architecture/requirements/0001-system.md]`
- **Related ADRs**: `[../../02.architecture/decisions/0001-example.md]`

## Scope & Non-goals

- **Covers**:
- **Does Not Cover**:

## Agent Role

- **Primary Role**:
- **Primary User / Caller**:
- **Success Definition**:

## Inputs / Outputs

- **Inputs**:
- **Outputs**:
- **Expected Structured Format**:

## Orchestration Model

- `single-agent | planner-worker | router-specialist | handoff`
- **Why this model**:
- **Escalation / Handoff rules**:

## Tools & Permissions

| Tool | Purpose | Allowed Actions | Forbidden Actions | Failure Handling |
| --- | --- | --- | --- | --- |
| [Tool] | [Purpose] | [Allowed] | [Forbidden] | [Fallback] |

## Prompt / Policy Contract

- **System Instruction Summary**:
- **Policy Constraints**:
- **Versioning Rule**:

## Context & Memory Strategy

- **Session Context**:
- **Retrieval Strategy**:
- **Persistent Memory Rule**:
- **Privacy / Retention Notes**:

## Guardrails

- **Input Guardrails**:
- **Output Guardrails**:
- **Blocked Conditions**:
- **Human Escalation Rule**:

## Failure Modes & Fallback

- **Failure Mode 1**:
- **Fallback 1**:
- **Failure Mode 2**:
- **Fallback 2**:

## Evaluation Plan

- **Offline Evals**:
- **Online Signals**:
- **Acceptance Thresholds**:
- **Linked Task / Eval Docs**: `[../../04.execution/tasks/YYYY-MM-DD-feature.md]`

## Observability

- **Trace fields**:
- **Logs / Events**:
- **Redaction / Privacy Rules**:

## Related Documents

- **Tests**: `[./tests.md]`
- **Policy, direct operations target**: `[../../05.operations/policies/<policy>.md]`
- **Policy, domain operations target**: `[../../05.operations/policies/<domain>/<policy>.md]`
- **Runbook, direct operations target**: `[../../05.operations/runbooks/<topic>.md]`
- **Runbook, domain operations target**: `[../../05.operations/runbooks/<domain>/<topic>.md]`
