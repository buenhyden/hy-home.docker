---
title: "Storage, Secret Custody, Network and Lakehouse Convergence"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-22"
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

## Verification Evidence

| Acceptance criterion | Plan work unit | Task result | Durable owner |
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
| S03 timer | Task 10 / S03 | PASS (install): owner installed the units on 2026-09-22; `hyhome-backup.timer` enabled and active, installed units byte-identical to source, first run scheduled 2026-09-23 03:58 KST; first timer-driven run NOT_RUN yet | RUN-0021 step 3 |
| S04 structure | Task 10 / S04 | PASS: `seaweedfs-mount` removed; `seaweedfs` renders master/volume/filer/S3, `seaweedfs-mount` renders nothing; no remaining current reference | this Task |
| S04 accumulated gates | Task 10 / S04 | PASS: Compose 71 selections/314 services, operations catalog, projection (89 repositories), links (942 documents, 0 failures), `git diff --check`; 623 unit tests with 2 local-only failures (group-write bit on two entrypoint scripts from this worktree's umask 002, not tracked by Git; CI unaffected) | this Task |
| S05 phase 1 source | Task 10 / S05 | PASS: 150 services assigned, rendered memberships equal the assignment; every traced flow shares a segmented network (static trace plus review); review Critical/Important findings fixed; Compose 71 selections/314 services; 5/5 `NetworkSegmentationContractTests` | this Task, AD-0026 |
| S05 phase 1 live | Task 10 / S05 | PASS with one open item: 53 services recreated and healthy, SSO and forwarded headers verified; OpenBao sealed until the owner unseals | this Task |
| S06 source and rehearsal | Task 10 / S06 | PASS: 6/6 `SeaweedfsRehearsalTests`, 2/2 `SeaweedfsContractTests`, secret registry 110 rows (STRG-007–010) | GDE/POL/RUN-0024 |
| S06 HOME activation | Task 10 / S06 | PASS: healthy, anonymous refused, admin bucket round trip, only S3 routed, isolated internals, SeaweedFS set in the Restic snapshot; registry Value cells pending the owner's `SEC-003` repair | RUN-0024 |
| Offsite recovery | Task 10 / S03 | NOT_RUN: no offsite target (owner) | POL-0021 control 1 |

## Review Evidence

Pending: sequential review after each implemented stage.

## Commit Ledger

Branch `refactor/spec-0180-platform-convergence` from `1ac49fd35`.

| PR | Scope | State |
| --- | --- | --- |
| #191 | S00–S03 | merged |
| #192 | pre-commit repair, pgBackRest `archive-push` log level | merged |
| #193 | backup size measurement through a read-only container | merged |
| #194 | S03 live activation evidence | merged |
| this PR | S04 `seaweedfs-mount` removal | open |

## Rulings

| Decision | Basis | What could be wrong / cost |
| --- | --- | --- |
| Use the SeaweedFS built-in Iceberg REST catalog first | Present in 4.47; no extra service; one recovery set with the filer | Engine incompatibility; fallback is one external REST catalog chosen in S12 |
| Embedded filer store on a persistent volume | Avoids a PostgreSQL dependency cycle for backups | Metadata backup needs `filer.meta.backup` or a quiesced copy |
| Restic and pgBackRest on the other physical disk | Owner answer; no offsite target exists | Same-host loss destroys both copies; offsite stays open |
| Remove `mng-pg` from `k3d-hyhome` | No k8s consumer names it | An unrecorded k8s client loses access; re-adding is one line |

## Deferred Items

- Private registry `SEC-003` row spans three lines, so `gen-secrets.sh` metadata sync and generation refuse or would rewrite it (owner).
- Retained MinIO data volume `hy-home-infra_minio-data` (176.8 MB) is not backed up and has no scheduled disposal date (owner).

- OpenBao metrics token expires 2026-10-22: nothing alerts before expiry (the 13:55 token lapsed unnoticed). Add an expiry alert or rotate on a schedule (OpenBao subject owner).
- Prometheus k8s NodePort targets on `172.18.0.2` refuse connections; `.2` is Traefik's k3d address (observability owner).

- n8n queue configuration points at `redis://mng-n8n-valkey`, a name no service declares (found in S05 review; n8n stage owner).

- `mng-pg` rebuild to apply the quieter `archive-push` log level (next approved recreate).

- Prometheus still scrapes a `minio` target: its config is a single-file bind mount holding a replaced inode, so only a recreate clears it (next approved recreate). Single-file config mounts drift the same way for every service.
- Orphan secret file `secrets/storage/mlflow_s3_password.txt` (STRG-005/006 were removed in S07a); delete with the next secret review (owner).
- SeaweedFS has no Prometheus scrape job or alerts; MinIO's were removed with it. Add S3 `-metricsPort` on a network Prometheus reaches, a job and down/capacity alerts (observability owner).
- `secrets/storage/minio_*.txt` stay on disk after removal; delete them with the MinIO data disposition (owner).

- Identity transition scan grows about 0.25 MiB per merged fork against its 64 MiB budget (48.5 MiB after the S07b blob cache); bound the per-fork tree grep before it is reached again (governance tooling owner).
- `examples/operations/compose-core-readiness/` keeps `INFRA_SUBNET`/`INFRA_GATEWAY` and its own Vault rig; restate the example or declare it intentionally generic (owner).
- Alloy shipped logs for only 6 of 56 containers between the S05 phase 1 live apply (2026-09-22) and the phase 2 live apply; those container logs are lost for that window.
- Offsite backup destination (owner).
- `hy-home.k8s` External Secrets store repoint from Vault `.8` to OpenBao (other repository).
- Preserved Vault data (`${DEFAULT_SECURITY_DIR}/vault`, 40 KB, still in the Restic state set), `secrets/security/vault_token.txt` and `vault_unseal_keys.legacy.txt` disposition (owner approval).
- `examples/operations/compose-core-readiness/` still demonstrates a Vault-based readiness rig; restate it on OpenBao or declare it intentionally generic (owner).
