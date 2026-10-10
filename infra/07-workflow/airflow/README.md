---
title: "Airflow (07-workflow)"
version: "1.2.5"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
created: "2025-11-12"
---

# Airflow (07-workflow)

> Apache Airflow + CeleryExecutor + 네이티브 Keycloak Auth Manager입니다.

## Overview

Airflow는 `hy-home.docker`의 code-first 워크플로우 오케스트레이션 엔진입니다.
Compose 파일 하나에서 핵심 서비스와 선택적인 전용 Valkey를 구성합니다.

UI/API 인증은 OAuth2 Proxy ForwardAuth가 아니라
`KeycloakAuthManager`를 통해 Keycloak에 직접 연결합니다.

## Audience

- Data Engineers
- SREs
- AI Agents

## Scope

### In Scope

- apiserver
- scheduler
- dag-processor
- worker
- triggerer
- Flower
- StatsD
- DB/broker/auth wiring

### Out of Scope

- 개별 DAG 비즈니스 로직
- 외부 소스 인프라

## Structure

```text
airflow/
├── Dockerfile
├── docker-compose.yml
├── config/
└── README.md
```

## Current Implementation Notes

- base: [Dockerfile declaration](Dockerfile)
- image: [declared runtime image](../../tech-stack.versions.json)
- Python 선택: [Dockerfile](Dockerfile)의 `PYTHON_VERSION`은 base image의 `-python` variant와 constraints를 함께 선택합니다. 빌드에서 interpreter·core·provider의 실제 버전과 `pip check`를 검사합니다.
- provider: `apache-airflow-providers-keycloak`, [Dockerfile](Dockerfile)에 고정됨
- auth manager:
  `airflow.providers.keycloak.auth_manager.keycloak_auth_manager.KeycloakAuthManager`
- client: `home-airflow`
- realm: `hy-home.realm`
- client secret: Docker Secret
- Airflow internal JWT secret: Docker Secret
- API base URL: `https://airflow.${DEFAULT_URL}`
- local CA: certifi + 마운트된 mkcert root
- API server: `--proxy-headers`
- trusted proxy: [docker-compose.yml](docker-compose.yml)의 `FORWARDED_ALLOW_IPS`에 선언됨 (`edge_net`)
- Airflow route:
  `traefik.http.routers.airflow.middlewares: gateway-standard-chain@file`
- OAuth2 Proxy ForwardAuth: **Airflow에는 적용되지 않음**

### Token Boundary

Keycloak token:

- OIDC login
- Authorization Services

Airflow internal JWT:

- application session/API
- `airflow_api_jwt_secret`

두 토큰은 별개입니다.

## Service Readiness

| Field | Evidence |
| --- | --- |
| API | `airflow-apiserver` |
| Auth | Keycloak Auth Manager |
| DB | `mng-pg` |
| Broker | `mng-valkey` or `airflow-valkey` |
| Secret | DB/Fernet/JWT/Keycloak client |
| Health | `/api/v2/monitor/health` |

### SEC01 업데이트 검증 경계

