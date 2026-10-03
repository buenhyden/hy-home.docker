---
title: "성능 시험 결과 데이터베이스"
version: "0.1.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
---

# 성능 시험 결과 데이터베이스

## Overview

이 패키지는 개발 PostgreSQL의 공유 `perf_db`와 `quality` schema에 정규화된
시험 결과를 보관하는 소스 계약입니다. 엔진을 추가하지 않으며 관리 데이터베이스나
외부 프로젝트의 업무 데이터베이스를 사용하지 않습니다.

## Audience

성능 시험 결과 importer, 프로젝트별 권한, Grafana 읽기 경계를 구현하거나
검토하는 maintainer를 대상으로 합니다.

## Scope

`run_id`와 `attempt`의 변경 불가능한 실행 신원, artifact checksum, metric summary,
실행기가 보고한 판정과 별도 판정 권한의 이력을 저장합니다. 프로젝트 writer,
reader, verdict 역할은 명시적 manifest로 등록되며 모두 `NOLOGIN` group role입니다.
실제 login과 비밀 파일 발급은 프로젝트 승인 후 별도 작업이 소유합니다.
실행 전 중단은 시작·종료 시각을 `NULL`로 보존하며 완료 실행은 두 시각과 순서를
모두 검증합니다.

## Structure

- [`bootstrap.sql`](bootstrap.sql)은 고정된 `perf_db`, `perf_owner`,
  `perf_migrator` 경계를 만들고 schema migration을 호출합니다.
- [`schema.sql`](schema.sql)은 표, RLS, 멱등 실행 claim과 읽기 view를 소유합니다.
- [`provision.py`](provision.py)는 one-shot job의 secret 처리와 동시 실행 잠금을
  소유합니다.
- [`register.py`](register.py)는 프로젝트 manifest를 검증하고 등록 SQL만 출력합니다.
- [`project.example.json`](project.example.json)은 비밀값 없는 schema v1 예제입니다.

## Tech Stack

상위 개발 PostgreSQL [Dockerfile](../Dockerfile)과
[Compose](../../docker-compose.yml)에 선언된 이미지에서 PostgreSQL RLS, role
membership, JSONB와 core SHA-256 함수를 사용합니다. 별도 데이터베이스 이미지나
Python 의존성을 추가하지 않습니다.

## Configuration

등록 manifest는 `schema_version`, `project_id`, `roles.reader`, `roles.writer`,
`roles.verdict`만 허용합니다. 역할 이름은 임의 조합하지 않고 승인된 manifest에
직접 기록합니다. writer는 실행·artifact·metric INSERT와 같은 프로젝트 조회만,
reader는 같은 프로젝트 조회만, verdict 역할은 같은 프로젝트의 판정 event
INSERT만 받습니다. UPDATE, DELETE, 소유권, `BYPASSRLS`는 부여하지 않습니다.

`quality.run_results`는 `security_invoker` view이므로 조회자의 RLS가 그대로
적용됩니다. 전체 프로젝트를 읽는 Grafana login이나 secret은 이 패키지가 미리
만들지 않습니다.

`quality-results` profile은 `dev-pg`와 `dev-perf-provision` one-shot job을
선택합니다. 기존 `testing` profile의 k6 one-shot 의미는 유지되며 결과 적재가
필요한 실행은 두 profile을 명시적으로 함께 선택합니다. job은 admin secret을
프로세스 환경으로만 전달하고 별도 PostgreSQL 세션의 `pg_try_advisory_lock`을
bootstrap 종료까지 유지합니다. 동시 job은 exit 75로 종료되며 재실행이
필요합니다.

## Validation

저장소 루트에서 다음 정적 검사를 실행합니다.

```bash
python3 -m unittest tests.validation.test_perf_db_contract
python3 infra/04-data/dev-db/pg/perf/register.py \
  infra/04-data/dev-db/pg/perf/project.example.json --validate-only
```

실제 SQL 권한 검사는 고유 project, network, volume과 합성 비밀값을 사용하는
승인된 격리 PostgreSQL에서 수행해야 합니다. HOME 적용 결과로 해석하지 않습니다.

## How to Work in This Area

schema 변경은 새 migration version과 replay/conflict 검사를 함께 갱신합니다.
project 등록 SQL은 admin이 `perf_db` migration 적용 후 실행하며 출력에
credential을 포함하지 않습니다. 외부 프로젝트 importer는 한 transaction에서
`quality.import_payload`에 schema v1 envelope와 `payload_sha256` 필드를 제외한
canonical UTF-8 bytes를 전달합니다. DB가 JSON 동등성과 SHA-256을 다시 검사한
후 함수는
`inserted`일 때만 자식 행을 적재하고 `exact_replay`에서는 기존 행을 변경하지
않습니다.

## Related Documents

[문서 진입점](../../../../../docs/README.md)에서 SPEC-0203과 개발 데이터 운영
문서를 확인하십시오.
