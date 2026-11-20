---
title: "Workflow Tier (07-workflow)"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2025-11-12"
---

# Workflow Tier (07-workflow)

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

> Airflow의 code-first 오케스트레이션과 n8n의 low-code 자동화입니다.

#### Service

##### Purpose

###### Overview
<!-- core-payload-level:4 -->

`07-workflow`는 Airflow와 n8n을 운영합니다. 브로커는 공유 `mng-valkey`입니다.
앱별 전용 Valkey는 ADR-0062 결정 10으로 제거되었습니다.

인증은 서비스별로 다릅니다.

- Airflow: Native Keycloak Auth Manager
- Flower: OAuth2 Proxy ForwardAuth
- n8n: OAuth2 Proxy ForwardAuth

###### Audience
<!-- core-payload-level:4 -->

- Data Engineers
- Backend Developers
- Operators

###### Scope
<!-- core-payload-level:4 -->

- Airflow
- n8n
- 워크플로우 브로커
- 워크플로우 DB
- 공개 UI 인증 경계

###### Structure
<!-- core-payload-level:4 -->

```text
07-workflow/
├── airflow/
├── n8n/
└── README.md
```

###### Service Matrix
<!-- core-payload-level:4 -->

| Service | Protocol | Profile | Authentication |
| --- | --- | --- | --- |
| `airflow-apiserver` | HTTP | `workflow` | Native Keycloak Auth Manager |
| `airflow-scheduler` | internal | `workflow` | internal |
| `airflow-worker` | internal | `workflow` | internal |
| `flower` | HTTP | `airflow-flower`(opt-in) | OAuth2 Proxy ForwardAuth |
| `n8n` | HTTP | `workflow` | OAuth2 Proxy ForwardAuth |
| `n8n-worker` | internal | `workflow` | internal |

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| `airflow-apiserver` HTTP | `airflow-apiserver` | 이 README는 소비자를 기록하지 않는다. | `workflow` profile에서 Native Keycloak Auth Manager로 인증한다. | 이 README는 실패 처리를 기록하지 않는다. |
| `flower` HTTP | `flower` | 이 README는 소비자를 기록하지 않는다. | `airflow-flower`(opt-in) profile에서 OAuth2 Proxy ForwardAuth로 인증한다. | 이 README는 실패 처리를 기록하지 않는다. |
| `n8n` HTTP | `n8n` | 이 README는 소비자를 기록하지 않는다. | `workflow` profile에서 OAuth2 Proxy ForwardAuth로 인증한다. | 이 README는 실패 처리를 기록하지 않는다. |

###### Configuration
<!-- core-payload-level:4 -->

- Airflow/n8n DB: `mng-pg`
- 기본 브로커: `mng-valkey`
- Airflow UI 인증: Keycloak 직접 연동
- Flower/n8n UI 인증: ForwardAuth

###### Security Boundary
<!-- core-payload-level:4 -->

없음: 이 디렉터리는 Compose 서비스나 secret 참조를 직접 선언하지 않으며, 하위 `airflow/`, `n8n/`가 각자 선언한다.

#### Usage

##### Prerequisites

###### Tech Stack
<!-- core-payload-level:4 -->

| Category | Technology | Notes |
| --- | --- | --- |
| Orchestration | Airflow | CeleryExecutor |
| Automation | n8n | queue mode |
| Broker | Valkey | shared/dedicated |
| Database | PostgreSQL | `mng-pg` |

##### Selected Start

###### Usage
<!-- core-payload-level:4 -->

1. Airflow/n8n 운영 문서를 확인합니다.
2. Airflow 인증 변경 시에는 Native OIDC 계약을 확인합니다.
3. Flower/n8n 인증 변경 시에는 ForwardAuth 계약을 확인합니다.
4. 브로커 프로필과 host/secret 쌍을 함께 검토합니다.
5. hardening/compose 검증을 실행합니다.

###### Change Impact
<!-- core-payload-level:4 -->

- Airflow 버전/provider 변경 -> DB/인증 마이그레이션이 필요할 수 있음
- 브로커 변경 -> worker에 영향
- 인증 미들웨어 변경 -> 로그인/접근에 영향

###### Convergence service and command map
<!-- core-payload-level:5 -->

저장소 루트에서 실행합니다. 정적 사전 점검은 `docker compose --profile workflow config --quiet`, 핵심 대상 시작은 `docker compose --profile workflow up -d`입니다.

| Package/services | Class | Exact profiles |
| --- | --- | --- |
| Airflow core, StatsD exporter | HOME | `workflow`, `workflow-airflow` |
| Flower | opt-in(2026-11-10 owner 결정) | `airflow-flower` |
| n8n core, workers, task runners | HOME | `workflow`, `workflow-n8n` |

안정적인 문서 진입점은 [docs/README.md](../../docs/README.md)이며 정확한 Stage 05 대상은 `docs/05.operations/01.guides/08.workflows-and-automation/0050-airflow.md`의 `GDE/POL/RUN-0050`과 `docs/05.operations/01.guides/08.workflows-and-automation/0053-n8n.md`의 `GDE/POL/RUN-0053`입니다.

#### Checks

##### Readiness

###### Testing
<!-- core-payload-level:4 -->

```bash
HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 07-workflow
```

##### Failure Handling

###### Related Documents
<!-- core-payload-level:4 -->

- [Data](../04-data/README.md)
- [Observability](../06-observability/README.md)
- [Gateway](../01-gateway/README.md)
- **Auth Integration**: `docs/05.operations/01.guides/03.identity-and-access/0079-application-auth-integration.md` (진입점: [docs/README.md](../../docs/README.md))
- [Documentation index](../../docs/README.md)

워크플로우 서비스는 소유자가 확인한 상시 HOME 역량입니다. 런타임 고정 값은 Compose/Dockerfile 선언이 소유하고 [파생된 Compose 이미지 프로젝션](../tech-stack.versions.json)으로 드리프트를 검증합니다.

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 이 디렉터리는 자체 헬스체크나 관측 대상을 선언하지 않으며, 하위 `airflow/`, `n8n/`가 각자 선언한다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
