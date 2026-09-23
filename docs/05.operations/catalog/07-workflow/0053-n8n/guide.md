---
title: "n8n Usage Guide"
version: "1.1.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0053"
parent_ids:
- "POL-0053"
implementation_services:
  infra/07-workflow/n8n/docker-compose.yml:
  - n8n
  - n8n-task-runner
  - n8n-task-runner-worker
  - n8n-valkey
  - n8n-valkey-exporter
  - n8n-worker
created: "2026-05-10"
---

# n8n Usage Guide

## Usage

### Overview

이 가이드는 `hy-home.docker`의 n8n 로우코드 자동화 환경을 사용하는 방법을 설명한다. 현재 구현은 `n8n`, `n8n-worker`, `n8n-task-runner`, `n8n-task-runner-worker` queue mode 구성이다. `dedicated-valkey` profile은 dedicated `n8n-valkey`를 기동하지만, 실제 broker는 `N8N_VALKEY_HOST`/`N8N_VALKEY_SECRET` pair가 선택하며 기본값은 공유 `mng-valkey`다.

### Usage Type

`system-guide | how-to`

### Target Audience

- Developer
- Operator
- Integration Maintainer
- AI Agent

### Purpose

- n8n UI, webhook, public API, queue worker 구성을 이해한다.
- workflow 작성, 테스트, 활성화, 오류 처리의 기본 흐름을 맞춘다.
- credential과 secret을 노출하지 않는 운영 경계를 유지한다.
- 반복 복구 절차는 paired runbook으로 넘긴다.

### Prerequisites

- `infra/07-workflow/n8n/README.md`의 service readiness 확인
- n8n 접근 권한과 필요한 Docker Secrets 준비
- root workflow compose 검증 권한

### Step-by-step Instructions

#### 1. Architecture and Components

n8n은 확장성을 위해 분산형 큐 아키텍처를 사용하며, 주요 컴포넌트는 다음과 같다:

- **n8n Main**: 사용자 인터페이스(UI), API 서버, 워크플로우 엔진.
- **n8n Worker**: 대규모 비동기 작업 처리를 담당하는 작업 실행기.
- **n8n Task Runners**: `n8n-task-runner`와 `n8n-task-runner-worker`가 외부 runner 모드에서 broker endpoint에 연결한다.
- **Valkey Broker**: compose 파일은 `infra/07-workflow/n8n/docker-compose.yml` 하나다. `dedicated-valkey` profile은 `n8n-valkey`와 exporter를 기동할 뿐이다. `${N8N_VALKEY_HOST:-mng-valkey}`와 `${N8N_VALKEY_SECRET:-mng_valkey_password}`가 실제 broker를 선택하며 두 값을 matching pair로 바꾸지 않으면 공유 `mng-valkey`가 유지된다.
- **Metadata DB**: 워크플로우 레시피 및 사용자 자격 증명(`Credentials`)을 저장하는 PostgreSQL 데이터베이스.

#### 2. Access and Integration

- **Web UI**: `https://n8n.${DEFAULT_URL}` 에 접속하여 시각적으로 자동화 로직을 설계한다.
- **Public API**: 필요한 경우 `N8N_PUBLIC_API_BASE_URL`을 통해 프로그래밍 방식으로 워크플로우를 제어할 수 있다.
- **Webhook**: 외부 서비스로부터의 이벤트를 수신할 수 있도록 `WEBHOOK_URL`이 명시적으로 구성되어 있다.

#### 3. Workflow Authoring and Activation

- 필요한 trigger/action node를 선택하고 node 간 data flow를 명시한다.
- 복잡한 변환은 `Code` node 또는 sub-workflow로 분리한다.
- 새 워크플로우 설계 시 `Manual Execution`으로 개별 노드의 데이터 입출력을 검증한다.
- 실패 알림이 필요한 workflow에는 error workflow 또는 notification node를 연결한다.
- 검증 완료 후 `Active`로 전환한다.

#### 4. Credential and Secret Boundary

- 모든 인증 정보는 n8n 내부의 `Credentials` 탭에서 관리한다.
- credential은 metadata DB에 암호화되어 저장되며, `N8N_ENCRYPTION_KEY_FILE`은 Docker Secret으로 주입된다.
- workflow export, API response, screenshot evidence에는 credential value, token, webhook secret 원문을 포함하지 않는다.

#### 5. Custom Node Extension

