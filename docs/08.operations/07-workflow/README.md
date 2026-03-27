# Workflow & Orchestration Operations

> Airflow, n8n, Airbyte 운영 정책 및 통제 기준.

## Overview

이 디렉터리는 `07-workflow` 계층의 운영 정책 문서를 모은다. 각 문서는 허용/금지 행위, 변경 승인 절차, 예외 처리, 준수 검증 기준을 정의한다.

## Audience

이 README의 주요 독자:

- SRE / Platform Operators
- Security & Compliance Owners
- Change Approvers
- AI Agents under policy constraints

## Scope

### In Scope

- 워크플로 엔진 운영 정책(Airflow, n8n, Airbyte)
- 배포 승격/변경 승인 통제
- 보안/자격 증명/로그 보존 정책

### Out of Scope

- 서비스 사용 가이드 (07.guides 담당)
- 장애 조치 절차 (09.runbooks 담당)

## Structure

```text
07-workflow/
├── 01.dag-deployment.md # DAG 배포/승인 정책
├── airflow.md           # Airflow 운영 정책
├── n8n.md               # n8n 운영 정책
├── airbyte.md           # Airbyte 운영 정책
└── README.md            # This file
```

## How to Work in This Area

1. 새 정책 문서는 `../../99.templates/operation.template.md`를 사용한다.
2. `Controls`와 `AI Agent Policy Section`은 필수로 채운다.
3. 정책 변경 시 대응 Runbook과 Plan/Task 링크를 함께 갱신한다.

## Related References

- **PRD**: [2026-03-26-07-workflow.md](../../01.prd/2026-03-26-07-workflow.md)
- **ARD**: [0007-workflow-architecture.md](../../02.ard/0007-workflow-architecture.md)
- **Spec**: [07-workflow/spec.md](../../04.specs/07-workflow/spec.md)
- **Guides**: [07-workflow Guides](../../07.guides/07-workflow/README.md)
- **Runbooks**: [07-workflow Runbooks](../../09.runbooks/07-workflow/README.md)
