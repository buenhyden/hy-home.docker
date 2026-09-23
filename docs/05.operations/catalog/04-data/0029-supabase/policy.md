---
title: "Supabase Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0029"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# Supabase Operations Policy

> This policy governs the current self-hosted Supabase stack in `hy-home.docker`.

---

## Overview

이 정책은 `infra/04-data/operational/supabase`의 exact `supabase` profile stack 운영 기준을 정의한다. 핵심 통제는 Kong 중심 공개 접근, Docker Secrets, `${DEFAULT_DATA_DIR}/supabase/...` runtime mounts와 database/storage/config를 하나의 recovery unit으로 관리하는 것이다.

## Policy Scope

- **Systems**: `studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `imgproxy`, `meta`, `functions`, `analytics`, `db`, `vector`, `supavisor`
- **Configs**: `infra/04-data/operational/supabase/docker-compose.yml`, `${DEFAULT_DATA_DIR}/supabase/api/kong.yml`, storage, functions, logs, database init SQL, pooler config --quiet
- **Networks**: `supabase_net`
- **Ports**: Kong `8000`/`8443`, analytics `4000`, Postgres `5432`, pooler `6543` as declared through compose host-port variables
- **Agents**: AI agents reviewing or updating operations docs, compose references, validation evidence, or Supabase runtime boundaries

## Controls

- **Required**:
  - Supabase secrets are injected through Docker Secrets under `/run/secrets/`.
  - Public API and dashboard access must follow the compose-declared Kong route and linked stack config.
  - Documentation must state that Studio has no direct host port in the current compose file.
  - Runtime mounts under `${DEFAULT_DATA_DIR}/supabase/...` must be treated as implementation state and kept in sync with infra README and operations docs.
  - JWT, anon, service-role, dashboard, SMTP, database, vault, and crypto key values must never be written into documentation or evidence.
  - A backup set must include PostgreSQL globals/roles, schema and data; Storage metadata plus object files; mounted Kong/functions/pooler configuration; and protected Auth/JWT/SMTP/provider settings with versions, checksums, retention and restore evidence.
  - Restore rehearsal must use a fresh isolated stack. Restore roles/schema/data in dependency order, reconcile Storage objects with metadata, apply configuration/secrets separately, and verify Auth, REST, Realtime, Storage, Functions and pooler paths.
  - The update guide's configuration backup is not a database or Storage backup. Upgrade/removal requires a coherent restore-tested set, compatibility review, capacity check and explicit approval.
- **Allowed**:
  - Metadata-only compose validation with `docker compose ... config --quiet`.
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

- Run `docker compose --profile supabase config --quiet` after changing compose-facing documentation.
- Run `python3 scripts/validation/check-document-links.py --mode all` after policy, guide, runbook, README, or link updates.
- Search updated docs for direct Studio host-port assumptions, old Compose CLI spelling, template copyright remnants, and secret material before committing.

## Review Cadence

Review on any change to Supabase compose services, ports, profiles, networks, secret refs, runtime mounts, Kong routing, or linked operations documents. Otherwise review during the regular Stage 05 operations audit.

---

## Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](guide.md) (`GDE-0029`), [Runbook](runbook.md) (`RUN-0029`)

## Related Documents

- [Compose implementation: infra/04-data/operational/supabase/docker-compose.yml](../../../../../infra/04-data/operational/supabase/docker-compose.yml)

- [Supabase self-hosted restore guidance](https://supabase.com/docs/guides/self-hosting/restore-from-platform)
- [Supabase self-hosted update guidance](https://supabase.com/docs/guides/self-hosting/updating)
- [Supabase source and licenses](https://github.com/supabase/supabase)

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
- [Infrastructure service README](../../../../../infra/04-data/operational/supabase/README.md)
