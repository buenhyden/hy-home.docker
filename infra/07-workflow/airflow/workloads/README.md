---
title: "Airflow Workloads"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
---

# Airflow Workloads

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Service

##### Purpose

###### Overview
<!-- core-payload-level:4 -->

기존 Airflow에서 선택하는 개별 배치의 canonical source를 둡니다.
폴더 존재는 HOME 배포나 실행 승인을 뜻하지 않습니다.

###### Scope
<!-- core-payload-level:4 -->

현재 독립 매니페스트 검증·게시 배치를 소유합니다. Airflow 이미지·관리 DB와
공통 네트워크는 기존 소유자를 따릅니다. Wiki와 학습 앱을 구현하지 않습니다.

###### Structure
<!-- core-payload-level:4 -->

- [manifest-pipeline/](manifest-pipeline/README.md): DEV 매니페스트 배치.

##### Interfaces

###### Inputs and Outputs
<!-- core-payload-level:4 -->

없음: 이 디렉터리 자체는 포트나 API를 노출하지 않으며, 입출력 계약은 `manifest-pipeline/README.md`가 기술한다.

###### Security Boundary
<!-- core-payload-level:4 -->

없음: 이 디렉터리 자체에는 secret 정의가 없으며, worker 전용 `OPSFLOW_SECRET_DIR` 경계는 `manifest-pipeline/README.md`의 Security Boundary가 기술한다.

#### Usage

##### Prerequisites

없음: 이 디렉터리는 Compose나 Dockerfile 없이 소스만 두며, 실행은 `infra/07-workflow/airflow/docker-compose.yml`의 Airflow 서비스가 `manifest-pipeline/`의 DAG와 `workflow_lib`를 읽기 전용으로 mount해 수행한다.

##### Selected Start

###### Usage
<!-- core-payload-level:4 -->

선택 workload의 README와 현재 Task를 읽고 합성시험부터 수행합니다.
실제 대상·권한·복구 경계가 확정되기 전에는 서비스를 시작하지 않습니다.

#### Checks

##### Readiness

없음: 이 디렉터리 자체의 검사는 없으며, 소스 검증은 `manifest-pipeline/README.md`의 Selected Start를 따른다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

이 서비스의 런북은 다음과 같다.

- RUN-0050: `docs/05.operations/03.runbooks/08.workflows-and-automation/0050-airflow.md`

###### Related Documents
<!-- core-payload-level:4 -->

- [Airflow](../README.md)
- [문서 탐색](../../../../docs/README.md)

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 이 디렉터리는 헬스체크나 관측 대상을 선언하지 않으며, 상태와 복구는 Airflow 서비스와 RUN-0050이 소유한다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
