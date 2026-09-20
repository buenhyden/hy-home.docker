---
title: "SeaweedFS"
version: "1.0.2"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
created: "2025-12-06"
---

# SeaweedFS

## Overview

This package defines the repository's optional SeaweedFS surface.

## Audience

It is intended for operators and maintainers evaluating SeaweedFS.

## Scope

[`docker-compose.yml`](docker-compose.yml) defines `seaweedfs-master`,
`seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, and `seaweedfs-mount`.
Profiles `seaweedfs` and `storage-seaweedfs` select core plus S3;
`seaweedfs-mount` additionally selects the privileged FUSE mount.

## Structure

Master and volume state use `seaweedfs-master-data` and
`seaweedfs-volume-data`. Services join `infra_net`; the S3 route uses the standard
gateway chain. Current source declares no secret, internal authentication/TLS or
mounted security configuration. The mount adds `SYS_ADMIN` and `/dev/fuse` and
therefore needs explicit host-capability approval. Master, volume, filer and S3
expose only their declared internal HTTP/gRPC ports; no host `ports` mapping is
declared. Each core/S3 service has an HTTP health check, while the privileged mount
has no health check. Commands/configuration are inline; `security.toml.example` is
not mounted.

## How to Work in This Area

```bash
docker compose --env-file .env.example --profile seaweedfs config --quiet
docker compose --env-file .env.example --profile seaweedfs config --services
docker compose --env-file .env.example --profile seaweedfs-mount config --quiet
```

SeaweedFS remains OPTIONAL and is not an automatic MinIO replacement. Recovery
must coordinate engine-aware volume backup, filer metadata and quiesced
master/topology state at one point, then validate on a same-version isolated
target. The official backup page describes limitations, so recovery remains
unverified until rehearsal.

## Related Documents

Use the [documentation entry point](../../../../docs/README.md) to locate Stage 05
subject `04-data/0024-seaweedfs` and POL-0021. Official sources:
[data backup](https://github.com/seaweedfs/seaweedfs/wiki/Data-Backup),
[security](https://github.com/seaweedfs/seaweedfs/wiki/Security-Configuration), and
[license](https://github.com/seaweedfs/seaweedfs/blob/master/LICENSE).
