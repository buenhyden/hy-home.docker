# Workflow & Orchestration Operations

> 워크플로 오케스트레이션 시스템의 운영 정책 및 거버넌스.

## Overview

이 디렉터리는 `hy-home.docker` 플랫폼의 워크플로 엔진(Airflow, n8n 등)을 안정적으로 운영하기 위한 정책과 통제 기준을 담고 있습니다. 시스템 레이어의 리소스 관리, 보안 가이드라인, 변경 관리 절차를 규정합니다.

## Audience

이 README의 주요 독자:

- **SREs / Operators**: 클러스터 유지보수 및 자원 최적화 담당자
- **Security Officers**: 시스템 접근 제어 및 비밀번호 관리 감독자
- **AI Agents**: 변경 이력 추적 및 정책 준수 여부 자동 분석

## Scope

### In Scope

- **Policy Definition**: Airflow/n8n 서비스의 가용성 및 성능 목표 설정
- **Change Control**: DAG 및 워크플로 배포 절차 승인 규칙
- **Security Compliance**: 인증, 인가 및 Secret 관리 표준

### Out of Scope

- 개별 파이프라인 개발 방법론 (07.guides 담당)
- 장애 발생 시 단계별 복구 절차 (09.runbooks 담당)

## Structure

```text
07-workflow/
├── 01.dag-deployment.md  # DAG 배포 및 스테이징 정책
├── airflow.md               # Airflow 운영 정책 (운영 정책)
├── n8n.md                   # n8n 운영 정책 (운영 정책)
└── 01.dag-deployment.md     # Airflow DAG 배포 및 승인 절차
```

## How to Work in This Area

1. [v2026.03 표준 템플릿](../../99.templates/operation.template.md)을 준수하여 작성합니다.
2. 모든 정책 문서는 **Overview (KR)** 섹션을 필수로 포함해야 합니다.
3. 정책 변경 시 반드시 관련 [ARD](../../02.ard/README.md) 또는 [ADR](../../03.adr/README.md)과 연결합니다.

## Related References

- **ARD**: [Workflow Infrastructure ARD](../../02.ard/07-workflow.md)
- **Runbook**: [Workflow Recovery Runbooks](../../09.runbooks/07-workflow/README.md)
