---
title: "비밀 파일 관리"
version: "1.0.5"
type: "common/repository-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
created: "2026-02-23"
---

# 비밀 파일 관리

> Docker Secrets 포맷의 민감 정보 파일 경로와 운영 규칙을 관리하는 보안 진입 문서

## Overview

`secrets/`는 `hy-home.docker` 인프라에서 사용하는 비밀번호, 키, 토큰, 인증서 관련 파일 경로를 Docker Secrets 포맷으로 배치하는 공간입니다. 이 README는 secret 값 자체가 아니라 디렉터리 구조, registry, 생성/검증 절차, 안전한 운영 원칙을 설명합니다.

이 작업 범위에서는 `secrets/**/*.txt` 값 파일을 열람하지 않습니다. 파일명, 디렉터리 구조, `SENSITIVE_ENV_VARS.md.example`, 관련 README와 스크립트 설명만 기준으로 분석하고 문서화합니다.

## Audience

이 README의 주요 독자:

- 운영자
- 보안 관리자
- 개발자
- AI 에이전트

## Scope

### In Scope

- Docker secret 파일의 경로 체계와 책임 범위
- secret registry와 example 파일의 사용 방식
- secret 생성/동기화 스크립트 안내
- 문서 작성 시 민감값을 노출하지 않는 기준

### Out of Scope

- secret 값, token, private key, 인증서 원문
- 운영 승인 없는 secret 교체 또는 재생성
- 외부 secret manager 마이그레이션
- Docker Compose runtime 동작 변경

## Structure

```text
secrets/
├── auth/                 # Traefik, Keycloak, proxy 관련 인증 secret
├── automation/           # Airflow, n8n 등 자동화 서비스 secret
├── backup/               # HOME 백업 키와 dev-pg 전용 키 경로
├── certs/                # 로컬 TLS 인증서 파일 경로
├── common/               # SMTP, webhook 등 공통 secret
├── data/                 # OpenSearch, Supabase, AI 도구 관련 secret
├── db/                   # HOME DB secret; dev-pg/·dev-valkey/는 개발 전용
├── labs/                 # 독립 LAB별 credential 경로
├── observability/        # Grafana와 monitoring stack secret
├── security/             # OpenBao 서비스 자격 증명
├── storage/              # SeaweedFS object storage secret
├── tools/                # SonarQube 등 선택 도구 secret
├── SENSITIVE_ENV_VARS.md.example  # registry 예시
└── README.md             # 이 문서
```

## Getting Started

먼저 [공개 등록표](SENSITIVE_ENV_VARS.md.example)에서 ID·경로·용도를 확인하고, 해당 Compose 선언에서 실제 소비 여부를 확인합니다. 파일 값과 개인 등록표는 문서 검토에 사용하지 않습니다.

## How to Work in This Area

1. secret 값 파일을 열지 말고, 먼저 이 README와 `SENSITIVE_ENV_VARS.md.example`를 확인합니다.
2. 새 secret 경로가 필요하면 대응 서비스의 `infra/` Compose 정의와 registry mapping을 함께 확인합니다.
3. secret 생성 또는 누락 파일 보강은 `./scripts/operations/gen-secrets.sh` 같은 승인된 스크립트를 우선 사용합니다.
4. 인증서 파일은 Developer Environment Operations (`docs/05.operations/guides/0002-developer-environment.md`)의 local TLS 절차와 관련 runbook을 따릅니다.
5. 문서, 로그, commit, PR 설명에는 secret 값 원문을 쓰지 않습니다.

## Navigation / Inventory

2026-10-03 경로 인벤토리는 `secrets/`의 활성 하위 영역 전체를 다룹니다. 공개 등록표의 ID는 138개이며, 파일 경로 105개와 환경 변수 전용 ID 33개로 나뉩니다. 소유자 작업 트리에는 등록표·README·무시된 퇴역/백업 영역을 제외한 활성 파일이 122개 있습니다. 등록된 자격 증명 파일 105개와 별도 책임의 산출물 17개입니다. 개발/LAB 파일 20개는 SPEC-0202-TSK-0002에 따라 2026-10-03 발급했습니다. 이 경로 집계는 서비스 준비 상태나 자격 증명의 유효성을 증명하지 않습니다.

