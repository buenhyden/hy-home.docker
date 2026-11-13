---
title: "Airflow Workloads"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# Airflow Workloads

## Purpose

### Service Role

#### Overview

기존 Airflow에서 선택하는 개별 배치의 canonical source를 둡니다.
폴더 존재는 HOME 배포나 실행 승인을 뜻하지 않습니다.

#### Scope

현재 독립 매니페스트 검증·게시 배치를 소유합니다. Airflow 이미지·관리 DB와
공통 네트워크는 기존 소유자를 따릅니다. Wiki와 학습 앱을 구현하지 않습니다.

#### Structure

- [manifest-pipeline/](manifest-pipeline/README.md): DEV 매니페스트 배치.

### Supported Environment

없음: 이 디렉터리는 Compose나 Dockerfile 없이 소스만 두며, 실행은 `infra/07-workflow/airflow/docker-compose.yml`의 Airflow 서비스가 `manifest-pipeline/`의 DAG와 `workflow_lib`를 읽기 전용으로 mount해 수행한다.

## Interfaces

### Inputs and Outputs

없음: 이 디렉터리 자체는 포트나 API를 노출하지 않으며, 입출력 계약은 `manifest-pipeline/README.md`가 기술한다.

### Security Boundary

없음: 이 디렉터리 자체에는 secret 정의가 없으며, worker 전용 `OPSFLOW_SECRET_DIR` 경계는 `manifest-pipeline/README.md`의 Security Boundary가 기술한다.

## Development

### Local Workflow

#### Usage

선택 workload의 README와 현재 Task를 읽고 합성시험부터 수행합니다.
실제 대상·권한·복구 경계가 확정되기 전에는 서비스를 시작하지 않습니다.

### Checks

없음: 이 디렉터리 자체의 검사는 없으며, 소스 검증은 `manifest-pipeline/README.md`의 Local Workflow를 따른다.

## Operations

### Runbook Links

이 서비스의 런북은 다음과 같다.

- RUN-0050: `docs/05.operations/runbooks/08-workflows-and-automation/0050-airflow.md`

#### Related Documents

- [Airflow](../README.md)
- [문서 탐색](../../../../docs/README.md)

### Observability and Recovery

없음: 이 디렉터리는 헬스체크나 관측 대상을 선언하지 않으며, 상태와 복구는 Airflow 서비스와 RUN-0050이 소유한다.
