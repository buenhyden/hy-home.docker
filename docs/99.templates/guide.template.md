---
status: draft
---

<!-- Target: docs/05.operations/guides/<tier>/<topic>.md -->

# {Service} Usage Guide

> Use this template for `docs/05.operations/guides/<tier>/<topic>.md`.
>
> Rules:
>
> - This document explains how to use, configure, or understand a service.
> - This document is not an operations policy and must not contain `## Policy Scope`, `## Controls`, or `## Review Cadence`.
> - This document is not a step-by-step recovery procedure. If the primary purpose is rollback, recovery, or ordered remediation, write a Runbook instead.
> - Target-relative links are calculated from the copied target path, not from `docs/99.templates/`.

---

## Usage

### Overview (KR)

{이 문서가 다루는 서비스/컴포넌트와 이 가이드를 언제 참조해야 하는지 설명한다.}

### Usage Type

`how-to | onboarding | system-guide | troubleshooting-guide | operational-reference`

### Target Audience

- Operator
- Developer
- Contributor
- AI Agent

### Purpose

{이 가이드가 독자에게 가능하게 하는 작업 또는 이해.}

### Prerequisites

- {Prerequisites 1}
- {Prerequisites 2}

### Step-by-step Instructions

1. {Step 1}
2. {Step 2}
3. {Step 3}

### Common Pitfalls

- {Pitfall 1: 현상과 회피 방법}
- {Pitfall 2}

## Common Checks

- `{verification command}`
- {expected result}

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은
[recovery runbook]({relative-path-to-runbook})을 따른다.

N/A — no corresponding runbook.

## Related Documents

Use only links that apply to the copied target path. Delete unused examples before committing.

Domain-depth examples (two levels deep):

- [Operations index](../../README.md)
- [Operations policy](../../policies/<tier>/<topic>.md)
- [Recovery runbook](../../runbooks/<tier>/<topic>.md)

Nested-depth examples (three levels deep):

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/<tier>/<subdomain>/<topic>.md)
- [Recovery runbook](../../../runbooks/<tier>/<subdomain>/<topic>.md)