| 영역 | 등록 경로 | 선언·권한 부여 | 존재 | 미발급 | 역할과 별도 산출물 |
| --- | ---: | ---: | ---: | ---: | --- |
| `auth/` | 14 | 13 | 14 | 0 | 게이트웨이·인증·OIDC, 파생 입력 1개 |
| `automation/` | 4 | 4 | 4 | 0 | Airflow·n8n |
| `backup/` | 6 | 6 | 6 | 0 | pgBackRest·Restic, 등록표 밖 보호된 OpenBao 스냅샷 1개 |
| `certs/` | 0 | 0 | 0 | 0 | 별도 TLS/CA 산출물 15개: bind 소비 14개, 호스트 전용 서명 키 `rootCA-key.pem` 1개(0400) |
| `common/` | 5 | 5 | 5 | 0 | 전달·공통 연동 |
| `data/` | 15 | 15 | 15 | 0 | OpenSearch·Supabase·데이터/AI |
| `db/` | 26 | 25 | 26 | 0 | HOME·개발 DB, 전환 보류 1개 |
| `labs/` | 14 | 14 | 14 | 0 | 독립 LAB 전용 |
| `observability/` | 2 | 1 | 2 | 0 | Grafana·메트릭, 파생 입력 1개 |
| `security/` | 2 | 1 | 2 | 0 | OpenBao, 호스트 전용 복구 입력 1개와 등록표 밖 보관 산출물 1개 |
| `storage/` | 8 | 8 | 8 | 0 | SeaweedFS/S3 |
| `tools/` | 9 | 9 | 9 | 0 | 선택형 엔지니어링 도구 |
| **합계** | **105** | **101** | **105** | **0** | **별도 인증서·스냅샷·보관 산출물 17개** |

공개 ID·경로·날짜·용도 메타데이터의 원본은 `SENSITIVE_ENV_VARS.md.example`입니다. `SENSITIVE_ENV_VARS.md`는 값을 보존하는 Git 무시 대상 투영본입니다. `.backup-<date>/`와 `.retired/<date>/`는 보관 영역이며 활성 파일 수와 Compose 마운트에서 제외합니다. 빈 디렉터리 표식은 현재 또는 승인된 발급 경로에만 둡니다. 폐기된 NoSQL·메시징 표식을 제거할 때 무시된 실제 파일은 삭제하지 않았습니다.

## Root and LAB ownership

루트 include 그래프가 소비하는 `.env.example` 변수는 219개이고, 독립 `labs/.env.example`에는 `LAB_` 변수 39개가 있습니다. 공개 집합과 대응 개인 집합은 서로 겹치지 않습니다. 루트 Compose는 `secrets/labs/` 밖의 secret 87개를 선언하고, 독립 LAB 진입점 7개는 `secrets/labs/` 아래 secret 14개만 선언합니다.

루트 관리자 UI의 CIDR 입력은 RedisInsight·Dozzle·Open Notebook을 제어하므로 현재 소스에서 `LAB_ALLOWED_CIDRS`를 `ADMIN_UI_ALLOWED_CIDRS`로 바꿨습니다. 인증 입력 두 개도 실제 소비자에 맞춰 `OPENSEARCH_ADMIN_USERNAME`과 `GRAFANA_OIDC_CLIENT_ID`로 명확히 했습니다. main의 개인 `.env`에는 이전 소스 롤백 호환성을 위해 이전 세 이름도 같은 값으로 남겨 두었습니다. 이 세 입력은 LAB 자원이 아닙니다.