2026-10-10 공식 [Airflow release](https://github.com/apache/airflow/releases/tag/3.3.2)와 <!-- runtime-version-exception: compatibility — immutable source evidence reference; Compose/Dockerfile owns the deployment pin -->
[Keycloak provider PyPI](https://pypi.org/project/apache-airflow-providers-keycloak/0.11.0/)를 조회했습니다. <!-- runtime-version-exception: compatibility — immutable source evidence reference; Compose/Dockerfile owns the deployment pin -->
Compose의 모든 Airflow role은 같은 core·Python·provider build args와 로컬 이미지 태그를 사용합니다.
base의 OCI index digest는 Dockerfile이 소유하며 실제 배포 digest와 구별합니다.

[보존된 upstream constraints](constraints-upstream-3.3.2-python3.13.txt)는 <!-- runtime-version-exception: compatibility — immutable source evidence reference; Compose/Dockerfile owns the deployment pin -->
[공식 Python constraints](https://raw.githubusercontent.com/apache/airflow/constraints-3.3.2/constraints-3.13.txt)의 <!-- runtime-version-exception: compatibility — immutable source evidence reference; Compose/Dockerfile owns the deployment pin -->
원문입니다. upstream Keycloak·common-compat·Celery pin과 최신 직접 provider의 차이는 Dockerfile에 명시한 overlay로 해결합니다.
다른 pin은 보존하며 의존성을 정상 해석합니다. resolver나 `pip check` 실패는 업데이트 장애입니다.
런타임 `_PIP_ADDITIONAL_REQUIREMENTS`를 Compose에서 전달하지 않습니다. 추가 의존성은 이미지에서 검증해야 합니다.

UNIT의 build-input 정합 시험과 ISOLATED 후보 빌드를 HOME 적용 성공으로 해석하지 않습니다.
HOME cookie/bearer·logout·Keycloak 권한 이행·Celery 취소·scheduler fork/OTel·중립 DAG 실행은 NOT_RUN입니다.
현재 OTel 제한은 기존 장애 완화로 유지하며 수정 완료로 기록하지 않습니다.
SEC01 담당자는 2026-10-17까지 이 항목을 다음 검증 대상으로 확인해야 합니다.

HOME 전환 전 MNG DB, DAG·plugin·config, Fernet/JWT와 독립 복구 경계의 백업을 확인하고
후보 이미지에서 DB migration을 시험합니다. rollback은 사전 DB/파일 백업을 이전 검증 이미지의
빈 환경에 복원하는 절차이며 이미지 태그만 낮추는 방식은 허용하지 않습니다.
15분 중단 한도와 실제 복원은 NOT_RUN이고 총괄 통합 순서 확인 후 수행합니다.

이번 후보 검증은 `HYHOME_WORKFLOW_REHEARSAL=1 python3 -m unittest
tests.validation.test_workflow_version_bundle`로 수행했습니다. 2026-10-10 UNIT 5건과
ISOLATED 3건이 PASS(EXIT 0)였습니다. 시험 입력은 위 소스·Compose·constraints·두 n8n
Dockerfile·n8n Compose·시험 파일의 경로순 내용 SHA-256
`26e926e1bb82fd085ef1a6844b7d967315f5e76206cd36c79d8fca22556a73cf`입니다.

Airflow 후보를 네트워크·호스트 mount 없이 실행해 실제 interpreter/core/direct provider,
`pip check`, auth manager/Celery import를 확인했습니다. 다른 client의 credential grant와
기본 비활성인 JWT federation client를 거부하는 검사는 설치한 provider에서 수행했지만
exchange와 crypto는 mock을 사용했습니다. 실제 Keycloak login·token 검증으로 기록하지 않습니다.
linux/amd64 후보 manifest는
`sha256:c9096805e76159e0b18d55a5e357b1958894c291ebf88e9af2a497de208f227e`이고
서명·SBOM·scan·HOME rollout·DB 복원은 NOT_RUN입니다.

독립 검토 후 후보 실행 경계를 보완했습니다. 변경된 digest·다른 architecture·다른 OS는
container 생성 전에 거부합니다. native 시험은 mutable tag로 실행하지 않고 기록한 로컬
OCI index를 `--platform linux/amd64`로 inspect하여 위 platform manifest와 OS/architecture를
대조한 다음 같은 immutable index를 `--pull never`로 실행합니다. index와 platform manifest는
서로 다른 식별자입니다. 보완 후 같은 opt-in 명령은 8건 PASS(EXIT 0, 40.474초)였습니다.

Dockerfile lint에서 pipeline shell의 명시 선언 누락을 확인해 upstream의
`/bin/bash`와 `pipefail`·`errexit`·`nounset`·`nolog` 옵션을 그대로 선언했습니다.
이 변경으로 Airflow 후보를 다시 빌드하고 새 immutable OCI index
`sha256:8c139dddc7fcb484970340045848ae9f4d8d09f5b5444762e96f5b80504886f2`가
선택하는 위 manifest에서 전체 8건을 새로 실행했습니다. 이전 후보의 시험 결과나 scan을
새 digest의 증거로 재사용하지 않습니다. 새 digest의 서명·SBOM·scan은 NOT_RUN입니다.

## Keycloak Bootstrap

Required realm roles:

```text
Viewer
User
Op
Admin
SuperAdmin
```

```bash
docker compose exec airflow-apiserver   airflow keycloak-auth-manager create-all     --username keycloak_admin     --user-realm master     --password
```

기존 non-team 구성에서 provider 0.9.0으로 업그레이드한 이후: <!-- runtime-version-exception: migration — permission migration is required when crossing this provider boundary -->

```bash
docker compose exec airflow-apiserver   airflow keycloak-auth-manager create-permissions     --username keycloak_admin     --user-realm master     --password
```

## Usage

1. Airflow guide/policy/runbook 확인.
2. DAG lifecycle guide 확인.
3. auth route는 gateway-only 유지.
4. secret 원문을 로그/문서에 기록하지 않는다.
5. provider upgrade 시 Keycloak permission migration 검토.
6. failure는 endpoint matrix로 authentication vs authorization을 구분.

## Tech Stack

| Category | Technology | Version |
| --- | --- | --- |
| Airflow | Apache Airflow | declared version |
| Keycloak Provider | apache-airflow-providers-keycloak | declared version |
| Executor | CeleryExecutor | 분산 실행 |
| Broker | Valkey | 공유/전용 |
| DB | PostgreSQL | 관리용 DB |

## Available Scripts

```bash
HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 07-workflow
docker compose exec airflow-apiserver airflow db check
docker compose exec airflow-apiserver airflow dags list
```

## Troubleshooting

- config PermissionError -> 공유 볼륨 소유자/런타임 UID 확인
- DB migration -> 동일 이미지에서 `airflow db migrate` 실행
- JWT alg/format -> ForwardAuth 토큰 충돌 확인
- `invalid_scope` -> Keycloak Authorization bootstrap 확인
- role 404 -> 필수 realm role 확인
- callback 403 -> `_oauth_state` 확인
- Pool/DAG/Asset only 403 -> 리소스 authorization 확인

### Convergence contract

- Airflow core/Flower/StatsD 서비스는 `workflow`/`workflow-airflow`에서 **HOME**이며 Airflow Valkey와 그 exporter는 `dedicated-valkey`에서 **OPTIONAL**입니다.
- Root preflight: `docker compose --profile workflow config --quiet`. Root start: `docker compose --profile workflow up -d airflow-apiserver airflow-scheduler airflow-dag-processor airflow-worker airflow-triggerer flower airflow-statsd-exporter`.
- `dedicated-valkey`는 해당 쌍만 시작합니다. 실제로 선택하려면 `AIRFLOW_VALKEY_HOST`와 `AIRFLOW_VALKEY_SECRET`을 함께 일치시켜야 합니다.
- 안정적인 진입점: [docs/README.md](../../../docs/README.md). 정확한 Stage 05 경로: `docs/05.operations/guides/0050-airflow.md`; ID: `GDE-0050`, `POL-0050`, `RUN-0050`. 격리 복구는 계획되어 있으나 아직 실행되지 않았습니다.

## Related Documents

- **Architecture**: `docs/02.architecture/descriptions/0007-workflow-architecture.md`
- **Guide**: `docs/05.operations/guides/0050-airflow.md`
- **Policy**: `docs/05.operations/policies/0050-airflow.md`
- **Runbook**: `docs/05.operations/runbooks/0050-airflow.md`
- **Auth Integration**: `docs/05.operations/guides/0079-application-auth-integration.md`
- **Incident**: `docs/05.operations/incidents/2026/inc-0002-airflow-keycloak-native-auth/incident.md`

런타임 고정 값은 Compose/Dockerfile 선언이 소유하고 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)으로 드리프트를 검증합니다.
