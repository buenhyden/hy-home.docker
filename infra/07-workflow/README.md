---
title: "Workflow Tier (07-workflow)"
version: "1.2.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
created: "2025-11-12"
---

# Workflow Tier (07-workflow)

> Airflow code-first orchestration and n8n low-code automation.

## Overview

`07-workflow`는 Airflow와 n8n을 운영한다. broker는 shared `mng-valkey` 또는
`dedicated-valkey` profile로 전용 instances를 기동할 수 있다. 실제 broker 전환은 각 서비스의 host/secret environment pair를 함께 바꿔야 한다.

Authentication은 서비스별로 다르다.

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
- workflow broker
- workflow DB
- public UI auth boundary

## Structure

```text
07-workflow/
├── airflow/
├── n8n/
└── README.md
```

## How to Work in This Area

1. Airflow/N8n operations docs 확인.
2. Airflow auth 변경은 Native OIDC contract 확인.
3. Flower/n8n auth 변경은 ForwardAuth contract 확인.
4. broker profile과 host/secret pair를 함께 검토.
5. hardening/compose validation 실행.

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
- default broker: `mng-valkey`
- `dedicated-valkey`: dedicated Airflow/n8n Valkey
- Airflow UI auth: Keycloak direct
- Flower/n8n UI auth: ForwardAuth

## Testing

```bash
HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 07-workflow
```

## Change Impact

- Airflow version/provider -> DB/Auth migration 가능
- broker -> workers 영향
- auth middleware -> login/access 영향

### Convergence service and command map

Run from the repository root: `docker compose --profile workflow config --quiet` for static preflight and `docker compose --profile workflow up -d` for the core target.

| Package/services | Class | Exact profiles |
| --- | --- | --- |
| Airflow core, Flower, StatsD exporter | HOME | `workflow`, `workflow-airflow` |
| n8n core, workers, task runners | HOME | `workflow`, `workflow-n8n` |
| Airflow Valkey + exporter | OPTIONAL | `dedicated-valkey` |
| n8n Valkey + exporter | OPTIONAL | `dedicated-valkey` |

The profile starts optional brokers but does not select them. Set each application's matching host and secret selector together. The stable documentation entry point is [docs/README.md](../../docs/README.md); exact Stage 05 subjects are `GDE/POL/RUN-0050` at `docs/05.operations/catalog/07-workflow/0050-airflow/` and `GDE/POL/RUN-0053` at `docs/05.operations/catalog/07-workflow/0053-n8n/`.

## Related Documents

- [Data](../04-data/README.md)
- [Observability](../06-observability/README.md)
- [Gateway](../01-gateway/README.md)
- [Auth Integration](../../docs/README.md)
- [Documentation index](../../docs/README.md)

Workflow services are owner-confirmed always-on HOME capabilities; runtime pins are owned by the Compose/Dockerfile declarations and the [derived Compose image projection](../tech-stack.versions.json) provides drift verification.
