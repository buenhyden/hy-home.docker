# Workflow & Orchestration Guides

> Airflow, n8n, Airbyte 사용/이해 중심 문서 인덱스.

## Overview

이 디렉터리는 `07-workflow` 계층의 사용자 가이드를 제공한다. 목적은 시스템 이해, 온보딩, 실무 사용 흐름 정리이며 정책 정의나 장애 복구 절차는 포함하지 않는다.

## Audience

이 README의 주요 독자:

- Developers
- Data Engineers
- Operators
- AI Agents

## Scope

### In Scope

- Airflow 시스템 이해 및 DAG 개발 가이드
- n8n 자동화 설계/운영 가이드
- Airbyte 도입 및 동기화 운영 준비 가이드

### Out of Scope

- 운영 정책/통제 기준 (08.operations 담당)
- 장애 대응/복구 절차 (09.runbooks 담당)

## Structure

```text
07-workflow/
├── 01.airflow-dag-dev.md    # Airflow DAG 개발 가이드
├── 02.n8n-automation.md     # n8n 자동화 가이드
├── airflow-dag-basics.md    # Airflow DAG 기초
├── airflow.md               # Airflow 시스템 가이드
├── n8n.md                   # n8n 시스템 가이드
├── airbyte.md               # Airbyte 운영 준비 가이드
└── README.md                # This file
```

## How to Work in This Area

1. 새 가이드는 `../../99.templates/guide.template.md`를 사용한다.
2. 문서에는 `Overview (KR)`, `Prerequisites`, `Step-by-step Instructions`, `Common Pitfalls`를 포함한다.
3. 각 가이드에서 대응되는 Operation/Runbook 링크를 함께 유지한다.

## Related References

- **PRD**: [2026-03-26-07-workflow.md](../../01.prd/2026-03-26-07-workflow.md)
- **ARD**: [0007-workflow-architecture.md](../../02.ard/0007-workflow-architecture.md)
- **ADR**: [0007-airflow-n8n-hybrid-workflow.md](../../03.adr/0007-airflow-n8n-hybrid-workflow.md)
- **Spec**: [07-workflow/spec.md](../../04.specs/07-workflow/spec.md)
- **Operations**: [07-workflow Operations](../../08.operations/07-workflow/README.md)
- **Runbooks**: [07-workflow Runbooks](../../09.runbooks/07-workflow/README.md)
