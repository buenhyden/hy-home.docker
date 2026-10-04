---
title: "비밀 파일 관리"
version: "1.2.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2026-02-23"
---

# 비밀 파일 관리

## Overview

`secrets/`는 HOME 서비스와 독립 LAB의 자격 증명, 인증서, 복구 산출물을 보관한다. 이 문서는 경로와 소유권만 설명하며 값은 기록하지 않는다. 공개 등록표의 ID와 경로는 [SENSITIVE_ENV_VARS.md.example](SENSITIVE_ENV_VARS.md.example)이 소유하고, Git에서 제외된 `SENSITIVE_ENV_VARS.md`는 같은 메타데이터와 개인 값 칸을 가진다.

## Audience

운영자, 보안 관리자, Compose 작성자와 검증 담당자가 사용한다.

## Scope

- 루트 Compose와 독립 LAB의 비밀 파일 경로, 공개·개인 등록표, 파일 권한과 검증 진입점을 다룬다.
- 실제 값 발급·회전, HOME 재시작, 데이터 복구는 해당 서비스의 승인된 운영 절차가 소유한다.
- `.env`와 `.env.example`, `labs/.env`와 `labs/.env.example`은 각각 키 집합을 맞춘다. 실제 값은 개인 파일에만 두며, 선택되지 않은 LAB 시나리오의 입력은 미설정 상태로 표시한다.

## Structure

| 경로 | 책임 |
| --- | --- |
| `auth/` | 게이트웨이·OIDC·관리자 인증 |
| `automation/` | Airflow·n8n 자동화 |
| `backup/` | pgBackRest·Restic 키와 OpenBao 복구 스냅샷 |
| `certs/` | TLS·CA 인증서와 호스트 전용 서명 키 |
| `communication/` | SMTP·Slack·Stalwart 전달 자격 증명 |
| `data/` | 검색·Supabase 등 데이터 서비스 |
| `db/` | 관리·개발 DB와 Valkey, SurrealDB. 프로젝트별 새 자격 증명은 승인된 등록 후 배치 |
| `labs/` | 루트와 분리된 LAB별 자격 증명 |
| `observability/` | 관측 서비스 인증 |
| `security/` | OpenBao 토큰·unseal·보관 정보 |
| `storage/` | SeaweedFS·S3 인증 |
| `tools/` | 선택형 도구 인증 |
| `.backup-<date>/`, `.retired/<date>/` | Git과 Compose에서 제외된 보호 백업·퇴역 보관 |

값 파일은 `영역/서비스/파일`로 배치한다. `auth/`는 Traefik·Keycloak·OAuth2 Proxy와 각 OIDC 소비자, `automation/`은 Airflow·n8n, `data/`는 OpenSearch·Qdrant·Supabase, `storage/`는 SeaweedFS, `tools/`는 도구별 디렉터리로 나눈다. `communication/`은 공용 SMTP·Slack·Stalwart·Supabase 전달 자격 증명을 구분한다. 기존 `common/`과 `communication/`, `db/surreal_db/`와 `db/surrealdb/`의 동일 파일은 각각 새 서비스별 경로와 `db/surrealdb/`의 단일 원본으로 통합한다.

`db/mng-pg/`는 관리 metadata와 Grafana 관리 reader, `db/dev-pg/`는 개발 관리자·fixture 역할·dbt·Debezium을 소유한다. `db/legacy-app/`는 사용하지 않는 기존 app_db의 전환·롤백 보관이며 신규 프로젝트에 재사용하지 않는다. Valkey는 `db/mng-valkey/`, `db/dev-valkey/`, 선택형 n8n 전용 `db/n8n-valkey/`로 분리한다. `backup/mng-pg/`와 `backup/dev-pg/`는 각 pgBackRest 키, `backup/restic/`는 로컬·원격 저장소 자격 증명, `backup/openbao/`는 스냅샷을 소유한다.

`certs/`와 `labs/`의 기존 서비스별 배치는 유지한다. `security/openbao/`의 token·unseal·custody 정보, 인증서와 OpenBao 스냅샷은 각각 Docker Secret 등록 행 또는 별도 운영 소유권으로 관리한다. 비밀값 ID는 경로 이동에도 유지하고 등록표 갱신일은 메타데이터 검토일로 기록한다.

HOME 전환 전에는 실행 중 소비자가 사용하는 옛 경로에 동일 inode의 호환 하드링크를 보존한다. 이는 값의 별도 사본이 아니다. 한 경로를 원자적으로 교체하면 다른 경로와 분리될 수 있으므로 credential 회전·HOME 재시작·호환 경로 제거는 새 Compose 반영 후 승인된 운영 검증을 거친다. 백업·퇴역 자료는 활성 서비스 디렉터리와 합치지 않는다.

## Getting Started

1. [공개 등록표](SENSITIVE_ENV_VARS.md.example)의 ID·경로·날짜·용도를 확인하고 [루트 Compose](../docker-compose.yml) 또는 해당 `labs/*.yml`의 실제 소비자를 대조한다.
2. 개인 파일을 다루는 작업은 대상·승인·백업·복구 범위를 Task에 기록한다. 값 파일이나 개인 등록표의 원문을 채팅·문서·Git 출력에 넣지 않는다.
3. 다른 승인된 작업 트리의 공개 예제를 소비해야 하면, 개인 파일이 있는 원본 체크아웃에서 해당 작업 트리의 스크립트를 `--sync-metadata-prune --metadata-source-root <승인된-공개-작업트리>`로 실행한다. 이 옵션은 메타데이터 모드에만 적용되며 개인 값은 원본 체크아웃에 남고 다른 작업 트리에 복제하지 않는다. 먼저 `--sync-metadata-prune-check`로 변경 여부를 확인한다.
4. 값 없이 공개 계약을 확인할 때 `bash scripts/operations/gen-secrets.sh --dry-run`을 사용한다. 개인 메타데이터 비교는 승인된 범위에서 `--sync-metadata-prune-check`를 사용한다.

## Usage

- 새 ID는 기존 번호를 재사용하지 않는다. 공개 등록표의 구분·경로·생성/갱신일·용도를 실제 소비자에 맞추고, 개인 등록표는 값 칸만 보존하여 [기존 동기화 스크립트](../scripts/operations/gen-secrets.sh)로 정렬한다.
- 값 파일은 Git에서 기본 제외한다. 자격 증명 디렉터리는 최대 `0750`(새 경로·호스트 전용은 `0700`도 허용), 보호 백업·퇴역 영역은 `0700`으로 유지한다. 그룹 쓰기 권한을 주지 않는다. 호스트 백업·호환 참조와 새 경로의 접근 권한을 확인하고, 서비스의 UID/GID 읽기 검사는 승인된 격리 환경에서 수행한다.
- 루트 `.env`에는 현재 공개 키에 대응하는 실제 값을 보존한다. `labs/.env`의 선택형 Locust 시나리오·결과 경로처럼 승인된 대상이 없는 값은 임의 경로로 채우지 않는다.
- 실제 credential 교체에는 서버 측 값 변경, 소비자 재시작, 검증과 복구 계약이 함께 필요하다. 파일 이동이나 메타데이터 정렬만으로 교체가 완료되지는 않는다.

## Related Documents

- [문서 인덱스](../docs/README.md): 아래 단계 문서는 이 인덱스에서 찾는다.
- 민감 변수 비교: `docs/05.operations/guides/0010-sensitive-env-vars-comparison.md`
- 백업·복구 정책: `docs/05.operations/policies/0021-backup-and-restore.md`
- README 양식: `docs/99.templates/templates/common/readme-repository.template.md`
