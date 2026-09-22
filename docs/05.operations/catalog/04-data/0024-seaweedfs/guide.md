---
title: "SeaweedFS Usage Guide"
version: "1.2.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
layer: "operations"
artifact_id: "GDE-0024"
parent_ids:
- "POL-0024"
implementation_services:
  infra/04-data/lake-and-object/seaweedfs/docker-compose.yml:
  - 'seaweedfs-filer'
  - 'seaweedfs-master'
  - 'seaweedfs-s3'
  - 'seaweedfs-volume'
created: "2026-05-10"
---

# SeaweedFS Usage Guide

## Usage

SeaweedFS is the S3 object store that takes over from MinIO one consumer at a
time in SPEC-0180 S07. Until then it stays OPTIONAL. S3 at
`http://seaweedfs-s3:8333` (path-style, region `us-east-1`) is the only
interface. The privileged FUSE mount was removed in S04, and the master and
filer have no route.

### Current implementation

[`infra/04-data/lake-and-object/seaweedfs/docker-compose.yml`](../../../../../infra/04-data/lake-and-object/seaweedfs/docker-compose.yml)
defines `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer` and
`seaweedfs-s3`. Profiles `seaweedfs` and `storage-seaweedfs` select all four.
Each starts through
[`config/hyhome-seaweedfs.sh`](../../../../../infra/04-data/lake-and-object/seaweedfs/config/hyhome-seaweedfs.sh)
as UID 1000. The script builds `security.toml` (volume and filer JWT keys, gRPC
mTLS) and, for S3, the identities file from Docker secrets. It refuses to start
when a secret or certificate is missing.

State is on the data disk: `${DEFAULT_DATA_DIR}/seaweedfs/master`, `/volume`
and `/filer` (the embedded leveldb2 store). Master, volume and filer are only
on `seaweed_internal`. S3 also joins `object_net` for clients and `edge_net`
for the `s3.${DEFAULT_URL}` route.

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
taken in that order with vacuum paused ([RUN-0024](runbook.md), RUN-0021).

An image upgrade needs an official release review and a passing rehearsal.
Consumer cutover from MinIO is S07, one consumer at a time. SeaweedFS is
Apache-2.0 licensed.

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

- [Operations policy](policy.md)
- [Health and recovery runbook](runbook.md)
- [Backup policy](../0021-backup-and-restore/policy.md)
