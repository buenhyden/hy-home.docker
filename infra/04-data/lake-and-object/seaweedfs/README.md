---
title: "SeaweedFS"
version: "1.2.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
created: "2025-12-06"
---

# SeaweedFS

## Overview

This package defines SeaweedFS, the S3 object store that replaces MinIO one
consumer at a time (SPEC-0180 S07).

## Audience

It is intended for operators and maintainers of object storage.

## Scope

[`docker-compose.yml`](docker-compose.yml) defines `seaweedfs-master`,
`seaweedfs-volume`, `seaweedfs-filer`, and `seaweedfs-s3`. Profiles
`seaweedfs`, `storage-seaweedfs` and every S3 consumer profile (`storage`,
`obs`, `logs`, `tracing`, `nginx`, `mlops`, `data-science`) select them with
`seaweedfs-buckets`. S3 is the only interface:
the FUSE mount was removed in S04, and master and filer have no route.

## Structure

| Path | Role |
| --- | --- |
| `docker-compose.yml` | four services, data-disk bind volumes, secrets |
| `config/hyhome-seaweedfs.sh` | start script: builds JWT, gRPC mTLS and S3 identity configuration from secrets |
| `config/s3-identities.conf` | bucket-scoped consumer identities (loki, tempo, mlflow, terrakube) and anonymous CDN reads |
| `config/seaweedfs-buckets.sh` | `seaweedfs-buckets` job: idempotent bucket creation with the admin identity |
| `config/seaweedfs-migrate.sh` | `seaweedfs-migrate` job (S07 only): MinIO → SeaweedFS copy with a count and byte check |
| `bin/gen-grpc-certs.sh` | host script: issues the SeaweedFS-only gRPC CA and certificates |

State lives under `${DEFAULT_DATA_DIR}/seaweedfs/{master,volume,filer}`, owned
by UID 1000. Master, volume and filer are only on `seaweed_internal`. S3 also
joins `object_net` for clients and `edge_net` for its route.

## How to Work in This Area

```bash
docker compose --env-file .env.example --profile seaweedfs config --quiet
HYHOME_SEAWEEDFS_REHEARSAL=1 python3 -m unittest \
  tests.validation.test_compose_baseline_gates.SeaweedfsRehearsalTests
```

First activation, backup and restore follow RUN-0024. The daily backup takes
filer metadata and the volume and master trees in one ordered set (RUN-0021).

## Related Documents

Use the [documentation entry point](../../../../docs/README.md) to locate Stage 05
subject `04-data/0024-seaweedfs` and POL-0021. Official sources:
[data backup](https://github.com/seaweedfs/seaweedfs/wiki/Data-Backup),
[security](https://github.com/seaweedfs/seaweedfs/wiki/Security-Configuration), and
[license](https://github.com/seaweedfs/seaweedfs/blob/master/LICENSE).
