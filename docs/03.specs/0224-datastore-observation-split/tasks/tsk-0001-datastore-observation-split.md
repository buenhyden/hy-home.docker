---
title: "Datastore Observation Split Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0224-TSK-0001"
parent_ids:
- "SPEC-0224-PLAN-0001"
created: "2026-10-09"
---

# Datastore Observation Split Task

## Objective

Observe DEV and MNG PostgreSQL and Valkey through dedicated least-privilege
monitor accounts, tell the two scopes apart in Prometheus and Grafana, and
alert on real failures without paging for an intentional DEV stop.

## Inputs and Authorization

On 2026-10-09 the owner asked to execute prompt 14 (DEV PostgreSQL and Valkey
exporters and the DEV/MNG observation split), with the earlier instructions
that DEV and MNG datastores receive the same treatment and that every service
using MNG or DEV Valkey be reviewed for impact. The work started from the
SPEC-0223 head `b3d60383b` while PR #399 waited on `candidate-quality`; the
branch is rebased onto `main` once SPEC-0223 merges. This package is the
single writer of both Valkey ACL renderers, both monitor provisioners, the
four exporter definitions, the Prometheus datastore jobs and the datastore
alert rules. Prompt 14 names the MNG monitor accounts, so their two secrets
were issued on HOME for this change.

## Work Log

### Baseline

DEV already had `dev-pg-exporter` and `dev-valkey-exporter` on monitor
accounts (SPEC-0213 TSK-0002 W5), scraped by Prometheus. Gaps found:

| Item | Before |
| --- | --- |
| `mng-pg-exporter` | Built a DSN from `mng_postgres_password` (administrator) in a shell entrypoint |
| `mng-valkey-exporter` | Passed `mng_valkey_password` (shared `default`) as `-redis.password` on argv |
| `dev_pg_monitor` | Member of all of `pg_monitor`; password never rotated by a rerun |
| `devmonitor` | Also allowed `SLOWLOG GET` (returns command arguments), `CONFIG GET`, `CLIENT LIST` |
| Scrape labels | Scope only implied by job name; no engine label |
| Alerts | `ValkeyDown` covered only the MNG exporter; `PostgresDown` was unscoped; no way to mark DEV as intentionally off |
| Dashboards | PostgreSQL filtered on `release` and `kubernetes_namespace`, Valkey on `namespace` variables built for Kubernetes; the PostgreSQL panels were empty |

HOME before the change: all four jobs `up 1`, `pg_up`/`redis_up` 1, scrape
times 0.097 s and 0.091 s (PostgreSQL) and 0.045 s and 0.025 s (Valkey),
exporters at 8 to 11 MiB and under 2 % CPU.

### Measurement

Isolated runs of the pinned exporters against the pinned servers on an
internal network:

- `redis_exporter` with only `+ping +info` still reports `redis_up 1` and no
  scrape error; the ACL log lists the commands it tries. With
  `-config-command=- -set-client-name=false -exclude-latency-histogram-metrics`
  it needs `COMMAND INFO`, `SLOWLOG LEN` and `COMMANDLOG LEN` besides `PING`
  and `INFO`; `SLOWLOG GET` is then its only refused command (one aggregated
  ACL log entry). No dashboard or alert uses `redis_config_*`, slowlog,
  latency or client metrics.
- `postgres_exporter` with `pg_read_all_stats` and `pg_read_all_settings`
  fails only the `wal` collector (`pg_ls_waldir`); adding EXECUTE on that
  function makes every collector succeed with `pg_monitor` absent.
- Passwords: base64, base64url and hex work. A space, or a mix of quote,
  double quote and backslash, makes the exporter build a malformed key/value
  DSN, report `pg_up 0`, and log the DSN including part of the password.
  HOME's existing DEV monitor secrets are base64url.

### W1 Monitor Roles

