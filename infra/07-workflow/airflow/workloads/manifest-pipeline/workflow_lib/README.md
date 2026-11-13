---
title: "Manifest Pipeline Library"
version: "0.2.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# Manifest Pipeline Library

## Purpose

### Service Role

#### Overview

엄격한 합성 manifest parser와 task 실행 시 사용하는 전용 I/O adapter를 둡니다.

#### Scope

원본 bytes 기반 ID, 불변 records, 허용 source/date/path, 보호 설정 파일과
S3 readback·불량 입력 격리·PG 게시를 소유합니다. 다른 DB·객체·자격 증명은 접근 대상이 아닙니다.

#### Structure

- [manifest.py](manifest.py): parser·ID·partition·게시 순서.
- [adapters.py](adapters.py): 보호 JSON·S3·parameterized PostgreSQL.
- [tls.py](tls.py): 보호된 CA 검증과 쓰기 금지한 메모리 사본의 수명 관리.

### Supported Environment

Airflow의 apiserver, scheduler, dag-processor, triggerer, worker가 `workflow_lib/`를 `infra/07-workflow/airflow/docker-compose.yml`에서 읽기 전용으로 mount해 import한다. 이 폴더에는 Compose나 Dockerfile이 없다.

## Interfaces

### Inputs and Outputs

DAG가 호출하는 Python 모듈(`manifest.py`, `adapters.py`, `tls.py`)이며 자체 포트는 없다. `adapters.py`가 `/run/opsflow`의 `pg.json`, `s3.json`을 읽고 `tls.py`가 `ca.pem`을 다룬다.

### Security Boundary

`/run/opsflow`의 `pg.json`, `s3.json`은 고정 경로를 확인한 뒤 읽고, `ca.pem`은 `tls.py`가 검증해 전달한다. 값은 이 폴더에 두지 않는다.

## Development

### Local Workflow

#### Usage

드라이버는 task 실행 때만 import합니다. 실제 endpoint와 권한 검증을 합성
double의 PASS로 대신하지 않습니다. 설정 예시는 실행 가능한 credential이 아닙니다.

`Store.put_quarantine(key, body, reason)`은 1MiB 이하의 검증 실패 원본을
`manifest-quarantine/<source>/<business_date>/<sha256>.json`에 조건부로 보존합니다.
Content-Type은 key 확장자와 같은 `application/json`이며(SeaweedFS는 `.json` key를
요청값과 관계없이 이 형식으로 저장한다) 메타데이터 `reason`은 고정 코드
`manifest_invalid` 또는 `partition_mismatch`, `data-version`은 원본 SHA-256입니다.
기존 객체의 bytes와 메타데이터가 다르거나 보존에 실패하면 게시를 중단합니다.
크기 초과·읽기 실패는 원본이 보존됐다고 기록하지 않습니다.

정상 반환값은 `run_id`, `data_version`, `status`, `records`입니다. `data_version`은
기존 원본 digest이고 run ID 계산은 유지합니다. 검증과 S3 readback 뒤에만 SQL
게시를 호출하며, 실패한 입력은 DB 결과와 outbox를 만들지 않습니다.

### Checks

없음: 이 폴더 자체의 검사 명령은 없으며, 검증은 상위 `manifest-pipeline/README.md`의 Local Workflow가 지정한 unittest를 따른다.

## Operations

### Runbook Links

이 서비스의 런북은 다음과 같다.

- RUN-0050: `docs/05.operations/runbooks/08-workflows-and-automation/0050-airflow.md`

#### Related Documents

- [배치](../README.md)
- [예시](../fixtures/README.md)

### Observability and Recovery

없음: 이 폴더는 라이브러리이며 헬스체크나 관측 대상을 선언하지 않는다. 상태는 Airflow 서비스와 RUN-0050이 소유한다.
