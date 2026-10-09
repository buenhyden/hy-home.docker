---
title: "Airflow Usage Guide"
version: "1.1.4"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "GDE-0050"
parent_ids:
- "POL-0050"
implementation_services:
  infra/07-workflow/airflow/docker-compose.yml:
  - airflow-apiserver
  - airflow-dag-processor
  - airflow-init
  - airflow-scheduler
  - airflow-statsd-exporter
  - airflow-triggerer
  - airflow-valkey
  - airflow-valkey-exporter
  - airflow-worker
  - flower
created: "2026-05-10"
---

# Airflow Usage Guide

## Overview

이 문서는 `hy-home.docker` 플랫폼의 Apache Airflow 시스템에 대한 가이드다. 현재 구현은 Airflow, `airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`, `flower`, `airflow-statsd-exporter`를 기준으로 한다.

## Audience and Goal

**대상**

- **Developers**: DAG 개발 및 시스템 통합
- **Operators**: 서버 상태 모니터링 및 리소스 관리
- **AI Agents**: 자동화된 스케줄링 환경 분석

**목적**

- Airflow 분산 아키텍처 (CeleryExecutor) 이해
- 웹 UI 및 모니터링 도구 접근 방법 확인
- 기본 개발 환경 설정 및 검증 절차 습득

## Usage

`airflow-valkey-exporter`는 별도로 선택한 Airflow 전용 broker의 관측기다. HOME 관리 broker는 자체 exporter를 사용하며 exporter health로 broker readiness를 대신하지 않는다.

### 사전 조건

- **Docker/Compose**: 로컬 실행 환경
- **Secrets**: `airflow_keycloak_client_secret`, `airflow_api_jwt_secret` 등 서비스 접근 권한
- **Network**: `airflow_net` 외부 통신 가능 상태

### 사용 절차

#### 현재 구현 변경사항

- Airflow는 [Dockerfile](../../../infra/07-workflow/airflow/Dockerfile)에 선언된 upstream base와 Python constraints로 Keycloak provider를 포함한 로컬 이미지를 빌드한다. 실행 image tag는 [Compose](../../../infra/07-workflow/airflow/docker-compose.yml)에서 확인한다.
- 인증 manager는
 `airflow.providers.keycloak.auth_manager.keycloak_auth_manager.KeycloakAuthManager`다.
 `AIRFLOW_KEYCLOAK_CLIENT_ID`, `KEYCLOAK_REALM`, `KEYCLOAK_URL`은 환경 설정으로,
 client secret은 `airflow_keycloak_client_secret` Docker Secret으로 전달한다.
- API server는 시작 전에 시스템 CA와 `${DEFAULT_CERT_DIR}/rootCA.pem`을 합쳐
 임시 CA bundle을 만들고 `airflow api-server --proxy-headers`로 실행한다.
 Forwarded header 신뢰 범위는 Traefik 고정 주소 `10.250.1.2`(`edge_net`)로 제한한다.
- 기본 Celery broker는 `mng-valkey`다. `dedicated-valkey` profile은
  `airflow-valkey`와 exporter를 **기동만** 한다. 전용 broker를 실제로 쓰려면
  `AIRFLOW_VALKEY_HOST=airflow-valkey`와
  `AIRFLOW_VALKEY_SECRET=airflow_valkey_password`를 함께 설정해야 한다.

#### 시스템 아키텍처 이해

Airflow는 다음과 같은 분산 컴포넌트로 구성됩니다:

- **Scheduler & DAG Processor**: 작업 예약 및 DAG 파일 해석 (독립 실행으로 안정성 확보)
- **Celery Workers**: 실제 태스크가 실행되는 동적 확장 노드
- **Valkey Broker**: 스케줄러와 워커 간의 메시지 교환. compose 파일은 `infra/07-workflow/airflow/docker-compose.yml` 하나다. `${AIRFLOW_VALKEY_HOST:-mng-valkey}`와 `${AIRFLOW_VALKEY_SECRET:-mng_valkey_password}`가 실제 선택을 결정하며, `dedicated-valkey` profile만 추가해도 이 두 기본값은 바뀌지 않는다.
- **API Server**: UI 및 외부 통합을 위한 `airflow-apiserver` 엔드포인트

로그인 흐름은 `airflow.${DEFAULT_URL}`에서 Traefik HTTPS route를 거쳐
Keycloak auth manager가 처리한다. Keycloak client secret이나 JWT secret을
로그, Compose 출력, DAG 코드에 기록하지 않는다.

