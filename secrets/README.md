---
title: "Secret Handling Surface"
version: "1.0.5"
type: "common/repository-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
created: "2026-02-23"
---

# Secrets Management

> Docker Secrets 포맷의 민감 정보 파일 경로와 운영 규칙을 관리하는 보안 진입 문서

## Overview

`secrets/`는 `hy-home.docker` 인프라에서 사용하는 비밀번호, 키, 토큰, 인증서 관련 파일 경로를 Docker Secrets 포맷으로 배치하는 공간입니다. 이 README는 secret 값 자체가 아니라 디렉터리 구조, registry, 생성/검증 절차, 안전한 운영 원칙을 설명합니다.

이 작업 범위에서는 `secrets/**/*.txt` 값 파일을 열람하지 않습니다. 파일명, 디렉터리 구조, `SENSITIVE_ENV_VARS.md.example`, 관련 README와 스크립트 설명만 기준으로 분석하고 문서화합니다.

## Audience

이 README의 주요 독자:

- Operators
- Security Maintainers
- Developers
- AI Agents

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
├── backup/               # HOME 백업 키와 미발급 dev-pg 전용 키 경로
├── certs/                # 로컬 TLS 인증서 파일 경로
├── common/               # SMTP, webhook 등 공통 secret
├── data/                 # OpenSearch, Supabase, AI 도구 관련 secret
├── db/                   # HOME DB secret; dev-pg/·dev-valkey/는 미발급 개발 전용
├── labs/                 # 독립 LAB별 새 credential 참조 자리(현재 미발급)
├── observability/        # Grafana와 monitoring stack secret
├── security/             # OpenBao 서비스 자격 증명
├── storage/              # SeaweedFS object storage secret
├── tools/                # SonarQube 등 선택 도구 secret
├── SENSITIVE_ENV_VARS.md.example  # registry 예시
└── README.md             # This file
```

## How to Work in This Area

1. secret 값 파일을 열지 말고, 먼저 이 README와 `SENSITIVE_ENV_VARS.md.example`를 확인합니다.
2. 새 secret 경로가 필요하면 대응 서비스의 `infra/` Compose 정의와 registry mapping을 함께 확인합니다.
3. secret 생성 또는 누락 파일 보강은 `./scripts/operations/gen-secrets.sh` 같은 승인된 스크립트를 우선 사용합니다.
4. 인증서 파일은 Developer Environment Operations (`docs/05.operations/guides/0002-developer-environment.md`)의 local TLS 절차와 관련 runbook을 따릅니다.
5. 문서, 로그, commit, PR 설명에는 secret 값 원문을 쓰지 않습니다.

## Navigation / Inventory

The 2026-10-03 path-only inventory covers every active child of `secrets/`.
The public registry has 138 IDs: 105 file paths and 33 environment-only IDs.
The owner checkout has 102 active files outside the registry/README and ignored
retirement or backup areas: 85 registered credential files and 17 artifacts
with separate ownership. The 20 registered but absent paths are six unissued
`dev-pg`/`dev-valkey`/backup credentials and 14 unissued LAB credentials.
Counts describe paths, never file contents or service readiness.

| Area | Registry paths | Declared and granted | Present | Unissued | Role and separate artifacts |
| --- | ---: | ---: | ---: | ---: | --- |
| `auth/` | 14 | 13 | 14 | 0 | Gateway, identity and OIDC; one derived input |
| `automation/` | 4 | 4 | 4 | 0 | Airflow and n8n |
| `backup/` | 6 | 6 | 5 | 1 | pgBackRest and Restic; one protected OpenBao snapshot outside the registry |
| `certs/` | 0 | 0 | 0 | 0 | 15 separate TLS/CA artifacts: 14 bind consumed, `rootCA-key.pem` host-only signing key (0400) |
| `common/` | 5 | 5 | 5 | 0 | Delivery and integrations |
| `data/` | 15 | 15 | 15 | 0 | OpenSearch, Supabase and data/AI |
| `db/` | 26 | 25 | 21 | 5 | HOME databases plus unissued dev-pg/dev-valkey; one cutover hold |
| `labs/` | 14 | 14 | 0 | 14 | Standalone LAB only |
| `observability/` | 2 | 1 | 2 | 0 | Grafana and metrics; one derived input |
| `security/` | 2 | 1 | 2 | 0 | OpenBao; one host-only recovery input and one custody artifact outside the registry |
| `storage/` | 8 | 8 | 8 | 0 | SeaweedFS/S3 |
| `tools/` | 9 | 9 | 9 | 0 | Optional engineering tools |
| **Total** | **105** | **101** | **85** | **20** | **17 separate cert/snapshot/custody artifacts** |

`SENSITIVE_ENV_VARS.md.example` owns public ID/path/date/purpose metadata.
`SENSITIVE_ENV_VARS.md` is its ignored value-preserving projection. Ignored
`.backup-<date>/` and `.retired/<date>/` are custody areas, excluded from the
active counts and from Compose mounts. Empty markers exist only for current
or approved unissued path contracts; obsolete NoSQL and messaging markers
were removed without deleting ignored files.

## Root and LAB ownership

Root `.env.example` has 219 names consumed by the root include graph; standalone
`labs/.env.example` has 39 `LAB_` names. The public sets and their private
counterparts are disjoint. Root Compose declares 87 secrets outside
`secrets/labs/`; the seven standalone LAB entrypoints declare 14 secrets only
under `secrets/labs/`. A root administrator UI CIDR input was renamed from
`LAB_ALLOWED_CIDRS` to `ADMIN_UI_ALLOWED_CIDRS` in candidate source because it
controls RedisInsight, Dozzle and Open Notebook in the root graph. Two identity
inputs were clarified as `OPENSEARCH_ADMIN_USERNAME` and
`GRAFANA_OIDC_CLIENT_ID`; their former names described different products or
a proxy that is no longer the Grafana auth owner. The main private `.env`
retains all three old keys only for current main compatibility until source
landing; each new alias has the same value. None is a LAB resource. The ten
private-only compatibility names are `DBT_DB_NAME`, `DBT_SOURCE_SCHEMA`,
`ES_PERFORMANCE_ANALYZER_HOST_PORT`, `ES_PERFORMANCE_ANALYZER_PORT`,
`LAB_ALLOWED_CIDRS`, `OPENSEARCH_CLUSTER_NAME`, `SERVICE_POSTGRES_DB`,
`SERVICE_POSTGRES_USERNAME`, `ELASTIC_USERNAME` and
`GRAFANA_PROXY_CLIENT_ID`. Current main still consumes them; review removal
after source landing and rollback closure. The upstream Supabase `.env.example` inside
`infra/04-data/supabase/` uses product-defined key names; the sample web
service `.env.example` uses its own `WEB_HOST_PORT`. Neither is the root or
standalone LAB environment contract.

## LAB Credential Boundary

`labs/*.yml`은 루트 Compose의 secret 선언을 소비하지 않습니다. LAB 자격 증명은
`secrets/labs/<topology>/`에 토폴로지별로 새로 발급한 뒤 해당 독립 Compose에만
읽기 전용으로 연결합니다. 현재 추적된 `.gitkeep`은 디렉터리 계약이며 비밀값이
아닙니다. `postgresql-ha`, `valkey-cluster`, `couchdb`, `mongodb`,
`opensearch-cluster`의 실제 새 credential 파일은 아직 발급되지 않았습니다.
Cassandra LAB는 현재 인증 secret을 선언하지 않으며 내부망 단일 노드로만 분류합니다. Kafka LAB은
현재 secret file을 선언하지 않지만 전용 KRaft ID와 새 상태 경로가 필요합니다.

기존 HA/NoSQL 실습 전용 credential은 새 LAB 자격 증명으로 재사용하지 않습니다.
소비자 확인 후 파일명·권한·inode를 확인하고 기존 정책의
`secrets/.retired/<date>/<original subdirectory>/`로 보존합니다. 정상 HOME이
계속 소비하는 관리 PostgreSQL·OpenSearch·Traefik secret은 이 경계에 포함하지
않습니다. 이전 LAB 자격 증명 10개는 `.retired/2026-10-02/`에 보존되어
있어 현재 main의 오래된 LAB profile을 그대로 재시작하면 필요한 파일이 없을 수
있습니다. 후보 LAB 소스 반영 또는 승인된 복원 전에는 이전 profile을 실행하지
않습니다. 비밀값 발급·회전, 컨테이너 재생성·실행, 복구는 각각 별도의 실행 계약입니다.

개발 엔진의 새 참조는 `secrets/db/dev-pg/` (관리자·fixture 역할별),
`secrets/db/dev-valkey/admin_password.txt`,
`secrets/backup/dev-pg/pgbackrest_cipher_pass.txt`입니다. 경로가 Compose에 선언되어
있어도 현재 파일 발급이나 역할 비밀번호 동기화가 완료됐다는 뜻은 아닙니다.
`secrets/db/dev-pg/`, `secrets/db/dev-valkey/`, `secrets/backup/dev-pg/`는
기존 HOME secret과 분리된 미발급 경로입니다. OpenSearch LAB credential은
`secrets/labs/opensearch-cluster/`에 두며 인증서는 이 트리가 아니라
`LAB_OPENSEARCH_CERT_DIR`의 별도 읽기 전용 경로가 소유합니다.

## Inventory Classification

현재 인벤토리는 secret 값이나 인증서 원문을 열람하지 않고 파일명, 디렉터리, 루트·LAB Compose 선언, registry 예시만 기준으로 분류합니다. 기존 HOME secret 경로는 실행 중 소비자와 재시작 경계가 있어 이 소스 변경에서 이동하지 않습니다.

| Classification | Current Evidence | Handling Rule |
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

Root declarations without a service grant are retired from Compose. Unused
registry rows are removed from both schema copies after owner-approved review;
retained values and individual credential files remain unchanged. `PG-020` is
held for the existing `app_db` cutover and has no current candidate Compose
consumer; review retirement only after approved HOME cutover and rollback-window
closure. Removed IDs
remain reserved by history and must not be reused.

`SEC-001` / `secrets/security/vault_token.txt` left the public schema with the
Vault source in SPEC-0180 S08. On 2026-09-23 the owner-requested cleanup pruned
the private `SEC-001` and MinIO `STRG-001`–`STRG-006` rows (the local registry
backup keeps them) and moved the unused files to the quarantine below. On
2026-09-25 SPEC-0182 W5 disposed of the quarantined MinIO and Vault files in
`secrets/.retired/2026-09-23/` (the four `storage/minio_*` files,
`storage/mlflow_s3_password.txt`, `tools/terrakube_minio_secret_key.txt`,
`security/vault_token.txt` and `security/vault_unseal_keys.legacy.txt`) and
`secrets/.backup-20260923/`, together with the MinIO data and the Vault tree.
The legacy Vault root token is moot.

Unused credential files are not deleted in place. They move to
`secrets/.retired/<date>/<original subdirectory>/` (`0700`, Git-ignored) until
an approved disposal. Before a private registry or `.env` rewrite, keep a copy
in `secrets/.backup-<date>/` (`0700`/`0600`, Git-ignored) and remove it once
the result is verified. Both directories are outside every Compose mount.

`SEC-002` / `secrets/security/openbao_token.txt` is the manually issued
Prometheus credential for authenticated OpenBao metrics. It is not generated by
metadata synchronization and must carry only the dedicated `prometheus` policy.
Never substitute an OpenBao root token, human operator token or renderer Agent
token.

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

현재 동기화 스크립트는 같은 checkout의 공개 스키마와 private projection을
세 쌍(등록표, root env, LAB env)으로 처리합니다. 후보 소스가 main에 반영되기
전에는 main의 기존 소비자가 쓰는 환경 키를 보존합니다. 2026-10-03의 한 차례
개인 등록표 메타데이터 정리는 138개 ID의 값 칸을 그대로 둔 채 후보 공개판의
경로·날짜·용도만 반영했으며, 보호된 ignored 백업을 남겼습니다. 현재 main checkout의 공개 등록표는 아직 126 ID이고 main의 개인 등록표는
후보 공개 계약 138 ID에 정렬되어 있습니다. 후보 소스가 반영되기 전 main의
옛 `gen-secrets.sh --sync-metadata*`를 실행하면 이전 ID를 다시 추가하거나
후보 메타데이터를 되돌릴 수 있으므로 사용하지 않습니다. 소스 반영 뒤
같은 checkout에서 `--sync-metadata-check`를 실행하고, legacy root 키의
퇴역을 별도 소비자 검토로 결정합니다. `--sync-metadata-prune`는 그 전환
승인이 없으면 사용하지 않습니다.

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
- [Documentation index](../docs/README.md)