개인 환경 파일에만 있는 호환 변수 10개는 `DBT_DB_NAME`, `DBT_SOURCE_SCHEMA`, `ES_PERFORMANCE_ANALYZER_HOST_PORT`, `ES_PERFORMANCE_ANALYZER_PORT`, `LAB_ALLOWED_CIDRS`, `OPENSEARCH_CLUSTER_NAME`, `SERVICE_POSTGRES_DB`, `SERVICE_POSTGRES_USERNAME`, `ELASTIC_USERNAME`, `GRAFANA_PROXY_CLIENT_ID`입니다. 이전 소스와 실행 중 HOME 소비자의 롤백 가능성을 보존하므로 운영 전환과 롤백 기간 종료 뒤 제거 여부를 검토합니다. `infra/04-data/supabase/`의 상위 제품 `.env.example`은 제품 정의 변수명을 쓰고, 예제 웹 서비스의 `.env.example`은 자체 `WEB_HOST_PORT`를 씁니다. 둘 다 루트 또는 독립 LAB 환경 계약이 아닙니다.

## LAB Credential Boundary

`labs/*.yml`은 루트 Compose의 secret 선언을 소비하지 않습니다. LAB 자격 증명은
`secrets/labs/<topology>/`에 토폴로지별로 새로 발급한 뒤 해당 독립 Compose에만
읽기 전용으로 연결합니다. 현재 추적된 `.gitkeep`은 디렉터리 계약이며 비밀값이
아닙니다. `postgresql-ha`, `valkey-cluster`, `couchdb`, `mongodb`,
`opensearch-cluster`의 14개 새 credential 파일은 2026-10-03에 발급했으며,
서비스 기동·인증 성공은 별도 검증입니다.
Cassandra LAB는 현재 인증 secret을 선언하지 않으며 내부망 단일 노드로만 분류합니다. Kafka LAB은
현재 secret file을 선언하지 않지만 전용 KRaft ID와 새 상태 경로가 필요합니다.

기존 HA/NoSQL 실습 전용 credential은 새 LAB 자격 증명으로 재사용하지 않습니다.
소비자 확인 후 파일명·권한·inode를 확인하고 기존 정책의
`secrets/.retired/<date>/<original subdirectory>/`로 보존합니다. 정상 HOME이
계속 소비하는 관리 PostgreSQL·OpenSearch·Traefik secret은 이 경계에 포함하지
않습니다. 이전 LAB 자격 증명 10개는 `.retired/2026-10-02/`에 보존되어
있어 이전 main 소스의 LAB profile로 롤백하여 재시작하면 필요한 파일이 없을 수
있습니다. 승인된 복원 전에는 이전 profile을 실행하지 않습니다. 비밀값 발급·회전, 컨테이너 재생성·실행, 복구는 각각 별도의 실행 계약입니다.

개발 엔진의 새 참조는 `secrets/db/dev-pg/` (관리자·fixture 역할별),
`secrets/db/dev-valkey/admin_password.txt`,
`secrets/backup/dev-pg/pgbackrest_cipher_pass.txt`입니다. 경로가 Compose에 선언되어
있다는 사실만으로 역할 비밀번호 동기화나 서비스 기동이 증명되지는 않습니다.
`secrets/db/dev-pg/`, `secrets/db/dev-valkey/`, `secrets/backup/dev-pg/`는
기존 HOME secret과 분리된 새 발급 경로입니다. OpenSearch LAB credential은
`secrets/labs/opensearch-cluster/`에 두며 인증서는 이 트리가 아니라
`LAB_OPENSEARCH_CERT_DIR`의 별도 읽기 전용 경로가 소유합니다.

## Inventory Classification

현재 인벤토리는 secret 값이나 인증서 원문을 열람하지 않고 파일명, 디렉터리, 루트·LAB Compose 선언, registry 예시만 기준으로 분류합니다. 기존 HOME secret 경로는 실행 중 소비자와 재시작 경계가 있어 이 소스 변경에서 이동하지 않습니다.

