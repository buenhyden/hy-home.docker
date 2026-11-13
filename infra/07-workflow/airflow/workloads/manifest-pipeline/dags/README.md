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

공개 `airflow.sdk`를 사용하는 단일 수동 배치입니다. 등록 중 workload 파일·DB·S3를 읽지 않습니다.

최대 active run/task 각각 하나, pool 한 slot, timeout과 bounded retry를 선언합니다.
실제 pool 생성·Celery worker 실행은 별도 검증 대상입니다.

#### Structure

- [source_manifest_ingest.py](source_manifest_ingest.py): 검증·보관·게시 한 task.

### Supported Environment

없음: 이 디렉터리에는 Compose 파일이나 Dockerfile이 없어 독립 런타임 환경을 선언하지 않는다. 포함 항목은 `source_manifest_ingest.py`이다.

## Interfaces

### Inputs and Outputs

없음: 이 폴더는 자체 포트나 네트워크 인터페이스를 선언하지 않으며 `source_manifest_ingest.py`만 둔다.

### Security Boundary

없음: 이 폴더에는 Compose 서비스와 secret 정의가 없으며, secret 값을 저장소에 두지 않는다.

## Development

### Local Workflow

현재 기본은 paused·schedule None입니다. Task 실행에서만 ingest 설정을 읽고
XCom에는 run ID·원본 SHA-256인 data_version·status·행수만 전달합니다.
원본 payload·객체 메타데이터·자격은 전달하지 않으며 예외는 고정된 실패 코드로 제한합니다.

### Checks

없음: 이 폴더는 자체 테스트나 검증 스크립트를 두지 않는다.

## Operations

### Runbook Links

#### Related Documents

- [배치](../README.md)
- [Library](../workflow_lib/README.md)

### Observability and Recovery

없음: 이 폴더에는 헬스체크나 관측 대상 선언이 없다.
