# Workflow & Orchestration Runbooks

> 장애 복구 및 반복 운영 작업을 위한 단계별 실행 지침(Step-by-step).

## Overview

이 디렉터리는 `hy-home.docker` 워크플로 엔진(Airflow, n8n 등)의 장애 상황 대응과 정기적인 관리 작업을 위한 런북을 포함합니다. 운영자가 긴급 상황에서 고민 없이 즉시 실행할 수 있는 실질적인 절차를 제공합니다.

## Audience

이 README의 주요 독자:

- **Site Reliability Engineers (SREs)**: 시스템 복구 및 긴급 장애 대응 담당자
- **Maintenance Teams**: 정기 점검 및 사용자 관리 수행자
- **AI Agents**: 장애 자동 탐지 및 복구 시나리오 실행 에이전트

## Scope

### In Scope

- **Incident Recovery**: 핵심 서비스(WebUI, Scheduler, Workers) 복구 절차
- **Administrative Tasks**: 계정 관리, 비밀번호 초기화, 권한 설정
- **Maintenance**: DB 영구 볼륨 정리 및 마이그레이션 작업

### Out of Scope

- 파이프라인 개발 가이드 (07.guides 담당)
- 시스템 아키텍처 및 설계 원칙 (02.ard 담당)

## Structure

```text
09.runbooks/07-workflow/
├── airflow.md               # Airflow 서비스 복구 및 관리 런북 (런북)
├── n8n.md                   # n8n 서비스 복구 및 관리 런북 (런북)
├── airflow-worker-recovery.md # Airflow 워커 리소스 복구 심화
└── README.md                # 이 파일
```

## How to Work in This Area

1. [v2026.03 표준 템플릿](../../99.templates/runbook.template.md)에 따라 절차를 단계별로 작성합니다.
2. 모든 명령어는 복사하여 즉시 실행 가능한 형태여야 합니다.
3. 복구 후 반드시 **Verification Steps**를 통해 정상화 여부를 확인하도록 구성합니다.

## Related References

- **Operations**: [Workflow Operations](../../08.operations/07-workflow/README.md)
- **Incidents**: [Incident Records](../../10.incidents/README.md)
- **Architecture**: [Workflow Architecture ARD](../../02.ard/07-workflow.md)
