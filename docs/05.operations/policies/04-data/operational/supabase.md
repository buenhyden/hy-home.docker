---
status: active
---
<!-- Target: docs/05.operations/policies/04-data/operational/supabase.md -->

# Supabase Operations Policy

> This policy governs the current self-hosted Supabase stack in `hy-home.docker`.

---

## Overview

이 정책은 `infra/04-data/operational/supabase`의 data profile stack 운영 기준을 정의한다. 핵심 통제는 Kong 중심의 공개 접근, Docker Secrets 기반 credential 관리, `${DEFAULT_DATA_DIR}/supabase/...` runtime mount 관리, 그리고 guide/policy/runbook 간 현재 구현 정합성 유지이다.

## Policy Scope

- **Systems**: `studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `imgproxy`, `meta`, `functions`, `analytics`, `db`, `vector`, `supavisor`
- **Configs**: `infra/04-data/operational/supabase/docker-compose.yml`, `${DEFAULT_DATA_DIR}/supabase/api/kong.yml`, storage, functions, logs, database init SQL, pooler config
- **Networks**: `infra_net`
- **Ports**: Kong `8000`/`8443`, analytics `4000`, Postgres `5432`, pooler `6543` as declared through compose host-port variables
- **Agents**: AI agents reviewing or updating operations docs, compose references, validation evidence, or Supabase runtime boundaries

## Controls

- **Required**:
  - Supabase secrets are injected through Docker Secrets under `/run/secrets/`.
  - Public API and dashboard access must follow the compose-declared Kong route and linked stack config.
  - Documentation must state that Studio has no direct host port in the current compose file.
  - Runtime mounts under `${DEFAULT_DATA_DIR}/supabase/...` must be treated as implementation state and kept in sync with infra README and operations docs.
  - JWT, anon, service-role, dashboard, SMTP, database, vault, and crypto key values must never be written into documentation or evidence.
- **Allowed**:
  - Metadata-only compose validation with `docker compose ... config`.
  - Read-only service health/log checks that do not expose secret values.
  - Approved JWT or dashboard credential rotation when backed by task/incident evidence and corresponding runbook steps.
  - Kong host-port access using the declared `SUPABASE_KONG_HTTP_HOST_PORT` and `SUPABASE_KONG_HTTPS_HOST_PORT` variables.
- **Disallowed**:
  - Assuming direct Studio access through an unpublished local host port.
  - Bypassing Kong for public Supabase API exposure without approved implementation and documentation updates.
  - Committing generated Kong config with embedded secret values.
  - Performing destructive database restore, storage deletion, or credential rotation as a documentation-only action.

## Exceptions

Exceptions require explicit owner or user approval and must record scope, commands, affected services, secret-safety considerations, validation output, and rollback/escalation state in related task or incident evidence.

## Verification

- Run `docker compose -f infra/04-data/operational/supabase/docker-compose.yml --profile data config` after changing compose-facing documentation.
- Run `bash scripts/validation/check-repo-contracts.sh` after policy, guide, runbook, README, or link updates.
- Run `bash scripts/validation/check-doc-implementation-alignment.sh` when the change is part of implementation-vs-doc drift remediation.
- Search updated docs for direct Studio host-port assumptions, old Compose CLI spelling, template copyright remnants, and secret material before committing.

## Review Cadence

Review on any change to Supabase compose services, ports, profiles, networks, secret refs, runtime mounts, Kong routing, or linked operations documents. Otherwise review during the regular Stage 05 operations audit.

---

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/operational/supabase.md)
- [Recovery runbook](../../../runbooks/04-data/operational/supabase.md)
- [Infrastructure service README](../../../../../infra/04-data/operational/supabase/README.md)
