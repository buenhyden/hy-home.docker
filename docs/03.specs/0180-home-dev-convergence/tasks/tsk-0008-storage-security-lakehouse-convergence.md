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

## Verification Evidence

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| S00 inventory and live state | Task 10 / S00 | PASS: four-column state, consumers and requirement trace recorded above | this Task |
| S01 target design | Task 10 / S01 | PASS (design): tree, duplicate rulings, interfaces, networks, order | this Task |

## Review Evidence

Pending: sequential review after each implemented stage.

## Commit Ledger

Branch `refactor/spec-0180-platform-convergence` from `1ac49fd35`.

## Rulings

| Decision | Basis | What could be wrong / cost |
| --- | --- | --- |
| Use the SeaweedFS built-in Iceberg REST catalog first | Present in 4.47; no extra service; one recovery set with the filer | Engine incompatibility; fallback is one external REST catalog chosen in S12 |
| Embedded filer store on a persistent volume | Avoids a PostgreSQL dependency cycle for backups | Metadata backup needs `filer.meta.backup` or a quiesced copy |
| Restic and pgBackRest on the other physical disk | Owner answer; no offsite target exists | Same-host loss destroys both copies; offsite stays open |
| Remove `mng-pg` from `k3d-hyhome` | No k8s consumer names it | An unrecorded k8s client loses access; re-adding is one line |

## Deferred Items

- Offsite backup destination (owner).
- `hy-home.k8s` External Secrets store repoint from Vault `.8` to OpenBao (other repository).
- Legacy Vault data (`vault/data`, 28 KB) and `vault_unseal_keys.legacy.txt` disposition (owner approval).
