---
title: "Runtime and Legacy Data"
version: "0.4.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-26"
layer: "specs"
artifact_id: "SPEC-0182-TSK-0002"
parent_ids:
- "SPEC-0182"
- "SPEC-0182-PLAN-0001"
created: "2026-09-25"
---

# Runtime and Legacy Data

## Objective

Carry out W3–W6 of the [Plan](../plan.md) in approved windows.

## Inputs

Read-only investigation of 2026-09-25:

- **`mng-pg`:** the quieter `[global:archive-push] log-level-console=warn` is
  in source (`infra/04-data/operational/mng-db/pg/backup/pgbackrest.conf:21-22`,
  commit `4b8d06011`) but the running image predates it; the file is baked in
  by `COPY`. About 24 `archive-push` lines per hour. Procedure: RUN-0021 step
  2.
- **Single-file mounts:** 21 repository configuration files are mounted as
  single files into 18 running containers; five differ from the host by
  SHA-256: Superset `superset_config.py`, Kafbat UI
  `dynamic_config.template.yaml`, and `hyhome-seaweedfs.sh` in the SeaweedFS
  master, volume and filer. Pyroscope has no shell to check.
- **Legacy data:** MinIO directory `…/volumes/data/minio/data-1` (177M) behind
  volume `hy-home-infra_minio-data`, unused and outside Restic; the Vault tree
  `…/volumes/security/vault` (sparse `vault.db`, `raft/` owned by the
  container UID), still in `infra/09-tooling/restic/sets/state-include.txt:20-21`;
  quarantined files in `secrets/.retired/2026-09-23/` (four MinIO files,
  `mlflow_s3_password.txt`, `tools/terrakube_minio_secret_key.txt`,
  `vault_token.txt`, `vault_unseal_keys.legacy.txt`); images
  `quay.io/minio/minio` (241MB) and `hashicorp/vault:2.1.1` (740MB). No
  step-by-step disposal procedure exists; RUN-0024:61, RUN-0085:52-53,
  POL-0021:44 and `secrets/README.md:116-121` only require approval.
- **Outside HOME:** HOME (POL-0078:125-129) renders 40 services; 23 more
  `hy-home-infra` containers run (crawl4ai, dcgm-exporter, dozzle, pyroscope,
  tempo, jupyterlab, the Kafka and CDC set, mailpit, mlflow, open_notebook,
  surrealdb, pact-broker, pushgateway, redisinsight, registry, stalwart,
  superset, wiremock); `kafka-2` and `kafka-3` are Created; five `k3d-hyhome-*`
  containers belong to hy-home.k8s.

## Work Log

- 2026-09-25 W6: rendered HOME was 40 services (37 plus three one-shot
  init jobs). The running `hy-home-infra` containers outside it and the
  owner's decision for each:

  | Containers | Profile | Consumers and stop risk | Owner decision |
  | --- | --- | --- | --- |
  | `tempo`, `pyroscope`, `dcgm-exporter` | `tracing`, `profiling`, `obs-gpu` | HOME Alloy, Traefik and Grafana send traces and profiles; Prometheus scrapes GPU metrics. Stopping them breaks exports and datasources | Added to HOME |
  | `registry` | `tooling`, `registry` | Development image registry | Added to HOME for default use |
  | `kafka-1`, `kafka-connect`, `schema-registry`, `kafka-exporter`, `mlflow`, `jupyterlab` | `cdc`, `messaging`, `mlops`, `data-science` | W7 restore subjects; `hyhome_app_slot` on `mng-pg` active, lag 664 kB; stopping Connect with the slot kept grows WAL | Kept until W7, then decided again |
  | `dozzle`, `redisinsight`, `kafbat-ui`, `kafka-rest-proxy` | `admin`, `messaging-admin`, `messaging-rest` | Operator UIs; no configured consumers | Kept outside HOME for operator use |
  | `wiremock`, `pact-broker`, `mailpit`, `crawl4ai`, `open_notebook`, `surrealdb`, `superset`, `stalwart`, `pushgateway` | `api-mock`, `contract-testing`, `mail-dev`, `crawl4ai`, `notebook`, `bi`, `mail-server`, `batch-metrics` | No configured consumers; none is a scrape target; Alertmanager mails through its own smarthost | Stopped (`docker stop`; restart policy `unless-stopped`, so they stay stopped) |

  `kafka-2` and `kafka-3` stay Created and the exited init, provision, Flink
  and Trino containers stay exited. POL-0078, the root and infra READMEs,
  POL-0006 and AD-0031 now name HOME with `tracing profiling obs-gpu
  registry`; each adds only its own service, so HOME renders 44 (41 plus the
  three init jobs).