| 분류 | 현재 근거 | 관리 기준 |
| --- | --- | --- |
| `compose-declared` | 루트 87개와 LAB 14개의 분리된 `secrets:` 선언; 파일 존재 검사는 별도 실행 증거 | 각 Compose 영역의 Docker Secret mount 계약으로 관리 |
| `bind-mounted-cert` | `certs/`의 CA·서버·SeaweedFS gRPC 인증서 14개 bind 소비와 host 전용 `rootCA-key.pem` 1개 | canonical certificate path는 `secrets/certs/`; 값/원문은 문서화하지 않음 |
| `snapshot/custody` | `backup/openbao/pre-change.snap`, `security/openbao_metrics_token.custody` | Docker Secret registry 밖의 보호된 운영 산출물; 승인된 복구·토큰 runbook이 소유 |
| `derived-input` | `auth/traefik_admin_password.txt`처럼 생성 스크립트가 실제 소비하는 입력 | 파생 소비자 근거가 있는 항목만 registry에 유지 |
| `cutover-retained` | `PG-020`은 후보 Compose 소비자가 없지만 기존 `app_db` 롤백·전환에 필요할 수 있음 | 운영 전환 및 롤백 기간 종료 승인까지 공개·개인 registry에 유지; 값과 파일은 그대로 둠 |
| `retired/local-only` | 현행 소비자와 승인된 전환 보존 근거가 없는 이전 credential 파일 | 활성 registry에서 제외하되 파일 삭제·credential 폐기는 별도 승인 |
| `private-registry` | `SENSITIVE_ENV_VARS.md` | 개인 gitignored registry로 취급하고 내용은 열람하지 않음 |
| `example-registry` | `SENSITIVE_ENV_VARS.md.example` | 새 환경과 문서 검토용 예시 mapping |

`infra/secrets/certs/` 같은 비표준 local-only 경로가 보이더라도 문서 진입점이나 인증서 절차의 기준으로 사용하지 않습니다. 인증서 기준 경로는 항상 `secrets/certs/`입니다.

서비스에 부여되지 않은 루트 선언은 Compose에서 제외합니다. 사용하지 않는 등록표 행은 소유자 검토 뒤 공개·개인 사본에서 함께 제거하며, 보존 대상 값과 개별 자격 증명 파일은 그대로 둡니다. `PG-020`은 기존 `app_db` 전환에 대비해 보존 중이고 현재 후보 Compose 소비자는 없습니다. 승인된 HOME 전환과 롤백 기간 종료 뒤 퇴역을 검토합니다. 제거한 ID는 이력에 예약되어 재사용하지 않습니다.

`SEC-001`/`secrets/security/vault_token.txt`는 SPEC-0180 S08에서 Vault 소스와 함께 공개 스키마에서 제외됐습니다. 2026-09-23 소유자 요청으로 개인 등록표의 `SEC-001`과 MinIO `STRG-001`–`STRG-006` 행을 정리하고 백업을 남겼습니다. 미사용 파일은 검역 영역으로 옮겼습니다. 2026-09-25 SPEC-0182 W5에서 `secrets/.retired/2026-09-23/`의 MinIO·Vault 파일과 `secrets/.backup-20260923/`을 MinIO 데이터·Vault 트리와 함께 폐기했습니다. 이전 Vault root 토큰은 더 이상 효력이 없습니다.

미사용 자격 증명 파일은 제자리에서 삭제하지 않고 승인된 폐기 전까지 `secrets/.retired/<date>/<original subdirectory>/`(`0700`, Git 무시)에 보관합니다. 개인 등록표나 `.env`를 수정하기 전에는 `secrets/.backup-<date>/`(`0700`/`0600`, Git 무시)에 사본을 두고 결과 검증 뒤 정리합니다. 두 디렉터리는 모든 Compose 마운트 밖에 있습니다.

`SEC-002`/`secrets/security/openbao_token.txt`는 인증된 OpenBao 메트릭에 사용하는 수동 발급 Prometheus 자격 증명입니다. 메타데이터 동기화로 생성되지 않으며 전용 `prometheus` 정책만 가져야 합니다. OpenBao root 토큰, 운영자 토큰, renderer Agent 토큰으로 대체하지 않습니다.

## Secret Management System

### Registry

