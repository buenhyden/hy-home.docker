---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/operational/supabase.md -->

# Supabase Usage Guide

> Use this guide to understand and verify the current self-hosted Supabase stack.

---

## Usage

### Overview (KR)

`supabase`는 `infra/04-data/operational/supabase/docker-compose.yml`에 선언된 `data` profile 기반의 통합 백엔드 플랫폼이다. 현재 구현은 PostgreSQL, Kong Gateway, Auth, REST, Realtime, Storage, Studio, Edge Functions, analytics/logging, pooler를 `infra_net` 안에서 구성하고, 외부 접근은 compose에 선언된 Kong 및 일부 관리 포트를 통해 제한한다.

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
   docker compose -f infra/04-data/operational/supabase/docker-compose.yml --profile data config --services
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
   docker compose -f infra/04-data/operational/supabase/docker-compose.yml --profile data ps studio kong auth rest realtime storage db analytics supavisor
   ```

4. 데이터와 config 경계를 확인한다.

   Supabase runtime files are mounted from `${DEFAULT_DATA_DIR}/supabase/...`, including Kong config, storage, functions, database init SQL, logs, and pooler config. Update implementation docs and operations docs together when these mounts change.

### Common Pitfalls

- Assuming Studio is available through a direct local host port; the current compose file does not publish one.
- Bypassing Kong for public API access without an approved implementation change.
- Writing `supabase_anon_key`, `supabase_service_key`, JWT secrets, dashboard credentials, SMTP passwords, or database passwords into docs or evidence.
- Treating generated Kong or database config as documentation-only state; it is runtime configuration mounted from `${DEFAULT_DATA_DIR}`.

## Common Checks

- `docker compose -f infra/04-data/operational/supabase/docker-compose.yml --profile data config`
- `docker compose -f infra/04-data/operational/supabase/docker-compose.yml --profile data ps`
- Search the paired guide/policy/runbook for direct Studio host-port assumptions, old Compose CLI spelling, or template copyright remnants before committing.
- Expected result: compose renders, services match the compose file, and stale Studio/direct-port or template remnants are absent.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은
[recovery runbook](../../../runbooks/04-data/operational/supabase.md)을 따른다.

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/04-data/operational/supabase.md)
- [Recovery runbook](../../../runbooks/04-data/operational/supabase.md)
- [Infrastructure service README](../../../../../infra/04-data/operational/supabase/README.md)
