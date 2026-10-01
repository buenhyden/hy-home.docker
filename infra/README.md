---
title: "Infrastructure Surface"
version: "1.3.4"
type: "common/repository-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2025-11-24"
---

# Hy-Home Infrastructure (infra/)

> hy-home.docker 생태계를 위한 통합 서비스 정의 및 오케스트레이션 계층입니다.

## Overview

`infra/` 디렉터리는 전체 홈 서버와 AI 개발 환경의 **서비스 정의**를 관리합니다. 티어와 컴포넌트 디렉터리는 Compose 선언, 빌드 소스, 마운트된 설정을 소유합니다. 루트 `docker-compose.yml`은 `include`로 등록된 fragment들을 집계하며 일부 fragment는 여러 서비스를 소유합니다. 디렉터리 구성과 프로필은 런타임 격리를 보장하지 않습니다.

## Audience

이 README의 주요 독자:

- **Operators**: 인프라 배포 및 서비스 라이프사이클 관리.
- **AI Agents**: 시스템 탐색, 자동화된 설정, 스케일링.
- **Developers**: 애플리케이션 개발을 위한 인프라 서비스 소비.

## Scope

### In Scope

- 12개 기능 티어에 걸친 서비스 정의.
- 루트 `docker-compose.yml`을 통한 전역 오케스트레이션.
- Compose 파일 목록과 각 서비스를 선택하는 프로필.
- **Docker Profiles**(`core`, `mng`, `obs` 등)를 사용한 표준화된 실행 모델.
- 리소스 최적화 및 보안 하드닝 템플릿.

### Out of Scope

- 세부 내부 서비스 설정 (`docs/05.operations/` 또는 하위 모듈 README 참고).
- 애플리케이션 비즈니스 로직과 프론트엔드 소스 코드.
- 자격 증명 및 민감 변수 (`secrets/`에서 관리).

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
`docs/05.operations/policies/0078-compose-profile-vocabulary.md`다. 전수 분류와 관측 일자는 Stage 90의
기존 local Docker service consolidation 연구에 기록한다.

## Tech Stack

실행 version pin의 원본은 각 Compose/Dockerfile 선언이다.
[version projection](tech-stack.versions.json)은 tracked Compose image 선언에서
파생한 기계 판독 projection이며 drift 검사와 업데이트 소유권 탐색에 사용한다.
Dockerfile `FROM`/`ARG`와 inline build의 pin은 별도 build authority이므로 이
projection이 그것들의 완전한 목록이라고 주장하지 않는다. README에는 source link
없이 exact patch literal을 복제하지 않는다.

| Category | Technology | Notes |
| :--- | :--- | :--- |
| 오케스트레이션 | Docker Compose | `include`와 명시적 `profiles` |
| 엣지 라우터 | Traefik v3.x | 동적 서비스 디스커버리 |
| 인증 | Keycloak / OIDC | 중앙 집중식 IAM |
| 옵저버빌리티 | LGTM Stack | Loki, Grafana, Tempo, Prometheus |

## Execution Model

HOME은 접근·인증·비밀 기반, 관리 PostgreSQL/Valkey, 단일 노드 오브젝트 저장소,
AI 및 워크플로우, 기본 관측을 상시 제공한다. 사용자는 AI와 워크플로우의 상시
필요성을 확인했다. 모델 추론과 이미지 생성의 동시 GPU 사용은 별도 자원 검증
대상이며 컨테이너를 상시 실행한다고 모든 작업의 동시 실행이 보장되지는 않는다.

| Selection | Purpose |
| --- | --- |
| `core` | 게이트웨이, 인증, OpenBao 부트스트랩 선택; 전체 HOME 선택은 아님 |
| `mng` | 선택된 HOME 서비스에 필요한 공유 관리 데이터베이스/브로커 및 exporter |
| `ai workflow storage` | 상시 확인된 AI/워크플로우 기능과 그 오브젝트/벡터/상태 의존성 |
| `obs-core obs-host availability logs alerting` | HOME 메트릭, 호스트 가시성, 가용성, 로그, 알림 |
| `tracing profiling obs-gpu` | HOME Alloy, Traefik, Grafana, Prometheus가 이미 전송하거나 스크레이프하는 HOME 트레이스(Tempo), 프로파일(Pyroscope), GPU 메트릭(DCGM exporter) |
| `registry` | HOME 개발용 컨테이너 레지스트리 |
| `tooling` | Registry와 SonarQube; HOME에서 제외됨(registry만 `registry`를 통해 HOME에 합류) |
| `testing` | k6와 Locust master/worker 쌍; HOME에서 제외됨 |
| `iac` | OpenTofu와 Terrakube API/UI/executor; HOME에서 제외됨 |
| `dependency-update` | Renovate 업데이트 작업만; `tooling`과 HOME에서 제외됨 |

