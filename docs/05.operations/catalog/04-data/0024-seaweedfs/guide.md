---
title: "SeaweedFS Usage Guide"
version: "1.0.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "GDE-0024"
parent_ids:
- "POL-0024"
implementation_services:
  infra/04-data/lake-and-object/seaweedfs/docker-compose.yml:
  - 'seaweedfs-filer'
  - 'seaweedfs-master'
  - 'seaweedfs-mount'
  - 'seaweedfs-s3'
  - 'seaweedfs-volume'
created: "2026-05-10"
---

# SeaweedFS Usage Guide

## Usage

SeaweedFS is an OPTIONAL master/volume/filer/S3 topology with no proven current
client. It is retained for a named file/object-storage experiment and is not the
HOME MinIO replacement. The FUSE mount is a separate privileged selector.

## Current implementation

[`infra/04-data/lake-and-object/seaweedfs/docker-compose.yml`](../../../../../infra/04-data/lake-and-object/seaweedfs/docker-compose.yml)
defines `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`
and `seaweedfs-mount`. Profiles `seaweedfs` and `storage-seaweedfs` select the
master, volume, filer and S3 services; `seaweedfs-mount` selects the core services
plus the privileged mount.

`seaweedfs-master-data` and `seaweedfs-volume-data` are Docker-managed volumes.
Filer metadata is not a separate persistent volume in current source. Services
join `infra_net`; S3 routes through the standard gateway chain. No secret,
authentication, transport encryption or mounted `security.toml` is declared.
The mount adds `SYS_ADMIN` and `/dev/fuse`, so it is never implied by ordinary S3
selection.

## Images, configuration and resource controls

The Compose file owns the pinned `chrislusf/seaweedfs` image; repository Renovate
may propose updates and the version projection is derived. Root
`SEAWEEDFS_*_HTTP_PORT` and `SEAWEEDFS_*_GRPC_PORT` keys control the declared
listeners; no credential environment key is present. Master/filer extend
`template-stateful-med`, volume `template-stateful-high`, S3
`template-infra-med`, and mount `template-host-observer-med`; every service except
the mount declares health checks. Flow is master → volume, filer → master/volume,
then S3 or FUSE → filer.

## Static preflight

```bash
docker compose --env-file .env.example --profile seaweedfs config --quiet
docker compose --env-file .env.example --profile seaweedfs config --services
docker compose --env-file .env.example --profile seaweedfs-mount config --quiet
```

Run from the repository root. Activation requires a named client, capacity and
security review, especially for the unauthenticated S3 endpoint and FUSE access.

## Recovery and lifecycle

A usable recovery set coordinates volume data, filer metadata and the master
topology inventory at one accepted write boundary. The local master volume may be
quiesced for rollback evidence, but upstream does not define it as a portable
restore artifact. The official backup page describes
`weed backup` for volume data and `fs.meta.save`/`fs.meta.load` for filer metadata,
and recommends a same-version target; it also describes its procedures as limited.
[RUN-0024](runbook.md) therefore requires an isolated rehearsal and records that
complete recovery remains unverified.

Upgrade or MinIO-migration work needs a separate spec, official release review,
S3/file semantic tests, export/restore proof and rollback. SeaweedFS is Apache-2.0
licensed; mounted clients and images retain their own license obligations.

## Official references

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
