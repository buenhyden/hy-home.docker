---
title: "Datastore Observation Split"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0224"
parent_ids:
- "REQ-0004"
- "REQ-0007"
- "AD-0004"
- "AD-0006"
created: "2026-10-09"
---

# Datastore Observation Split

## Overview

SPEC-0213 gave the DEV exporters their own monitor accounts, but the MNG
exporters still read the PostgreSQL administrator password and the shared
Valkey password, the latter on the exporter's command line. The DEV
PostgreSQL role held all of `pg_monitor` and the Valkey monitor role could
run `SLOWLOG GET`, which returns command arguments. Prometheus could not tell
MNG from DEV series except by job name, every datastore alert treated a DEV
target that was stopped on purpose as a failure, and the PostgreSQL and
Valkey dashboards filtered on Kubernetes labels that never existed here, so
they showed no data. Prompt 14 asks for dedicated monitor roles on both
scopes, scope and engine labels, alerts that separate a scrape failure from a
database failure and an intentional stop from an outage, and per-scope
dashboards on the existing Prometheus and Grafana.

## Scope

In scope: the DEV and MNG PostgreSQL monitor roles and provision jobs, the
DEV and MNG Valkey monitor ACL rules, the four exporter definitions, the
Prometheus datastore jobs, a start script that renders the DEV targets with
their declared state, the datastore alert rules, the PostgreSQL and Valkey
dashboards, their tests and isolated rehearsal, the affected READMEs and
Runbooks, and the HOME rollout. Out of scope: a new time-series store, writing
metrics to a database, renaming exporter metrics, TLS between exporters and
the databases (both servers run without TLS on internal networks), and the
other Valkey consumers' accounts.

## Contracts

1. PostgreSQL monitor roles. `dev_pg_monitor` and `mng_pg_monitor` are marked
   LOGIN roles with `pg_read_all_stats`, `pg_read_all_settings` and EXECUTE on
   `pg_ls_waldir()`, measured as what every enabled collector needs; they are
   not `pg_monitor` members and have no other privilege; a run fails if any
   other membership, direct or through another role, is present. Sessions are
   read-only with a 10 s statement timeout and three connections. Each
   provision run sets the password from the secret (rotation) and refuses a
   secret outside a 16 to 512 character base64 alphabet before any role change,
   because postgres_exporter logs a malformed DSN with the password in it. The
   role can read server-wide activity and settings, including other sessions'
   query text in `pg_stat_activity`; that is the observation boundary.
2. Valkey monitor roles. `devmonitor` and `mngmonitor` have
   `-@all +ping +info +command|info +slowlog|len +commandlog|len`, each with
   its own secret. The exporters disable `CONFIG`, `CLIENT SETNAME` and the
   latency histogram; `SLOWLOG GET` stays refused and is the only exporter
   entry in the ACL log. redis_exporter has no per-collector signal, so a lost
   Valkey grant is caught by the rehearsal's ACL log check, not by an alert.
3. Exporter inputs. No exporter mounts an administrator secret. The
   PostgreSQL exporters read `DATA_SOURCE_URI`, `DATA_SOURCE_USER` and
   `DATA_SOURCE_PASS_FILE`; the Valkey exporters put the password in their own
   environment, never on the command line. Exporters keep the read-only root,
   dropped capabilities, `no-new-privileges`, the low resource template and no
   host port.
4. Scrape labels. The four jobs keep their names, `cluster`, `namespace` and
   `domain`, and add `db_scope` (`mng`|`dev`), `db_engine`
   (`postgresql`|`valkey`) and `expected_state`. MNG targets are static with
   `expected_state="on"`. DEV targets are rendered at Prometheus start from
   `PROMETHEUS_DEV_DATA_EXPECTED` (`on`|`off`); any other value stops the start,
   and Compose supplies `on` when the key is missing, so a forgotten key
   alerts rather than silences.
5. Alerts. `up` is the scrape and `pg_up`/`redis_up` the database. MNG down
   alerts are critical; DEV down alerts are warnings that fire only with
   `expected_state="on"`, and the shared memory, rejected-connection and
   restart alerts are warnings for DEV. A MNG outage pages once: the exporter
   error alert stays quiet while `pg_up` is 0. A DEV target answering for an hour while declared
   off, a missing target, a failed collector and a scrape over 5 s are
   reported. No absent alert is removed.
6. Dashboards. The PostgreSQL and Valkey dashboards select by `db_scope` and
   open with a MNG/DEV comparison row; existing panels keep their queries
   apart from the label filter.

## Acceptance Criteria

1. Unit tests cover the monitor SQL and ACL rules, both exporter definitions,
   the scrape labels, the start script's states and refusals, the Prometheus
   tmpfs ownership, and the alert scoping.
2. The isolated rehearsal, run against the Compose-rendered exporters, shows
   every collector succeeding, network logins with refused wrong passwords and
   writes, refused Valkey key and config commands, a wrong exporter password
   reported as `pg_up`/`redis_up` 0 while the exporter stays up, a lost
   collector grant reported and restored, a database stop and recovery,
   rotation, a refused non-base64 secret, secret-free metrics and logs, scope
   labels in Prometheus, an exporter stop, and promtool alert scenarios.
3. On HOME both scopes are scraped with their labels, the monitor roles hold
   only their grants, the exporter ACL log shows only `SLOWLOG GET`, every MNG
   Valkey consumer reconnects, an exporter stop while declared on raises a
   pending DEV alert and recovers, and a declared-off stop raises none.
4. The changed gate, the staged style check and `candidate-quality` pass.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-datastore-observation-split.md)
- [DEV data and monitor accounts](../0213-dev-data-and-influx-retirement/spec.md)
- [RedisInsight Valkey inspection](../0223-redisinsight-valkey-inspection/spec.md)
- [Request baseline](../0212-request-baseline-and-reconciliation/spec.md)
