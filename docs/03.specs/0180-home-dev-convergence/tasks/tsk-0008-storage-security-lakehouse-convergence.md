---
title: "Storage, Secret Custody, Network and Lakehouse Convergence"
version: "0.1.1"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0180-TSK-0008"
parent_ids:
- "SPEC-0180"
- "SPEC-0180-PLAN-0001"
- "SPEC-0180-TSK-0007"
created: "2026-09-22"
---

# Storage, Secret Custody, Network and Lakehouse Convergence

## Objective

Execute the owner's sequential S00→S19 mission of 2026-09-22 against the single
HOME and development host: restructure `infra/04-data` and its operations
catalog, remove HashiCorp Vault while preserving OpenBao, replace MinIO with
SeaweedFS consumer by consumer, segment Docker networks and minimize
`k3d-hyhome`, add Restic, pgBackRest, Testcontainers, WireMock, Pact Broker,
Spark with Iceberg, Trino, Flink, Great Expectations, Superset and a configured
Stalwart, then close OIDC/OAuth2 Proxy, environment/secret metadata and
documentation drift. Each stage records source readiness separately from live
acceptance.

## Inputs

- Base: main `1ac49fd3534ddf5ca324ea5874403513bd0c2592` (local HEAD = `origin/main`,
  clean) on 2026-09-22. Hosted `validation-full` at that head: run `35689074480`,
  job `106622008055`, success (owner-supplied; the result proves the base only).
- Worktree `.worktrees/convergence` (ignored path inside the checkout), branch
  `refactor/spec-0180-platform-convergence`. The main checkout remains the bind
  source of the running `hy-home-infra` project and is not edited.
- Supersession: the owner's mission replaces two earlier dispositions — Vault
  and Vault Agent as MIGRATE-only (m0021 ledger) and "SeaweedFS is not the
  automatic MinIO successor". Removal of legacy source is now the target;
  deleting legacy data or credentials still needs its own approval.
- Owner answers (2026-09-22): execution scope is source plus isolated tests plus
  per-step live approval; Restic and pgBackRest use the other physical disk
  (SSD `/` and HDD data disk cross each other), offsite recovery stays open;
  Stalwart is internal-only; every new tool is an opt-in profile outside the
  eight-profile HOME command.
- [REQ-0027](../../../01.requirements/0027-home-development-host.md),
  [AD-0031](../../../02.architecture/descriptions/0031-home-development-host.md),
  [Spec](../spec.md), [Plan](../plan.md), Task 0007,
  [POL-0077](../../../05.operations/catalog/12-infra-net/0077-ip-address-management/policy.md),
  [POL-0078](../../../05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md),
  [POL-0021](../../../05.operations/catalog/04-data/0021-backup-and-restore/policy.md),
  [m0021 inventory](../../../90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md).

## Work Log

### S00 — Baseline, inventory and live state

Read: bootstrap, Claude adapter, approval/task-checklist/workflow/output-style
policies, the SPEC-0180 Spec, Plan and Tasks 0001–0007, REQ-0027, AD-0031,
POL-0021, POL-0077, the m0021 ledger and all root and leaf Compose files.

Preserved from Task 0007 (not re-implemented): feature-owned provisioning and
its runner, dbt secret redaction, `trusted_ips` removal and identity-only
`sso-auth`, Grafana authentication, Open Notebook loopback API, the `infra_net`
static/dynamic split (`172.19.1.0/24`), containerd on the SSD with Docker
data-root on the data disk, OpenBao unseal custody (SEC-003) separate from the
legacy Vault key file, and the Agent's fresh SecretID renewal.

Four-column state (read-only inspection, 2026-09-22):

| Surface | Declared (base) | Deployed | Running | Target |
| --- | --- | --- | --- | --- |
| Containers | 45 includes, 140 services | 53 selected | 53 up, all healthy or no healthcheck | new tools opt-in only |
| Vault, Vault Agent | `legacy-vault` profile | not deployed | not running; host `vault/data` holds a 28 KB Raft tree, image `hashicorp/vault:2.1.1` present | no active source; data kept pending owner disposition |
| MinIO single | 7 profiles | deployed | `minio` up; buckets `loki-bucket` 95 MB, `tempo-bucket` 38 MB, `mlflow-artifacts` 40 KB, `cdn-bucket` and `doc-intel-assets` empty | SeaweedFS; no active MinIO |
| MinIO cluster (4) | LAB | not deployed | not running | removed with MinIO |
| SeaweedFS (5) | OPTIONAL, filer without persistent store, S3 without identities, FUSE mount privileged | not deployed | not running | durable HOME object store |
| `k3d-hyhome` members | 11 declared | 9 attached | Traefik, Prometheus, Loki, Tempo, Alloy, Grafana, `mng-valkey`, `mng-pg`, OpenBao | verified cross-boundary consumers only |
| ksqlDB (3), StarRocks (2) | OPTIONAL | not deployed | no host data directory or volume | duplicate candidates (S01) |
| Spark, Iceberg, Trino, Flink, Superset, Pact Broker, WireMock, Great Expectations, Restic, pgBackRest, Testcontainers | absent | — | — | implemented per stage |
| Stalwart | OPTIONAL, env-only admin/OIDC hints | not deployed | not running | configured internal mail |

Host facts: 12 CPUs, 31 GiB RAM (16 GiB available), `/` SSD 197 GB at 73 %,
data disk HDD 2.7 TB at 1 %. `mng-pg` runs `postgres:18.6-alpine`
(runtime-version-exception: history — dated read-only observation, not a pin).
No `restic`, `pgbackrest` or Java on the host. SeaweedFS `4.47` exposes a built-in
Iceberg REST catalog (`weed s3 -port.iceberg`, default 8181) with optional
credential vending, and an embedded IAM API.

`k3d-hyhome` consumers measured in the sibling `hy-home.k8s` repository
(`5d382767`, read-only): ExternalServices for Prometheus `.10`, Alloy `.11`,
Tempo `.12`, Loki `.13`, Grafana `.14`, Valkey `.9`, PostgreSQL `.15`
(the LAB `pg-router`, not `mng-pg`) and Vault `.8`; Traefik routes to
`k3d-hyhome-serverlb`. No k8s manifest names `mng-pg` (`.16`) or OpenBao
(`.17`); the k8s External Secrets store still targets the non-running Vault.

MinIO consumers found in source (94 active files): Loki, Tempo, MLflow and its
artifact provisioning, JupyterLab (SDK through MLflow proxy), Terrakube
(state/output), Nginx (`cdn-bucket` upstream), Grafana MinIO dashboards,
Prometheus scrape jobs and alert rules, `minio-create-buckets`
(`doc-intel-assets` has no consumer), the core-readiness example, secret
registry rows STRG-001…006 and tests. Airflow and n8n reference MinIO only in
documentation.

Active HashiCorp Vault references (69 files): the Vault package, root include
and secrets, Grafana dashboards `vault.json` and `vault-hcp.json`, Prometheus
jobs and `alert_rules.vault.yml`, Renovate compose, version projection,
hardening and core-readiness scripts, operations catalog code/tests and the
0016 subject. OpenBao-compatible `VAULT_*` keys, Supabase's PostgreSQL Vault
extension and archived history are not Vault service references.

### Requirement trace

| Request | Stage | Durable owner |
| --- | --- | --- |
| `infra/04-data` and `catalog/04-data` restructure | S01, S04 | this Task, 04-data README |
| Vault removal, OpenBao preserved | S08 | 0085 OpenBao subject |
| MinIO → SeaweedFS | S06, S07 | 0024 SeaweedFS subject |
| Network segmentation, `k3d-hyhome` minimum | S05 | POL-0077, AD-0026 |
| Restic, pgBackRest | S03 | POL-0021, 0028 subject |
| Testcontainers | S09 | tests README |
| WireMock, Pact Broker | S10, S11 | new 09-tooling subjects |
| Spark + Iceberg, Trino, Flink | S12–S14 | new 04-data lakehouse subject |
| Great Expectations | S15 | new 09-tooling subject |
| Superset with Keycloak OIDC | S16 | new 04-data BI subject |
| Stalwart | S17 | Stalwart subject |
| OIDC/OAuth2 Proxy alignment | S18 | POL-0079 |
| Duplicate/legacy removal, env/secret, documents, templates | S19 | this Task |

### S01 — Target structure, duplicates, networks and migration order

Option comparison: full renumbering was rejected (identifier churn with no
functional gain); in-place patching was rejected (keeps MinIO and Vault
active); a **domain-selective restructure** is chosen. Existing tier folders
under `infra/04-data` stay; new responsibilities get new folders; removed
engines lose their folder. Stage 05 subjects keep their stable identifiers and
change their implementation binding.

Target `infra/04-data` (changed paths only):

```text
infra/04-data/
├── lake-and-object/
│   ├── minio/            removed after S07 acceptance
│   └── seaweedfs/        durable filer store, IAM, Iceberg REST catalog
├── lakehouse/            new
│   ├── spark/            batch and table maintenance job image
│   ├── trino/            SQL coordinator
│   └── flink/            JobManager/TaskManager
├── analytics/
│   ├── ksql/             removed (Flink owns stream processing)
│   ├── starrocks/        removed (Trino over Iceberg owns analytic SQL)
│   └── superset/         new BI web
└── operational/mng-db/pg/
    └── backup/           new pgBackRest image and configuration
```

Other new paths: `infra/09-tooling/{restic,wiremock,pact-broker,great-expectations}`,
`tests/integration/` for Testcontainers. Iceberg is a table format served by
the SeaweedFS catalog, not a separate service; Testcontainers is a test library.

Duplicate dispositions:

| Pair | Ruling | Evidence and condition |
| --- | --- | --- |
| Vault / OpenBao | Remove Vault source (S08) | Not running; k8s store must repoint to OpenBao (external follow-up) |
| MinIO / SeaweedFS | Remove MinIO after per-consumer cutover (S07) | Upstream archived; five buckets, 133 MB |
| MinIO cluster | Remove with MinIO | LAB, never deployed |
| ksqlDB / Flink | Remove ksqlDB after Flink acceptance (S19) | No host data, datagen is a no-op, no consumer |
| StarRocks / Trino + Iceberg | Remove StarRocks after Trino acceptance (S19) | No host data or consumer |
| `seaweedfs-mount` | Remove | Privileged FUSE with no consumer; S3 is the interface |
| Spark / Flink / Trino | Keep all | batch/maintenance, streaming, interactive SQL |
| Superset / Grafana | Keep both | data analysis vs operational observability |
| Restic / pgBackRest | Keep both | files and dumps vs PostgreSQL physical/WAL/PITR |
| WireMock / Pact / Testcontainers | Keep all | stub, contract gate, container lifecycle |
| Mailpit / Stalwart | Keep both | test capture vs real internal mail |
| Traefik / Nginx, k6 / Locust, InfluxDB, NoSQL and PostgreSQL labs | Unchanged | m0021 rulings stand; Nginx CDN upstream moves to SeaweedFS |

Final interfaces fixed before implementation:

- S3 endpoint `http://seaweedfs-s3:8333`, path-style, region `us-east-1`,
  one identity per consumer scoped to its bucket.
- Iceberg REST catalog `http://seaweedfs-s3:8181`, warehouse bucket
  `lakehouse`, namespaces `dev` and `test` separated from production data.
- OIDC callbacks stay `https://<service>.${DEFAULT_URL}/…` through Traefik.

Network target (S05 implements; DNS names first, fixed addresses only where a
contract consumes them):

| Network | Members | Allowed flows |
| --- | --- | --- |
| `edge_net` | Traefik, OAuth2 Proxy, every routed backend | Traefik → backend; backend → Traefik for OIDC discovery |
| `mng_data_net` | `mng-pg`, `mng-valkey`, exporters, their clients | client → PostgreSQL/Valkey |
| `object_net` | `seaweedfs-s3`, S3 and Iceberg clients | client → S3 8333 and catalog 8181 |
| `seaweed_internal` (internal) | master, volume, filer, S3 gateway | storage-internal only |
| `obs_net` | Prometheus, Alloy, Loki, Tempo, Pyroscope, Grafana, Alertmanager, exporters, OTLP producers | scrape and push |
| `kafka_net` | Kafka, Schema Registry, Connect, REST proxy, kafbat, exporter, Flink | broker clients |
| `mail_net` | Stalwart, Mailpit, SMTP senders | SMTP submission |
| `lakehouse_net` | Spark, Trino, Flink, Superset, Great Expectations | engine and BI traffic |
| `crawl4ai_net` | Crawl4AI | unchanged isolation |
| `k3d-hyhome` (external) | Traefik, Prometheus, Alloy, Loki, Tempo, Grafana, `mng-valkey`, OpenBao | measured k8s consumers only; `mng-pg` and Vault leave |

Migration order: S02 contracts → S03 independent backups → S04 source moves →
S05 networks (new beside old, group by group) → S06 SeaweedFS durable and
secured → S07 one consumer at a time with freeze and final delta → S08 Vault →
S09–S17 new tools on the new networks and storage → S18 auth → S19 removals
and convergence. No MinIO data is deleted before S07 acceptance and a verified
backup.

### S02 — Shared contracts, safe configuration handling, regression baseline

- Stage 99: all 40 registered template sources were read (headings and author
  prompts; package README, guide, policy and runbook in full). The package
  README prompt already requires profiles, dependencies, networks, ports,
  persistence, env keys, secret references, health semantics and removal or
  migration state; the runbook prompt already requires approval boundaries,
  backup/restore, migration, stop conditions and evidence. No contract gap for
  the new requirements was found, so no template, schema or registry changes.
  The per-template ledger is completed in S19 because a later stage may still
  expose a gap.
- Contract changes routed to their stages: POL-0077 requires a fixed address
  for every service, which conflicts with DNS-first networks and dynamic
  one-shot jobs; the policy and its validator change first in S05. Each new
  profile gets a POL-0078 row and each new service an authored m0021 inventory
  row in the stage that adds it.
- Env/secret tooling is already safe and is not reimplemented:
  `gen-secrets.sh` parses `.env` without `source`/`eval`, writes through 0600
  temporary files and atomic `mv`, rejects symlinked metadata paths, and has 30
  regression tests. Private check in the main checkout (names only):
  `--sync-metadata-check` exit 0; `.env` and `.env.example` key sets equal.
- Accumulated regression set run after every stage: Compose validation (all
  selections), operations catalog, version projection `--check`, document
  metadata (changed) and links, focused unit tests, `check-all-hardening.sh`,
  `gen-secrets.sh --dry-run`, and from S07/S08 the removed-reference checks.
- Baseline `run-ci-gate.py --profile full` at `170b89cd3`: 486 tests, one
  failure (`service-inventory-source: untracked build Dockerfile`) caused by
  this stage's in-progress S03 file while the gate ran; everything else passed.

### S03 — Restic and pgBackRest

Implemented (SOURCE_READY/LIVE_PENDING):

- `mng-pg` is built from `infra/04-data/operational/mng-db/pg/backup/`: the same
  PostgreSQL base plus the pinned Alpine `pgbackrest` package, so
  `archive_command` runs inside the server as UID/GID 70. Stanza `mng`,
  `aes-256-cbc` repository, zstd, two full backups retained,
  `archive_timeout=${POSTGRES_ARCHIVE_TIMEOUT:-300}`. The passphrase (BKP-001)
  reaches pgBackRest through a 0600 include file written at start, never env
  or tracked config. The repository binds `${BACKUP_STATE_REPO_DIR}/pgbackrest`
  on the SSD while `PGDATA` stays on the data disk.
- `infra/09-tooling/restic/`: `restic` (default `snapshots`; `init` never
  re-initializes; `forget-prune` requires `HYHOME_PRUNE_CONFIRM`) and
  `backup-sqlite-export` under profile `backup` (automation). Two repositories
  cross the disks: data-disk state → SSD, `secrets/` and `.env` → data disk.
  Live engine directories are excluded and covered by their own method.
- Host orchestrator `bin/hyhome-backup.sh` under `hyhome-backup.timer` (daily
  03:30 KST, idle I/O): `flock`, same-filesystem refusal, pgBackRest full
  (Sunday) or differential, PostgreSQL globals, Valkey RDB, SQLite exports,
  Restic backup and check, staging cleanup only on success. It reads paths
  from `docker compose config` and never sources `.env`.
- Contracts: root secrets `pgbackrest_cipher_pass`, `restic_password`; public
  keys `BACKUP_STATE_REPO_DIR`, `BACKUP_HOST_REPO_DIR`, `POSTGRES_ARCHIVE_TIMEOUT`;
  registry rows BKP-001/BKP-002 (dry-run 106 rows); POL-0078 `backup`; GDE/RUN-0021
  added and POL-0021 rows for PostgreSQL, Valkey and three SQLite stores updated
  with offsite recovery stated as not provided; mng-db, Restic and 09-tooling
  READMEs; m0021 rows; version projection (+3 images).