`mng-pg-monitor-provision` runs `pg/provision/monitor.sql` through the
existing `run-feature-provision.sh`; `dev-pg-monitor-provision` keeps its
Python wrapper with the same SQL contract. Both create the marked role only
when absent, refuse an unmarked or elevated role of that name, refuse a
non-base64 secret before any change, set the password from the secret on
every run, grant the three measured privileges, revoke `pg_monitor` if held,
and set `default_transaction_read_only`, a 10 s statement timeout and three
connections. `mngmonitor` joins the MNG ACL renderer with the narrowed rule,
and `devmonitor` takes the same rule. The ECC pre-commit hook flagged the
psql variable form `PASSWORD :'var'` as a credential; the MNG SQL uses
`format(... %L)` with `\gexec` like the Grafana provisioner instead of
bypassing the hook. Two secrets and their rows (PG-037, CACHE-026) were
added; POL-0078 and the service inventory list the new job.

### W2 Exporters

`mng-pg-exporter` drops its shell entrypoint and reads
`DATA_SOURCE_URI`/`DATA_SOURCE_USER`/`DATA_SOURCE_PASS_FILE` after the
provision job completes. Both Valkey exporters authenticate as their monitor
user with the password exported into their own environment and run with the
three measured flags. `redis_exporter` reads a JSON password map from
`-redis.password-file`; rendering one would put the same value in a second
file with no gain over the process environment, so the environment is kept.

### W3 Scrape Labels

The four jobs carry `db_scope`, `db_engine` and `expected_state`. The DEV jobs
use file discovery: `prometheus/scripts/start.sh` validates
`PROMETHEUS_DEV_DATA_EXPECTED`, writes both target files beside their final
names and renames them, then execs Prometheus. A missing or unknown value
exits 64. `PROMETHEUS_DEV_DATA_EXPECTED="on"` was added to `.env.example` and,
key only, to HOME's `.env`. promtool accepts both configurations with the
rendered targets.

### W4 Alerts and Dashboards

`PostgresDown`, `ValkeyDown` and `PostgresqlExporterError` are scoped to MNG.
`DevPostgresDown`, `DevValkeyDown` and `DevDatastoreExporterDown` are warnings
gated on `expected_state="on"`. `MngDatastoreExporterDown`,
`DevDatastoreUpWhileDeclaredOff`, `DatastoreScrapeTargetMissing`,
`DatastoreCollectorFailed` and `DatastoreScrapeSlow` are new. Both dashboards
replace the Kubernetes variables with a multi-value `db_scope` variable and
add a three-panel MNG/DEV comparison row (scrape and database up with the
expected state, sessions or clients, and throughput).

### W5 Rehearsal, Consumers and HOME

The isolated rehearsal (`HYHOME_DATASTORE_OBSERVATION_REHEARSAL=1`) runs the
exporters exactly as `docker compose config` renders them. Its first run
found that the `/etc/prometheus` tmpfs was root-owned, so `start.sh`, running
as `nobody`, could not create the target directory and Prometheus would not
have started; the tmpfs now sets `uid=65534,gid=65534,mode=0755` and a unit
test pins it. After that fix 11 of 11 pass. The RedisInsight rehearsal needed
the new MNG monitor secret mounted and passes 9 of 9.

Consumer review: MNG Valkey's `default` user and password are unchanged, so
OAuth2 Proxy, n8n, Airflow, Flower, the k3d clients and Gatus are unaffected;
RedisInsight uses `mnginspector`. DEV Valkey consumers use project users,
which this change does not touch. Nothing else uses either monitor account.

HOME rollout from `8af637f3f` (detached checkout):

