---
title: "n8n Low-code Automation"
version: "1.2.2"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2025-11-12"
---

# n8n Low-code Automation

## Overview

n8n은 시각적 인터페이스로 워크플로우 자동화를 구현하는 로우코드 도구이다. 복잡한 Airflow DAG와 달리 직관적인 노드 연결로 API 통합, 웹후크 처리, 이벤트 기반 자동화를 빠르게 배포할 수 있다.

## Audience

이 README의 주요 독자:

- Workflow Operators
- Integration Developers
- AI Agents

## Scope

### In Scope

- n8n 메인 서비스, worker, task runner, 메타데이터 DB, queue 모드 compose 연결
- 비밀이 아닌 환경 변수와 런타임 토폴로지 노트
- 정식 가이드, 정책, 런북, 워크플로우 스펙으로의 연결

### Out of Scope

- Airflow DAG 작성 및 스케줄러 운영
- n8n 자격 증명 값, 워크플로우 시크릿, 내보낸 비공개 워크플로우 데이터
- 서드파티 SaaS 계정 설정

## Structure

```text
n8n/
├── Dockerfile
├── dev.Dockerfile
├── docker-compose.yml  # n8n, worker, task runner, and queue wiring
├── docker-entrypoint*.sh
├── custom/
└── README.md           # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | n8n Low-code Automation 서비스 leaf. [root docker-compose.yml](../../../docker-compose.yml) -> `infra/07-workflow/n8n/docker-compose.yml` 경로로 루트 include가 활성화됨. 이 파일 하나가 이 디렉터리의 유일한 Compose 파일임 |
| Config files | `docker-compose.yml` |
| Config values | env 키: `GENERIC_TIMEZONE`, `TZ`, `DB_TYPE`, `DB_POSTGRESDB_HOST`, `DB_POSTGRESDB_PORT`, `DB_POSTGRESDB_DATABASE`, `DB_POSTGRESDB_USER`, `DB_POSTGRESDB_PASSWORD_FILE` 외 다수; 프로필: `workflow`, `dev` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml) -> `infra/07-workflow/n8n/docker-compose.yml` 경로로 무조건 루트 include되며 프로필(`workflow`, `dev`)로 선택됨 |
| Networks | `edge_net`, `mng_data_net`, `n8n_net`, `obs_net` |
| Volumes | `n8n-data:/home/node/.n8n:rw`, `./custom:/home/node/.n8n/custom:rw`, `n8n-task-runner-worker-data:/home/node/.n8n:rw`, `n8n-data`, `n8n-task-runner-data`, `n8n-task-runner-worker-data`, `n8n-valkey-data:/data:rw`, `n8n-valkey-data` |
| Ports | `${N8N_PORT:-5678}`, `${N8N_BROKER_PORT:-5679}`, `${N8N_TASK_RUNNER_PORT:-5680}`, `${VALKEY_PORT:-6379}`, `${VALKEY_BUS_PORT:-16379}`, `${VALKEY_EXPORTER_PORT:-9121}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.n8n.rule`, `traefik.http.routers.n8n.entrypoints`, `traefik.http.routers.n8n.middlewares`, `traefik.http.routers.n8n.tls`, `traefik.http.routers.n8n.service`, `traefik.http.services.n8n.loadbalancer.server.port` |
| Secret refs | 이름: `mng_valkey_password`, `n8n_db_password`, `n8n_encryption_key`, `n8n_runner_auth_token`, `n8n_valkey_password`; 마운트: `/run/secrets/mng_valkey_password`, `/run/secrets/n8n_db_password`, `/run/secrets/n8n_encryption_key`, `/run/secrets/n8n_runner_auth_token`, `/run/secrets/n8n_valkey_password` |
| Healthcheck | `n8n`, `n8n-worker`, `n8n-task-runner`, `n8n-task-runner-worker`, `dedicated-valkey` 프로필의 `n8n-valkey`에 Compose 헬스체크가 선언되어 있음. exporter는 의존성 기반으로 게이트됨 |
| Operations | Guide (`docs/05.operations/guides/0053-n8n.md`), Policy (`docs/05.operations/policies/0053-n8n.md`), Runbook (`docs/05.operations/runbooks/0053-n8n.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`로 시작한 뒤 서비스 로그와 연결된 런북 근거를 확인합니다. |

## How to Work in This Area

공통 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../../../.agents/governance/agentic.md)와 [documentation protocol](../../../.agents/governance/documentation-protocol.md)을 따른다.

1. n8n 설정을 변경하기 전에 연결된 운영 가이드, 정책, 런북을 검토합니다.
2. 외부 자격 증명은 n8n의 암호화된 Credentials 시스템이나 Docker Secrets에 보관합니다.
3. 통합을 추가하기 전에 간단한 로우코드 자동화와 Airflow가 소유하는 DAG 워크플로우를 구분합니다.
4. compose나 queue 모드를 변경한 뒤에는 아래 검증 명령을 실행합니다.
5. 병렬 워크로드를 변경할 때는 `EXECUTIONS_MODE: queue` 동작을 염두에 둡니다.

6. **Modularization**: 복잡한 로직은 `Sub-workflows`로 분리해 재사용성을 확보하십시오.
7. **Credential Safety**: 모든 외부 인증 정보는 n8n 내부의 `Credentials` 시스템에 암호화되어 저장되어야 하며 `docker-compose.yml`의 시크릿(`secrets`)으로 안전하게 공급됩니다.

## Tech Stack

| Component | Technology | Version | Note |
| :--- | :--- | :--- | :--- |
| Core Service | n8n | declared version | Node.js 기반 |
| Metadata DB | PostgreSQL | Management PostgreSQL | `infra/04-data/operational/mng-db`를 통해 관리됨 |
| Queue Broker | Valkey (Redis 호환) | declared version; 기본값은 `${N8N_VALKEY_HOST:-mng-valkey}`, `dedicated-valkey` 프로필에서는 `n8n-valkey` | Queue 오케스트레이션 |
| Task Runner | n8nio/runners | declared version | 격리된 실행 환경 |

## Architecture

n8n 환경은 고성능과 확장성을 위해 분산 모드로 구성된다:

- **Main Service**: UI 제공 및 워크플로우 관리.
- **Worker**: 실제 태스크 실행 담당 (Valkey 큐 기반).
- **Task Runner**: 특정 복잡한 태스크를 격리된 환경에서 안전하게 처리.
- **Valkey**: 워커 간 작업 분배를 위한 메시지 브로커.

## Traceability (Golden 5)

- **PRD**: 07-workflow PRD (`docs/01.requirements/0008-workflow.md`)
- **ARD**: 07-workflow Architecture Description (`docs/02.architecture/descriptions/0007-workflow-architecture.md`)
- **ADR**: N8N Integration ADR (`docs/02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md`)
- **Plan**: 활성 Spec 패키지 없음. 이전 SPEC-0008은 폐기되었습니다 (`docs/98.archive/tombstones/03.specs/0008-workflow.md`).

## Validation

- README나 n8n에 영향을 주는 Compose 참조 변경 후에는 `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- n8n 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.

