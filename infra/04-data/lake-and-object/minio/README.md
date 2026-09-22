---
title: "MinIO Object Storage"
version: "1.0.2"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
created: "2025-11-12"
---

# MinIO object storage

## Overview

This package defines the repository's HOME and LAB MinIO surfaces.

## Audience

It is intended for operators and maintainers of MinIO-backed object storage.

## Scope

[`docker-compose.yml`](docker-compose.yml) defines HOME `minio` and
`minio-create-buckets` for `storage`, `obs`, `logs`, `tracing`, and `nginx`.
`mlops` and `data-science` select `minio` only as the copy source for the
`mlflow-artifacts` cutover; consumers now use SeaweedFS (SPEC-0180 S07).
[`docker-compose.cluster.yaml`](docker-compose.cluster.yaml) defines LAB
`minio1`–`minio4` for `storage-cluster`. The root project includes both sources.

## Structure

HOME state is `minio-data` at `${DEFAULT_DATA_DIR}/minio/data-1`; LAB members use
separate `data1` through `data4` paths. Root/application identities use
`minio_root_username`, `minio_root_password`, `minio_app_username`, and
`minio_app_user_password`. Services use `infra_net`; API/console routes use
`gateway-standard-chain@file`. Gateway TLS does not prove internal TLS or storage
encryption. The service API/console listen on the Compose-declared internal ports
and are gateway-routed; no direct host `ports` mapping exists. The service checks
its live-health endpoint and bootstrap is a completion job. Configuration is
inline in Compose; no external server configuration file is mounted.

The bootstrap creates `loki-bucket`, `tempo-bucket`, `cdn-bucket`, and
`doc-intel-assets`; only `cdn-bucket` is intentionally public-read.

## How to Work in This Area

```bash
docker compose --env-file .env.example --profile storage config --quiet
docker compose --env-file .env.example --profile storage config --services
docker compose --env-file .env.example --profile storage-cluster config --quiet
```

Run from the repository root. The four-node topology shares one host and is LAB.
Back up through an object-aware mirror/replication plus bucket policies, IAM,
versioning and object metadata to a separate encrypted target; do not raw-copy
active `/data`. Restore into an isolated compatible target and validate every
named client before cutover.

The [community repository](https://github.com/minio/minio) was archived and says
it is no longer maintained. Preserve current HOME data while a separate migration
evaluation reviews compatibility and licensing.

## Related Documents

Use the
[documentation entry point](../../../../docs/README.md) to locate Stage 05 subject
`04-data/0023-minio` and POL-0021.
