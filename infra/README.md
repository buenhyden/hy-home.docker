---
title: "Infrastructure Surface"
version: "1.3.0"
type: "common/repository-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
created: "2025-11-24"
---

# Hy-Home Infrastructure (infra/)

> Unified service definition and orchestration layer for the hy-home.docker ecosystem.

## Overview

The `infra/` directory manages the **Service Definitions** for the entire home server and AI development environment. Tier and component directories own Compose declarations, build sources and mounted configuration. Root `docker-compose.yml` aggregates the registered fragments with `include`; some fragments own multiple services. Directory organization and profiles do not establish runtime isolation.

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
- Standardized execution models using **Docker Profiles** (`core`, `mng`, `obs`, etc.).
- Resource optimization and security hardening templates.

### Out of Scope

- Detailed internal service configuration (see `docs/05.operations/` or sub-module READMEs).
- Application business logic and frontend source code.
- Credentials and sensitive variables (managed in `secrets/`).

## Infrastructure Tiers (01-11)

| Tier | Category | Key Services | Status |
| :--- | :--- | :--- | :--- |
| **01** | **Gateway** | [Traefik](./01-gateway/traefik), [Nginx](./01-gateway/nginx) | HOME / optional; see disposition |
| **02** | **Identity** | [Keycloak](./02-auth/keycloak), [OAuth2-Proxy](./02-auth/oauth2-proxy) | HOME / optional; see disposition |
| **03** | **Security** | [OpenBao](./03-security/openbao) | HOME bootstrap; Vault is legacy migration |
| **04** | **Data** | [mng-db](./04-data/operational/mng-db), [MinIO](./04-data/lake-and-object/minio), [Qdrant](./04-data/specialized/qdrant) | HOME / optional; see disposition |
| **05** | **Messaging** | [Kafka](./05-messaging/kafka) | Optional; cluster is LAB |
| **06** | **Observability** | [Grafana](./06-observability/grafana), [Prometheus](./06-observability/prometheus), [Loki](./06-observability/loki), [Tempo](./06-observability/tempo) | HOME / optional; see disposition |
| **07** | **Workflow** | [Airflow](./07-workflow/airflow), [n8n](./07-workflow/n8n) | HOME / optional; see disposition |
| **08** | **AI** | [Ollama](./08-ai/ollama), [Open WebUI](./08-ai/open-webui), [ComfyUI](./08-ai/comfyui) | HOME |
| **09** | **Tooling** | [SonarQube](./09-tooling/sonarqube), [Terrakube](./09-tooling/terrakube) | Dev/Ops |
| **10** | **Communication** | [Mailpit](./10-communication/mailpit), [Stalwart](./10-communication/stalwart) | DEV / optional |
| **11** | **Laboratory** | [Dozzle](./11-laboratory/dozzle), [RedisInsight](./11-laboratory/redisinsight), [Open Notebook](./11-laboratory/open-notebook) | Admin |

## Compose Inventory Snapshot

루트 [Compose](../docker-compose.yml)의 `include`가 파일 목록을, 각 서비스의
`profiles`가 활성화 범위를 소유한다. 파일 수와 서비스 수를 문서 상수로
관리하지 않는다. `common-optimizations.yml`의 상속 자원 제한과 보안 설정도
최종 모델에 포함된다. profile 미선택은 전체 스택 시작을 의미하지 않는다.

```bash
# 공개 예제만 사용해 이름을 조회한다. 실제 .env의 전체 config는 출력하지 않는다.
docker compose --env-file .env.example config --profiles
docker compose --env-file .env.example --profile '*' config --services
```

프로파일 어휘와 목적은 POL-0078이 소유한다. [문서 인덱스](../docs/README.md)에서
Compose Profile Vocabulary Policy로 이동한다. Canonical path는
`docs/05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md`다. 전수 분류와 관측 일자는 Stage 90의
기존 local Docker service consolidation 연구에 기록한다.

## Tech Stack

실행 version pin의 원본은 각 Compose/Dockerfile 선언이다.
[version projection](tech-stack.versions.json)은 tracked Compose image 선언에서
파생한 기계 판독 projection이며, drift 검사와 업데이트 소유권 탐색에 사용한다.
Dockerfile `FROM`/`ARG`와 inline build의 pin은 별도 build authority이므로 이
projection이 그것들의 완전한 목록이라고 주장하지 않는다. README에는 source link
없이 exact patch literal을 복제하지 않는다.

| Category | Technology | Notes |
| :--- | :--- | :--- |
| Orchestration | Docker Compose | `include` and explicit `profiles` |
| Edge Router | Traefik v3.x | Dynamic service discovery |
| Identity | Keycloak / OIDC | Centralized IAM |
| Observability | LGTM Stack | Loki, Grafana, Tempo, Prometheus |

## Execution Model

HOME은 접근·인증·비밀 기반, 관리 PostgreSQL/Valkey, 단일 노드 오브젝트 저장소,
AI 및 워크플로우, 기본 관측을 상시 제공한다. 사용자는 AI와 워크플로우의 상시
필요성을 확인했다. 모델 추론과 이미지 생성의 동시 GPU 사용은 별도 자원 검증
대상이며, 컨테이너 상시 실행이 모든 작업의 동시 실행 보장은 아니다.