#### UI 접근 및 모니터링

- **Main UI**: `https://airflow.${DEFAULT_URL}` (작업 모니터링, 로그 확인)
- **Flower Dashboard**: `https://flower.${DEFAULT_URL}` (Celery 워커 부하 상태 확인)
- **Metrics**: Prometheus/Grafana를 통해 StatsD 지표 확인 가능

#### 개발 환경 검증

새로운 DAG를 추가하기 전에 다음 명령으로 시스템 상태를 확인합니다:

```bash

# workflow root compose static validation
HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh

# DAG 목록 로드 확인
docker compose exec airflow-apiserver airflow dags list
```

### Service readiness and build selection

로컬 Airflow build를 공유하는 서비스는 `airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`, `airflow-init`, `flower` 7개다. 별도 이미지인 `airflow-statsd-exporter`와 함께 HOME 8개를 구성한다.

| Identity | 정상 역할과 기대 신호 | 상태·준비 상태의 한계 |
| --- | --- | --- |
| `airflow-apiserver` | UI/API와 Keycloak 네이티브 로그인, `/api/v2/monitor/health`의 구성 요소별 JSON 상태 | HTTP 200은 상태 조회의 성공만 뜻하므로 응답 본문의 DB·scheduler 상태를 확인한다. |
| `airflow-scheduler` | DAG 실행 예약과 선언된 scheduler 상태 서버 | heartbeat만으로 worker의 작업 실행을 입증할 수 없다. |
| `airflow-dag-processor` | 마운트한 DAG 파싱과 `DagProcessorJob` 점검 | 파싱 성공, 예약 처리, 작업의 외부 효과를 구분한다. |
| `airflow-worker` | Celery 작업 실행과 선언된 Celery ping | 공유 로그·DB 메타데이터를 큐·작업 상태와 대조한다. |
| `airflow-triggerer` | 지연 작업 재개와 `TriggererJob` 점검 | 정상 상태여도 대기 중인 외부 이벤트가 완료된 것은 아니다. |
| `airflow-init` | 마이그레이션 가능한 일회성 초기화와 종료 코드 | root로 디렉터리를 만들지만 소유권은 바꾸지 않는다. HTTP 점검이나 사용자 역할 부여는 없고, 자원 점검은 용량을 강제하지 않고 경고한다. |
| `flower` | 프록시 SSO로 보호한 Celery 모니터링 UI와 HTTP 상태 | 모니터링 가용성은 worker 상태와 다르며 독립적인 워크플로 원본 백업을 소유하지 않는다. |
| `airflow-statsd-exporter` | 추적되는 매핑으로 StatsD 이벤트를 수집 지표로 변환 | Compose healthcheck가 없으며 이벤트 지표는 해당 이벤트가 있어야 생긴다. 매핑은 보존 대상이지만 지표 캐시는 워크플로 이력이 아니다. |
| `airflow-valkey` | 일치하는 호스트·secret 쌍을 선택했을 때 쓰는 OPTIONAL 전용 broker와 인증된 PONG | 기본값은 공유 `mng-valkey`다. 큐의 영속 상태만으로 정확한 재실행 여부를 판단하지 않는다. |
| `airflow-valkey-exporter` | OPTIONAL broker 지표와 exporter HTTP 점검 | exporter 상태만으로 broker 인증이나 큐 준비 상태를 입증하지 않는다. 원본 데이터 백업은 소유하지 않는다. |

Build context는 저장소 root이고 linked Dockerfile·Compose args를 사용하며 target은 없다. Compose가 서로 다른 base/stage 기본값을 덮어쓴다. `PYTHON_VERSION`은 constraints 파일만 선택하고 interpreter를 고정하지 않는다. Dockerfile은 constraints 기반 의존성과 고정 Keycloak provider를 설치하고 로컬 COPY 없이 upstream entrypoint/CMD를 상속한다. 서비스별 command를 쓰되 init은 entrypoint를 바꾼다. Dockerfile 기본값만 쓰는 직접 build는 Compose build와 달라 별도 조정이 필요하다. 정확한 pin은 소스가 소유한다.

Init 전에 소유자 절차로 host DAG/log/plugin/config의 runtime UID 권한, CA, DB/role과 선택 broker를 준비한다. 공유 DB/broker readiness는 Compose가 보장하지 않는다. Keycloak permission bootstrap은 사용자 역할을 부여하지 않으므로 따로 확인한다. Airflow는 native SSO와 표준 gateway chain을 사용하고 proxy SSO 추가는 이중 인증이 된다. Flower는 proxy SSO를 유지한다.

