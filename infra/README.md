# Hy-Home Infrastructure (infra/)

> Unified service definition and orchestration layer for the hy-home.docker ecosystem.

## Overview

The `infra/` directory manages the **Service Definitions** for the entire home server and AI development environment. It follows a strictly tiered architecture (01-11), where each service is isolated in its own subdirectory containing a `docker-compose.yml`. These definitions are aggregated into the root `docker-compose.yml` using the `include` feature, providing a modular yet unified infrastructure management experience.

## Audience

이 README의 주요 독자:

- **Operators**: Infrastructure deployment and service lifecycle management.
- **AI Agents**: System discovery, automated configuration, and scaling.
- **Developers**: Consuming infrastructure services for application development.

## Scope

### In Scope

- Service definitions across 11 functional tiers.
- Global orchestration via root `docker-compose.yml`.
- Inventory status for root-active, optional, standalone, and variant Compose files.
- Standardized execution models using **Docker Profiles** (`core`, `data`, `obs`, etc.).
- Resource optimization and security hardening templates.

### Out of Scope

- Detailed internal service configuration (see `docs/07.guides/` or sub-module READMEs).
- Application business logic and frontend source code.
- Credentials and sensitive variables (managed in `secrets/`).

## Infrastructure Tiers (01-11)

| Tier | Category | Key Services | Status |
| :--- | :--- | :--- | :--- |
| **01** | **Gateway** | [Traefik](01-gateway/traefik/), [Nginx](01-gateway/nginx/) | Production |
| **02** | **Identity** | [Keycloak](02-auth/keycloak/), [OAuth2-Proxy](02-auth/oauth2-proxy/) | Production |
| **03** | **Security** | [Vault](03-security/vault/) | Production |
| **04** | **Data** | [mng-db](04-data/operational/mng-db/), [MinIO](04-data/lake-and-object/minio/), [Qdrant](04-data/specialized/qdrant/) | Production |
| **05** | **Messaging** | [Kafka](05-messaging/kafka/), [RabbitMQ](05-messaging/rabbitmq/) | Production / Optional |
| **06** | **Observability** | [Grafana](06-observability/grafana/), [Prometheus](06-observability/prometheus/), [Loki](06-observability/loki/), [Tempo](06-observability/tempo/) | Production |
| **07** | **Workflow** | [Airflow](07-workflow/airflow/), [n8n](07-workflow/n8n/) | Production |
| **08** | **AI** | [Ollama](08-ai/ollama/), [Open WebUI](08-ai/open-webui/) | Production |
| **09** | **Tooling** | [SonarQube](09-tooling/sonarqube/), [Terrakube](09-tooling/terrakube/) | Dev/Ops |
| **10** | **Communication** | [Stalwart / MailHog](10-communication/mail/) | Optional |
| **11** | **Laboratory** | [Portainer](11-laboratory/portainer/), [Homer](11-laboratory/dashboard/) | Admin |

## Compose Inventory Snapshot

`infra/`에는 현재 47개의 `docker-compose*.yml` 파일과 40개의 Compose service directory가 있습니다. 루트 `docker-compose.yml`이 활성 include로 직접 묶는 파일은 14개이며, 나머지는 optional, standalone, 또는 variant로 분류합니다.

| Status | Meaning | Documentation Rule |
| --- | --- | --- |
| `root-active` | 루트 `include`에 주석 없이 포함된 Compose 파일 | 루트 실행면으로 문서화할 수 있음 |
| `root-commented-optional` | 루트 `include`에 주석 처리된 optional Compose 파일 | 보유 구성으로만 설명하고 기본 실행면으로 과장하지 않음 |
| `standalone-only` | `infra/`에 존재하지만 루트 include 목록에 없는 Compose 파일 | service README와 직접 실행 절차를 기준으로 설명 |
| `dev/cluster variant` | `.dev.yml`, `.cluster.yml`, v2 등 대체 실행 파일 | 대상 profile과 검증 범위를 함께 기록 |

현재 `root-active` 파일은 gateway/auth/security, MinIO, mng-db, Qdrant, Kafka dev, observability dev, n8n dev, Airflow dev, Dozzle, RedisInsight, Open Notebook으로 제한됩니다. 전체 보유 Compose 수와 root-active 수를 혼동하지 않습니다.

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| Orchestration | Docker Compose v2.20+ | Using `include` & `profiles` |
| Edge Router | Traefik v3.x | Dynamic service discovery |
| Identity | Keycloak / OIDC | Centralized IAM |
| Observability | LGTM Stack | Loki, Grafana, Tempo, Prometheus |

## Execution Model

