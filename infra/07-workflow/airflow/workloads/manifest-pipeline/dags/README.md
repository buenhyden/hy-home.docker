---
title: "Manifest Pipeline DAG"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
---

# Manifest Pipeline DAG

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

공개 `airflow.sdk`를 사용하는 단일 수동 배치입니다. 등록 중 workload 파일·DB·S3를 읽지 않습니다.

###### Scope
<!-- core-payload-level:4 -->

최대 active run/task 각각 하나, pool 한 slot, timeout과 bounded retry를 선언합니다.
실제 pool 생성·Celery worker 실행은 별도 검증 대상입니다.

###### Structure
<!-- core-payload-level:4 -->

- [source_manifest_ingest.py](source_manifest_ingest.py): 검증·보관·게시 한 task.

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| S3 매니페스트 -> DEV PostgreSQL 게시 | `source_manifest_ingest.py` DAG(Airflow worker) | DEV PostgreSQL | worker의 `/run/opsflow/s3.json`·`pg.json`으로 접속하며 XCom에는 run ID·data_version·status·행수만 전달한다. | timeout과 bounded retry를 선언하고 예외는 고정된 실패 코드로 제한한다. |

###### Inputs and Outputs
<!-- core-payload-level:4 -->

이 DAG는 worker의 `/run/opsflow/s3.json`과 `/run/opsflow/pg.json`을 읽어 S3의 매니페스트를 검증하고 DEV PostgreSQL에 게시한다. 자체 포트는 열지 않는다.

###### Security Boundary
<!-- core-payload-level:4 -->

접속 정보는 worker에만 mount되는 `/run/opsflow`의 `s3.json`, `pg.json`이며 값은 이 폴더에 두지 않는다. 경계 상세는 상위 `manifest-pipeline/README.md`의 Security Boundary를 따른다.

#### Usage

##### Prerequisites

Airflow의 apiserver, scheduler, dag-processor, triggerer, worker가 `source_manifest_ingest.py`를 `infra/07-workflow/airflow/docker-compose.yml`에서 읽기 전용으로 mount해 실행한다. 이 폴더에는 Compose나 Dockerfile이 없다.

##### Selected Start

###### Usage
<!-- core-payload-level:4 -->

현재 기본은 paused·schedule None입니다. Task 실행에서만 ingest 설정을 읽고
XCom에는 run ID·원본 SHA-256인 data_version·status·행수만 전달합니다.
원본 payload·객체 메타데이터·자격은 전달하지 않으며 예외는 고정된 실패 코드로 제한합니다.

#### Checks

##### Readiness

없음: 이 폴더 자체의 검사 명령은 없으며, DAG 검증은 상위 `manifest-pipeline/README.md`의 Selected Start가 지정한 unittest를 따른다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

이 서비스의 런북은 다음과 같다.

- RUN-0050: `docs/05.operations/03.runbooks/08.workflows-and-automation/0050-airflow.md`

###### Related Documents
<!-- core-payload-level:4 -->

- [배치](../README.md)
- [Library](../workflow_lib/README.md)

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 이 폴더는 헬스체크를 선언하지 않는다. DAG는 수동·paused 상태이며 실행 상태는 Airflow 서비스와 RUN-0050이 소유한다.

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