HOME은 `core mng ai workflow storage obs-core obs-host availability logs alerting tracing profiling obs-gpu registry`의
profile 조합이다. 현재 서비스 목록은 공개 예제 환경의 `docker compose config --services`로 조회한다. 위 조합은 검토 대상 HOME 선택이며 배포 승인이 아니다. OpenBao 초기화·unseal·
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
HYHOME_COMPOSE_PROFILES="core mng ai workflow storage obs-core obs-host availability logs alerting tracing profiling obs-gpu registry" \
  bash scripts/validation/validate-docker-compose.sh
```

실제 기동·재시작·복구는 운영 문서의 대상 서비스와 승인 경계를 따른다.
개별 leaf Compose는 루트 network와 secret 선언에 의존하므로 루트에서 검증한다.

## Structure

각 tier의 기능과 현재 패키지 배치는 다음과 같습니다.

| Tier | Category | Key Services | Status |
| :--- | :--- | :--- | :--- |
| **01** | **Gateway** | [Traefik](./01-gateway/traefik), [Nginx](./01-gateway/nginx) | HOME / 선택적; disposition 참고 |
| **02** | **Identity** | [Keycloak](./02-auth/keycloak), [OAuth2-Proxy](./02-auth/oauth2-proxy) | HOME / 선택적; disposition 참고 |
| **03** | **Security** | [OpenBao](./03-security/openbao) | HOME 부트스트랩 |
| **04** | **Data** | [mng-db](./04-data/mng-db), [SeaweedFS](./04-data/seaweedfs), [Qdrant](./04-data/qdrant), [RedisInsight](./04-data/redisinsight) | HOME / 선택적; disposition 참고 |
| **05** | **Messaging** | [Kafka](./05-messaging/kafka) | 선택적; 클러스터는 LAB |
| **06** | **Observability** | [Grafana](./06-observability/grafana), [Prometheus](./06-observability/prometheus), [Loki](./06-observability/loki), [Tempo](./06-observability/tempo), [Dozzle](./06-observability/dozzle) | HOME / 선택적; disposition 참고 |
| **07** | **Workflow** | [Airflow](./07-workflow/airflow), [n8n](./07-workflow/n8n) | HOME / 선택적; disposition 참고 |
| **08** | **AI** | [Ollama](./08-ai/ollama), [Open WebUI](./08-ai/open-webui), [ComfyUI](./08-ai/comfyui), [Open Notebook](./08-ai/open-notebook), [MLflow](./08-ai/mlflow) | HOME / 선택적 |
| **09** | **Platform Operations** | [OpenTofu](./09-platform-ops/opentofu), [Terrakube](./09-platform-ops/terrakube), [Registry](./09-platform-ops/registry), [Renovate](./09-platform-ops/renovate), [Restic](./09-platform-ops/restic) | HOME / 명시적 작업 |
| **10** | **Communication** | [Stalwart](./10-communication/stalwart) | 선택적 내부 메일 |
| **11** | **Quality** | [k6](./11-quality/k6), [Locust](./11-quality/locust), [SonarQube](./11-quality/sonarqube), [WireMock](./11-quality/wiremock), [Pact Broker](./11-quality/pact-broker), [Conftest](./11-quality/conftest), [Mailpit](./11-quality/mailpit) | DEV / 명시적 검증 |
| **12** | **Analytics** | [Flink](./12-analytics/flink), [Trino](./12-analytics/trino), [Superset](./12-analytics/superset), [dbt](./12-analytics/dbt), [JupyterLab](./12-analytics/jupyterlab) | OPTIONAL / LAB |


```text
infra/
├── 01-gateway/        # Edge Routing & SSL Ingress
├── 02-auth/           # SSO, IAM, and OAuth2 Proxy
├── 03-security/       # OpenBao
├── 04-data/           # Persistence (SQL, NoSQL, Object)
├── 05-messaging/      # Event Streaming (Kafka)
├── 06-observability/  # Monitoring, Logging, Tracing
├── 07-workflow/       # DAG Orchestration & Automation
├── 08-ai/             # LLM Inference & RAG Engines
├── 09-platform-ops/        # IaC, 아티팩트, 의존성 유지보수와 공통 백업
├── 10-communication/  # 운영 메일
├── 11-quality/        # 소프트웨어·설정·성능·계약 검증과 테스트 메일
├── 12-analytics/      # Processing, SQL, quality, BI and transformation
├── common-optimizations.yml # Shared Docker templates
└── README.md          # This file
```

Data와 Analytics는 중간 분류 폴더 없이 패키지를 직접 배치합니다. Observability는
tier Compose가 여러 하위 설정 폴더를 묶고 Dozzle만 별도 leaf Compose를
사용하는 예외입니다. 디렉터리
번호는 기동 순서가 아니며 root include와 service profile이 선택을 결정합니다.

## Service Documentation Rubric

각 서비스 README는 같은 서비스 디렉터리의 Compose/설정 파일과 정합성을 유지해야 하며
다음의 agent 검증 가능 필드를 다뤄야 합니다.

| Field | Required evidence |
| :--- | :--- |
| Purpose | 서비스 역할, 티어, 해당 서비스를 선택하는 프로필 |
| Config files | Git 추적 `infra/**/{compose,docker-compose}*.{yml,yaml}`, Dockerfile, 스크립트, 마운트된 설정 경로 |
| Config values | 동작에 영향을 주는 비밀이 아닌 환경 변수 키와 기본값 |
| Compose linkage | 루트 include/프로필 상태 및 변형 compose 파일 |
| Networks | 선언된 네트워크와 의도된 신뢰 경계 |
| Volumes | 영속 데이터, 바인드 마운트, 백업 관련 경로 |
| Ports | 내부 및 노출 포트와 프로토콜 참고 사항 |
| Labels | Traefik, 라우팅, 옵저버빌리티, 정책 레이블 |
| Secret refs | 시크릿 이름과 마운트 경로만; 시크릿 값은 절대 포함하지 않음 |
| Healthcheck | 헬스 엔드포인트 또는 해당 없을 때의 명시적 사유 |
| Operations | 정식 가이드, 정책, 런북, 서비스 README 참조 |
| Validation | 관련 compose, hardening, repo-contract 점검 |
| Troubleshooting | 알려진 실패 모드와 첫 진단 명령 |

## How to Work in This Area

1. **Service Addition**: `infra/<tier>/<service>/` 디렉터리와 Compose/Dockerfile 구현 소스를 만듭니다.
2. **Global Integration**: 새 Compose fragment는 루트 `docker-compose.yml`의 `include`에 추가하고 각 서비스의 `profiles:`와 POL-0078 소속을 함께 갱신합니다. HOME 여부는 새 어휘가 아니라 현재의 consumer 근거로 결정합니다.
3. **Configuration and ownership**: 공개 환경 변수/시크릿 스키마와 secret-file 참조를 함께 추가하고 값은 절대 문서화하지 않습니다. Compose 이미지 고정 값은 projection/updater owner와 동기화하고 Dockerfile 빌드 고정 값은 해당 Dockerfile authority에 연결합니다.
4. **Operations and documentation**: 서비스 Guide의 `implementation_services` 매핑에 정확한 Compose 경로/서비스 바인딩을 추가하고 Policy/Runbook, 서비스 README, 현재 Spec/Task를 같은 변경에서 갱신합니다. operations catalog가 전역 조인을 검증하므로 별도 registry/checker를 만들지 않습니다.
5. **Validation**: `scripts/validation/validate-docker-compose.sh`, operations catalog, metadata 및 link 점검을 변경 범위에 맞게 실행합니다.

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