- 공개 ID·환경 키·경로·자동화 메타데이터의 원본은 `SENSITIVE_ENV_VARS.md.example`과 실제 Compose 소비자입니다.
- `SENSITIVE_ENV_VARS.md`는 개인 값을 보존하는 gitignored 투영이며 ID·env-key 집합은 검증된 공개 계약과 같아야 합니다.
- 새 환경이나 문서 검토에서는 `SENSITIVE_ENV_VARS.md.example`을 사용합니다.
- registry는 파일 경로, 대응 `.env` 변수, 자동화 상태, 갱신 이력을 추적해야 합니다.

### Automation

```bash
# 공개 메타데이터만 조사한다. 비밀 값·private registry·.env를 읽지 않는다.
bash scripts/operations/gen-secrets.sh --dry-run

# 아래 두 모드는 private 값을 프로세스 내부에서 보존하지만 출력하지 않는다.
# check는 쓰지 않으며 drift=1, unsafe/ambiguous input=2를 반환한다.
bash scripts/operations/gen-secrets.sh --sync-metadata-check
bash scripts/operations/gen-secrets.sh --sync-metadata

# 실제 소비자 검토와 미사용 키 제거 승인을 받은 경우에만 사용한다.
bash scripts/operations/gen-secrets.sh --sync-metadata-prune-check
bash scripts/operations/gen-secrets.sh --sync-metadata-prune
```

기본 메타데이터 정렬은 기존 Value cell, 알 수 없는 개인 행, 기존 `.env`와 `labs/.env` assignment와
주석을 보존합니다. 빠진 공개 키와 placeholder 행만 추가하며 secret 파일 생성·읽기·
변경, htpasswd 생성, 회전은 수행하지 않습니다. 경로 이탈·symlink·중복 ID/키·해석할 수
없는 행은 거부하고 원자적 파일 교체를 사용합니다. 기존 대상도 regular
non-symlink 파일이어야 합니다. `0600`은 정렬 후 목표 mode입니다. mode만 다른 경우는 입력 거부가 아니라 check에서
변경 필요로 보고하고 write에서 내용과 함께 원자적으로 `0600`으로 교체합니다.
동시 수동 편집은 중단하고 다시 검사합니다. 개인 값을 shell `source`로
실행하거나 전체 내용을 출력하지 않습니다.

엄격한 prune 모드는 공개 스키마에 없는 개인 registry 행과 `.env` 키를 제거해
registry와 루트·LAB 환경 파일의 세 쌍을 공개 계약에 일치시킵니다. 공개 스키마의 실제 소비자는 실행 전에 검토해야
하며 이 모드 자체는 사용 여부를 추측하지 않습니다. 먼저 0700 디렉터리에 0600
백업을 만든 뒤 유지 대상 값/생성일이 보존됐는지와 집합이 일치하는지 검증합니다. 비밀 파일은
삭제하지 않습니다. 모호한 multiline 환경변수는 안전하게 거부합니다.

옵션 없는 실행은 루트와 LAB의 개인 환경 파일에서 registry 환경 ID 값을 읽는 별도 생성/갱신 기능이며 비밀 파일과 htpasswd를 쓸 수 있습니다. 두 환경 파일에 같은 키가 있으면 거부합니다.
메타데이터 감사 용도로는 실행하지 않습니다. `--check`는 이 생성 기능의 도구까지 검사하므로
`htpasswd`가 없는 호스트에서는 실패할 수 있습니다. 메타데이터 모드는 이를 요구하지 않습니다.

특정 secret을 교체해야 할 때는 값을 문서에 쓰지 말고, 승인된 운영 절차에 따라 secure input 또는 스크립트 기반 생성 방식으로 처리합니다. 교체 후에는 해당 서비스의 runbook에 따라 재시작과 검증을 수행합니다.

