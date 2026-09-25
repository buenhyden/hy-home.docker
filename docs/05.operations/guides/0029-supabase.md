---
title: "Supabase Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0029"
parent_ids:
- "POL-0029"
implementation_services:
  infra/04-data/operational/supabase/docker-compose.yml:
  - 'analytics'
  - 'auth'
  - 'db'
  - 'functions'
  - 'imgproxy'
  - 'kong'
  - 'meta'
  - 'realtime'
  - 'rest'
  - 'storage'
  - 'studio'
  - 'supavisor'
  - 'vector'
created: "2026-05-10"
---

# Supabase Usage Guide

> Use this guide to understand and verify the current self-hosted Supabase stack.

---

## Usage

### Overview

`supabase`는 [Compose 구현](../../../infra/04-data/operational/supabase/docker-compose.yml)에 선언된 exact `supabase` profile 기반의 `OPTIONAL` 통합 백엔드 플랫폼이다. 13개 서비스가 PostgreSQL, Kong, Auth, REST, Realtime, Storage, Studio, Functions, analytics/logging과 pooler를 `supabase_net`에서 구성한다. 이 서비스들은 하나의 recovery unit이며 database dump만으로 Storage objects, mounted functions/config, JWT/provider settings를 복구할 수 없다.

### Current implementation

| Field | Repository-specific decision |
| --- | --- |
| Consumer and data rationale | OPTIONAL integrated backend for applications that need PostgreSQL, Auth, APIs, Realtime, objects, functions and pooling. |
| Source / updater | [Compose](../../../infra/04-data/operational/supabase/docker-compose.yml) owns 13 image declarations; coordinated upstream compatibility review is required. |
| Services / profile | 13 mapped services in frontmatter; exact `supabase`. |
| Flow / dependency | Kong fronts API paths; PostgreSQL is the metadata/data core; Storage couples metadata to object files; Supavisor pools database traffic. |
| Exposure / persistence | Kong/analytics/PostgreSQL/pooler host ports are source-declared; Studio has no direct port; `${DEFAULT_DATA_DIR}/supabase` owns data/config. |
| Environment / secrets | Compose owns public configuration keys; database, JWT, anon/service, dashboard, SMTP, vault, crypto and analytics credentials are Docker Secrets. |
| Health / resources | per-service healthchecks and dependency graph; each service uses its Compose-declared shared template, so aggregate capacity must be reviewed. |
| Security | Kong boundary, secret mounts, JWT/provider consistency, and no credential material in generated evidence. |
| Backup / upgrade | PostgreSQL + Storage + config/functions + Auth/secret references form one recovery set; upstream update config backup alone is insufficient. |
| License / edition | The self-hosted stack combines components with repository-documented licenses; review the exact component/image set before redistribution or managed-service use. |

### Usage Type

`system-guide | operational-reference`

### Target Audience

- Operator
- Developer
- SRE
- AI Agent

### Purpose

이 가이드는 Supabase stack의 현재 서비스 구성, 접근 경로, secret 경계, 일반 확인 방법을 설명한다. 사용자는 직접 Studio host port를 가정하지 않고, compose가 선언한 Kong/API 경로와 운영 runbook을 기준으로 상태를 확인해야 한다.

### Prerequisites

- Repository checkout at the project root.
- Docker Compose access on the local or approved infrastructure host.
- `DEFAULT_DATA_DIR` points to prepared Supabase config, storage, function, log, and database paths.
- Docker Secret files referenced by the stack are prepared; secret values must not be copied into docs, logs, or commits.

### Step-by-step Instructions

1. 현재 compose surface를 확인한다.

   ```bash
   docker compose --profile supabase config --services
   ```

   Expected services: `studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `imgproxy`, `meta`, `functions`, `analytics`, `db`, `vector`, `supavisor`.

2. 공개 접근 경로를 확인한다.

   - Kong HTTP: `${SUPABASE_KONG_HTTP_HOST_PORT:-8000}:8000/tcp`
   - Kong HTTPS: `${SUPABASE_KONG_HTTPS_HOST_PORT:-8443}:8443/tcp`
   - Analytics: `${SUPABASE_ANALYTICS_HOST_PORT:-4000}:4000`
   - Postgres/pooler: `${SUPABASE_POSTGRES_HOST_PORT:-5432}:5432`, `${SUPABASE_POOLER_PROXY_PORT_TRANSACTION_HOST_PORT:-6543}:6543`
   - Studio has no direct host port in the current compose file; use the approved route exposed by Kong and stack configuration.

3. 서비스 상태를 확인한다.

   ```bash
   docker compose --profile supabase ps studio kong auth rest realtime storage db analytics supavisor
   ```

4. 데이터와 config 경계를 확인한다.

   Supabase runtime files are mounted from `${DEFAULT_DATA_DIR}/supabase/...`, including Kong config, storage, functions, database init SQL, logs, and pooler config. Update implementation docs and operations docs together when these mounts change.

5. recovery inventory는 PostgreSQL roles/schema/data, Storage metadata와 object files, mounted Kong/functions/pooler configuration, Auth/JWT/SMTP/provider settings를 별도 protected artifacts로 기록한다. 빈 격리 stack에서 이들을 coherent set으로 복원한 뒤에만 recoverable로 판정한다.

### Common Pitfalls

- Assuming Studio is available through a direct local host port; the current compose file does not publish one.
- Bypassing Kong for public API access without an approved implementation change.
- Writing `supabase_anon_key`, `supabase_service_key`, JWT secrets, dashboard credentials, SMTP passwords, or database passwords into docs or evidence.
- Treating generated Kong or database config as documentation-only state; it is runtime configuration mounted from `${DEFAULT_DATA_DIR}`.
- Using the self-hosted update config backup as a database or Storage backup; upstream documents that update backup as configuration-only.

## Common Checks

- `docker compose --profile supabase config --quiet`
- `docker compose --profile supabase ps`
- Search the paired guide/policy/runbook for direct Studio host-port assumptions, old Compose CLI spelling, or template copyright remnants before committing.
- Expected result: compose renders, services match the compose file, and stale Studio/direct-port or template remnants are absent.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은
[recovery runbook](../runbooks/0029-supabase.md)을 따른다.

## Traceability

- Declared parent: [Supabase Operations Policy](../policies/0029-supabase.md) (`POL-0029`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Policy](../policies/0029-supabase.md) (`POL-0029`), [Runbook](../runbooks/0029-supabase.md) (`RUN-0029`)

## Related Documents

- [Supabase self-hosted restore guidance](https://supabase.com/docs/guides/self-hosting/restore-from-platform)
- [Supabase self-hosted update guidance](https://supabase.com/docs/guides/self-hosting/updating)
- [Supabase source and licenses](https://github.com/supabase/supabase)

- [Operations index](../README.md)
- [Operations policy](../policies/0029-supabase.md)
- [Recovery runbook](../runbooks/0029-supabase.md)
- [Infrastructure service README](../../../infra/04-data/operational/supabase/README.md)
- [Compose implementation: infra/04-data/operational/supabase/docker-compose.yml](../../../infra/04-data/operational/supabase/docker-compose.yml)
