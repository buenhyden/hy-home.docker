---
title: "SeaweedFS Usage Guide"
version: "1.5.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-25"
layer: "operations"
artifact_id: "GDE-0024"
parent_ids:
- "POL-0024"
implementation_services:
  infra/04-data/lake-and-object/seaweedfs/docker-compose.yml:
  - 'seaweedfs-buckets'
  - 'seaweedfs-filer'
  - 'seaweedfs-master'
  - 'seaweedfs-s3'
  - 'seaweedfs-volume'
created: "2026-05-10"
---

# SeaweedFS Usage Guide

## Usage

SeaweedFS is the S3 object store; it replaced MinIO in SPEC-0180 S07. It is part of HOME through the consumer profiles. S3 at
`http://seaweedfs-s3:8333` (path-style, region `us-east-1`) is the only
interface. The privileged FUSE mount was removed in S04, and the master and
filer have no route.

### Current implementation

[`infra/04-data/lake-and-object/seaweedfs/docker-compose.yml`](../../../infra/04-data/lake-and-object/seaweedfs/docker-compose.yml)
defines `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer` and
`seaweedfs-s3`. Profiles `seaweedfs` and `storage-seaweedfs` select all four.
Each starts through
[`config/hyhome-seaweedfs.sh`](../../../infra/04-data/lake-and-object/seaweedfs/config/hyhome-seaweedfs.sh)
as UID 1000. The script builds `security.toml` (volume and filer JWT keys, gRPC
mTLS) and, for S3, the identities file from Docker secrets. It refuses to start
when a secret or certificate is missing.

State is on the data disk: `${DEFAULT_DATA_DIR}/seaweedfs/master`, `/volume`
and `/filer` (the embedded leveldb2 store). Master, volume and filer are only
on `seaweed_internal`. S3 also joins `object_net` for clients and `edge_net`
for the `s3.${DEFAULT_URL}` route.

Only S3 serves Prometheus metrics (`-metricsPort=9327`); Prometheus scrapes
`seaweedfs-s3:9327` over `edge_net` as job `seaweedfs-s3`. Master, volume and
filer stay unscraped on the internal network. Alerts: `SeaweedFSS3Down`
(target down 2m) and `SeaweedFSDataDiskLow` (data-disk filesystem under 15%
free for 10m, from node-exporter).

### Consumers, buckets and migration

| Consumer | Bucket | Identity (access key ID) | Secret |
| --- | --- | --- | --- |
| Loki | `loki-bucket` | `loki` | STRG-011 |
| Tempo | `tempo-bucket` | `tempo` | STRG-012 |
| MLflow | `mlflow-artifacts` | `mlflow` | STRG-013 |
| Terrakube | `tfstate` | `terrakube` | STRG-014 |
| Spark (Iceberg) | `lakehouse` table bucket | `lakehouse` | STRG-015 |
| Nginx `/cdn/` | `cdn-bucket` | `anonymous` (object reads only) | none |

`seaweedfs-buckets` (aws-cli, admin identity) creates the five buckets and,
under `lakehouse` only, `seaweedfs-table-bucket` creates the `lakehouse` table
bucket, its policy and the `dev` and `test` namespaces, all idempotently; every bucket-owning consumer waits for it (Nginx waits for
`seaweedfs-s3` only). The S07 cutover copied each
MinIO bucket through the S3 API and left a `hyhome-migration/<bucket>.cutover`
marker object; the copy job was removed with MinIO. The retained MinIO data,
volume and image were disposed of on 2026-09-25 (SPEC-0182 W5), which ended
the S07 rollback path.

### Images, configuration and resource controls

The Compose file owns the pinned `chrislusf/seaweedfs` image; Renovate may
propose updates and the version projection is derived. Root
`SEAWEEDFS_*_HTTP_PORT` and `SEAWEEDFS_*_GRPC_PORT` keys control the listeners.
`SEAWEEDFS_S3_ADMIN_ACCESS_KEY` names the admin identity. Its secret key
(STRG-010) and the JWT keys (STRG-008, STRG-009) are secret files, and the gRPC
certificates come from `bin/gen-grpc-certs.sh`. Master and filer extend
`template-stateful-med`, volume `template-stateful-high`, and S3
`template-infra-med`; every service has a health check. The volume server
refuses writes below 20 GiB free. Flow: master → volume, filer →
master/volume, then S3 → filer.

### Static preflight and rehearsal

```bash
docker compose --env-file .env.example --profile seaweedfs config --quiet
HYHOME_SEAWEEDFS_REHEARSAL=1 python3 -m unittest \
  tests.validation.test_compose_baseline_gates.SeaweedfsRehearsalTests
```

Run these from the repository root. The rehearsal needs Docker and uses only
disposable data.

### Verified S3 behaviour (4.47, 2026-09-22 rehearsal)

| Area | Result |
| --- | --- |
| Anonymous PUT/list, wrong secret | 403; `SignatureDoesNotMatch` |
| Filer GET/PUT and volume POST without JWT | 401 |
| gRPC without a client certificate | TLS alert `certificate required` |
| PUT with content type, user metadata and tags; HEAD; tagging read | preserved |
| Range GET, list with prefix, URL-encoded key with space and `+` | correct bytes and key |
| 20 MiB multipart upload | round trip identical; ETag has the `-N` part suffix, so it is not an MD5 |
| Presigned GET | correct bytes |
| Key `a` then `a/b` | both stored and readable with their own bytes |
| Volume server stopped | GET fails instead of returning data |
| Restart; restore of volume and master trees plus `fs.meta.load` into empty stores | objects identical |

Versioning, Object Lock, SSE, notifications and lifecycle rules were not
tested. S07 tests any that a consumer needs before its cutover.

### Recovery and lifecycle

The backup set is the filer metadata export plus the volume and master trees,
taken in that order with vacuum paused ([RUN-0024](../runbooks/0024-seaweedfs.md), RUN-0021).

An image upgrade needs an official release review and a passing rehearsal.
SeaweedFS is Apache-2.0 licensed.

### Official references

- [SeaweedFS data backup](https://github.com/seaweedfs/seaweedfs/wiki/Data-Backup)
- [SeaweedFS security configuration](https://github.com/seaweedfs/seaweedfs/wiki/Security-Configuration)
- [SeaweedFS repository and license](https://github.com/seaweedfs/seaweedfs)

## Common Checks

Confirm exact root profiles, services, health/resource controls, writable-state
ownership, secret references, exposure and the engine-specific recovery boundary.
A static pass is configuration evidence only; runtime and restore remain separate.

## Traceability

- Artifact: `GDE-0024`; governing policy: `POL-0024`.
- Runtime authority: `infra/04-data/lake-and-object/seaweedfs/docker-compose.yml`.

## Related Documents

- [Operations policy](../policies/0024-seaweedfs.md)
- [Health and recovery runbook](../runbooks/0024-seaweedfs.md)
- [Backup policy](../policies/0021-backup-and-restore.md)
