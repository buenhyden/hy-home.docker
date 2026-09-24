---
title: "Runtime and Legacy Data"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-25"
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

Pending.

## Verification Evidence

Pending.

## Review Evidence

Pending.

## Commit Ledger

No PR yet.

## Rulings

See the Plan.

## Deferred Items

None yet.
