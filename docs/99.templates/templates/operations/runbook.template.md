---
status: draft
---

<!-- Target: docs/05.operations/runbooks/<tier>/<topic>.md -->

# {Service} {Operation} Runbook

> Use this template for `docs/05.operations/runbooks/<tier>/<topic>.md`.
>
> Rules:
>
> - This document exists for immediate execution — ordered steps, evidence capture, rollback, and escalation.
> - Write the human-facing procedure in Korean. Preserve commands, paths,
>   service names, Docker profiles, environment variables, secret IDs, expected
>   evidence labels, and quoted upstream terms exactly.
> - This document is not a policy definition and must not contain `## Policy Scope`, `## Controls`, or `## Review Cadence`.
> - This document is not a tutorial-first guide. Usage context belongs in the paired Guide.
> - If the primary purpose is post-incident analysis, write a Postmortem instead.
> - Rollback or Recovery must be factual-only. If no verified steps exist, write `N/A — no verified rollback procedure` and route to `## Escalation`.
> - Target-relative links are calculated from the copied target path, not from `docs/99.templates/`.

---

## {Service} {Operation} Procedure

> Scope: {one-line scope statement}

### Overview

{이 런북이 다루는 범위와 언제 사용해야 하는지 설명한다.}

### Purpose

{이 런북이 해결하는 운영 문제.}

### Canonical References

- **Spec**: N/A — no upstream source
- **Policy**: N/A — no upstream source
- **Guide**: N/A — no upstream source

## When to Use

{트리거 조건, 증상, 또는 실행 기준.}

## Procedure

### Checklist

- [ ] {Pre-condition check 1}
- [ ] {Pre-condition check 2}

### Steps

1. {Step 1}
2. {Step 2}
3. {Step 3}

### Verification Steps

- `{verification command}`
- {expected result}

### Observability and Evidence Sources

- **Logs**: {log location or command}
- **Metrics**: {metric name or dashboard link}

### Safe Rollback or Recovery Procedure

1. {Rollback step 1}
2. {Rollback step 2}

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: N/A

## Evidence

- {캡처할 로그, 명령 출력, 대시보드 스크린샷}

## Rollback or Recovery

{검증된 안전한 롤백/복구 절차. 검증된 절차가 없으면 `N/A — no verified rollback or recovery procedure is documented yet`을 기록하고 `## Escalation`으로 독자를 안내한다.}

## Escalation

{에스컬레이션 담당자, 기준, 제공해야 할 컨텍스트.}

## Related Documents

Use only links that apply to the copied target path. Delete unused examples before committing.

Domain-depth examples (two levels deep):

- [Operations index](../../README.md)
- [Usage guide](../../guides/<tier>/<topic>.md)
- [Operations policy](../../policies/<tier>/<topic>.md)

Nested-depth examples (three levels deep):

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/<tier>/<subdomain>/<topic>.md)
- [Operations policy](../../../policies/<tier>/<subdomain>/<topic>.md)
