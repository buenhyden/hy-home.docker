---
title: "Workflow Tier (07-workflow)"
version: "1.2.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-18"
created: "2025-11-12"
---

# Workflow Tier (07-workflow)

> Airflow code-first orchestration and n8n low-code automation.

## Overview

`07-workflow`는 Airflow와 n8n을 운영한다. broker는 shared `mng-valkey` 또는
`dedicated-valkey` profile의 dedicated instance를 사용한다.

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
| Orchestration | Airflow 3.3.1 | CeleryExecutor |
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

## Related Documents

- [Data](../04-data/README.md)
- [Observability](../06-observability/README.md)
- [Gateway](../01-gateway/README.md)
- [Auth Integration](../../docs/05.operations/catalog/02-auth/0079-application-auth-integration/guide.md)
- [Documentation index](../../docs/README.md)