## Troubleshooting

- 이 leaf는 루트 네트워크, Docker Secrets, 루트 include 컨텍스트에 의존하므로 루트 workflow 검증 명령으로 시작합니다.
- queue나 자격 증명 설정을 변경하기 전에 n8n 서비스 로그와 연결된 런북을 확인합니다.

### Convergence contract

- n8n core/worker/task runner는 `workflow`/`workflow-n8n`에서 **HOME**이며, n8n Valkey와 exporter는 `dedicated-valkey`에서 **OPTIONAL**입니다.
- Root preflight: `docker compose --profile workflow config --quiet`. Root start: `docker compose --profile workflow up -d n8n n8n-worker n8n-task-runner n8n-task-runner-worker`.
- `dedicated-valkey`는 해당 쌍만 시작합니다. 실제 선택은 `N8N_VALKEY_HOST`와 `N8N_VALKEY_SECRET`을 함께 일치시켜야 합니다.
- 안정적인 진입점: [docs/README.md](../../../docs/README.md). 정확한 Stage 05 경로: `docs/05.operations/guides/0053-n8n.md`; ID: `GDE-0053`, `POL-0053`, `RUN-0053`. 격리 복구는 계획되어 있으나 아직 실행되지 않았습니다.

## Related Documents

- **Guide**: n8n usage guide (`docs/05.operations/guides/0053-n8n.md`)
- **Policy**: n8n operations policy (`docs/05.operations/policies/0053-n8n.md`)
- **Runbook**: n8n recovery runbook (`docs/05.operations/runbooks/0053-n8n.md`)
- [Documentation index](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하고 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)으로 드리프트를 검증합니다.

Build source authority: [Dockerfile](Dockerfile), [dev.Dockerfile](dev.Dockerfile).
