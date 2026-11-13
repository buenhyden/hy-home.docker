---
title: "Manifest Pipeline DAG"
version: "0.2.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# Manifest Pipeline DAG

## Purpose

### Service Role

#### Overview

공개 `airflow.sdk`를 사용하는 단일 수동 배치입니다. 등록 중 workload 파일·DB·S3를 읽지 않습니다.

#### Scope

최대 active run/task 각각 하나, pool 한 slot, timeout과 bounded retry를 선언합니다.
실제 pool 생성·Celery worker 실행은 별도 검증 대상입니다.

#### Structure

- [source_manifest_ingest.py](source_manifest_ingest.py): 검증·보관·게시 한 task.

### Supported Environment

Airflow의 apiserver, scheduler, dag-processor, triggerer, worker가 `source_manifest_ingest.py`를 `infra/07-workflow/airflow/docker-compose.yml`에서 읽기 전용으로 mount해 실행한다. 이 폴더에는 Compose나 Dockerfile이 없다.

## Interfaces

### Inputs and Outputs

이 DAG는 worker의 `/run/opsflow/s3.json`과 `/run/opsflow/pg.json`을 읽어 S3의 매니페스트를 검증하고 DEV PostgreSQL에 게시한다. 자체 포트는 열지 않는다.

### Security Boundary

접속 정보는 worker에만 mount되는 `/run/opsflow`의 `s3.json`, `pg.json`이며 값은 이 폴더에 두지 않는다. 경계 상세는 상위 `manifest-pipeline/README.md`의 Security Boundary를 따른다.

## Development

### Local Workflow

#### Usage

현재 기본은 paused·schedule None입니다. Task 실행에서만 ingest 설정을 읽고
XCom에는 run ID·원본 SHA-256인 data_version·status·행수만 전달합니다.
원본 payload·객체 메타데이터·자격은 전달하지 않으며 예외는 고정된 실패 코드로 제한합니다.

### Checks

없음: 이 폴더 자체의 검사 명령은 없으며, DAG 검증은 상위 `manifest-pipeline/README.md`의 Local Workflow가 지정한 unittest를 따른다.

## Operations

### Runbook Links

이 서비스의 런북은 다음과 같다.

- RUN-0050: `docs/05.operations/runbooks/08-workflows-and-automation/0050-airflow.md`

#### Related Documents

- [배치](../README.md)
- [Library](../workflow_lib/README.md)

### Observability and Recovery

없음: 이 폴더는 헬스체크를 선언하지 않는다. DAG는 수동·paused 상태이며 실행 상태는 Airflow 서비스와 RUN-0050이 소유한다.