### Source-backed operating contract

- **Purpose/classification**: Airflow 코어 8개 서비스는 owner-confirmed `HOME` orchestration capability다. `airflow-valkey`와 exporter는 shared broker를 분리할 때만 쓰는 `OPTIONAL` pair다.
- **Profiles/source**: 코어는 `workflow`/`workflow-airflow`, 전용 broker pair는 `dedicated-valkey`; authoritative source는 [Compose](../../../infra/07-workflow/airflow/docker-compose.yml)와 [Dockerfile](../../../infra/07-workflow/airflow/Dockerfile)이다.
- **상태 흐름**: DAG는 `dags` mount를 통해 들어온다. scheduler/processor는 PostgreSQL database `airflow`에 기준이 되는 metadata를 영속 저장하며 이 database는 `mng-pg`에 있다. Celery message는 선택된 Valkey를 거치며 worker는 task log를 `airflow-logs`에 쓴다. queue 내용은 처리 중인 작업을 조율하는 상태이며 영속 workflow 기록이 아니다.
- **secret·환경 설정**: `airflow_db_password`, `airflow_fernet_key`, `airflow_api_jwt_secret`, `airflow_keycloak_client_secret`과 선택된 broker password를 보존한다. `AIRFLOW_VALKEY_HOST`와 `AIRFLOW_VALKEY_SECRET`은 같은 broker를 선택해야 한다. Fernet key는 암호화된 Connections와 분리하여 복구할 수 없다.
- **의존성·보안**: `mng-pg`, 선택된 Valkey, Keycloak, Traefik, root CA와 `airflow_net`이 준비되어야 한다. native Keycloak Auth Manager가 Airflow UI를 보호하고 Flower는 gateway auth chain을 사용한다. 내부 scheduler, worker, broker 또는 database port를 노출하지 않는다.
- **영속성·자원**: PostgreSQL metadata와 `airflow-dags`, `airflow-logs`, `airflow-plugins`, `airflow-config`가 복구 세트를 이룬다. Compose CPU/memory 값은 source limit이며 측정된 여유 용량이 아니다. 관찰된 scheduler/worker/DB/broker 부하를 근거로만 규모를 조정한다.
- **정상 사용·수명 주기**: 저장소 root에서 `docker compose --profile workflow config --quiet`를 사용한 뒤, 대상별 기동과 upgrade는 [RUN-0050](../runbooks/0050-airflow.md)을 따른다. workflow 전체를 시작하면 n8n과 migration을 수행할 수 있는 초기화도 실행될 수 있다. pause/drain, 일관된 DB/artifact/key backup, migration, canary와 재개 결정은 Runbook이 소유한다.
- **공식 문서·license**: [Airflow database 설정](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html), [Connections/Fernet 지침](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html), [권장 운영 방식](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)을 따른다. Apache Airflow에는 Apache-2.0 license가 적용된다.

### Common Checks

- `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 07-workflow`
- Runtime이 실행 중이면 `docker compose exec airflow-apiserver airflow dags list`

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0050-airflow.md)을 따른다.

### Traceability

- Declared parent: [Airflow Operations Policy](../policies/0050-airflow.md) (`POL-0050`)
- Governing authority: [Workflow Tier (07-workflow) Architecture Description](../../02.architecture/descriptions/0007-workflow-architecture.md) (`AD-0007`)
- Subject peers: [Policy](../policies/0050-airflow.md) (`POL-0050`), [Runbook](../runbooks/0050-airflow.md) (`RUN-0050`)

## Troubleshooting

- guide에 policy control이나 복구 절차를 직접 섞어 목적 프로파일을 흐리는 경우
- target-relative link를 템플릿 위치 기준으로 계산하는 경우
- 검증 명령 실행 결과 없이 운영 가능 상태를 단정하는 경우

- **Scheduler Heavy Load**: DAG 파일 내에서 DB 쿼리나 파일 시스템 접근을 직접 수행하면 스케줄러 성능이 저하됩니다.
- **Worker Timeout**: 리소스 부족으로 워커가 종료되면 태스크가 `Queued` 상태로 멈출 수 있습니다.
- **XCom Abuse**: XCom은 작은 데이터 교환용입니다. 대용량 데이터는 S3(SeaweedFS) 등 외부 저장소를 사용하십시오.

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0050-airflow.md)
- [Recovery runbook](../runbooks/0050-airflow.md)
