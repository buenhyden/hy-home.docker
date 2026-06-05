---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/operational/mng-db.md -->

# Management Database Usage Guide

> Use this guide to understand and verify the current `mng-db` implementation.

---

## Usage

### Overview

`mng-db`는 플랫폼 관리 서비스가 공유하는 PostgreSQL/Valkey 운영 데이터 계층이다. 현재 구현은 `infra/04-data/operational/mng-db/docker-compose.yml`의 `mng` 및 `dev` profile로 선언되며, Keycloak, n8n, Airflow, Terrakube, SonarQube, 기본 service DB를 위한 PostgreSQL role/database와 Valkey cache를 제공한다.

### Usage Type

`system-guide | operational-reference`

### Target Audience

- Operator
- Developer
- SRE
- AI Agent

### Purpose

이 가이드는 `mng-db`의 현재 compose 구조, 네트워크 경계, 초기화 job, 일반 점검 절차를 이해하고 상위 관리 서비스와의 연결을 검토할 수 있게 한다.

### Prerequisites

- Repository checkout at the project root.
- Docker Compose access on the local or approved infrastructure host.
- Docker Secret files referenced by the compose file are prepared; secret values must not be copied into docs, logs, or commits.
- Service data paths referenced through `DEFAULT_MANAGEMENT_DIR` are available to the runtime host.

### Step-by-step Instructions

1. 현재 compose surface를 확인한다.

   ```bash
   docker compose -f infra/04-data/operational/mng-db/docker-compose.yml --profile mng config --services
   ```

   Expected services: `mng-valkey`, `mng-valkey-exporter`, `mng-pg`, `mng-pg-init`, `mng-pg-exporter`.

2. 네트워크 경계를 확인한다.

   - `mng-pg` and `mng-valkey`: `infra_net`, `k3d-hyhome`
   - `mng-pg-init`, `mng-pg-exporter`, `mng-valkey-exporter`: `infra_net`
   - The legacy shared-network name is not part of the current implementation.

3. PostgreSQL 초기화 범위를 확인한다.

   `mng-pg-init` applies `pg/init-scripts/init_users_dbs.sql` and maintains logical databases for `n8n`, `keycloak`, `airflow`, `terrakube`, `sonarqube`, and the service DB declared by `SERVICE_POSTGRES_DB` with the corresponding service role.

4. 일반 상태를 확인한다.

   ```bash
   docker compose -f infra/04-data/operational/mng-db/docker-compose.yml --profile mng ps mng-pg mng-valkey mng-pg-exporter mng-valkey-exporter
   ```

### Common Pitfalls

- Treating `mng-db` as the HA PostgreSQL cluster. HA production data belongs to `infra/04-data/relational/postgresql-cluster/`.
- Referencing legacy shared-network names; the current `mng-db` compose uses `infra_net` and `k3d-hyhome`.
- Writing secret values, generated passwords, or token material into documentation while describing `/run/secrets/` usage.
- Running the init job without first confirming the compose render and linked policy/runbook context.

## Common Checks

- `docker compose -f infra/04-data/operational/mng-db/docker-compose.yml --profile mng config`
- `docker compose -f infra/04-data/operational/mng-db/docker-compose.yml --profile mng ps`
- Search the paired guide/policy/runbook for legacy network names or old Compose CLI spelling before committing.
- Expected result: compose renders, documented services match the compose file, and stale network or command references are absent.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은
[recovery runbook](../../../runbooks/04-data/operational/mng-db.md)을 따른다.

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/04-data/operational/mng-db.md)
- [Recovery runbook](../../../runbooks/04-data/operational/mng-db.md)
- [Infrastructure service README](../../../../../infra/04-data/operational/mng-db/README.md)