| Step | Result |
| --- | --- |
| MNG monitor secrets | Created at mode `0640`, 43 base64url characters; values not displayed |
| `mng-valkey` recreate | Healthy; users `default`, `mnginspector`, `mngmonitor`; consumers back: 14 redis-py, 7 go-redis, n8n and 19 unnamed `default` connections, 2 RedisInsight |
| `dev-valkey` recreate | Healthy; `devmonitor` has the narrowed rule |
| Both provision jobs | Exit 0; both roles LOGIN, not elevated, limit 3, read-only, 10 s timeout, the three grants, no `pg_monitor` |
| Exporters and Prometheus | All healthy; DEV targets rendered with `expected_state: "on"` |
| Scrapes | Four jobs `up 1` with `db_scope`, `db_engine`, `expected_state`; `pg_up`/`redis_up` 1; no failed collector; no datastore alert |
| Load | Scrape 0.107 s and 0.101 s (PostgreSQL), 0.013 s and 0.010 s (Valkey, down from 0.045 s and 0.025 s) |
| ACL log | After a reset, only `SLOWLOG GET` by `devmonitor`; MNG only `SLOWLOG GET` by `mngmonitor` |
| Network client | Both PostgreSQL monitor roles log in over the data network with read-only sessions; a wrong password fails; DDL is refused. Valkey monitor users get NOPERM for `SCAN`, `KEYS`, `CONFIG GET`, `SLOWLOG GET`; a wrong password gets WRONGPASS |
| Exporter stop, declared on | `dev-pg-exporter` stopped at 11:01:43; `up 0` at 11:01:49 and `DevDatastoreExporterDown` pending; restarted, `up 1` and `pg_up 1` at 11:02:21, alert cleared at 11:02:30 |
| Declared off | Prometheus recreated with `PROMETHEUS_DEV_DATA_EXPECTED=off`; both DEV exporters stopped at 11:02:57; both targets `up 0` with `expected_state="off"` at 11:03:12; at 11:09:30, past the 5 min window, no datastore alert existed |
| Restore | Exporters started and Prometheus recreated from `.env` (`on`); at 11:10:40 both DEV targets `up 1`, all four `pg_up`/`redis_up` 1, all healthy |
| Grafana | Both dashboards reloaded at 10:56 UTC with the `db_scope` variable and the comparison row. Run against HOME for each scope, all 46 Valkey queries and 74 of 88 PostgreSQL queries return data; the empty ones filter `!= 0` on currently zero counters (active sessions, inserts, deletes) or read `pg_stat_bgwriter` checkpoint and backend columns that PostgreSQL 17 moved to `pg_stat_checkpointer`, an upstream dashboard gap outside this package |

### W6 Documents

The MNG, DEV, DEV PostgreSQL and DEV Valkey READMEs, the Prometheus README
and the Grafana coverage table describe the monitor roles, scope labels and
expected state. Runbooks 0028 (MNG alerts and rotation), 0100 (DEV alerts and
the intentional-stop procedure) and 0045 (observation alerts) gained a
section each. The changed-document metadata check reports no violation.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Monitor roles | 1 | W1 | Provision, ACL and secret metadata tests | `262801692` | PASS | W1 Monitor Roles | accepted |
| Exporter inputs | 1 | W2 | Boundary tests | `5fa8a3eb4` | PASS | W2 Exporters | accepted |
| Scrape labels | 1 | W3 | Label and start-script tests; promtool on both configurations | `5a2733bff` | PASS | W3 Scrape Labels | accepted |
| Alerts and dashboards | 1 | W4 | Scoping and dashboard contract tests; promtool rule scenarios | `f6a0a64f8` | PASS | W4 Alerts and Dashboards | accepted |
| Prometheus tmpfs | 2 | W5 | Static test; rehearsal | `183c416e6` | PASS | W5 Rehearsal, Consumers and HOME | accepted |
| Isolated rehearsal | 2 | W5 | 11 rehearsal tests | `00fd1ff59` | PASS | W5 Rehearsal, Consumers and HOME | accepted |
| RedisInsight consumer | 2 | W5 | 9 rehearsal tests | `8af637f3f` | PASS | W5 Rehearsal, Consumers and HOME | accepted |
| HOME rollout | 3 | W5 | Probes, queries, ACL log, client inventory, exporter stop, declared-off stop, dashboard queries | `8af637f3f` | PASS | W5 Rehearsal, Consumers and HOME | accepted |
| Documents | 3 | W6 | Metadata check-changed | branch head | PASS | W6 Documents | accepted |

## Review and Completion

Not complete: W7 validation and the merge remain. The branch is based on the
SPEC-0223 head, which must merge first.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