Review (read-only reviewer, 2026-09-22): no blocker; three high, five medium
and six low findings, all corrected before commit. H1 runbook restore target
now `chmod 0755` and the rehearsal uses 0755 instead of 0777; H2 the state set
is an allowlist (`sets/state-include.txt`) instead of an incomplete denylist;
H3 an unset repository key renders a missing path so only `mng-pg` recreation
fails, and RUN-0021 syncs `.env` before checkout; M1
`archive-push-queue-max=4GiB`; M2 `mem_limit: 1g`; M3 new SQLite sidecars are
handed back to the database owner (verified on a stopped WAL database) and
sources use `create_host_path: false`; M4 20 GiB free-space floor, EXIT-trap
staging cleanup, four-hour timeout; M5 recorded below as not run; L1 dump
command, L2 `cmd` refuses `forget`/`prune`, L3 missing Valkey fails the run,
L4 multi-line cipher secret rejected, L5 wording, L6 `pull --ignore-buildable`.

Owner decisions (2026-09-22): the owner first moved `BACKUP_STATE_REPO_DIR`
to the data disk for SSD capacity, then asked for a capacity review and set the
rule "keep the original SSD path if the repository can be capped below 5 GB".
Measured inputs: all databases 96 MB, WAL about 14 MB/h, allowlisted trees about
0.3 GB; Airflow logs (175 MB, +64 MB/day) and `airflow-valkey` left the
allowlist. The cap is enforceable without automatic deletion: after pgBackRest
(whose retention expires old backups) the orchestrator measures the SSD
repository and, at or over `BACKUP_STATE_MAX_GIB=5`, skips Restic and fails the
run. Estimated steady size is under 3 GB, so the SSD path
`/home/hyunyoun/backups` stays and the same-disk exception was withdrawn. The
orchestrator also refuses a repository inside a backed-up source, the only
self-amplifying layout, and logs repository sizes every run. The estimate is
replaced by the first measured sizes after the live switch.

Rehearsal findings fixed before commit: the entrypoint's `umask 077` leaked
into the official entrypoint and left the `PGDATA` parent untraversable for
`postgres`; a restored server needs the image entrypoint, the read-only
repository and the cipher secret because recovery runs `archive-get`; root
with only `DAC_READ_SEARCH` cannot write the repository, so Restic uses
`DAC_OVERRIDE` with every source mounted read-only; SQLite export needed
`chmod` before `chown`; restore runs in a plain container.

### S03 live activation (2026-09-22, owner-approved)

The owner approved the merge, the checkout update, the `mng-pg` switch, the
backup directories and the timer. PR #191 (S00–S03) was merged by the owner
while `validation-changed` failed on three pre-commit hooks; #192 repaired them
and #193 fixed a live finding; both passed `validation-changed` and are merged.

| Step | Result | Evidence |
| --- | --- | --- |
| Operations checkout | `1ac49fd35` → `0b16d32dc` → `c45fe2fa8` (fast-forward) | clean before each pull |
| `.env` and secrets | four keys added, existing values preserved, key sets equal; BKP-001/002 generated (16 characters, 0640) | `--sync-metadata-check` exit 0 |
| Directories | SSD `/home/hyunyoun/backups/{pgbackrest (70:70 0750), restic, staging (0700)}`; data disk `/home/hyunyoun/storage/backups/restic` (0700) | set through a root container; no sudo |
| Pre-switch dump | 2.4 MB, 9 databases, completion marker present, mode 0600 | `storage/backups/mng-pg/20260922T163235-pre-pgbackrest/` |
| `mng-pg` recreate | healthy on `hy-home/mng-pg:18.6-pgbackrest`, restarts 0; `archive_mode=on`; archiver 4 archived / 0 failed after start; passphrase absent from env and `<redacted>` in logs | 53 containers up; `airflow-triggerer` reconnected once |
| Stanza and full backup | `stanza-create` and `check` succeeded; full `20260922-073354F`: database 95.5 MB, repository 10.7 MB | `pgbackrest info` `status: ok` |
| First orchestrator run (07:55 UTC) | exit 1: pgBackRest diff and all exports succeeded, host `du` could not read the root-owned Restic repository, so Restic was skipped; staging emptied by the EXIT trap | fixed in #193 |
| Second orchestrator run (08:20 UTC) | exit 0: diff 5 MB; three SQLite exports with integrity ok; Restic state 234.8 MiB added (225.1 MiB stored), host 118.8 KiB; both `restic check` no errors; state repository 275 MiB of the 5 GiB budget; staging empty | this Task |
| Grafana dashboard check | not a defect: the legacy `dashboard` table is empty because Grafana 13 keeps dashboards in unified storage; `resource` holds 67 `dashboard.grafana.app` dashboards and 6 folders, and the provisioner logs `finished to provision dashboards` | read-only `immutable=1` query of the live volume |
| Live restore check | restored `.env` hash equals the live file; restored Grafana export integrity ok with the same row counts as the live database; scratch removed | isolated scratch directory |

