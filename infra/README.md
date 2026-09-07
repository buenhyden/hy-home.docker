---
title: "Infrastructure Surface"
version: "1.0.1"
type: "common/repository-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
created: "2025-11-24"
---

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
- Compose file inventory, and the profile that selects each service.
- Standardized execution models using **Docker Profiles** (`core`, `data`, `obs`, etc.).
- Resource optimization and security hardening templates.

### Out of Scope

- Detailed internal service configuration (see `docs/05.operations/` or sub-module READMEs).
- Application business logic and frontend source code.
- Credentials and sensitive variables (managed in `secrets/`).

## Infrastructure Tiers (01-11)

| Tier | Category | Key Services | Status |
| :--- | :--- | :--- | :--- |
| **01** | **Gateway** | [Traefik](./01-gateway/traefik), [Nginx](./01-gateway/nginx) | Production |
| **02** | **Identity** | [Keycloak](./02-auth/keycloak), [OAuth2-Proxy](./02-auth/oauth2-proxy) | Production |
| **03** | **Security** | [Vault](./03-security/vault) | Production |
| **04** | **Data** | [mng-db](./04-data/operational/mng-db), [MinIO](./04-data/lake-and-object/minio), [Qdrant](./04-data/specialized/qdrant) | Production |
| **05** | **Messaging** | [Kafka](./05-messaging/kafka), [RabbitMQ](./05-messaging/rabbitmq) | Production / Optional |
| **06** | **Observability** | [Grafana](./06-observability/grafana), [Prometheus](./06-observability/prometheus), [Loki](./06-observability/loki), [Tempo](./06-observability/tempo) | Production |
| **07** | **Workflow** | [Airflow](./07-workflow/airflow), [n8n](./07-workflow/n8n) | Production |
| **08** | **AI** | [Ollama](./08-ai/ollama), [Open WebUI](./08-ai/open-webui) | Production |
| **09** | **Tooling** | [SonarQube](./09-tooling/sonarqube), [Terrakube](./09-tooling/terrakube) | Dev/Ops |
| **10** | **Communication** | [Stalwart / MailHog](./10-communication/mail) | Optional |
| **11** | **Laboratory** | [Portainer](./11-laboratory/portainer), [Homer](./11-laboratory/dashboard) | Admin |

## Compose Inventory Snapshot

`infra/`에는 41개의 Compose 파일이 있습니다. 이 중 40개는 `docker-compose*.yml`이고 1개는 MinIO cluster variant인 `docker-compose.cluster.yaml`입니다. Compose service directory는 40개입니다. 루트 `docker-compose.yml`은 이 41개를 모두 주석 없이 `include`합니다.

파일 목록은 무엇이 기동되는지를 결정하지 않습니다. `include:`는 파일을 무조건 병합하고, 선택한 profile이 어떤 서비스가 resolve되는지를 결정합니다. profile 이름의 canonical 정의는 [Compose Profile Vocabulary Policy](../docs/05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md)가 소유합니다.

| Fact | Value | Documentation Rule |
| --- | --- | --- |
| Compose 파일 | 41 | 파일 존재가 곧 기동을 뜻하지 않음 |
| Service directory | 40 | MinIO leaf만 파일 2개를 보유 |
| 루트 `include` 항목 | 41 | 주석 처리된 include 항목은 없음 |
| 활성화 결정자 | 선택한 profile | 서비스 설명은 그 서비스의 `profiles:` 값을 근거로 작성 |
| Template security baseline 검사 대상 | 40 (`.yml`만) | `docker-compose.cluster.yaml`은 그 검사에서만 제외되며, 루트 include에서는 제외되지 않음 |

profile을 하나도 선택하지 않으면 어떤 서비스도 resolve되지 않습니다. 서비스를 "루트에 포함되었다"는 이유로 기본 실행면으로 서술하지 않고, 그 서비스를 선택하는 profile 이름을 함께 적습니다.

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
- `profiles: [ "messaging" ]`: 메시징 브로커 (Kafka, RabbitMQ)
- `profiles: [ "messaging-option" ]`: RabbitMQ 단독/호환 profile alias
- `profiles: [ "obs" ]`: 모니터링 및 로기 (LGTM Stack)
- `profiles: [ "workflow" ]`: 워크플로우 엔진 (Airflow, n8n)
- `profiles: [ "ai" ]`: AI/LLM 엔진 및 Vector DB
- `profiles: [ "admin" ]`: 관리 대시보드 및 운영 보조 도구

## Getting Started

### 1. Prerequisites

- **Docker Engine** >= 24.0.0
- **Docker Compose** >= 2.20.0
- **NVIDIA Container Toolkit** (Optional, for AI GPU acceleration)
- **Secret Inventory**: Ensure `scripts/operations/gen-secrets.sh` has been executed.

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

## Service Documentation Rubric

Each service README must stay aligned with the Compose/config files in the same
service directory and cover the following agent-verifiable fields:

| Field | Required evidence |
| :--- | :--- |
| Purpose | Service role, tier, and the profiles that select its services |
| Config files | Local `docker-compose*.yml`, Dockerfile, scripts, and mounted config paths |
| Config values | Non-secret environment keys and defaults that affect operation |
| Compose linkage | Root include/profile status and any variant compose files |
| Networks | Declared networks and intended trust boundary |
| Volumes | Persistent data, bind mounts, and backup-relevant paths |
| Ports | Internal and exposed ports with protocol notes |
| Labels | Traefik, routing, observability, or policy labels |
| Secret refs | Secret names and mounted paths only; never secret values |
| Healthcheck | Health endpoint or explicit reason when not applicable |
| Operations | Canonical guide, policy, runbook, or service README reference |
| Validation | Relevant compose, hardening, and repo-contract checks |
| Troubleshooting | Known failure modes and first diagnostic command |

## How to Work in This Area

1. **Service Addition**: `infra/<tier>/<service>/` 디렉토리를 생성하고 `docker-compose.yml`을 작성합니다.
2. **Global Integration**: 새 서비스 compose 파일은 루트 `docker-compose.yml`의 `include`에 주석 없이 추가하고, 각 서비스에 `profiles:`를 선언한 뒤 그 이름을 POL-0078에 등록합니다.
3. **Configuration**: 환경 변수가 필요하면 루트 `.env.example`에 추가하고, 민감 값은 `secrets/`에 분리합니다.
4. **Validation**: `scripts/validation/validate-docker-compose.sh`를 실행하여 구조적 정합성을 확인합니다.

공유 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../.agents/governance/agentic.md)와 [documentation protocol](../.agents/governance/documentation-protocol.md)로 라우팅한다.

1. 타겟 계층과 기존 서비스 패턴을 파악한다.
2. 새 서비스가 `common-optimizations.yml` 템플릿을 준수하는지 확인한다.
3. 상세 컨텍스트는 [bootstrap 정규 로드 순서](../.agents/governance/bootstrap.md#canonical-load-order)에 따라 요청에 필요한 문서만 해석한다.
4. 이 README의 "Infrastructure Tiers" 테이블을 업데이트하여 추적성을 유지한다.

## Related Documents

- [Official Guides](../docs/05.operations/README.md)
- [Operation Specs](../docs/05.operations/README.md)
- [Architecture Details](../docs/02.architecture/descriptions/README.md)
- [Secret Management](../secrets/README.md)
- [Root Compose](../docker-compose.yml)
- [Tech Stack Versions](./tech-stack.versions.json)
