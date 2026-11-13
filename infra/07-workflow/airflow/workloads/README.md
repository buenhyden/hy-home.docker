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

기존 Airflow에서 선택하는 개별 배치의 canonical source를 둡니다.
폴더 존재는 HOME 배포나 실행 승인을 뜻하지 않습니다.

현재 독립 매니페스트 검증·게시 배치를 소유합니다. Airflow 이미지·관리 DB와
공통 네트워크는 기존 소유자를 따릅니다. Wiki와 학습 앱을 구현하지 않습니다.

#### Structure

- [manifest-pipeline/](manifest-pipeline/README.md): DEV 매니페스트 배치.

### Supported Environment

없음: 이 디렉터리에는 Compose 파일이나 Dockerfile이 없어 독립 런타임 환경을 선언하지 않는다. 포함 항목은 `manifest-pipeline/`이다.

## Interfaces

### Inputs and Outputs

없음: 이 디렉터리는 자체 포트나 네트워크 인터페이스를 선언하지 않으며, 인터페이스는 하위 `manifest-pipeline/`가 각자 선언한다.

### Security Boundary

없음: 이 디렉터리는 Compose 서비스나 secret 참조를 직접 선언하지 않으며, 하위 `manifest-pipeline/`가 각자 선언한다.

## Development

### Local Workflow

선택 workload의 README와 현재 Task를 읽고 합성시험부터 수행합니다.
실제 대상·권한·복구 경계가 확정되기 전에는 서비스를 시작하지 않습니다.

### Checks

없음: 이 디렉터리는 자체 테스트나 검증 스크립트를 두지 않으며, 하위 `manifest-pipeline/`가 각자 둔다.

## Operations

### Runbook Links

#### Related Documents

- [Airflow](../README.md)
- [문서 탐색](../../../../docs/README.md)

### Observability and Recovery

없음: 이 디렉터리는 자체 헬스체크나 관측 대상을 선언하지 않으며, 하위 `manifest-pipeline/`가 각자 선언한다.
