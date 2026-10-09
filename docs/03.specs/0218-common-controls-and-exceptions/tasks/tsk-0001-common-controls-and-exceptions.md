---
title: "Common Controls and Exceptions Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0218-TSK-0001"
parent_ids:
- "SPEC-0218-PLAN-0001"
created: "2026-10-09"
---

# Common Controls and Exceptions Task

## Objective

Check every root and LAB service's effective controls against exact
exceptions, fix the templates and leaves where the defaults were wrong, and
record resource limits honestly as budgets or measurements.

## Inputs and Authorization

The current user request on 2026-10-09 asks to execute prompt 05 of the
analysis pack (common resource, permission and exception model) with
per-unit commits and a per-Spec PR merge. Baseline `main` `abfe94cca`. The
registry issues SPEC-0218. HOME recreation of running services is not part
of this request; changed definitions apply when the owner recreates them.

## Work Log

### Starting State

Rendering the root with every profile and the eight LAB entrypoints gives 162
services. Against the controls this package checks, 160 had no PID limit, 42
carried the secrets group without reading a secret, 15 kept the default
capability set (`ollama`, `surrealdb` and 13 LAB DB nodes), 7 daemons had no
healthcheck, `ollama` also lacked `no-new-privileges` and `init`, and 96 have
a writable root filesystem. Both shell validators rendered only the `core`
profile, so most of this was never checked. The registry keyed exceptions by
service name only: `pg-0`, `pg-1`, `pg-2` and `etcd-*` named LAB services
the root render never contains, and QW-005 required every service to declare
a Docker secret.

### W1 Schema v2 and Validator

`scripts/validation/compose_controls.py` renders all nine models and checks
registered controls against schema v2 entries keyed by scope, Compose file,
service and control. `check-template-security-baseline.sh` now runs it; it
also keeps the template-adoption check. `check-quickwin-baseline.sh`, its
gate node, aggregate, manifest record and fixtures retire, because its
checks (restart, healthcheck, no-new-privileges, CPU, memory) are enforced
here and its secret rule was wrong. The v1 sections became 35 exact entries.
Ten unit tests cover each enforced control, lifecycle classification, exact
values, root and LAB distinction and every registry defect. Commit
`9fada6380`.

### W2 Healthchecks