- 2026-09-25 W4: the recreate-on-edit rule went into POL-0006 and
  `scripts/operations/check-config-mount-hashes.py` reads each single-file
  mount through `docker exec … cat`. `docker cp` was rejected: the daemon
  resolves a bind mount to the fresh host file, so it reported every stale
  mount as a match (on `kafbat-ui` the container still held the old inode,
  2738 bytes against 2689 on the host). A read-only run found 14 match,
  4 diff (`kafbat-ui`; `hyhome-seaweedfs.sh` in SeaweedFS master, volume and
  filer) and Pyroscope unreadable (no shell). With the owner's approval, and
  16 hours before `hyhome-backup.timer`, the agent recreated `kafbat-ui`,
  then `seaweedfs-master`, `seaweedfs-volume` and `seaweedfs-filer`, each
  after the previous was healthy, then `pyroscope`.

- 2026-09-25 W3: with the owner's approval, RUN-0021 step 2. Preconditions:
  stanza `mng` status ok, last full backup `20260922-073354F`, 29G free under
  the state directory, cluster 118 MB. A `pg_dumpall` went to a `0600` file
  under `umask 077` (2.7 MB, dump-complete trailer present); the running image
  was tagged `hy-home/mng-pg:pre-0182` (`sha256:1a3e1b08…`). The rebuilt
  image (`sha256:0abb5ce5…`) carries the `archive-push` console level; `mng-pg`
  was recreated at 02:44:28Z and healthy at 02:44:51Z. The dump was deleted
  after verification.

- 2026-09-25 W5: preconditions met: the cutover markers for `cdn-bucket`,
  `loki-bucket`, `mlflow-artifacts` and `tempo-bucket` exist in
  `/buckets/hyhome-migration/`; MLflow holds the same two artifact keys in
  MinIO and SeaweedFS; MinIO `doc-intel-assets` was empty. Final inventory
  through a read-only `alpine:3` container: MinIO `data-1` 2059 files,
  180381162 bytes, tree hash prefix `560a8f1091d1f7dd`; Vault tree 2 files,
  33628160 bytes, prefix `454cb71757d257bd`. Credential files by name, size,
  mode and date: the four `storage/minio_*` files (10 or 16 bytes, `0640`,
  2026-09-23), `storage/mlflow_s3_password.txt` (16, `0640`, 2026-09-21),
  `tools/terrakube_minio_secret_key.txt` (16, `0600`, 2026-03-19),
  `security/vault_token.txt` (29, `0600`, 2026-03-23),
  `security/vault_unseal_keys.legacy.txt` (295, `0600`, 2026-03-23) and
  `secrets/.backup-20260923/` (`.env` 14939 and `SENSITIVE_ENV_VARS.md` 20855,
  `0600`). #271 removed the `security/vault` Restic include and corrected
  RUN-0024, RUN-0035, RUN-0085, POL-0021 and `secrets/README.md`; after it
  merged the owner ran the six approved disposal commands: volume
  `hy-home-infra_minio-data`, the MinIO directory and the Vault tree (both
  through a root container), the eight quarantined files,
  `secrets/.backup-20260923/` and images `hashicorp/vault` and
  `quay.io/minio/minio`. The SPEC-0180 S07 rollback path has ended and the
  legacy Vault root token is moot.

## Verification Evidence

- W5 disposal: volume absent from `docker volume ls`; `minio/data-1` and
  `security/vault` absent (only `openbao` remains under `security/`); 0 of the
  8 targeted files remain and the other 6 quarantined files are kept;
  `secrets/.backup-20260923/` absent; neither image listed. The first Restic
  snapshot without the Vault tree is taken by `hyhome-backup.timer` on
  2026-09-26 03:45 KST and is checked then.
- W3: `pgbackrest --stanza=mng check` completed successfully;
  `archive_mode` on; after a forced WAL switch `pg_stat_archiver` shows
  `00000001000000030000005F` archived with 0 failures and no `archive-push`
  line in the container log. CDC connector `hyhome-app-postgres` and its task
  `RUNNING`; `hyhome_app_slot` active with `wal_status` `reserved`. Keycloak,
  n8n, n8n-worker, the Airflow services, Flower, MLflow and `mng-pg-exporter`
  healthy; Keycloak logged 3 errors during the restart and none after
  02:46Z. Hash check: match 18, diff 0.
- W4 hash check after the recreates (`--root` the main checkout): match 18,
  diff 0; Pyroscope unreadable by design, and fresh by construction since it
  was recreated at 02:30:46Z against a file last changed on 2026-09-16.
- W4 SeaweedFS: Loki and Tempo each logged one flush error at 02:30:17Z and
  02:30:22Z while the filer restarted (02:30:15Z); both retried, Tempo
  reclaimed the block at 02:32:38Z, and neither logged an error after
  02:31Z. Vacuum is enabled: its disable flag is master memory state and the
  master was recreated; `hyhome-backup.service` was inactive with its last
  run successful.

## Review Evidence

Pending.

## Commit Ledger

| PR | Scope | State |
| --- | --- | --- |
| #268 | W6 container decisions; HOME adds `tracing profiling obs-gpu registry` | merged |
| #270 | W4 hash check, recreate-on-edit rule, recreates; W3 `mng-pg` rebuild | merged |
| #271 | W5 Restic include and document corrections | merged |
| #273 | W5 disposal evidence | merged |

## Rulings

See the Plan.

## Deferred Items

None yet.