- 필요한 경우 `infra/07-workflow/n8n/custom` 경로에 사용자 정의 node를 추가할 수 있다.
- custom node 추가 전 security review와 root validation을 완료한다.

#### 6. Development and Verification

- **Local Runner**: 새로운 노드나 복잡한 JS 코드는 n8n 내부의 `Code` 노드에서 직접 실행하여 즉시 결과를 확인할 수 있다.
- **Static Validation**: repo root에서 `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`를 실행한다. service-local compose 파일은 root network/secrets context 없이 단독 `config` 대상으로 쓰지 않는다.
- **Runtime Health**: runtime이 실행 중이면 `docker compose exec n8n wget -qO- http://localhost:${N8N_PORT:-5678}/healthz`를 확인한다.

### Common Pitfalls

- 대규모 배치/의존성 DAG를 n8n에 넣어 worker queue를 장시간 점유하는 경우. 이 경우 Airflow로 분리한다.
- workflow가 많은 node를 포함해 유지보수가 어려워지는 경우. `Sub-workflows`로 분리한다.
- webhook을 외부에 노출하면서 gateway allowlist, SSO, rate-limit 경계를 검토하지 않는 경우.
- service-local compose를 root network/secrets context 없이 단독 readiness evidence로 사용하는 경우.

### Source-backed operating contract

- **Purpose/classification**: `n8n`, worker, task runner, and init are owner-confirmed `HOME` automation services. `n8n-valkey` and its exporter are an `OPTIONAL` dedicated broker pair.
- **Profiles/source**: core services use `workflow`/`workflow-n8n`; the pair uses `dedicated-valkey`. [Compose](../../../../../infra/07-workflow/n8n/docker-compose.yml) and its selected Dockerfiles are authoritative.
- **State flow**: PostgreSQL database `n8n` on `mng-pg` is durable workflow/execution metadata; `n8n-data`, runner data, and `custom/` hold local application, binary, and extension artifacts; Valkey carries queue coordination. Queue state is not a complete recoverable workflow history.
- **Secrets/environment**: preserve `n8n_db_password`, `n8n_encryption_key`, `n8n_runner_auth_token`, and the selected broker password. `N8N_VALKEY_HOST` and `N8N_VALKEY_SECRET` must be switched together; the profile alone leaves defaults on `mng-valkey`/`mng_valkey_password`.
- **Dependencies/security**: PostgreSQL, selected Valkey, Traefik/OAuth2 Proxy/Keycloak, Qdrant where a workflow uses it, root CA, and `n8n_net` must be ready. Task runners stay internal and use the auth token; the UI uses the gateway auth chain.
- **Persistence/resources**: recover PostgreSQL and matching encryption key together with local data, custom nodes, and externally stored binary artifacts. Compose limits are source declarations, not measured headroom.
- **Normal use/lifecycle**: render from root with `docker compose --profile workflow config --quiet`. Before backup or update, disable schedules/webhooks and external producers, drain/reconcile executions, back up PostgreSQL and artifacts consistently, upgrade with the upstream sequence, then verify credentials, a manual workflow, queue workers, webhooks, and task runners before resuming.
- **Upstream/license**: follow the official [queue mode](https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/enable-queue-mode/), [encryption key](https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/configuration-examples/set-a-custom-encryption-key/), [backup/restore](https://docs.n8n.io/deploy/host-n8n/keep-n8n-running/backup-and-restore/), and [update](https://docs.n8n.io/deploy/host-n8n/keep-n8n-running/update-n8n/) guidance. n8n uses its Sustainable Use License/fair-code terms; verify use against the pinned release.

## Common Checks

- `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 07-workflow`
- Runtime이 실행 중이면 `docker compose exec n8n wget -qO- http://localhost:${N8N_PORT:-5678}/healthz`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](runbook.md)을 따른다.

## Traceability

- Declared parent: [n8n Operations Policy](policy.md) (`POL-0053`)
- Governing authority: [Workflow Tier (07-workflow) Architecture Description](../../../../02.architecture/descriptions/0007-workflow-architecture.md) (`AD-0007`)
- Subject peers: [Policy](policy.md) (`POL-0053`), [Runbook](runbook.md) (`RUN-0053`)

## Related Documents

- [n8n Compose](../../../../../infra/07-workflow/n8n/docker-compose.yml)

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../../../README.md)
- [Operations policy](policy.md)
- [Recovery runbook](runbook.md)
- [07-workflow architecture](../../../../02.architecture/descriptions/0007-workflow-architecture.md)