`hy-home.docker`는 Docker Compose의 **Profiles** 기능을 사용하여 서비스 활성화를 제어합니다. 이를 통해 시스템 자원(Memory/CPU)을 효율적으로 관리할 수 있습니다.

### Service Profiles

`hy-home.docker`는 Docker Compose의 **Profiles**를 사용하여 환경별/목적별 서비스 그룹을 제어합니다.

- `profiles: [ "core" ]`: 필수 인프라 (Traefik, Keycloak, OAuth2 Proxy, Vault)
- `profiles: [ "dev" ]`: 루트 통합 개발 스택
- `profiles: [ "auth" ]`: 인증 계층
- `profiles: [ "security" ]`: Vault 보안 계층
- `profiles: [ "data" ]`: 범용 데이터 저장소 (Qdrant 등)
- `profiles: [ "mng" ]`: 시스템 관리용 DB 계층 (mng-db)
- `profiles: [ "storage" ]`: 오브젝트 및 파일 저장소 (MinIO)
- `profiles: [ "messaging" ]`: 핵심 메시징 브로커 (Kafka)
- `profiles: [ "obs" ]`: 모니터링 및 로기 (LGTM Stack)
- `profiles: [ "workflow" ]`: 워크플로우 엔진 (Airflow, n8n)
- `profiles: [ "ai" ]`: AI/LLM 엔진 및 Vector DB
- `profiles: [ "admin" ]`: 관리 대시보드 및 운영 보조 도구

## Getting Started

### 1. Prerequisites

- **Docker Engine** >= 24.0.0
- **Docker Compose** >= 2.20.0
- **NVIDIA Container Toolkit** (Optional, for AI GPU acceleration)
- **Secret Inventory**: Ensure `scripts/gen-secrets.sh` has been executed.

### 2. Integrated Execution (Standard)

기본 진입점은 저장소 루트의 `docker-compose.yml`입니다.

```bash
# 전체 필수 서비스 실행 (core 프로필)
docker compose --profile core up -d

# 특정 계층 통합 실행 (예: AI 계층)
docker compose --profile ai up -d
```

### 3. Standalone Verification

개별 폴더 내에서 독립적으로 서비스를 실행하고 검증할 수 있습니다.

```bash
cd infra/01-gateway/traefik
docker compose up -d
```

## Structure

```text
infra/
├── 01-gateway/        # Edge Routing & SSL Ingress
├── 02-auth/           # SSO, IAM, and OAuth2 Proxy
├── 03-security/       # Vault and Security Hardening
├── 04-data/           # Persistence (SQL, NoSQL, Object)
├── 05-messaging/      # Event Streaming (Kafka, RabbitMQ)
├── 06-observability/  # Monitoring, Logging, Tracing
├── 07-workflow/       # DAG Orchestration & Automation
├── 08-ai/             # LLM Inference & RAG Engines
├── 09-tooling/        # DevOps, QA & Performance Tools
├── 10-communication/  # Mail & Messaging Infrastructure
├── 11-laboratory/     # Experimental & Admin Dashboards
├── common-optimizations.yml # Shared Docker templates
└── README.md          # This file
```

## How to Work in This Area

1. **Service Addition**: `infra/<tier>/<service>/` 디렉토리를 생성하고 `docker-compose.yml`을 작성합니다.
2. **Global Integration**: 루트 `docker-compose.yml`의 `include`에 새 서비스를 추가할 때 `root-active`, `root-commented-optional`, `standalone-only`, `dev/cluster variant` 상태를 함께 갱신합니다.
3. **Configuration**: 환경 변수가 필요하면 루트 `.env.example`에 추가하고, 민감 값은 `secrets/`에 분리합니다.
4. **Validation**: `scripts/validate-docker-compose.sh`를 실행하여 구조적 정합성을 확인합니다.

## Related References

- [Official Guides](../docs/07.guides/README.md)
- [Operation Specs](../docs/08.operations/README.md)
- [Architecture Details](../docs/02.ard/README.md)
- [Secret Management](../secrets/README.md)
- [Root Compose](../docker-compose.yml)
- [Tech Stack Versions](tech-stack.versions.json)

## AI Agent Guidance

수정 전에 Agent는 다음을 수행해야 함:

1. 타겟 계층과 기존 서비스 패턴을 파악한다.
2. 새 서비스가 `common-optimizations.yml` 템플릿을 준수하는지 확인한다.
3. `[LOAD:SPEC]` 등 JIT 마커를 사용하여 상세 컨텍스트를 확보한다.
4. 이 README의 "Infrastructure Tiers" 테이블을 업데이트하여 추적성을 유지한다.

---
*Maintained by the hy-home.docker Platform Team*