The statsd and Valkey exporters check their metrics endpoint with `wget`,
which their images contain; `dcgm-exporter` has bash but no `head`, `grep` or
HTTP client, so it reads the status line through `/dev/tcp`; the Flink task
manager checks its registration with the job manager; the LAB Mongo Express
checks its listener. Each command passed in its exact image (Flink's shares
the job manager's image and was not run); the MongoDB LAB later reached
healthy with it. Seven exceptions retired. Commit `e00181953`.

### W3 Secrets Group

The shared base no longer grants `SECRETS_GID`; the 119 leaves that read a
secret or a bind under a secrets directory declare it, Traefik and
oauth2-proxy beside their certificate group. Of the 55 running HOME services,
37 keep their groups and 18 lose 1000 on recreation; none of their mounts
holds a file readable only through that group. Commit `e87d4f6c3`.

### W4 Conftest URL Credentials

The literal-secret rule read only secret-named keys and accepted any value
containing `://`. A URL with a literal userinfo password or a secret-named
query parameter is now denied under every key; interpolated passwords, plain
endpoints and secret paths pass. Two new policy tests (one fails against the
previous policy), and the corpus now includes `labs/*.yml`: 18 policy tests
and 308 corpus checks pass. Commits `558f1fcee`, `7356509d4`.

### W5 Capabilities and Data Group

The DB templates drop all capabilities. LAB runs set each leaf:

| Service | Capabilities added | Evidence |
| --- | --- | --- |
| MongoDB, OpenSearch nodes, root SurrealDB | none beyond the existing set | LAB green or ready with none |
| Cassandra | `CHOWN`, `FOWNER`, `SETGID`, `SETUID` | 1 node `UN` |
| CouchDB | plus `DAC_OVERRIDE` | `vm.args` permission denied without it; 3 of 3 nodes with it |
| Spilo (`pg-*`) | plus `DAC_OVERRIDE` | `chown` could not read `pgroot/data` without it; 3 members, 1 leader with it |

The same runs exposed a gap in W3: group 1000 is also the host data group.
etcd failed with permission denied on `/etcd-data`, and on HOME OpenBao
(`/openbao/data`), its agent (`/openbao/agent`, `/openbao/out`) and
Pyroscope (`/var/lib/pyroscope`) write `1000:1000` mode-775 directories only
through it. They keep the group as recorded exceptions; re-owning OpenBao's
Raft data on HOME is a separate decision. Commit `6d7026084`.

### W6 GPU Template

`template-stateful-ai-high` had no security fields. With `cap_drop: ALL`,
`no-new-privileges` and `init`, `ollama/ollama:0.40.0` detected the GTX 1060
through CUDA and loaded `tev1:0.8b` onto it (KV and compute buffers on
`CUDA0`); the template now extends the service defaults. `init` and `gpu`
are enforced; the GPU check also sees `gpus:` and `runtime: nvidia`, which
found ComfyUI. Commit `23b40d548`.

### W7 Process Limits

Measurements available on 2026-10-09: an idle `docker stats` of the running
HOME services, the peak PID count of every LAB container sampled every 3 s
through startup, and seven days of cAdvisor memory, throttling and OOM data
in Prometheus. No load, backfill, backup, restore or concurrent GPU run was
measured, so the limits are initial budgets:

| Tier | `pids_limit` | Highest observed |
| --- | --- | --- |
| dev | 128 | none running |
| low | 256 | `flower` 23 |
| med | 512 | `grafana` 122 at idle |
| high and DB | 1024 | `kafka-1` 121 at idle, LAB Kafka 128 at startup |
| LAB OpenSearch, Cassandra | 2048 | 64 and 104 at startup |

Every LAB ran under these limits with at least 5.2 times headroom, and the
running HOME services have at least 4.2 times. Commit `e0741bd28`.

Other seven-day observations, recorded as candidates, not changes: no OOM
event in any container; `prometheus` peaked at 1512 MiB of its 2 GiB limit;
`node-exporter` was CPU-throttled in 44% of periods at 0.5 CPU yet its
slowest scrape took 1.0 s against the 10 s default timeout;
`mng-valkey-exporter` was throttled in 16% of periods. A change needs a
latency or error target that these limits are shown to miss.

### W8 Documents and Validation

POL-0001, the operations runbook, the script manifest, the gate contract and
this package describe the new validator; the Spec index and registry issue
SPEC-0218. The first changed-profile run failed only in
`test_secret_metadata_sync`: the LAB entrypoints used `SECRETS_GID`, which
`labs/.env.example` did not declare, and declaring it broke the rule that LAB
keys stay disjoint from root keys. The LAB files now use `LAB_SECRETS_GID`
(commits `66ed30f78`, `3aed94faa`). The rerun of
`python3 scripts/validation/run-ci-gate.py --profile changed --local-only` in
a clean worktree at `3aed94faa`, soft-reset to `abfe94cca`, exited 0: 13 test
runs passed (1,726 tests); 28 tests skipped as the gate contract's declared
Docker rehearsals (backup, CDC, integration, mail, PostgreSQL, SeaweedFS,
SSO), which this run did not execute. The SPEC-0212 ledger is unchanged; no
ledger item maps to this package alone.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Validator and schema | 1, 2 | W1 | Ten unit tests; validator on the tree | `9fada6380` | PASS | W1 Schema v2 and Validator | accepted |
| Healthchecks | 3 | W2 | Exact-image commands; MongoDB LAB healthy | `e00181953` | PASS | W2 Healthchecks | accepted |
| Secrets group | 3 | W3 | Group comparison and mount scan of running HOME services | `e87d4f6c3` | PASS | W3 Secrets Group | accepted |
| URL credentials | 4 | W4 | Policy tests RED then GREEN; corpus | `558f1fcee` | PASS | W4 Conftest URL Credentials | accepted |
| Capabilities | 2, 3 | W5 | LAB runs with none, four and five capabilities | `6d7026084` | PASS | W5 Capabilities and Data Group | accepted |
| GPU template | 3 | W6 | Exact-image GPU run | `23b40d548` | PASS | W6 GPU Template | accepted |
| PID budgets | 3 | W7 | All LABs under the limits; HOME headroom | `e0741bd28` | PASS | W7 Process Limits | accepted |
| Validation | 5 | W8 | Changed gate, exit 0 | `3aed94faa` | PASS | W8 Documents and Validation | accepted |

## Review and Completion

Not complete. Open for the owner:

- Recreate HOME services to apply the definitions; the first Open WebUI
  recreation also re-keys sessions (SPEC-0204).
- Re-own OpenBao, its agent and Pyroscope data directories to the service
  users to retire their group exceptions.
- Load, backfill, backup, restore and concurrent GPU measurements before any
  limit is called optimal; read-only root filesystems for the 96 writable
  services.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
