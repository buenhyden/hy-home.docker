# Workflow & Orchestration Runbooks

> Airflow, n8n, Airbyte 장애 대응 및 복구 실행 절차.

## Overview

이 디렉터리는 `07-workflow` 계층의 실행형 런북 모음이다. 운영자는 장애 발생 시 본문 절차를 순서대로 실행하고, 검증/증적/롤백 단계를 반드시 수행해야 한다.

## Audience

이 README의 주요 독자:

- On-call SRE
- Platform Operators
- Incident Commander
- AI Agents with human approval

## Scope

### In Scope

- Airflow 서비스 복구
- Airflow Worker 장애 심화 대응
- n8n 서비스 복구
- Airbyte 동기화/워커 장애 복구

### Out of Scope

- 정책 정의 및 승인 규칙 (08.operations 담당)
- 사용 가이드/온보딩 (07.guides 담당)

## Structure

```text
07-workflow/
├── airflow.md                 # Airflow 서비스 복구 런북
├── airflow-worker-recovery.md # Airflow Worker 장애 심화 대응
├── n8n.md                     # n8n 서비스 복구 런북
├── airbyte.md                 # Airbyte 동기화/워커 복구 런북
└── README.md                  # This file
```

## How to Work in This Area

1. 새 런북은 `../../99.templates/runbook.template.md`를 사용한다.
2. `When to Use`, `Procedure`, `Verification`, `Safe Rollback`을 항상 채운다.
3. 복구 종료 후 Incident/Postmortem 링크를 남긴다.

## Related References

- **PRD**: [2026-03-26-07-workflow.md](../../01.prd/2026-03-26-07-workflow.md)
- **ARD**: [0007-workflow-architecture.md](../../02.ard/0007-workflow-architecture.md)
- **Spec**: [07-workflow/spec.md](../../04.specs/07-workflow/spec.md)
- **Guides**: [07-workflow Guides](../../07.guides/07-workflow/README.md)
- **Operations**: [07-workflow Operations](../../08.operations/07-workflow/README.md)
- **Incidents**: [Incidents README](../../10.incidents/README.md)
