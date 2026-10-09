---
title: "RedisInsight Valkey Inspection"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0223"
parent_ids:
- "REQ-0004"
- "REQ-0005"
- "AD-0004"
created: "2026-10-09"
---

# RedisInsight Valkey Inspection

## Overview

RedisInsight reached `dev-valkey` with the `devadmin` superuser and `mng-valkey`
with the shared management password, both stored unencrypted. It listened on
every attached network, so any peer on `mng_data_net`, `dev_data_net`,
`n8n_net` or `airflow_net` could open the UI around Traefik SSO, and its
health check only tested that `/data` existed. SPEC-0212 item 16 assigns
RedisInsight access to `dev-valkey` here, and the owner asked that MNG Valkey
receive the same treatment.

## Scope

In scope: the DEV and MNG Valkey ACL renderers and their service roles, the
MNG Valkey start path, RedisInsight networks, listener, pre-set connections,
secrets, encryption and health check, their tests and isolated rehearsal, the
RedisInsight Guide, Policy and Runbook, the affected READMEs, the HOME rollout
and the review of every service that uses either Valkey. Out of scope: exporter
accounts and scrape labels (prompt 14), a write role, and the optional
dedicated n8n, Airflow and OAuth2 Proxy Valkey stores.

## Contracts

1. Inspector roles. `devinspector` and `mnginspector` have
   `~* resetchannels -@all +@read +@connection -@dangerous +info`, measured
   against RedisInsight 3.8.0: the key browser, key details, values and the
   overview work; writes, `KEYS`, `CONFIG`, `ACL`, `FLUSH*`, `EVAL` and
   `PUBLISH` are refused. Each role has its own secret, and a renderer refuses
   any two roles or projects sharing one. Application accounts keep their
   `SCAN` ban.
2. MNG compatibility. MNG Valkey renders its ACL at start; the `default` user
   keeps `mng_valkey_password`, so every existing consumer authenticates as
   before.
3. Listener scope. RedisInsight listens only on its fixed `edge_net` address,
   Traefik uses `edge_net`, and data-network peers cannot reach the UI port.
   `n8n_net` and `airflow_net` are dropped.
4. Pre-set connections. `DEV / dev-valkey` and `MNG / mng-valkey` are recreated
   on every start from environment variables; `start.sh` loads the inspector
   passwords and `RI_ENCRYPTION_KEY` from secrets, and stored passwords are
   encrypted. Admin, monitor and application secrets are never stored.
5. Trust boundary. The key browser shows every key name in a database, so
   RedisInsight access is an administrator boundary; `MATCH` or prefix filters
   are not project isolation.
6. Health. The container health check reads `/api/health/`; database
   connectivity is a separate check.

## Acceptance Criteria

1. Renderer tests cover each role line, refused shared secrets, refused
   malformed or missing secrets, and the MNG `default` user.
2. The isolated rehearsal covers UI health and listener scope, a data-network
   bypass attempt, distinct pre-set connections, reads, refused writes and
   commands, encrypted stored passwords, a DEV outage and recovery, and
   inspector rotation.
3. On HOME both connections work through the inspectors, writes are refused,
   the bypass is refused, unauthenticated requests go to SSO, a DEV outage
   shows an error and recovers, inspector rotation works, and no admin or
   inspector secret remains readable in the RedisInsight store.
4. Every service that uses MNG or DEV Valkey is reviewed for impact.
5. The changed gate, the staged style check and `candidate-quality` pass.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-redisinsight-valkey-inspection.md)
- [Request baseline](../0212-request-baseline-and-reconciliation/spec.md)
- [DEV data](../0213-dev-data-and-influx-retirement/spec.md)