| Selection | Purpose |
| --- | --- |
| `core` | Gateway, identity, and OpenBao bootstrap selection; it is not the complete HOME selection |
| `mng` | Shared management database/broker and exporters needed by the selected HOME services |
| `ai workflow storage` | Confirmed always-on AI/workflow capability and its object/vector/state dependencies |
| `obs-core obs-host availability logs alerting` | HOME metrics, host visibility, availability, logs and alerts |
| `tooling` | Registry and SonarQube only; excluded from HOME |
| `testing` | k6 and the Locust master/worker pair; excluded from HOME |
| `iac` | OpenTofu and Terrakube API/UI/executor; excluded from HOME |
| `dependency-update` | Renovate update job only; excluded from `tooling` and HOME |

HOME은 `core mng ai workflow storage obs-core obs-host availability logs alerting`의
37-service selection이다. 위 조합은 검토 대상 HOME 선택이며 배포 승인이 아니다. OpenBao 초기화·unseal·
AppRole provisioning, bind directory 권한, GPU 준비, 데이터 백업을 먼저 확인한다.
초기화 job의 성공 종료와 daemon의 health를 구분한다. cluster·legacy·maintenance
프로파일은 업무 소비자와 검증 목적이 확인될 때만 별도로 선택한다.

## Getting Started

저장소 루트에서 Docker Engine과 Compose `include` 지원을 확인한다. 공개
환경 스키마는 [.env.example](../.env.example), secret 참조 계약은
[Secret Management](../secrets/README.md)를 따른다. 비밀 값은 문서와 명령 출력에
넣지 않는다. NVIDIA workload는 호스트 드라이버와 Container Toolkit이 필요하다.

```bash
# 구성 검증만 수행하며 컨테이너를 시작하지 않는다.
HYHOME_COMPOSE_PROFILES="core mng ai workflow storage obs-core obs-host availability logs alerting" \
  bash scripts/validation/validate-docker-compose.sh
```

실제 기동·재시작·복구는 운영 문서의 대상 서비스와 승인 경계를 따른다.
개별 leaf Compose는 루트 network와 secret 선언에 의존하므로 루트에서 검증한다.

## Structure

```text
infra/
├── 01-gateway/        # Edge Routing & SSL Ingress
├── 02-auth/           # SSO, IAM, and OAuth2 Proxy
├── 03-security/       # OpenBao; Vault migration surface
├── 04-data/           # Persistence (SQL, NoSQL, Object)
├── 05-messaging/      # Event Streaming (Kafka)
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
| Config files | Git-tracked `infra/**/{compose,docker-compose}*.{yml,yaml}`, Dockerfile, scripts, and mounted config paths |
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

1. **Service Addition**: `infra/<tier>/<service>/` 디렉터리와 Compose/Dockerfile implementation source를 만듭니다.
2. **Global Integration**: 새 Compose fragment는 루트 `docker-compose.yml` `include`에 추가하고, 각 service의 `profiles:`와 POL-0078 membership을 함께 갱신합니다. HOME 여부는 새 vocabulary가 아니라 current consumer evidence로 결정합니다.
3. **Configuration and ownership**: public environment/secret schema와 secret-file reference를 함께 추가하고, 값은 절대 문서화하지 않습니다. Compose image pin은 projection/updater owner와 동기화하고 Dockerfile build pin은 해당 Dockerfile authority에 연결합니다.
4. **Operations and documentation**: service Guide의 `implementation_services` mapping에 exact Compose path/service binding을 추가하고, Policy/Runbook, service README, current Spec/Task를 같은 변경에서 갱신합니다. operations catalog가 global joins를 검증하므로 별도 registry/checker를 만들지 않습니다.
5. **Validation**: `scripts/validation/validate-docker-compose.sh`, operations catalog, metadata 및 link checks를 변경 범위에 맞게 실행합니다.

공유 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../.agents/governance/agentic.md)와 [documentation protocol](../.agents/governance/documentation-protocol.md)로 라우팅한다.

1. 타겟 계층과 기존 서비스 패턴을 파악한다.
2. 새 서비스가 `common-optimizations.yml` 템플릿을 준수하는지 확인한다.
3. 상세 컨텍스트는 [bootstrap 정규 로드 순서](../.agents/governance/bootstrap.md#canonical-load-order)에 따라 요청에 필요한 문서만 해석한다.
4. 이 README의 "Infrastructure Tiers" 테이블을 업데이트하여 추적성을 유지한다.

## Related Documents

- Official Guides (`docs/05.operations/README.md`)
- Operation Specs (`docs/05.operations/README.md`)
- Architecture Details (`docs/02.architecture/descriptions/README.md`)
- [Secret Management](../secrets/README.md)
- [Root Compose](../docker-compose.yml)
- [Tech Stack Versions](./tech-stack.versions.json)
- [Documentation index](../docs/README.md)
