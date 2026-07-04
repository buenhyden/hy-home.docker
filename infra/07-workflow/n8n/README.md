# n8n Low-code Automation

## Overview (KR)

n8n은 시각적 인터페이스를 통해 워크플로우 자동화를 구현하는 로우코드 도구이다. 복잡한 Airflow DAG와 달리 직관적인 노드 연결을 통해 API 통합, 웹후크 처리, 이벤트 기반 자동화를 빠르게 배포할 수 있다.

## Audience

이 README의 주요 독자:

- Workflow Operators
- Integration Developers
- AI Agents

## Scope

### In Scope

- n8n main service, worker, task runner, metadata DB, and queue mode compose wiring
- Non-secret environment and runtime topology notes
- Links to canonical guide, policy, runbook, and workflow spec

### Out of Scope

- Airflow DAG authoring and scheduler operation
- n8n credential values, workflow secrets, and exported private workflow data
- Third-party SaaS account configuration

## Structure

```text
n8n/
├── Dockerfile
├── dev.Dockerfile
├── docker-compose.dev.yml
├── docker-compose.yml  # n8n, worker, task runner, and queue wiring
├── docker-entrypoint*.sh
├── custom/
└── README.md           # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | n8n Low-code Automation service leaf; root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/07-workflow/n8n/docker-compose.dev.yml`; service-local production-like compose is `docker-compose.yml` |
| Config files | `docker-compose.dev.yml`, `docker-compose.yml` |
| Config values | env keys: `GENERIC_TIMEZONE`, `TZ`, `DB_TYPE`, `DB_POSTGRESDB_HOST`, `DB_POSTGRESDB_PORT`, `DB_POSTGRESDB_DATABASE`, `DB_POSTGRESDB_USER`, `DB_POSTGRESDB_PASSWORD_FILE`, plus 31 more; profiles: `workflow`, `dev` |
| Compose linkage | root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/07-workflow/n8n/docker-compose.dev.yml`; local compose only: `docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `n8n-data:/home/node/.n8n:rw`, `./custom:/home/node/.n8n/custom:rw`, `n8n-task-runner-worker-data:/home/node/.n8n:rw`, `n8n-data`, `n8n-task-runner-data`, `n8n-task-runner-worker-data`, `n8n-valkey-data:/data:rw`, `n8n-valkey-data` |
| Ports | `${N8N_PORT:-5678}`, `${N8N_BROKER_PORT:-5679}`, `${N8N_TASK_RUNNER_PORT:-5680}`, `${VALKEY_PORT:-6379}`, `${VALKEY_BUS_PORT:-16379}`, `${VALKEY_EXPORTER_PORT:-9121}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.n8n.rule`, `traefik.http.routers.n8n.entrypoints`, `traefik.http.routers.n8n.middlewares`, `traefik.http.routers.n8n.tls`, `traefik.http.routers.n8n.service`, `traefik.http.services.n8n.loadbalancer.server.port` |
| Secret refs | names: `mng_valkey_password`, `n8n_db_password`, `n8n_encryption_key`, `n8n_runner_auth_token`, `n8n_valkey_password`; mounts: `/run/secrets/mng_valkey_password`, `/run/secrets/n8n_db_password`, `/run/secrets/n8n_encryption_key`, `/run/secrets/n8n_runner_auth_token`, `/run/secrets/n8n_valkey_password` |
| Healthcheck | Compose healthcheck declared for `n8n`, `n8n-worker`, `n8n-task-runner`, `n8n-task-runner-worker`, and service-local `n8n-valkey`; exporter is dependency-gated |
| Operations | [Guide](../../../docs/05.operations/guides/07-workflow/n8n.md), [Policy](../../../docs/05.operations/policies/07-workflow/n8n.md), [Runbook](../../../docs/05.operations/runbooks/07-workflow/n8n.md) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`, then inspect service logs and linked runbook evidence. |

## How to Work in This Area

1. Review the linked operations guide, policy, and runbook before changing n8n configuration.
2. Keep external credentials in n8n's encrypted credentials system or Docker Secrets.
3. Distinguish quick low-code automation from Airflow-owned DAG workflows before adding integrations.
4. After compose or queue-mode changes, run the validation commands listed below.

## Tech Stack

| Component | Technology | Version | Note |
| :--- | :--- | :--- | :--- |
| Core Service | n8n | 2.29.5 | Node.js based |
| Metadata DB | PostgreSQL | Management PostgreSQL | Managed via `infra/04-data/operational/mng-db` |
| Queue Broker | Valkey (Redis-compatible) | 9.1.0 service-local, shared `mng-valkey` in root dev | Queue orchestration |
| Task Runner | n8nio/runners | 2.29.5 | Isolated execution environment |

## Architecture

n8n 환경은 고성능 및 확장성을 위해 분산 모드로 구성된다:

- **Main Service**: UI 제공 및 워크플로우 관리.
- **Worker**: 실제 태스크 실행 담당 (Valkey 큐 기반).
- **Task Runner**: 특정 복잡한 태스크를 격리된 환경에서 안전하게 처리.
- **Valkey**: 워커 간 작업 분배를 위한 메시지 브로커.

## AI Agent Guidance

1. **Modularization**: 복잡한 로직은 `Sub-workflows`를 활용하여 분리하고 재사용성을 확보하십시오.
2. **Credential Safety**: 모든 외부 인증 정보는 n8n 내부의 `Credentials` 시스템에 암호화되어 저장되어야 하며, `docker-compose.yml`의 시크릿(`secrets`)을 통해 안전하게 공급됩니다.
3. **Execution Mode**: `EXECUTIONS_MODE: queue`로 설정되어 있으므로 대량의 병렬 작업 처리가 가능합니다.

## Traceability (Golden 5)

- **PRD**: [07-workflow PRD](../../../docs/01.requirements/2026-03-26-07-workflow.md)
- **ARD**: [07-workflow ARD](../../../docs/02.architecture/requirements/0007-workflow-architecture.md)
- **ADR**: [N8N Integration ADR](../../../docs/02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md)
- **Spec**: [07-workflow Technical Spec](../../../docs/03.specs/07-workflow/spec.md)
- **Plan**: [07-workflow Implementation Plan](../../../docs/04.execution/plans/2026-03-26-07-workflow-standardization.md)

## Validation

- Run `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect n8n.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking n8n documentation ready.

## Troubleshooting

- Start with the root workflow validation command because this leaf depends on root `infra_net`, Docker Secrets, and root include context.
- Check n8n service logs and the linked runbook before changing queue or credential settings.

## Related Documents

- **Guide**: [n8n usage guide](../../../docs/05.operations/guides/07-workflow/n8n.md)
- **Policy**: [n8n operations policy](../../../docs/05.operations/policies/07-workflow/n8n.md)
- **Runbook**: [n8n recovery runbook](../../../docs/05.operations/runbooks/07-workflow/n8n.md)
- **Spec**: [07-workflow Technical Spec](../../../docs/03.specs/07-workflow/spec.md)
