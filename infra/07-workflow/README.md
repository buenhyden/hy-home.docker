---
title: "Workflow Tier (07-workflow)"
version: "1.2.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2025-11-12"
---

# Workflow Tier (07-workflow)

> Airflow의 code-first 오케스트레이션과 n8n의 low-code 자동화입니다.

## Overview

`07-workflow`는 Airflow와 n8n을 운영합니다. 브로커는 공유 `mng-valkey`를 쓰거나
`dedicated-valkey` 프로필로 전용 인스턴스를 기동할 수 있습니다. 실제 브로커
전환 시에는 각 서비스의 host/secret 환경 변수 쌍을 함께 바꿔야 합니다.

인증은 서비스별로 다릅니다.

- Airflow: Native Keycloak Auth Manager
- Flower: OAuth2 Proxy ForwardAuth
- n8n: OAuth2 Proxy ForwardAuth

## Audience

- Data Engineers
- Backend Developers
- Operators
- AI Agents

## Scope

- Airflow
- n8n
- 워크플로우 브로커
- 워크플로우 DB
- 공개 UI 인증 경계

## Structure

```text
07-workflow/
├── airflow/
├── n8n/
└── README.md
```

## How to Work in This Area

1. Airflow/n8n 운영 문서를 확인합니다.
2. Airflow 인증 변경 시에는 Native OIDC 계약을 확인합니다.
3. Flower/n8n 인증 변경 시에는 ForwardAuth 계약을 확인합니다.
4. 브로커 프로필과 host/secret 쌍을 함께 검토합니다.
5. hardening/compose 검증을 실행합니다.

## Tech Stack

| Category | Technology | Notes |
| --- | --- | --- |
| Orchestration | Airflow | CeleryExecutor |
| Automation | n8n | queue mode |
| Broker | Valkey | shared/dedicated |
| Database | PostgreSQL | `mng-pg` |

## Service Matrix

| Service | Protocol | Profile | Authentication |
| --- | --- | --- | --- |
| `airflow-apiserver` | HTTP | `workflow` | Native Keycloak Auth Manager |
| `airflow-scheduler` | internal | `workflow` | internal |
| `airflow-worker` | internal | `workflow` | internal |
| `flower` | HTTP | `workflow` | OAuth2 Proxy ForwardAuth |
| `n8n` | HTTP | `workflow` | OAuth2 Proxy ForwardAuth |
| `n8n-worker` | internal | `workflow` | internal |
| `n8n-task-runner` | internal | `workflow` | internal |

## Configuration

- Airflow/n8n DB: `mng-pg`
- 기본 브로커: `mng-valkey`
- `dedicated-valkey`: Airflow/n8n 전용 Valkey
- Airflow UI 인증: Keycloak 직접 연동
- Flower/n8n UI 인증: ForwardAuth

## Testing

```bash
HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 07-workflow
```

## Change Impact

- Airflow 버전/provider 변경 -> DB/인증 마이그레이션이 필요할 수 있음
- 브로커 변경 -> worker에 영향
- 인증 미들웨어 변경 -> 로그인/접근에 영향

### Convergence service and command map

저장소 루트에서 실행합니다. 정적 사전 점검은 `docker compose --profile workflow config --quiet`, 핵심 대상 시작은 `docker compose --profile workflow up -d`입니다.

| Package/services | Class | Exact profiles |
| --- | --- | --- |
| Airflow core, Flower, StatsD exporter | HOME | `workflow`, `workflow-airflow` |
| n8n core, workers, task runners | HOME | `workflow`, `workflow-n8n` |
| Airflow Valkey + exporter | OPTIONAL | `dedicated-valkey` |
| n8n Valkey + exporter | OPTIONAL | `dedicated-valkey` |

이 프로필은 선택적 브로커를 시작만 할 뿐 선택하지는 않습니다. 각 애플리케이션에 맞는 host와 secret 선택자를 함께 설정해야 합니다. 안정적인 문서 진입점은 [docs/README.md](../../docs/README.md)이며 정확한 Stage 05 대상은 `docs/05.operations/guides/0050-airflow.md`의 `GDE/POL/RUN-0050`과 `docs/05.operations/guides/0053-n8n.md`의 `GDE/POL/RUN-0053`입니다.

## Related Documents

- [Data](../04-data/README.md)
- [Observability](../06-observability/README.md)
- [Gateway](../01-gateway/README.md)
- **Auth Integration**: `docs/05.operations/guides/0079-application-auth-integration.md` (진입점: [docs/README.md](../../docs/README.md))
- [Documentation index](../../docs/README.md)

워크플로우 서비스는 소유자가 확인한 상시 HOME 역량입니다. 런타임 고정 값은 Compose/Dockerfile 선언이 소유하고 [파생된 Compose 이미지 프로젝션](../tech-stack.versions.json)으로 드리프트를 검증합니다.
