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

엄격한 합성 manifest parser와 task 실행 시 사용하는 전용 I/O adapter를 둡니다.

원본 bytes 기반 ID, 불변 records, 허용 source/date/path, 보호 설정 파일과
S3 readback·불량 입력 격리·PG 게시를 소유합니다. 다른 DB·객체·자격 증명은 접근 대상이 아닙니다.

#### Structure

- [manifest.py](manifest.py): parser·ID·partition·게시 순서.
- [adapters.py](adapters.py): 보호 JSON·S3·parameterized PostgreSQL.
- [tls.py](tls.py): 보호된 CA 검증과 쓰기 금지한 메모리 사본의 수명 관리.

### Supported Environment

없음: 이 디렉터리에는 Compose 파일이나 Dockerfile이 없어 독립 런타임 환경을 선언하지 않는다. 포함 항목은 `__init__.py`, `adapters.py`, `manifest.py`, `tls.py`이다.

## Interfaces

### Inputs and Outputs

없음: 이 폴더는 자체 포트나 네트워크 인터페이스를 선언하지 않으며 `__init__.py`, `adapters.py`, `manifest.py`, `tls.py`만 둔다.

### Security Boundary

없음: 이 폴더에는 Compose 서비스와 secret 정의가 없으며, secret 값을 저장소에 두지 않는다.

## Development

### Local Workflow

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

없음: 이 폴더는 자체 테스트나 검증 스크립트를 두지 않는다.

## Operations

### Runbook Links

#### Related Documents

- [배치](../README.md)
- [예시](../fixtures/README.md)

### Observability and Recovery

없음: 이 폴더에는 헬스체크나 관측 대상 선언이 없다.