동기화 스크립트는 같은 작업 트리의 공개 등록표·루트 환경 파일·LAB 환경 파일과
각 개인 투영본을 한 쌍씩 처리합니다. 이 소스의 공개 등록표는 138개 ID이고,
소유자 작업 트리의 개인 등록표도 값 칸을 보존한 채 138개 ID에 정렬되어 있습니다.
2026-10-03 개인 등록표 메타데이터 정리 전에는 Git 무시 백업을 남겼습니다.
로컬 main 반영 뒤 같은 작업 트리에서 `--sync-metadata-check`가 1개 파일의
메타데이터 차이를 보고했습니다. 개인 파일 세 개를 무시된 보호 경로에 백업한 뒤
`--sync-metadata`로 값은 보존하며 1개 파일을 정렬했고, 재검사에서는 변경 필요
파일이 0개였습니다. 실제 secret 파일은 변경하지 않았습니다.
개인 환경 파일의 이전 루트 변수는 현재 HOME 롤백 경계가 끝날 때까지 보존하고,
실제 소비자 검토 뒤 퇴역을 결정합니다. `--sync-metadata-prune`는 별도 승인된
전환 전에는 사용하지 않습니다.

## Security Policy

- `.txt` secret 값 파일은 Git에 커밋하지 않습니다.
- secret 값 파일, private key, token, 인증서 원문을 응답이나 문서에 노출하지 않습니다.
- host filesystem encryption과 Docker secret mount 정책을 운영 환경 기준에 맞게 유지합니다.
- registry와 실제 파일 경로가 달라지면 문서와 검증 절차를 함께 갱신합니다.
- secret 값 파일 mode는 소유자와 `SECRETS_GID`(기본 1000, 소유자의 primary group)만
  읽는 `0640`이 기준입니다. 소유자가 아닌 UID로 실행되는 컨테이너는 공통 template의
  `group_add: ['${SECRETS_GID:-1000}']`로 group read를 얻습니다. 모든 capability를
  제거한 root도 파일 권한 검사를 우회하지 못하므로 `0600`은 소유자 UID 1000 컨테이너만
  읽을 수 있습니다. `gen-secrets.sh`는 새 파일을 `0640`으로 씁니다.
- 아직 실행 검증하지 않은 서비스만 소비하는 파일은 `0644`로 남습니다. 해당 서비스를
  활성화할 때 컨테이너 내부 read test와 `/proc` supplementary group 확인 후 `0640`으로
  낮춥니다. Compose 소비자가 없는 파일은 `0600`입니다. `certs/`는 별도의
  `hyhome-certs` group(`CERT_GROUP_GID`) 모델을 유지합니다.
- legacy Vault 전용이었던 `vault_token.txt`(SEC-001)와 `vault_unseal_keys.legacy.txt`는
  2026-09-25 SPEC-0182 W5 폐기 조치로 `secrets/.retired/2026-09-23/`로 이동했으며
  더 이상 `secrets/security/`에 있지 않습니다. 두 파일 모두 OpenBao를 unseal할 수
  없습니다.
- OpenBao 관련 값은 `secrets/security/`에서 관리합니다(owner 결정, 2026-09-22).
  `openbao_unseal_keys.txt`(SEC-003, `0600`, host 전용)는 Shamir unseal share 3개를
  줄당 하나씩 담고, 그중 2개로 unseal합니다. `openbao_token.txt`(SEC-002)는 Prometheus
  `sys/metrics` 읽기 토큰입니다. initial root token은 폐기되어 저장하지 않으며, Agent
  token은 Agent가 자체 디렉터리에서 관리합니다. 세 share를 한 파일에 두는 것은
  OpenBao runbook(`docs/05.operations/runbooks/0085-openbao.md`)의
  분리 보관 기준에 대한 명시적 예외입니다.
- AI Agent는 secret 값 파일 열람이 필요해 보이는 상황에서도 먼저 사용자 승인과 안전한 대체 절차를 요청해야 합니다.

## Related Documents

- [../README.md](../README.md)
- [../AGENTS.md](../AGENTS.md)
- `docs/05.operations/README.md`
- `docs/99.templates/templates/common/readme-repository.template.md`
- [SENSITIVE_ENV_VARS.md.example](./SENSITIVE_ENV_VARS.md.example)
- [문서 인덱스](../docs/README.md)