Live findings fixed: host `du` cannot read the UID 70 pgBackRest repository
(#192) nor the root-owned Restic repository (#193); both sizes now come from a
read-only, networkless container. The `archive-push` log level change in #192
is baked into the image and applies at the next `mng-pg` rebuild.
`pre-commit` 4.6.1 was installed in a user venv on the owner's approval, so the
local changed gate now runs completely (exit 0).

### S04 — `infra/04-data` structure

The S01 move table keeps every existing tier folder; S04 therefore carries out
its only source decomposition now. Removals that depend on later acceptance
stay with their stage: MinIO after S07, ksqlDB and StarRocks after S19.
`lakehouse/` and `analytics/superset/` are created by S12 and S16, not as empty
placeholders now. Moving InfluxDB and OpenSearch to `specialized/` and the
NoSQL, PostgreSQL and Valkey labs under a new `lab/` folder was considered and
rejected: S01 ruled them unchanged, and the moves would touch 115 referencing
files for no functional change.

| Unit | Change | Semantics before → after |
| --- | --- | --- |
| `seaweedfs-mount` removal | service and `seaweedfs-mount` profile removed from the SeaweedFS Compose; package README, GDE/POL/RUN-0024, POL-0078 (two rows), 04-data README and the m0021 generated inventory updated | privileged `SYS_ADMIN` FUSE service with no consumer and no data → none; master/volume/filer/S3, their two volumes, ports and profiles `seaweedfs`/`storage-seaweedfs` unchanged; no container existed, so no live change |

The m0021 lifecycle ledger and its prose are dated Stage 90 judgments and keep
their original wording; the generated inventory is the current view.

### S05 — Network segmentation, phase 1 (dual-homed)

Flows came from the rendered configuration of every profile: each service's
own references (environment, commands, health checks, mounted read-only
configuration), `depends_on`, Traefik routes, the Nginx upstreams, the Traefik
file provider, Prometheus scrape targets, Grafana datasources and Gatus
endpoints. Heuristic matches that are not connections were checked and
dropped: Grafana dashboard text naming Nginx and Registry, Tempo's
`registry:` configuration key, Qdrant → Supabase `storage`, and Vault Agent
template paths naming Grafana, Keycloak and OAuth2 Proxy.

Deviation from the S01 table, with the reason:

| Change | Reason |
| --- | --- |
| added `secrets_net`, `ai_net`, `lab_net` and one network each for Airflow, n8n, Supabase and Terrakube | S01 listed no home for agent → secret store, AI backends, LAB cluster internals, or application-private stores such as the unauthenticated `airflow-valkey`; putting them on shared networks would recreate the mesh |
| `mail_net` and `lakehouse_net` deferred to S17 and S12 | no service sends SMTP over a Docker network today, and no lakehouse service exists |
| `pg-router` stays on `k3d-hyhome` | it is a measured k8s consumer (`.15`) that the S01 member list omitted |
| services with no container peer (Registry, Renovate, OpenTofu, Locust) get the project default network in phase 2 | Compose needs a network for egress and published ports; a dedicated network adds nothing |

Phase 1 adds the 13 networks with explicit `10.250.x.0/24` subnets (Docker's
automatic pool cannot take one first) and attaches each service beside its
existing `infra_net` address. `seaweed_internal` is the only `internal`
network: an internal-only service cannot publish host ports. Traefik gets
`10.250.1.2` with the `keycloak.`/`auth.${DEFAULT_URL}` OIDC aliases on
`edge_net`, where dynamic addresses start at `.128`. The Traefik provider
network, the hardening checks and `k3d-hyhome` stay as they are until phase 2.

Phase 1 is not traffic-neutral. A name shared on several networks may resolve
on a segmented network rather than `infra_net`, which network wins is not
verified here (an isolated DNS probe was not approved), so phase 1 is made
correct for either answer:

| Review finding | Fix |
| --- | --- |
| SeaweedFS master and S3 listened on the address their own name resolves to; volume had no bind | master, volume and S3 bind `0.0.0.0` |
| OAuth2 Proxy trusts only `172.19.0.2`, but Traefik reaches it by name, possibly from `10.250.1.2` | `trusted_proxy_ips` and Airflow `FORWARDED_ALLOW_IPS` trust both addresses |
| OpenSearch node 1 (also on `edge_net`) may announce an address nodes 2 and 3 cannot reach | nodes get fixed `lab_net` addresses `.11`–`.13` (dynamic range `.128/25`) and announce them with `network.publish_host` |
| CouchDB Erlang node names `couchdb-N.infra_net` resolve only through `infra_net` aliases | the same aliases are added on `lab_net` |

AD-0026 has the network table, GDE-0077 the rule for new services, and five
`NetworkSegmentationContractTests` check the routed, scrape, trusted-proxy,
bind-address and OpenSearch announce contracts over every leaf Compose file
(duplicate service names fail).

Phase 2, after phase 1 is live and verified, will remove `infra_net` from
every service and from the root. It will also switch the Traefik provider and
the OAuth2 Proxy label to `edge_net`, drop `172.19.0.2` from the trusted
proxies, remove `mng-pg` from `k3d-hyhome`, and rewrite POL/RUN-0077 and the
hardening checks. The review also found phase 2 items: the Alloy Docker log
filter keeps only `project_net|infra_net` targets (`config.alloy`,
`config.home.alloy`); the MinIO cluster overlay is `infra_net` only (removed
with MinIO in S07, so phase 2 must not precede S07 or must move it to
`lab_net`); and RedisInsight reaches only `mng_data_net` stores.

### S05 phase 1 live activation (2026-09-22, owner-approved)

The operations checkout was already at `f6e507955` (#196). The 53 running
services (the 8-profile HOME set plus Kafka, MLflow, JupyterLab, Open Notebook,
SurrealDB, Registry, DCGM and Crawl4AI) were recreated with
`up -d --no-deps --pull never`. `--no-deps` kept the init jobs from rerunning;
`--pull never` kept Open Notebook's moving `v1-latest-single` tag on its local
image.

| Step | Result |
| --- | --- |
| Dry run | 51 recreate, Registry and Crawl4AI unchanged, 9 networks created (`lab_net`, `seaweed_internal`, `supabase_net`, `terrakube_net` have no running member) |
| First apply (10:5x–11:03 UTC) | exit 1: `--wait` aborted when n8n was briefly unhealthy while `mng-pg` restarted; the containers not yet started were left in `Created` |
| Second apply without `--wait` | exit 0; 53 running; after the health wait 51 healthy, 2 without a health check (as before) |
| DNS order | from Traefik, `oauth2-proxy` and `grafana` resolve to `edge_net` addresses and `keycloak.hy.home.arpa` to `10.250.1.2`: the phase-1 review's premise holds, so the dual trusted-proxy fix was required |
| SSO | Prometheus/Loki/Alloy forward-auth returns the Keycloak redirect whose state keeps `https://prometheus.hy.home.arpa/` (forwarded headers trusted); Grafana, Keycloak, Dozzle login redirects; Gatus and Airflow 200 |
| Startup noise | OAuth2 Proxy and Gatus crashed and restarted until Keycloak and Traefik were ready (OIDC discovery 404/503), then ran normally |
| Prometheus | 21 up, 10 down: 8 k8s NodePort targets on `172.18.0.2` (connection refused; `.2` is Traefik's own k3d address, `k3d-hyhome` was not changed, pre-apply state not captured, so a pre-existing target error is likely but unverified), OpenSearch (not running), OpenBao (503, sealed) |
| OpenBao | sealed after its restart (initialized, 2-of-3 shares): owner unseal required; no key material read |

OpenBao follow-up (owner-approved, 2026-09-22): the owner unsealed OpenBao.
The metrics scrape then returned 403. The earlier metrics token had expired, and
a token issued with the human operator identity cannot carry the `prometheus`
policy: `hy-home-operator` has no policy or orphan-token rights. Following
RUN-0085 "Prometheus Metrics Credential", the owner staged an OIDC operator
token in the container once. A single scripted process then ran the
authenticated generate-root ceremony, with shares fed from
`openbao_unseal_keys.txt` through stdin and decoded with the OTP in the same
process. The temporary root wrote `prometheus` (`read` on `sys/metrics`) and
issued an orphan, no-default-policy token with a 720h TTL. Checks: metrics read
allowed, a KV secret read denied, policy list denied. The root was then revoked
and the staged operator token deleted. The token file was replaced atomically,
keeping mode 0640 and its group, and the accessor and expiry
(`2026-10-22T11:54Z`, requested TTL) went to the ignored
`openbao_metrics_token.custody`. After a Prometheus recreate the `openbao`
target is up. No share, OTP or token value was printed or passed as a host
argument.

Lesson for phase 2: recreate in dependency waves, providers first
(`mng-pg`, `mng-valkey`, Keycloak, Traefik), then the rest. Do not rely on
`--wait` across the whole set. Plan the OpenBao unseal for its restart.

### S06 — SeaweedFS as a durable, secured store

The image's own facts decided the design. `/entrypoint.sh` adds `-mdir=/data`
and `-dir=/data` only when the first argument is the bare subcommand; every
tracked command started with `-v=1`, so master and volume wrote to `/tmp` (the
flag defaults), and the filer's leveldb2 store (`/data/filerldb2`) had no
volume. The same entrypoint needs root to `chown` and `su-exec`, which
`cap_drop: ALL` forbids. No SeaweedFS volume existed on HOME, so nothing was
lost or migrated. `gateway-standard-chain` has no authentication, so the
master UI (`seaweedfs.`) and the whole filer (`cdn.`) were public. S3 also
listens by default on gRPC (`port+10000`), Iceberg (8181) and Lance (9101).
The tracked `security.toml.example` used a format SeaweedFS does not read.

| Requirement | Implementation |
| --- | --- |
| persistent set | bind volumes `${DEFAULT_DATA_DIR}/seaweedfs/{master,volume,filer}`; `-mdir=/data`, `-dir=/data`; filer on the embedded leveldb2 store (no start or recovery dependency, portable through `fs.meta.save`); UID 1000, so no root step |
| explicit identities, no anonymous write | `hyhome-seaweedfs.sh` writes `s3.json` from `SEAWEEDFS_S3_ADMIN_ACCESS_KEY` and STRG-010 and refuses to start without them; per-consumer bucket-scoped identities come with each S07 cutover |
| no IAM bypass | volume and filer HTTP need JWTs (STRG-008, STRG-009) for reads and writes; master and filer routes removed, both only on `seaweed_internal` |
| TLS and internal authentication | gRPC mutual TLS for all four components from a SeaweedFS-only CA (`bin/gen-grpc-certs.sh`, CA key discarded); S3 is SigV4 over HTTP on `object_net`, HTTPS through Traefik |
| minimal surface | `-port.iceberg=0 -port.lance=0 -iam=false` until S12 |
| capacity | `-minFreeSpace=20GiB`; replication `000` (same-host copies are not availability) |
| independent backup | the orchestrator pauses vacuum, saves filer metadata, Restic reads the volume and master trees, vacuum resumes in the EXIT trap; allowlist gains `data/seaweedfs/{volume,master}`; POL-0021 records why this live read is accepted |

`SeaweedfsRehearsalTests` (opt-in `HYHOME_SEAWEEDFS_REHEARSAL=1`) renders the
real services onto disposable data and two internal networks. It passed 6/6
on 2026-09-22. It covered refusals (anonymous 403, wrong secret, filer and
volume 401 without a JWT, gRPC TLS alert without a client certificate). It
covered the consumer API: content type, metadata, tags, range, prefix listing,
an encoded key, a 20 MiB multipart upload whose ETag is not an MD5, presigned
GET, and keys `a` and `a/b` coexisting. It also showed that the bind paths
hold the data, that a GET fails while the volume server is down, that objects
survive a restart, and that the backup set restores into empty stores with
identical bytes. Versioning, Object Lock, SSE, notifications and lifecycle
were not tested; S07 tests whichever a consumer needs.

Sequential review findings and their disposition:

| Finding | Disposition |
| --- | --- |
| Critical: master, volume and filer were still on `infra_net`, where any container could take a write JWT from `/dir/assign` or delete a bucket through `/col/delete` | removed from `infra_net`; now only on `seaweed_internal`; contract test pins the network set; the rehearsal checks S3 clients cannot reach them |
| Important: `weed shell` may exit 0 on failed commands; a stale export could pass as current | the orchestrator fails on a non-zero exit, error text, an empty export or a half-running pair, and removes the export before and after each save; the rehearsal observed exit 1 for a failed `fs.meta.load` (the premise does not hold for that command) and no error text in normal output |
| Important: the consistency claim was too strong | narrowed in POL-0024 and POL-0021: objects overwritten or deleted inside the Restic window may restore as missing; restore runs `volume.fsck` |
| `-port.grpc` not passed, config read from the `/data` bind first, partial certificate sets reported as complete | `-port.grpc` from the port keys; `working_dir: /etc/seaweedfs`; the certificate script requires the full set or `--rotate` |
| every container mounts every component key | accepted: the S3 container already holds the client certificate and both JWT keys, which give the same reach |
| the SeaweedFS trees count against the 5 GiB state budget | deferred to S07, where consumer data first arrives |

### S06 HOME activation (2026-09-22, owner-approved)

| Step | Result |
| --- | --- |
| Operations checkout | fast-forward to `f7a6c55cf` (#197). The owner's local `.gitignore` line for `*.custody` was not in main because #197 merged before that commit; it was restored at once and is carried by #198 |
| Secrets | `gen-secrets.sh --sync-metadata-check` refused its input: the private registry's `SEC-003` row spans three lines (its multi-line Value cell was not read). Generation also rewrites that registry, so STRG-008–010 were created with the same method instead (16 alphanumeric characters, 0640, group `SECRETS_GID`), and `SEAWEEDFS_S3_ADMIN_ACCESS_KEY` was appended to `.env`. Registry Value cells for them stay empty until the owner repairs `SEC-003` and runs `--sync-metadata` |
| Certificates | issued into `secrets/certs/seaweedfs` (0700, keys 0640); no ignore rule covered that directory, so one was added locally and in #198 before anything else ran |
| Start | `${DEFAULT_DATA_DIR}/seaweedfs/{master,volume,filer}` created (UID 1000); four services healthy on the first `up --wait` |
| Checks | anonymous PUT and list 403 on `object_net`; admin create, head and delete of a disposable bucket exit 0; `s3.` route 403 without credentials, `seaweedfs.` and `cdn.` 404; master, volume and filer only on `seaweed_internal`; state on the binds (`m9333`, `N.dat/.idx/.vif`, `filer/filerldb2`); master and volume also create an empty `filerldb2` directory from the image `filer.toml` (4 KiB, harmless) |
| Telemetry | the master logs that it reports usage to `telemetry.seaweedfs.com` once 10 GiB are stored; with no egress on `seaweed_internal` the name does not resolve. The owner chose not to add `-telemetry=false`; if the master ever gets egress, revisit |
| Backup | a manual orchestrator run exited 0: the latest state snapshot holds `exports/seaweedfs-filer.meta` and `data/seaweedfs/{master,volume}`; no export left in the container; state repository 289 MiB of 5 GiB |

### S07a — Consumer switch to SeaweedFS (source)

Live MinIO inventory (2026-09-22): `loki-bucket` 103 MB, `tempo-bucket`
89 MB, `mlflow-artifacts` 40 KB. `cdn-bucket` and `doc-intel-assets` are empty,
and `tfstate` was never created. `doc-intel-assets` has no consumer and is not
recreated.

| Unit | Change |
| --- | --- |
| identities | `config/s3-identities.conf`: `loki`, `tempo`, `mlflow`, `terrakube` scoped to their bucket (STRG-011–014); `anonymous` may only read `cdn-bucket`; the start script refuses to start when any listed secret is missing |
| buckets | `seaweedfs-buckets` (aws-cli, admin) creates the five buckets idempotently; consumers wait for it |
| migration | `seaweedfs-migrate` (`storage-migration`, MinIO `mc`): S3-API mirror per bucket that adds missing objects; `FINAL=1` also overwrites and deletes, requires identical key and size listings and writes the cutover marker; removed with MinIO |
| profiles | SeaweedFS joins every S3 consumer profile and so HOME; `iac` is excluded (automation, forbidden in HOME), so Terrakube runs with `storage` |
| Loki, Tempo | endpoint `seaweedfs-s3:8333`, region `us-east-1`, own identity; the image entrypoints read `S3_SECRET_KEY_FILE`; image tags renamed (`hy/loki:3.7.8-seaweedfs`, `hy/tempo:3.0.3-seaweedfs`) so the new entrypoint is always built, which also fixes tags that named older versions than their Dockerfiles |
| MLflow | endpoint and `mlflow` identity; `mlflow-artifact-provision`, its MinIO script, `MLFLOW_S3_USER`, `mlflow_s3_password` and STRG-005/006 removed |
| Terrakube | `terrakube` identity, endpoint, region `us-east-1` for state and output |
| Nginx | `/minio/` (the whole S3 API) and `/minio-console/` replaced by read-only `/cdn/` → `cdn-bucket` (GET/HEAD only) |

Sequential review findings and their disposition:

| Finding | Disposition |
| --- | --- |
| `/cdn/*.png` and other static extensions were taken by the server-level asset regex | `location ^~ /cdn/`; forwarded headers restored; static contract test |
| a repeated copy after a switch would overwrite consumer writes even without deletion | default runs add missing objects only; `FINAL=1` overwrites, deletes, requires identical key and size listings, then writes `hyhome-migration/<bucket>.cutover`; every later run for that bucket is refused |
| the count check used awk, which the MinIO image lacks (verified: no awk, sed or grep), and ignored listing failures | bash-only listing with checked `mc` status; key and size comparison |
| POL-0078 still named the removed MLflow job; Terrakube had no bucket ordering | rows corrected; `iac` row says Terrakube runs with `storage`; Terrakube waits for `seaweedfs-buckets` (`required: false`) |
| Loki and Tempo accepted an empty secret; stale MinIO text in 0023, 0044 and the MinIO README | refused; text corrected |
| MinIO `cdn-bucket` public policy could carry over with `--preserve` | not copied (empty); stated in RUN-0024 |
| hard-coded `8333` in consumers | accepted: it is the S01 interface contract |

`SeaweedfsRehearsalTests` passed 8/8 after the fixes, including the new scope
and migration tests. The migration test uses a disposable MinIO: the first copy,
then source edits, a deletion and an addition, then `FINAL=1` matching exactly,
then a refused re-run. `loki` is
refused on `tempo-bucket` and cannot create a bucket, and anonymous access
returns 200 for a CDN object but 403 for listing, PUT and DELETE. MinIO
itself, its bootstrap, its Prometheus job, dashboards and the MinIO subject
stay until S07b; architecture and requirement mentions are swept there.

### S07a live cutover (2026-09-22, owner-approved)

PR #200 merged as `887aa70da`; the operations checkout was fast-forwarded to it.
Nginx and Terrakube were not running, so only Loki, Tempo and MLflow were
switched.

| Step | Result |
| --- | --- |
| Secrets | STRG-011–014 created by the S06 method (32 alphanumeric characters, 0640); registry Value cells stay empty until `SEC-003` is repaired |
| SeaweedFS | `seaweedfs-s3` recreated with the identities (healthy); `seaweedfs-buckets` created all five buckets |
| Initial copy | `loki-bucket` 1263 objects / 98,022,560 B, `tempo-bucket` 464 / 69,820,711 B, `mlflow-artifacts` 2 / 4 B, `cdn-bucket` 0; both sides equal |
| Loki | image built, stopped, `FINAL=1` equal (1263) and marked, recreated healthy. The 6-hour counts for 3 to 2 days before (191368, 325259, 315666) match the pre-cutover baseline exactly; new lines are queryable; the only error was a start-up `empty ring` |
| Tempo | image built, stopped, `FINAL=1` equal (496 / 71,930,488 B) and marked, recreated healthy. The pre-cutover baseline trace `bf7ba3a2…` from 2 days before is returned; search works; the bucket grew to 516 objects. Start-up dropped one partial WAL block written at stop time (`failed to replay block. removing`), so traces received in the last seconds before stop may be lost |
| MLflow | stopped, `FINAL=1` equal (2) and marked, recreated. The operator `.env` still set `MLFLOW_S3_ENDPOINT_URL` to MinIO (only `.env.example` changed in source); that one value was changed and MLflow recreated. An existing artifact returns 200 through the artifact proxy, and PUT, GET and DELETE of a probe succeed |
| `cdn-bucket` | empty on both sides; `FINAL=1` marked |
| Scope | 3×3 list check with each consumer key: own bucket allowed, the other two denied |
| MinIO | still running with its data untouched; the rollback is the previous configuration against it. `doc-intel-assets` is empty and was not copied |

### S07b — MinIO removal (source)

| Unit | Change |
| --- | --- |
| Compose | `infra/04-data/lake-and-object/minio/` (HOME node, bucket job, LAB `minio1`–`minio4`) and its root includes removed; the `storage-cluster` profile goes with it. `seaweedfs-migrate`, its script and the `storage-migration` profile removed |
| Secrets | `minio_root_*` and `minio_app_*` root declarations and STRG-001–004 removed; registry counts 268/58/208, 79 declarations, 108 rows |
| Environment | `MINIO_PORT` and `MINIO_CONSOLE_PORT` removed from `.env.example` and the core-readiness example (which also held `MINIO_APP_USERNAME`) |
| Observability | Prometheus `minio` job (both configs), the `Minio_alerts` group and `minio` in the missing-target regex removed; Grafana `minio.json` and `minio-bucket.json` removed |
| Catalog | POL-0078 member lists, the `storage-cluster` and `storage-migration` rows and the storage-cluster compatibility row removed; the catalog profile map entry removed; m0021 authored rows removed and the inventory regenerated; tech-stack projection resynced (one image removed) |
| Stage 05 | 0023-minio preserved under `docs/98.archive/superseded/` with `superseded_by` GDE/POL/RUN-0024 and three Retention Catalog rows (source `988059fe8`); inbound links removed; RUN-0024 replaces the cutover procedure with the retained-data note; POL-0021 row describes the retained, unbacked MinIO directory |
| Documents | Requirements 0001/0002/0004/0007, descriptions 0001/0004/0006/0009/0019/0021/0024/0026 (MinIO addresses marked released), infra and secrets READMEs now name SeaweedFS |
| Tests | rehearsal drops the migration job, the disposable MinIO and test 7 (7 tests remain) |

Sequential review: no critical or important finding. Minor wording fixes
applied: the retained MinIO directory is described as removed from source, not
as stopped, until the live step runs; stale scope text in the lake-and-object
README and m0021; Nginx waits only for `seaweedfs-s3`; RUN-0024 rollback no
longer names a cluster. The gate also found links from Tasks 0001/0005, POL-0021
and m0021 to removed paths (now identifiers or RUN-0024) and an empty
`0023-minio` directory left by the move. Rehearsal 7/7 passed; the archive
`Source` `988059fe8` is reachable from `main` (#201 merge commit).

CI `validation-changed` failed twice on #202 with `Git identity scan exceeded
its output bound`, independent of this change: the allocation transition scan
shares one 64 MiB budget, reads the registry blob again for every merged fork,
and measured 65.6 MiB locally; the synthetic PR merge commit adds one more
fork. `validate_allocation_transition` now reads each immutable blob once
(cache hits still honour the per-call limit), which brings the scan to 48.5
MiB; a test asserts no blob is read twice. The scan still grows about 0.25 MiB
per merge (one tree grep per fork), so the bound will be reached again after
roughly 60 more merges.

Kept deliberately: ADR-0001 and ADR-0006 name MinIO as the context of their
decisions and are not rewritten; the historical live snapshot table in m0021
and earlier Task text keep their MinIO rows as evidence.

Runtime is not changed by this source step. After merge, the running `minio`
container becomes a Compose orphan and is stopped and removed in a separately
approved live step; its data directory stays.

### S07b live cleanup (2026-09-23, owner-approved)

Owner approved container removal and secret deletion.

| Step | Result |
| --- | --- |
| Containers | `minio` stopped and removed; the exited `minio-create-buckets` and `mlflow-artifact-provision` removed. No MinIO container remains |
| Data | volume `hy-home-infra_minio-data` kept untouched: 176.8 MB (`loki-bucket` 102.5 MB, `tempo-bucket` 73.5 MB, `mlflow-artifacts` 40 KB, `cdn-bucket` and `doc-intel-assets` empty) |
| Secrets | the four `secrets/storage/minio_*.txt` deleted. Object data is unencrypted and readable by a new MinIO server, but the IAM state in `.minio.sys` was encrypted with those root credentials and is not recoverable |
| Environment | operator `.env` lost `MINIO_APP_USERNAME`, `MLFLOW_S3_USER`, `MINIO_PORT`, `MINIO_CONSOLE_PORT` and the MinIO wording; `config --quiet` passes for storage, obs and mlops |
| Prometheus | a HUP reload dropped the `Minio_alerts` group, so no false `MinioServiceDown` fires. The scrape job survives the reload because `prometheus.dev.yml` is a single-file bind mount and the edit replaced the host inode; the container still reads the old file and shows a down `minio` target until it is recreated |
| Consumers | `seaweedfs-*`, `infra-loki`, `infra-tempo` and `mlflow` healthy after the removal |

### S08 — Vault removal (source)

Vault and `vault-agent` were not running and had no consumer; OpenBao is the
HOME secret authority. The preserved data path and seal material stay.

| Unit | Change |
| --- | --- |
| Compose | `infra/03-security/vault/` (server, agent, `vault.hcl`, `vault-agent.hcl`, ten Agent templates) and the root include removed; the `legacy-vault` profile and its POL-0078 rows go with it (the profile-category vocabulary entry stays, as a checker test uses it) |
| Secrets | `SEC-001` (`secrets/security/vault_token.txt`) removed from the registry; counts 266 public, 107 rows; `migration_only` is now empty |
| Environment | `VAULT_PORT` and `VAULT_CLUSTER_PORT` removed from `.env.example` |
| Hardening | `check_03_security` rewrote its Vault assertions for OpenBao (image from the registry, Agent output mount, gateway chain, `infra_net` and k3d addresses, Raft, mlock, TLS and telemetry from `BAO_LOCAL_CONFIG`, AppRole paths, templates, healthchecks); the full run passes |
| Observability | Grafana `vault-hcp.json` (HCP cloud, needs a `cluster_id` this host never had) removed. `vaults.json` and `alert_rules.vault.yml` stay: OpenBao keeps the `vault_` metric prefix, verified live (263 `vault_*` series, `openbao` target up) |
| Catalog | 0016-vault preserved under `docs/98.archive/superseded/` with `superseded_by` GDE/POL/RUN-0085 and three Retention Catalog rows (source `a797331dc`); m0021 rows removed and the inventory regenerated; tech-stack projection resynced |
| Documents | REQ-0003 now names OpenBao throughout; descriptions 0003/0004/0018/0026/0031, the 03-security README and index, governance quality standards, Prometheus and workflow subjects, and `infra/README.md` follow; Task 0001 rows cite `GDE-0016` as an identifier instead of a link |

Sequential review findings and their disposition:

| Finding | Disposition |
| --- | --- |
| `Security/vault.json` (28 panels) queries `up{job="vault"}`, the job this change removes, and `Security/openbao.json` is the same dashboard ported | removed; only `Infrastructure/vaults.json` and `alert_rules.vault.yml`, which are metric-name based, stay |
| AD-0003 still called Vault a retained component and described OpenBao/Vault coexistence, contradicting the rewritten REQ-0003 it pairs with | rewritten |
| `secrets/README.md` still called `SEC-001` a public-schema exception, so a prune run would now silently target that private row | rewritten with the prune warning |
| `docs/05.operations/catalog/03-security/README.md`: removing the Vault row left a blank line inside the Structure table, breaking it; scope text still claimed a Vault subject | fixed |
| `infra/03-security/README.md` still advertised a `vault.${DEFAULT_URL}` UI route | fixed |
| `common-optimizations.exceptions.json` kept `vault` and `vault-agent` secret exemptions; a future service of that name would inherit them | removed |
| `migration_only` classification had no compose file left, making its mutation test vacuous | the classification and its test removed; the suite is now a four-way split |
| m0021 ruling cell contradicted itself ("removed" then "retain MIGRATE-only") | rewritten |

Left as found: REQ-0003 keeps `FR-0004 Audit Logging` and `NFR-0007` local API
caching, which the declared OpenBao configuration does not implement (no audit
device, no Agent cache stanza), and no service mounts `openbao-agent-out`. These
predate S08 and belong to the OpenBao subject owner.

Kept deliberately: ADR-0003 and ADR-0018 record the decisions of their time and
are not rewritten; `examples/operations/compose-core-readiness/` keeps its own
self-contained Vault rig, which names no repository package; the Restic state
set still backs up `security/vault`.

### S05 phase 2 — `infra_net` removal (source)

Phase 1 is live and verified, MinIO and Vault are gone, so the shared mesh has
no remaining dependant.

| Unit | Change |
| --- | --- |
| Services | 135 `infra_net` attachments removed across 41 Compose files; every service keeps only the networks whose peers it uses. Registry, Renovate, OpenTofu and Locust have no container peer and now use the project default network |
| Root | the `infra_net` definition and its `172.19.0.0/16` IPAM removed, and with them the now-orphan `INFRA_SUBNET`, `INFRA_IP_RANGE` and `INFRA_GATEWAY` keys (public keys 263, optional 205) |
| Gateway | Traefik's Docker provider network and the OAuth2 Proxy router label are `edge_net`; OAuth2 Proxy and Airflow trust only `10.250.1.2` |
| k3d | `mng-pg` left `k3d-hyhome` (no k8s consumer named it); `mng-valkey` stays, it is measured |
| Alloy | the Docker log filter kept only `project_net\|infra_net` targets. Live check: of 56 running containers just 13 were selected and 6 were shipping, so most container logs were silently dropped after phase 1. Upstream documents that `loki.source.docker` deduplicates targets by container ID, so the network filter was never needed; it now keeps every Compose-managed container |
| Hardening | eleven fixed-address assertions covered `infra_net` addresses that no longer exist. A new `check_service_network` helper reads one service block, so the replacements stay per service (13 assertions, including `openbao-agent`, `surrealdb` and the OAuth2 Proxy Valkey exporter, which a file-wide grep would not have distinguished). Negative-tested: an absent network and an unknown service both fail |
| Documents | AD-0026 and REQ-0023 rewrote the single-mesh model as flow-scoped networks and dropped the `172.19.0.x` allocation table; GDE/POL/RUN-0077 now govern membership rather than fixed-address assignment; `.agents` environment constraints, nine architecture descriptions, five requirements and 40 package READMEs follow, with README network rows generated from the Compose files |

Sequential review findings and their disposition:

| Finding | Disposition |
| --- | --- |
| RedisInsight kept only `edge_net` and `mng_data_net`, so the Valkey cluster, n8n Valkey and Airflow Valkey it exists to inspect became unreachable; no Compose key names those hosts, so no check caught it | `lab_net`, `n8n_net` and `airflow_net` added |
| the new Alloy keep rule matched every Compose project on the host, not just this one | pinned to `hy-home-infra` |
| REQ-0023 still asked for predictable addressing in the removed `172.19.0.0/16` | rewritten |
| about 20 operations subjects still described `infra_net` as live, two of them as instructions ("backends must be on `infra_net` to be discovered", the Registry exposure radius) | each rewritten from the Compose files; the CouchDB Erlang node names keep their original spelling |
| the `12-infra-net` index, the RUN-0077 parent link and the POL-0077 review item still named the old subject | rewritten |
| the hardening conversion lost per-service granularity | `check_service_network` added (above) |
| a Loki search-command example had its `rg` pattern rewritten by the sweep | restored to a pattern that matches the new rule |

Live application is a separate approved step: removing a network from a
service requires recreating it, and CouchDB's Erlang node names keep working
only through the `lab_net` aliases phase 1 added.

### S05 phase 2 live apply (2026-09-23, owner-approved)

The approved unit was the full recreate. The CouchDB profile is not running,
so the `lab_net` aliases were not exercised live.

| Step | Result |
| --- | --- |
| Scope | 56 running containers, 52 of them attached to `infra_net`. The active profile set was derived from the running services (`admin ai crawl4ai data-science dev messaging notebook obs obs-gpu tooling workflow`) so the recreate could name every service explicitly and start nothing new |
| Dry run | `docker compose up -d --no-deps --dry-run <56 services>`: 52 recreates, no container creations; `lab_net` and `hy-home-infra_default` to be created |
| Apply | First pass stopped at `dependency failed to start: container airflow-apiserver is unhealthy` — the API server was still inside its start period, so 23 dependants stayed `Created`. A second identical pass once it reported healthy completed them; no other failure |
| Network | `infra_net` reached 0 members and was removed. The project now runs on `edge_net`, `obs_net`, `mng_data_net`, `object_net`, `secrets_net`, `ai_net`, `kafka_net`, `airflow_net`, `n8n_net`, `crawl4ai_net`, `lab_net`, `seaweed_internal`, `k3d-hyhome` and the project default |
| Containers | 56 running, the same set as before; none missing. `kafka-2`/`kafka-3` remain in `Created` from 2026-09-22 and predate this step |
| Logs | Loki `container_name` label values went from 6 to 56, so the phase 1 log loss is closed. The window from 2026-09-22 to this apply stays unrecoverable |
| Metrics | Prometheus `up==1` 21, `up==0` 10. The stale `minio` target is gone with the config remount. The ten down targets are the eight k3s NodePort jobs, `opensearch` (not running) and `openbao` |
| Gateway | `grafana.hy.home.arpa` and `keycloak.hy.home.arpa` answer `302` to the SSO redirect through Traefik on `edge_net`. A `gateway-standard-chain@file does not exist` error appeared for ~90 seconds while Traefik loaded the Docker provider ahead of the file provider, then stopped |
| Reachability | `redisinsight` resolves `mng-valkey`; `n8n-valkey` and `airflow-valkey` do not resolve because the `dedicated-valkey` profile is not running. `mlflow` resolves `seaweedfs-s3`, `alloy` resolves `loki` |
| Gatus | 6 of 7 endpoints up; `OpenBao` is the one down |

OpenBao sealed on restart, as it did at the phase 1 apply, and the plan should
have named the unseal ceremony as part of this step rather than leaving it to
be discovered. The owner unsealed it the same day: `sealed=false`, the
`openbao` scrape target returned to `up=1`. The Agent still needs a fresh
AppRole SecretID, because a SecretID is single-use and the Agent deletes its
file after reading it; until then it logs `no known secret ID`. No running
consumer broke — the rendered Agent outputs persist in the `openbao-agent-out`
volume. The SecretID delivery stays with the owner under RUN-0085.

### S09 — Testcontainers (source)

Testcontainers is a test library, not a service, so S09 adds no Compose file,
no profile row and no m0021 inventory row. The S01 target structure reserved
`tests/integration/`, but the CI gate adapter admits only `tests.validation`
and `tests.lib` modules and every test module must be reachable from the full
profile, so the test lives in `tests/validation/` and joins the
`compose-baseline-regressions` suite, where it reports as skipped.

| Unit | Change |
| --- | --- |
| Subject | `mng-pg-init`'s bootstrap SQL. `test_compose_baseline_gates.py` already proves statically that the job passes every `psql` variable the script reads; nothing proved the script runs. The file is `\gexec` and `\connect` meta-commands that only `psql` executes, and the job reruns on every `core` start, so a non-idempotent statement fails the stack instead of a gate |
| Test | `tests/validation/test_mng_pg_init_sql.py`: starts PostgreSQL through Testcontainers, runs the real SQL twice with the same variables the job passes, then asserts the five feature roles, the service role, their databases and each database's owner |
| Image pin | read from `services.mng-pg-init.image` in the Compose file, so the test cannot drift from the declaration it exercises |
| Opt-in | skips unless `HYHOME_INTEGRATION=1` and `testcontainers` is importable, so `unittest discover -s tests` stays runnable with no Docker daemon and the CI profiles, which do not install the dependency, are unaffected |
| Dependencies | `tests/requirements-integration.txt`. Renovate's `pip_requirements` manager covers only `infra/**/requirements.txt`, so this file is manually owned like `scripts/requirements.txt`; the Renovate description now says so |
| Documents | `tests/README.md` gains the structure row and an opt-in run section (1.0.3 → 1.1.0) |

Evidence: 2/2 pass against the declared `postgres:18.6-alpine` in 18s; the same
discovery skips both with a reason when the opt-in is absent. The host has no
`pip`, so the real run used a `python:3.12` container with the Docker socket,
`--network host` and the repository bind-mounted at its own absolute path.

Sequential review findings and their disposition:

| Finding | Disposition |
| --- | --- |
| a generated random password would repeat the GitGuardian false positive that PR #200 hit | one visible placeholder constant, with a comment saying why an empty password is not an option |
| a hard-coded image tag would drift from the job it claims to exercise | the tag is read from the Compose declaration |
| a new dependency surface with no named update owner breaks the Behavior Contract | Renovate's `pip_requirements` description names it as manually owned |
| the changed gate failed `test_every_test_module_is_reachable_from_the_full_profile`: the module was in no suite, and a `tests.integration` module is outside the adapter grammar | moved to `tests/validation/` and registered in `leaf.compose-baseline-regressions`, not a widened adapter grammar |

### S10 — WireMock (source)

| Unit | Change |
| --- | --- |
| Service | `infra/09-tooling/wiremock/`: `wiremock/wiremock:3.13.2-alpine` under the read-only template, UID 1000, all capabilities dropped, 512 MiB; tracked `mappings/` mounted read-only; request journal capped at 1000 entries; health from `/__admin/health` |
| Exposure | the admin API is unauthenticated, so the host port `127.0.0.1:${WIREMOCK_HOST_PORT:-18088}` is loopback-only like the registry and no Traefik route or OIDC client exists; containers use `wiremock:8080` on the project default network |
| Profile | new `api-mock` (capability) with a POL-0078 row and a companion row; not part of HOME or any domain profile |
| Contracts | root include; public key `WIREMOCK_HOST_PORT` in `.env.example` (the operator `.env` gains it at the live step); version projection +1 image; authored m0021 row rendered by `render_service_inventory` |
| Documents | new subject `0092-wiremock` (GDE/POL/RUN-0092), package README, 09-tooling infra and catalog READMEs |

Evidence: `validate-docker-compose.sh` default mode 70 selections and 336
services, and `api-mock` alone 1 service; `check-operations-catalog.py` PASS;
`sync-tech-stack-versions.sh --check` in sync; `check-all-hardening.sh
09-tooling` PASS. An isolated Compose project (`-p s10-probe`, host port 18188)
started the real definition healthy with `user=1000:1000`, a read-only root,
`CapDrop=[ALL]`, a 512 MiB limit and a `127.0.0.1` binding; the tracked stub
answered, an unknown path returned 404 and appeared in
`__admin/requests/unmatched/near-misses`, and `__admin/mappings/reset` reloaded
one mapping; the project was removed afterwards. Live start is NOT_RUN and
needs its own approval.

Sequential review (read-only reviewer) findings and their disposition:

| Finding | Disposition |
| --- | --- |
| the default network is also an unauthenticated admin boundary, and AD-0026 listed only peerless services there | AD-0026 names WireMock and the rule; policy and guide state that any default-network container has full admin rights and a named consumer gets a scoped network |
| the policy claimed the read-only mount forbids recording | reworded: it blocks persisting; recording or `proxyBaseUrl` is a policy prohibition |
| the loopback binding, the only exposure control, had no gate | `check_09_tooling` asserts the `127.0.0.1` publication |
| catalog table split by blank lines; hard-coded 18088 in commands; redundant healthcheck redirections; inventory row missing the HOME requirement link | fixed |
| AD-0009 lists no profile for dbt, Restic or WireMock | pre-existing drift; deferred to S19 document convergence |

### S11 — Pact Broker (source)

| Unit | Change |
| --- | --- |
| Services | `infra/09-tooling/pact-broker/`: `pact-broker-db-provision` (the shared `run-feature-provision.sh` runner with feature SQL derived from MLflow's: refuses administrator or foreign roles and foreign database owners, idempotent) and `pact-broker` (`pactfoundation/pact-broker:3.0.0-pactbroker2.121.2`, read-only template, image user `ruby`, all capabilities dropped, 512 MiB) |
| Credentials | the image reads credentials only from the environment, so the entrypoint exports both passwords from Docker secrets into the broker process; none is declared in Compose `environment` or argv. New secrets `pact_broker_db_password` (PG-026) and `pact_broker_basic_auth_password` (AUTO-018); public keys `PACT_BROKER_DB_USER` (PG-027), `PACT_BROKER_BASIC_AUTH_USERNAME` (AUTO-019), `PACT_BROKER_DB_NAME`, `PACT_BROKER_HOST_PORT` |
| Exposure | basic auth on the UI and whole API, public read off, only the heartbeat public; host port `127.0.0.1:${PACT_BROKER_HOST_PORT:-19292}`; no route; `PACT_DO_NOT_TRACK` disables the image's analytics ping; `mng_data_net` only |
| Profile | new `contract-testing` (capability), added to the `mng-pg`/`mng-pg-init` dependency closure; POL-0078 row, companion row and the closure row |
| Contracts | root include and two root secrets; `FEATURE_JOBS`/`FEATURE_SECRETS` in the provisioning contract tests; pinned counts in `test_secret_metadata_sync`; AD-0026 `mng_data_net` members; version projection +1 image; two authored m0021 rows plus the re-rendered `mng-pg-init` profile cell |
| Documents | new subject `0093-pact-broker` (GDE/POL/RUN-0093), package README, 09-tooling infra and catalog READMEs |

Evidence: `validate-docker-compose.sh` default mode 71 selections and 340
services; `check-operations-catalog.py` PASS; version projection in sync;
`check-all-hardening.sh` PASS; provisioning and secret-metadata tests pass.
An isolated project (`-p s11-probe`, a stub `mng-pg` on a separately named
network, visible placeholder secrets) ran the real definition: provisioning
exit 0 and idempotent on re-run; broker healthy as `ruby` with a read-only root,
`CapDrop=[ALL]` and a `127.0.0.1` binding; 401 without credentials, heartbeat
200, 200 with credentials, a pact published (201) and read back; no secret in
the container environment or any log; the project and its network removed.
Live start is NOT_RUN: it needs the two secrets generated and the `.env` keys
added, then its own approval.

Sequential review (read-only reviewer) findings and their disposition:

| Finding | Disposition |
| --- | --- |
| the loopback binding and disabled public read had no hardening assertion | `check_09_tooling` asserts both |
| the base-init contamination guard did not name the new feature | regex now includes `pact` |
| the runbook named exit 64 for a missing secret; `set -e` exits 1 there | runbook distinguishes 64 (empty) from 1 (missing or unreadable) |
| hard-coded basic-auth user in a documented command; blank line splitting the AUTO registry table | fixed |
| Renovate's default versioning treats `-pactbroker2.121.2` as a fixed suffix, so the pin would never move | packageRule with regex versioning on the image version |
| `PACT_BROKER_BASE_URL` unset | kept unset; POL-0093 records why and when to set it |
| fourth near-copy of the feature-provisioning SQL prologue | deferred: a shared prologue is worth extracting the next time the refusal logic changes |

### S10/S11 CI finding (after merge)

PRs #210 and #214 were merged while `validation-changed` failed on
`invalid-initial-status`: new guide, policy, runbook and package README
documents must start at `draft`, and the eight WireMock and Pact Broker
documents were created `active`. The local gate did not catch it because it
selects the metadata comparison base only from `EVENT_NAME` and `PR_BASE_SHA`,
which a local run does not set. Moving them back needs reverse-transition
override evidence, so they stay `active` and this record is the deviation.
From S12 on, new documents start at `draft` (promoted after live acceptance)
and `check-document-metadata.py --mode check-changed` runs locally with
`TEMPLATE_GATE_BASE` set to `origin/main`.

### S12 — Spark and Iceberg (source)

| Unit | Change |
| --- | --- |
| Catalog | `seaweedfs-s3` enables the built-in Iceberg REST catalog on `${SEAWEEDFS_ICEBERG_PORT:-8181}` (exposed on `object_net`, no host port, no route); Lance and embedded IAM stay off. The catalog signs with the S3 identities (SigV4) |
| Table bucket | new `seaweedfs-table-bucket` job (`lakehouse` only) creates the `lakehouse` table bucket (admin-owned), a policy granting the `lakehouse` identity ten namespace and table actions (no policy change, no bucket deletion), and the `dev` and `test` namespaces, all idempotent; `seaweedfs-buckets` is unchanged apart from an empty-secret check |
| Identity | new `lakehouse` identity (STRG-015) with `Read/Write/List/Tagging:lakehouse`; secret mounted into `seaweedfs-s3` and `spark` |
| Spark | `infra/04-data/lakehouse/spark/`: `apache/spark:4.1.3-scala2.13-java21-python3-ubuntu` plus `iceberg-spark-runtime-4.1_2.13` and `iceberg-aws-bundle` 1.11.0 added with SHA-256 checksums (SHA-1 matched Maven Central). One-shot job on `template-job-med` with 2 CPUs and 2 GiB, read-only root, `object_net` only. The wrapper writes `spark-defaults.conf` to tmpfs (catalog `lakehouse` as default, in-memory session catalog, no UI) and exports the secret into the process. Default command `SHOW NAMESPACES` |
| Profile | new `lakehouse` (capability) with the SeaweedFS closure; POL-0078 row and companion row |
| Contracts | root include and secret; `SEAWEEDFS_ICEBERG_PORT` (the bucket name and region are fixed, not knobs); AD-0026 `object_net`; SeaweedFS guide and policy (consumer row, minimal-surface control); version projection (local image); m0021 row and re-rendered SeaweedFS rows; pinned counts in `test_secret_metadata_sync`; the SeaweedFS surface test now asserts the catalog flag, no host port and an S3-only route |
| Documents | new subject `0094-lakehouse` (GDE/POL/RUN-0094, `draft`), Spark package README (`draft`), 04-data infra and catalog READMEs |

Design finding: a scoped identity cannot create a namespace in a table bucket
it does not own, and `Admin:<bucket>` does not grant table bucket creation.
Two working options were measured: a bucket owned by the identity's account
(`weed shell s3tables.bucket -account`) or an admin-owned bucket with a table
bucket policy. The policy route was chosen because it stays inside the existing
`aws-cli` job and needs no master or JWT access. Another identity sees the
table bucket as not found.

Evidence (isolated SeaweedFS 4.47 probe and the repository rehearsal):
the bucket script created the bucket, policy and namespaces and a second run
changed nothing; the built image as `spark` with a read-only root and
`CapDrop=[ALL]` listed namespaces, created a table, inserted and counted three
rows, compacted with `rewrite_data_files` and dropped the table with `PURGE`,
using only the `lakehouse` identity, which was denied on `loki-bucket`.
The disposable SeaweedFS rehearsal (`HYHOME_SEAWEEDFS_REHEARSAL=1`, the real
rendered services on temporary data) passes 8/8, including the new
`test_3_lakehouse_catalog_is_scoped_to_its_identity`.

`validate-docker-compose.sh` (`lakehouse`: 7 services), catalog, hardening,
version projection and the metadata check against `origin/main` pass. Live is
NOT_RUN: it needs STRG-015 generated, the `.env` key, a `seaweedfs-s3`
recreate and a `seaweedfs-table-bucket` run, each approved.

Sequential review (read-only reviewer) findings and their disposition:

| Finding | Disposition |
| --- | --- |
| `s3tables:*` also granted policy and bucket control, contradicting the documents | measured: SeaweedFS enforces table actions individually; ten actions (`GetTableBucket`, `List/Create/Get/DeleteNamespace`, `ListTables`, `Create/Get/Update/DeleteTable`) carry a full Spark round trip (create, insert, `rewrite_data_files`, `expire_snapshots`, schema change, `DROP … PURGE`); the identity is denied `PutTableBucketPolicy` and `DeleteTableBucket`, asserted in the rehearsal and a hardening check |
| `LAKEHOUSE_TABLE_BUCKET` renamed the bucket but not the identity scope; `LAKEHOUSE_S3_REGION` could disagree with the job | both knobs removed; `lakehouse` and `us-east-1` are fixed |
| the S3 Tables steps sat in `seaweedfs-buckets`, on the startup path of eight profiles | moved to `seaweedfs-table-bucket` under `lakehouse` only; Spark waits on it |
| POL-0024 and the SeaweedFS README still listed the old profiles and identities | updated, with the new job and its policy reset behaviour |
| no automated check read the Spark wrapper; S12 added no hardening line | `check_04_data` asserts the four catalog keys and forbids a wildcard or control action in the table bucket policy |
| `AWS_REGION` unguarded, no empty admin-secret check, unconditional policy rewrite undocumented, namespace list compared as ordered, `cpus: 2.0` | fixed |
| POL-0086 has no row for checksum-pinned build downloads (also the Gatus tarball) | deferred: pre-existing gap; the Spark README states manual ownership |

### k3d removal (source, owner instruction 2026-09-23)

The owner asked to remove the k3d integration from Traefik and everywhere
else, and chose the full scope including Kubernetes observability. This
replaces the S01/S05 "minimal `k3d-hyhome` membership" target with none.

| Unit | Change |
| --- | --- |
| Networks | `k3d-hyhome` attachment and fixed address removed from Traefik (`.2`), Prometheus, Loki, Tempo, Alloy, Grafana, `mng-valkey`, OpenBao (`.17`) and `pg-router`; the root external network and `K3D_HYHOME_NET_NAME` (root and core-readiness examples) removed |
| Traefik | file-provider routes `adminer-k3d`, `argocd-k3d`, `headlamp-k3d`, `kiali-k3d`, `rollouts-k3d` deleted; `k3s.yml` kept, it routes the native k3s NodePort and not k3d (matches #217) |
| Prometheus | the Argo CD, kube-state-metrics, Istio and Argo Rollouts NodePort jobs and `alert_rules.k8s.yml` removed from both configs |
| Grafana | the `Kubernetes` dashboard folder (20 dashboards) and its provider, the four Argo CD dashboards, and the `k3d-hyhome` default of the Prometheus dashboard's cluster variable removed |
| Checks | the OpenBao `172.18.0.17` hardening assertion and the `k3d-hyhome` string in the core-readiness guard removed (the guard still rejects any external network); pinned public env-key counts updated |
| Documents | REQ-0023 STORY-03 and FR-0003, AD-0026 description, 0031, spec, POL/GDE-0077, Prometheus guide and policy, and the Traefik, OpenBao, observability, Grafana, Loki, Tempo and PostgreSQL-cluster READMEs; the m0021 inventory re-rendered. The ADR-0026 decision record is left as the historical decision |

Evidence: `validate-docker-compose.sh` 71 selections; catalog PASS;
hardening PASS; metadata check against `origin/main` 0 violations; the
Compose, secret-metadata and core-readiness tests and `run-ci-gate.py --profile changed` (exit 0) pass. Live is NOT_RUN: the
nine containers keep their `k3d-hyhome` endpoint until each is recreated, and
the `k3d-hyhome` network itself (owned by k3d) is not deleted.

### Conftest (source, owner request 2026-09-23)

The owner asked for Conftest to be implemented and included in the Docker
stack.

| Unit | Change |
| --- | --- |
| Service | `infra/09-tooling/conftest/`: `openpolicyagent/conftest:v0.70.1` one-shot job under the new `policy-check` profile; UID 1000, read-only root, `network_mode: none`, only `infra/` mounted read-only (never `secrets/`, `.env` or the Docker socket) |
| Policies | `compose` namespace: deny privileged outside `cadvisor`, missing profile, `:latest` or untagged image, literal value in a password/secret/token/key variable; warn on host ports on all interfaces. `dockerfile` namespace: deny untagged or `:latest` `FROM`, `ADD` from a URL without `--checksum` |
| Tests | `compose_test.rego` and `dockerfile_test.rego` (12 cases); `run.sh` runs `conftest verify` before testing the source |
| Contracts | root include; POL-0078 `policy-check` row; m0021 row; version projection |
| Documents | new subject `0095-conftest` and package README, all `draft`; 09-tooling infra and catalog READMEs |

Evidence: the first run of the secret rule flagged 17 declarations, all false
positives (booleans, URLs, `*_CMD`, `/run/secrets/` paths); the rule now
exempts those shapes and each is a passing unit case. The job then reports
verify 12/12, Compose 281 checks with 0 failures and 44 warnings (ports on all
interfaces, mostly ingress, mail, Kafka and OpenSearch), and Dockerfile 51
checks with 0 failures. A planted file with `:latest`, privileged, no profile
and a literal password fails all four rules.

On the owner's follow-up the job is a CI check: `leaf.conftest-policy`
(`scripts/validation/check-conftest-policy.sh`, which runs the declared
Compose job and exits 2 without Docker) is a `repository-integrity` validator
and a child of `local.template-security-baseline` (pinned in
`ci_gate_contract.py`), with a manifest row and `ConftestPolicyGateTests`
pinning the job's isolation and the script's use of the declared job; `run-ci-gate.py --profile changed` exit 0 with the new leaf.

`test_secret_metadata_sync` treats a secret path in any mounted file as a
reference, so mounting `infra/` made `conftest` look like a reader of 30
secrets. `SOURCE_ANALYSIS_SERVICES = {"conftest"}` exempts it from that
scan, and a new test keeps the exemption safe: such a service holds no secret
grant, has `network_mode: none` and mounts only read-only, non-`secrets` paths.

The merge with main also moves the pinned public and optional env-key counts
to 269 and 211: #217 added `TRAEFIK_BIND_IP` and #218 kept the old counts, so
`test_secret_metadata_sync` failed on main.

### Prometheus API for hy-home.k8s (source, owner decisions 2026-09-23)

After the k3d removal nothing collects Kubernetes metrics: the NodePort jobs
are gone, and no cluster sample reaches the remote-write receiver. hy-home.k8s
asked for host-address access (Prometheus `192.168.0.13:9090` for Alloy remote
write and Kiali queries, Grafana `3000` with an anonymous Viewer API). The
owner chose Basic Auth through Traefik instead of an unauthenticated host port,
and no anonymous Grafana access (Kiali shows Grafana as unreachable).

| Unit | Change |
| --- | --- |
| Route | `prometheus-api` router on the Prometheus host, limited to `/api/v1/`, with `gateway-standard-chain` and the new `prometheus-api-auth` Basic Auth middleware; the UI keeps SSO, the admin API stays disabled, no host port is published |
| Secrets | `OBS-012` (`PROMETHEUS_API_USERNAME`), `OBS-013` (generated password file, a registry path exception like `INFRA-002`) and the derived htpasswd `INFRA-007`, granted to Traefik only; `gen-secrets.sh` derives it like `INFRA-003`/`INFRA-004` |
| Checks | `check_06_observability` pins the route rule, its middlewares and the middleware's `usersFile`; the secret metadata test counts the new key, declaration and rows |
| Documents | POL-0045 route control and disallowed widening, GDE-0045 client contract, GDE-0013 and the Traefik README secret list |

Evidence: `gen-secrets.sh --dry-run` plans `derive-htpasswd` for `INFRA-007`
and `create-generated-file` for `OBS-013`; compose validation, hardening and
the secret metadata and Compose tests pass. Live is NOT_RUN: generating
`OBS-013`/`INFRA-007`, setting the username in `.env`, and recreating Traefik
(new secret mount) and Prometheus (new router label) each need approval. The
OpenBao Kubernetes auth reconfiguration for the recreated cluster (new CA) is
also live and separately approved. (Later on 2026-09-23 the live route answered
`401` without and `200` with the credential; see the hy-home.k8s integration
runbook section.) The cluster-side Alloy and Kiali settings
belong to hy-home.k8s.

From the same request: `mng-valkey` publishes `${VALKEY_MNG_HOST_POST:-26379}`
(was `-`, so an empty value no longer drops the default); the misspelled key
name stays because the private `.env` sets it. Loki `3100`, Tempo `3200` and
Valkey `26379` stay published for the cluster. Alloy publishes OTLP
`4317/4318`, but the HOME config (`config.home.alloy`) has no OTLP receiver, so
connections are refused; deferred until a cluster trace path needs it.

### S13 — Trino (source)

| Unit | Change |
| --- | --- |
| Service | `infra/04-data/lakehouse/trino/`: `trinodb/trino:483` single node under `lakehouse`, `object_net`, read-only root with tmpfs data directory, 2 CPUs and 2 GiB, health check, waits for `seaweedfs-s3` and `seaweedfs-table-bucket` |
| Catalog | `catalog/lakehouse.properties`: Iceberg REST on the SeaweedFS catalog, `SIGV4` with `signing-name=s3`, native S3 path-style; endpoints and the `lakehouse` identity come from `${ENV:…}`, which `hyhome-trino.sh` fills from STRG-015 |
| Exposure | no authentication, so `127.0.0.1:${TRINO_HOST_PORT:-18090}` only and no route (POL-0078 companion row, POL-0094 control, hardening) |
| Contracts | root include; POL-0078 `lakehouse` members; m0021 row; `.env.example` `TRINO_HOST_PORT`; version projection; `check_04_data` pins loopback, no route, SigV4 and the environment-sourced secret |
| Documents | 0094 guide, policy and runbook extended; Trino package README (draft); Spark and 04-data READMEs |

Measured on an isolated SeaweedFS 4.47 with the scoped identity: SigV4 fails
at start unless `s3.aws-access-key`/`s3.aws-secret-key` are set, and listing
tables fails with `Failed to list views` unless
`iceberg.rest-catalog.view-endpoints-enabled=false`. With both, create,
insert, update, `optimize`, schema change, list and table removal work. The
SeaweedFS rehearsal now starts the rendered `trino` service and proves the
same round trip (`test_3_trino_reads_and_writes_the_lakehouse_catalog`); 9/9
pass. Live is NOT_RUN: it needs the S12 live steps first.

### Secret, env and OpenBao cleanup (owner request 2026-09-23)

Live, on the owner's instruction; names, counts and booleans only.

| Step | Result |
| --- | --- |
| Diagnosis | the private registry `SEC-003` row spanned three lines, so `--sync-metadata` rejected the file and 16 public IDs added since S06 never reached it; OBS-013/INFRA-007 files existed at 0 bytes |
| Backup | private registry and `.env` copied to `secrets/.backup-20260923/` (`0700`/`0600`) |
| SEC-003 | registry value compared privately with `openbao_unseal_keys.txt` (same three lines: true), then replaced by the example's placeholder row; the file stays the single copy |
| Sync | `--sync-metadata` then `--sync-metadata-prune`: 16 IDs added, 7 retired rows (`SEC-001`, `STRG-001`–`006`) and 6 retired `.env` keys (`INFRA_*`, `K3D_HYHOME_NET_NAME`, `VAULT_*`) removed, 7 public keys added; both checks exit 0 |
| Generation | `gen-secrets.sh` created PG-026, STRG-015, AUTO-018, OBS-013 and derived INFRA-007 (all non-empty, `0640`) |
| Quarantine | 14 files with no consumer (MinIO, Vault, InfluxDB, Supabase DB key, SonarQube, Terrakube MinIO, agent-office Valkey, `mlflow_s3_password`, empty `web_scraper_chrome_path`) moved to `secrets/.retired/2026-09-23/`; `openbao_metrics_token.custody` stays |
| Modes | 38 world-readable secret files set to `0640` after checking every consumer has `group_add` 1000 or runs as uid 0/1000; `certs/rootCA.pem` stays public |

Deviation: `secrets/README.md` said not to prune the private `SEC-001` row
before the Vault credential disposition. The prune removed it; the backup
keeps the row and the token file is quarantined, so nothing is lost, and the
README now states the new state. The backup registry was not Git-ignored:
`.gitignore` now covers `secrets/.backup-*/` and `secrets/.retired/`, and the
main checkout excludes them locally until this merges.

Source changes in the same branch:

- OpenBao policies: the uncommitted `eso-read-platform.hcl` began with a stray
  path line (invalid HCL); all policies now have header comments and
  `bao policy fmt` layout. `operator.hcl` adds `auth/kubernetes/config` and
  `auth/token/create/k8s-bootstrap`. Hardening keeps the two k8s policies
  read-only and every policy free of path wildcards.
- RUN-0085: new "hy-home.k8s Kubernetes Auth" section (one-time root session;
  per-rebuild OIDC operator steps with `disable_local_ca_jwt` and the
  `k8s-bootstrap` token role), procedure numbering fixed, legacy Vault file
  location updated. POL-0085 and GDE-0085 state the new operator scope.
- `gen-secrets.sh` rewrote the INFRA-003/004 htpasswd files on every run
  because bcrypt salts differ; it now keeps an entry that `htpasswd -v`
  verifies, with a regression test.

Live NOT_RUN: Traefik must be recreated to read the new INFRA-007 file (a
single-file mount keeps the old inode); the OpenBao root session and per-
rebuild steps are the owner's (OIDC browser login).

### OpenBao Kubernetes auth live application (2026-09-23)

Run by the owner from a throwaway `openbao/openbao:2.6.2` client container;
results only, no values.

| Step | Result |
| --- | --- |
| Session 1 (temporary root) | `kubernetes` auth enabled; policies `eso-read-platform`, `k8s-bootstrap`, `hy-home-operator` written; token role `k8s-bootstrap`; `secret/platform/argocd` version 1; root revoked (lookup rejected), generate-root not started. The ESO role write lost its namespace argument to a broken line continuation, and the snapshot, CA read and token write failed with permission denied because the container ran as its own non-root user |
| Session 2 (`--user` = host uid, one-line commands) | snapshot `pre-k8s-role.snap` taken before root; role `eso-read-platform` bound to `external-secrets/external-secrets`; root revoked (lookup rejected); `auth/kubernetes/config` host `https://192.168.0.13:6550` with the new cluster CA, as the OIDC operator |
| Bootstrap token | first write needed `-force`. The reissued token had policies `default`, `k8s-bootstrap`, orphan `true`, read `platform/argocd` allowed and `hy-home/02-auth/keycloak` denied, but a TTL of about 32 days: token roles ignore `token_ttl`/`token_max_ttl`, so the role had no cap. That token revokes itself; the operator reissues with `ttl=2h explicit_max_ttl=2h` |
| Pending | next root session: `auth/token/roles/k8s-bootstrap` `token_explicit_max_ttl=2h` |

RUN-0085 now carries the commands as run: host preparation, the client
container with `--user`, one-line commands, root passed per command through a
shell function, and `-force` for the token role.

### hy-home.k8s integration runbook (owner request 2026-09-23)

The owner asked for one document with the whole procedure. New subject
`12-infra-net/0096-k8s-integration` (guide, policy, runbook; draft) holds the
host-address contract, its controls and an eight-phase runbook: repository,
secrets and `.env`, gateway and Prometheus, host endpoints, OpenBao Kubernetes
auth, hand-off, verification from both sides, and cleanup, with a
troubleshooting table from every error met today. RUN-0085's k8s section is
now a pointer, so the procedure has one owner. The runbook passes the
Prometheus credential to curl through stdin (`-K -`), not an argument, and
reads the OpenBao client image from Compose.

Measured while writing it: phase 3.2 gives `401` without and `200` with the
credential, and `401` for the UI path; phase 4.1 shows ports 443, 3100, 3200
and 26379 open. Six Compose containers are still attached to the orphaned
`k3d-hyhome` network. There is currently no k3d cluster (port 6550 is closed),
so after the rebuild, phase 5 (5.1–5.3, 5.5–5.7) must run again with the new
CA.

### Prometheus API credential through OpenBao (hy-home.k8s request 2026-09-23)

hy-home.k8s (PR #72) reads the Prometheus API credential from OpenBao
`secret/platform/prometheus-api` through ESO for Alloy remote write, Kiali and
Argo Rollouts analysis.

| Unit | Change |
| --- | --- |
| Policies | `eso-read-platform` reads `platform/prometheus-api` data and metadata; `hy-home-operator` may create, read and update that entry (rotation without root); `bao policy fmt` clean |
| RUN-0096 | client container mounts the password file and passes the non-secret username as `PROM_API_USER`; 5.4 split into 5.4.1 first setup (now also writes the entry), 5.4.2 additional application (Session 3: both policies, the entry, the `k8s-bootstrap` cap) and 5.4.3 verify and revoke, with expected outputs; new rotation section covering `OBS-013`, `INFRA-007` and the OpenBao entry; troubleshooting row for `401` after a rotation |
| Documents | GDE/POL-0096, GDE/POL-0045, GDE-0085 and the OpenBao README state the new source and the joint rotation |

Live Session 3 is the owner's (NOT_RUN). Expected results to record:
`2`, `2`, `current_version` at least `1`, `7200`, `root revoked`,
`Started false`. Grafana anonymous access stays off (owner decision earlier on
2026-09-23). Conftest exists as the `policy-check` Docker job and CI gate, with
no host binary; a `~/.local/bin/conftest` for hy-home.k8s `policy-gates` is not
installed.

A diagnostic in this session printed the last character of two secret files
while checking for trailing newlines. Only a boolean should have been printed.

### S14 — Flink (source)

New leaf `infra/04-data/lakehouse/flink/` under the `lakehouse` profile: a
session cluster (`flink-jobmanager`, `flink-taskmanager` with two slots) built
from the `flink` 2.1 Java 21 image plus the Iceberg Flink runtime, the AWS
bundle, the Kafka SQL connector and the Hadoop client, each pinned by
SHA-256. The probe showed the Hadoop client is required
(`ClassNotFoundException: org.apache.hadoop.conf.Configuration`) and that the
image entrypoint needs root for `gosu`, so the services run as UID 9999
through their own wrapper and pass Flink settings as `-D` arguments; the image
configuration file stays untouched under a read-only root.

| Unit | Change |
| --- | --- |
| Catalog and identity | the wrapper exports the `lakehouse` secret into each JVM and writes `CREATE CATALOG lakehouse` (SigV4, S3FileIO, path-style) to `/tmp/lakehouse.sql`; the SQL client loads it with `-i` |
| Exposure | REST API and UI on `127.0.0.1:${FLINK_HOST_PORT:-18091}` only, no route, `web.submit.enable=false` |
| Networks | `object_net` (catalog, S3) and `kafka_net` (`kafka-1:19092`); Kafka stays in its own profile, so it is not a dependency |
| State | file checkpoints in `${DEFAULT_DATA_DIR}/flink/checkpoints`, shared by both containers; the operator creates it `2770` and the containers write through `SECRETS_GID` |
| Checks | hardening pins loopback, submit off, no route and the catalog signing keys; version projection adds the local image; `FLINK_HOST_PORT` in `.env.example` (public 272, optional 213) |
| Documents | GDE/POL/RUN-0094, POL-0078 `lakehouse` row, `04-data` README, Spark and Trino README links, m0021 rows |

Rehearsal (`test_3_flink_writes_the_lakehouse_catalog`, isolated SeaweedFS,
checkpoint directory `2770`): a batch insert and a checkpointed streaming
insert from a bounded `datagen` source both commit, and a batch count returns
7 rows. The full SeaweedFS rehearsal passes 10/10. A negative hardening run
with `web.submit.enable=true` fails on that pin. Live is NOT_RUN: it needs the
checkpoint directory, the image build and the S12 live steps, each approved.
ksqlDB removal (S19) waits for Flink live acceptance.

Sequential review (read-only reviewer): no Critical; security no findings.

| Finding | Disposition |
| --- | --- |
| A streaming `INSERT` never commits: checkpointing is off by default and the interval is a client setting, so a JobManager `-D` cannot enable it | fixed: the wrapper's catalog file sets a 60 s interval; guide and README say so |
| m0021 recovery cells for `flink-*` carried Spark's "holds no state" text | fixed: they name the checkpoint directory as recoverable job state |
| Rehearsal did not pin `SECRETS_GID`, so UID 9999 depended on the host GID | fixed: the render environment sets it to the test user's group |
| `install -d` gives the operator's primary group, not `SECRETS_GID` | fixed: `-g "${SECRETS_GID:-1000}"` in README and RUN-0094 |
| TaskManager took its limits implicitly from the template | fixed: explicit 2 CPUs / 2 GiB |
| Bind volume had no "must exist" note | fixed |
| A bare `sql-client.sh` has no catalog or credentials | fixed: README troubleshooting line |
| List `/tmp` and `/run` explicitly | not applied: Compose rejects the duplicate `/tmp` mount from the template (`target /tmp already mounted`) |

After the fixes: hardening, Compose, catalog, links, metadata (against the
current `origin/main`), secret-metadata tests and the Flink rehearsal pass.
`run-ci-gate.py --profile changed` passed its 487-test document suite; its only
failures were the two local group-write checks from this worktree's umask
(recorded under S04), which pass after `chmod g-w` on the tracked executables.

### S15 — Great Expectations (source)

New leaf `infra/04-data/lakehouse/great-expectations/` under the `lakehouse`
profile: a one-shot job built from `python` plus GX Core and the Trino
SQLAlchemy dialect pinned in `requirements.txt` (Renovate). `hyhome-gx.py`
builds an ephemeral context with a Trino SQL data source
(`trino://great-expectations@trino:8080/lakehouse`) and checks each tracked
suite in `suites/` (`<schema>.<table>` plus GX expectations) on a whole-table
batch. The default command lists suites; `validate` exits `0` when every suite
passes, `1` when an expectation fails and `2` when nothing could be checked.
Usage events are off (`GX_ANALYTICS_ENABLED=false`); no port, no secret,
UID 1000, read-only root.

| Unit | Change |
| --- | --- |
| Service | `great-expectations` (`template-job-med`, `object_net`, depends on a healthy `trino`), suites mounted read-only |
| Checks | hardening pins analytics off, read-only suites, no port and the job template; version projection adds the local image |
| Documents | GDE/POL/RUN-0094, POL-0078 `lakehouse` row, `04-data` README, m0021 row |

Measured before the leaf existed, against a disposable Trino with a memory
catalog: the suite passed on two distinct rows and exited `1` after a
duplicate key. Rehearsal (`test_3_great_expectations_passes_and_fails_through_trino`,
isolated SeaweedFS with the HOME Trino): the tracked `lakehouse-rehearsal`
suite passes on `test.gx_rehearsal` and the same suite exits `1` after a
duplicate id. Error paths measured on the built image: no suites, a one-part
table name, a mismatched `name`, malformed JSON and an unreachable Trino each
exit `2` with the cause on stderr. A negative hardening run with analytics on
fails on that pin. Live is NOT_RUN: it needs the S12/S13 live steps.

Sequential review (read-only reviewer): no Critical.

| Finding | Disposition |
| --- | --- |
| `validate` with no suites exited 0 | fixed: no suites is exit `2` |
| Placement differs from the S01 design (`09-tooling`, `lakehouse_net`) | ruling added below |
| `ProgressBarsConfig` may not exist in GX 1.x | kept: the rehearsal runs GX 1.23.1 with it, and without it the run printed progress bars |
| m0021 lifecycle cell carried Spark's text | fixed for `great-expectations`, and for the `trino` and `flink-*` rows that had the same copy |
| One- or three-part table names, errors sharing exit `1`, unread `name`, unused `GX_SUITES_DIR`, a needless `chmod` layer, image tag drift on a GX bump, unpinned job template | fixed: two-part check, exit `2` for errors, `name` must match, path inlined, layer removed, README step, hardening pin |

### S16 — Superset with Keycloak OIDC (source)

New leaf `infra/04-data/analytics/superset/` under a new `bi` profile and a new
Stage 05 subject `04-data/0097-superset`. The image is `apache/superset` plus
the PostgreSQL driver, Authlib and the Trino dialect (`requirements.txt`,
Renovate). `superset-db-provision` creates the feature-owned role and database
on `mng-pg` through the shared runner; `superset-init` migrates, syncs roles
and registers `lakehouse` as `trino://superset@trino:8080/lakehouse`; the web
server runs one gunicorn process behind Traefik.

| Unit | Change |
| --- | --- |
| Login | Flask-AppBuilder OAuth with provider `keycloak` (client `home-superset`, PKCE S256, userinfo at `<realm>/protocol/openid-connect/userinfo`); registration role `Gamma`; router `gateway-standard-chain@file` only (POL-0079 native OIDC list) |
| Secrets | PG-028 database password, PG-029 user, IAM-013 client secret, AUTO-020 signing key; all Docker secret files read by `superset_config.py`. The migration engine reads only the URI, so the URI with the password is built in memory (`URL.create`); nothing puts a credential in the environment or argv |
| Trust | public CAs plus the local root CA written to `/tmp` for the Keycloak calls |
| Checks | hardening pins OIDC, `Gamma`, PKCE, the file-based key, no key variable and no port; feature-job contract and secret-metadata tests (public 275, optional 216, declarations 86, rows 119); version projection |
| Documents | GDE/POL/RUN-0097 (Keycloak client spec and first admin), POL-0078 `bi`, POL/GDE-0079 client matrix, `04-data` READMEs, m0021 rows |

Rehearsal (`FeatureProvisioningRehearsalTests.test_6_superset_migrates_and_serves_on_its_own_database`,
throwaway PostgreSQL on an internal network, a database password with a quote,
a backslash and an `@`): provisioning, the init job's own command twice, the
`lakehouse` row in `dbs`, `/health` `200`, anonymous `/api/v1/database/`
`401`, the Keycloak option on `/login/`, and no password or client secret in
the container environment. The class passes 6/6. A negative hardening run with
registration role `Admin` fails on that pin. The first probe showed the
migration engine ignores `SQLALCHEMY_ENGINE_OPTIONS` (`fe_sendauth: no
password supplied`), which is why the URI carries the password.

Live is NOT_RUN: the Keycloak client `home-superset` (a remote change),
IAM-013, secret generation, the image build and the first admin are the
owner's, each approved. Group-based access (`allowed_groups`) stays an open
owner decision; until then any realm user can log in as `Gamma`.

Sequential review (read-only reviewer): no Critical.

| Finding | Disposition |
| --- | --- |
| No hardening control for the router chain | fixed: gateway chain pinned, `sso-auth` refused |
| CA bundle rewritten in place on every config import | fixed: staged per process and replaced atomically |
| Missing secret or root CA surfaced as a bare traceback | fixed: named `superset: … is missing or not a file` error |
| Authlib pinned over the image's own copy | kept: the base image has no Authlib (`ModuleNotFoundError` in the probe); comment added |
| Rate-limit store line repeats the default | removed |
| POL-0078 closure row lacked `bi` | fixed |
| Runbook `exec` without `--profile bi`; throwaway admin password in argv | fixed: profile added; the password is unusable without form login and is not kept |
| `/tmp` arrives only from the template | comment added (same as Flink) |
| `ENABLE_PROXY_FIX` trusts forwarded headers from any `edge_net` peer | not changed: repository-wide pattern; belongs to the network-flow policy |
| `superset-init` holds the client secret it does not use | not changed: the shared config reads it at import |

The Keycloak userinfo round trip is unverified until the live login.

### S17 — Stalwart as configured internal mail (source)

The tracked leaf could not start on its pinned image: v0.16 has no
`stalwart-mail` binary, keeps its datastore in `/var/lib/stalwart` and reads
only the datastore location from `config.json`; listeners, domains and relay
policy live in the datastore and are set through the management API. The leaf
also published SMTP, submission, SMTPS, IMAPS and ManageSieve on every host
interface, against the owner's internal-only answer.

| Unit | Change |
| --- | --- |
| Server | image user (UID 2000), read-only root, `cap_drop: ALL` plus `NET_BIND_SERVICE` (the binary carries that file capability and cannot exec without it under `no-new-privileges`); no host port; `edge_net` for the routed admin UI and new `mail_net` (10.250.14.0/24) for SMTP |
| Configuration | `config/config.json` (RocksDB datastore) and `config/plan.ndjson` applied by the one-shot `stalwart-config` (server image plus pinned `stalwart-cli` 1.0.12, which ships without a shell): domain `${DEFAULT_URL}`, host `mail.${DEFAULT_URL}`, listeners reconciled to SMTP 25, submission 587, IMAPS 993, HTTP 8080, `allowRelaying = false` |
| Secret | `stalwart_password` (COMM-006) becomes `STALWART_RECOVERY_ADMIN` inside the server and job processes only; the Compose file has no credential |
| Mailpit | also joins `mail_net` for container SMTP capture |
| Env | ten unused host-port keys and `STALWART_PORT` removed from `.env.example` (public 264, optional 205) |
| Checks | hardening pins no host port, the relay rule, no credential variable, `mail_net` and the read-only template |
| Documents | GDE/POL/RUN-0070 v2, Stalwart and tier READMEs, POL-0078 `mail-server`, AD-0026 network table, m0021 rows, version projection |

Measured on a throwaway server: a fresh datastore listens on 25, 443, 465,
993, 995, 4190 and 8080. After the plan and one restart it listens on 25, 587,
993 and 8080 only; a second apply converges (`0 failed`). An empty named
volume takes the image directory's owner (UID 2000) on first mount, so a
forced UID 1000 failed with `Permission denied` on the RocksDB `LOG`; the
server now runs as the image user. Rehearsal (`StalwartRehearsalTests`,
rendered HOME services on an internal network): plan applied twice, restart,
exactly those four listeners, `220 mail.rehearsal.test`, `550 5.1.2 Relay not
allowed` for an external recipient, the local domain recognised, and the admin
secret absent from the logs.

TLS on 587/993 uses Stalwart's default certificate until a Certificate object
is configured. Live is NOT_RUN: the data directory, the image build, the plan
and a restart are the owner's, each approved. Native OIDC for the admin UI
stays with S18 (Task 0007 item 6).

### S18 — Route authentication alignment (source)

All 50 Traefik HTTP router declarations (49 Compose labels and the
file-provider `k3s-ingress`) were classified by what a request that passes
Traefik meets (`gateway-standard-chain@file` is only retry and circuit
breaker). Four reached an application with no identity check:

| Route | Profile | Finding | Change |
| --- | --- | --- | --- |
| `qdrant` | HOME (`ai`) | no API key; full read, write, delete and snapshots | SSO chain; the gRPC TCP route (which also carried an HTTP middleware Traefik cannot apply) removed |
| `kafka-rest` | `messaging` | REST Proxy without authentication | SSO chain |
| `schema-registry` | `messaging` | register or delete schemas without authentication | SSO chain |
| `mongo-express` | `mongodb` | credentials set but ignored: 1.x reads them only with `ME_CONFIG_BASICAUTH=true` (image `config.default.js`), leaving database admin open | `ME_CONFIG_BASICAUTH: 'true'` |

`grafana-static` (two static files) stays open by design. The cluster
variant of the `opensearch` router had no middleware; it now has the same
chain as the single-node route. Containers keep using service names on their
networks, so no internal client changes.

`RouteAuthContractTests` fails when a router has neither the SSO chain nor
an entry in its named list (native OIDC, identity provider, application or
gateway credentials, SigV4, static), when the list goes stale, when a router
has no middleware, or when any TCP router exists; GDE-0079 carries the same
matrix. A negative run with the Kafka routes reverted fails and names both.
The Open Notebook row in GDE-0079 said ForwardAuth was kept, but the router
has not used it since `b90b74837`; the row now states the IP allowlist and
application password.

Independent review (3 Important, 4 Minor, all fixed): the test missed the
file-provider router `k3s-ingress`, which has no gateway authentication, and
merged router names, so dropping the `opensearch-node1` chain would have
passed while the single-node declaration kept it. It now reads
`infra/01-gateway/traefik/dynamic/` and checks each declaration; the same
`opensearch-node1` mutation fails and names that service. `k3s-ingress` is
listed as unauthenticated and deferred to the owner. The Qdrant guide,
policy, runbook and README still described the gRPC route; the Kafka REST
comment named the router instead of the service; POL-0079's native list
lacked Dozzle and Grafana. The mongo-express premise still needs its live
proof: an unauthenticated request returning 401 after the recreate.

Also closed here, from the S17 review (merged before its review returned):
the `mail_net` trust boundary (management API and IMAPS are reachable there
without the gateway SSO chain) and the permanent fallback admin with its
rotation sequence in POL-0070 and AD-0026; the unused
`STALWART_HEALTHCHECK_URL`; paired-name comments; the template wording; the
test file's `__main__` guard moved to the end so every class is collected.

Open owner decisions at S18 (decided in S19): `allowed_groups`, the Stalwart admin UI
OIDC (its OIDC backend validates bearer tokens and does not start a browser
login), Terrakube proxy removal, and a Qdrant API key (would also need every
client configured). Live is NOT_RUN: each changed service needs a recreate to
pick up its labels or environment.

### S19 — Convergence and the approval-gated live list (source)

**Removals.** ksqlDB and StarRocks stay: the S01 rulings remove them only
after Flink and Trino live acceptance, and both are NOT_RUN. Nothing else
from S01's duplicate list remains in source (MinIO in S07, Vault in S08,
`infra_net` in S05 phase 2, k3d in its own change).

**ksqlDB and StarRocks removal (source, 2026-09-24).** Flink and Trino live
acceptance PASSED the same day (Flink batch and checkpointed streaming
inserts; a Trino read verified through Great Expectations against the
SeaweedFS Iceberg catalog). Per the S01 rulings above, ksqlDB and StarRocks
are removed: `infra/04-data/analytics/ksql/` and
`infra/04-data/analytics/starrocks/` are deleted, their root `docker-compose.yml`
includes and `.env.example` `KSQLDB_*` keys are gone, the `ksql` Compose
profile and its `kafka-1`/`schema-registry` membership and kafbat-ui RBAC
resource are removed, and GDE/POL/RUN-0018 (ksqlDB) and GDE/POL/RUN-0020
(StarRocks) move to `docs/98.archive/superseded/05.operations/catalog/04-data/`
with `status: superseded` and `superseded_by` pointing at GDE/POL/RUN-0094
(the Flink/Trino lakehouse subject). Neither service was ever deployed on this
host (no host data directory or volume existed), and `ksql-datagen` was
already a no-op with no consumer, so this is a source-only removal with no
live cutover step. ADR-0015 and ADR-0019 keep their original Context and
Decision text and gain a `## Follow-up` note naming Flink and Trino as the
current replacements, per the repository's no-rewrite-history convention.
The owner then chose supersession: ADR-0039 (analytics engines after the
lakehouse convergence) and ADR-0040 (the 04-data hardening gate restated
without ksqlDB) were proposed in #249 and accepted in the follow-up PR, which
moves ADR-0015 and ADR-0019 to `docs/98.archive/superseded/02.architecture/decisions/`
with `superseded_by` and two ledger rows. REQ-0005 was reviewed with them: its
scope now covers InfluxDB, OpenSearch, Flink and Trino, stream processing
and SQL/OLAP are restated engine-neutrally as FR 0005 and 0006 (acceptance
cites the 2026-09-24 live run), and FR numbers 0002 and 0004 are retired
into `reserved_history`.

**Template ledger.** S02 read all 40 registered templates and found no gap
for the planned tools. S10–S17 added thirteen services (Conftest one more) with the existing
package README, guide, policy and runbook shapes; none needed a new heading
or field. One validator false positive was met: the runtime-version check
reads an SMTP enhanced status code such as the relay refusal's as a version
pin (S17), worked around by naming the refusal in words (deferred below).

**Documents.** AD-0009 now names the `analytics-engineering`,
`contract-testing`, `api-mock`, `backup` and `policy-check` profiles (the
drift recorded in S10).

**Env and secret metadata.** Public `.env.example`, the example registry and
the root secret declarations agree (`test_secret_metadata_sync`). The private
copies change only on the owner's run: `gen-secrets.sh --sync-metadata-check`,
then `--sync-metadata` for the Superset rows (PG-028, PG-029, IAM-013,
AUTO-020) and `--sync-metadata-prune` for the eleven Stalwart port keys
removed in S17.

**Owner auth decisions (2026-09-24).** The four open decisions were
verified against source, running containers and upstream documentation, then
decided by the owner:

| Decision | Verified basis | Source change |
| --- | --- | --- |
| OAuth2 Proxy `allowed_groups = ["/admins"]` | the allowlist was commented and `email_domains=["*"]`, so every realm user passed every SSO route; the realm has one human user, in `/admins`; Kafbat already maps the full-path `/admins` from the same `groups` claim | config, hardening guard, GDE/POL-0079 |
| Stalwart admin UI keeps gateway SSO plus its own admin login | Stalwart's OIDC directory replaces the password backend for every account, so IMAP/SMTP clients would need App Passwords | POL-0070 records the decision; item closed |
| Terrakube at `iac` activation | not running; API and UI reuse the OAuth2 Proxy client id; the API route's ForwardAuth blocks Terraform CLI, API-token calls and `terrakube-executor`, which calls the API by its public URL | compose comment, README, GDE-0079 row |
| Qdrant API key | zero collections; the only real client is the Prometheus scrape (Open WebUI sets `VECTOR_DB_URL` without `VECTOR_DB`, so it uses its default store); `edge_net` members could write without authentication | `qdrant_api_key` (AI-008), start script, Prometheus `bearer_token_file` in both configs, `QdrantApiKeyContractTests`, Qdrant docs |

Qdrant rehearsal with a synthetic key on `qdrant/qdrant:v1.19.1-unprivileged`:
`/readyz` 200 without the key (the healthcheck is unchanged), `/metrics` and
`/collections` 401 without it, `/metrics` 200 with `Authorization: Bearer`.

**`k3s-ingress` removal (owner decision 2026-09-24).** The file-provider
router forwarded any `*.k8s.hy.home.arpa` host to `192.168.0.13:32246` with no
gateway authentication. Native k3s is still active on the host and that
NodePort answers (404 at `/`), but the Traefik access log shows no request
through the router in the prior seven days. `k3s.yml` is deleted; the route
contract has no unauthenticated exception left. The running Traefik watches
the operations checkout's `dynamic/` directory, so the router disappears when
that checkout pulls the merge; no restart. Rollback: restore the file from Git.

Independent review of the decisions (3 Important, 7 Minor): the rollback
signal for `allowed_groups` assumed a visible 403 that `sso-errors` hides;
POL-0034 kept a no-authentication sentence; the Terrakube record missed the
executor. All fixed, with the test's blank lines and two more assertions (the
Prometheus grant and the root declaration). The Qdrant alert rule, the
exporter-down regex and the dashboard used job `qdrant-monitor` while the
scrape job is `qdrant`, so `QdrantDown` could never fire; now `qdrant`.
Deferred: a read-only key for Prometheus and the unused Open WebUI
`VECTOR_DB_URL`, which the RAG workflow docs still describe.

The Mailpit hardening test failed on main since S17: its fixture tree lacked
the Stalwart plan, so the Stalwart relay guard failed before the Mailpit check.
The fixture now copies `plan.ndjson`.

**Approval-gated live list** (each step separately approved; none run when written; the Done marks and the live sections below record what ran later):

| Stage | Live steps |
| --- | --- |
| S10 WireMock, S11 Pact Broker | start on their profiles; Pact Broker needs its DB provisioning **Done 2026-09-24** |
| S12 Spark, S13 Trino, S14 Flink, S15 Great Expectations | STRG-015 and the `.env` key, `seaweedfs-s3` recreate, `seaweedfs-table-bucket`; Flink checkpoint directory (`2770`, group `SECRETS_GID`) and image build **Done 2026-09-24** |
| S16 Superset | Keycloak client `home-superset` (remote), IAM-013, secret generation, image build, first admin **Done 2026-09-24** |
| S17 Stalwart | empty data directory, image build for `stalwart-config`, plan, restart **Done 2026-09-24** |
| S18 routes | recreate `qdrant`, `kafka-rest`, `schema-registry`, `mongo-express` and the OpenSearch cluster node where running **Done 2026-09-24** (running services only) |
| S19 `allowed_groups` | recreate `oauth2-proxy`; then an owner login through one SSO route must reach the application. `sso-errors` turns 401–403 into the sign-in flow, so a denial shows as a loop ending on the OAuth2 Proxy error page and a group denial in its log, not as a 403 at the route. On that signal the `groups` claim is missing from the proxy's token: restore the previous config and recreate (rollback) **Done 2026-09-24** (S19 live apply) |
| S19 Qdrant key | generate AI-008 (`gen-secrets.sh`), recreate `qdrant` and `prometheus` (a new secret mount needs a recreate, not a reload); `/collections` 401 without the key, `up{job="qdrant"}` 1 **Done 2026-09-24** (S19 live apply) |
| Terrakube | at `iac` activation: Keycloak client `home-terrakube` (remote), drop the API ForwardAuth, audience/RBAC acceptance |
| hy-home.k8s | RUN-0096 Session 3 (Prometheus API KV, token-role cap) and phase 5 after a k3d rebuild; disconnect the six containers from the orphaned `k3d-hyhome` network Network disconnect **done 2026-09-24**; Session 3 is the owner's |
| Acceptance | Flink and Trino live acceptance, then the ksqlDB and StarRocks removals Flink/Trino **PASS 2026-09-24**; removals follow |

### S19 live apply (2026-09-24, owner-approved)

| Step | Result |
| --- | --- |
| Pull #240 into the operations checkout | fast-forward `77296f652` → `5cfd9de8a`; Traefik dropped `k3s-ingress` without a restart (`*.k8s.hy.home.arpa` now 404 from Traefik); other routes unchanged |
| AI-008 | `secrets/data/qdrant_api_key.txt` created alone (16 alphanumeric, 0640, never printed). `gen-secrets.sh` was not used: its no-argument run would also create the unapproved Superset secrets, and `--sync-metadata-check` refuses the private registry because its SEC-003 row had 4 pipe separators instead of 9 (a multi-line value split the row). The owner restored the row to the public placeholder after confirming the shares are intact in `secrets/security/openbao_unseal_keys.txt`;`--sync-metadata`then added AI-008, PG-028, PG-029, IAM-013 and AUTO-020 (`files_changed=2`, values preserved, secret files untouched) and a rerun of the check reports`files_changed=0` |
| `qdrant` recreate | healthy; `/readyz` 200 without the key, `/collections` and `/metrics` 401 without it, `/collections` 200 with it; the key is not in the container's environment metadata; the stale `qdrant-grpc` TCP router and its "middleware does not exist" error are gone |
| `prometheus` recreate | healthy; `up{job="qdrant"}` 1 through `bearer_token_file`; `QdrantDown` loaded with `job="qdrant"`. `opensearch` (not running) and `cadvisor` (first scrape pending) were the only unhealthy targets |
| `oauth2-proxy` recreate | **Failed then fixed.** The new container crash-looped: `extra_hosts` pinned `keycloak.`/`auth.` to `host-gateway` (172.17.0.1), and Traefik publishes 443 only on `TRAEFIK_BIND_IP` since its recreate 11 hours earlier, so OIDC discovery was refused. The previous container had discovered at start 21 hours earlier, which hid the defect. Every SSO route answered 500 from about 22:52:28 to 22:53:30 UTC. Removing the two `extra_hosts` lines lets it resolve Keycloak through the Traefik `edge_net` alias like every other service; recreated healthy, unauthenticated SSO requests get 401 with the sign-in page. A test now fails if any service pins `keycloak.`/`auth.` to a host entry |
| Owner login through an SSO route | **Pass.** The owner (in `/admins`) reached the application through an SSO route after the recreate; OAuth2 Proxy logged no group denial in the following two hours. `allowed_groups` is live |

### Remaining live activation (2026-09-24, owner-approved)

| Step | Result |
| --- | --- |
| `k3d-hyhome` network | The cluster was rebuilt 2026-09-23 and uses only host endpoints (`*-external` EndpointSlices on `192.168.0.13`, ESO through `https://openbao.hy.home.arpa`); the six Compose containers were only in k3d's injected NodeHosts. Disconnected without restart; all six healthy; ExternalSecrets unchanged (`argocd-notifications-secret` and `postgres-app-secret` were already `False`, optional) |
| S18 recreates | `schema-registry`, `kafka-rest-proxy`: 401 at the routes; Kafka Connect reaches Schema Registry directly (200) and both connectors stay `RUNNING`. `mongo-express` and the OpenSearch cluster are not running, so nothing to recreate |
| S10 WireMock | healthy; admin 200 on `127.0.0.1:18088`, refused on the LAN; one tracked mapping |
| S11 Pact Broker | `pact-broker-db-provision` exit 0 (`--no-deps`: `mng-pg` hash unchanged, `mng-pg-init` not re-run); broker healthy, 401 without and 200 with basic auth, loopback only |
| S17 Stalwart | data directory created empty (UID 2000 on first start); plan: 3 created, 4 updated, 5 default listeners removed; after restart only 25, 587, 993, 8080 listen; relay refused `550 Relay not allowed`; admin route 401 |
| S12–S15 lakehouse | `seaweedfs-s3` recreated for the `lakehouse` identity (Loki and Tempo showed no S3 errors); table bucket and `dev`/`test` namespaces created; Spark lists both; Trino healthy on loopback; Flink checkpoint directory `2770`; Flink batch INSERT and a checkpointed streaming INSERT into `test.gx_rehearsal` (23 rows) finished; Trino reads 23 rows; Great Expectations suite `lakehouse-rehearsal` exit 0, three expectations true. **Flink and Trino live acceptance: PASS** |
| Operations checkout modes | 47 tracked files `0600` and 6 directories `0700` from pulls run with a restrictive umask; Flink could not read its start script and the rebuilt GX image copied an unreadable script. Restored `644`/`755` (Git reports no change), images rebuilt; later pulls use umask `022` |
| Secret registry parity (owner rule) | #243 merged; `0600` backups, then `--sync-metadata-prune`: the private registry equals the public one except value cells (209 lines each) and `.env` has exactly the public key set (the 11 retired Stalwart keys removed) |
| Superset secrets | PG-028 and AUTO-020 generated (0640). The generation run copied the three-line SEC-003 unseal-share file into its table cell and split the row again, which is how SEC-003 broke twice before; the registry was rebuilt from the public text with SEC-003 back to its placeholder and the copy holding the shares was shredded. Generation now skips multi-line values (#244) |
| S16 Superset | **Pass.** The owner created `home-superset`; four settings differed from RUN-0097 (redirect URI and web origin with the typo `hy.hom.arpa`, a service account enabled, no PKCE) and were corrected with the secret unchanged (the IAM-013 file's hash equals Keycloak's; mode set to `0640`). Generation filled the registry, which now differs from the public file only in value cells (SEC-003 empty by design). Image built; `superset-db-provision` and `superset-init` exit 0 (`--no-deps`); `superset` healthy; `/health` 200; `/login/keycloak` redirects to `home-superset` with the right redirect URI; Admin created for the `/admins` user before first login; the owner's OIDC login reached Superset as `Admin`. The browser's `service-worker.js` request is a harmless 404 |
| RUN-0096 Session 3 | owner-run (OIDC browser login and a temporary root from unseal shares). Evidence it may already be done: `kiali-grafana-auth` and both `prometheus-api-auth` ExternalSecrets are synced; only the owner can confirm the `k8s-bootstrap` role cap (`7200`) |

## Verification Evidence

Rows record each stage's result when it closed; `live NOT_RUN` rows for S10–S19
were later run, and their results are in the live sections of the Work Log.

| Stage check | Plan unit | Result at the time | Owner |
| --- | --- | --- | --- |
| S00 inventory and live state | Task 10 / S00 | PASS: four-column state, consumers and requirement trace recorded above | this Task |
| S01 target design | Task 10 / S01 | PASS (design): tree, duplicate rulings, interfaces, networks, order | this Task |
| S02 contracts and baseline | Task 10 / S02 | PASS: no template gap; env/secret safety already present; baseline recorded | this Task, S19 ledger |
| S03 static backup contracts | Task 10 / S03 | PASS 6/6 `BackupContractTests` (allowlist, recursion guard, budget order, queue cap, single-line secret, `cmd` delete refusal) | `test_compose_baseline_gates` |
| S03 accumulated gates | Task 10 / S03 | PASS: Compose 72 selections/318 services, operations catalog, projection, links, metadata changed 0, secret dry-run 106 rows, 224 unit tests (8 opt-in skipped), hardening, `git diff --check` | this Task |
| S03 isolated rehearsal | Task 10 / S03 | PASS 3/3 `BackupRestoreRehearsalTests` (`HYHOME_BACKUP_REHEARSAL=1`, after review fixes): stanza, check, full, diff, PITR to 150 of 999 rows on timeline 2 into a 0755 target; empty secret exit 64; Restic init skip, allowlist, read-only source, restore content, wrong password, prune and `cmd forget` refusal | RUN-0021 |
| S03 manual rehearsal | Task 10 / S03 | PASS: wrong pgBackRest passphrase `status: error`; SQLite WAL export kept an uncheckpointed row; Valkey `--rdb -` reload returned the key | this Task |
| S03 orchestrator end to end | Task 10 / S03 | PASS (live, 08:20 UTC) after one exit-1 run fixed by #193 | RUN-0021 step 4 |
| S03 live switch | Task 10 / S03 | PASS: `mng-pg` on the pgBackRest image, stanza, full and diff backups, WAL archive | RUN-0021 steps 1–3 |
| S03 live restore | Task 10 / S03 | PASS (files): `.env` hash and Grafana export verified from live snapshots; PostgreSQL PITR on HOME data NOT_RUN (synthetic rehearsal only) | RUN-0021 steps 5–6 |
| S03 timer | Task 10 / S03 | PASS (install): owner installed the units on 2026-09-22; `hyhome-backup.timer` enabled and active, installed units byte-identical to source, first timer-driven run 2026-09-23 03:58 KST ended `Result=success`, exit `0` (systemd, read 2026-09-24) | RUN-0021 step 3 |
| S04 structure | Task 10 / S04 | PASS: `seaweedfs-mount` removed; `seaweedfs` renders master/volume/filer/S3, `seaweedfs-mount` renders nothing; no remaining current reference | this Task |
| S04 accumulated gates | Task 10 / S04 | PASS: Compose 71 selections/314 services, operations catalog, projection (89 repositories), links (942 documents, 0 failures), `git diff --check`; 623 unit tests with 2 local-only failures (group-write bit on two entrypoint scripts from this worktree's umask 002, not tracked by Git; CI unaffected) | this Task |
| S05 phase 1 source | Task 10 / S05 | PASS: 150 services assigned, rendered memberships equal the assignment; every traced flow shares a segmented network (static trace plus review); review Critical/Important findings fixed; Compose 71 selections/314 services; 5/5 `NetworkSegmentationContractTests` | this Task, AD-0026 |
| S05 phase 1 live | Task 10 / S05 | PASS with one open item: 53 services recreated and healthy, SSO and forwarded headers verified; OpenBao sealed until the owner unseals | this Task |
| S06 source and rehearsal | Task 10 / S06 | PASS: 6/6 `SeaweedfsRehearsalTests`, 2/2 `SeaweedfsContractTests`, secret registry 110 rows (STRG-007–010) | GDE/POL/RUN-0024 |
| S06 HOME activation | Task 10 / S06 | PASS: healthy, anonymous refused, admin bucket round trip, only S3 routed, isolated internals, SeaweedFS set in the Restic snapshot; registry Value cells pending the owner's `SEC-003` repair | RUN-0024 |
| S05 phase 2 source | Task 10 / S05 | PASS: 135 attachments removed across 41 Compose files, `infra_net` and its env keys gone, 13 `check_service_network` assertions replace the fixed-address ones; review findings fixed | this Task, AD-0026 |
| S05 phase 2 live | Task 10 / S05 | PASS: 56 containers recreated, `infra_net` removed, Loki container coverage 6 → 56, SSO 302, Gatus 6/7 then 7/7 after the owner's unseal; Agent SecretID open | this Task |
| S09 Testcontainers | Task 10 / S09 | PASS: 2/2 integration tests against the declared PostgreSQL pin after the move to `tests/validation/`; skip-without-opt-in verified; `run-ci-gate.py --profile changed` exit 0 | tests README |
| S10 WireMock | Task 10 / S10 | PASS: Compose all selections, catalog, version projection, hardening (now asserting the loopback binding); isolated Compose rehearsal healthy and hardened; review findings applied; `run-ci-gate.py --profile changed` exit 0; live NOT_RUN | 0092 subject |
| S11 Pact Broker | Task 10 / S11 | PASS: Compose all selections, catalog, version projection, hardening, provisioning and secret-metadata tests; isolated rehearsal (auth, publish, secret hygiene, idempotent provisioning); review findings applied; `run-ci-gate.py --profile changed` exit 0; live NOT_RUN | 0093 subject |
| S12 Spark and Iceberg | Task 10 / S12 | PASS: Compose, catalog, hardening, version projection, metadata check-changed, provisioning and secret tests; isolated catalog and Spark round trip with the scoped identity; SeaweedFS rehearsal 8/8; review findings applied; `run-ci-gate.py --profile changed` exit 0; live NOT_RUN | 0094 subject |
| S14 Flink | Task 10 / S14 | PASS (source): Compose, catalog, hardening (with a negative), version projection, secret-metadata tests; isolated batch and checkpointed streaming inserts; SeaweedFS rehearsal 10/10; live NOT_RUN | 0094 subject |
| S15 Great Expectations | Task 10 / S15 | PASS (source): Compose, catalog, hardening (with a negative), version projection, links, metadata; isolated pass then exit `1` on a duplicate key; exit `2` error paths; live NOT_RUN | 0094 subject |
| S16 Superset | Task 10 / S16 | PASS (source): Compose, catalog, hardening (with a negative), projection, links, metadata, feature-job and secret-metadata tests; isolated provisioning, idempotent init, health, `401`, OIDC option, no credential in env; PostgreSQL rehearsal 6/6; live NOT_RUN | 0097 subject |
| S17 Stalwart | Task 10 / S17 | PASS (source): Compose (`mail-server`, `dev`), catalog, hardening, projection, links, metadata, network and secret-metadata tests; rehearsal: four listeners after restart, relay refused, idempotent plan, no secret in logs; live NOT_RUN | 0070 subject |
| S18 route authentication | Task 10 / S18 | PASS (source): route contract test (with a negative), Compose, catalog, hardening, links, metadata; four open routes closed; live NOT_RUN | GDE/POL-0079 |
| S19 convergence | Task 10 / S19 | PASS (source): AD-0009 profile drift closed; template ledger no gap; removals held for live acceptance; live list consolidated | this Task |
| Offsite recovery | Task 10 / S03 | NOT_RUN: no offsite target (owner) | POL-0021 control 1 |

## Review Evidence

Completion approval (2026-09-24): two independent read-only reviews of the Spec,
Plan and Tasks ran before approval, one on specification and traceability and
one on evidence honesty and security. Both returned APPROVE WITH FIXES; every
finding was fixed in #252. The owner then approved the Spec and Plan.

Each stage from S12 on was reviewed by an independent read-only reviewer
before its PR; the findings and their dispositions are in the stage sections
above (S12, S13, S14, S15, S16). S17 was merged before its review returned;
its findings go in a follow-up. Earlier stages (S00–S11) record their review
in their own sections.

## Commit Ledger

Branch `refactor/spec-0180-platform-convergence` from `1ac49fd35`.

| PR | Scope | State |
| --- | --- | --- |
| #191 | S00–S03 | merged |
| #192 | pre-commit repair, pgBackRest `archive-push` log level | merged |
| #193 | backup size measurement through a read-only container | merged |
| #194 | S03 live activation evidence | merged |
| #195 | S04 `seaweedfs-mount` removal | merged |
| #196 | S05 phase 1 networks | merged |
| #197 | S06 SeaweedFS durable and authenticated | merged |
| #198 | OpenBao repair and S06 HOME activation evidence | merged |
| #199 | backup timer installation evidence | merged |
| #200 | S07a consumer switch | merged |
| #201 | S07a live cutover evidence | merged |
| #202 | S07b MinIO removal | merged |
| #205 | S07b live cleanup evidence | merged |
| #206 | S08 Vault removal | merged |
| #207 | S05 phase 2 `infra_net` removal | merged |
| #208 | S05 phase 2 live evidence | merged |
| #209 | S09 Testcontainers | merged |
| #210 | S10 WireMock | merged |
| #211 | S10/S11 CI finding (TypeScript pin) | merged |
| #214 | S11 Pact Broker | merged |
| #215 | S12 Spark and Iceberg | merged |
| #216 | S12 pre-commit fixes | merged |
| #217 | k8s routes handed to hy-home.k8s | merged |
| #218 | k3d removal | merged |
| #219 | Conftest | merged |
| #220 | inventory projection of the Traefik bind address | merged |
| #221 | test count and `renovate.json` newline | merged |
| #222 | Prometheus API for hy-home.k8s | merged |
| #223 | S13 Trino | merged |
| #224 | OpenBao k8s policies, runbook and secret tooling | merged |
| #225 | OpenBao k8s commands as run | merged |
| #226 | `k8s-bootstrap` token two-hour cap | merged |
| #227 | OpenBao k8s setup procedure | merged |
| #228 | hy-home.k8s integration runbook | merged |
| #229 | Prometheus API credential through OpenBao | merged |
| #230 | POL-0096 link fix | merged |
| #231 | Kiali Grafana token through OpenBao | merged |
| #232 | S14 Flink | merged |
| #233 | S15 Great Expectations | merged |
| #234 | S16 Superset | merged |
| #235 | S17 Stalwart | merged |
| #236 | Task ledger and stale evidence corrections | merged |
| #237 | S18 route authentication and S17 review follow-ups | merged |
| #238 | S18 independent review fixes (#237 merged before the review returned) | merged |
| #239 | S19 convergence and the four owner auth decisions | merged |
| #240 | `k3s-ingress` removal and the S19 review fixes (#239 merged before both) | merged |
| #241 | S19 live apply and the OAuth2 Proxy Keycloak route fix | merged |
| #242 | S19 live close: owner login and private registry repair | merged |
| #243 | Private secret registry mirrors the public one except values | merged |
| #244 | Multi-line secret files stay out of the registry; remaining live activation | merged |
| #245 | Real-lineage identity tests pinned to a fixed commit (CI bound) | merged |
| #246 | ksqlDB and StarRocks removal; Superset live record | merged |
| #247 | RUN-0096 snapshot custody | merged |
| #249 | ADR-0039/0040 proposed; REQ-0005 restated | merged |
| #248 | Alloy HOME OTLP receiver forwarding traces to Tempo | merged |
| #250 | ADR-0039/0040 accepted; ADR-0015/0019 superseded; ruff format fix | merged |
| #251 | Alloy OTLP live record | merged |
| #252 | SPEC-0180 to review, SPEC-0181 draft, review fixes | merged |
| this PR | SPEC-0180 Spec and Plan approved | open |

## Rulings

| Decision | Basis | What could be wrong / cost |
| --- | --- | --- |
| Use the SeaweedFS built-in Iceberg REST catalog first | Present in 4.47; no extra service; one recovery set with the filer | Engine incompatibility; fallback is one external REST catalog chosen in S12 |
| Embedded filer store on a persistent volume | Avoids a PostgreSQL dependency cycle for backups | Metadata backup needs `filer.meta.backup` or a quiesced copy |
| Restic and pgBackRest on the other physical disk | Owner answer; no offsite target exists | Same-host loss destroys both copies; offsite stays open |
| Great Expectations in `04-data/lakehouse` on `object_net`, not `09-tooling` on `lakehouse_net` (S01) | It is a Trino client under the lakehouse subject like the other engines, and `lakehouse_net` was never created (S12–S14 use `object_net`) | A later `lakehouse_net` split moves every lakehouse leaf together |
| Remove `mng-pg` from `k3d-hyhome` | No k8s consumer names it | An unrecorded k8s client loses access; re-adding is one line |

## Deferred Items

Closure (2026-09-24): the open items below, the Terrakube and RUN-0096 rows of the live list and the offsite and PITR gaps in Verification Evidence move to [SPEC-0181](../../0181-home-residual-operations/spec.md). Struck items are closed here. The Alloy log gap is lost history, accepted as a residual in the Spec's completion basis.

- ~~CI `validation-changed` fails on every PR: the identity scan exceeds its 64 MiB bound (first seen on #243).~~ Closed 2026-09-24: only the two real-lineage unit tests scanned from the approved baseline to a moving HEAD; the gate itself scans the PR's own merges. The tests now run on a detached checkout of a fixed commit (#245): 23.2 MiB and 20 s, constant.

- ~~Private `secrets/SENSITIVE_ENV_VARS.md` SEC-003 row split across lines, blocking `--sync-metadata` (owner).~~ Closed 2026-09-24: restored to the public placeholder and synced (S19 live apply). It has broken this way twice; keep unseal shares only in their file.

- Prometheus scrapes Qdrant with the full API key; a `QDRANT__SERVICE__READ_ONLY_API_KEY` secret would be least privilege (Qdrant owner).

- Open WebUI sets `VECTOR_DB_URL` without `VECTOR_DB`, so the value is unused and Qdrant is not its store. Remove the key or select Qdrant with the API key (Open WebUI owner).

- ~~File-provider router `k3s-ingress` forwards `*.k8s.` hosts to the native k3s NodePort with no gateway authentication (owner).~~ Closed 2026-09-24: removed in S19 on the owner's decision.
- ~~`test_compose_baseline_gates.py` has pre-existing `ruff format` drift and one `PLW1510` (`subprocess.run` without `check`, S16 Superset rehearsal); CI does not run ruff (test owner).~~ Closed 2026-09-24: CI does run `ruff format` on changed-Python PRs (#249 failed on it); the test file, `superset_config.py` and `hyhome-gx.py` are formatted and the call has `check=False`.

- ~~Private registry `SEC-003` row spans three lines, so `gen-secrets.sh` metadata sync and generation refuse or would rewrite it (owner).~~ Closed 2026-09-23: the row was replaced by the example placeholder after a private equality check (secret cleanup section).
- Retained MinIO data volume `hy-home-infra_minio-data` (176.8 MB) is not backed up and has no scheduled disposal date (owner).

- OpenBao metrics token expires 2026-10-22: nothing alerts before expiry (the 13:55 token lapsed unnoticed). Add an expiry alert or rotate on a schedule (OpenBao subject owner).
- ~~Prometheus k8s NodePort targets on `172.18.0.2`~~ closed by the k3d removal: the jobs are gone.

- n8n queue configuration points at `redis://mng-n8n-valkey`, a name no service declares (found in S05 review; n8n stage owner).

- `mng-pg` rebuild to apply the quieter `archive-push` log level (next approved recreate).

- Single-file config bind mounts keep the original inode, so a host edit never reaches the container. The stale Prometheus `minio` target this produced cleared with the S05 phase 2 recreate; every other single-file config mount drifts the same way (observability owner).
- ~~Orphan secret file `secrets/storage/mlflow_s3_password.txt` (STRG-005/006 were removed in S07a); delete with the next secret review (owner).~~ Closed 2026-09-23: quarantined in `secrets/.retired/2026-09-23/`.
- SeaweedFS has no Prometheus scrape job or alerts; MinIO's were removed with it. Add S3 `-metricsPort` on a network Prometheus reaches, a job and down/capacity alerts (observability owner).
- `secrets/storage/minio_*.txt` stay on disk after removal; delete them with the MinIO data disposition (owner).

- ~~Identity transition scan grows about 0.25 MiB per merged fork against its 64 MiB budget (48.5 MiB after the S07b blob cache); bound the per-fork tree grep before it is reached again (governance tooling owner).~~ Closed 2026-09-24 with the pinned-lineage tests above.
- `examples/operations/compose-core-readiness/` keeps `INFRA_SUBNET`/`INFRA_GATEWAY` and its own Vault rig; restate the example or declare it intentionally generic (owner).
- OpenBao Agent has no SecretID after the S05 phase 2 recreate: a SecretID is single-use and the Agent deletes its file after reading it, so every Agent restart needs a fresh one delivered through the RUN-0085 protected channel. Until then the Agent logs `no known secret ID` and renders nothing new (owner).
- Every OpenBao restart costs an unseal ceremony and an Agent SecretID delivery, and this has now interrupted two approved recreates. Decide whether that stays manual or moves to an auto-unseal seal (OpenBao subject owner).
- Alloy shipped logs for only 6 of 56 containers between the S05 phase 1 live apply (2026-09-22) and the phase 2 live apply; those container logs are lost for that window.
- Offsite backup destination (owner).
- The runtime-version check reads SMTP enhanced status codes (for example the relay refusal) as version pins; narrow its pattern or allow a status-code context (governance tooling owner).
- ~~Alloy HOME config has no OTLP receiver while `4317/4318` stay published; add one when hy-home.k8s sends traces or logs over OTLP (observability owner).~~ Closed 2026-09-24: #248 added the receiver (traces to `tempo:4317`); `infra-alloy` was recreated on owner approval and is healthy, both receivers listen, and a smoke span sent to `192.168.0.13:4318` was found in Tempo. hy-home.k8s traces arrive after that repository restarts its `apps` and `ingress-nginx` pods (k8s side).
- ~~`hy-home.k8s` External Secrets store: after the k3d removal no Compose service is reachable from the cluster, so the store needs another route to OpenBao or its own secret source (other repository).~~ Closed 2026-09-23: the cluster reaches OpenBao through the host route in the hy-home.k8s integration runbook (RUN-0096), with Kubernetes auth and the `eso-read-platform` role.
- Preserved Vault data (`${DEFAULT_SECURITY_DIR}/vault`, 40 KB, still in the Restic state set), `secrets/security/vault_token.txt` and `vault_unseal_keys.legacy.txt` disposition (owner approval).
- `examples/operations/compose-core-readiness/` still demonstrates a Vault-based readiness rig; restate it on OpenBao or declare it intentionally generic (owner).
