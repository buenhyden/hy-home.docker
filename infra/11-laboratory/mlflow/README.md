---
title: "Laboratory MLflow Tracking Server"
version: "1.0.2"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2026-09-21"
---

# Laboratory MLflow Tracking Server

> 관리 PostgreSQL과 전용 SeaweedFS 버킷을 기반으로 하는 실험 추적 및 모델 레지스트리입니다.

## Overview

MLflow는 실행(run), 파라미터, 메트릭, 등록된 모델, 아티팩트를 기록합니다.
추적 저장소는 `mng-pg`의 전용 데이터베이스에 있으며 아티팩트는
`mlflow-artifacts` SeaweedFS 버킷에 저장되고 서버를 통해 프록시되므로
(`--serve-artifacts`), SDK 클라이언트는 오브젝트 스토리지 자격 증명을
보유하지 않습니다. Lifecycle: **OPTIONAL**이며 `mlops` 또는 `data-science`
프로필에서만 선택됩니다. HOME이나 현재 8개 프로필 운영 선택에는 포함되지
않습니다.

## Audience

- **Data scientists and ML engineers**: JupyterLab이나 스크립트에서 실험 기록.
- **Operators**: 추적 저장소와 아티팩트의 프로비저닝, 백업, 복구.
- **AI agents**: 소유 Guide, Policy, Runbook에 따라 이 패키지를 변경.

## Scope

- **Included**: 추적 서버, 기능 소유 데이터베이스 프로비저닝 작업, 게이트웨이 라우트.
- **Excluded**: SeaweedFS(버킷 및 identity)와 `mng-pg` 서버 운영(각자의 패키지), JupyterLab, 모델 서빙,
  MLflow 인증 플러그인(채택되지 않음; Guide 참고).

## Structure

```text
.
├── Dockerfile                    # Official MLflow image + PostgreSQL/S3 client libraries
├── requirements.txt              # Pinned client libraries for the server image
├── docker-compose.yml            # mlflow, mlflow-db-provision
├── provisioning/
│   └── mng-pg.sql                # Role, database and CONNECT policy (feature-owned)
└── README.md
```

## Tech Stack

| Component | Source | Purpose |
| --- | --- | --- |
| `mlflow` | 공식 MLflow 이미지를 기반으로 한 [Dockerfile](Dockerfile) | 추적 서버 및 아티팩트 프록시 |
| `mlflow-db-provision` | [Compose](docker-compose.yml), PostgreSQL client 이미지 | 공유 [provisioning runner](../../04-data/operational/mng-db/pg/provision/run-feature-provision.sh)를 통해 [mng-pg.sql](provisioning/mng-pg.sql)을 실행 |

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며
[파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)은 드리프트 검증에 쓰입니다.

## Configuration

| Field | Value |
| --- | --- |
| Profiles | `mlops`, `data-science` (둘 다 의존성 클로저를 위해 `mng-pg`, `mng-pg-init`, SeaweedFS도 함께 선택) |
| Start order | `mng-pg` healthy → `mng-pg-init` → `mlflow-db-provision`; `seaweedfs-buckets` 완료; 그다음 `mlflow` |
| Network / port | `ai_net`, `edge_net`, `mng_data_net`, `object_net`; `expose`를 통한 내부 `${MLFLOW_PORT:-5000}`; 호스트 포트 없음 |
| Route | `gateway-standard-chain`, `sso-errors`, `sso-auth`를 사용하는 `https://mlflow.${DEFAULT_URL}` |
| Allowed hosts | `mlflow:*`, `mlflow.${DEFAULT_URL}`, `localhost:*`, `127.0.0.1:*` (DNS 리바인딩 방지) |
| Environment keys | `MLFLOW_PORT`, `MLFLOW_DB_USER`, `MLFLOW_DB_NAME`, `MLFLOW_ARTIFACT_BUCKET`, `MLFLOW_S3_ENDPOINT_URL`, `MLFLOW_S3_REGION`; admin 연결에는 `POSTGRES_DEFAULT_USER`, `POSTGRES_DEFAULT_DB` 사용 |
| Secrets | `mlflow_db_password` (PG-021), `seaweedfs_s3_mlflow_secret_key` (STRG-013); 프로비저닝 작업은 `mng_postgres_password`도 읽음 |
| Credential handling | 데이터베이스 비밀번호는 `PGPASSWORD`로, S3 시크릿은 `AWS_SECRET_ACCESS_KEY`로 libpq에 전달되며 둘 다 백엔드 URI나 argv에는 나타나지 않습니다 |
| Persistence | 컨테이너 자체에는 없음; 상태는 `mng-pg` 데이터베이스와 SeaweedFS 버킷에 있습니다 |
| Health | 내부 포트의 `GET /health`; 프로세스가 응답함을 증명할 뿐 DB/버킷 쓰기 접근은 증명하지 않습니다 |

SeaweedFS identity `mlflow`(액세스 키 ID `mlflow`)는 `mlflow-artifacts`만
읽기·쓰기·목록 조회할 수 있으며
([identities](../../04-data/lake-and-object/seaweedfs/config/s3-identities.conf)),
다른 버킷에는 접근할 수 없습니다.

## Validation

- `HYHOME_COMPOSE_PROFILES="mlops data-science" bash scripts/validation/validate-docker-compose.sh`
- `python3 -m unittest tests.validation.test_compose_baseline_gates` (정적 프로비저닝 계약)
- `HYHOME_PG_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.FeatureProvisioningRehearsalTests` (일회용 PostgreSQL 필요; Docker 필요)
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## How to Work in This Area

1. 프로필을 선택하기 전에 등록된 시크릿 워크플로우를 통해 `secrets/db/postgres/mlflow_password.txt`와
   `secrets/storage/seaweedfs_s3_mlflow_secret_key.txt`가 존재하는지 확인합니다.
2. 선택 사항을 정적으로 검증한 뒤, 소유자의 환경에서 승인된 대상으로만 시작합니다. 예:
   `docker compose --profile core --profile mlops up -d mlflow`.
3. SDK 클라이언트는 `MLFLOW_TRACKING_URI`를 가리키게 하고 브라우저 사용자는 게이트웨이 라우트를 사용합니다.
4. 기능별 SQL은 `provisioning/`에 유지하며 공유 `mng-pg-init` SQL에 MLflow 구문을 추가하지 않습니다.

## Related Documents

- **Guide**: MLflow usage guide (`docs/05.operations/guides/0088-mlflow.md`)
- **Policy**: MLflow operations policy (`docs/05.operations/policies/0088-mlflow.md`)
- **Runbook**: MLflow recovery runbook (`docs/05.operations/runbooks/0088-mlflow.md`)
- [Documentation index](../../../docs/README.md)
